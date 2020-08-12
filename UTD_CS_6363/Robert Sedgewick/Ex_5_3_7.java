/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Brute force algorithm that counts occurences of 
 * the pattern in the given string
 */

public class Ex_5_3_7 {
	
	private String pat;
	private int count;
	private int[] occ;
	
	public Ex_5_3_7(String pat){
		this.pat=pat; this.count=0;
	}
	
	public int searchAll(String txt){
		
		int N=txt.length(),M=pat.length();
		occ = new int[N/M];
		for(int i=0; i<N-M; i++){
			int j=0;
			for(j=0; j<M; j++){
				if(txt.charAt(i+j)!=pat.charAt(j)){
					break;
				}
			}
			
			if(j==M) {occ[count++]=i;}
		}
		
		//for(int i=0; i<count; i++){	StdOut.print(occ[i]+" ");}
		
		
		return count;
	}
	
	public static void main(String args[]){
		
		int[] num = new int[100];
		int val=0;
		for(int i=0; i<100; i++){
			String pat = new RandomData().generateRandomString(10);
			String txt = new RandomData().generateRandomString(10000);
			//StdOut.println("txt:"+txt+"\n"+"pat:"+pat);
			
			Ex_5_3_7 ob = new Ex_5_3_7(pat);		
			num[i]=ob.searchAll(txt);
			if(num[i]!=0) val=val+num[i];
		}
		
		StdOut.println("Matched for a 10 string in 10000 rand string for "+val+ " times.");
	}

}
