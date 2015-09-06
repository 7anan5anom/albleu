# coding: utf-8
'''
    AL-BLEU is the Arabic Language MT automatic evaluator, a modified version of BLEU.
    It uses MADA analysis of the translation and reference. 
    
    Usage:
    python albleu.py <path-to-evaluation-directory>
    
    Input arguments:
    <path-to-evaluation-directory>: must contain: e-hyp (tranlsation),
    e-test (reference), e-hyp.mada, and e-test.mada
    
    Note: MADA analysis files should be created specifically for the
    e-hyp/e-test files, i.e. every line in e-hyp corresponds to a line
    in e-hyp.mada in the same order. Same thing goes for e-test.
    
    Author: Hanan Alshikhabobakr, CMU-Qatar
    Date: March 9th, 2014
    
'''

from __future__ import print_function
import sys, re, codecs, itertools, string, math, os, copy, subprocess, os
home = os.path.dirname(os.path.abspath(__file__))
sys.path.append(home+"/utils/")
from feat_and_stem import *

mainpath = ""
MIN_TAKE = 4 #minimum number of features to match
max_Ngram   = 4 #bleu max n-gram by default
hyp_count   = [0] * max_Ngram
ref_count   = [0] * max_Ngram
match_count=[0.0] * max_Ngram
score =     [0.0] * max_Ngram
indscore =  [0.0] * max_Ngram
hypstemdict = {}
hyp_posdict = {}
refstemdict = {}
ref_posdict = {}

'''
    Finds reference index of a matching stem
'''
def findstem(str,ref_words,temphypdict, temprefdict):
    hypstems = []
    refstems = []
    #get hyp stems
    if str in temphypdict.keys():
        hypstems = temphypdict[str]
    #get stems for all words in ref
    for i,word in enumerate(ref_words):
        if word in temprefdict.keys():
            for stem in temprefdict[word]:
                for hypstem in hypstems:
                    if hypstem == stem:
                        return i
    return -1

'''
    Generates features-tuples n-grams for a given sentence
'''
def generate_feature_ngrams(words,n,dict):
    length = len(words)
    array = {}
    #check for stem existence
    for i in range(length-n+1):
        templist = words[i:i+n]
        ngram = []
        for t in templist:
            if t in dict.keys():
                if len(dict[t]) > 0:
                    ngram.append(dict[t][0])
        if len(ngram)==n:
            array[i] = (ngram,templist)
    return array

'''
    Generates n-grams for a given sentence
'''
def generate_ngrams(words,n):
    length = len(words)
    array = {}
    for i in range(length-n+1):
        array[i] = " ".join(words[i:i+n])
    return array

'''
    Checks the matching precision feature vectors/tuples and stem
'''
def get_stem_feat_precision(tuple1, tuple2):
    weight = 0.0
    count = 0
    stemin = 0
    if tuple1[0] == tuple2[0] and tuple1[0] != "na":
        count += 1
        weight += POS_COST
    if tuple1[1] == tuple2[1] and tuple1[1] != "na":
        count += 1
        weight += GEN_COST
    if tuple1[2] == tuple2[2] and tuple1[2] != "na":
        count += 1
        weight += NUM_COST
    if tuple1[3] == tuple2[3] and tuple1[3] != "na":
        count += 1
        weight += STT_COST
    if tuple1[4] == tuple2[4] and tuple1[4] != "na":
        count += 1
        weight += PER_COST
    
    if tuple1[5] == tuple2[5] and tuple1[5] != "na":
        count += 1
        stemin = 1
        weight += STEM_COST
    
    return [weight,count]

#Stemming functions
'''
    Generates stemmed n-grams for a given sentence
'''
def generate_stem_ngrams(words,n,stemdict):
    length = len(words)
    array = {}
    #check for stem existence
    
    for i in range(length-n+1):
        templist = words[i:i+n]
        ngram = []
        for t in templist:
            if t in stemdict.keys():
                if len(stemdict[t]) >0:
                    ngram.append(stemdict[t][0])
        if len(ngram)==n:
            array[i] = " ".join(ngram)
    return array

'''
    Takes in a sentence, and its dictionary of stems or POS.
    Returns an array of all possible 2-gram that contains exactly 1 stem/pos.
'''
def bigram_half_stem(words,dict):
    length = len(words)
    array = {}
    for i in range(length-1):
        seg1 = []
        seg2 = []
        stem1 = ""
        stem2 = ""
        
        seg1.append(words[i])
        if words[i] in dict.keys():
            stem = dict[words[i]]
            if len(stem) > 0:
                seg2.append(stem[0])
                stem2 = stem[0]
        
        seg2.append(words[i+1])
        if words[i+1] in dict.keys():
            stem = dict[words[i+1]]
            if len(stem) > 0:
                seg1.append(stem[0])
                stem1 = stem[0]
        
        if len(seg1) == 2:
            array[(i,stem1)] = " ".join(seg1) #add a tuple
        if len(seg2) == 2:
            array[(i,stem2)] = " ".join(seg2)
    return array

