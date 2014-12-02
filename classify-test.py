from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords

import nltk.classify.maxent

import operator

kTOKENIZER = TreebankWordTokenizer()

def word_filter(word):
    """
    Simple stemmer and stop filter
    """
    
    stem = wn.morphy(word)
    stop = stopwords.words('english')
    if stem:
        if stem.lower() not in stop:
            return stem.lower()

class FeatureExtractor:
    def __init__(self):
        """
        You may want to add code here
        """
        
        None
    
    def text_features(self, sentence):
        d = defaultdict(float)
        # words = sentence.lower().split()
        # for ww in words:
        #     d[word_filter(ww)] += 1

        # newA = dict(sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
        return d

    def guess_dict(self, vals):
        d = defaultdict(float)
        for jj in vals.split(", "):
            key, val = jj.split(":")
            d[key.strip()] = float(val)
        return d

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this amount')
    args = parser.parse_args()
    
    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(open("train.csv", 'r'))
    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []

    for ii in train:
        if args.subsample < 1.0 and int(ii['Question ID']) % 100 > 100 * args.subsample:
            continue
        
        feat = fe.text_features(ii['Question Text'])
        Q_guess = fe.guess_dict(ii['QANTA Scores'])
        W_guess = fe.guess_dict(ii['IR_Wiki Scores'])
        

        if int(ii['Question ID']) % 5 == 0:
            
            top_wiki_guess = max(W_guess, key=W_guess.get)
            # print ("ii: %s, top_wiki_guess: %s, and aswer is: %s" % (ii['Question ID'], top_wiki_guess, ii['Answer']))
            top_qanta_quess = max(Q_guess, key=Q_guess.get)

            feat['top_wiki_guess'] = top_wiki_guess
            feat['top_qanta_quess'] = top_qanta_quess
            dev_test.append((feat, ii['Answer']))

        else:
            top_wiki_guess = max(W_guess, key=W_guess.get)
            top_qanta_quess = max(Q_guess, key=Q_guess.get)

            feat['top_wiki_guess'] = top_wiki_guess
            feat['top_qanta_quess'] = top_qanta_quess

            dev_train.append((feat, ii['Answer']))
        
        full_train.append((feat, ii['Answer']))

    
    print("dev_train: %s" %dev_train)
    # trained_encode = nltk.classify.maxent.MaxentFeatureEncodingI.train(dev_train)
    # print("type of trained encode: ", type(trained_encode))
    # print("encoder labels: %s" %)

    # Train a classifier
    print("Training classifier ...")
    # classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    classifier = nltk.classify.MaxentClassifier.train(dev_train, 'IIS', trace=3, max_iter=3)

    classifier.show_most_informative_features(n=10, show='all')
    print("wights len: %d" %len(classifier.weights()))
    # print("encoder labels: %s" %classifier.MaxentFeatureEncodingI.labels())
    print("classifier weights: %s" %classifier.weights())

    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1

        # print("prediction=", prediction)
        # print("ii[1]=", ii[1])
    print("Accuracy on dev: %f" % (float(right) / float(total)))

    # Retrain on all data
    # classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)
    dev_full = dev_train + dev_test
    classifier = nltk.classify.MaxentClassifier.train(dev_full, 'IIS', trace=3, max_iter=3)
    
    # Read in test section
    test = {}
    for ii in DictReader(open("test.csv")):
        test[ii['Question ID']] = classifier.classify(fe.text_features(ii['Question ID']))

    # Write predictions
    o = DictWriter(open('pred.csv', 'w'), ['id', 'pred'])
    o.writeheader()
    for ii in sorted(test):
        o.writerow({'id': ii, 'pred': test[ii]})
