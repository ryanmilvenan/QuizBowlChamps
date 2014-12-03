from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
from nltk.classify import maxent
from nltk.util import ngrams

import re
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer

kTOKENIZER = TreebankWordTokenizer()

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

class FeatureExtractor:
    def __init__(self):
        """
        You may want to add code here
        """
        
        None
    
    def features(self, text):
        d = defaultdict(int)
        for ii in kTOKENIZER.tokenize(text):
            d[morphy_stem(ii)] += 1

        Q=[]
        Q3=ii['QANTA Scores']
        Q2=re.split(':',Q3)
        for item in Q2:
            if counter>0:
                Q1=re.split(',',item,1) #split on first comma only!
                for ele in Q1:
                    Q.append(re.sub(' ','',ele))
            else:
                Q.append(item)
            counter=1
        counter=0
        print Q
        for ii in range(0,20):
            d[Q[ii*2]] +=1

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
    counter=0
    for ii in train:
        if args.subsample < 1.0 and int(ii['Question ID']) % 100 > 100 * args.subsample:
            continue
        if ii['category']=='history':
            #features
            d = defaultdict(int) #stemmer
            # q = defaultdict(int) #QANTA scores
            # i = defaultdict(int) #IR scores
            # c = defaultdict(int) #category

            ##Simple stemmer
            # for jj in kTOKENIZER.tokenize(ii['Question Text']):
            #     stem = wn.morphy(jj)
            #     if stem:
            #         d[stem.lower()]+=1

            # bigrams of words counter
            bi=ngrams(nltk.word_tokenize(ii['Question Text'].lower()),3)
            for kk in bi:
                # print kk
                d[kk]+=1

            
            ###QANTA and IR scores
            Q=[]
            Q3=ii['QANTA Scores']
            Q2=re.split(':',Q3)
            for item in Q2:
                if counter>0:
                    Q1=re.split(',',item,1) #split on first comma only!
                    for ele in Q1:
                        Q.append(re.sub(' ','',ele))
                else:
                    Q.append(item)
                counter=1
            counter=0

            I=[]
            I3=ii['IR_Wiki Scores']
            I2=re.split(':',I3)
            for item in I2:
                if counter>0:
                    I1=re.split(',',item,1) #split on first comma only!
                    for ele in I1:
                        I.append(re.sub(' ','',ele))
                else:
                    I.append(item)
                counter=1
            counter=0

            # normalize the QANTA and IR scores
            maxQ=1.0
            maxI=1.0
            for jj in range(0,3):
                if float(Q[jj*2+1]) > maxQ:
                    maxQ=float(Q[jj*2+1])
                if float(I[jj*2+1]) > maxI:
                    maxI=float(I[jj*2+1])

            # for jj in range(0,5):
            #     d[Q[jj*2]] += 0
            #     d[I[jj*2]] += 0
            # for jj in range(0,3):
            #     d[Q[jj*2]] += int(float(Q[jj*2+1])*5/maxQ)
            #     d[I[jj*2]] += int(float(I[jj*2+1])*5/maxI)

            # ###category
            # d[ii['category']]+=5

            # feat=d
            # feat = fe.features(ii['Question Text'])

            if int(ii['Question ID']) % 5 == 0:
                dev_test.append((d, ii['Answer']))
                # dev_test.append((q, ii['Answer']))
                # dev_test.append((i, ii['Answer']))
                # dev_test.append((c, ii['Answer']))
            else:
                dev_train.append((d, ii['Answer']))
                # dev_train.append((q, ii['Answer']))
                # dev_train.append((i, ii['Answer']))
                # dev_train.append((c, ii['Answer']))
            # full_train.append((feat, ii['cat']))

    # Train a classifier
    print("Training classifier ...")
    # classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)
    #encoding = maxent.TypedMaxentFeatureEncoding.train(train, count_cutoff=3, alwayson_features=True),
    classifier = nltk.classify.MaxentClassifier.train(dev_train, 'GIS', trace=3,  max_iter=3)

    right = 0
    total = len(dev_test)
    for ii in dev_test:
        # print ii
        # if ii['category']=='history':
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
    print("Accuracy on dev: %f" % (float(right) / float(total)))

    classifier.show_most_informative_features(20)
    # # Retrain on all data
    # classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)
    
    # # Read in test section
    # test = {}
    # for ii in DictReader(open("test.csv")):
    #     test[ii['id']] = classifier.classify(fe.features(ii['text']))

    # # Write predictions
    # o = DictWriter(open('pred.csv', 'w'), ['id', 'pred'])
    # o.writeheader()
    # for ii in sorted(test):
    #     o.writerow({'id': ii, 'pred': test[ii]})
