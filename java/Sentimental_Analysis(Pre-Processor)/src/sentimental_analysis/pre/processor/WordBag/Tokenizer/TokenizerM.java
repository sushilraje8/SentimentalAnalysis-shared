/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package sentimental_analysis.pre.processor.WordBag.Tokenizer;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
/**
 *
 * @author Sushil-PC
 */
public class TokenizerM {
  

    private TokenizerME tokenizer;
   
    public void setUp(){
        
        
        TokenizerModel Tmodel = initialiseTokenizer();
        getTokenizerH(Tmodel);
    }

    /**
     *
     * @param Sentences
     * @return
     */
    public HashSet<String> getTokens(String[] Sentences){
        ArrayList<String> tokens = new ArrayList<>();
        StopWordFilter SWF = new StopWordFilter();
        NameFilter NF = new NameFilter();
        stemmerWrap SW = new stemmerWrap();
        PartsofSpeechFilter POSF = new PartsofSpeechFilter() ;
        for (String sentence : Sentences ){
            tokens.addAll(Arrays.asList((NF.filterNames(SWF.filterStopWords(cleanWord(POSF.filterNouns(tokenizer.tokenize(sentence)))))))); 
            
        }
        return new HashSet<>(tokens);
    }
    private String[] cleanWord(String[] tokens){
        int i = 0;
        for( String token : tokens){
            tokens[i] = token.replaceAll("(\'|\")","");
        }
        return tokens;
    }
    
    
    
    //Set Up Helper function
    private TokenizerModel initialiseTokenizer(){
        try {
            FileInputStream modelIn = new FileInputStream("C:\\Users\\Sushil-PC\\Dropbox\\SentimentalAnalysis-shared\\java\\en-token.bin");
            try {
                return new TokenizerModel(modelIn);
            }
            catch (IOException ex) {
                System.out.println("Exception Thrown Tokenizer Model (TokenizerModel) : "+ex.getMessage());
                System.out.println("Stack Trace");
                ex.printStackTrace();
            }
        } catch (FileNotFoundException ex) {
            Logger.getLogger(TokenizerM.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("Exception Thrown En-Token-bin : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
        return null;
    }
    
    private void getTokenizerH(TokenizerModel Tmodel){
        if( Tmodel == null){
            System.out.println("Tokenizer Model is NULL!");
        } 
        try{
            tokenizer = new TokenizerME(Tmodel);
        }catch(Exception ex){
            System.out.println("Exception Thrown Tokenizer (getTokenizerH) : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
    }
   
    
}



