from csv import DictReader, DictWriter
from sets import Set
import ast

# test1 = DictReader(open("train.csv", 'r'))
# correctAnswerSet=Set()
# for ii in test1:
# 	# if int(ii['Question ID'])%5!=0:
# 	# print ii['Answer']
# 	# if ii['category']=='science':
# 	correctAnswerSet.add(ii['Answer'])

# for kk in sorted(correctAnswerSet):
# 	print kk


# predictedAnswerSet=Set()
# test1 = DictReader(open("pred1.csv", 'r'))
# for ii in test1:
# 	predictedAnswerSet.add(ii['Answer'])

# print "Intersect = ",predictedAnswerSet.intersection(correctAnswerSet)
# print ""
# print "Everything else in pred = ",predictedAnswerSet.difference(correctAnswerSet)
# print ""


predAnswers={}
pred = DictReader(open("predScienceText3.csv", 'r'))
for ii in pred:
	answers=ast.literal_eval(ii['Answer'])
	qid=ast.literal_eval(ii['Question ID'])
	# print qid,answers[0][0],answers[0][1]
	predAnswers[qid]=answers[0][0]
	# print answers[1]

pred = DictReader(open("predSocialText3.csv", 'r'))
for ii in pred:
	answers=ast.literal_eval(ii['Answer'])
	qid=ast.literal_eval(ii['Question ID'])
	# print qid,answers[0][0],answers[0][1]
	predAnswers[qid]=answers[0][0]

pred = DictReader(open("predHistoryText2.csv", 'r'))
for ii in pred:
	answers=ast.literal_eval(ii['Answer'])
	qid=ast.literal_eval(ii['Question ID'])
	# print qid,answers[0][0],answers[0][1]
	predAnswers[qid]=answers[0][0]

pred = DictReader(open("predLitText2.csv", 'r'))
for ii in pred:
	answers=ast.literal_eval(ii['Answer'])
	qid=ast.literal_eval(ii['Question ID'])
	# print qid,answers[0][0],answers[0][1]
	predAnswers[qid]=answers[0][0]

# Write predictions
o = DictWriter(open('pred3.csv', 'wb'), ['Question ID', 'Answer'])
o.writeheader()
for ii in sorted(predAnswers):
    o.writerow({'Question ID': ii, 'Answer': predAnswers[ii]})
