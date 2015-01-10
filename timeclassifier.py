#!/usr/bin/env python
# -*- coding: UTF-8  -*-
from gensim import corpora, models, similarities
import jieba
from bs4 import BeautifulSoup
from glob import glob
import dateutil.parser
import numpy as np
import mx
import timex
import random
import datetime


testlist = []
DATAPATH = "/home/urjeans/ir/database/*"

for kkk in range(len(glob(DATAPATH))):
    content=''
    sentences = open(glob("database/" + str(kkk))[0]).read()
    soup = BeautifulSoup(sentences)
    content+=soup.find('title').get_text()
    for jjj in soup.findAll('p'):
        content += jjj.get_text()
    testlist.append(content)
words=[]
jieba.set_dictionary('dict.txt.big')
for doc in testlist:
    words.append(list(jieba.cut(doc.lower(), cut_all=False)))

token = "，。！？：；「」『』\n 、　".decode("utf8")
for iii, textlist in enumerate(words):
    words[iii] = [text for text in textlist if text not in token]
dic = corpora.Dictionary(words)
corpus = [dic.doc2bow(text, allow_update=True) for text in words] #print corpus
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dic))   #need to get from print dic 25

newsdic = {}
with open("news_to_news_random_id_unlabeled_table_groundtruth_no_original_id.txt") as f:
    for line in f:
        (key, val1, val2) = line.split()
        newsdic[int(key)] = [val1, val2]


def getBasetime(newsid):
    global tfidf, index, corpus, newsdic
    vec = corpus[int(newsid)]
    sims = index[tfidf[vec]]
    result = sorted(list(enumerate(sims)), reverse=True, key=lambda x: x[1])
    for idx, k in enumerate(result):
        if result[idx + 1][0] in newsdic:
            timeobj = mx.DateTime.DateTime(int(newsdic[result[idx + 1][0]][1].split('-')[0]), int(newsdic[result[idx + 1][0]][1].split('-')[1]), int(newsdic[result[idx + 1][0]][1].split('-')[2]))
            return timeobj
    assert False, "Error: Can't find any time for news " + str(newsid)

def getTime(newsid):
    """
    Do something to get the lastest date in the article, in Unix Time form (a.k.a. seconds from 1970/1/1)
    """
    flag = 0
    fp = open('database/'+newsid)
    soup = BeautifulSoup(fp)
    tagtimes = list()
    #content +=soup.find('title').get_text()
    for i in soup.findAll('p'):
        text = i.get_text()
        #    content += text.strip() + "\n"
        tagged = timex.ground(timex.tag(text), getBasetime(newsid))
        soup2 = BeautifulSoup(tagged)
        if soup2.timex2 != None:
	    flag = 1
            for i in soup2.findAll('timex2'):
                try:
                    # print "tagged time: " + str(i)
                    timestr = i['val']
                except KeyError:
                    print "Error tagged time: " + str(i)
                    continue
                if timestr != 'UNKNOWN':
                    try:
                        tagtimes.append(int(dateutil.parser.parse(timestr).strftime('%s')))
                    except ValueError:
                        continue
                else:
                    print i
    if flag ==0:
        # print("OMG no tags!")
        randtime = random.randint(1370016000,1416758400)
        print("Fail to get timetag from news " + str(newsid) + " , assign " + str(randtime))
        return int(randtime)
    else:
        if tagtimes != list():
            print("Time prediction for news " + str(newsid) + ": " + str(np.array(tagtimes).min()))
            return np.array(tagtimes).min()
        else:
            randtime = random.randint(1370016000,1416758400)
            print("Fail to get timetag from news " + str(newsid) + " , assign " + str(randtime))
            return int(randtime)


# fq = open("query.txt", "r")
fphase1 = open("phase1_pooling_result.txt", "r")
fout1 = open("phase1_time_sorted_id.txt", "w") 
fout2 = open("phase1_time_sorted.txt", "w")
for q in fphase1:
    newslist = q.strip().split(" ")
    newstime = list()
    for ijk in newslist:
        newstime.append(getTime(ijk)) 

    """
    vec = list()
    for i in range(len(query)):
        for j in range(len(dic.doc2bow(list(jieba.cut(query[i].lower(), cut_all=False))))):
            vec.append(dic.doc2bow(list(jieba.cut(query[i].lower(), cut_all=False)))[j])
    sims = index[tfidf[vec]]
    print vec
    """
    
    sortednews = sorted(zip(newslist, newstime), key=lambda x:x[1])   
    for t in sortednews:
        fout1.write(str(t[0]) + " ")
        fout2.write(str(datetime.datetime.fromtimestamp(float(t[1])).strftime('%Y-%m-%d')) + " ")
    fout1.write('\n')
    fout2.write('\n') 

fphase1.close()
