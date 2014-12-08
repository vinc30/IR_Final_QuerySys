#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def spli(s):
#s = sys.argv[1]
#    print s
    slist = []
    keys = []
    temp=''
    for i in s:
        if not isinstance(i,unicode):
            i = i.decode("utf-8")
#  print i
        if(check_contain_chinese(i)):
            if (temp<>''):
                slist.append(temp)
                key = '%X' %ord(i)
                keys.append(key)
                temp = ''
            slist.append(i)
            key = '%X' % ord(i)
            keys.append(key)
        else :
            if(i!=' '):
                temp+=i
            else: 
                slist.append(temp)
                key = '%X' %ord(i)
                keys.append(key)
                temp = ''
    if (temp<>''):
        slist.append(temp)
        key = '%X' %ord(i)
        keys.append(key)
        temp = ''
    return slist
#for i in range(0,len(slist)):
#       print slist[i]
#return slist
#if(u'北' in slist[i]):
#       print "haha"
#   else:
#       print "QQ"
#print len(slist)
#print slist

#print len(keys)
#print keys
