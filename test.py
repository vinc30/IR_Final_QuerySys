#!/usr/bin/env python  
# -*- coding: UTF-8  -*-  
from gensim import corpora, models, similarities
import jieba
import os
import sys
from bs4 import BeautifulSoup
from glob import glob
testlist = []
DATAPATH = "/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/minidata/*"
for i in glob(DATAPATH):
    content=''
    sentences = open(i).read()
    soup = BeautifulSoup(sentences)
    for i in soup.findAll('p'):
        content += i.get_text()
    testlist.append(content)

#testlist = ["我喜欢吃土豆","土豆是个百搭的东西","我不喜欢今天雾霾的北京"]
words=[]
for doc in testlist:
    words.append(list(testlist))
#    print words
dic = corpora.Dictionary(words)
#print dic
#print dic.token2id

#for word,index in dic.token2id.iteritems():
#   print word +" 编号为:"+ str(index)
corpus = [dic.doc2bow(text) for text in words] #print corpus

tfidf = models.TfidfModel(corpus)
vec = [(0, 1), (4, 1)] #print tfidf[vec]
corpus_tfidf = tfidf[corpus]
"""
for doc in corpus_tfidf:
    print doc 
"""
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=1109)#need to get from print dic 25
sims = index[tfidf[vec]]
print list(enumerate(sims))
