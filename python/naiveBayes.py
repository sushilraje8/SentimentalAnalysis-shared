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
        doc[i] = read_normalized_data(i)
        if doc[i] is None:
            doc[i] = normalize_data(lines[i])
            dump_normalized_data(i, doc[i])
        vocab[i] = len(set(doc[i]))
    print "Data ready for training!"


def normalize_data(lines):
    norm_words = []
    punctuation = ['!', '.', ';', ':', '\'', '"','`','?']
    exceptions = ['\n', '\'s', '\'t', " "]
    stemmer = PorterStemmer()
    stop = stopwords.words('english')
    mega_stop_list = list(itertools.chain(punctuation, exceptions))
    print "    Now Normalizing......."
    for sentence in lines:
        words = [stemmer.stem(word.lower()) for word in word_tokenize(sentence.rstrip("\\n")) if word not in [stop, "not"]]
        norm_words.extend([word for word in negate_Ngram(words) if not re.match("[0-9]+", word) if word.lower() not in mega_stop_list])
    return norm_words

def negate_Ngram(words):
    negation = False
    #delims = "?.,!:;"
    result = []
    prev = None
    pprev = None
    for word in words:
        #stripped = word.strip(delims).lower()
        negated = "not_" + word if negation else word
        result.append(negated)
        if prev:
            bigram = prev + " " + negated
            #result.append(bigram)
            if pprev:
                trigram = pprev + " " + bigram
                #result.append(trigram)

            pprev = prev
        prev = negated
        if any(neg in word for neg in ["not", "n't", "no"]):
            negation = not negation
        if any(c in word for c in "?.,!:;"):
            negation = False
    return result

def filterNouns(words):
    word_tags = pos_tag(words)
    return [word_tag[0] for word_tag in word_tags if word_tag[1] not in ["NN", "NNP", "NNS", "NN$"]]


def calculate_class_priori():
    doc_sizes = [len(lines[i]) for i in range(0, 5)]
    return [(1.0*doc_sizes[i]/sum(doc_sizes)) for i in range(0, 5)]




def train(threshold):
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
                if not class_cond[i].has_key(word) and doc[i].count(word) > threshold:
                        class_cond[i][word] = doc[i].count(word) #word frequencies
                j += 1
                if j % 5000 == 0:
                    print j, "Features trained on!"
                if j >= 200000:
                    break
            dump_features(i, class_cond[i])
        class_total[i] = sum(class_cond[i].values())
    prune_features()
    print class_priori, class_total, class_cond


def prune_features():
    feature_MI = MyDict()
    print "Pruning Features....."
    for i in range(0, 5):
        for keys in read_features(i):
            feature_MI[keys] = Mutual_Info(keys)
            max_MI = max(data for data in feature_MI.values())
            min_MI = min(data for data in feature_MI.values())
            threshold = ((max_MI - min_MI)/2) + min_MI
            for fMI in feature_MI:
                fMI = fMI.strip()
                for j in range(0, 5):
                    if class_cond[j].has_key(fMI) and threshold > class_cond[j][fMI]:
                        print "Length", len(class_cond[j])
                        del class_cond[j][fMI]
                        print "Length", len(class_cond[j])


def Mutual_Info(word):
    #print "Calculating Mutual Info......"
    total = sum(class_total);
    MI = 0
    for i in range(0, 5):
        joint_prob_cw = (class_cond[i][word] + 1) / total  #laplace smoothing
        prob_w = sum(class_cond[j][word] for j in range(0, 5)) / total
        prob_c = class_total[i] / total

        joint_prob_cnw = (class_total[i] - class_cond[i][word]) / total
        prob_nw = sum( (class_total[j] - class_cond[j][word]) for j in range(0, 5)) / total
        MI += joint_prob_cw * log10( joint_prob_cw / ( prob_w * prob_c ) ) / (2.30258)
        MI += joint_prob_cnw * log10( joint_prob_cnw / ( prob_nw * prob_c ) ) / (2.30258)
    return MI


def classify(lines):
    posteriori = [0, 0, 0, 0, 0]
    matches = 0
    counter = 0
    [sentences, scores] = get_sentence_canonical(lines)
    for sentence, score in zip(sentences, scores):
        for i in range(0, 5):
            class_cond[i] = read_features(i)
            log_prob = [log10((class_cond[i][word] + 1.0)/(class_total[i] + vocab[i])) for word in sentence]
            log_prob.append(log10(float(class_priori[i])))
            posteriori[i] = sum(log_prob)
        if int(score) - posteriori.index(max(posteriori)) == 0:
            print sentence, score
            matches += 1
        counter += 1
        print matches*(1.0)/counter
    print sentences, scores

    #sum(class_cond[i].values())
def dump_normalized_data(classi, doc):
    nfile = open("data/NaiveBayes_NormData_"+str(classi)+".txt", "w")
    nfile.write("~!~".join(doc))
    nfile.close()

def read_normalized_data(classi):
    if not os.path.exists("data/NaiveBayes_NormData_"+str(classi)+".txt"):
        return None
    nfile = open("data/NaiveBayes_NormData_"+str(classi)+".txt", "r")
    doc = nfile.read().split("~!~")
    nfile.close()
    return doc


def dump_features(classi, class_condi):
    nfile = open("feature/NaiveBayes_Features_"+str(classi)+".txt", "w")
    for word, prob in class_condi.iteritems():
        nfile.write(word+"~!~"+str(prob)+"\n")
    nfile.close()

def read_features(classi):
    temp = MyDict()
    if not os.path.exists("feature/NaiveBayes_Features_"+str(classi)+".txt"):
        return None
    for line in get_file_lines("feature/NaiveBayes_Features_"+str(classi)+".txt"):
        ld = line.split("~!~")
        if ld[0].strip() != "":
            temp[ld[0].strip()] = float(ld[1].strip().rstrip("\\n"))
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
train(5) #passing threshold a pre-pruning
classify(get_file_lines("data/test.tsv"))