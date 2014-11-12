from collections import defaultdict
from csv import DictReader, DictWriter

import urllib
import urllib2
import json
import re

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

def word_filter(word):
    """
    Simple stemmer and stop filter
    """
    
    stem = wn.morphy(word)
    stop = stopwords.words('english')
    if stem:
        if stem.lower() not in stop:
            return stem.lower()

# A function that associates an answer with its wikipedia article
# text in the supplied dictionary.
def wiki_grab(answer, wiki_dict):
    url = 'http://en.wikipedia.org/w/api.php'
    values = {'action': 'query',
              'prop'  : 'extracts',
              'titles': answer,
              'rvprop': 'content',
              'format': 'json'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    jsonRes = response.read()
    textDict = json.loads(jsonRes)
    page = textDict['query']['pages'].keys()
    html = textDict['query']['pages'][page[0]]['extract']
    text = remove_tags(html)
    wiki_dict[answer] = text

def remove_tags(raw_html):
    cleanr =re.compile('<.*?>')
    clean_text = re.sub(cleanr,'', raw_html)
    return clean_text


class FeatureExtractor:
	def __init__(self):

		# Single dict for feature vector
		# self._d = defaultdict(float)
            None

	def guess_dict(self, vals):
		d = defaultdict(float)
		for jj in vals.split(", "):
			key, val = jj.split(":")
			d[key.strip()] = float(val)
		return d

	def text_features(self, sentence):
		d = defaultdict(float)
		words = sentence.lower().split()
		for ww in words:
			d[word_filter(ww)] += 1
		return d


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this amount')
    args = parser.parse_args()
    
    # Init and create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(open("train.csv", 'r'))
    
    # Split off dev section
    pos_train = []
    oth_train = []

    pos_test = []
    oth_test = []
    
    # pos_full = []
    # oth_full = []

    # Train 
    for ii in train:
        if args.subsample < 1.0 and int(ii['Question ID']) % 100 > 100 * args.subsample:
            continue

        # The following calls return one <type 'collections.defaultdict'>
        feat = fe.text_features(ii['Question Text'])
        Q_guess = fe.guess_dict(ii['QANTA Scores'])
        W_guess = fe.guess_dict(ii['IR_Wiki Scores'])
        
        # if ii['Answer'] == 'carthage' and ii['Sentence Position'] == '3':
        #     print "A \n", ii['Answer']
        #     print "Q \n", Q_guess, max(Q_guess, key=Q_guess.get)
        #     print "W \n", W_guess, max(W_guess, key=W_guess.get)
        #     print "T \n", feat
        # print type(Q_guess)

        if int(ii['Question ID']) % 5 == 0:
            
            # Append pos and oth for W_guess
            if max(W_guess, key=W_guess.get) == ii['Answer']:
                feat[ii['Answer']] = True
                pos_test.append(feat)
            else:
                feat[ii['Answer']] = False
                oth_test.append(feat)

            # Append pos and oth for Q_guess
            if max(Q_guess, key=Q_guess.get) == ii['Answer']:
                feat[ii['Answer']] = True
                pos_test.append(feat)
            else:
                feat[ii['Answer']] = False
                oth_test.append(feat)
        
        else:
        
            # Append pos and oth for W_guess
            if max(W_guess, key=W_guess.get) == ii['Answer']:
                feat[ii['Answer']] = True
                pos_train.append(feat)
            else:
                feat[ii['Answer']] = False
                oth_train.append(feat)

            # Append pos and oth for Q_guess
            if max(Q_guess, key=Q_guess.get) == ii['Answer']:
                feat[ii['Answer']] = True
                pos_train.append(feat)
            else:
                feat[ii['Answer']] = False
                oth_train.append(feat)

        # if max(W_guess, key=W_guess.get) == ii['Answer']:
        #     pos_full.append(W_guess)
        # else:
        #     oth_full.append(W_guess)

    # Train a classifier
    print("Training classifier ...")
    classifier = nltk.classify.PositiveNaiveBayesClassifier.train(pos_train, oth_train)
    # classifier = nltk.classify.MaxentClassifier.train(dev_train, 'IIS', trace=3, max_iter=5)

    # print pos_test[6]
    # test = pos_test[0]
    # print classifier.classify(test)

    # Test the classfier 
    pos_right = 0
    oth_right = 0
    pos_total = len(pos_test)
    oth_total = len(oth_test)

    # Test for 'True' with positives
    for ii in pos_test:
        prediction = classifier.classify(ii)
        # print "Answer: ", max(ii, key=ii.get)
        if prediction == True:
            pos_right += 1

    # Test for 'False' with others
    for ii in oth_test:
        prediction = classifier.classify(ii)
        # print "Answer: ", max(ii, key=ii.get)
        if prediction == False:
            oth_right += 1


    right = pos_right + oth_right
    total = pos_total + oth_total
    print("Accuracy on dev: %f" % (float(right) / float(total)))

    # # Retrain on all data
    # print("Training classifier on all training data...")
    # classifier = nltk.classify.PositiveNaiveBayesClassifier.train((pos_test + pos_train),(oth_test + oth_train))
    
    # # Read in test section
    # test = {}
    # for ii in DictReader(open("test.csv")):
    #     test[ii['Question ID']] = classifier.classify(fe.guess_dict(ii['IR_Wiki Scores']))

    # # Write predictions
    # o = DictWriter(open('pred.csv', 'w'), ['id', 'pred'])
    # o.writeheader()
    # for ii in sorted(test):
    #     o.writerow({'id': ii, 'pred': test[ii]})
