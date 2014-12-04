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
    # A dictionary to hold the wikipedia article text for each answer of each question
	wiki_texts = {}

	wiki.get_all_answers_for_questions(train, question_ids, answers_for_question)
	wiki.retrieve_wikipedia_info_for_question_answers(question_ids, answers_for_question, wiki_texts)
	wiki.write_articles_to_file(wiki_texts)
	
    # Retrieve wiki info
    #wiki.get_all_answers_for_questions(train, question_ids, answers_for_question)
    #wiki.retrieve_wikipedia_info_for_question_answers_textify(question_ids, answers_for_question, wiki_texts)