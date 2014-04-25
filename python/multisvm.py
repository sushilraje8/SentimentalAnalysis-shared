import sys
sys.path.append('C:\Users\Sushil-PC\Dropbox\SentimentalAnalysis-shared\python\libsvm-3.18\libsvm-3.18\python')
from svmutil import *
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import PorterStemmer
import pickle

X = [[]]
y = [[] for i in range(0, 5)]
dictionary = []
model = [0, 0, 0, 0, 0]
stemmer = PorterStemmer();

def prepare_dictionary():
    global dictionary
    if len(dictionary) is 0:
        print "     Preparing dictionary....."
        #dictionary = [word.rstrip("\n") for word in get_file_lines("dictionary/tempDictionary.txt")]
        dictionary = [stemmer.stem_word(word.rstrip("\n")) for word in get_file_lines("dictionary/tempDictionary")]

def vectorize_data(sentences, scores):
    global X, y, dictionary
    print "     Preparing Vectorized input......."
    #X = [[1 if sentence.__contains__(word) else 0 for word in dictionary] for sentence in sentences]
    X = [[1 if sentence.__contains__(word) else 0 for word in dictionary] for sentence in sentences]
    print "     Preparing vectorized labels......."
    y = scores

def get_sentence_scores(train_data):
    print "Getting training Data details......"
    prev_indx = -1
    sentences = []
    scores = []
    i = 0
    for line in train_data:
        if i < 7000:
        #curr_indx = int(line.split("\t")[1])
        #if curr_indx != prev_indx:
            """
            tokens = [word for word in word_tokenize(str(line.split("\t")[2]))]
            sentences.append(tokens)
            """
            stemed_tokens = [stemmer.stem(word) for word in word_tokenize(str(line.split("\t")[2]))]
            sentences.append(stemed_tokens)
            scores.append(int(line.split("\t")[3]))
            i += 1
        #prev_indx = curr_indx
    return [sentences, scores]

def prepare_data():
    print "Preparing Data....."
    print "Reading vectorized Data....."
    #X = pickle_read_wrapper("data/vector_data")
    #y = pickle_read_wrapper("data/vector_label")
    if len(X) is 1 or len(y) is not 5:
        print "Vectorized data Not found! Vectorizing again...."
        train_data = get_file_lines("data/trainML.tsv")
        [sentences, scores] = get_sentence_scores(train_data)
        prepare_dictionary()
        vectorize_data(sentences, scores)
        print "     Dumping Vectorized Data....."
        #pickle_dump_wrapper(X, "data/vector_data")
        #pickle_dump_wrapper(y, "data/vector_label")

def train():
    prob = svm_problem(y, X)
    linear_kernel = '-t 0 -c 10  -b 1'
    gaussian_kernel = '-t 2 -c 50 -g 50'
    param = svm_parameter(gaussian_kernel)
    return svm_train(prob, param)

def get_models():
    for i in range(0, 5):
        model[i] = svm_load_model('models/Movie_Reviews-'+str(i)+'.model')

def predict(test_data):
    [sentences, scores] = get_sentence_scores(test_data)
    vectorize_data(sentences, scores)
    y_final = [0 for i in range(0, len(y[0]))]
    y_display = [0 for i in range(0, len(y[0]))]
    for i in range(0, 5):
        print "Checking for class ", i
        p_label, p_acc, p_val = svm_predict(y[i], X, model[i])
        y_final = [j if p_label[int(j)] == 1.0 else y_final[key] for key, j in enumerate(p_label)]
        print y[i].count(1), p_label.count(1.0), len(p_label)
        print "Label: ", p_label
        print "Y Final: ", y_final
    """
    for i in range(0, 5):
        y[i] = [i if y[i] is 1 in y[key] else 0 for key, i in enumerate(y[i])]
    for i in range(0, 5):
        for j in range(0, len(y[0])):
            y_display[j] += y[i][j]
    print [y_display]
    print y_final
    """



def predict2(test_data):
    [sentences, scores] = get_sentence_scores(test_data)
    vectorize_data(sentences, scores)
    y_final = [0 for i in range(0, len(y[0]))]
    y_display = [0 for i in range(0, len(y[0]))]

    cnt = 0
    print "Checking for class ", i
    p_label, p_acc, p_val = svm_predict(y[i], X, model[i])
    y_final = [j if p_label[int(j)] == 1.0 else y_final[key] for key, j in enumerate(p_label)]
    for key, j in enumerate(p_label):
        if p_label[int(j)] == j:
            cnt += 1
    print "Number of output label 1 ", cnt
    print "Number of orig label 1 ", y
    print "Label: ", p_label
    print "Y Final: ", y_final
    """
    for i in range(0, 5):
        y[i] = [i if y[i] is 1 in y[key] else 0 for key, i in enumerate(y[i])]
    for i in range(0, 5):
        for j in range(0, len(y[0])):
            y_display[j] += y[i][j]
    print [y_display]
    print y_final
    """



def get_file_lines(file, mode='r'):
    file_handler = open(file, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines

def pickle_read_wrapper(file):
    if file is None:
        print "Pickle Error: file empty"
        return
    oFile = open(file, "rb")
    obj = pickle.load(oFile)
    oFile.close()
    return obj

def pickle_dump_wrapper(obj, file):
    if obj is None or file is None:
        print "Pickle Error: file or Obj empty"
        return
    oFile = open(file, "wb")
    pickle.dump(obj, oFile)
    oFile.close()

def main(re_train):
    global model
    if re_train:
        prepare_data()
        model = train()

        for i in range(0, 5):
            print "Saving model!!!!...."
            svm_save_model('models/Movie_Reviews_multi_class-'+str(i)+'.model', model[i])
    else:
        get_models()


    test_data = get_file_lines("data/trainML.tsv")

    predict(test_data)
    #predict2(test_data)




main(1)