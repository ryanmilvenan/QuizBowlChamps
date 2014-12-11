#NLP Test Algorithms
# Try 3 will atempt to take thousands of individual features
# and optimize them for a top score!

from collections import defaultdict
from collections import Counter
from csv import DictReader, DictWriter
from sets import Set
from functools import partial
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import TreebankWordTokenizer
# from nltk.classify import PositiveNaiveBayesClassifier
from nltk.util import ngrams

stop = stopwords.words('english')

#Finds the max value given a dictionary and returns the key
def maxScore(d):
	v=list(d.values())
	k=list(d.keys())
	return k[v.index(max(v))]

########### PART 1 : Training #########################
#Fields:
#Question ID, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category

correctAnswerSet=Set()
QANTA={}
IR={}
words=[]
featuresInTestSet=[]

test1 = DictReader(open("test.csv", 'r'))
for ii in test1:
	# if int(ii['Question ID'])%5!=0:
	if ii['category']=='science':
		#Split on everything that isn't alpha-numeric
		words=re.split('\W+',ii['Question Text'].lower())

		for kk in words:
			featuresInTestSet.append(kk)

# print featuresInTestSet
# print len(featuresInTestSet)


train = DictReader(open("train.csv", 'r'))

#make a defaultdict of default dicts to store all data with answers
# d['the']['carthage']+=1  increment dictionary carthage within
# dictionary the by 1
#feature will contain all the feature we're looking at with an associated score
featureText = defaultdict(lambda: defaultdict(int))
featureQ = defaultdict(lambda: defaultdict(int))
featureIR = defaultdict(lambda: defaultdict(int))

#New features can be inserted and trained in this loop
for ii in train:
	# if int(ii['Question ID'])%5!=0:
	if ii['category']=='science':
		#Split on everything that isn't alpha-numeric
		words=re.split('\W+',ii['Question Text'].lower())

		for kk in words:
			if kk in featuresInTestSet:
				featureText[kk][ii['Answer']]+=1
				# print kk



train = DictReader(open("train.csv", 'r'))


# ####MAKE ANSWER SET HERE################################################
# ##########Make sure to increase top answers!
# topAnswers=5
# answerSet=defaultdict(set)
totalQuestions=0
totalQuestions2=0
for ii in train:
	if (int(ii['Question ID'])%2-1)==0:
		if ii['category']=='science':
			totalQuestions2+=1

	if int(ii['Question ID'])%2==0:
		if ii['category']=='science':
			totalQuestions+=1


#Question ID, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category

print "LOADING INTO RAM"

####LOAD INTO RAM#####
train = DictReader(open("train.csv", 'r'))
allData=defaultdict()
for ii in train:
	if ii['category']=='science':
		correctAnswerSet.add(ii['Answer'])
		allData[ii['Question ID'],ii['Sentence Position']]=[ii['Question Text'],ii['QANTA Scores'],ii['IR_Wiki Scores'],ii['Answer'],ii['category']]
	# print allData[ii['Question ID'],ii['Sentence Position']][4]

##0=QText,1=Qscore,2=IRscore,3=Answer,4=cat

###PICK INITIAL FEATURES####
totalScoreList = defaultdict() 
totalScore={}
featureWeights=defaultdict()
featureWeightsText=defaultdict()
featureWeightsQ=defaultdict()
featureWeightsIR=defaultdict()

###individual words features:
for feature in featureText:
	# cCorrect=0
	# # train = DictReader(open("train.csv", 'r'))
	# for ii in allData:
	# 	if int(ii[0])%5==0:
	# 		# if allData[ii][4]=='science':
	# 		totalScore={}

	# 		# words=re.split('\W+',allData[ii][0].lower())

	# 		for answer in correctAnswerSet:
	# 			answerSet[ii[0]].add(answer)


# 				# 	print word, featureText[word][ii['Answer']]
	# if cCorrect>12:
	# print "Accuracy with",feature," = ", float(cCorrect)/float(totalQuestions),float(cCorrect)
	#select useful features
	# if cCorrect>11:
		#[best weight,most q's answered], initialize weight to 1
	featureWeightsText[feature]=[0.001,0.001,0]
		# print "Accuracy with",feature," = ", float(cCorrect)/float(totalQuestions),float(cCorrect)



####CALCULATE EQUATION USING INITIAL FEATURES

print "MADE IT PAST FEATURE SELECTION"
#equation dict will store scores for all questions for all answers for all features. Messy, I know...
# equationDict=defaultdict(lambda: defaultdict(float))
recursivedict = lambda: defaultdict(recursivedict)
equationDict = recursivedict()

