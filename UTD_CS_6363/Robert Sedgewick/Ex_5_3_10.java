/**
 * 
 */
package SubstringSearch;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Rabin Karp implementation of all the occurences of the pattern
 * in the given string txt 
 */

public class Ex_5_3_10 {
	
	private String pat;
	private long Q,RM,patHash;
	private int M,R=256;
	
	private int count=0;
	private int[] occ;
	
	public Ex_5_3_10(String pat){
		this.pat=pat; M= pat.length();
		
		RM=1;Q=997;
		for(int i=0; i<R; i++){
			RM = (R*RM) %Q; 
		}
		
		patHash = hash(pat,M);
	}
	
	public long hash(String key, int M){
		long h=0;
		for(int i=0; i<M; i++){
			h = (R*h+ key.charAt(i)) %Q;
		}
		return h;
	}
	
	public int searchAll(String txt){
		int N= txt.length();
		occ = new int[N/M];
		long txtHash= hash(txt,M);
		if(txtHash == patHash) occ[count++]=0;
		
		for(int i=M; i<N-M; i++){
			
			txtHash = (txtHash+Q - RM*txt.charAt(i-M)%Q)%Q;
			txtHash = (txtHash*R + txt.charAt(i))%Q ; 
			
			if(txtHash == patHash) occ[count++]=i;
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
			
			Ex_5_3_10 ob = new Ex_5_3_10(pat);		
			num[i]=ob.searchAll(txt);
			if(num[i]!=0) val=val+num[i];
		}
		
		StdOut.println("Matched for a 2 string in 1000 rand string for "+val+ " times.");
	}

}
