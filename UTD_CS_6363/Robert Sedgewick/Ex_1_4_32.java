package AnalysisOfAlgorithms;

import java.io.*;
import java.util.*;

import edu.princeton.cs.algs4.*;

public class Ex_1_4_32<Item> {
	
	public static int N =0;
	public static int[] a =  new int[100];
	public static double[] timedet = new double[4];
	
	public static void push(int val){
		if(N == a.length){ resize();}
		a[N] = val;
		N++;
	}
	
	public static void resize(){
		int[] ares = new int[2*a.length];
		for(int i=0;i<a.length;i++){
			ares[i] = a[i];
		}		
		a = ares;
	}
	
	public static void main(String args[]){
		Scanner scan =null;
		Stopwatch stw = new Stopwatch();
		for(int j=0;j<1000;j++){
			for(int i=0;i<4;i++){
					try{
						if(i==0) scan = new Scanner(new File("1Kints.txt"));
						if(i==1) scan =  new Scanner(new File("2Kints.txt"));
						if(i==2) scan = new Scanner(new File("4Kints.txt"));
						if(i==3) scan =  new Scanner(new File("8Kints.txt"));
					} catch(Exception e){
						StdOut.println("File not found!");					
					}
				Ex_1_4_32<Integer> st = new Ex_1_4_32<Integer>();
				while(scan.hasNextInt()){
					st.push(scan.nextInt());
				}
				timedet[i] += stw.elapsedTime();	
			}
		}
		for(int i=0;i<4;i++){
			StdOut.println("The file considered: "+Math.pow(2, i)*1000+" integers, Elapsed time: "+ timedet[i]);
			double x = Math.log(Math.pow(2, i)*1000);
			double y = Math.log(timedet[i]/1000);
			StdOut.println("x: "+x+"y: "+y);
			StdDraw.point(x/10, y/10);
			StdDraw.setPenRadius(.009);
		}
		
	}
	
}
