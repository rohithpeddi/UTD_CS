import java.io.File;
import java.io.PrintWriter;
import java.util.Scanner;

import edu.princeton.cs.algs4.*;

public class shellvsinsertion {
	private static int[] n1 = new int[1000];
	private static int[] n2 = new int[1000];
	
	static int shellcomp=0,incomp=0,shellex=0,inex=0;
	
	public shellvsinsertion(){
		int i=0;
		Scanner scan = null;
		try{
			scan = new Scanner(new File("1Kints.txt"));
			while(i<1000){
				int n = scan.nextInt();
				n1[i] = n; n2[i++] = n;
			}
		} catch(Exception e){
			StdOut.println(e.getMessage());
		}
	}
	
	public static int sless(int i,int j, int[] ar){
		shellcomp++;
		if(ar[i]<ar[j]) return 1;
		else if(ar[i]>ar[j]) return -1;
		else return 0;
	}
	
	public static int iless(int i,int j, int[] ar){
		incomp++;
		if(ar[i]<ar[j]) return 1;
		else if(ar[i]>ar[j]) return -1;
		else return 0;
	}
	
	public static void sexch(int i, int j, int[] ar){
		shellex++;
		int temp = ar[i];
		ar[i]= ar[j];
		ar[j] = temp;
	}
	
	public static void iexch(int i, int j, int[] ar){
		inex++;
		int temp = ar[i];
		ar[i]= ar[j];
		ar[j] = temp;
	}
	
	public static void shellsort(int[] ar){
		int h = 1;
		while(h< ar.length/3) h = 3*h +1;
		while(h>=1){
			for(int i=h; i<ar.length;i++){
				for(int j=i;j>=h && (sless(j,j-h,ar)>0);j=j-h){
					sexch(j,j-h,ar);
				}
			}
			h = h/3;
		}
	}
	
	public static void insertionsort(int ar[]){
		for(int i=1;i<ar.length;i++){
			for(int j=i;j>0 && (iless(j,j-1,ar)>0);j--){
				iexch(j,j-1,ar);
			}
		}
	}
	
	public static void main(String args[]){
		shellvsinsertion ob = new shellvsinsertion();
		PrintWriter pw = null;
		Scanner sc =null;
		try{
			//pw = new PrintWriter(new File("1Kints-sorted.txt"),"UTF-8");
			//for(int i:n1){StdOut.print(i+" ");pw.println(i);}
			int[] a = new int[1000];
			sc = new Scanner(new File("1Kints-sorted.txt"));
			int i=0;
			while(i<1000){
				a[i++] = sc.nextInt();
			}
			shellsort(a); insertionsort(a);
		} catch(Exception e){
			StdOut.print(e.getMessage());
		} finally{
			//pw.close();
			sc.close();
		}
		
		//for(int i:n2){StdOut.print(i+" ");}
		
		StdOut.println("Shell sort:" +shellcomp+ "-compares,"+ shellex +"-exchanges" );
		StdOut.println(" ");
		StdOut.println("Insertion sort:" + incomp+ "-compares,"+ inex +"-exchanges" );
	}
	
}
