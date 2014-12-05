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
# cIR=0
# cQ=0
# cEither=0
# match=0
# cTotal=0
# fdist=FreqDist()
# for ii in train:
# 	if (ii['category']=='social'):
# 		either=0
# 		#Check top value of QANTA and IR accuracy
# 		if re.split(':',re.split(',',ii['IR_Wiki Scores'])[0])[0]==ii['Answer']:
# 			cIR+=1
# 			either+=1
# 			if re.split(':',re.split(',',ii['QANTA Scores'])[0])[0]==ii['Answer']:
# 				match+=1
# 		if re.split(':',re.split(',',ii['QANTA Scores'])[0])[0]==ii['Answer']:
# 			cQ+=1
# 			either+=1
# 		if either>0:
# 			cEither+=1
# 		fdist[ii['Answer']]+=1


# 		cTotal+=1
# # print fdist.most_common(100)
# # fdist.tabulate()
# # print "cTotal = ",cTotal
# print "Accuracy IR top pick = ",float(cIR)/float(cTotal)
# print "Accuracy QANTA top pick = ",float(cQ)/float(cTotal)
# print "QANTA or IR top pick match and are correct = ",float(cEither)/float(cTotal)
# print "QANTA and IR top pick match and are correct = ",float(match)/float(cTotal)




# ######################################################
# scoreInQANTAorIR=0.0
# scoreInTop5=0.0
# scoreInTop10=0.0
# train1 = DictReader(open("train.csv", 'r'))
# for ii in train1:
# 	if (ii['category']=='science'):


# 		Q=[]
# 		I=[]
# 		counter=0 #This is used in case the first item has a comma before a :
# 		#for example 'charles,_evans_hughes:5.03163689658' would mess up without it

# 		#BUNCH OF DATA PROCESSING!
# 		Q3=ii['QANTA Scores']
# 		Q2=re.split(':',Q3)
# 		for item in Q2:
# 			if counter>0:
# 				Q1=re.split(',',item,1) #split on first comma only!
# 				for ele in Q1:
# 					Q.append(re.sub(' ','',ele))
# 			else:
# 				Q.append(item)
# 			counter=1
# 		counter=0
# 		# print Q
# 		I3=ii['IR_Wiki Scores']
# 		I2=re.split(':',I3)
# 		for item in I2:
# 			if counter>0:
# 				I1=re.split(',',item,1) #split on first comma only!
# 				for ele in I1:
# 					I.append(re.sub(' ','',ele))
# 			else:
# 				I.append(item)
# 			counter=1


# 		#Use top 5 scores
# 		for kk in range(0,20):

# 			if (Q[kk*2]==ii['Answer']) or (I[kk*2]==ii['Answer']):
# 				scoreInQANTAorIR+=1
# 				break
# 		for kk in range(0,5):
# 			if (Q[kk*2]==ii['Answer']) or (I[kk*2]==ii['Answer']):
# 				scoreInTop5+=1
# 				break
# 		for kk in range(0,10):
# 			if (Q[kk*2]==ii['Answer']) or (I[kk*2]==ii['Answer']):
# 				scoreInTop10+=1
# 				break

# print "Answer in any QANTA or IR top 5 = ",float(scoreInTop5)/float(cTotal)
# print "Answer in any QANTA or IR top 10 = ",float(scoreInTop10)/float(cTotal)
# print "Answer in any QANTA or IR options (top 20) = ",float(scoreInQANTAorIR)/float(cTotal)

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
bigrams = defaultdict(lambda: defaultdict(int)) #of words
trigrams = defaultdict(lambda: defaultdict(int)) #of letters
words=[]
bi=[]
tri=[]
correctAnswerSet=Set()

for ii in train2:
	# if i>0:
	# 	break
	# correctAnswerSet.add(ii['Answer'])
	if int(ii['Question ID'])%5!=0:
		if (ii['category']=='history'):
			correctAnswerSet.add(ii['Answer'])
			# word counter
			#Split on everything that isn't alpha-numeric
			words=re.split('\W+',ii['Question Text'].lower())
			for kk in words:
				stem = wn.morphy(kk)
				if stem==None:
					1
				else:
					text[stem][ii['Answer']]+=1
				# text[kk][ii['Answer']]+=1

			# bigrams of words counter
			bi=ngrams(nltk.word_tokenize(ii['Question Text'].lower()),2)
			for kk in bi:
				# print kk
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
inAnswerSet=0
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


zeroToFour=0.0
fourToEight=0.0
eightToTwelve=0.0
twelvePlus=0.0

zeroToFourTotal=0.0
fourToEightTotal=0.0
eightToTwelveTotal=0.0
twelvePlusTotal=0.0


#8160 total probs,1632
#science: q=10.0,ir=0.02,text=1/1500,bi=0.00075,tri=0.00001,ias=2,nias=-1,top 3 ans, 0.66341
#1055 probs,211 tested

#lit: q=10,ir=1.2,text=1/5000,bi=0.02,tri=0.001,ias=0,nias=0,top 1 ans, 0.77388
#3097 probs,620 tested

#history q=10.0,ir=1.2,bi=0.02,text=1/2000,tri=0.0001,else=0,top 1 ans, 0.86666
#2379 probs,476

#social: q=10,ir=0.02,text=1/1500,bi=0.03,tri=0.0001,ias=2,nias=-1,top 2 ans, 0.62068
#1629 probs,325 tested

