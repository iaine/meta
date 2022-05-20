'''
Let's topic model the manifesto
Visualise as heatmap and produces a gexf graph for Gephi
'''

from collections import defaultdict, Counter
import numpy as np

from bs4 import BeautifulSoup
import gensim
from gensim import corpora
from gensim import models
import networkx as nx
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

with open("making-the-metaverse-what-it-is-how-it-will-be-built-and-why-it-matters-3710f7570b04") as fh:
    data = fh.read()
fh.closed

html_data = soup = BeautifulSoup(data, 'html.parser')
paras = html_data.find_all('p')

#build the documents
documents = [docs.text for docs in paras]

stoplist = stopwords.words('english')
stoplist += ['-', '--', '—', "'", '’'] #variety of dashes used in Medium's HTML


texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in documents
]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]


tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

topics = 5

lda_model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=topics)  # initialize an LSI transformation
corpus_lda = lda_model[corpus_tfidf]

#print the topics out
for idx, topic_words in lda_model.show_topics():
    topic_word = ','.join([k.split('*')[1] for k in topic_words.split('+')])
    print("{} -> {}".format(idx, topic_word))

#@todo: read in the original document and topic per paragraph?
#print out the percentages per topic per document
#at this stage, probably better as a chunk. 
data_arr = np.zeros((len(texts)+1, topics))
i=0
for tops in lda_model.get_document_topics(corpus):
    i+=1
    for t in tops:
        data_arr[i][t[0]] = t[1]  

# useful: https://github.com/stefanpernes/dariah-nlp-tutorial/blob/master/lda_heatmap.py
topic_labels = [*range(1, topics +1)]
#plt.title( "Topic Model Heat Map" )
plt.figure(figsize=(100,20))    # if many items, enlarge figure
plt.pcolor(data_arr, norm=None, cmap='Reds')
plt.yticks(np.arange(data_arr.shape[0])+1.0)
plt.xticks(np.arange(data_arr.shape[1])+0.5, topic_labels, rotation='90')
plt.gca().invert_yaxis()
plt.colorbar(cmap='autumn')
plt.tight_layout()
plt.savefig('imgs/topics_heatmap.png')

#set up count array        
words = []
#let's visualise as a network
# https://paperperweek.wordpress.com/2017/12/20/data-visualization-for-gensim-lda-and-word2vec/
g = nx.Graph()

for idx, topic_words in lda_model.show_topics():
    g.add_node(idx)
    for k in topic_words.split('+'):
        #get the name and remove quote marks
        m = k.split('*')[1].replace('"', '').strip()
        if m != "-" or m != "--":
            words.append(m)
            if m not in g.nodes:
                g.add_node(m)
            g.add_edge(idx,m)
       
#export the graph as gexf so that it can be used in Gephi
nx.write_gexf(g, "imgs/manifest.gexf")

#Counter of topic words
counted_words = Counter(words)
#print(counted_words)

objects = []
performance = []
for w in counted_words.items():
    objects.append(w[0])
    performance.append(w[1])

y_pos = np.arange(len(objects))

plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Counts')
plt.title('Words in Topics')

#plt.show()
plt.savefig('imgs/topics.png')