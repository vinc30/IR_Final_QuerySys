from bs4 import BeautifulSoup
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
train = []
# f = open('news_to_news_random_id_unlabeled_table_groundtruth_no_original_id.txt','r')  #need to change file path
f = open('/home/urjeans/ir/news_to_news_random_id_unlabeled_table_groundtruth_no_original_id.txt','r')  #need to change file path
for line in f:
    content =""
    line = line.split()
    date = line.pop()
    news = line.pop()
    num_id = line.pop()
    print num_id
    fp = open('../github/IR_Final_QuerySys/database/news_random_id_unlabeled_new/'+ num_id,'r') #need to chnage file path
    soup = BeautifulSoup(fp)
    content+=soup.find('title').get_text()
    for i in soup.findAll('p'):
        content += i.get_text()
    train.append( (content,int(news)) )
    fp.close()
#print w
cl = NaiveBayesClassifier(train)
print ('done')
content = ""
fp = open('../github/IR_Final_QuerySys/database/news_random_id_unlabeled_new/67065','r') # need to change file path
soup = BeautifulSoup(fp)
content+=soup.find('title').get_text()
for i in soup.findAll('p'):
    content += i.get_text()
print (cl.classify(content))
content = ""
fp = open('../github/IR_Final_QuerySys/database/news_random_id_unlabeled_new/47238','r') # need to change file path
soup = BeautifulSoup(fp)
content+=soup.find('title').get_text()
for i in soup.findAll('p'):
    content += i.get_text()
print (cl.classify(content))
content = ""
fp = open('../github/IR_Final_QuerySys/database/news_random_id_unlabeled_new/29169','r')  # need to change file path
soup = BeautifulSoup(fp)
content+=soup.find('title').get_text()
for i in soup.findAll('p'):
    content += i.get_text()
print (cl.classify(content))
