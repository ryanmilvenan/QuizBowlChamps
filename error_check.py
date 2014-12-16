from csv import DictReader, DictWriter

test = DictReader(open("test.csv", 'r'))
testDict = {}

for item in test:
	testDict[item['Question ID']] = item['category']



key = DictReader(open("key.csv", 'r'))
keyDict = {};

for item in key:
	answer_info = {}
	answer = item['Answer']
	question_id = item['Question ID']
	cat = testDict[question_id]
	answer_info['category'] = cat
	answer_info['answer'] = answer
	keyDict[question_id] = answer_info

history = 0.0
totalHistory = 0.0
literature = 0.0
totalLiterature = 0.0
social = 0.0
totalSocial = 0.0
science = 0.0
totalScience = 0.0

pred = DictReader(open("pred6.csv", 'r'))
predDict = {}

for item in pred:
	predDict[item['Question ID']] = item['Answer']

hist_error = {}
lit_error = {}
social_error = {}
science_error = {}

for item in sorted(predDict):
	question_id = item
	pred_answer = predDict[item]
	actual_answer_info = keyDict[item]
	actual_answer = actual_answer_info['answer']
	actual_answer_category = actual_answer_info['category']
	
	if actual_answer_category == 'history':
		totalHistory += 1
		if pred_answer == actual_answer:
			history += 1
		else:
			error = {}
			error['correct'] = actual_answer
			error['incorrect'] = pred_answer
			hist_error[question_id] = error

	if actual_answer_category == 'lit':
		totalLiterature += 1
		if pred_answer == actual_answer:
			literature += 1
		else:
			error = {}
			error['correct'] = actual_answer
			error['incorrect'] = pred_answer
			lit_error[question_id] = error

	if actual_answer_category == 'social':
		totalSocial += 1
		if pred_answer == actual_answer:
			social += 1
		else:
			error = {}
			error['correct'] = actual_answer
			error['incorrect'] = pred_answer
			social_error[question_id] = error

	if actual_answer_category == 'science':
		totalScience+= 1
		if pred_answer == actual_answer:
			science += 1
		else:
			error = {}
			error['correct'] = actual_answer
			error['incorrect'] = pred_answer
			science_error[question_id] = error


print("History: ", history, "Total History: ", totalHistory, "Percentage Correct: %f" % (history/totalHistory))
print("\n")
for error in hist_error:
	print(error, "Correct Answer: ", hist_error[error]['correct'], "Incorrect Answer: ", hist_error[error]['incorrect'])
print("\n")
print("Literature: ", literature, "Total History: ", totalLiterature, "Percentage Correct: %f" % (literature/totalLiterature))
print("\n")
for error in lit_error:
	print(error, "Correct Answer: ", lit_error[error]['correct'], "Incorrect Answer: ", lit_error[error]['incorrect'])
print("\n")
print("Social: ", social, "Total Social: ", totalSocial, "Percentage Correct: %f" % (social/totalSocial))
print("\n")
for error in social_error:
	print(error, "Correct Answer: ", social_error[error]['correct'], "Incorrect Answer: ", social_error[error]['incorrect'])
print("\n")
print("Science: ", science, "Total Science: ", totalScience, "Percentage Correct: %f" % (science/totalScience))
print("\n")
for error in science_error:
	print(error, "Correct Answer: ", science_error[error]['correct'], "Incorrect Answer: ", science_error[error]['incorrect'])
print("\n")













