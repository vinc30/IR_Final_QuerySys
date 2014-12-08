"""
The IR2014fall final project, phase I


To-do:
    1. Given a query string
    2. Iterate through all docs and calculate TF-IDF for each doc
    3. Return the top 100 highest tf-idf doc

ISSUES:
    #1: can't handle chinese query
    #2: A mysterious func that turn .xml file into word segments
"""

import sys
import transfer
from glob import glob


# def seg(string):
#    return ["foo", "amy", "bob", "charlie"]

def calIDF(datapath, qstr):
    idf = float(0)
    dbfiles = glob(datapath)
    for docpath in dbfiles:
        # wordset = seg(open(docpath, "r").read())
        wordset = transfer.load_xml_file(docpath, " ")
        # if qstr in wordset:
        #     idf += 1
        if qstr[0] in wordset:
            idx = wordset.index(qstr[0])
            match = 1
            for i in range(len(qstr)):
                if qstr[i] != wordset[idx + i]:
                    match = 0
            if match == 1:
                idf += 1
    return idf / float(len(dbfiles))


def calTF(wordlist, qstr):
    # return float(wordlist.count(qstr)) / float(len(wordlist))
    tf = 0
    if qstr[0] in wordlist:
        idxlist = [i for (i, j) in enumerate(wordlist) if j == qstr]
        for idx in idxlist:
            match = 1
            for i in len(qstr):
                if qstr[i] != wordlist[idx + i]:
                    match = 0
            if match == 1:
                tf += 1
    return float(tf) / float(len(wordlist))


def calTFIDF(datapath, wordlist, qstr):
    return calTF(wordlist, qstr) * calIDF(datapath, qstr)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Error: Invalid input arguments"
    
    # query = []
    # for i in range(len(sys.argv) - 1):
    #     query.append(sys.argv[i + 1])
    fq = open("query.txt", "r")

    # ISSUE#1: Can't handle Chinese query  
    
    # Iterate through all data
    DATAPATH = "/home/urjeans/ir/database/*"
    # print "#doc = " + str(len(glob(DATAPATH)))
    scores = list()
    dbfiles = glob(DATAPATH)
    for query in fq:
        terms = query.strip().split(" ")
        for i in range(len(terms) - 1):
            keyword = terms[i + 1].decode("utf-8")
            for docpath in dbfiles:
                # ISSUE#2: A mysterious func that turn .xml file into word segments
                # words = seg(open(docpath, "r").read())
                words = transfer.load_xml_file(docpath, " ")
                score = float(0)
                for q in query:
                    score += calTFIDF(DATAPATH, words, q)
                scores.append(score)
            rank = sorted(zip(range(len(scores)), scores), key=lambda i:i[1], reverse=True)
            for i in range(100):
                print rank[i]
