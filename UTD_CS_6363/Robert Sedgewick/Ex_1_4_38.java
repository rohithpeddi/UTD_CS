package AnalysisOfAlgorithms;

import edu.princeton.cs.algs4.*;

public class Ex_1_4_38 {
	
	public static int M = 1000;
	
	public static int[] mints = new int[M];
	private Stopwatch stw;
	
	public Ex_1_4_38(){
		int max = 100000,min = -100000;
		for(int i=0;i<M;i++){
			mints[i] = StdRandom.uniform(min, max);
		}
		stw = new Stopwatch();
	}
	
	public double ThreeSum(){
		int count =0;
		for(int i=0;i<M;i++){
			for(int j=i+1;j<M;j++){
				for(int k=j+1;k<M;k++){
					if(mints[i]+mints[j]+mints[k]==0) ++count;
				}
			}
		}
		StdOut.println("Count:"+ count);
		double time = stw.elapsedTime();
		return time;
	}
	
	public double NaiveThreeSum(){
		int count =0;
		for(int i=0;i<M;i++){
			for(int j=0;j<M;j++){
				for(int k=0;k<M;k++){
					if(i<j && j<k){if(mints[i]+mints[j]+mints[k]==0) ++count;}
				}
			}
		}
		StdOut.println("Count:"+ count);
		double time = stw.elapsedTime();
		return time;
	}
	
	public static void main(String args[]){
		Ex_1_4_38 ob = new Ex_1_4_38();
		double three_sum_time = ob.ThreeSum();
		double naive_three_sum_time = ob.NaiveThreeSum();
		StdOut.println("ThreeSum: "+three_sum_time+"\nNaiveThreeSum: "+naive_three_sum_time);
	}
}