cCorrect=0
count=0
for jj in range(0,1):
	for ii in allData:
		count+=1
		if (int(ii[0])%2)==0:
			# if allData[ii][4]=='science':
			print count


			words=re.split('\W+',allData[ii][0].lower())

			for answer in correctAnswerSet:

				##Adding single word features
				for feature in featureWeightsText:  ##dict containing all features and their current weights
					# equationDict[ii][answer][feature]=0.0
					for word in words:
						if word==feature:
							if featureText[word][answer]>0:
								equationDict[ii][answer][feature]=0



				for feature in featureWeightsText:  ##dict containing all features and their current weights
					# equationDict[ii][answer][feature]=0.0
					for word in words:
						# if word not in stop:  ##remove stop words
						if word==feature:
							if featureText[word][answer]>0:
								equationDict[ii][answer][feature]+=1.0/featureText[word][answer]



for (k,v) in featureWeightsText.iteritems():
	featureWeights[k]=v


print "MADE IT TO WEIGHT SELECTION"

mostCorrect=0
listRange=[]
for i in range(0,4):
	listRange.append(float(i)/10.0)
############### "TRAIN" again trying different weights################
for jj in range(0,1):
	mostCorrect=0
	if jj>0:
		print "Switching test sets"
	for feat in featureWeights:
		if jj==0:
			if mostCorrect==totalQuestions:
				break
		if jj==1:
			if mostCorrect==totalQuestions2:
				break
		for weight in listRange:
			cCorrect=0
			featureWeights[feat][0]=weight
			for ii in allData:
				if (int(ii[0])%2)==0:
					# if allData[ii][4]=='science':
					totalScore={}
					answersUsedSoFar=Set()
					# words=re.split('\W+',allData[ii][0].lower())
					for answer in equationDict[ii]:
						# if answer[0] not in answersUsedSoFar:
						totalScore[answer]=0

						for feature in equationDict[ii][answer]:
							totalScore[answer]+=equationDict[ii][answer][feature]*featureWeights[feature][0]
							# print 
							# print totalScore[answer[0]],equationDict[ii][answer][feature],featureWeights[feature][0]

						# answersUsedSoFar.add(answer[0])  #Avoid redoing answers found in IR and QANTA


					pickedAnswer=maxScore(totalScore)

					# print "Picked Answer = ",pickedAnswer,"Real Answer = ",allData[ii][3]

					# totalScoreList[ii]=pickedAnswer
					if pickedAnswer==allData[ii][3]:
						cCorrect+=1

			
			if mostCorrect<cCorrect:
				featureWeights[feat][1]=weight
				mostCorrect=cCorrect
				print "Accuracy = ", float(cCorrect)/float(totalQuestions),feat,featureWeights[feat][1],"Iteration = ",jj

		featureWeights[feat][0]=featureWeights[feat][1] #update feature weight to best so far
	print "Accuracy = ", float(cCorrect)/float(totalQuestions),"Iteration = ",jj

print "Final Accuracy On Dev = ", float(cCorrect)/float(totalQuestions)
#####################TESTING ON DEV####################################
cCorrect=0
# equationDict=defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

######USE ON TEST DATA#########################
testFile = DictReader(open("test.csv", 'r'))
test=defaultdict(list)

for ii in testFile:
	if ii['category']=='science':
		answerSet=Set() #I put possible answers in a set to avoid duplicates
		totalScore={}
		Q=[]
		I=[]
		counter=0 #This is used in case the first item has a comma before a :
		#for example 'charles,_evans_hughes:5.03163689658' would mess up without it


		words=re.split('\W+',ii['Question Text'].lower())

		for answer in correctAnswerSet:
			totalScore[answer]=0

			for feature in featureWeightsText:
				for word in words:
					if word==feature:
						if featureText[word][answer]>0:
							totalScore[answer]+=1.0/featureText[word][answer]*featureWeightsText[feature][0]


		for qq in range(0,11):
			pickedAnswer=maxScore(totalScore)
			test[ii['Question ID']].append((pickedAnswer,totalScore[pickedAnswer]))
			totalScore[pickedAnswer]=-1


# Write predictions
o = DictWriter(open('predScienceText1.csv', 'wb'), ['Question ID', 'Answer'])
o.writeheader()
for ii in sorted(test):
    o.writerow({'Question ID': ii, 'Answer': test[ii]})


