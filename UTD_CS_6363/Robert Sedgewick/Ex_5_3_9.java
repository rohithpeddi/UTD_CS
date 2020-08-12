/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Boyer Moore for number of occurences of a pattern 
 * in a string and list them all 
 */

public class Ex_5_3_9 {
	
	private String pat;
	private int[] right;
	
	private int count;
	public int[] occ;
	
	public Ex_5_3_9(String pat){
		this.pat = pat;
		int M = pat.length(),R=256;
		right = new int[R];
		
		for(int i=0; i<R; i++)
			right[i]=-1;
		
		for(int i=0; i<M; i++)
			right[pat.charAt(i)]=i;
		
	}
	
	public int searchAll(String txt){
		int M=pat.length(),N = txt.length(),skip=0;
		occ = new int[N/M + M];
		
		for(int i=0; i<=N-M; i+=skip){
			skip=0;
			//StdOut.println("Checking: "+i);
			for(int j=M-1;j>=0;j--){
				if(txt.charAt(i+j)!= pat.charAt(j)){
					//StdOut.println("Checking: "+pat.charAt(j)+"&"+txt.charAt(i+j));
					skip = j-right[pat.charAt(j)];
					if(skip<1) skip=1;	
					break;
				}		
				
				if(skip==0 && j==0) {
					//StdOut.println(count);
					occ[count++] = i; j=M-1;
					skip=1;
				}
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
			StdOut.println("txt:"+txt+"\n"+"pat:"+pat);
			
			Ex_5_3_9 ob = new Ex_5_3_9(pat);		
			num[i]=ob.searchAll(txt);
			if(num[i]!=0) val=val+num[i];
		}
		
		StdOut.println("Matched for a 2 string in 10000 rand string for "+val+ " times.");
	}

}
