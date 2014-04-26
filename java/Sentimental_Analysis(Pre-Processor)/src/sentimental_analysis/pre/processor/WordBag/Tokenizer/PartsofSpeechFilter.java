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
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.postag.POSModel;
import opennlp.tools.util.Span;
import org.apache.commons.lang3.ArrayUtils;

/**
 *
 * @author Sushil-PC
 */
public class PartsofSpeechFilter {
    
    
    private POSTaggerME POSTagger;
   
    public void setUp(){
        POSModel Pmodel = initialisePOS();
        getPOSTaggerME(Pmodel);
    }
    public String[] filterNouns(String[] tokens){
        setUp();
        String[] tags = new String[tokens.length];
        ArrayList<String> newTokens = new ArrayList<>();
        tags = POSTagger.tag(tokens);
        Integer[] positions = getTagstoInclude(tags);
        for(Integer pos:positions ){
            newTokens.add(tokens[pos]);
            //System.out.println(tokens[pos]);
        }
        return newTokens.toArray (new String [newTokens.size ()]);                   
    }
    //Set Up Helper function
    private POSModel  initialisePOS(){
        try {
            FileInputStream modelIn = new FileInputStream("C:\\Users\\Sushil-PC\\Dropbox\\SentimentalAnalysis-shared\\java\\en-pos-maxent.bin");
            try {
                return new POSModel(modelIn);
            }
            catch (IOException ex) {
                System.out.println("Exception Thrown POS Model (initialisePOS) : "+ex.getMessage());
                System.out.println("Stack Trace");
                ex.printStackTrace();
            }
            
        } catch (FileNotFoundException ex) {
            Logger.getLogger(TokenizerM.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("Exception Thrown En-pps-maxent-bin : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
        return null;
    }
    
    private void getPOSTaggerME(POSModel Pmodel){
        if( Pmodel == null){
            System.out.println("POS Model is NULL!");
        } 
        try{
            POSTagger = new POSTaggerME(Pmodel);
        }catch(Exception ex){
            System.out.println("Exception Thrown POSTaggerME (getPOSTaggerME) : "+ex.getMessage());
            System.out.println("Stack Trace");
            ex.printStackTrace();
        }
    }
    
    private Integer[] getTagstoInclude(String[] tags){
    
        ArrayList<Integer> positions = new ArrayList<>();
        String[] POS = new String[] {
            "FW",
            "JJ",
            "JJR",
            "JJS",
            "RB",
            "RBR",
            "RBS",
            "POS",
            "UH",
            "VB",
            "VBD",
            "VBG",
            "VBN",
            "VBZ"
        };
        String[] POSi = new String[] {
            "NN",
            "NNS",
            "NNP",
            "NNPS"
        };
        int i = 0;
        for(String tag:tags){
            if(!ArrayUtils.contains(POSi, tag.trim())){
                positions.add(i);
            }
            i++;
        }
        int[] pos = new int[i];
        Integer [] intArray = new Integer[positions.size()];
        return (positions.toArray(intArray));
    }
}


/*

LoveAngerHatePeaceLoyaltyIntegrityPrideCourageDeceitHonestyTrustCompassionBraveryMiseryChildhoodKnowledgePatriotismFriendshipBrillianceTruthCharityJusticeFaithKindnessPleasureLibertyFreedomDelightDespairHopeAweCalmJoyReality

*/