#NLP Test Algorithms

from collections import defaultdict
from collections import Counter
from csv import DictReader, DictWriter
from sets import Set

import re
import nltk
from nltk import FreqDist
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.classify import PositiveNaiveBayesClassifier
from nltk.util import ngrams

train = DictReader(open("train.csv", 'r'))
#Fields:
#Question ID, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category


#Finds the max value given a dictionary and return the key
def maxScore(d):
	v=list(d.values())
	k=list(d.keys())
	return k[v.index(max(v))]

################################################################
## This section just uses the top score of each answer generator as
## the answer we're submitting
cIR=0
cQ=0
cEither=0
match=0
cTotal=0
fdist=FreqDist()
for ii in train:
	either=0
	#Check top value of QANTA and IR accuracy
	if re.split(':',re.split(',',ii['IR_Wiki Scores'])[0])[0]==ii['Answer']:
		cIR+=1
		either+=1
		if re.split(':',re.split(',',ii['QANTA Scores'])[0])[0]==ii['Answer']:
			match+=1
	if re.split(':',re.split(',',ii['QANTA Scores'])[0])[0]==ii['Answer']:
		cQ+=1
		either+=1
	if either>0:
		cEither+=1
	fdist[ii['Answer']]+=1


	cTotal+=1
# print fdist.most_common(100)
# fdist.tabulate()
print "Accuracy IR = ",float(cIR)/float(cTotal)
print "Accuracy QANTA = ",float(cQ)/float(cTotal)
print "QANTA or IR match and are correct = ",float(cEither)/float(cTotal)
print "QANTA and IR match and are correct = ",float(match)/float(cTotal)




######################################################
scoreInQANTAorIR=0.0
train1 = DictReader(open("train.csv", 'r'))
for ii in train1:

	Q=[]
	I=[]
	counter=0 #This is used in case the first item has a comma before a :
	#for example 'charles,_evans_hughes:5.03163689658' would mess up without it

	#BUNCH OF DATA PROCESSING!
	Q3=ii['QANTA Scores']
	Q2=re.split(':',Q3)
	for item in Q2:
		if counter>0:
			Q1=re.split(',',item,1) #split on first comma only!
			for ele in Q1:
				Q.append(re.sub(' ','',ele))
		else:
			Q.append(item)
		counter=1
	counter=0
	# print Q
	I3=ii['IR_Wiki Scores']
	I2=re.split(':',I3)
	for item in I2:
		if counter>0:
			I1=re.split(',',item,1) #split on first comma only!
			for ele in I1:
				I.append(re.sub(' ','',ele))
		else:
			I.append(item)
		counter=1


	#Use top 5 scores
	for kk in range(0,20):

		if (Q[kk*2]==ii['Answer']) or (I[kk*2]==ii['Answer']):
			scoreInQANTAorIR+=1
			break
		
print "Answer in any QANTA or IR options = ",float(scoreInQANTAorIR)/float(cTotal)

#######################################################
train2 = DictReader(open("train.csv", 'r'))

##This section uses every word of the text + QANTA + IR scores to pick answer
#Fields:
#Question ID, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category
#Using this counter to look at the first few questions only
i=0;

# textFull = defaultdict(lambda: defaultdict(int))
answer=[]

#make a defaultdict of default dicts to store all data with answers
# d['the']['carthage']+=1  increment dictionary carthage within
# dictionary the by 1
text = defaultdict(lambda: defaultdict(int))
bigrams = defaultdict(lambda: defaultdict(int))
trigrams = defaultdict(lambda: defaultdict(int))
words=[]
bi=[]

