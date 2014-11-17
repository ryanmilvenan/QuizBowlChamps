import re
from collections import defaultdict
from collections import Counter
from csv import DictReader, DictWriter
from sets import Set

# QANTA="carthage:4.46484593046, nelson,_mandela:3.46234617073, verdun:3.15971690441, mali_empire:3.07175457186, ancient,_corinth:3.01212692235, safavid_dynasty:2.11277334269, gang,_of_four:2.11277334269, cherokee:2.08967018412, charles_lindbergh:2.07650192779, maximilien_de_robespierre:1.91357333451, gadsden_purchase:1.89950155507"
QANTA="charles,_evans_hughes:5.03163689658, schenck_v._united_states:5.00447155416, louis_brandeis:4.251191427, john_marshall:3.57516842587, woodrow_wilson:2.69267126618, earl_warren:2.52644672017, daniel_webster:2.52504337845, william_howard_taft:2.46076409081, roger_b._taney:2.38564044248, benjamin_harrison:2.36968404277, clarence_darrow:2.04152432131, henry_the_navigator:2.00899062863, benjamin_disraeli:2.00899062863, manifest_destiny:1.9511654148, warren_g._harding:1.94673112462, plessy_v._ferguson:1.94478820265, muhammad_ali_jinnah:1.90438445581, stephen_a._douglas:1.82649976526, magna_carta:1.81674013471, alexander_hamilton:1.8037037425"

Q=re.split(':',QANTA)
# print Q
F=[]
counter=0
for item in Q:
	print "item=",item

	# W=re.split('/([^,]+)/',item)
	if counter > 0:
		W=re.split(',',item,1)
		print "W=",W
		for ele in W:
			F.append(re.sub(' ','',ele))
			counter+=1
			# print counter
			# print ele
	counter+=1
print F

# QANTA={}
# for kk in range(0,20):
# 	# print kk,kk*2,kk*2+1
# 	QANTA[F[kk*2]]=F[kk*2+1]

# print QANTA
# qScore=0.0
# irScore=0.0
# answerSet=Set()

# for kk in range(0,20):
# 	QANTA[F[kk*2]]=F[kk*2+1]
# 	# IR[I[kk*2]]=I[kk*2+1]

# for kk in range(0,3):
# 	answerSet.add(F[kk*2])
# 	# answerSet.add(I[kk*2])
		

# for answer in answerSet:
# 	# print answer
# 	textScore=0.0
# 	biScore=0.0

# 	#Get QANTA and IR scores
# 	try:
# 		qScore=float(QANTA[answer])
# 	except KeyError:
# 		qScore=0.0