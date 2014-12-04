from csv import DictReader, DictWriter
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import wiki_module as wiki

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this amount')
	args = parser.parse_args()

	train = DictReader(open("train.csv", 'r'))

	question_ids = []
	answers_for_question = {}

	wiki.get_all_answers_for_questions(train, question_ids, answers_for_question)
	print "Number of answers %f" % len(answers_for_question)
