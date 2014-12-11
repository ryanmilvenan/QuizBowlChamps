from collections import defaultdict

def maxScore(d):
	v=list(d.values())
	k=list(d.keys())
	return k[v.index(max(v))]

d={}
d['answer']=15
d['answer2']=20
d['answer18']=25

test=defaultdict(list)

for ii in range(0,3):
	pickedAnswer=maxScore(d)
	test[ii].append((pickedAnswer,d[pickedAnswer]))
	d[pickedAnswer]=-1

print d
print test

