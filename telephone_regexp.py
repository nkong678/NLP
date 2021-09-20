"""
Created on Tue Sep 14 17:23:22 2021

@author: nkong
"""


import nltk
import sys
import re

if (len(sys.argv) < 2):
    fname = input("Please enter the file name.\n")
else:
    fname = sys.argv[1]
f = open(fname, "r", encoding="utf8")
raw = f.read()
#spaced
noParentheses = '((\+\d+)?(\d\d\d[\ \-\.])?(\d\d\d[\ \-\.]\d\d\d\d))'
#hyphenated
# hyphen = '((\d\d\d\-)?(\d\d\d\-\d\d\d\d))'
# #period
# period = '((\d\d\d\.)?(\d\d\d\.\d\d\d\d))'
# #spaced with area code in parentheses
# pspaced = '(\(\d\d\d\)(\ \d\d\d\ \d\d\d\d))'
#hyphenated with area code in parentheses
parentheses = '((\+\d+)?\(\d\d\d\)[\ \-\.]\d\d\d[\ \-\.]\d\d\d\d)'
# #periods with area code in parentheses
# pperiod = '(\(\d\d\d\)\.\d\d\d\.\d\d\d\d)'
query = noParentheses + '|' + parentheses
list = re.finditer(query, raw)
output = open("telephone_output.txt", "w")
for item in list:
    output.write(item.group(0) + '\n')
