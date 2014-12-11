#!/usr/bin/env python
# -*- coding: UTF-8  -*-
from gensim import corpora, models, similarities
import jieba
from bs4 import BeautifulSoup
from glob import glob
testlist = []
# DATAPATH = "/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/minidata/*"
DATAPATH = "/home/urjeans/ir/database/*"

#news_random_id_unlabeled_new/*"
for i in range(len(glob(DATAPATH))):
#print i
    content=''
    sentences = open(glob("database/" + str(i))[0]).read()
#sentences = open( glob('minidata/'+ str(i)) ).read()
    soup = BeautifulSoup(sentences)
    content+=soup.find('title').get_text()
    for i in soup.findAll('p'):
        content += i.get_text()
    testlist.append(content)
#testlist = ["我喜欢吃土豆","土豆是个百搭的东西","我不喜欢今天雾霾的北京"]
words=[]
jieba.set_dictionary('dict.txt.big')
for doc in testlist:
    words.append(list(jieba.cut(doc.lower(), cut_all=False)))
    # words.append(doc.split()) 
#    print words
dic = corpora.Dictionary(words)
#print dic
#print dic.token2id
#for word,index in dic.token2id.iteritems():
#   print word +" 编号为:"+ str(index)
corpus = [dic.doc2bow(text, allow_update=True) for text in words] #print corpus
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
fq = open("query.txt", "r")
#for query in querylist:
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dic))#need to get from print dic 25
for q in fq:
    query = "".join(q.strip().split(" ")[1:])
#query = "鄭捷 捷運"
    vec = dic.doc2bow(list(jieba.cut(query.lower(), cut_all=False))) # or like corpus = [dic.doc2bow(text) for text in words]
    # vec = dic.doc2bow(query.split())
    sims = index[tfidf[vec]]
    print vec
#    for doc in corpus_tfidf:
#   print doc
#    """
    result = sorted(list(enumerate(sims)), reverse=True, key=lambda x: x[1])
    resultlist = list()

    for i in range(100):
        resultlist.append(result[i])
    fresult = open("result_nojieba.txt", "a+")
    fresult.write(str(resultlist) + "\n")
fresult.close()
