import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

public class quicksort {
	
	public static int partition(int lo, int hi,Comparable[] ar){
		int i=lo, j=hi+1;
		while(true){
			
			while(less(ar[++i],ar[lo])<=0){
				if(i==hi) break;				
			}
			while(less(ar[--j],ar[lo])>=0){
				if(j==lo) break;				
			}
			
			if(i>=j) break;
			exch(i,j,ar);
			
		}
		exch(lo,j,ar);
		return j;
		
	}
	
	public static void sort(Comparable[] ar){
		StackTraceElement[] stacktrace = Thread.currentThread().getStackTrace();
		String method = stacktrace[0].getMethodName();
		if(method.equalsIgnoreCase("init")) StdRandom.shuffle(ar);
		
		
		sort(0,ar.length-1,ar);		
	}
	
	public static int less(Comparable a, Comparable b){
		if(a.compareTo(b)<0) return -1;
		else if(a.compareTo(b)==0) return 0;
		else return 1;
	}
	
	public static void sort(int lo, int hi, Comparable[] ar){
		for(Comparable x:ar){StdOut.print(x+" ");} StdOut.println("");
		if(lo>=hi) return;
		int r = partition(lo,hi,ar);StdOut.println("Partition:"+ r);
		sort(lo,r-1,ar);sort(r+1,hi,ar);		
	}
	
	public static void exch(int i, int j, Comparable[] ar){
		Comparable temp;
		temp = ar[i];
		ar[i] = ar[j];
		ar[j] = temp;
		//StdOut.print(",("+i+":"+j+")");StdOut.println("");
	}
	
	public static void init(Comparable[] a){
		Scanner scan = null;
		try{
			scan = new Scanner(new File("20ints.txt"));
			int i=0;
			while(i<20){
				a[i++] = scan.nextInt();
			}
		} catch(Exception e){
			StdOut.println("File not found!");
		}
		
		for(Comparable x:a){StdOut.print(x+" ");} StdOut.println("\n\n");
		sort(a);
		for(Comparable x:a){StdOut.print(x+" ");} StdOut.println("");
	}
	
	public static void inittrace(){
		String delims = " ";
		String val = "E A S Y Q U E S T I O N";
		String[] str = val.split(delims);
		for(Comparable x:str){StdOut.print(x+" ");} StdOut.println("\n\n");
		sort(str);
		for(Comparable x:str){StdOut.print(x+" ");} StdOut.println("");
	}
	
	public static void main(String args[]){
		//Integer[] a = new Integer[20];
		inittrace();		
	}
	
}
