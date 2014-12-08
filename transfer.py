#!/usr/bin/env python  
# -*- coding: UTF-8  -*-  
import os 
import sys
import split
from glob import glob 
import xml.etree.ElementTree as ET  
reload(sys)
sys.setdefaultencoding('utf8')
def load_xml_file(filename,test_word):
#    print root.tag    
#    workpath = os.getcwd()
    slist = []
    root = ET.parse(filename).getroot()
    temp = root[0][2]
    for child in temp:
        s1 = child.text
#print s1
        if s1 is None:
            pass
        else :
            slist+=split.spli(s1)
#        for i in range(0,len(slist)):
#           if(test_word in slist[i]):
#               print slist[i],"yaya"
#       `    else :
#               print slist[i]
#    for i in range(0,len(slist)):
#       print slist[i]
    return slist
#str_symptom = str(li).replace('u\'','\'')
#       str_symptom.decode("utf8-escape")
#        temp = [x.encode('utf-8') for x in li]
if __name__ == '__main__':
    f = open('query.txt')
#   for l in f:
#       temp_test=l.strip().split(' ').pop()
#       break
#   for i in temp_test:
#       temp_test.replace(" ","")
# print temp_test
    workpath = os.getcwd()
#    DATA = '/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/database/*'
#   for f in glob(DATA):
    load_xml_file("database/100093" ,u"億")
