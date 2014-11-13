from __future__ import print_function
import sys
import math
import csv
import operator

from nltk.tokenize import WordPunctTokenizer

class FileReader:
    stop_words = []
    compound_words = []
    delimiter = ','

    document_word_histogram = {}
    document_frequency = {}

    def __init__(self, year_documents=False, stop_words=None, compound_words=None, delimiter=','):
        self.delimiter = delimiter
        self.year_documents = year_documents
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
            for doc_id, row in enumerate(reader):

                year = row[1]
                text = WordPunctTokenizer().tokenize(row[column].lower())

                doc_nr = doc_id
                if self.year_documents:
                    doc_nr = year

                word_count_per_document = {}
                if doc_nr not in self.document_word_histogram:
                    self.document_word_histogram[doc_nr] = word_count_per_document
                else:
                    word_count_per_document = self.document_word_histogram[doc_nr]

                nr_words = 0;
                for word in text:
                    if word not in self.stop_words:
                        nr_words += 1
                        if word not in word_count_per_document:
                            word_count_per_document[word] = 1
                        else:
                            word_count_per_document[word] += 1
               
                        if word not in self.document_frequency:
                            self.document_frequency[word] = set()
                            self.document_frequency[word].add(doc_nr)
                        else:
                            self.document_frequency[word].add(doc_nr);
                    
                self.document_word_histogram[doc_nr] = word_count_per_document
                #print(self.document_word_histogram)
        print("PROCESSED: " + str(len(self.document_frequency)) + " types", file=sys.stderr)
                
    def compute_tfidf(self, column=None, sparse=False, limit=None):
        words_idx = []
        for k in self.document_frequency.keys():
            words_idx.append(k) 

        for doc_nr, document in self.document_word_histogram.items():
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

                N = len(self.document_word_histogram)
                idf = math.log(N / len(v))
                doc_tf_idfs.append(tf*idf)
            if sparse:
                sorted_tf_idfs_pos = [i[0] for i in sorted(enumerate(doc_tf_idfs), key=lambda x:x[1], reverse=True)]
                sorted_tf_idf_words = []
                for idx in sorted_tf_idfs_pos:
                    sorted_tf_idf_words.append(words_idx[idx])

                if limit is None:
                    limit = len(self.document_frequency)
                
                tfidf_word_tuples = (zip(sorted(doc_tf_idfs,reverse=True),sorted_tf_idf_words)[0:limit])
                output_string = ""
                for (t1,t2) in tfidf_word_tuples:
                    output_string += str(t1) + "\t" + str(t2) + "\t"
                print(str(doc_nr) + "\t" + output_string)
            else:
                print(doc_tf_idfs)
        print("PROCESSED: " + str(len(self.document_word_histogram)) + " documents", file=sys.stderr)
        print("PROCESSED: " + str(len(self.document_frequency)) + " words", file=sys.stderr)
 
