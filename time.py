import jieba.posseg as pseg
from bs4 import BeautifulSoup
f = open('./phase1_pooling_result.txt')
for line in f:
	#str = f. readline()
	tmp = line.split()
	for i in tmp:
		fp =open('../../news_random_id_unlabeled_new/'+i)
		soup = BeautifulSoup(fp)
		content = ""
		print i
		for s in soup.findAll('p'):
			content +=s.get_text()
		words = pseg.cut(content)
		fp.close()
		for w in words:
			if w.flag =='t' or w.flag=='tg':
				print w.word
		print "\n"