'''
    Takes in a sentence, and its dictionary of stems.
    Returns an array of all possible n-gram that contains exactly 1 stem.
'''
def one_stem(words,dict,n):
    length = len(words)
    array = {}
    #for the segment fitched from i to i+n
    for i in range(length+1-n):
        seg = []
        stem_track = [""]*n
        for j in range(n):
            seg.append([])
        
        stemCount = 0
        #for each word within the segment
        count = 0
        for st in range(i,i+n):
            for j in range(n):
                if j == stemCount:
                    if words[st] in dict.keys():
                        stem = dict[words[st]]
                        if len(stem) > 0:
                            seg[j].append(stem[0])
                            stem_track[count] = stem[0]
                            count += 1
                else:
                    seg[j].append(words[st])
            stemCount += 1
        count = 0
        for j in range(n):
            if len(seg[j]) == n:
                array[(i,stem_track[count])] =" ".join(seg[j])
                count+=1
    return array

'''
    Takes in a sentence, and its dictionary of stems.
    Returns an array of all possible n-gram that contains n-1 stems.
'''
def one_surface(words,dict,n):
    length = len(words)
    array = {}
    for i in range(length+1-n):
        seg = []
        for j in range(n):
            seg.append([])
        stemCount = 0
        count = 0
        surface_word = [""]*n
        for st in range(i,i+n):
            for j in range(n):
                if j == stemCount:
                    seg[j].append(words[st])
                    surface_word[count] = words[st]
                    count += 1
                else:
                    if words[st] in dict.keys():
                        stem = dict[words[st]]
                        if len(stem) > 0:
                            seg[j].append(stem[0])
            stemCount += 1
        count = 0
        for j in range(n):
            if len(seg[j]) == n:
                array[(i,surface_word[count])] = " ".join(seg[j])
            count += 1
    return array

'''
    Takes in a sentence, and its dictionary of stems.
    Returns an array of all possible 4-gram that contains exactly 2 stems.
'''
def two_stem(words,dict):
    length = len(words)
    array = {}
    
    for i in range(length+1-4):
        seg = []
        for j in range(6):
            seg.append([])
        
        stem_track = []
        for j in range(6):
            stem_track.append([])
        
        stemCount = 0
        for st in range(i,i+4):
            
            #swws
            if stemCount == 0 or stemCount == 3:
                if words[st] in dict.keys():
                    stem = dict[words[st]]
                    if len(stem) > 0:
                        seg[0].append(stem[0])
                        stem_track[0].append(stem[0])
            else:
                seg[0].append(words[st])
            #wssw
            if stemCount == 1 or stemCount == 2:
                if words[st] in dict.keys():
                    stem = dict[words[st]]
                    if len(stem) > 0:
                        seg[1].append(stem[0])
                        stem_track[1].append(stem[0])
            else:
                seg[1].append(words[st])
            #wwss
            if stemCount == 2 or stemCount == 3:
                if words[st] in dict.keys():
                    stem = dict[words[st]]
                    if len(stem) > 0:
                        seg[2].append(stem[0])
                        stem_track[2].append(stem[0])
            else:
                seg[2].append(words[st])
            
            #ssww
            if stemCount == 0 or stemCount == 1:
                if words[st] in dict.keys():
                    stem = dict[words[st]]
                    if len(stem) > 0:
                        seg[3].append(stem[0])
                        stem_track[3].append(stem[0])
            else:
                seg[3].append(words[st])
            
            #swsw
            if stemCount == 0 or stemCount == 2:
                if words[st] in dict.keys():
                    stem = dict[words[st]]
                    if len(stem) > 0:
                        seg[4].append(stem[0])
                        stem_track[4].append(stem[0])
            else:
                seg[4].append(words[st])
            
            #wsws
            if stemCount == 1 or stemCount == 3:
                if words[st] in dict.keys():
                    stem = dict[words[st]]
                    if len(stem) > 0:
                        seg[5].append(stem[0])
                        stem_track[5].append(stem[0])
            else:
                seg[5].append(words[st])
            
            stemCount += 1
        
        for j in range(6):
            if len(seg[j]) == 4:
                array[(i,j)] = " ".join(seg[j])
    return array

