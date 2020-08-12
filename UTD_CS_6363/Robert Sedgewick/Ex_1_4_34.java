package AnalysisOfAlgorithms;

import edu.princeton.cs.algs4.*;

public class Ex_1_4_34 {
	
	public static int max = 0,collector =0,prev = 0, current=0;
	
	public static void printst(){
		StdOut.println("Enter 0 if the answer is right\nEnter 1 if it is father from previous\nEnter -1 if it is closer than previous\nEnter 2 if it is equidistant from both");
	}
	
	public static int check(int val){
		StdOut.println("Is your chosen value:"+ val);
		//printst();
		int send = StdIn.readInt();
		return send;
	}
	
	public static void main(String args[]){
		Stopwatch stw = new Stopwatch();
		int i=0;int lo =0; 
		StdOut.println("Enter the max value in range");
		max = StdIn.readInt();
		int hi = max;
		while(true){	
			int mid = lo+ (hi-lo)/2;
			StdOut.println("lo: "+lo+", hi: "+hi+", mid:"+mid);
			if(i==0) {				
				prev = max;
				if(check(max)==0) { StdOut.println("Chosen number is"+ prev);break;}
			}
			current = mid; int j = check(mid);
			if(j==0) { StdOut.println("Chosen number is"+ current);break;}
			else if(j==1) {lo = current+ ((prev-current)/2);}
			else if(j==-1){hi = current+((hi-current)/2);}
			else if(j== 2){StdOut.println("Choosen number is"+ (current+prev)/2);break;}
			prev = current;
			i++;
		}
	}
}
