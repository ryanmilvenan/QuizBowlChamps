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

train = DictReader(open("train.csv", 'r'))

#make a defaultdict of default dicts to store all data with answers
# d['the']['carthage']+=1  increment dictionary carthage within
# dictionary the by 1
#feature will contain all the feature we're looking at with an associated score
featureText = defaultdict(lambda: defaultdict(int))
featureQ = defaultdict(lambda: defaultdict(int))
featureIR = defaultdict(lambda: defaultdict(int))

words=[]

#New features can be inserted and trained in this loop
for ii in train:
	# if int(ii['Question ID'])%5!=0:
	if ii['category']=='social':
		#Split on everything that isn't alpha-numeric
		words=re.split('\W+',ii['Question Text'].lower())

		for kk in words:
			featureText[kk][ii['Answer']]+=1

		Q=[]
		I=[]
		counter=0 #This is used in case the first item has a comma before a :
		#for example 'charles,_evans_hughes:5.03163689658' would mess up without it

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
			# featureText[Q[kk*2]][ii['Answer']]=[float(Q[kk*2+1]),0,0]
			featureQ[Q[kk*2]][ii['Answer']]=float(Q[kk*2+1])*10
			# print featureQ[Q[kk*2]][ii['Answer']]
			# featureText[I[kk*2]][ii['Answer']]=[float(I[kk*2+1]),0,0]
			featureIR[I[kk*2]][ii['Answer']]=float(I[kk*2+1])


train = DictReader(open("train.csv", 'r'))


####MAKE ANSWER SET HERE################################################
##########Make sure to increase top answers!
topAnswers=5
answerSet=defaultdict(set)
totalQuestions=0

for ii in train:
	if int(ii['Question ID'])%5==0:
		if ii['category']=='social':
			totalQuestions+=1
			qScore=0.0
			irScore=0.0
			
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

			#Use topAnswers number of answers
			for kk in range(0,20):
				QANTA[Q[kk*2]]=Q[kk*2+1]
				IR[I[kk*2]]=I[kk*2+1]

			for kk in range(0,topAnswers):
				answerSet[ii['Question ID']].add(Q[kk*2])
				answerSet[ii['Question ID']].add(I[kk*2])
				# answerSet.add(Q[kk*2])
				# answerSet.add(I[kk*2])

			##maybe add answers from correctAnswerSet later...


#Question ID, Question Text, QANTA Scores, Answer, Sentence Position, IR_Wiki Scores, category

print "LOADING INTO RAM"

####LOAD INTO RAM#####
train = DictReader(open("train.csv", 'r'))
allData=defaultdict()
for ii in train:
	if ii['category']=='social':
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
	cCorrect=0
	# train = DictReader(open("train.csv", 'r'))
	for ii in allData:
		if int(ii[0])%5==0:
			# if allData[ii][4]=='social':
			totalScore={}

			# words=re.split('\W+',allData[ii][0].lower())

			for answer in correctAnswerSet:
				answerSet[ii[0]].add(answer)
			# for answer in answerSet[ii[0]]:
			# 	# totalScore[ii][answer]=0
			# 	totalScore[answer]=0
			# 	# print "Answer = ", answer
			# 	for word in words:
			# 		if word==feature:
			# 			# print "feature Score = ",featureText[word][answer]
			# 			if featureText[word][answer]>0:
			# 				# totalScore[ii][answer]+=1.0/featureText[word][answer]
			# 				totalScore[answer]+=1.0/featureText[word][answer]


			# pickedAnswer=maxScore(totalScore)
			# # totalScoreList[ii]=pickedAnswer
			# if pickedAnswer==allData[ii][3]:
			# 	cCorrect+=1


# 				# 	print word, featureText[word][ii['Answer']]
	# if cCorrect>12:
	# print "Accuracy with",feature," = ", float(cCorrect)/float(totalQuestions),float(cCorrect)
	#select useful features
	# if cCorrect>11:
		#[best weight,most q's answered], initialize weight to 1
	featureWeightsText[feature]=[0.001,0.001,0]
		# print "Accuracy with",feature," = ", float(cCorrect)/float(totalQuestions),float(cCorrect)

# ###QANTA features:
# for feature in featureQ:
# 	cCorrect=0
# 	# train = DictReader(open("train.csv", 'r'))
# 	for ii in allData:
# 		if int(ii[0])%5==0:
# 			# if allData[ii][4]=='social':
# 			totalScore={}

# 						#BUNCH OF DATA PROCESSING!
# 			Q3=allData[ii][1]
# 			Q2=re.split(':',Q3)
# 			for item in Q2:
# 				if counter>0:
# 					Q1=re.split(',',item,1) #split on first comma only!
# 					for ele in Q1:
# 						Q.append(re.sub(' ','',ele))
# 				else:
# 					Q.append(item)
# 				counter=1
# 			counter=0
# 			# print Q

# 			for answer in answerSet[ii[0]]:
# 				# totalScore[ii][answer]=0
# 				totalScore[answer]=0
# 				# print "Answer = ", answer


