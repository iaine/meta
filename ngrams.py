'''
Les automated view of the data
'''

from collections import defaultdict, Counter
import string 

import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams

import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud,STOPWORDS


stoplist = stopwords.words('english')
stoplist += ['-', '--', '—', "'", '’'] #variety of dashes used in Medium's HTML

with open("metaverse.txt", "r") as fh:
    documents = fh.read()
fh.closed

documents = documents.translate(str.maketrans('', '', string.punctuation))

#tokenize
tokens = nltk.word_tokenize(documents)
filtered_tokens = [w for w in tokens if not w in stoplist]

gram = 2

#Create the ngrams
bgs = nltk.ngrams(filtered_tokens,gram)

#compute frequency distribution for all the bigrams in the text
fdist = nltk.FreqDist(bgs)

counted_ngrams= fdist.most_common(50)

def _tuple_to_string(tup):
    '''
    Method to convert tuple to string
    '''
    return " ".join([k1 for k1 in tup])

def word_cloud(counted_ngrams, file_path):
    '''
    Function to create word cloud from list
    '''
    d = {}
    for k,v in counted_ngrams:
        d[_tuple_to_string(k)] = int(v)

    WC = WordCloud(stopwords=stoplist, 
        max_words=50,
        background_color="white").generate_from_frequencies(d)

    plt.imshow(WC)
    plt.axis("off")
    plt.savefig(file_path)

word_cloud(counted_ngrams, "imgs/word_cloud.png")

def count_as_histogram(counted_ngrams, file_path):
    objects = []
    performance = []
    for w in counted_ngrams:
        objects.append(_tuple_to_string(w[0]))
        performance.append(w[1])

    y_pos = np.arange(len(objects))

    plt.figure(figsize=(50,20)) 
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Counts')
    plt.title('Words in Topics')
    plt.savefig(file_path)

count_as_histogram(counted_ngrams, "imgs/word_freqs.png")