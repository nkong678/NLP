# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:06:26 2021

@author: nkong
"""

import nltk
import sys
print(len(sys.argv))
if (len(sys.argv) == 1):
    fname = input("Please enter the filename.\n")
else:
    fname = sys.argv[0]
f = open(fname)
raw = f.read()
print(raw)
