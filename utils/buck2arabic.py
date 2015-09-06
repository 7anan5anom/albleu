# This is a buckwlater to unicode script. It uses simple replace methods

# First define a replacement function and call it "toUnicode"

def toUnicode(text):

    """The function takes a text and returns a Unicode representation of it"""

    text = text.replace( "'" , u"\u0621" )

    text = text.replace( "|" , u"\u0622" )

    text = text.replace( ">" , u"\u0623" )

    text = text.replace( "&" , u"\u0624" )

    text = text.replace( "<" , u"\u0625" )

    text = text.replace( "}" , u"\u0626" )

    text = text.replace( "A" , u"\u0627" )

    text = text.replace( "b" , u"\u0628" )

    text = text.replace( "p" , u"\u0629" )

    text = text.replace( "t" , u"\u062A" )

    text = text.replace( "v" , u"\u062B" )

    text = text.replace( "j" , u"\u062C" )

    text = text.replace( "H" , u"\u062D" )

    text = text.replace( "x" , u"\u062E" )

    text = text.replace( "d" , u"\u062F" )

    text = text.replace( "*" , u"\u0630" )

    text = text.replace( "r" , u"\u0631" )

    text = text.replace( "z" , u"\u0632" )

    text = text.replace( "s" , u"\u0633" )

    text = text.replace( "$" , u"\u0634" )

    text = text.replace( "S" , u"\u0635" )

    text = text.replace( "D" , u"\u0636" )

    text = text.replace( "T" , u"\u0637" )

    text = text.replace( "Z" , u"\u0638" )

    text = text.replace( "E" , u"\u0639" )

    text = text.replace( "g" , u"\u063A" )

    text = text.replace( "_" , u"\u0640" )

    text = text.replace( "f" , u"\u0641" )

    text = text.replace( "q" , u"\u0642" )

    text = text.replace( "k" , u"\u0643" )

    text = text.replace( "l" , u"\u0644" )

    text = text.replace( "m" , u"\u0645" )

    text = text.replace( "n" , u"\u0646" )

    text = text.replace( "h" , u"\u0647" )

    text = text.replace( "w" , u"\u0648" )

    text = text.replace( "Y" , u"\u0649" )

    text = text.replace( "y" , u"\u064A" )

    text = text.replace( "F" , u"\u064B" )

    text = text.replace( "N" , u"\u064C" )

    text = text.replace( "K" , u"\u064D" )

    text = text.replace( "a" , u"\u064E" )

    text = text.replace( "u" , u"\u064F" )

    text = text.replace( "i" , u"\u0650" )

    text = text.replace( "~" , u"\u0651" )

    text = text.replace( "o" , u"\u0652" )

    text = text.replace( "`" , u"\u0670" )

    text = text.replace( "{" , u"\u0671" )

    return text.strip().encode("utf8")



import codecs, sys



                         