for ii in train2:
	# if i>0:
	# 	break
	if i%5!=0:
		# word counter
		#Split on everything that isn't alpha-numeric
		words=re.split('\W+',ii['Question Text'].lower())
		for kk in words:
			text[kk][ii['Answer']]+=1

		# bigrams of letters counter
		bi=ngrams(ii['Question Text'].lower(),2)
		for kk in bi:
			bigrams[kk][ii['Answer']]+=1

		# trigrams of letters counter
		tri=ngrams(ii['Question Text'].lower(),3)
		for kk in tri:
			trigrams[kk][ii['Answer']]+=1
		# print re.split(',',re.sub(':',',',re.sub(' ','',ii['QANTA Scores'])))
		# print re.split(',',re.sub(':',',',re.sub(' ','',ii['IR_Wiki Scores'])))
		# print re.split(',',re.sub(' ','',ii['QANTA Scores']))
	# words=re.split('\W+',ii['Question Text'].lower())
	# for kk in words:
	# 	textFull[kk][ii['Answer']]+=1
	i+=1

##examples of how to access the dictionaries
# print text['it'] 
# print text['it']['carthage']

#Actually run the algorithm 
train3 = DictReader(open("train.csv", 'r'))
totalQuestions=0
cCorrect=0
i=0
Q=[]
QANTA={}
qScore=0.0
I=[]
IR={}
irScore=0.0
textScore=0.0
biScore=0.0
totalScore=0.0
totalScoreList={}

qWeight=50.0
irWeight=0.08
textWeight=1.0/50.0
# textWeight=0
biWeight=0.0000333333
triWeight=0.00025


for ii in train3:
	# print ii['Question ID']
	if i%5==0:
		totalQuestions+=1
		qScore=0.0
		irScore=0.0
		answerSet=Set()
		totalScoreList={}
		Q=[]
		I=[]
		counter=0 #This is used in case the first item has a comma before a :
		#for example 'charles,_evans_hughes:5.03163689658' would mess up without it

		#BUNCH OF DATA PROCESSING!
		Q3=ii['QANTA Scores']
		Q2=re.split(':',Q3)
		for item in Q2:
			if counter>0:
				Q1=re.split(',',item,1) #split on first comma only!
				for ele in Q1:
					Q.append(re.sub(' ','',ele))
			else:
				Q.append(item)
			counter=1
		counter=0
		# print Q
		I3=ii['IR_Wiki Scores']
		I2=re.split(':',I3)
		for item in I2:
			if counter>0:
				I1=re.split(',',item,1) #split on first comma only!
				for ele in I1:
					I.append(re.sub(' ','',ele))
			else:
				I.append(item)
			counter=1


		#Use top 5 scores
		for kk in range(0,20):
			QANTA[Q[kk*2]]=Q[kk*2+1]
			IR[I[kk*2]]=I[kk*2+1]

		for kk in range(0,1):
			answerSet.add(Q[kk*2])
			answerSet.add(I[kk*2])
			

		for answer in answerSet:
			# print answer
			textScore=0.0
			biScore=0.0
			triScore=0.0

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

			#Get bigrams score
			for gram in ngrams(ii['Question Text'].lower(),2):
				biScore+=bigrams[gram][answer]

			#Get bigrams score
			for gram in ngrams(ii['Question Text'].lower(),3):
				triScore+=trigrams[gram][answer]

			# print 'qScore=',qScore*qWeight, 'irScore=',irScore*irWeight, 'textScore=',textScore*textWeight, "biScore=", biScore*biWeight
			# print 'qScore=',qScore, 'irScore=',irScore, 'textScore=',textScore, "biScore=", biScore

			##Scoring algorithm:
			##with text = IR*w1+QANTA*w2+textscores*w3+bigram*w4
			totalScore=irScore*irWeight+qScore*qWeight+textScore*textWeight+biScore*biWeight+triScore*triWeight
			# totalScore=irScore*irWeight+qScore*qWeight+textScore*textWeight
			# totalScore=irScore*irWeight+qScore*qWeight
			totalScoreList[answer]=totalScore

		
		#Calc final answer
		if maxScore(totalScoreList)==ii['Answer']:
			cCorrect+=1
		# else:
			# print maxScore(totalScoreList), ii['Answer']
	i+=1

print "Accuracy with text = ", float(cCorrect)/float(totalQuestions)



