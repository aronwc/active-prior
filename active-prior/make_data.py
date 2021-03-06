""" Parse and pickle various datasets. """

import argparse
import logging
import pickle
import random
import sys

import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import load_digits
from sklearn.feature_extraction.text import CountVectorizer

import data


logger = logging.getLogger(__name__)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', default='news', help='name of data to load')
    ap.add_argument('--output', default='/data/active-prior/news.pkl', help='pickled data file')
    return ap.parse_args()


def digits():
    """ Digit recognition. """
    d = load_digits(2)
    return data.Data(d.data[:200], d.target[:200], d.data[200:], d.target[200:])


def news():
    """ 20 newsgroup graphics vs windows """
    vec = CountVectorizer(min_df=5, stop_words='english')
    cats = ['comp.graphics', 'comp.windows.x']
    # cats = ['alt.atheism', 'talk.religion.misc']
    # cats = ['rec.sport.baseball', 'sci.crypt']

    newstrain = fetch_20newsgroups(subset='train',
                                   remove=('headers', 'footers', 'quotes'),
                                   categories=cats,
                                   shuffle=True, random_state=random.randint(1, 1e8))
    newstrain.data = vec.fit_transform(newstrain.data)
    newstest = fetch_20newsgroups(subset='test',
                                  remove=('headers', 'footers', 'quotes'),
                                  categories=cats,
                                  shuffle=True, random_state=random.randint(1, 1e8))
    newstest.data = vec.transform(newstest.data)
    return data.Data(newstrain.data, newstrain.target, newstest.data, newstest.target)


def main():
    args = parse_args()
    logging.info(args)
    data = getattr(sys.modules[__name__], args.name)()
    logging.info('saving %s data with %d training and %d testing instances and %d labels' %
                 (args.name, len(data.ytrain), len(data.ytest), len(set(data.ytrain))))
    pickle.dump(data, open(args.output, 'wb'))


if __name__ == '__main__':
    main()
