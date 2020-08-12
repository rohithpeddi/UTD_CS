/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/******************************************************
 * KNUTH MORRIS PRATT SUBSTRING SEARCH
 * 
 * Initially computes a DFA array which tells us the restart 
 * state of the pattern while the txt goes from left to right
 * without any change in the increment 
 * 
 * Search plays with the state of the pattern variable
 * 
 * Time: O(N)
 * Space: Storage(false) - No backup of text is required 
 * 
 ******************************************************/
public class KMP {
	
	private String pat;
	private int[][] dfa;
	
	public KMP(String pat){
		this.pat = pat; 
		int R = 256,M = pat.length(); 
		dfa = new int[R][M];
		
		dfa[pat.charAt(0)][0]=1;
		for(int X=0,j=1;j<M;j++){
			
			for(int c=0; c<R; c++){
				dfa[c][j]=dfa[c][X];
			}
			dfa[pat.charAt(j)][j] =j+1;
			X = dfa[pat.charAt(j)][X];			
		}		
	}
	
	public int search(String txt){
		int N = txt.length(),M = pat.length();
		int i,j;
		for(j=0, i=0;i<N && j<M; i++){
			j = dfa[txt.charAt(i)][j];
			//StdOut.println("Value of (j,i):"+j+","+i);
		}
		
		if(j==M) return i-M;
		else return N;
	}
	
	public static void main(String args[]){
		int M= 35,N=1000000;
		String pat = new RandomData().generateRandomString(M);
		String txt = new RandomData().generateRandomString(N);
		StdOut.println("Text: "+txt+"\n"+"Pattern: "+pat);
		KMP kmp = new KMP(pat);
		int val = kmp.search(txt);
		if(val<N) StdOut.println(txt.substring(val,val+M));
		else StdOut.println("Match not found !");
	}	

}
