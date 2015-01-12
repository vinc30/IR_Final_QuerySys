from dateutil import parser
f = open('news_to_news_random_id_unlabeled_table_groundtruth_no_original_id.txt')
dic = dict()
for line in f:
    str = line.split()
    temp =str.pop()
    temp2 = str.pop()
    temp3 = str.pop()
    dic[temp3] = temp
fTA = open('phase1_pooling_result.txt')
f.close()
f = open('hw119399_b00902047_1e4e4e55a9191d3_1.txt')
fout = open('eva.txt','w')
for i in range(20):
    dic_test=dict()
    str1 =fTA.readline()
    str2 =f.readline()
    string = str2.split()
    strTA = str1.split()
    for j in string:
        if j in strTA:
            pass
        else:
	    try:
	        dic_test[j]= dic[j]
	    except KeyError:
		pass
    for j in dic_test:
	dic_result= sorted(dic_test.iteritems(), key=lambda d:d[1], reverse = False)
    for j in dic_result:
	fout.write("%s "%j[0])
    fout.write('\n')
fout.close()
fTA.close()
f.close()
