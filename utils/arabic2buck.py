# This is a simple script to turn any Arabic text encoded in utf-8

# to Buckwalter translietration and it seems to be very fast

# It uses the simple replace method to do all the action.

def buckwalter(text):

             text = text.replace(u"\u0621", "'")

             text = text.replace(u"\u0622", "|")

             text = text.replace(u"\u0623", ">")

             text = text.replace(u"\u0624", "&")

             text = text.replace(u"\u0625", "<")

             text = text.replace(u"\u0626", "}")

             text = text.replace(u"\u0627", "A")    

             text = text.replace(u"\u0628","b") # baa'

             text = text.replace(u"\u0629","p") # taa' marbuuTa

             text = text.replace(u"\u062A", "t")# taa'

             text = text.replace(u"\u062B","v") # thaa'

             text = text.replace(u"\u062C","j") # jiim

             text = text.replace(u"\u062D","H") # Haa'

             text = text.replace( u"\u062E", "x")# khaa'

             text = text.replace(u"\u062F", "d")# daal

             text = text.replace(u"\u0630", "*")# dhaal

             text = text.replace(u"\u0631", "r")# raa'

             text = text.replace(u"\u0632", "z")# zaay

             text = text.replace(u"\u0633","s") # siin

             text = text.replace(u"\u0634", "$")# shiin

             text = text.replace(u"\u0635","S") # Saad

             text = text.replace(u"\u0636", "D")# Daad

             text = text.replace(u"\u0637","T") # Taa'

             text = text.replace(u"\u0638", "Z")# Zaa' (DHaa')

             text = text.replace(u"\u0639", "E")# cayn

             text = text.replace(u"\u063A", "g")# ghayn

             text = text.replace(u"\u0640","_") # taTwiil

             text = text.replace(u"\u0641","f") # faa'

             text = text.replace(u"\u0642","q") # qaaf

             text = text.replace(u"\u0643", "k")# kaaf

             text = text.replace( u"\u0644", "l")# laam

             text = text.replace(u"\u0645","m") # miim

             text = text.replace(u"\u0646","n") # nuun

             text = text.replace(u"\u0647", "h")# haa'

             text = text.replace(u"\u0648", "w")# waaw

             text = text.replace(u"\u0649", "Y")# 'alif maqSuura

             text = text.replace(u"\u064A", "y")# yaa'

             text = text.replace(u"\u064B", "F")# fatHatayn

             text = text.replace(u"\u064C", "N") # Dammatayn

             text = text.replace( u"\u064D", "K")# kasratayn

             text = text.replace(u"\u064E", "a")# fatHa

             text = text.replace(u"\u064F","u") # Damma

             text = text.replace(u"\u0650", "i")# kasra

             text = text.replace(u"\u0651", "~")# shaddah

             text = text.replace(u"\u0652", "o")# sukuun

             text = text.replace(u"\u0670","`") # dagger 'alif

             text = text.replace(u"\u0671", "{")# waSla

             return text.strip().encode("utf-8")


######################################################################################

import codecs, sys
