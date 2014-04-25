import sys
sys.path.append('C:\Users\Sushil-PC\Dropbox\SentimentalAnalysis-shared\python\pybrain-master\pybrain-master\pybrain')

from cmath import log
from nltk import PorterStemmer,pos_tag
from nltk.tokenize import word_tokenize
import nltk.help as nhelp
#from math import log, exp

class MyDict(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        #return 0

word_list = [[] for x in range(0, 5)]
stemmer = PorterStemmer()
feature_polarity = [MyDict()  for x in range(0, 5)]
total_words = [0, 0, 0, 0, 0]

def get_word_list(sentences, index):
    print "Preparing Word List ", index, "......."
    global word_list,stemmer
    punctuation = ['!', '.', ';', ':', '\'', '"','`']
    exceptions = ['\n', '\'s', '\'t', 'n\'t','not']
    for sentence in sentences:
        #wordlist[index].extend(tokenize.word_tokenize(sentences[i])) #CLEAN document!!
        #word_list[index].extend([stemmer.stem(word_tag.lower()) for word_tag in set(word_tokenize(sentence))])

        knot = 0
        for word_tag in set(word_tokenize(sentence)):
            if word_tag.lower() == "not":
                knot = 1
            elif word_tag in punctuation:
                knot = 0
            if word_tag.lower() not in punctuation and word_tag.lower() not in exceptions:
                if knot == 0:
                    word_list[index].append(stemmer.stem(word_tag.lower()))# if word_tag[1] in ['WRB', 'VBZ','VBP','VBN', 'VBG', 'VBD', 'VB', 'RBS', 'RBR', 'RB', 'JJS', 'JJR', 'JJ' ]]) #CLEAN document!!
                else:
                    word_list[index].append("not_"+stemmer.stem(word_tag.lower()))# if word_tag[1] in ['WRB', 'VBZ','VBP','VBN', 'VBG', 'VBD', 'VB', 'RBS', 'RBR', 'RB', 'JJS', 'JJR', 'JJ' ]]) #CLEAN document!!

    #word_list[index] = list(set(word_list[index])) # eliminating duplicates)
    #print word_list#[index]

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
                feature_polarity[4-i]["not_"+feature] = 0
            feature_polarity[i][feature] += word_list[i].count(feature)
            feature_polarity[4-i]["not_"+feature] += word_list[i].count("not_"+feature)
        j += 1
        if j % 1000 == 0:
            print "     ", j, " features processed ......."
    #prune_features(stem_features)
    file = open("feature/trainedFeatures.txt","w")
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
                polarity[i] = 1/abs(sum(log((feature_polarity[i][word] + 1.0) / (2.0 * total_words[i])) if feature_polarity[i][word] is not None else ( 1/(2.0*(total_words[i]))) for word in sent_word_list))
            for word in sent_word_list:
                if feature_polarity[i][word] is not None:
                    for j in range(0, 5):
                        score = polarity.index(max(polarity))
                        if score - get_sentence_score(sentence) != 0:
                            print j, word, feature_polarity[j][word], 1.0*feature_polarity[j][word]/total_words[i], 'LP: ',(feature_polarity[i][word] + 1.0) / (2.0 * total_words[i])

            score = polarity.index(max(polarity))
            if score - get_sentence_score(sentence) != 0:
                matches += 1
                print polarity, matches*1.0/counter
                print "Polarity :", polarity.index(max(polarity)), "Sentence :", sentence
            counter += 1
            print matches,counter

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
    return int(columns[1].strip("'"))

def get_sentence_score(lines):
    columns = lines.split("\t");
    return  int(columns[3].strip("'"))

def get_file_lines(file, mode='r'):
    file_handler = open(file, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines

def main():
    for i in range(0, 5):
        get_word_list(get_file_lines("data/train_" + str(i) + ".tsv"), i)
    train(get_file_lines('dictionary/tempUniGramDictionary'))
    classify(get_file_lines('data/test.tsv'))

main()