'''
    Checks the matching precision feature vectors
'''
def get_precision(tuple1, tuple2):
    weight = 0.0
    count = 0
    if tuple1[0] == tuple2[0] and tuple1[0] != "na":
        count += 1
        weight += POS_COST
    if tuple1[1] == tuple2[1] and tuple1[1] != "na":
        count += 1
        weight += GEN_COST
    if tuple1[2] == tuple2[2] and tuple1[2] != "na":
        count += 1
        weight += NUM_COST
    if tuple1[3] == tuple2[3] and tuple1[3] != "na":
        count += 1
        weight += STT_COST
    if tuple1[4] == tuple2[4] and tuple1[4] != "na":
        count += 1
        weight += PER_COST
    return [weight,count]

'''
    Finds n-gram matches on four different levels of accuracy.
    First level: search for all possible exact mathces
    Second level: search for both feature and stem matches
    Third level: feature matches
    Forth level: stem matches
    In the three first levels, all words of the n-gram are generated in that level.
    For the Forth level (i.e. stem match), we allow exact and stem matches within 
    the n-gram.
'''
def ngram(hyp_words, orgref, ref_words, n, tst_wrds, hyp, v):
    
    unmatched = []
    taken_ref = []
    #look for all possible exact matches
    ref_grams = generate_ngrams(ref_words,n)
    for j in range (0,tst_wrds-n+1):
        ref = orgref
        count = 1
        strv = ' '.join(hyp_words[j:j+n])
        match_is_found = 0
        for curndx in ref_grams.keys():
            if strv == ref_grams[curndx]:
                ndx = curndx
                if not(ndx in taken_ref) and match_is_found == 0:
                    taken_ref.append(ndx)
                    match_count[n-1] += 1
                    match_is_found = 1
        
        #keep track of unmatched index
        if match_is_found == 0:
            unmatched.append(j)
    if albleu_on == 1:
        #match all POS+stem
        ref_stem_grams = generate_feature_ngrams(ref_words,n,ref_stemposdict)
        hyp_stem_grams = generate_feature_ngrams(hyp_words,n,hyp_stemposdict)
        
        for seg in hyp_stem_grams.keys():
            for refseg in ref_stem_grams.keys():
                #check all grams in the ngram
                flag_not_match = 0
                scores_match_precision = []
                tempposstr = ""
                reftempposstr = ""
                stemtemp = ""
                
                for position in range(n):
                    
                    match_precision = get_stem_feat_precision(hyp_stem_grams[seg][0][position],ref_stem_grams[refseg][0][position])
                    scores_match_precision.append(match_precision[0])
                    
                    tempposstr += str(hyp_stem_grams[seg][1][position])+str(hyp_stem_grams[seg][0][position])
                    reftempposstr += str(ref_stem_grams[refseg][1][position])+str(ref_stem_grams[refseg][0][position])
                
                    if match_precision[1]  < MIN_TAKE :
                        flag_not_match = 1
                
                if flag_not_match == 0:
                    ndx = refseg
                    if not(ndx in taken_ref) and seg in unmatched:
                        unmatched.remove(seg)
                        taken_ref.append(ndx)
                        match_count[n-1] += min(scores_match_precision)


    
        #match all POS
        ref_stem_grams = generate_feature_ngrams(ref_words,n,ref_posdict)
        hyp_stem_grams = generate_feature_ngrams(hyp_words,n,hyp_posdict)
        
        for seg in hyp_stem_grams.keys():
            for refseg in ref_stem_grams.keys():
                #check all grams in the ngram
                flag_not_match = 0
                scores_match_precision = []
                
                for position in range(n):
                    
                    match_precision = get_precision(hyp_stem_grams[seg][0][position],ref_stem_grams[refseg][0][position])
                    scores_match_precision.append(match_precision[0])
                                    
                    if match_precision[1]  < MIN_TAKE :
                        flag_not_match = 1
                
                if flag_not_match == 0:
                    ndx = refseg
                    if not(ndx in taken_ref) and seg in unmatched:
                        unmatched.remove(seg)
                        taken_ref.append(ndx)
                        match_count[n-1] += min(scores_match_precision)
        
        #2-gram
        if n == 2:
            #match one stem
            ref_stem_grams = bigram_half_stem(ref_words,refstemdict)
            hyp_stem_grams = bigram_half_stem(hyp_words,hypstemdict)
            
            for hypcurndx in hyp_stem_grams:
                seg = hyp_stem_grams[hypcurndx]
                for curndx in ref_stem_grams.keys():
                    if seg == ref_stem_grams[curndx]:
                        ndx = curndx[0]
                        if not(ndx in taken_ref) and hypcurndx[0] in unmatched:
                            unmatched.remove(hypcurndx[0])
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST+1)/n
            
            
            #match all stems
            ref_stem_grams = generate_stem_ngrams(ref_words,n,refstemdict)
            hyp_stem_grams = generate_stem_ngrams(hyp_words,n,hypstemdict)
            for hypcurndx in hyp_stem_grams:
                seg = hyp_stem_grams[hypcurndx]
                for curndx in ref_stem_grams.keys():
                    if seg == ref_stem_grams[curndx]:
                        ndx = curndx
                        if not(ndx in taken_ref) and hypcurndx in unmatched:
                            unmatched.remove(hypcurndx)
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST*2)/n
        
        
        #3-gram
        if n == 3:
            #match one stem
            ref_one_stem = one_stem(ref_words,refstemdict,n)
            hyp_one_stem = one_stem(hyp_words,hypstemdict,n)
            for hypcurndx in hyp_one_stem:
                for curndx in ref_one_stem.keys():
                    seg = hyp_one_stem[hypcurndx]
                    if seg == ref_one_stem[curndx]:
                        ndx = curndx[0]
                        if not(ndx in taken_ref) and hypcurndx[0] in unmatched:
                            unmatched.remove(hypcurndx[0])
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST+1*2)/n
            
            #match two stem
            ref_two_stem = one_surface(ref_words,refstemdict,n)
            hyp_two_stem = one_surface(hyp_words,hypstemdict,n)
            
            for hypcurndx in hyp_two_stem:
                for curndx in ref_two_stem.keys():
                    seg = hyp_two_stem[hypcurndx]
                    if seg == ref_two_stem[curndx]:
                        ndx = curndx[0]
                        if not(ndx in taken_ref) and hypcurndx[0] in unmatched:
                            unmatched.remove(hypcurndx[0])
                            taken_ref.append(ndx)
                            match_count[n-1] +=  (STEM_COST*2+1)/n
            
            #match fully stem
            ref_stem_grams = generate_stem_ngrams(ref_words,n,refstemdict)
            hyp_stem_grams = generate_stem_ngrams(hyp_words,n,hypstemdict)
            for hypcurndx in hyp_one_stem:
                for curndx in ref_one_stem.keys():
                    seg = hyp_one_stem[hypcurndx]
                    if seg == ref_one_stem[curndx]:
                        ndx = curndx[0]
                        if not(ndx in taken_ref) and hypcurndx[0] in unmatched:
                            unmatched.remove(hypcurndx[0])
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST+1*3)/n
        
        #4-gram
        if n == 4:
            #match one stem
            ref_one_stem = one_stem(ref_words,refstemdict,n)
            hyp_one_stem = one_stem(hyp_words,hypstemdict,n)
            for hypcurndx in hyp_one_stem:
                for curndx in ref_one_stem.keys():
                    seg = hyp_one_stem[hypcurndx]
                    if seg == ref_one_stem[curndx]:
                        ndx = curndx[0]
                        if not(ndx in taken_ref) and hypcurndx[0] in unmatched:
                            unmatched.remove(hypcurndx[0])
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST+1*3)/n
            
            #match two stems
            ref_two_stem = two_stem(ref_words,refstemdict)
            hyp_two_stem = two_stem(hyp_words,hypstemdict)
            for hypcurndx in hyp_two_stem:
                for curndx in ref_two_stem.keys():
                    seg = hyp_two_stem[hypcurndx]
                    if seg == ref_two_stem[curndx]:
                        ndx = curndx[0]
                        if not(ndx in taken_ref) and hypcurndx[0] in unmatched:
                            unmatched.remove(hypcurndx[0])
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST*2+1*2)/n
            
            #match three stems
            ref_three_stem = one_surface(ref_words,refstemdict,n)
            hyp_three_stem = one_surface(hyp_words,hypstemdict,n)
            for hypcurndx in hyp_three_stem:
                for curndx in ref_three_stem.keys():
                    seg = hyp_three_stem[hypcurndx]
                    if seg == ref_three_stem[curndx]:
                        ndx = curndx[0]
                        if not(ndx in taken_ref) and hypcurndx[0] in unmatched:
                            unmatched.remove(hypcurndx[0])
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST*3+1)/n
            
            #match fully stem
            ref_stem_grams = generate_stem_ngrams(ref_words,n,refstemdict)
            hyp_stem_grams = generate_stem_ngrams(hyp_words,n,hypstemdict)
            for hypcurndx in hyp_stem_grams:
                seg = hyp_stem_grams[hypcurndx]
                for curndx in ref_stem_grams.keys():
                    if seg == ref_stem_grams[curndx]:
                        ndx = curndx
                        if not(ndx in taken_ref) and hypcurndx in unmatched:
                            unmatched.remove(hypcurndx)
                            taken_ref.append(ndx)
                            match_count[n-1] += (STEM_COST*4)/n


