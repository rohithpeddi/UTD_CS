/**
 * 
 */
package StringSorts;

import java.io.File;
import java.util.Scanner;


/*************************

 * @author rohith peddi

 *************************/
public class Quick3string {
	
	private int R = 256;
	private String[] aux;
	private int M=15; //	cut-off for insertion sort
	
	public Quick3string(String[] ar){
		
		
		sort(ar);
				
	}
	
	/***************charAt IMPLEMENTATION*****************/
	
	public int charAt(String s, int d){
		if(d<s.length()) return s.charAt(d);
		else return -1;
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
	
	/***************RECURSIVE SORT IMPLEMENTATION*****************/
	
	public void sort(String[] a){
		int N = a.length; 
		aux = new String[N];
		sort(a,0,N-1,0);
	}
	
	public void sort(String[] a, int lo, int hi, int d){
		
		if(hi<=lo+M){
			insertion_sort(a,lo,hi,d); return;
		}
		
		int lt =lo, gt =hi;
		int v = charAt(a[lo],d);
		int i=lo+1;
		
		while(i<=gt){
			
			int t = charAt(a[i],d);
			if(t<v) exch(a,lt++,i++);
			else if(t>v) exch(a,i,gt--);
			else i++;
		}
		
		sort(a,lo,lt-1,d);
		if(v>=0) sort(a,lt,gt,d+1);
		sort(a,gt+1,hi,d);
		
	}
	
	/***************MAIN IMPLEMENTATION*****************/
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("2000_randstrings.txt"));
			//Quick3string ob = new Quick3string(scan);
			scan.close();
			
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
