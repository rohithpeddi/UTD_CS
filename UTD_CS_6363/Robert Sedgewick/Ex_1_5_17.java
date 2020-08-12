import java.io.*;
import java.util.*;

import edu.princeton.cs.algs4.*;

public class Ex_1_5_17 {
	
	private static int N=0;
	private static int[][] ar;
	
	public static void main(String args[]){
		Scanner scan = null;
		try{
			scan = new Scanner(new File("tinyUF.txt"));
		} catch(Exception e){
			StdOut.println("File not found");
		}
		
		N = scan.nextInt();
		//StdOut.print(N);
		for(int i=0;i<N;i++){
			for(int j=0;j<N;j++){
				StdDraw.point((double)i/10, (double)j/10);
				//StdOut.println((double)i/10+":"+(double)j/10+",");
				StdDraw.setPenRadius(.005);
			}
		}
		ar = new int[N][2];
		int p=0;
		while(p<10){
			ar[p][0] = scan.nextInt();
			ar[p][1] = scan.nextInt();			
			StdDraw.line((double)ar[p][0]/10, 0, (double)ar[p][1]/10, (double)p/10);
			StdOut.print(ar[p][0]+": "+ ar[p][1]+",");
			p++;
		}
		
	}
	
}
