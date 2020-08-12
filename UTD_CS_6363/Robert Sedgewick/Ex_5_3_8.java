/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * KMP version which shows all the occurences of the pattern 
 * int the search text.
 */

public class Ex_5_3_8 {
	
	private String pat;
	private int[][] dfa;
	
	private int count;
	private int[] occ;
	
	public Ex_5_3_8(String pat){
		int R=256,M=pat.length();
		this.pat =pat; dfa = new int[R][M]; this.count=0;
		
		dfa[pat.charAt(0)][0]=1;
		for(int X=0,j=0; j<M; j++){
			
			for(int i=0; i<R; i++){
				dfa[i][j] = dfa[i][X];
			}
			
			dfa[pat.charAt(j)][j] = j+1;
			X = dfa[pat.charAt(j)][X];
		}
	}
	
	public int searchAll(String txt){
		int N=txt.length(),M=pat.length();
		occ = new int[N/M];
		int i,j,c=1;
		for(i=0,j=0; i<N-M && j<M; i+=c){
			c=1;
			j = dfa[txt.charAt(i)][j];
			
			if(j==M) {				
				//StdOut.println("Entered: "+ i);
				occ[count++]=i-M;
				c = -M+2; 
				//StdOut.println("Entered: "+ c);
				if(c==0) c=1;
				j=0;
			}
		}
		
		return count;
	}
	
	public static void main(String args[]){
		int[] num = new int[100];
		int val=0;
		for(int i=0; i<num.length; i++){
			String pat = new RandomData().generateRandomString(2);
			String txt = new RandomData().generateRandomString(1000);
			//StdOut.println("txt:"+txt+"\n"+"pat:"+pat);
			
			Ex_5_3_8 ob = new Ex_5_3_8(pat);		
			num[i]=ob.searchAll(txt);
			if(num[i]!=0) val=val+num[i];
		}
		
		StdOut.println("Matched for a 10 string in 10000 rand string for "+val+ " times.");
	}

}
