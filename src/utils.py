import numpy as np
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from json import dump
from time import time

nlp = spacy.load('en_core_web_sm')


def get_average_of_sent(sent):
    return np.average((sent[sent > 0]))


def get_threshold_value(res):

    avg_of_sents = np.nan_to_num(np.apply_along_axis(get_average_of_sent, 1, res))
    sum_of_averages = avg_of_sents.sum()

    return sum_of_averages / avg_of_sents.shape[0]



def find_sentences(res, factor = 1):

    threshold = get_threshold_value(res) * factor
    filter_arr = []
    for sentence in res:
        passes = False
        if get_average_of_sent(sentence) >= threshold:
            passes = True
        filter_arr.append(passes)

    return filter_arr


def cleanup(sent):
    filter_arr = []
    words = nlp(str(sent))
    tokens = []
    for word in words:

        if not (word.is_stop or word.is_punct or word.is_space or word.text == '=' or word.lemma_ == '-PRON-'):
            tokens.append(re.sub(r'[\t\n\r=]', '', word.lemma_.lower()))

    return ' '.join(tokens)


def sanitize_for_model(sents):
    clean_func = np.vectorize(cleanup)
    return clean_func(sents)



def sanitize_original(sent):
    return re.sub(r'[\t\n\r]', '', sent)



def get_TFIDF(sents):
    vc = TfidfVectorizer()
    res = np.nan_to_num(vc.fit_transform(sents).toarray())

    return res


def load_data(fname):
    f = open(f'../data/{fname}/inp.txt')
    data = f.read()
    f.close()
    return data


def write_data(fname, data):
    f = open(f'../data/{fname}/out.json', 'w')
    dump(data, f, indent=4)
    return f.close()
