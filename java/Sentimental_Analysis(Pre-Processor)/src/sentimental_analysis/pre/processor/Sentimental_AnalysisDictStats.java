package sentimental_analysis.pre.processor;
import java.io.BufferedReader;
import java.util.Set;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.logging.Level;
import java.util.logging.Logger;
import sentimental_analysis.pre.processor.Sentimental_AnalysisPreProcessor;
import sentimental_analysis.pre.processor.WordBag.Tokenizer.TokenizerM;
import org.apache.commons.lang3.*;
/**
 *
 * @author Sushil-PC
 */
public class Sentimental_AnalysisDictStats extends Sentimental_AnalysisPreProcessor{

    public static void main(String[] args){
        Sentimental_AnalysisDictStats Dstats = new Sentimental_AnalysisDictStats();
        Set<String>[] class_dict = Dstats.getTokens(true);
        Set<String>[] crossReferences = Dstats.findCrossReferences(class_dict);
        Dstats.printCrossClassDict(crossReferences,"ref");
        Set<String>[] crossDifferences = Dstats.findCrossDifferences(class_dict);
    }

    private Set<String>[] getTokens(boolean retokenize){
        System.out.println("Tokenizing");
        Set<String>[] tokens = new Set[5];
        if(retokenize){
            Sentimental_AnalysisPreProcessor SAP = new Sentimental_AnalysisPreProcessor();
            TokenizerM tokenizerM = new TokenizerM();
            tokenizerM.setUp();
            for(int i=0; i <= 4; i++){
                String[] Sentences = getData("train_"+i+".tsv",1,90);//
                tokens[i] = tokenizerM.getTokens(Sentences);
                SAP.saveTokens("dict_"+i+".txt", tokens[i]);
            }
        }
        System.out.println("Tokenizing finished!!");
        return tokens;
    }
    private Set<String>[] findCrossReferences(Set<String>[] class_dict){
        System.out.println("Cross References");
        int dict_size = class_dict.length, counter = 0;
        Set<String>[] crossReferences;
        crossReferences = new HashSet[10];
        for(int i = 0; i < dict_size; i++ ){
            for(int j = 0; j < dict_size; j++ ){
                if( i < j ){
                    try{
                        crossReferences[counter] = new HashSet<>(class_dict[i]);
                    }catch(Exception e){
                        System.out.println(e.getMessage());
                    }
                    crossReferences[counter].retainAll(class_dict[j]);
                    counter++;
                }
            }
        }
        System.out.println("Cross References Finished");
        return crossReferences;
    }
     private Set<String>[] findCrossDifferences(Set<String>[] class_dict){
        int dict_size = class_dict.length, counter = 0;
        Set<String>[] crossReferences = new HashSet[10];
        for(int i = 0; i < dict_size; i++ ){
            for(int j = 0; j < dict_size; j++ ){
                if( i < j ){
                    crossReferences[counter] = new HashSet<String>(class_dict[i]);
                    crossReferences[counter].removeAll(class_dict[j]);
                    counter++;
                }
            }
        }
        return crossReferences;
    }
    private void printCrossClassDict(Set<String>[] cross_class_dict, String type){

        switch(type){
            case "ref":
                System.out.println("Cross Refernces!!");
                break;
            default:
                break;
        }
        int dict_type = 0;
        for(Set class_dict:cross_class_dict){
            System.out.println("Cross Reference "+dict_type);
            Set<String> set_class_dict = new HashSet<String>(class_dict);
            for(String word:set_class_dict){
                
                System.out.println(word);
            }
            dict_type++;
        }

        
    }
     protected String[] getData(String file_name, int start_line, int number_of_sentences){
        
        String line = "";
        String[] lineContents = new String[4];
        int sentence_counter = 0;
        String[] fData = new String[number_of_sentences];
        try {
            System.out.println("C:\\Users\\Sushil-PC\\Dropbox\\SentimentalAnalysis-shared\\python\\data\\"+file_name);
            BufferedReader buffer = new BufferedReader(new FileReader("C:\\Users\\Sushil-PC\\Dropbox\\SentimentalAnalysis-shared\\python\\data\\"+file_name));
            while((line = buffer.readLine()) != null){
                if(sentence_counter < number_of_sentences){
                    fData[sentence_counter] = line; 
                    sentence_counter++;
                }
            }
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Sentimental_AnalysisPreProcessor.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("Exception Thrown Data File (main) : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        } catch (IOException ex) {
            Logger.getLogger(Sentimental_AnalysisPreProcessor.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("Exception Thrown Data File (main) : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
        return fData;
    }
}
