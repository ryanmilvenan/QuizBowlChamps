from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import RegexpTokenizer

class FeatureExtractor:
	def __init__(self):
		"""
		You may want to add code here
		"""
		self._d = defaultdict(float)

	def score_dict(self, vals):
		d = self._d
		for jj in vals.split(", "):
			key, val = jj.split(":")
			d[key.strip()] = float(val)
		return d

	def text_features(self, sentence):
		d = self._d
		words = sentence.lower().split()
		for ww in words:
			d[ww] += 1
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
    dev_train = []
    dev_test = []
    full_train = []

    # Train 
    for ii in train:
        if args.subsample < 1.0 and int(ii['Question ID']) % 100 > 100 * args.subsample:
            continue
        feat = fe.text_features(ii['Question Text'])
        # print ii['Question Text']
        if int(ii['Question ID']) % 5 == 0:
            # Appends feature stem and category key
            dev_test.append((feat, ii['Answer']))
        else:
        	dev_train.append((feat, ii['Answer']))
            # Appends feature stem and category key

    	full_train.append((feat, ii['Answer']))

    # Train a classifier
    print("Training classifier ...")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    # classifier = nltk.classify.MaxentClassifier.train(dev_train, 'IIS', trace=3, max_iter=5)


    # Test the classfier 
    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    print("Accuracy on dev: %f" % (float(right) / float(total)))

    # Retrain on all data
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)
    
    # Read in test section
    test = {}
    for ii in DictReader(open("test.csv")):
        test[ii['Question ID']] = classifier.classify(fe.text_features(ii['Question Text']))

    # # Write predictions
    # o = DictWriter(open('pred.csv', 'w'), ['id', 'pred'])
    # o.writeheader()
    # for ii in sorted(test):
    #     o.writerow({'id': ii, 'pred': test[ii]})
