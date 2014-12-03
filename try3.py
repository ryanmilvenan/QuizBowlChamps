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
test={}
categories=['lit','history','social','science']
for cat in categories:
	print "Categoy = ", cat
	train = DictReader(open("train.csv", 'r'))

	#make a defaultdict of default dicts to store all data with answers
	# d['the']['carthage']+=1  increment dictionary carthage within
	# dictionary the by 1
	text = defaultdict(lambda: defaultdict(int))
	bigrams = defaultdict(lambda: defaultdict(int))
	trigrams = defaultdict(lambda: defaultdict(int))
	words=[]
	bi=[]
	tri=[]

	#New features can be inserted and trained in this loop
	for ii in train:
		if ii['category']==cat:
			#Split on everything that isn't alpha-numeric
			words=re.split('\W+',ii['Question Text'].lower())

			#Associate words with the correct answer
			for kk in words:
				text[kk][ii['Answer']]+=1

			# bigrams of letters counter
			bi=ngrams(nltk.word_tokenize(ii['Question Text'].lower()),2)
			for kk in bi:
				bigrams[kk][ii['Answer']]+=1

			# trigrams of letters counter
			tri=ngrams(ii['Question Text'].lower(),3)
			for kk in tri:
				trigrams[kk][ii['Answer']]+=1

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
	biScore=0.0
	triScore=0.0
	#Dictionary containing the scores of all possible answers
	totalScoreList={}
	#Dictionary to store question id and associated answer
	

	if cat=='lit':
		qWeight=10.0
		irWeight=0.6
		textWeight=1.0/300.0
		biWeight=1.0
		triWeight=0.001
	elif cat=='history':
		qWeight=10.0
		irWeight=1.2
		textWeight=1.0/300.0
		biWeight=1.0
		triWeight=0.0
	elif cat=='social':
		qWeight=10.0
		irWeight=1.2
		textWeight=1.0/1000.0
		biWeight=1.0
		triWeight=0.00001
	elif cat=='science':
		qWeight=10.0
		irWeight=0.0
		textWeight=1.0/100.0
		biWeight=1.0
		triWeight=0.001
	print "Weights = ", qWeight,irWeight,textWeight,biWeight,triWeight
	for ii in testFile:
		if ii['category']==cat:
			totalQuestions+=1
			qScore=0.0
			irScore=0.0
			answerSet=Set() #I put possible answers in a set to avoid duplicates
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

			
			for kk in range(0,20):
				QANTA[Q[kk*2]]=Q[kk*2+1]
				IR[I[kk*2]]=I[kk*2+1]

			#Use top 5 scores
			for kk in range(0,3):
				answerSet.add(Q[kk*2])
				answerSet.add(I[kk*2])
				
			#Loop over every answer to and calculate score, put score in dictionary
			#Additional featurs can be added in this loop
			for answer in answerSet:
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
				for gram in ngrams(nltk.word_tokenize(ii['Question Text'].lower()),2):
					biScore+=bigrams[gram][answer]

				#Get trigrams score
				for gram in ngrams(ii['Question Text'].lower(),3):
					triScore+=trigrams[gram][answer]

				##Scoring algorithm:
				##with text = ir*irweight+qanta*qantaweight+text*textweight+...feature*featureweight
				totalScore=irScore*irWeight+qScore*qWeight+textScore*textWeight+biScore*biWeight+triScore*triWeight
				#Put score for specific answer in dictionary
				totalScoreList[answer]=totalScore	

			#Associate the question ID with the best answer
			test[ii['Question ID']]=maxScore(totalScoreList)

# Write predictions
o = DictWriter(open('pred.csv', 'wb'), ['Question ID', 'Answer'])
o.writeheader()
for ii in sorted(test):
    o.writerow({'Question ID': ii, 'Answer': test[ii]})