# 				for kk in range(0,20):
# 					if Q[kk*2]==feature:
# 						totalScore[answer]+=float(Q[kk*2+1])


# 			pickedAnswer=maxScore(totalScore)
# 			# totalScoreList[ii]=pickedAnswer
# 			if pickedAnswer==allData[ii][3]:
# 				cCorrect+=1

# 		#[best weight,most q's answered], initialize weight to 0
# 	featureWeightsQ[feature]=[0.001,0,0]
	# print "Accuracy with",feature," = ", float(cCorrect)/float(totalQuestions),float(cCorrect)

# ###IR features:
# for feature in featureIR:
# 	cCorrect=0
# 	# train = DictReader(open("train.csv", 'r'))
# 	for ii in allData:
# 		if int(ii[0])%5==0:
# 			# if allData[ii][4]=='social':
# 			totalScore={}

# 						#BUNCH OF DATA PROCESSING!
# 			I3=allData[ii][2]
# 			I2=re.split(':',I3)
# 			for item in I2:
# 				if counter>0:
# 					I1=re.split(',',item,1) #split on first comma only!
# 					for ele in I1:
# 						I.append(re.sub(' ','',ele))
# 				else:
# 					I.append(item)
# 				counter=1

# 			for answer in answerSet[ii[0]]:
# 				# totalScore[ii][answer]=0
# 				totalScore[answer]=0
# 				# print "Answer = ", answer


# 				for kk in range(0,20):
# 					if I[kk*2]==feature:
# 						totalScore[answer]+=float(I[kk*2+1])


# 			pickedAnswer=maxScore(totalScore)
# 			# totalScoreList[ii]=pickedAnswer
# 			if pickedAnswer==allData[ii][3]:
# 				cCorrect+=1

# 		#[best weight,most q's answered], initialize weight to 0
# 	featureWeightsIR[feature]=[0.001,0,0]
# 	# print "Accuracy with",feature," = ", float(cCorrect)/float(totalQuestions),float(cCorrect)



####CALCULATE EQUATION USING INITIAL FEATURES

print "MADE IT PAST FEATURE SELECTION"
#equation dict will store scores for all questions for all answers for all features. Messy, I know...
# equationDict=defaultdict(lambda: defaultdict(float))
recursivedict = lambda: defaultdict(recursivedict)
equationDict = recursivedict()

cCorrect=0
count=0
for ii in allData:
	count+=1
	if int(ii[0])%5==0:
		# if allData[ii][4]=='social':
		print count

		# 	#BUNCH OF DATA PROCESSING!
		# Q3=allData[ii][1]
		# Q2=re.split(':',Q3)
		# for item in Q2:
		# 	if counter>0:
		# 		Q1=re.split(',',item,1) #split on first comma only!
		# 		for ele in Q1:
		# 			Q.append(re.sub(' ','',ele))
		# 	else:
		# 		Q.append(item)
		# 	counter=1
		# counter=0
		# print Q
		# I3=allData[ii][2]
		# I2=re.split(':',I3)
		# for item in I2:
		# 	if counter>0:
		# 		I1=re.split(',',item,1) #split on first comma only!
		# 		for ele in I1:
		# 			I.append(re.sub(' ','',ele))
		# 	else:
		# 		I.append(item)
		# 	counter=1

		words=re.split('\W+',allData[ii][0].lower())

		for answer in answerSet[ii[0]]:

			##Adding single word features
			for feature in featureWeightsText:  ##dict containing all features and their current weights
				# equationDict[ii][answer][feature]=0.0
				for word in words:
					if word==feature:
						if featureText[word][answer]>0:
							equationDict[ii][answer][feature]=0
			# for feature in featureWeightsQ:
			# 	for kk in range(0,20):
			# 		if Q[kk*2]==feature:
			# 			equationDict[ii][(answer,'Q')][(feature,'Q')]=0
			# for feature in featureWeightsIR:
			# 		if I[kk*2]==feature:
			# 			equationDict[ii][(answer,'IR')][(feature,'IR')]=0


			for feature in featureWeightsText:  ##dict containing all features and their current weights
				# equationDict[ii][answer][feature]=0.0
				for word in words:
					# if word not in stop:  ##remove stop words
					if word==feature:
						if featureText[word][answer]>0:
							equationDict[ii][answer][feature]+=1.0/featureText[word][answer]
			# for feature in featureWeightsQ:
			# 	for kk in range(0,20):
			# 		if Q[kk*2]==feature:
			# 			equationDict[ii][(answer,'Q')][(feature,'Q')]+=float(Q[kk*2+1])
			# for feature in featureWeightsIR:
			# 		if I[kk*2]==feature:
			# 			equationDict[ii][(answer,'IR')][(feature,'IR')]+=float(I[kk*2+1])

# for (k,v) in featureWeightsQ.iteritems():
# 	featureWeights[(k,'Q')]=v
	# print k,'Q',v
# for (k,v) in featureWeightsIR.iteritems():
# 	featureWeights[(k,'IR')]=v
for (k,v) in featureWeightsText.iteritems():
	featureWeights[k]=v


