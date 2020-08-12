/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/******************************************************
 * BOYER MOORE SUBSTRING SEARCH
 * 
 * Initially computes a skip array which tells us how far
 * should we skip in order to match the pattern elements 
 * 
 * Search always compares from right to left 
 * 
 * Time: O(N/M)
 * Space: Storage(true)
 * 
 ******************************************************/

public class BoyerMoore {
	
	private int[] right;
	private String pat;
	
	public BoyerMoore(String pat){
		this.pat = pat; int R =256,M=pat.length();
		right = new int[R];
		
		for(int i=0; i<R; i++)
			right[i]= -1;
		
		for(int i=0; i<M; i++)
			right[pat.charAt(i)] = i;

	}
	
	public int search(String txt){
		int N = txt.length(),M = pat.length();
		int i,j,skip=0;
		for(i=0; i<N-M ;i+=skip){
			skip=0;
			for(j=M-1; j>=0; j--){
				if(pat.charAt(j)!= txt.charAt(i+j)){
					skip = j-right[txt.charAt(i+j)];
					if(skip<1) skip=1;
					break;
				}
			}
			if(skip==0) return i;
		}
		return N;
	}
	
	public static void main(String args[]){
		int M= 15,N=10000;
		String pat = new RandomData().generateRandomString(M);
		String txt = new RandomData().generateRandomString(N);
		StdOut.println("Text: "+txt+"\n"+"Pattern: "+pat);
		BoyerMoore bm = new BoyerMoore(pat);
		int val = bm.search(txt);
		if(val<N) StdOut.println("Found at: "+ val+": "+txt.substring(val,val+M));
		else StdOut.println("Match not found !");
	}

}