qWeight=10.0

irWeight=1.2

biWeight=0.02

textWeight=1.0/2000.0

triWeight=0.001

inCorrectAnswerSet=0
notInCorrectAnswerSet=0

topAnswers=1

for ii in train3:
	# print ii['Question ID']
	if int(ii['Question ID'])%5==0:
		if ii['category']=='history':
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

			for kk in range(0,topAnswers):
				answerSet.add(Q[kk*2])
				answerSet.add(I[kk*2])
			# for kk in correctAnswerSet:
			# 	answerSet.add(kk)
				

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
				words=re.split('\W+',ii['Question Text'].lower())
				for kk in words:
					stem = wn.morphy(kk)
					# print stem
					if stem==None:
						1
					else:
						textScore+=text[stem][answer]
						# print 'HAHAHAHAAHAHHAHAHAAH'

				# for word in re.split('\W+',ii['Question Text'].lower()):
				# 	stem = wn.morphy(word)
				# 	print stem
    # 				if stem!='None':
    # 					print 'HAHAHAAHAHAHAAHAHAHAAHAHAHAAHAHAHAA'
    # 				else:
				# 		textScore+=text[stem][answer]
				# 		print "MADE IT MADE IT MADE IT MADE IT MADE IT"
					# textScore+=text[word][answer]

				#Get bigrams score
				for gram in ngrams(nltk.word_tokenize(ii['Question Text'].lower()),2):
					biScore+=bigrams[gram][answer]

				#Get trigrams score
				for gram in ngrams(ii['Question Text'].lower(),3):
					triScore+=trigrams[gram][answer]

				if (answer in correctAnswerSet):
					answerSetScore=inCorrectAnswerSet
				else:
					answerSetScore=notInCorrectAnswerSet

				# print 'qScore=',qScore*qWeight, 'irScore=',irScore*irWeight, 'textScore=',textScore*textWeight, "biScore=", biScore*biWeight
				# print 'qScore=',qScore, 'irScore=',irScore, 'textScore=',textScore, "biScore=", biScore

				##Scoring algorithm:
				##with text = IR*w1+QANTA*w2+textscores*w3+bigram*w4
				totalScore=answerSetScore+irScore*irWeight+qScore*qWeight+textScore*textWeight+biScore*biWeight+triScore*triWeight
				# totalScore=irScore*irWeight+qScore*qWeight+textScore*textWeight
				# totalScore=irScore*irWeight+qScore*qWeight
				totalScoreList[answer]=totalScore

		
			#Calc final answer
			pickedAnswer=maxScore(totalScoreList)
			# print totalScoreList[pickedAnswer]
			# if pickedAnswer==ii['Answer']:
			# 	cCorrect+=1
			if pickedAnswer==ii['Answer']:
				cCorrect+=1
			if (ii['Answer'] in correctAnswerSet):
				inAnswerSet+=1

			#####STATS BASED ON SCORE#####
			if pickedAnswer==ii['Answer']:
				if totalScoreList[pickedAnswer]<=4:
					zeroToFour+=1
				if totalScoreList[pickedAnswer]<=8 and totalScoreList[pickedAnswer]>4:
					fourToEight+=1
				if totalScoreList[pickedAnswer]<=12 and totalScoreList[pickedAnswer]>8:
					eightToTwelve+=1
				if totalScoreList[pickedAnswer]>12:
					twelvePlus+=1

			if totalScoreList[pickedAnswer]<=4:
				zeroToFourTotal+=1
			if totalScoreList[pickedAnswer]<=8 and totalScoreList[pickedAnswer]>4:
				fourToEightTotal+=1
			if totalScoreList[pickedAnswer]<=12 and totalScoreList[pickedAnswer]>8:
				eightToTwelveTotal+=1
			if totalScoreList[pickedAnswer]>12:
				twelvePlusTotal+=1

			# if totalScoreList[pickedAnswer]<=4:
			# 	pickedAnswer=Q[0]

			# else:
			# 	totalScoreList[pickedAnswer]=0
			# 	pickedAnswer=maxScore(totalScoreList)
			# 	if pickedAnswer==ii['Answer']:
			# 		cCorrect+=1
			# print ii['Question ID'],maxScore(totalScoreList), ii['Answer']
			# test[ii['Question ID']]=maxScore(totalScoreList)
			# else:
			# 	print maxScore(totalScoreList), ii['Answer']
	i+=1

print "totalQuestion = ",totalQuestions
print "Accuracy with text = ", float(cCorrect)/float(totalQuestions)
# print len(correctAnswerSet)
print "In Answer Set? ", inAnswerSet, inAnswerSet/float(totalQuestions)
# print "zero to four =" ,zeroToFour/zeroToFourTotal, zeroToFourTotal/totalQuestions
# print "four to eight = ", fourToEight/fourToEightTotal, fourToEightTotal/totalQuestions
print "eightToTwelve =", eightToTwelve/eightToTwelveTotal, eightToTwelveTotal/totalQuestions
print "twelvePlus =", twelvePlus/twelvePlusTotal, twelvePlusTotal/totalQuestions


# # Write predictions
# o = DictWriter(open('pred3.csv', 'wb'), ['Question ID', 'Answer'])
# o.writeheader()
# for ii in sorted(test):
#     o.writerow({'Question ID': ii, 'Answer': test[ii]})


