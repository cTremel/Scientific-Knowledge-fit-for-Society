#import Config as CON
import os
import sys
import random
import json
import time
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import string
import penman
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from rapidfuzz.distance import Levenshtein
import amrlib
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize

#Declare some necessary global functions and objects
stog = amrlib.load_stog_model()
wordnet_lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
current_time_ms = lambda: int(round(time.time() * 1000))

'''
I have already read the corpus, and computed frequency (in how many paper it appears) of each author-provided-keyword.
'''
keyword_filename = os.path.join("/../KnowUREnvironment/","keyword_frequency.txt")
assert(os.path.exists(keyword_filename))

with open(keyword_filename, encoding='utf-8') as f:
    keyword_frequency = json.loads(f.read())

'''
Top keywords are the ones that cover 80% of total keyword appearances.
keyword_frequency[x] = how many times keyword x appeared in the corpus
'''
i = 0
sum_frequency = 0
freq_list = []

for key in keyword_frequency.keys():
    i +=1
    f = keyword_frequency[key]
    freq_list.append(f)
    sum_frequency += f

top_keywords = []
cumulated_frequency = 0
for key in keyword_frequency.keys():
    f = keyword_frequency[key]
    cumulated_frequency += f
    top_keywords.append(key)
    #Set it to 0.6 (60%) for a quick run
    if cumulated_frequency>(0.8*sum_frequency):
        break

'''
Try to discard repeated appearance of the same keyword in a different form
'''
top_keywords = list(set([wordnet_lemmatizer.lemmatize(k.lower()) for k in top_keywords]))

plt.plot(np.arange(0,len(top_keywords)),freq_list[0:len(top_keywords)]); #Show frequency distribution of top keywords
plt.xlabel('n (n-th frequent keyword)')
plt.ylabel('Keyword frequency')

#Write top keywords to a file
with open('top_keywords.txt', 'w') as f:
    for item in top_keywords:
        f.write("%s\n" % item)