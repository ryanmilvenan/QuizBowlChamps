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
# stop.append('its')
stop.append('.')
stop.append(',')


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
	# if int(ii['Question ID'])%5==0:
	if ii['category']=='lit':
		#Split on everything that isn't alpha-numeric
		words = nltk.word_tokenize(ii['Question Text'])
		bi=nltk.bigrams(words)
		for kk in bi:
			if len(kk[0])>2 or len(kk[1])>2:
				if kk[0] not in stop or kk[1] not in stop:
					featuresInTestSet.append(kk)
				# print kk

# print "LENGTH FEATURESET = ",len(featuresInTestSet)


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
	if ii['category']=='lit':
	#Split on everything that isn't alpha-numeric
		words = nltk.word_tokenize(ii['Question Text'])
		bi=nltk.bigrams(words)
		for kk in bi:
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
	if (int(ii['Question ID'])%5)==0:
		if ii['category']=='lit':
			totalQuestions2+=1

	# if int(ii['Question ID'])%2==0:
	if ii['category']=='lit':
		# if (int(ii['Question ID'])%5)!=0:
		totalQuestions+=1


#Question ID, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category

print "LOADING INTO RAM"

####LOAD INTO RAM#####
train = DictReader(open("train.csv", 'r'))
allData=defaultdict()
for ii in train:
	if ii['category']=='lit':
		allData[ii['Question ID'],ii['Sentence Position']]=[ii['Question Text'],ii['QANTA Scores'],ii['IR_Wiki Scores'],ii['Answer'],ii['category']]
		# if int(ii['Question ID'])%5!=0:
		correctAnswerSet.add(ii['Answer'])
	# print allData[ii['Question ID'],ii['Sentence Position']][4]

##0=QText,1=Qscore,2=IRscore,3=Answer,4=cat

###PICK INITIAL FEATURES####
totalScoreList = defaultdict() 
totalScore={}
featureWeights=defaultdict()
featureWeightsText=defaultdict()


###individual words features, assign initial weights:
for feature in featureText:
	# print feature
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
		# if (int(ii[0])%2)==0:
		# if allData[ii][4]=='science':
		print count

		words = nltk.word_tokenize(allData[ii][0])
		bi=nltk.bigrams(words)
		bigrams=[]
		for b in bi:
			bigrams.append(b)
		# bi=ngrams(nltk.word_tokenize(allData[ii][0].lower()),2)
		# print bi

		for answer in correctAnswerSet:
			# print "answer = ",answer

			##Adding single word features
			for feature in featureWeightsText:  ##dict containing all features and their current weights
				# print feature,featureWeightsText[feature]
				# equationDict[ii][answer][feature]=0.0
				for b in bigrams:
					# print b, feature
					if b==feature:
						# print b, feature
						if featureText[b][answer]>0:
							equationDict[ii][answer][feature]=0
							# print b, feature, equationDict[ii][answer][feature]



			for feature in featureWeightsText:  ##dict containing all features and their current weights
				# equationDict[ii][answer][feature]=0.0
				for b in bigrams:
					if b==feature:
						if featureText[b][answer]>0:
							equationDict[ii][answer][feature]+=1.0/featureText[b][answer]



for (k,v) in featureWeightsText.iteritems():
	featureWeights[k]=v


print "MADE IT TO WEIGHT SELECTION"

mostCorrect=0
listRange=[]
for i in range(0,4):
	listRange.append(float(i)/10.0)
############### "TRAIN" again trying different weights################
for jj in range(0,1):
	for feat in featureWeights:
		if mostCorrect==totalQuestions:
			break
		for weight in listRange:
			cCorrect=0
			featureWeights[feat][0]=weight
			for ii in allData:
				# if (int(ii[0])%5)!=0:
					# if allData[ii][4]=='science':
				totalScore={}
				for answer in equationDict[ii]:
					totalScore[answer]=0

					for feature in equationDict[ii][answer]:
						totalScore[answer]+=equationDict[ii][answer][feature]*featureWeights[feature][0]
						# print 
				try:
					pickedAnswer=maxScore(totalScore)
				except ValueError:
					pickedAnswer=''
					# totalScoreList[ii]=pickedAnswer
				if pickedAnswer==allData[ii][3]:
					cCorrect+=1


		
			if mostCorrect<cCorrect:
				featureWeights[feat][1]=weight
				mostCorrect=cCorrect
				print "Accuracy = ", float(cCorrect)/float(totalQuestions),feat,featureWeights[feat][1],"Iteration = ",jj

		featureWeights[feat][0]=featureWeights[feat][1] #update feature weight to best so far
	print "Accuracy = ", float(mostCorrect)/float(totalQuestions),"Iteration = ",jj

print "Final Accuracy On Dev = ", float(cCorrect)/float(totalQuestions)
#####################TESTING ON DEV####################################
cCorrect=0
# equationDict=defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

######USE ON TEST DATA#########################
testFile = DictReader(open("test.csv", 'r'))
test=defaultdict(list)

for ii in testFile:
	if ii['category']=='lit':
		# if int(ii['Question ID'])%5==0:
		totalScore={}


		words = nltk.word_tokenize(ii['Question Text'])
		bi=nltk.bigrams(words)
		bigrams=[]
		for b in bi:
			bigrams.append(b)

		for answer in correctAnswerSet:
			totalScore[answer]=0

			for feature in featureWeightsText:
				for b in bigrams:
					if b==feature:
						if featureText[b][answer]>0:
							totalScore[answer]+=1.0/featureText[b][answer]*featureWeightsText[feature][0]


		for qq in range(0,11):
			pickedAnswer=maxScore(totalScore)
			test[ii['Question ID']].append((pickedAnswer,totalScore[pickedAnswer]))
			totalScore[pickedAnswer]=-1
print "Accuracy On test after weight selection = ", float(cCorrect)/float(totalQuestions2)


# Write predictions
o = DictWriter(open('predLitBigrams3.csv', 'wb'), ['Question ID', 'Answer'])
o.writeheader()
for ii in sorted(test):
    o.writerow({'Question ID': ii, 'Answer': test[ii]})


