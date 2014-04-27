import os.path
from symbol import break_stmt
from nltk import PorterStemmer,pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re, itertools
from math import log10

class MyDict(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return 0



lines = [0, 0, 0, 0, 0]
doc = [[] for i in range(0, 5)]
vocab = [0, 0, 0, 0, 0]
class_priori = [0, 0, 0, 0, 0]
class_cond = [MyDict() for i in range(0, 5)]
class_total = [0, 0, 0, 0, 0]




def prepare_data():
    global lines, doc, vocab
    print "Preparing Data....."
    for i in range(0, 5):
        print " Fetching and Normalizing Data for class ",i
        lines[i] = get_file_lines("data/train_"+str(i)+"_n.tsv")
        doc[i] = normalize_data(lines[i])
        vocab[i] = len(set(doc[i]))
    print "Data ready for training!"


def normalize_data(lines):
    norm_words = []
    punctuation = ['!', '.', ';', ':', '\'', '"','`','?']
    exceptions = ['\n', '\'s', '\'t', 'n\'t','not', " "]
    stemmer = PorterStemmer()
    stop = stopwords.words('english')
    print "    Now Normalizing......."
    for sentence in lines:
        words = [stemmer.stem(word) for word in word_tokenize(sentence.rstrip("\\n"))]
        norm_words.extend([word.lower() for word in words if not re.match("[0-9]+", word) if word.lower() not in list(itertools.chain(punctuation, exceptions, stop))])
    return norm_words

def calculate_class_priori():
    doc_sizes = [len(lines[i]) for i in range(0, 5)]
    return [(1.0*doc_sizes[i]/sum(doc_sizes)) for i in range(0, 5)]

def train():
    global class_priori, class_cond, class_total
    print "Training Data......."
    class_priori = calculate_class_priori()
    print "Priori Calculated!"
    for i in range(0, 5):
        j = 0
        print "Length of class ",len(doc[i])
        print "Calculating class conditional/total probabilities for class ", i
        class_cond[i] = read_features(i)
        if class_cond[i] is None:
            class_cond[i] = MyDict()
            for word in doc[i]:
                if doc[i].count(word) > 2:
                    class_cond[i][word] = doc[i].count(word) #word frequencies

                j += 1
                if j % 5000 == 0:
                    print j, "Features trained on!"
                    if j == 50000:
                        break


        dump_features(i, class_cond[i])
        class_cond[i] = []
        class_total[i] = sum(class_cond[i].values())
    print class_priori, class_total, class_cond

def classify(lines):
    posteriori = [0, 0, 0, 0, 0]
    matches = 0
    counter = 0
    [sentences, scores] = get_sentence_canonical(lines)
    for sentence, score in [sentences, scores]:
        for i in range(0, 5):
            class_cond[i] = read_features(i)
            posteriori[i] = sum(log10( (class_cond[i][word] + 1.0)/(class_total[i] + vocab[i]) for word in sentence)  + log10(class_priori[i]) )
        if score - posteriori.index(max(posteriori)) == 0:
            print sentence, score
            matches += 1
        counter += 1
        print matches*(1.0)/counter
    print sentences, scores

    #sum(class_cond[i].values())

def dump_features(classi, class_condi):
    nfile = open("data/NaiveBayes_Features_"+str(classi)+".txt", "w")
    for word, prob in class_condi.iteritems():
        nfile.write(word+","+str(prob)+"\n")
    nfile.close()

def read_features(classi):
    temp = MyDict()
    if not os.path.exists("data/NaiveBayes_Features_"+str(classi)+".txt"):
        return None
    for line in get_file_lines("data/NaiveBayes_Features_"+str(classi)+".txt"):
        ld = line.split(",")
        temp[ld[0]] = int(ld[1].rstrip("\\n"))
    if temp.__sizeof__() == 0:
        return None
    return temp

def get_file_lines(file, mode='r'):
    file_handler = open(file, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines

def get_sentence_canonical(lines):
    sentences = [normalize_data([get_sentence_details(line, 2)]) for line in lines]
    scores = [get_sentence_details(line, 3) for line in lines]
    return [sentences, scores]


def get_sentence_details(lines, i):
    return lines.split("\t")[i];

prepare_data()
train()
classify(get_file_lines("data/test.tsv"))