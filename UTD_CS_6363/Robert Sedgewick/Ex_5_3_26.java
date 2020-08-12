/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Cyclic rotation check
 * 
 * Concatenate the string to be tested with itself 
 * and search for the original string as the pattern 
 * 
 */

public class Ex_5_3_26 {
	
	public boolean isCycle;
	
	public Ex_5_3_26(String orig,String test){
		
		this.isCycle = false;
		String text = test+test;
		BoyerMoore bm = new BoyerMoore(orig);
		
		if(bm.search(text)<text.length()) isCycle=true;
		
	}
	
	public static void main(String args[]){
		String orig = "example",test = "ampleex";
		Ex_5_3_26 ob = new Ex_5_3_26(orig,test);
		StdOut.println(ob.isCycle);
	}

}
