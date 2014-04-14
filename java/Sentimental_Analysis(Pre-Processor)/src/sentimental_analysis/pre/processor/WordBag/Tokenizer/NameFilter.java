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
import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import org.omg.CORBA.portable.InputStream;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import opennlp.tools.namefind.NameFinderME;
import opennlp.tools.namefind.TokenNameFinderModel;
import opennlp.tools.util.Span;
import opennlp.uima.namefind.NameFinder;
/**
/**
 *
 * @author Sushil-PC
 */
public class NameFilter {
    
    /*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/*
 * @author Sushil-PC
 */
    private NameFinderME NameFinder;
   
    public void setUp(){
        TokenNameFinderModel  Tmodel = initialiseNameFinder();
        getNameFinderMe(Tmodel);
    }
    public String[] filterNames(String[] tokens){
        setUp();
        ArrayList<String> newTokens = new ArrayList<>(Arrays.asList(tokens));
        for(int i = 0 ; i < newTokens.size(); i++){
            Span[] isName = NameFinder.find(new String[] {newTokens.get(i).trim()});
            if(isName.length > 0 && "person".equals(isName[0].getType().toString().trim())){
                newTokens.remove(i);
                i--;
            }
        }
        return newTokens.toArray (new String [newTokens.size ()]);                   
    }
    //Set Up Helper function
    private TokenNameFinderModel  initialiseNameFinder(){
        try {
            FileInputStream modelIn = new FileInputStream("C:\\Users\\Sushil-PC\\Dropbox\\SentimentalAnalysis-shared\\java\\en-ner-person.bin");
            try {
                return new TokenNameFinderModel(modelIn);
            }
            catch (IOException ex) {
                System.out.println("Exception Thrown Name FInder Model (TokenNameFinderModel) : "+ex.getMessage());
                System.out.println("Stack Trace");
                ex.printStackTrace();
            }
        } catch (FileNotFoundException ex) {
            Logger.getLogger(TokenizerM.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("Exception Thrown En-per-Token-bin : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
        return null;
    }
    
    private void getNameFinderMe(TokenNameFinderModel Tmodel){
        if( Tmodel == null){
            System.out.println("TokenNameFinder Model is NULL!");
        } 
        try{
            NameFinder = new NameFinderME(Tmodel);
        }catch(Exception ex){
            System.out.println("Exception Thrown TokenNameFinder (getNameFinderMe) : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
    }
}




    

