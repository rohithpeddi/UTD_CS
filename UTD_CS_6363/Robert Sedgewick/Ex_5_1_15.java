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

/****************************************************
 * SUBLINEAR SORT 
 * 
 * go for a LSD sort for first 16 bits then go for a 
 * insertion sort after wards
 ***************************************************/

public class Ex_5_1_15 {
	
	public void genRandInts(){
		try{
			PrintWriter pw = new PrintWriter(new File("10000posints.txt"));
			pw.println("10000");
			
			int i=0;
			while(i<10000){
				int num = StdRandom.uniform(1, 100000);
				pw.println(num+""); 
				i++;
			}
			
			pw.close();
			
		} catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public Ex_5_1_15(Scanner scan){
		
		int N = Integer.parseInt(scan.nextLine());
		
		String[] a = new String[N];int i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			StdOut.println(st);
			a[i++]=st;
		}
		
		sort(a,5);
		
		int j=0;
		while(j<N){			
			StdOut.println(a[j++]);
		}
		
	}
	
	private int charAt(String st, int d){
		if(d<st.length()) return st.charAt(d);
		else return -1;
	}
	
	public void sort(String[] a, int W){
		
		int N = a.length,R=256;
		String[] aux = new String[N];
		
		for(int d=W-1; d>=0; d--){
			
			int[] count = new int[R+2];
			
			for(int i=0; i<N; i++){
				count[charAt(a[i],d)+2]++;
			}
			
			for(int r=0;r<R; r++ ){
				count[r+1]+=count[r];
			}
			
			for(int i=0;i<N; i++){
				aux[count[charAt(a[i],d)+1]++] = a[i];
			}
			
			for(int i=0; i<N; i++){
				a[i]=aux[i];
			}
		}
		
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("10000posints.txt"));
			Ex_5_1_15 ob = new Ex_5_1_15(scan);
			ob.genRandInts();
			scan.close();
			
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
