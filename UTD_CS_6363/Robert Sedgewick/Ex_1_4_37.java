package AnalysisOfAlgorithms;

import java.util.Scanner;

import edu.princeton.cs.algs4.*;

public class Ex_1_4_37<Item> {
	
	public static int M = 10000000;
	
	public static int[] mints = new int[M];
	
	private Item[] a =(Item[]) new Object[100];
	private static int N=0;
	
	public void push(Item item){
		if(N==a.length){ resize();}
		a[N] = item;
		N++;
	}
	
	public void resize(){
		Item[] anew =(Item[]) new Object[2*a.length];
		for(int i=0;i<N;i++){
			anew[i] = a[i];
		}
		a = anew;
	}
	
	public Ex_1_4_37(){
		int max = 100000,min = -100000;
		for(int i=0;i<M;i++){
			mints[i] = StdRandom.uniform(min, max);
		}
	}
	
	public static class FixedCapacityStackOfInts{
		private int[] a ;
		private int N;
		
		public FixedCapacityStackOfInts(int cap){
			a = new int[cap];
		}
		
		public boolean isEmpty() {return N==0;}
		public int size() { return N;}
		
		public void push(int val){
			a[N++] = val;
		}
		
		public int pop(){
			return a[--N];
		}		
	}
	
	
	
	public static void main(String args[]){
		
		FixedCapacityStackOfInts fcs = new FixedCapacityStackOfInts(M);	
		Ex_1_4_37<Integer> afcs = new Ex_1_4_37<Integer>();
		Stopwatch stw = new Stopwatch();
		
		for(int i=0;i<M;i++){
			fcs.push(mints[i]);
		}
		
		double fcstime = stw.elapsedTime();
		
		for(int i=0;i<M;i++){
			afcs.push(mints[i]);
		}
			
		double afcstime = stw.elapsedTime();
		
		StdOut.println("For Fixed Capacity Stack Of Ints:"+ fcstime+"\nFor Fixed Capacity Stack <Integer>:"+ afcstime);
	}
}
