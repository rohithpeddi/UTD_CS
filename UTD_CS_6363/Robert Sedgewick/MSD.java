/**
 * 
 */
package StringSorts;

import java.io.File;
import java.io.PrintWriter;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

/*************************

 * @author rohith peddi

 *************************/
public class MSD {
	
	private int R = 256;
	private String[] aux;
	private int M=15; //	cut-off for insertion sort
	
	/***************GENERATE RANDOM STRINGS OF RANDOM LENGTHS*****************/
	
	public void randString(int N){
		
		String s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		String n = "0123456789";
		
		try{
			
			PrintWriter pw = new PrintWriter(new File("2000_randstrings.txt"));
			
			pw.println(N+"");
			
			for(int i=0; i<N; i++){
				String str="";
				int W = StdRandom.uniform(1, 15);
				for(int j=0; j<W; j++){
					
					if(j==5 || j==6 ||j==2||j==1){
						int num = StdRandom.uniform(0, 9);
						str+= n.charAt(num);
					}
					else{
						int num = StdRandom.uniform(0, 26);
						str+= s.charAt(num);
					}
					
				}
				pw.println(str);
				StdOut.println(str);			
				
			}
			
			pw.flush();
			
		} catch(Exception e){
			e.printStackTrace();
		}
		
		
	}
	
	/***************CONSTRUCTOR*****************/
	
	public MSD(Scanner scan){
		
		int N = Integer.parseInt(scan.nextLine());
		
		String[] a = new String[N];int i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			a[i++]=st;
		}
		
		sort(a);
		
		for(int j=0; j<N; j++){
			StdOut.println(a[j]);
		}
		
		StdOut.println(System.currentTimeMillis());
		
	}
	
	/***************charAt IMPLEMENTATION*****************/
	
	public int charAt(String s, int d){
		if(d<s.length()) return s.charAt(d);
		else return -1;
	}
	
	/***************RECURSIVE SORT IMPLEMENTATION*****************/
	
	public void sort(String[] a){
		int N = a.length; 
		aux = new String[N];
		sort(a,0,N-1,0);
	}
	
	//If the string ends, function returns -1 so to maintain invariant we are adding +2 
	
	private void sort(String[] a, int lo, int hi, int d){
		
		if(hi<=lo+M){
			insertion_sort(a,lo,hi,d); return;
		}
		
		int[] count = new int[R+2]; 
		
		for(int i=lo; i<=hi; i++){
			count[charAt(a[i],d)+2]++;
		}
		
		for(int r=0; r<R; r++){
			count[r+1]+=count[r];
		}
		
		for(int i=lo; i<=hi; i++){
			aux[count[charAt(a[i],d)+1]++] = a[i];
		}
		
		for(int i=lo; i<=hi; i++){
			a[i] = aux[i-lo];
		}
		
		for(int r=0; r<R; r++){
			sort(a,lo+count[r],lo+count[r+1]-1,d+1);
		}
		
	}
	
	/***************INSERTION SORT IMPLEMENTATION*****************/
	
	public void insertion_sort(String[] a, int lo, int hi, int d){
		
		for(int i=0; i<=hi; i++){
			for(int j=i; j>lo && less(a[j],a[j-1],d); j--){
				exch(a,j,j-1);
			}
		}
		
	}
	
	public void exch(String[] a, int i, int j){
		String temp = a[i]; a[i] = a[j]; a[j]= temp;
	}
	
	public boolean less(String v, String u, int d){
		return v.substring(d).compareTo(u.substring(d))<0;
	}
	
	/***************MAIN IMPLEMENTATION*****************/
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("2000_randstrings.txt"));
			MSD ob = new MSD(scan);
			scan.close();
			
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
