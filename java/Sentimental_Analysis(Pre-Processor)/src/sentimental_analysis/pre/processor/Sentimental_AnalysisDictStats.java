package sentimental_analysis.pre.processor;
import java.util.Set;
import sentimental_analysis.pre.processor.Sentimental_AnalysisPreProcessor;
import sentimental_analysis.pre.processor.WordBag.Tokenizer.TokenizerM;
/**
 *
 * @author Sushil-PC
 */
public class Sentimental_AnalysisDictStats extends Sentimental_AnalysisPreProcessor{
    
    public static void main(String[] args){
        Sentimental_AnalysisPreProcessor SAP = new Sentimental_AnalysisPreProcessor();
         TokenizerM tokenizerM = new TokenizerM();
         tokenizerM.setUp();
         for(int i=0; i < 2; i++){
            String[] Sentences = SAP.getData("train_"+i+".tsv",1,6000);//
            Set tokens = tokenizerM.getTokens(Sentences);
         }
         
        
    
    }
    
    
    
    
}
