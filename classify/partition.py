import shutil
import os, sys
from glob import glob
from random import shuffle
src = 'traindata/'
dst = 'train/'

count0 = 0
count1 = 0
count2 = 0
DATA0 = 'traindata/0/*'
DATA1 = 'traindata/1/*'
DATA2 = 'traindata/2/*'
temp=glob(DATA0)
shuffle(temp)
for f in temp:
	if count0<24000:
		shutil.copy2(f, dst+'0/')
		count0+=1
	elif count0>=24000:
		shutil.copy2(f, 'test/0/')
temp=glob(DATA1)
shuffle(temp)
for f in temp:
	if count1<24000:
		shutil.copy2(f, dst+'1/')
		count1+=1
	elif count1>=24000:
		shutil.copy2(f, 'test/1/')
temp=glob(DATA2)
shuffle(temp)
for f in temp:
	if count2<24000:
		shutil.copy2(f, dst+'2/')
		count2+=1
	elif count2>=24000:
		shutil.copy2(f, 'test/2/')