print "MADE IT TO WEIGHT SELECTION"

mostCorrect=0
listRange=[]
for i in range(0,3):
	listRange.append(float(i)/10.0)
############### "TRAIN" again trying different weights################
for jj in range(0,2):
	for feat in featureWeights:
		if mostCorrect==totalQuestions:
			break
		for weight in listRange:
			cCorrect=0
			featureWeights[feat][0]=weight
			for ii in allData:
				if int(ii[0])%5==0:
					# if allData[ii][4]=='social':
					totalScore={}
					answersUsedSoFar=Set()
					# words=re.split('\W+',allData[ii][0].lower())
					for answer in equationDict[ii]:
						# if answer[0] not in answersUsedSoFar:
						totalScore[answer]=0

						for feature in equationDict[ii][answer]:
							########maybe the eqDict answer needs to consider IR and Q?
							########feature weight is seemingly always zero, maybe a mismatch
							########between eDict and feature weights
							########consider 3 seperate loops, one for each feature type
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
	if ii['category']=='social':
		answerSet=Set() #I put possible answers in a set to avoid duplicates
		totalScore={}
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

		#Use topAnswers number of answers
		for kk in range(0,20):
			QANTA[Q[kk*2]]=Q[kk*2+1]
			IR[I[kk*2]]=I[kk*2+1]

		for kk in range(0,topAnswers):
			answerSet.add(Q[kk*2])
			answerSet.add(I[kk*2])

		for answer in correctAnswerSet:
			answerSet.add(kk)

		words=re.split('\W+',ii['Question Text'].lower())

		for answer in answerSet:
			totalScore[answer]=0

			for feature in featureWeightsText:
				for word in words:
					if word==feature:
						if featureText[word][answer]>0:
							totalScore[answer]+=1.0/featureText[word][answer]*featureWeightsText[feature][0]

			# for feature in featureWeightsQ:
			# 	for kk in range(0,20):
			# 		if Q[kk*2]==feature[0]:
			# 			totalScore[answer]+=float(Q[kk*2+1])*featureWeightsQ[feature][0]
		
			# for feature in featureWeightsIR:
			# 	for kk in range(0,20):
			# 		if IR[kk*2]==feature[0]:
			# 			totalScore[answer]+=float(IR[kk*2+1])*featureWeightsIR[feature][0]
		for qq in range(0,11):
			pickedAnswer=maxScore(totalScore)
			test[ii['Question ID']].append((pickedAnswer,totalScore[pickedAnswer]))
			totalScore[pickedAnswer]=-1


# Write predictions
o = DictWriter(open('predsocialText.csv', 'wb'), ['Question ID', 'Answer'])
o.writeheader()
for ii in sorted(test):
    o.writerow({'Question ID': ii, 'Answer': test[ii]})


#kk is teh individual feature
#featureText[kk] is a default dict containing all the posible answers associated with
#that feature and the number of times each feature was associated.
#ex: kk=hand
#featureText[kk]=defaultdict(<type 'int'>, {'dark_energy': [1, 0, 0], 'moment_of_inertia': [1, 0, 0]})

# for kk in featureText:
# 	# print featureText[kk]
# 	# print counter,kk,featureText[kk]
# 	counter+=1
# 	for jj in featureText[kk]:
# 		# for ii in range(0,3):
# 		#kk is the feature,jj is the associated answer, f[kk][jj] are the scores/values
# 		print kk,jj,featureText[kk][jj]

	# featureText[kk][ii['Answer']][0]+=1


	##########################IN CASE I FORGET HOW THIS WORKS##################################
	# for feat in featureWeights:
	# for weight in range(0,4):
	# 	cCorrect=0
	# 	featureWeights[feat][0]=weight
	# 	for ii in allData:
	# 		if int(ii[0])%5==0:
	# 			if allData[ii][4]=='social':
	# 				totalScore={}
	# 				words=re.split('\W+',allData[ii][0].lower())
	# 				for answer in answerSet[ii[0]]:
	# 					totalScore[answer]=0

	# 					for feature in featureWeights:
	# 						for word in words:
	# 							if word not in stop:  ##remove stop words
	# 								if word==feature:
	# 									if featureText[word][answer]>0:
	# 										totalScore[answer]+=1.0/featureText[word][answer]*featureWeights[feature][0]
	# 										equationDict[ii][answer][feature]+=1.0/featureText[word][answer]

	# 				pickedAnswer=maxScore(totalScore)
	# 				# totalScoreList[ii]=pickedAnswer
	# 				if pickedAnswer==allData[ii][3]:
	# 					cCorrect+=1

	# 	print "Accuracy = ", float(cCorrect)/float(totalQuestions),feat,weight
	# 	if featureWeights[feat][2]<cCorrect:
	# 		featureWeights[feat][1]=weight
	# 		featureWeights[feat][2]=cCorrect
	# featureWeights[feat][0]=featureWeights[feat][1] #update feature weight to best so far