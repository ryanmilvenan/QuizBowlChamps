from csv import DictReader, DictWriter

key = DictReader(open("test.csv", 'r'))
keyDict = {};

for item in key:
	keyDict[item['Question ID']] = item['Answer']

o = DictWriter(open('test_sorted.csv', 'wb'), ['Question ID', 'Answer'])
o.writeheader()
for ii in sorted(keyDict):
    o.writerow({'Question ID': ii, 'Answer': keyDict[ii]})