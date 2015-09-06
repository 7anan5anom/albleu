# coding: utf-8

#from __future__ import print_function
import sys, re, codecs,itertools,string,math,os
import buck2arabic


def getstem(infile):
    
    dict = {}
    posdict = {}
    stemposdict = {}
    
    for mada in  infile:
        
        if mada == "SENTENCE BREAK\n":
            return [dict,posdict,stemposdict]
    
        #add a word as a key
        temp = mada.split()
        if temp[0] == ";;WORD" and len(temp)>1:
            word =temp[1]
            wordInArabic = buck2arabic.toUnicode(word)
            dict [wordInArabic]=[]
            posdict [wordInArabic]=[]
            stemposdict [wordInArabic]=[]

        if("stem:" in mada):
            #finding stem
            result = re.search('stem:(.*) ', mada)
            #get the stem and remove punctution [uiao~'FKN]
            stem = re.sub('[uiao~\'FKN]',"",result.group(1))
            #add it to the list if it doesn't already exist
            stemInArabic = buck2arabic.toUnicode(stem)
            if (len(dict[wordInArabic]) == 0 ):
                dict[wordInArabic].append(stemInArabic)
           
        if("pos:" in mada and "gen:" in mada and "num:" in mada and "stt" in mada and "per" in mada ):
            pos = re.search('pos:(.*) ', mada).group(1).split()[0]
            gen = re.search('gen:(.*) ', mada).group(1).split()[0]
            num = re.search('num:(.*) ', mada).group(1).split()[0]
            stt = re.search('stt:(.*) ', mada).group(1).split()[0]
            per = re.search('per:(.*) ', mada).group(1).split()[0]
            
            tuple= (pos,gen,num,stt,per)
            #add it to the list
            if (len(posdict[wordInArabic]) == 0 ):
                if ("adj" in pos or "noun" in pos or "verb" in pos):
                    posdict[wordInArabic].append(tuple)

        if("pos:" in mada and "gen:" in mada and "num:" in mada and "stt" in mada and "per" in mada and "stem:" in mada):
            pos = re.search('pos:(.*) ', mada).group(1).split()[0]
            if not("adj" in pos or "noun" in pos or "verb" in pos):
                pos = "na"
            gen = re.search('gen:(.*) ', mada).group(1).split()[0]
            num = re.search('num:(.*) ', mada).group(1).split()[0]
            stt = re.search('stt:(.*) ', mada).group(1).split()[0]
            per = re.search('per:(.*) ', mada).group(1).split()[0]
            result = re.search('stem:(.*) ', mada)
            stem = re.sub('[uiao~\'FKN]',"",result.group(1))
            
            tuple= (pos,gen,num,stt,per,stem)
            #add it to the list
            if (len(stemposdict[wordInArabic]) == 0 ):
                    stemposdict[wordInArabic].append(tuple)

