import io
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk import corpus
import random
import pickle
import string
from collections import Counter
#from nltk.tokenize import word_tokenize
#import numpy as np
from cmath import log, exp
#from math import log, exp path=

class MyDict(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return 0

word_list = [[] for x in range(0, 5)]
stemmer = PorterStemmer()
feature_polarity = [MyDict()  for x in range(0, 5)]
total_words = [0, 0, 0, 0, 0]

def get_word_list(sentences, index):
    print "Preparing Word List ", index, "......."
    global word_list,stemmer
    for sentence in sentences:
        #wordlist[index].extend(tokenize.word_tokenize(sentences[i])) #CLEAN document!!
        word_list[index].extend([stemmer.stem(word.lower()) for word in set(word_tokenize(sentence))]) #CLEAN document!!
        print word_list[index]

def prune_features(features):
    for i in range(0, 5):
        for feature in features:
            if feature in feature_polarity[i] and feature_polarity[i][feature] == 0:
                del feature_polarity[i][feature]

def train(features):
    print "Start Training......"
    global stemmer
    stem_features = [stemmer.stem(feature.rstrip("\n").lower()) for feature in features]
    """
    probability = [0, 0, 0, 0, 0]
    classified_features = [[] for x in range(0, 5)]
    print "     Examining Feature Polarity......"
    """
    j = 0
    for feature in stem_features:
        for i in range(0, 5):
            if feature_polarity[i][feature] is None:
                feature_polarity[i][feature] = 0
            feature_polarity[i][feature] += word_list[i].count(feature)
        j += 1
        if j % 1000 == 0:
            print "     ", j, " features processed ......."
    prune_features(stem_features)
    file = open("trainedFeatures.txt","w")
    for i in range(0, 5):
        for feature in feature_polarity[i]:
            file.write(str(i)+" "+feature+" "+str(feature_polarity[i][feature])+"\n")
    for i in range(0, 5):
        total_words[i] = sum(feature_polarity[i].values())
    """
        probability[i] = (word_list[i].count(feature) * 1.0)/len(word_list[i])
        classified_features[probability.index(max(probability))].append(feature)
    for i in range(0, 5):
        feature_file = open("feature_" + str(i) + ".txt", "wb")
        pickle.dump(classified_features[i], feature_file)
        feature_file.close()
    """

def classify(sentences):
    print "Classifying sentences .........."
    polarity = [0, 0, 0, 0, 0]
    curr_sent = 0
    prev_sent = -1
    matches = 0
    counter = 1
    for sentence in sentences:
        curr_sent = get_sentence_num(sentence)
        if prev_sent != curr_sent:
            sent_word_list = [stemmer.stem(word.lower()) for word in set(word_tokenize(sentence))]
            for i in range(0, 5):
                polarity[i] = 1/abs(sum(log((feature_polarity[i][word] + 1.0) / (2.0 * total_words[i])) for word in sent_word_list if feature_polarity[i][word] is not None))


            score = polarity.index(max(polarity))
            if score - get_sentence_score(sentence) == 0:
                matches += 1
            print "Polarity :", polarity.index(max(polarity)), "Sentence :", sentence
            print polarity,matches*1.0/counter,counter
            counter += 1
        prev_sent = curr_sent

"""
def get_trained_features():
    trained_features = [[] for i in range(0, 5)]
    for i in range(0, 5):
        feature_file = open("feature_" + str(i) + ".txt", "rb")
        with pickle.load(feature_file) as feature_list:
            for feature in feature_list:
                trained_features[i][feature] += 1
    return trained_features
"""

def get_sentence_num(lines):
    columns = lines.split("\t");
    return  int(columns[1].strip("'"))

def get_sentence_score(lines):
    columns = lines.split("\t");
    return  int(columns[3].strip("'"))

def get_file_lines(file, mode='r'):
    file_handler = open(file, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines
def find_bigrams(input_list):
    return [input_list[i] + " " + input_list[i+1] for i in range(0,(len(input_list)-1))]
def bi_grams(datafile,idex):
    try:
        # read the contents of the whole file into ''filecontents''
        filecontents=get_file_lines(datafile)
        file2=open("./feature/Ngrams/bigram_"+ str(idex) + ".tsv", 'w')
        for filecontent in filecontents: 
            # strip all punctuation at the beginning and end of words, and 
            # convert all words to lowercase
            words= [ word.strip(string.punctuation).lower() for word in set(word_tokenize(filecontent)) ]
            #print words                    
            bigram_dict=find_bigrams(words)
            for bigram_item in bigram_dict :
                file2.write(str(bigram_item) + "\n")
    except IOError:
                print "I could not find the file, Please try again."
                exit()      
    

def main():
    for i in range(0, 5):
        #get_word_list(get_file_lines("./data/train_" + str(i) + ".tsv"), i)
        bi_grams(("./data/train_" + str(i) + ".tsv"), i)  
    #train(get_file_lines('tempDictionary.txt'))
    #classify(get_file_lines('test.tsv'))
main()





