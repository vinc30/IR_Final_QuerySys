import sklearn.datasets
import sys,os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from bs4 import BeautifulSoup
import numpy as np
from sklearn import metrics
#from sklearn.linear_model import SGDClassifier
train = sklearn.datasets.load_files(sys.argv[1],encoding='utf-8')
print "load done"
twenty_test = sklearn.datasets.load_files('classify/test',encoding='utf-8')
docs_test = twenty_test.data

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train.data)
tf_transformer = TfidfTransformer(use_idf=True).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, train.target)
#clf = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5)
f = open(sys.argv[2])#'/home/guest/ir/git/IR_Final_QuerySys/phase1_pooling_result.txt')
count = 1
fwrite= open('result_newspaper.txt','w')
for line in f:
	string = line.split(' ')
	fwrite.write('%d\n' %(count))
	for x in string:
		content = ""
		if x =='\n':
			continue
		fp = open(sys.argv[3]+x)#'/home/guest/ir/news_random_id_unlabeled_new/'+x)
		soup = BeautifulSoup(fp)
		content+=soup.find('title').get_text()
		for i in soup.findAll('p'):
			content += i.get_text()
		
#content = fp.read()
		docs_new = [content]
		X_new_counts = count_vect.transform(docs_new)
		X_new_tfidf = tfidf_transformer.transform(X_new_counts)
		predicted = clf.predict(X_new_tfidf)
		for doc, category in zip(docs_new, predicted):
			fwrite.write('%s %s ' %(x,train.target_names[category]))
		#print('%s => %s' % (x,train.target_names[category]))
	count += 1
	fwrite.write('\n')
f.close()
fwrite.close()

X_new_counts = count_vect.transform(docs_test)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
predicted = clf.predict(X_new_tfidf)
print np.mean(predicted == twenty_test.target)
print(metrics.classification_report(twenty_test.target, predicted,target_names=twenty_test.target_names))
print metrics.confusion_matrix(twenty_test.target, predicted)
