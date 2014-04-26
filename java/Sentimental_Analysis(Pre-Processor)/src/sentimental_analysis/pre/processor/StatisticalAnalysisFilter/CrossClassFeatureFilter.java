/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package sentimental_analysis.pre.processor.StatisticalAnalysisFilter;
import sentimental_analysis.pre.processor.WordBag.Tokenizer.stemmerWrap;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

import sentimental_analysis.pre.processor.Sentimental_AnalysisPreProcessor;
/**
 *
 * @author Sushil-PC
 */
public class CrossClassFeatureFilter extends Sentimental_AnalysisDictStats {
    
    public static void main(String[] args){
        
      CrossClassFeatureFilter CCFF = new CrossClassFeatureFilter();
        CCFF.setUp();
        String[] newFeatures = CCFF.filterFeatures(CCFF.getCrossClassReferences(),"dictionary\\tempUniGramDictionary");
        for(String feature:newFeatures)
            System.out.println(feature);
    
    
    }
    @Override
    protected void setUp(){
        super.setUp();
    }
    String[] filterFeatures(Set<String>[] ccfeaturevectors, String dict_path){
        stemmerWrap SW = new stemmerWrap();
        Set<String> dictionary = new HashSet<>(Arrays.asList(SW.stem(getData(dict_path))));
        Set<String> ccfeaturevector = new HashSet<>();
        System.out.println("****************************************************************************************");
        for(Set<String> features:ccfeaturevectors){
            ccfeaturevector.addAll(features);
        }
        System.out.println(dictionary.size());
        System.out.println(ccfeaturevector.size());
        try{
            dictionary.removeAll(ccfeaturevector);
        }catch(Exception e){
            System.out.println("Exception Thrown cross class feature (filterFeatures) : "+e.getMessage());
            System.out.println("Stack Trace");
            e.printStackTrace();
        }
        System.out.println(dictionary.size());

        return dictionary.toArray(new String[dictionary.size()]);
    }
}
