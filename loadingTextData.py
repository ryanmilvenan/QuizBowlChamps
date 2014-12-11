from csv import DictReader, DictWriter
from collections import defaultdict
import re


train = DictReader(open("predScienceText.csv", 'r'))
textData=defaultdict()
for ii in train:
		# correctAnswerSet.add(ii['Answer'])
	textData[ii['Question ID']]=ii['Answer']
	# print ii

print textData['8932']
answers=re.split(')',textData['8932'])
print answers
# for ii in textData['8932']:
# 	print ii