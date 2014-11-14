#NLP Test Algorithms
# For the actual test file

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


#Finds the max value given a dictionary and return the key
def maxScore(d):
	v=list(d.values())
	k=list(d.keys())
	return k[v.index(max(v))]

########### PART 1 : Training #########################
#Fields:
#Question ID, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category

train = DictReader(open("train.csv", 'r'))

#make a defaultdict of default dicts to store all data with answers
# d['the']['carthage']+=1  increment dictionary carthage within
# dictionary the by 1
text = defaultdict(lambda: defaultdict(int))
words=[]

#New features can be inserted and trained in this loop
for ii in train:
	#Split on everything that isn't alpha-numeric
	words=re.split('\W+',ii['Question Text'].lower())
	#Associate words with the correct answer
	for kk in words:
		text[kk][ii['Answer']]+=1

########## PART 2 : Run on test file ####################
testFile = DictReader(open("test.csv", 'r'))

totalQuestions=0 #Total number of questions
Q=[] #I put the QANTA scores into a list for editing
QANTA={} #Then I associate the keys(answers) with the values(scores)
qScore=0.0 #QANTA score for given answer
I=[] #I put the IR scores into a list for editing
IR={} #Then I associate the keys(answers) with the values(scores)
irScore=0.0 #IR score for given answer
textScore=0.0 #Score for simple counter
totalScore=0.0 #Score of all features*weights for a given answer
#Dictionary containing the scores of all possible answers
totalScoreList={}
#Dictionary to store question id and associated answer
test={}



for ii in testFile:
	totalQuestions+=1
	qScore=0.0
	irScore=0.0
	answerSet=Set() #I put possible answers in a set to avoid duplicates
	totalScoreList={}
	Q=re.split(',',re.sub(',_','_',re.sub(':',',',re.sub(' ','',ii['QANTA Scores']))))
	I=re.split(',',re.sub(',_','_',(re.sub(':',',',re.sub(' ','',ii['IR_Wiki Scores'])))))

	
	for kk in range(0,20):
		QANTA[Q[kk*2]]=Q[kk*2+1]
		IR[I[kk*2]]=I[kk*2+1]

	#Use top 5 scores
	for kk in range(0,5):
		answerSet.add(Q[kk*2])
		answerSet.add(I[kk*2])
		
	#Loop over every answer to and calculate score, put score in dictionary
	#Additional featurs can be added in this loop
	for answer in answerSet:
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
		##with text = IR+QANTA*2+textscores/200, change as necessary
		totalScore=irScore+qScore*2+textScore/200
		#Put score for specific answer in dictionary
		totalScoreList[answer]=totalScore	

	#Associate the question ID with the best answer
	test[ii['Question ID']]=maxScore(totalScoreList)

# Write predictions
o = DictWriter(open('pred.csv', 'wb'), ['id', 'pred'])
o.writeheader()
for ii in sorted(test):
    o.writerow({'id': ii, 'pred': test[ii]})
