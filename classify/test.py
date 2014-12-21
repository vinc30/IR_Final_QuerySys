from text.classifiers import NaiveBayesClassifier
#from text.blob import TextBlob
#-m textblob.download_corpora
#from nltk import NaiveBayesClassifier
train = [
         ('I love this sandwich.', '1'),
         ('This is an amazing place!', '1'),
         ('I feel very good about these beers.', '1'),
         ('This is my best work.', '1'),
         ("What an awesome view", '1'),
         ('I do not like this restaurant', '2'),
         ('I am tired of this stuff.', '2'),
         ("I can't deal with this", '2'),
         ('He is my sworn enemy!', '2'),
         ('My boss is horrible.', '2'),
         ('I like the girl','0'),
         ('This place is huge','0'),
         ('Mac is better than windows','0')
         ]
test = [
        ('The beer was good.', 'pos'),
        ('I do not enjoy my job', 'neg'),
        ("I ain't feeling dandy today.", 'neg'),
        ("I feel amazing!", 'pos'),
        ('Gary is a friend of mine.', 'pos'),
        ("I can't believe I'm doing this.", 'neg')
        ]
cl = NaiveBayesClassifier(train)
print(cl.classify("Their burgers are amazing."))  # "pos"
print(cl.classify("I don't like their pizza."))   # "neg"
blob = TextBlob("The beer was amazing. But the hangover was horrible. "
                "My boss was not pleased.", classifier=cl)
print(blob)
print(blob.classify())

for sentence in blob.sentences:
    print(sentence)
    print(sentence.classify())

# Compute accuracy
print("Accuracy: {0}".format(cl.accuracy(test)))

# Show 5 most informative features
cl.show_informative_features(5)
