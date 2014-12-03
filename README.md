QuizBowlChamps
==============

A classifier for answering quiz bowl questions. 

Team
===========
Reed Anderson, Aaron Holt, Vahid Mazdeh, Ryan Milvenan

(Ranking at [InClass Kaggle](http://inclass.kaggle.com/c/when-to-buzz/leaderboard "InClass Kaggle") under 'Quiz Bowl Champs'. )

Proposal
===========

We intend to use a binary MaxEnt (Logistic Regression) classifier implemented on PySpark MLlib and with Amazon EC2. We realise this is ambitious and introduces a library that most of the group has not worked with yet, so our first goal is to correctly compile the NLTK PositiveNaiveBayes and MaxEnt classifiers with the question answer data and some features, and later move to a PySpark implementation.

The advantage to first using the NLTK machine learning functions is that we'll mostly review and emulate Homework 4, but also have a working classifier to submit by November 14th; specifically, we'll gain a better understanding for the binary data structures used in the NLTK train() method as arguments and begin to identify features for the training algorithms. A possible solution right now might be to train a feature vector (for each answer) with: “True”/1 booleans from question text unigrams, values from QANTA score keys, values from sentence position, values from wiki_scores keys, and integer values representing each category. This feature vector will be represented as a dict in NLTK, and for PySpark we would have to explore feature extraction.

Doing machine learning across a distributed system sounds amazingly cool, but there are also some pragmatic reasons why we'd like to use PySpark. Most important is that Logistic Regression is ideal for binary classification (e.g., this project), but training a Logistic Regression classifier on a single CPU is impractical. Similar to Homework 4, while we could use a Naive Bayes classifier running on NLTK and a single CPU for this project, this would at best result in a mediocre Kaggle score. All considered, after we have a firm understanding of how the data is structured and potential features, we'll move on to the really fun stuff.