'''
    Computes the score for a given sentence
'''
def score_segment(hyp, ref,v):
    global max_Ngram
    hyp_words  = hyp.split()
    ref_words  = ref.split()
    hyp_length = len(hyp_words)
    ref_length = len(ref_words)
    max_Ngram = min(4,hyp_length)
    for j in range (1,max_Ngram+1): #compute ngram counts
        if (j <= hyp_length):
            hyp_count[j-1] += hyp_length - j + 1
    for j in range (1,max_Ngram+1): #compute ngram counts
        if (j <= ref_length):
            ref_count[j-1] += ref_length - j + 1
    #create dictionary for ref to avoid multiple counts of the same match
    tempref = ' '.join(ref_words)
    
    copy_ref_words = copy.deepcopy(ref_words)
    for i in range(1,max_Ngram+1):
        copy_ref_words = copy.deepcopy(ref_words)
        ngram(hyp_words, ref, copy_ref_words, i,hyp_length,hyp, v)
    
    #check if end of file
    if (hyp_count[0]>0 ):
        score_bleu()
        print_format()
    
    init()

'''
    Initializing arrays to score a new sentence 
'''
def init():
    for i in range(max_Ngram):
        hyp_count [i]  = 0
        ref_count  [i] = 0
        match_count[i]= 0.0
        score [i]=     0.0
        indscore [i]=  0.0

