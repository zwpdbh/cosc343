#NLTK routines for computing ngrams from a text, 
#and some demonstrations of how to use them
#Alistair Knott, 23/5/2016

import nltk
from nltk.corpus import PlaintextCorpusReader
import random

#Read in 'Pride and Prejudice" as a list of sentences (each of which is a list of words).
corpus_root = '[Absolute_Path_Name]';
wordlists = PlaintextCorpusReader(corpus_root, '.*');
pride_and_prejudice = wordlists.words('pride_and_prejudice.txt');

#build a generator holding ngrams from the text.
#the second argument tells you the arity of the ngram model: 2 is bigrams, 3 is trigrams, and so on.
ngrams = list(nltk.ngrams(pride_and_prejudice, 2));

#compute the frequencies of all ngrams. (Still need to compute unconditional probability distribution from this.)
freqs = nltk.FreqDist(ngrams);

#build a conditional probability distribution of the second word in the bigram based on the first word
cpd = nltk.ConditionalProbDist(nltk.ConditionalFreqDist(ngrams), nltk.MLEProbDist)

#list a few of the first words..
for word in cpd.conditions()[:10]:
    
    #Compute the most likely next word, and its probability
    most_likely_word = cpd[word].max();
    prob = cpd[word].prob(most_likely_word);
    
    #Compute a random next word, based on the conditional distribution:
    random_next_word = cpd[word].generate();

    string = "Word: "+word+". Most likely next word: "+most_likely_word+" (probability "+str(prob)+"); random next word "+random_next_word;
    print(string)

#generate some text
def generate_text(cpd, numwords):
    word = random.choice(cpd.conditions());
    list = [];
    for i in range(100):
        list.append(word);
        word = cpd[word].generate()

    print(' '.join(list))
