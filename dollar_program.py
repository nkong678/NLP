# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:06:26 2021

@author: nkong
"""

import nltk
import sys
import re

if (len(sys.argv) < 2):
    fname = input("Please enter the filename. \n")
else:
    fname = sys.argv[1]
f = open(fname, "r", encoding="utf8")
raw = f.read()
#read numerical values starting with $
nums = '(\$\d[\d\,]*[\d](\.?(\d\d))?)'
#read numerical values ending with dollar
numDollar = '(\d[\d\,]*\.?(\d\d)?\ dollar[s]?\ ((and)?[ ]\d\d cent[s]?)?)'
#read cents only , including $.53
cents = '(\$[0]?/.(\d\d))'
#read cents ending in "cents"
numCents = '\d+[ ]cent[s]?'
#read cents in words
centsOnlyWords = '((one|two|three|four|forty|five|six|seven|eight|nine|ten|eleven|twelve|thir|fif|eigh|twen)(teen|ty)?\-?)+[ ]cent(s)'
#read words depicting money
words = '((((one|two|three|four|forty|five|six|seven|eight|nine|ten|eleven|twelve|thir|fif|eigh|twen)(teen|ty)?\-?)[ ]?(hundred[s]?)?[ ]?(thousand[s])?[ ]?(million[s]?)?[ ]?(billion[s])?[ ]?(trillion[s]?)?)+[ ](dollar[s]?))'
#read numerical values with large qualifiers
numLargeQual = '(\$\d[\d\,]*[\d][ ](hundred[s]?)?[ ]?(thousand[s]?)?[ ]?(million[s]?)?[ ](billion[s]?)?[ ](trillion[s]?))'
query = nums +'|' + cents +'|' + numCents + '|' + centsOnlyWords + '|' + words + '|' + numLargeQual
# print(type(query))
list = re.finditer(query, raw)
for item in list:
    print(item.group(0))
