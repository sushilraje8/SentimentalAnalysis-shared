
import string
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
def get_file_lines(file1, mode='r'):
    file_handler = open(file1, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines

stopword_list = stopwords.words('english')

def find_bigrams(input_list):
    return [(input_list[i]) + " " + input_list[i+1] + "\n"  for i in range(0,(len(input_list)-1)) if input_list[i] not in stopword_list and input_list[i+1] not in stopword_list]


def bi_grams(datafile,idex):
    curr_sent = 0
    prev_sent = -1
    words = []
    try:
        file_data = get_file_lines(datafile)
        file2=open("dictionary/tempDictionary.txt",'a')
        for line in file_data:
            curr_sent = get_sentence_num(line)
            if prev_sent != curr_sent:
                words = [word.strip(string.punctuation).lower().strip() for word in list((word_tokenize(get_sentence(line)))) if str(word.strip(string.punctuation).lower().strip()) != ""]
                bigram_dict = find_bigrams(words)
                file2.writelines(bigram_dict)
            prev_sent = curr_sent
    except IOError:
                print "I could not find the file, Please try again."
                exit()

def get_sentence(line):
    columns = line.split("\t");
    return str(columns[2].strip("'"))

def get_sentence_num(lines):
    columns = lines.split("\t");
    return int(columns[1].strip("'"))

def main():
    bi_grams("data/trainML.tsv",1)
main()