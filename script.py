import csv 

QAclassifer = open('pred6.csv')
try2 = open('pred7.csv')

QA_list = []
try_list = []

for ii in QAclassifer:
	QA_list.append(ii)

for ii in try2:
	try_list.append(ii)

length = len(QA_list)
count = 0

if len(QA_list) == len(try_list):
	for ii in range(length):
		if QA_list[ii] != try_list[ii]:
			print "MISMATCH: \n", "QA_list ---", QA_list[ii], "try_list ---", try_list[ii]
			count += 1

print "MISMATCH COUNTS:", count
print "TOTAL QUESTIONS:", length-1