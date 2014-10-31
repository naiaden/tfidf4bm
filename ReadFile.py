from __future__ import print_function
import sys
import math
import csv
import operator

class FileReader:
    stop_words = []
    compound_words = []
    delimiter = ','

    document_frequencies = []
    document_frequency = {}

    def __init__(self, stop_words=None, compound_words=None, delimiter=','):
        self.delimiter = delimiter
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

    def learn_frequencies(self, file, column=None):
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            for doc_nr, row in enumerate(reader):
                word_count = {}

                text = row[column].split()
                for word in text:
                    if word not in self.stop_words:
                        if word not in word_count:
                            word_count[word] = 1
                        else:
                            word_count[word] += 1
                        
                        if word not in self.document_frequency:
                            self.document_frequency[word] = set()
                            self.document_frequency[word].add(doc_nr)
                        else:
                            self.document_frequency[word].add(doc_nr);
                    
                self.document_frequencies.append(word_count)
        print(len(self.document_frequency))
                
    def compute_tfidf(self, file, column=None, sparse=False, limit=None):
        words_idx = []
        for k in self.document_frequency.keys():
            words_idx.append(k) 

        for doc_nr, document in enumerate(self.document_frequencies):
            #            if doc_nr > 5:
            #    break

            doc_tf_idfs = []
            for k, v in self.document_frequency.items():
                tf = 0
                f = 0
                bla = ""
                if k in document:
                    f = document[k] 
                if f > 0:
                    tf = 1 + math.log(f)
                    bla = k

                N = len(self.document_frequencies)
                idf = math.log(N / len(v))
                doc_tf_idfs.append(tf*idf)
#                doc_tf_idfs.append([tf, f, bla])
            if sparse:
                sorted_tf_idfs_pos = [i[0] for i in sorted(enumerate(doc_tf_idfs), key=lambda x:x[1], reverse=True)]
                sorted_tf_idf_words = []
                for idx in sorted_tf_idfs_pos:
                    sorted_tf_idf_words.append(words_idx[idx])
                if limit is None:
                    print(zip(sorted(doc_tf_idfs,reverse=True),sorted_tf_idf_words))
                else:
                    print(str(doc_nr) + str(zip(sorted(doc_tf_idfs,reverse=True),sorted_tf_idf_words)[0:limit]))
            else:
                print(doc_tf_idfs)
        print("PROCESSED: " + str(doc_nr+1) + " documents", file=sys.stderr)
        print("PROCESSED: " + str(len(self.document_frequency)) + " words", file=sys.stderr)
 
