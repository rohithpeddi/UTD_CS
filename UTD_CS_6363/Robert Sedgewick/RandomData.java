/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdRandom;

/*************************

 * @author rohith peddi

 *************************/
public class RandomData {
	
	String lcasebl = "abcdefghijklm nopqrstuvwxyz";
	String lcase = "abcdefghijklmnopqrstuvwxyz";
	String binary = "01";
	
	public String generateRandomString(int N){
		
		String st="";
		
		for(int i=0; i<N; i++){
			int n = StdRandom.uniform(0, 26);
			st+= lcase.charAt(n);
		}
		
		return st;
	}

}
