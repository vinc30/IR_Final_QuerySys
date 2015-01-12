import shutil
import os, sys
#path = '/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/database/0'
#os.mkdir( path, 0755 );
#path = '/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/database/1'
#os.mkdir( path, 0755 );
#path = '/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/database/2'
#os.mkdir( path, 0755 );
src = '/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/database/news_random_id_unlabeled_new/'
dst = '/Users/wupoyu/Desktop/IR/github/IR_Final_QuerySys/database/'
f = open('../news_to_news_random_id_unlabeled_table_groundtruth_no_original_id.txt','r')  #need to change file path
for line in f:
    line = line.split()
    date = line.pop()
    news = line.pop()
    num_id = line.pop()
    shutil.copy2(src+num_id, dst+news)
