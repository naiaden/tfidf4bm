from ReadFile import FileReader
input_file = "bla.tsv"
content_column = 5

reader = FileReader(delimiter='\t', stop_words="stopwords.txt")
reader.learn_frequencies(input_file, column=content_column)
reader.compute_tfidf(column=content_column, sparse=True, limit=25)
