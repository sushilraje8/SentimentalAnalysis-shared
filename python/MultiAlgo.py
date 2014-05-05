import scipy
import sklearn
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import fetch_mldata
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, PorterStemmer,pos_tag
from nltk.corpus import stopwords
from sklearn.feature_extraction import stop_words
from sklearn import metrics
from sklearn import linear_model, naive_bayes, svm

#configure
lem_ch = 2
vect_ch = 1
algo_ch = 1
param_ch = [1, 10, 10]


corpus = []
corpus_test = []
X = []
X_test = []
y = []
y_test = []
stemmer = PorterStemmer()
def get_file_lines(file, mode='r'):
    file_handler = open(file, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines
opt = []

class Lemmaword_tokenizer(object):
    def __init__(self,opt):
        self.wnl = WordNetLemmatizer()
        self.option = opt
    def __call__(self, doc):
        if self.option == 1:
            return [word.lower() for word in word_tokenize(doc)]
        elif self.option == 2:
            return [stemmer.stem(word).lower() for word in word_tokenize(doc)]
        elif self.option == 3:
            print doc+"\n"
            return [stemmer.stem(word).lower() for word in word_tokenize(self.filterNouns(doc))]
        elif self.option == 4:
            return [word.lower() for word in word_tokenize(doc)]
        else:
             return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
    def filterNouns(words):
        word_tags = pos_tag(words)
        return [word_tag[0] for word_tag in word_tags if word_tag[1] not in ["NN", "NNP", "NNS", "NN$"]]


for i in range(0, 5):
    data = get_file_lines("data/train_"+str(i)+".tsv")
    corpus.extend(data)
    y.extend([i for x in range(0, len(data))])
data = []
for i in range(0, 5):
    data = get_file_lines("data/test_"+str(i)+".tsv")
    corpus_test.extend(data)
    y_test.extend([i for x in range(0, len(data))])


if vect_ch == 1:
    vectorizer = TfidfVectorizer(lowercase=True,tokenizer=word_tokenize,ngram_range=(1, 3),token_pattern=r'\b\w+\b', stop_words='english', use_idf=1)
else:
    vectorizer = CountVectorizer(ngram_range=(1, 3),token_pattern=r'\b\w+\b',tokenizer=Lemmaword_tokenizer(lem_ch), stop_words='english')

X = vectorizer.fit_transform(corpus)
X_test = vectorizer.transform(corpus_test)

if algo_ch == 1:
    clf = naive_bayes.MultinomialNB(alpha=param_ch[0])
elif algo_ch == 2:
    clf = svm.SVC(kernel='rbf',C=param_ch[1])
elif algo_ch == 3:
    clf = linear_model.LogisticRegression(C=param_ch[2])



clf.fit(X, y)
pred = clf.predict(X_test)
print "Accuracy :", metrics.accuracy_score(y_test, pred)
print "Precision :", metrics.precision_score(y_test, pred)
print "Recall :", metrics.recall_score(y_test, pred)
print "F1 Score", metrics.f1_score(y_test, pred)
print "Confusion Matrix"
print metrics.confusion_matrix(y_test, pred)
print "MI score", metrics.mutual_info_score(y_test, pred)