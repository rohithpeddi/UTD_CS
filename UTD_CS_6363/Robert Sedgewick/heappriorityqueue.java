import java.io.File;
import java.util.Arrays;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class heappriorityqueue {
	
	private int[] maxpq;
	private int N=0;
	
	public heappriorityqueue(int max){
		maxpq = new int[max+1];
	}
	
	public boolean isEmpty(){
		return N==0;
	}
	
	public int size(){
		return N;
	}
	
	public void insert(int last){
		int val=0;
		if(N<=10){
			maxpq[++N] = last;
			swim(N);
			return;
		}
		
		if(N == maxpq.length-1) {
			val=del_max(last);
		}
		
		if(val>0){
			exch(1,N--);
			sink(1);
			maxpq[++N] = last;
			swim(N);
		}	
		//printVal();
		
	}
	
	public int del_max(int last){
		if(maxpq[1]<last) return -1;
		else return 1;
	}
	
	public int delmax(){
		int max = maxpq[1];
		exch(1,N--);
		sink(1);
		maxpq[N+1] = (Integer) null;
		return max;
	}
	
	public void exch(int i, int j){
		int temp = maxpq[j];
		maxpq[j] = maxpq[i];
		maxpq[i] = temp;
	}
	
	public boolean less(int i, int j){
		return maxpq[i]<maxpq[j];
	}
	
	public void swim(int k){
		while(k>1 && (less(k/2,k))){
			exch(k/2,k);
			k=k/2;
		}
	}
	
	public void sink(int i){
		
		while(2*i<=N){
			int j=2*i;
			if(j<N && less(j,j+1)) j++;
			if(!less(i,j)) break;
			exch(i,j);
			i=j;
		}
	}
	
	public void printVal(){
		Arrays.sort(maxpq);
		for(int x:maxpq){
			StdOut.print(x+" ");
		} StdOut.println("\n");
	}
	
	public int[] init(){
		int[] input = new int[1000];
		Scanner scan =null;
		try{
			scan = new Scanner(new File("1Kints.txt"));
			for(int i=0;i<1000;i++){
				input[i] = scan.nextInt();
			}
		} catch(Exception e){
			StdOut.println("Caught exception: "+ e.getMessage());
		}
		
		
		return input;
	}
	
	public static void main(String args[]){
		heappriorityqueue ob = new heappriorityqueue(11);
		int[] ar = ob.init();
		for(int x:ar){StdOut.print(x+" ");} StdOut.println("\n");
		for(int i=0;i<ar.length;i++){
			ob.insert(ar[i]);
		}
		StdOut.println("Final Answer: \n \n");
		ob.printVal();
		Arrays.sort(ar);
		for(int x:ar){StdOut.print(x+" ");} StdOut.println("\n");
	}

}
