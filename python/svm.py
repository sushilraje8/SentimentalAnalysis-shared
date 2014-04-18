
from nltk.tokenize import word_tokenize

def get_word_list(sentences, index):
    print "Preparing Word List ", index, "......."
    global word_list,stemmer
    for sentence in sentences:
        #wordlist[index].extend(tokenize.word_tokenize(sentences[i])) #CLEAN document!!
        word_list[index].extend([stemmer.stem(word.lower()) for word in set(word_tokenize(sentence))]) #CLEAN document!!
    #print wordlist[index]

def get_file_lines(file, mode='r'):
    file_handler = open(file, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines

def main():
    for i in range(0, 5):
        get_word_list(get_file_lines("data/train_" + str(i) + ".tsv"), i)
   # train(get_file_lines('dictionary/tempDictionary.txt'))