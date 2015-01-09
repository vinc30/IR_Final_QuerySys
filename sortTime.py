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



def getTime(article):
    """
    Do something to get the lastest date in the article, in Unix Time form (a.k.a. seconds from 1970/1/1)
    """
    # Warning: mx.Datetime.now() should be replaced with some other time in 2014!!!!
    tagged = timex.ground(timex.tag(article), mx.DateTime.now())
    # example: tagged = u'<TIMEX2 val="2014W52">last week</TIMEX2>'
    soup = BeautifulSoup(tagged)
    if soup.timex2 == None:
        print("OMG can you believe that! This article has no time tags!==\n" + article + "\n==end of article").encode('utf-8')
        # print("OMG no tags!")
        return int(random.randint(1370016000,1416758400))
    else:
        tagtimes = list()
        for i in soup.findAll('timex2'):
            timestr = i['val']
            if timestr != 'UNKNOWN':
                tagtimes.append(int(dateutil.parser.parse(timestr).strftime('%s')))
            else:
                print i
        if tagtimes != list():
            return np.array(tagtimes).min()
        else:
            return 0



def file2str(filename):
    """
    Given the article name
    Do something to return the whole article without any <tag>
    """
    assert exists(join("database", filename)), "Error: FILE " + join("database", filename) + " is missing "
    fp = open(join("database", filename))
    soup = BeautifulSoup(fp)
    content = ""
    content +=soup.find('title').get_text()
    for i in soup.findAll('p'):
            content +=i.get_text()
    return content


if __name__ == "__main__":
    fphase1 = open("phase1_pooling_result.txt", "r")
    fout = open("phase1_pooling_result_time_sorted.txt", "w")
    for line in fphase1:
        news = line.strip().split(" ")
        newstime = list()
        for i in news:
            newstime.append(getTime(file2str(i)))
        sortednews = sorted(zip(news, newstime), key=lambda x:x[1])
        for t in sortednews:
            fout.write(str(t[1]) + " ")
        fout.write('\n')
