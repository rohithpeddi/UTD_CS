import java.lang.reflect.Array;
import java.util.Arrays;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

// 3 way partitioning

public class Ex_2_3_22 {
	
	private static int p=0,q=0;
	
	public static void sort(int[] ar){
		sort(0,ar.length-1,ar);
	}
	
	public static void insertion(int lo, int hi, int[] ar){
		
		for(int i=lo;i<=hi;i++){
			for(int j=i;j>lo && ar[j]<ar[j-1];j--){
				exch(j,j-1,ar);
			}
		}
		
	}
	
	public static void exch(int i,int j, int[] ar ){
		int temp = ar[j];
		ar[j]=ar[i]; ar[i]=temp;
	}
	
	public static void partition_3_way(int lo, int hi, int[] ar){
		
		/* Tukey ninther implementation partitioning */
		
		/*************************************************************/
		if(hi-lo>3){
			int[] part = new int[3];
			int val=0;
			for(int k=0;k<3;k++){
				
					int med=0;
					int[] median = new int[3];
					for(int i=0; i<3;i++){	median[i] = StdRandom.uniform(lo, hi); }
					int[] armedian = {ar[median[0]],ar[median[1]],ar[median[2]]};
					Arrays.sort(armedian); //comp= comp+5;
					for(int i=0; i<3;i++){	if(armedian[1]==ar[median[i]]) {med = median[i]; break;}}
					part[k]=med;
			}
			int[] armedian = {ar[part[0]],ar[part[1]],ar[part[2]]};
			Arrays.sort(armedian); 
			for(int i=0; i<3;i++){	if(armedian[1]==ar[part[i]]) {val = part[i]; break;}}
			exch(lo,val,ar);
		}
		/**************************************************************/
		
		
		int i=lo,j=hi+1;
		p=lo+1;q=hi;
		
		while(true){
			while(ar[++i]<=ar[lo]){
				if(ar[i]==ar[lo]) {	exch(i,p++,ar);}
				if(i==hi) break;
			}
			
			while(ar[lo]<ar[--j]){
				if(ar[j]==ar[lo]) {	exch(j,q--,ar);}
				if(j==lo) break;
			}
			
			if(i>=j) break;
			exch(i,j,ar);			
		}
		for(int a=p-1;a>=lo;a--){exch(j--,a,ar);}
		for(int b=q+1;b<=hi;b++){exch(i++,b,ar);}
		p = j; q = i;
	}
	
	public static void sort(int lo, int hi , int[] ar){
		//for(int x:ar){StdOut.print(x+" ");} StdOut.println("");
		if(lo>=hi) return;
		if(hi-lo>5){
			insertion(lo, hi, ar);
		} else {
			
			partition_3_way(lo,hi,ar);
			sort(lo,p,ar);sort(q,hi,ar);			
		}
	}
	
	public static void init100(){
		int[] ar = new int[100];
		for(int i=0; i<100;i++){ar[i]= StdRandom.uniform(10, 10000);}
		int[] arnew = (int[])Array.newInstance(ar.getClass().getComponentType(), 3*ar.length);
		System.arraycopy(ar, 0, arnew, 0, ar.length);
		System.arraycopy(ar, 0, arnew, ar.length, ar.length);
		System.arraycopy(ar, 0, arnew, 2*ar.length, ar.length);
		for(int x:arnew){StdOut.print(x+" ");} StdOut.println("\n");
		sort(arnew);
		for(int x:arnew){StdOut.print(x+" ");} StdOut.println("");
	}
	
	public static void main(String args[]){
		init100();
	}
	
}
