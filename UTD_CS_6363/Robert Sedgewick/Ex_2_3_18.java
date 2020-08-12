import java.util.Arrays;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

public class Ex_2_3_18 {
	
	private static int comp=0;
	
	public static void sort(int[] ar ){
		//StdRandom.shuffle(ar);
		sort(0,ar.length-1,ar);
	}
	
	public static int partition(int lo, int hi, int[] ar){
		
		if(hi-lo>3){
			int med=0;
			int[] median = new int[3];
			for(int i=0; i<3;i++){	median[i] = StdRandom.uniform(lo, hi); }
			int[] armedian = {ar[median[0]],ar[median[1]],ar[median[2]]};
			Arrays.sort(armedian); //comp= comp+5;
			for(int i=0; i<3;i++){	if(armedian[1]==ar[median[i]]) {med = median[i];++comp; break;}}
			exch(lo,med,ar);
		} 
		
		int i=lo,j=hi+1;
		while(true){
			while(ar[++i]<ar[lo]) {++comp;if(i==hi) break;}
			while(ar[lo]<ar[--j]) {++comp;}
			if(i>=j) break;
			exch(i,j,ar);
		}
		exch(lo,j,ar);
		return j;
	}
	
	public static void exch(int i, int j, int[] ar){
		int temp = ar[i];
		ar[i] = ar[j]; ar[j]=temp;
	}
	
	public static void sort(int lo, int hi, int[] ar){
		if(lo>=hi) return;
		int r = partition(lo,hi,ar);
		sort(lo,r-1,ar);sort(r+1,hi,ar);
	}
	
	
	/* ..........................................................*/
	
	
	public static void sort5(int[] ar ){
		//StdRandom.shuffle(ar);
		sort(0,ar.length-1,ar);
		
	}
	
	public static int partition5(int lo, int hi, int[] ar){
		StdOut.println("Entered");
		if(hi-lo>10){
			StdOut.println("Entered");
			int med=0;
			int[] median = new int[5];
			for(int i=0; i<5;i++){	median[i] = StdRandom.uniform(lo, hi); }
			int[] armedian = {ar[median[0]],ar[median[1]],ar[median[2]],ar[median[3]],ar[median[4]]};
			Arrays.sort(armedian); comp= comp+7;
			for(int i=0; i<3;i++){	if(armedian[2]==ar[median[i]]) {med = median[i];++comp; break;}}
			exch(lo,med,ar);
			StdOut.println(med+" ");
		} 
		
		int i=lo,j=hi+1;
		while(true){
			while(ar[++i]<ar[lo]) {++comp;if(i==hi) break;}
			while(ar[lo]<ar[--j]) {++comp;}
			if(i>=j) break;
			exch(i,j,ar);
		}
		exch(lo,j,ar);
		return j;
	}
	
	public static void sort5(int lo, int hi, int[] ar){
		if(lo>=hi) return;
		StdOut.println("Entered");
		int r = partition5(lo,hi,ar);
		sort5(lo,r-1,ar);sort5(r+1,hi,ar);
	}
	
	
	
	/* ..........................................................*/
	
	public static void sortor(int[] ar ){
		sort(0,ar.length-1,ar);
	}
	
	public static int partitionor(int lo, int hi, int[] ar){
		
		StdRandom.shuffle(ar);
		
		int i=lo,j=hi+1;
		while(true){
			while(ar[++i]<ar[lo]) {++comp;if(i==hi) break;}
			while(ar[lo]<ar[--j]) {++comp;}
			if(i>=j) break;
			exch(i,j,ar);
		}
		exch(lo,j,ar);
		return j;
	}
	
	public static void sortor(int lo, int hi, int[] ar){
		if(lo>=hi) return;
		int r = partitionor(lo,hi,ar);
		sortor(lo,r-1,ar);sortor(r+1,hi,ar);
	}
	
	/*....................................................*/
	
	
	public static void init100(){
		int[] ar = new int[100];int[] ar1 = new int[100];int[] ar2 = new int[100];
		comp =0;
		for(int i=0; i<100;i++){ar[i]= StdRandom.uniform(10, 10000);}
		System.arraycopy(ar, 0, ar1, 0, ar.length);
		System.arraycopy(ar, 0, ar2, 0, ar.length);
		//for(int x:ar){StdOut.print(x+" ");} StdOut.println("");
		sort(ar);
		//for(int x:ar){StdOut.print(x+" ");} StdOut.println("");
		StdOut.println("Comparisons in 3 median:"+comp+", Expected value:"+2.78*100/Math.log10(2));
		comp=0;
		sortor(ar1);
		StdOut.println("Comparisons in randomised:"+comp+", Expected value:"+2.78*100/Math.log10(2));
		comp=0;
		sort5(ar2);
		StdOut.println("Comparisons in 5-median:"+comp+", Expected value:"+2.78*100/Math.log10(2));
	}
	
	public static void init1000(){
		int[] ar = new int[1000];int[] ar1 = new int[1000];int[] ar2 = new int[1000];
		for(int i=0; i<1000;i++){ar[i]= StdRandom.uniform(10, 10000);}
		System.arraycopy(ar, 0, ar1, 0, ar.length);
		System.arraycopy(ar, 0, ar2, 0, ar.length);
		//for(int x:ar){StdOut.print(x+" ");} StdOut.println("");
		sort(ar);
		//for(int x:ar){StdOut.print(x+" ");} StdOut.println("");
		StdOut.println("Comparisons in 3-median:"+comp+", Expected value:"+2.78*1000/Math.log10(2));
		comp=0;
		sortor(ar1);
		StdOut.println("Comparisons in randomised:"+comp+", Expected value:"+2.78*1000/Math.log10(2));
		comp=0;
		sort5(ar2);
		StdOut.println("Comparisons in 5-median:"+comp+", Expected value:"+2.78*1000/Math.log10(2));
	}
	
	public static void init10000(){
		int[] ar = new int[10000];int[] ar1 = new int[10000];int[] ar2 = new int[10000];
		for(int i=0; i<10000;i++){ar[i]= StdRandom.uniform(10, 10000);}
		System.arraycopy(ar, 0, ar1, 0, ar.length);
		System.arraycopy(ar, 0, ar2, 0, ar.length);
		//for(int x:ar){StdOut.print(x+" ");} StdOut.println("");
		sort(ar);
		//for(int x:ar){StdOut.print(x+" ");} StdOut.println("");
		StdOut.println("Comparisons in 3-median:"+comp+", Expected value:"+2.78*10000/Math.log10(2));
		comp=0;
		sortor(ar1);
		StdOut.println("Comparisons in randomised:"+comp+", Expected value:"+2.78*10000/Math.log10(2));
		comp=0;
		sort5(ar2);
		StdOut.println("Comparisons in 5-median:"+comp+", Expected value:"+2.78*10000/Math.log10(2));
	}
	
	
	public static void init(){
		init100();
		//init1000();
		//init10000();
	}
	
	public static void main(String args[]){
		init();
	}

}
