# -*- coding: UTF-8  -*-  


"""
Usage: 
    python sortTime.py phase1_pooling_result.txt

Output:
    A file phase1_pooling_result_time_sorted.txt

"""


from bs4 import BeautifulSoup
import timex
from os.path import join, exists
import mx
import random
import dateutil.parser
import numpy as np
import datetime


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
        tagged = timex.ground(timex.tag(text), mx.DateTime.now())
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
                    tagtimes.append(int(dateutil.parser.parse(timestr).strftime('%s')))
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
            return randtime

def file2str(filename):
    """
    Given the article name
    Do something to return the whole article without any <tag>
    """
    # assert exists(join("../../news_random_id_unlabeled_new", filename)), "Error: FILE " + join("database", filename) + " is missing "
    # fp = open(join("../../news_random_id_unlabeled_new", filename))
    assert exists(join("database", filename)), "Error: FILE " + join("database", filename) + " is missing "
    fp = open(join("database", filename))
    soup = BeautifulSoup(fp)
    content = ""
    content +=soup.find('title').get_text()
    for i in soup.findAll('p'):
            text = str(i.get_text())
            content += text.strip() + "\n"
    return content


if __name__ == "__main__":
    fphase1 = open("phase1_pooling_result.txt", "r")
    fout1 = open("phase1_pooling_result_time_sorted.txt", "w")
    fout2 = open("phase1_pooling_result_time_sorted_id.txt", "w")
    for line in fphase1:
        news = line.strip().split(" ")
        newstime = list()
        for i in news:
            newstime.append(getTime(i))
        sortednews = sorted(zip(news, newstime), key=lambda x:x[1])
        for t in sortednews:
            fout1.write(str(t[1]) + " ")
            fout2.write(str( datetime.datetime.fromtimestamp(float(t[1])).strftime('%Y-%m-%d')) + " ")
        fout1.write('\n')
        fout2.write('\n')
    fphase1.close()
    fout1.close()
    fout2.close()
