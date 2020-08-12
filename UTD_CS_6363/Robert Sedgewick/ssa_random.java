import java.awt.Color;
import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

public class ssa_random {
		
	private static double[] ar;
	private static int N=100;
	
	public ssa_random(){
		ar = new double[N];
		for(int i=0;i<N;i++){
			ar[i] = StdRandom.random();
		}
	}
	
	public boolean less(double i , double j){
		return i<j;
	}
	
	public void exch(double[] ar, int i, int p){
		double temp =0;
		temp = ar[i]; ar[i] = ar[p]; ar[p] = temp;
	}
	
	public void sort(double[] ar){
		int M = ar.length;
		
		for(int i=0;i<M;i++){
			int min = i;
			for(int j=i+1;j<M;j++){
				if(less(ar[j],ar[min])) {min = j;}
			}
			animate(i,min);
			exch(ar,i,min);
		}
	}
	
	public void animate(int i,int min){
		for(int j=0;j<N;j++){
			StdOut.println(1.0*j/N+" "+ ar[j]/2.0+" "+ 0.5/N+ " "+ ar[j]/2.0+",   ");
			StdDraw.filledRectangle(1.0*j/N, ar[j]/2.0, 0.5/N, ar[j]/2.0);
			if(j==i) StdDraw.setPenColor(Color.BLUE);
			else if(j==min) StdDraw.setPenColor(Color.red);
			else StdDraw.setPenColor();
		}
		if(i<N-1) StdDraw.clear();
	}
	
	public static void main(String args[]){
		StdOut.print("BEFORE: ");
		ssa_random ssa = new ssa_random();
		for(double x:ar){StdOut.print(x+", ");} StdOut.println("");
		ssa.sort(ar); StdOut.print("AFTER: ");
		for(double x:ar){StdOut.print(x+", ");}
	}
}


