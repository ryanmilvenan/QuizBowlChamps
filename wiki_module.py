import urllib
import urllib2
import json
import re
from csv import DictWriter

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

def retrieve_wikipedia_info_for_question_answers_textify(question_ids, answers_dictionary, wiki_texts):
    wiki_data = {}
    for q_id in question_ids:
        wiki_texts[q_id] = {}
        answers_for_this_question = answers_dictionary[q_id]
        for answer in answers_for_this_question:
            found = wiki_data.get(answer, False)
            if not found:
                wiki_grab_textify(answer, wiki_data)
                page_exists = wiki_data.get(answer, False)
                if page_exists:
                    wiki_texts[q_id][answer] = wiki_data[answer]
            else:
                page_exists = wiki_data.get(answer, False)
                if page_exists:
                    wiki_texts[q_id][answer] = wiki_data[answer]

def retrieve_wikipedia_info_for_question_answers(question_ids, answers_dictionary, wiki_texts):
    wiki_data = {}
    for q_id in question_ids:
        wiki_texts[q_id] = {}
        answers_for_this_question = answers_dictionary[q_id]
        for answer in answers_for_this_question:
            found = wiki_data.get(answer, False)
            if not found:
                wiki_grab(answer, wiki_data)
                page_exists = wiki_data.get(answer, False)
                if page_exists:
                    wiki_texts[q_id][answer] = wiki_data[answer]
            else:
                page_exists = wiki_data.get(answer, False)
                if page_exists:
                    wiki_texts[q_id][answer] = wiki_data[answer]

# A function that associates an answer with its wikipedia article
# text in the supplied dictionary.
def wiki_grab_textify(answer, wiki_dict):
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
    #print json.dumps(textDict, sort_keys=True, indent=4, separators=(',', ': '))
    page = textDict['query']['pages'].keys()

    #If the content is found, extract it
    if page[0] != u'-1':
        html = textDict['query']['pages'][page[0]]['extract']
        wiki_text = remove_tags(html)
        wiki_text = wiki_text.encode('ascii', 'ignore')
        text = create_nltk_text_from_wiki(wiki_text)
        wiki_dict[answer] = text

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
    #print json.dumps(textDict, sort_keys=True, indent=4, separators=(',', ': '))
    page = textDict['query']['pages'].keys()

    #If the content is found, extract it
    if page[0] != u'-1':
        html = textDict['query']['pages'][page[0]]['extract']
        wiki_text = remove_tags(html)
        wiki_text = wiki_text.encode('ascii', 'ignore')
        wiki_dict[answer] = wiki_text

def create_nltk_text_from_wiki(wiki_text):
    tokens = nltk.word_tokenize(wiki_text)
    text = nltk.Text(tokens)
    return text
    

def remove_tags(raw_html):
    cleanr =re.compile('<.*?>')
    clean_text = re.sub(cleanr,'', raw_html)
    return clean_text

def get_all_answers_for_questions(training_text, question_ids, answers_dictionary):
    for ii in training_text:
        exists = answers_dictionary.get(ii['Question ID'], False)
        if exists:
            answers = exists
            qanta_answers = split_answers(ii['QANTA Scores'])
            ir_answers = split_answers(ii['IR_Wiki Scores'])
            for answer in qanta_answers:
                answers.add(answer)
            for answer in ir_answers:
                answers.add(answer)

            answers_dictionary[ii['Question ID']] = answers
        else:
            answers = set()
            qanta_answers = split_answers(ii['QANTA Scores'])
            ir_answers = split_answers(ii['IR_Wiki Scores'])
            for answer in qanta_answers:
                answers.add(answer)
            for answer in ir_answers:
                answers.add(answer)
            question_ids.append(ii['Question ID'])
            answers_dictionary[ii['Question ID']] = answers


def split_answers(answer_type):
    answers = []
    for jj in answer_type.split(", "):
            key, val = jj.split(":")
            answer_raw = key.strip()
            answer = answer_raw.replace('_', " ")
            answer = answer.title()
            answers.append(answer)
    return answers

def words_in_common(wiki_text, question_text):
    wiki_words = set(wiki_text)
    question_words = set(question_text)
    count = 0
    stop = stopwords.words('english')
    for word in question_words:
        if word in wiki_words and word not in stop:
            count += 1
    
    return count

def bigrams_in_common(wiki_text, question_text):
    print wiki_text.collocations()

def write_articles_to_file(wiki_texts):
    o = DictWriter(open('articles.csv', 'w'), ['answer', 'text'])
    o.writeheader()
    for article in wiki_texts:
        o.writerow({'answer':article, 'text':wiki_texts[article]})

