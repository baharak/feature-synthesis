"""
python features.py --jsons-file yelp_academic_dataset_review.json
"""
import argparse
import sys
import json
import csv
import random
import math
import re

from collections import namedtuple

def reader(input_file):
    line_num = 0
    for js in input_file:
        line_num += 1
        if len(js)==0:
            continue
        try:
            obj = json.loads(js)
            if obj["type"]=='review':
                yield obj
        except ValueError as e:
            ## the last line is "{" which makes it break
            print >> sys.stderr, '@%d: %s' % (line_num, e)


def flatten(input_file):
    all_reviews = []
    Review = namedtuple('Review', ['id', 'text'])
    # try:
    if True:
        for js in reader(input_file):
            # print "len of js is", len(js)
            rev =  Review(id=js.pop("useful", 0),
                          text=js.pop("text", 0))
            all_reviews.append(rev)
            # print len(all_reviews)
    # except:
    #         pass
    print len(all_reviews)
    return all_reviews


def tokenizer(text):
    return text.split()

def lowerizer(text):
    return map(lambda s: s.lower(), text)

def rm_punctuation(text):
    return map (lambda s: re.findall(r'\b[a-z]+\b', s, re.I), text)


def prepare_bag(reviews):
    l = []
    for review in reviews:
        data = (int(review[0]),
                rm_punctuation(lowerizer(tokenizer(review[1]))))
        l.append(data)
    return l

def create_word_bag(words_bag):
    wordbag_all = {}
    wordbag = (defaultdict(int), defaultdict(int))
    for words in words_bag:
        print words
        for word in words: # unigram
            wordbag[0][word] += 1
        for word1, word2 in zip(words[:-1],
                                words[1:]):
            wordbag[1][word1, word2] += 1

    wordbag_all.update(wordbag[0])
    wordbag_all.update(wordbag[1])

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsons-file',
                        type=argparse.FileType('r'))

    FLAGS = parser.parse_args(sys.argv[1:])
    prepared = prepare_bag(flatten(FLAGS.jsons_file)) ## very slow
    # create_word_bag(prepared)
