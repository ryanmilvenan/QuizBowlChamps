#NLP Test Algorithms

from collections import defaultdict
from collections import Counter
from csv import DictReader, DictWriter
from sets import Set

import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.classify import PositiveNaiveBayesClassifier
from nltk.util import ngrams

train = DictReader(open("train.csv", 'r'))
#Fields:
#Question, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category


#Finds the max value given a dictionary and return the key
def maxScore(d):
	v=list(d.values())
	k=list(d.keys())
	return k[v.index(max(v))]


## This section just uses the top score of each answer generator as
## the answer we're submitting
cIR=0
cQ=0
match=0
cTotal=0
for ii in train:

	#Check top value of QANTA and IR accuracy
	if re.split(':',re.split(',',ii['IR_Wiki Scores'])[0])[0]==ii['Answer']:
		cIR+=1
		if re.split(':',re.split(',',ii['QANTA Scores'])[0])[0]==ii['Answer']:
			match+=1
	if re.split(':',re.split(',',ii['QANTA Scores'])[0])[0]==ii['Answer']:
		cQ+=1

	cTotal+=1

print "Accuracy IR = ",float(cIR)/float(cTotal)
print "Accuracy QANTA = ",float(cQ)/float(cTotal)
print "QANTA and IR match and are correct = ",float(match)/float(cTotal)


##This section uses every word of the text + QANTA + IR scores to pick answer
#Fields:
#Question, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category


train2 = DictReader(open("train.csv", 'r'))
#Using this counter to look at the first few questions only
i=0;

# Split off dev section
dev_train = []
dev_test = []
full_train = []
textFull = defaultdict(lambda: defaultdict(int))
answer=[]

#make a defaultdict of default dicts to store all data with answers
# d['the']['carthage']+=1  increment dictionary carthage within
# dictionary the by 1
text = defaultdict(lambda: defaultdict(int))
words=[]

for ii in train2:
	# if i>0:
	# 	break
	if i%5!=0:
		#Split on everything that isn't alpha-numeric
		words=re.split('\W+',ii['Question Text'].lower())
		# print words
		for kk in words:
			text[kk][ii['Answer']]+=1
		# i+=1

		# print re.split(',',re.sub(':',',',re.sub(' ','',ii['QANTA Scores'])))
		# print re.split(',',re.sub(':',',',re.sub(' ','',ii['IR_Wiki Scores'])))
		# print re.split(',',re.sub(' ','',ii['QANTA Scores']))
	words=re.split('\W+',ii['Question Text'].lower())
	for kk in words:
		textFull[kk][ii['Answer']]+=1
	i+=1

##examples of how to access the dictionaries
# print text['it'] 
# print text['it']['carthage']

#Actually run the algorithm 
train3 = DictReader(open("train.csv", 'r'))
totalQuestions=0
cCorrect=0
cCorrect2=0
i=0
Q=[]
QANTA={}
qScore=0.0
I=[]
IR={}
irScore=0.0
textScore=0.0
totalScore=0.0
totalScoreList={}
totalScore2=0.0
totalScoreList2={}

pred={}


for ii in train3:
	if i%5==0:
		totalQuestions+=1
		qScore=0.0
		textScoreQANTA=0.0
		irScore=0.0
		textScoreIR=0.0
		answerSet=Set()
		totalScoreList={}
		Q=re.split(',',re.sub(',_','_',re.sub(':',',',re.sub(' ','',ii['QANTA Scores']))))
		I=re.split(',',re.sub(',_','_',(re.sub(':',',',re.sub(' ','',ii['IR_Wiki Scores'])))))

		# print I
		# QANTA=re.split(',',re.sub(' ','',ii['QANTA Scores']))
		#Use top 5 scores
		for kk in range(0,20):
			QANTA[Q[kk*2]]=Q[kk*2+1]
			IR[I[kk*2]]=I[kk*2+1]

		for kk in range(0,5):
			answerSet.add(Q[kk*2])
			answerSet.add(I[kk*2])
			

		for answer in answerSet:
			# print answer
			textScore=0.0

			#Get QANTA and IR scores
			try:
				qScore=float(QANTA[answer])
			except KeyError:
				qScore=0.0
			try:
				irScore=float(IR[answer])
			except KeyError:
				irScore=0.0

			#Get text score
			for word in re.split('\W+',ii['Question Text'].lower()):
				textScore+=text[word][answer]
			# print 'qScore=',qScore, 'irScore=',irScore, 'textScore=',textScore

			##Scoring algorithm:
			##with text = IR+QANTA*20+textscores/200, change as necessary
			totalScore=irScore+qScore*20+textScore/200
			totalScoreList[answer]=totalScore

			# ##without text = IR+QANTA*20
			# totalScore2=irScore+qScore*20
			# totalScoreList2[answer]=totalScore2			

		
		#Calc final answer
		if maxScore(totalScoreList)==ii['Answer']:
			cCorrect+=1
		# 	cCorrect2+=1

print "Accuracy with text = ", float(cCorrect)/float(totalQuestions)



# print 'ScoreList=',totalScoreList
# print maxScore(totalScoreList)



test1 = DictReader(open("test.csv", 'r'))
totalQuestions=0
cCorrect=0
cCorrect2=0
i=0
Q=[]
QANTA={}
qScore=0.0
I=[]
IR={}
irScore=0.0
textScore=0.0
totalScore=0.0
totalScoreList={}
totalScore2=0.0
totalScoreList2={}

test={}


for ii in test1:
	totalQuestions+=1
	qScore=0.0
	textScoreQANTA=0.0
	irScore=0.0
	textScoreIR=0.0
	answerSet=Set()
	totalScoreList={}
	Q=re.split(',',re.sub(',_','_',re.sub(':',',',re.sub(' ','',ii['QANTA Scores']))))
	I=re.split(',',re.sub(',_','_',(re.sub(':',',',re.sub(' ','',ii['IR_Wiki Scores'])))))

	# print I
	# QANTA=re.split(',',re.sub(' ','',ii['QANTA Scores']))
	#Use top 5 scores
	for kk in range(0,20):
		QANTA[Q[kk*2]]=Q[kk*2+1]
		IR[I[kk*2]]=I[kk*2+1]

	for kk in range(0,5):
		answerSet.add(Q[kk*2])
		answerSet.add(I[kk*2])
		

	for answer in answerSet:
		# print answer
		textScore=0.0

		#Get QANTA and IR scores
		try:
			qScore=float(QANTA[answer])
		except KeyError:
			qScore=0.0
		try:
			irScore=float(IR[answer])
		except KeyError:
			irScore=0.0

		#Get text score
		for word in re.split('\W+',ii['Question Text'].lower()):
			textScore+=text[word][answer]

		
		# print 'qScore=',qScore, 'irScore=',irScore, 'textScore=',textScore

		##Scoring algorithm:
		##with text = IR+QANTA*20+textscores/200, change as necessary
		totalScore=irScore+qScore*20+textScore/200
		totalScoreList[answer]=totalScore

		# ##without text = IR+QANTA*20
		# totalScore2=irScore+qScore*20
		# totalScoreList2[answer]=totalScore2			
	#Calc final answer
	test[ii['Question ID']] = maxScore(totalScoreList)
	# 	cCorrect2+=1





# Write predictions
o = DictWriter(open('pred.csv', 'w'), ['id', 'pred'])
o.writeheader()
for ii in sorted(test):
    o.writerow({'id': ii, 'pred': test[ii]})
