/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sentimental_analysis.pre.processor.WordBag.Tokenizer;
import sentimental_analysis.pre.processor.WordBag.Tokenizer.PorterStemmer;
/**
 *
 * @author Sushil-PC
 */
public class stemmerWrap {
    
    private PorterStemmer PS;
    private void setUp(){
    
        PS = new PorterStemmer();
        PS.reset();
    }
    public String[] stem(String[] tokens){
        setUp();
        int i = 0;
        for( String token: tokens){
            tokens[i] = PS.stem(token);
            PS.reset();
            i++;
        }
        return tokens;
    }
            
}
