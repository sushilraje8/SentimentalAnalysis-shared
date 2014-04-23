import string
from nltk.tokenize import word_tokenize
def get_file_lines(file1, mode='r'):
    file_handler = open(file1, mode)
    file_lines = file_handler.readlines()
    file_handler.close()
    return file_lines
def find_bigrams(input_list):
    return zip(input_list, input_list[1:])
    #return [input_list[i] + " " + input_list[i+1] for i in range(0,(len(input_list)-1))]
def bi_grams(datafile,idex):
    try:
        # read the contents of the whole file into ''filecontents''
        filecontents=get_file_lines(datafile)
        file2=open("bigramop.tsv",'w')
        #file2=open("./feature/Ngrams/bigram_"+ str(idex) + ".tsv", 'w')
        for filecontent in filecontents:
            file2.writelines(str(filecontent +"\n")) 
            # strip all punctuation at the beginning and end of words, and 
            # convert all words to lowercase
            words= [ word.strip(string.punctuation).lower() for word in set(word_tokenize(filecontent)) ]
            file2.writelines(word for word in words)
            file2.write("\n")                    
            bigram_dict=find_bigrams(words)
            for bigram_item in bigram_dict :
                file2.write(str(bigram_item) + "\n")
    except IOError:
                print "I could not find the file, Please try again."
                exit()      
def main():
    bi_grams("testtrain.tsv",1)
    #for i in range(0, 5):
        #get_word_list(get_file_lines("./data/train_" + str(i) + ".tsv"), i)
        #bi_grams(("./data/train_" + str(i) + ".tsv"), i)  
    #train(get_file_lines('tempDictionary.txt'))
    #classify(get_file_lines('test.tsv'))
main()