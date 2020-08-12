/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Tandem repeat search 
 * 
 * checking for the consecutive occurences of pattern
 * and  returning the longest string of consecutive occurence
 * 
 */

public class Ex_5_3_27 {
	
	public int[] res;
	
	public Ex_5_3_27(String orig,String test){
		
		String text = test;
		Ex_5_3_9 bm = new Ex_5_3_9(orig);
		bm.searchAll(text);
		this.res = bm.occ;
		
		int diff = orig.length();
		int max=0,count=0; 
		for(int i=0; i<res.length-1; i++){
			
			if(res[i+1]-res[i] == diff){
				//StdOut.println(res[i]+":"+res[i+1]+":"+count);
				count++;
			}  else {
				if(max<count) max = count;
				count=0;
			}
		}
		
		StdOut.println(max);
		
	}
	
	
	
	public static void main(String args[]){
		String orig = "abcab",test = "abcabcababcababcababcab";
		Ex_5_3_27 ob = new Ex_5_3_27(orig,test);
	}

}
