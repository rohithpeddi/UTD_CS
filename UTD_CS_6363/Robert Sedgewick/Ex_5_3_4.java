/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

//Boyer Moore for M consecutive blanks search 

public class Ex_5_3_4 {
	
	private String pat;
	private int[] right;
	
	public Ex_5_3_4(String pat){
		this.pat = pat;
		int M = pat.length(),R=256;
		right = new int[R];
		
		for(int i=0; i<R; i++)
			right[i]=-1;
		
		for(int i=0; i<M; i++)
			right[pat.charAt(i)]=i;
		
	}
	
	public int search(String txt){
		int M=pat.length(),N = txt.length(),skip=0;
		
		for(int i=0; i<N-M; i+=skip){
			skip=0;
			//StdOut.println("Checking: "+i);
			for(int j=M-1;j>=0;j--){
				if(txt.charAt(i+j)!= pat.charAt(j) && pat.charAt(j)!='.'){
					StdOut.println("Checking: "+pat.charAt(j)+"&"+txt.charAt(i+j));
					skip = j-right[pat.charAt(j)];
					if(skip<1) skip=1;	
					break;
				}							
			}
			
			if(skip==0) return i-M;
		}
		
		return N;
	}
	
	public static void main(String args[]){
		String txt = new RandomData().generateRandomString(10000);
		String pat = " . ";
		StdOut.println("Text: "+txt+"\n"+"Pattern: "+pat);
		Ex_5_3_4 bm = new Ex_5_3_4(pat);
		int val = bm.search(txt);
		if(val<100) StdOut.println("Found at: "+ val+": "+txt.substring(val,val+3));
		else StdOut.println("Match not found !");
	}

}
