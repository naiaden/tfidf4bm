from ReadFile import FileReader

reader = FileReader(stop_words="stopwords.txt")
reader.learn_df("input.txt", column=3)
reader.compute_tfidf("input.txt", column=3)
