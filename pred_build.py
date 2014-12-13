from __future__ import print_function
from csv import DictWriter, DictReader

import ast
import re
import os

def build_pred(file_index):
	has_file_index = re.compile(r"[%i]" % file_index)
	pred_files = []
	for file in os.listdir("./"):
		if file.endswith(".csv") and has_file_index.search(file) and (len(file) > 9):
			pred_files.append(file)
	
	pred_dicts = []
	for file in pred_files:
		pred_dict = DictReader(open(file, 'r'))
		pred_dicts.append(pred_dict)
	
	combined_dict = {}
	for pred_file in pred_dicts:
		for row in pred_file:
			answer_list = row['Answer']
			answer_list = ast.literal_eval(answer_list)
			answer = answer_list[0]
			answer = answer[0]
			combined_dict[row['Question ID']] = answer 

	o = DictWriter(open('pred'+str(file_index)+'.csv', 'wb'), ['Question ID', 'Answer'])
	o.writeheader()
	for row in sorted(combined_dict):
		o.writerow({'Question ID': row, 'Answer': combined_dict[row]})
	
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Build a prediction file with a supplied index')
    parser.add_argument('--index', type=int, default=None,
                        help='the file index to build from')
    args = parser.parse_args()
    build_pred(args.index)



