# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 15:25:36 2021

@author: nkong
"""
import sys
import string
import math
import numpy as np
from numpy.linalg import norm
from numpy import dot
import nltk
from nltk.tokenize import word_tokenize
from string import digits


def readQuery(queryPath, termList, stopList):
    queries = {}
    queryTF = {}
    terms = {}
    f = open(queryPath, "r")
    lines = f.readlines()
    queryID = 0
    
    query = ""
    for line in lines:
        #clean the line

        if line[0:2] == '.I':
            #if id
            queries[queryID] = query
            queryTF[queryID] = terms
            terms = {}
            queryID = line[3:6]
        elif line[0:2] == '.W':
            #if abstract tag line skip line
            query = ""
        else:
            line = line.translate(str.maketrans('','',digits))
            line = line.translate(str.maketrans('','',string.punctuation))
            words = word_tokenize(line)
            query += line
            for word in words:
                if word not in stopList:
                    if word not in terms:
                        terms[word] = 1
                    else:
                        terms[word] += 1
                    if word not in termList:
                        termList.append(word)
            
    queries[queryID] = query
    queryTF[queryID] = terms
    return (queries, termList, queryTF)

def readAbstract(abstractPath, stopList):
     abstracts = {}
     abstractTF = {}
     terms = {}
     termList = []
     f = open(abstractPath, "r")
     lines = f.readlines()
     abstractID = 0
     abstract = ""
     abstractFlag = False
     for line in lines:

        if line[0:2] == '.I':
            abstractFlag = False
            abstracts[abstractID] = abstract
            abstractTF[abstractID] = terms
            abstractID = line[3:6]
        elif line[0:2] == '.T':
            abstractFlag = False
        
        elif line[0:2] == '.A':
            abstractFlag = False
        
        elif line[0:2] == '.B':
            abstractFlag = False
        
        elif line[0:2] == '.W':
            abstractFlag = True
            abstract = ""
            
        elif abstractFlag:
            line = line.translate(str.maketrans('','',digits))
            line = line.translate(str.maketrans('','',string.punctuation))
            words = word_tokenize(line)
            abstract += line
            for word in words:
                if word not in stopList:
                    if word not in termList:
                        termList.append(word)
                    if word in terms:
                        terms[word] += 1
                    else:
                        terms[word] = 1
     abstracts[abstractID] = abstract
     abstractTF[abstractID] = terms
     return (abstracts, termList, abstractTF)
    
def CalculateIDF(documents, term, numDocs):
    docCount = 0
    for document in documents:
        if term in documents[document]:
            docCount += 1
    if docCount == 0:
        return 0
    
    return math.log(numDocs/docCount)
                
        
def main(args):
    qryFile = "cran.qry"
    abstractFile = "cran.all.1400"
    qtermList = []
    writeFile = open("output.txt", "w")
    

    stopList = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                'via','vs','with','that','can','cannot','could','may','might','must',\
                'need','ought','shall','should','will','would','have','had','has','having','be',\
                'is','am','are','was','were','being','been','get','gets','got','gotten',\
                'getting','seem','seeming','seems','seemed',\
                'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                'you','your','yours','me','my','mine','I','we','us','much','and/or'
                ]
    queries = readQuery(qryFile, qtermList, stopList)
    abstracts = readAbstract(abstractFile, stopList)
    queryIDF = {}
    abstractIDF = {}
    queryList = queries[0]
    qtermList = queries[1]
    queryTF = queries[2]
    abstractList = abstracts[0]
    aTermList = abstracts[1]
    abstractTF = abstracts[2]
    queryList.pop(0)
    queryTF.pop(0)
    queryTFIDF = {}
    abstractTFIDF = {}
    for term in qtermList:
        queryIDF[term] = CalculateIDF(queries[0], term, 225)
    for term in aTermList:
        abstractIDF[term] = CalculateIDF(abstractList, term, 1400)
        
    for query in queryList:
        queryTFIDF[query] = {}
        for word in queryTF[query]:
            queryTFIDF[query][word] = queryTF[query][word] * queryIDF[word]

    for abstract in abstractList:
        abstractTFIDF[abstract] = {}
        for word in abstractTF[abstract]:
            abstractTFIDF[abstract][word] = abstractTF[abstract][word] * abstractIDF[word]

    abstractVectors = {}
    for query in queryTFIDF:
        abstractVectors[query] = {}
        for abstract in abstractTFIDF:
            abstractVectors[query][abstract] = {}
            for word in queryTFIDF[query].keys():
                if word in abstractTFIDF[abstract]:
                    abstractVectors[query][abstract][word] = abstractTFIDF[abstract][word]
                else:
                    abstractVectors[query][abstract][word] = 0
    
    cosineSimilarity = {}
    for query in abstractVectors:
        cosineSimilarity[query] = {}
        queryVec = list(abstractVectors[query].values())
        for abstract in abstractVectors[query].keys():
            abstractVec = list(abstractVectors[query][abstract].values())
            cos = dot(queryVec, abstractVec)/ (norm(queryVec) * norm(abstractVec))
            if math.isnan(cos):
                cos = 0
            cosineSimilarity[query][abstract] = cos
    output = {}
    for query in cosineSimilarity:
        output[query] = sorted(cosineSimilarity[query].items(), key=lambda item: item[1], reverse=True)
    out = open("output.txt", "w")
    for query in output:
        for abstract in output[query]:
            if abstract[1] == 0:
                continue
            out.write(str(query) + " " + str(abstract) + " " + str(cosineSimilarity[query][abstract]) + "\n")

    
    
if __name__ == '__main__':
	main(sys.argv)