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
print testlist

#sentences = ["我喜欢吃土豆","土豆是个百搭的东西","我不喜欢今天雾霾的北京"]
words=[]
for doc in testlist:
    words.append(list(testlist))
#    print words
dic = corpora.Dictionary(words)
#print dic
#print dic.token2id
for word,index in dic.token2id.iteritems():
    print word +" 编号为:"+ str(index)
