#!/usr/bin/env python  
# -*- coding: UTF-8  -*-  
import os 
import sys
import split
from glob import glob 
from bs4 import BeautifulSoup
#import xml.etree.ElementTree as ET  
reload(sys)
sys.setdefaultencoding('utf8')
def load_xml_file(filename):
#    print root.tag    
    slist = []
#    tree =  ET()
#   tree = ET.parse(filename)
#    print root.tag
#temp = root[0][1]
#   print tree.tag
#    count =0
    string = open(filename).read()
    soup = BeautifulSoup(string)
    for i in soup.findAll('p'):
        content = i.get_text()
#       print s1
        if content is None:
            pass
        else :
            slist+=split.spli(content)
#       count +=1
#       if count==3:
#           break
#        for i in range(0,len(slist)):
#           if(test_word in slist[i]):
#               print slist[i],"yaya"
#       `    else :
#               print slist[i]
#    for i in range(0,len(slist)):
#       print slist[i]
    return slist
"""
    for i in range(0,len(slist)):
        print slist[i]"""    
#str_symptom = str(li).replace('u\'','\'')
#       str_symptom.decode("utf8-escape")
#        temp = [x.encode('utf-8') for x in li]
if __name__ == '__main__':
#    f = open('query.txt')
#   for l in f:
#       temp_test=l.strip().split(' ').pop()
#       break
#   for i in temp_test:
#       temp_test.replace(" ","")
# print temp_test
    DATA = '/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/database/*'
    for f in glob(DATA):
        load_xml_file(f)
#    load_xml_file("database/100180")