'''
    Iterates through the translation and reference documnts, along 
    with their corresponding MADA files.
'''
def score_doc(hypfile, reffile):
    linecount = 1
    hyp_mada_file = codecs.open(mainpath+"e-hyp.mada", 'r')
    ref_mada_file = codecs.open(mainpath+"e-test.mada", 'r')
    global hypstemdict, hyp_posdict, refstemdict, ref_posdict, ref_stemposdict, hyp_stemposdict
    
    for hyp, ref in itertools.izip(hypfile, reffile):
        
        hypstemdict = {}
        hyp_posdict = {}
        refstemdict = {}
        ref_posdict = {}
        
        hypdict = getstem(hyp_mada_file)
        refdict = getstem(ref_mada_file)
        if (hypdict != None):
            hypstemdict = hypdict[0]
            hyp_posdict = hypdict[1]
            hyp_stemposdict = hypdict[2]
            refstemdict = refdict[0]
            ref_posdict = refdict[1]
            ref_stemposdict = refdict[2]
        hyp1 = tokenize(hyp)
        ref1 = tokenize(ref)
        score_segment(hyp1, ref1, linecount)
        linecount +=1

'''
    Tokenize the Arabic specific punctuation marks that are not
    tokenized in normalize.pl helper file
'''
def tokenize(line):
    newline = line.replace("،"," ، ").replace("؛"," ؛ ").replace("؟"," ؟ ").replace("»"," » ").replace("«"," « ").replace("  "," ")
    return newline

'''
    Computes the bleu score give the match and word counts.
'''
def score_bleu():
    lenscore = min(0,1- ((ref_count[0]+0.0) / hyp_count[0]))
    cres = 0;
    for i in range(0,max_Ngram):
        pn = 0
        if hyp_count[i] > 0:
            pn  = (match_count[i]+0.0)/hyp_count[i];
            pn = round(pn,4)
            if pn == 0:
                pn = 0.001
        wn = 1.0/(i+1)
        res = 0
        indscore[i] = pn
        if (pn>0):
            res = math.log(pn)
            cres = cres + res
            score[i] = math.exp(cres*wn + lenscore )
            score[i] = round(score[i],4)

def print_format():
    print (score[max_Ngram-1])

#TODO: add option/script for document scoring! 
global STEM_COST, mainpath, POS_COST,GEN_COST, NUM_COST, PER_COST, STT_COST, albleu_on

albleu_on = 0
mainpath = sys.argv[1]
hyp_path = mainpath+"e-hyp"
ref_path = mainpath+"e-test"

#TODO: fix the values
STEM_COST=0.1
POS_COST=0.1
GEN_COST=0.1
NUM_COST=0.1
PER_COST=0.1
STT_COST=0.1 

normalize_dir = home+"/utils/normalize.pl"
hypfile = subprocess.check_output(["perl",normalize_dir,hyp_path]).split("\n")
reffile = subprocess.check_output(["perl",normalize_dir,ref_path]).split("\n")

score_doc(hypfile,reffile)
