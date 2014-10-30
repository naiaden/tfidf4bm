from __future__ import print_function
import sys
import csv
import operator

class FileReader:
    stop_words = []
    compound_words = []

    document_frequencies = []

    def __init__(self, stop_words=None, compound_words=None):
        if stop_words is not None:
            with open(stop_words, 'r') as f:
                for stop_word in f:
                    stop_word = stop_word.rstrip()
                    self.stop_words.append(stop_word)
            print("PROCESSED: " + str(len(self.stop_words)) + " stop words", file=sys.stderr)
        if compound_words is not None:
            with open(compound_words, 'r') as f:
                for compound_word in f:
                    compound_word = compound_word.rstrip()
                    self.compound_words.append(compound_word)
            print("PROCESSED: " + str(len(self.compound_words)) + " compound words", file=sys.stderr)

    def learn_df(self, file, column=None):
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for doc_nr, row in enumerate(reader):
                word_count = {}

                text = row[column].split()
                for word in text:
                    if word not in self.stop_words:
                        if word not in word_count:
                            word_count[word] = 1
                        else:
                            word_count[word] += 1
                self.document_frequencies.append(word_count)
                
    def compute_tfidf(self, file, column=None):
        with open(file, 'r') as f:
            
            reader = csv.reader(f)
            for doc_nr, row in enumerate(reader):
                document_frequency = self.document_frequencies[doc_nr]
                term_frequencies = {}
                
                print(document_frequency)
#
#                text = row[column].split()
#                for word in text:
#                    if word not in term_frequencies:
#                        term_frequencies[word] = 1
#                    else:
#                        term_frequencies[word] += 1
#                max_f = max(term_frequencies.iteritems(), key=operator.itemgetter(1))[1]
#                print(max_f)
#                for word in self.word_count:
#                    f = 0
#                    if word in term_frequencies:
#                        f = term_frequencies[word]
#                    tf = 0.5 + 0.5*f/max_f
#
#                    
#                    print(word + ":" + str(tf))
                     
