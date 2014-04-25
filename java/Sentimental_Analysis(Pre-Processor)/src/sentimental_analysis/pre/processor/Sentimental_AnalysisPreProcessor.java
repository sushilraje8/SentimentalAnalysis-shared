/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package sentimental_analysis.pre.processor;
import java.io.*;
import org.apache.commons.lang3.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;
import sentimental_analysis.pre.processor.WordBag.Tokenizer.NameFilter;
import sentimental_analysis.pre.processor.WordBag.Tokenizer.StopWordFilter;
import sentimental_analysis.pre.processor.WordBag.Tokenizer.TokenizerM;

/**
 *
 * @author Sushil-PC
 */
public class Sentimental_AnalysisPreProcessor {

    /**
     * @param args the command line arguments
     */
    
    public static void main(String[] args)  {
        Sentimental_AnalysisPreProcessor SAP = new Sentimental_AnalysisPreProcessor();
        TokenizerM tokenizerM = new TokenizerM();
        tokenizerM.setUp();
        String[] Sentences = SAP.getData("trainML.tsv",1,6000);//
        Set tokens = tokenizerM.getTokens(Sentences);
        SAP.saveTokens("tempDictionarywonouns.txt",tokens);
         
        
    }
    protected String[] getData(String file_name, int start_line, int number_of_sentences){
        
        String line = "";
        String[] lineContents = new String[4];
        int line_counter = 1,current_sentence = -1, previous_sentence = -1, sentence_counter = 0;
        String[] fData = new String[number_of_sentences];
        try {
            BufferedReader buffer = new BufferedReader(new FileReader("C:\\Users\\Sushil-PC\\Dropbox\\SentimentalAnalysis-shared\\python\\data\\"+file_name));
            while((line = buffer.readLine()) != null){
                lineContents = line.split("\t");
                current_sentence = Integer.parseInt(lineContents[1]);
                if(start_line <= line_counter && current_sentence != previous_sentence){
                    if(sentence_counter < number_of_sentences){
                        fData[sentence_counter] = lineContents[2]; 
                        sentence_counter++;
                    }else{
                        break;
                    }
                }  
                previous_sentence = current_sentence;
                line_counter++;
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
    private FileInputStream getFile(String file){
        try {
            return new FileInputStream(file);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Sentimental_AnalysisPreProcessor.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("Exception Thrown Data File (main) : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
        return null;
    }
    /*
     public Set<String> filterTokens(String[] tokens){
        ArrayList<String> tokenSet = new ArrayList<>();
        StopWordFilter SWF = new StopWordFilter();
        NameFilter NF = new NameFilter();
        tokenSet.addAll(Arrays.asList(NF.filterNames(SWF.filterStopWords(tokens))));
        return new HashSet<>(tokenSet);
    }
     */
     protected void saveTokens(String dictionary_name, Set tokens){
        try {
            FileWriter dictionary = new FileWriter("C:\\Users\\Sushil-PC\\Dropbox\\SentimentalAnalysis-shared\\python\\dictionary\\"+dictionary_name);
            System.out.println(StringUtils.join(tokens,","));
            dictionary.write(StringUtils.join(tokens,"\n"));
            dictionary.close();
        } catch (IOException ex) {
            Logger.getLogger(Sentimental_AnalysisPreProcessor.class.getName()).log(Level.SEVERE, null, ex);
        }
     
     }
     
     
}
