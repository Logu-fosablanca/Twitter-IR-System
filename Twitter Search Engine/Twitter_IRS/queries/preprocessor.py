import codecs
from collections import Counter
from .utils import process_txt

import csv
import re
# from sets import Set

from . import utils


class Preprocessor:
    def __init__(self, path):
        self.corpus_path = path

    def parse_corpus(self, raw=False):
        '''
        Parse the corpus text document into a list of dictionaries with key being id and value being the msg)
        :param raw: if True, we will not tokenize and filter the words in the messages; useful if we want to return the original message;
        :return: a list of dictionaries with document ids as keys, and either the raw msg or a list of tokenized, processed
        words
        '''
        corpus = {}
        with open(self.corpus_path, "r", encoding='utf-8-sig') as f:
            while True:
                row = f.readline()
                if len(row) == 0:
                    break
                corpus[row.split('\t')[0]] = row.split('\t')[1]

        return corpus;

    def create_tokens(self, processed_corpus):
        '''
        Creates a unique set of tokens that were identified after processing, stemming, and filtering the corpus text.
        :param processed_corpus: a corpus created from parse_corpus(False), in which messages are tokenized, filtered,
        and stremmed
        :return: a unique set of words in the corpus containing no duplicates
        '''
        corpus_tokens = set()
        for doc in processed_corpus:
            # for w in utils.process_txt(doc["msg"], True):
            for w in process_txt(processed_corpus[doc]):
                corpus_tokens.add(w)
        return corpus_tokens

    def create_corpus_counter(self, processed_corpus):
        '''
        Transforms a processed corpus dictionary (i.e. hashmap) of document ids as keys and their tokenized messages in
        a list as the values into a similar hashmap with document ids as keys, but values being a hashmap of the unique
        words in the message corresponding to their frequency. E.g. corupus_counter[doc_id] = {"fifa": 2, "world": 1, "cup": 1}.

        :param corpus: A parsed corpus in hashmap form with document ids as keys, and a list of the tokens in the message as values.
        :return: a list of dictionaries for each document, containing their id, and a dictionary of the words and
        corresponding frequencies
        '''
        corpus_counter = {}
        for doc in processed_corpus:
            corpus_counter[doc]= Counter(process_txt(processed_corpus[doc]));
        return corpus_counter
