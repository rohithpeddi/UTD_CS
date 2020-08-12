import java.awt.Color;

import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

public class isa_random {
	private static double[] ar;
	private static int N=300;
	
	public isa_random(){
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
			int j=0;
			for(j=i;j>0 && less(ar[j],ar[j-1]);j--){
				exch(ar,j,j-1);
			}	
			animate(i,j);
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
		if(i<N-1) {StdDraw.clear();}
	}
	
	public static void main(String args[]){
		StdOut.print("BEFORE: ");
		isa_random isa = new isa_random();
		for(double x:ar){StdOut.print(x+", ");} StdOut.println("");
		isa.sort(ar); StdOut.print("AFTER: ");
		for(double x:ar){StdOut.print(x+", ");}
	}
}
