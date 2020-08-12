/**
 * 
 */
package StringSorts;

import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.Queue;
import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*********************************************
 * QUEUE SORT
 * 
 * Instead of count array use a queue array of same
 * size and same kind of implementation
 * 
 ********************************************/

public class Ex_5_1_11 {	
	
	private int R = 256;
	private String[] aux;
	private int M=15;
	
	
	public Ex_5_1_11(Scanner scan){
		
		int N = Integer.parseInt(scan.nextLine());
		
		String[] a = new String[N];int i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			a[i++]=st;
		}
		
		sort(a);
		
		//for(int j=0; j<N; j++){			StdOut.println(a[j]);		}
		
		StdOut.println(System.currentTimeMillis());
		
	}
	
	/***************charAt IMPLEMENTATION*****************/
	
	public int charAt(String s, int d){
		if(d<s.length()) return s.charAt(d);
		else return -1;
	}
	
	/***************RECURSIVE SORT IMPLEMENTATION*****************/
	
	public void sort(String[] a){
		int N = a.length; 
		aux = new String[N];
		Queue<String> queue = new Queue<String>();
		for(int i=0; i<N; i++){
			queue.enqueue(a[i]);
		}
		
		queue = sort(queue,N,0);
		//StdOut.println(queue.size());
		while(!queue.isEmpty()){			
			StdOut.println(queue.dequeue());
		}
	}
	
	//If the string ends, function returns -1 so to maintain invariant we are adding +2 
	
	private Queue<String> sort(Queue<String> queue,int size,int d){
		
		//StdOut.println("Entered:"+queue.size());
		
		if(size<=M){ queue = insertion_sort(queue,d); return queue;}
		
		Queue<String>[] q = new Queue[R+2];
		
		for(int r=0; r<R+2; r++){
			q[r] = new Queue<String>();
		}
				
		while(!queue.isEmpty()){
			String str = queue.dequeue();			
			q[charAt(str,d)+2].enqueue(str);
		}
		
		//Recursively sort non empty queues and stitch all queues together
		
		for(int r=2; r<R+2; r++){		
			
			if(!q[r].isEmpty()){
				
				q[r] = sort(q[r],q[r].size(),d+1); 
				
			}
		}
		
		Queue<String> qf = new Queue<String>();
		for(int r=1; r<R+2;r++){
			
			if(!q[r].isEmpty()){
				//StdOut.println("Stitching:"+q[r].size());
				while(!q[r].isEmpty()){
					qf.enqueue(q[r].dequeue());
				}
			}
			
			//StdOut.println("qf size variation:"+q[r].size());
		}
		
		return qf;
		
	}
	
	/***************INSERTION SORT IMPLEMENTATION*****************/
	
	public Queue<String> insertion_sort(Queue<String> queue, int d){
		
		int N = queue.size();
		String[] ar = new String[N];
		for(int i=0; i<N; i++){
			ar[i] = queue.dequeue();
		}
		
		for(int i=1; i<N; i++){
			for(int j=i; j>0 && less(ar[j],ar[j-1],d); j--){
				exch(ar,j,j-1);
			}
		}
		
		Queue<String> q = new Queue<String>();
		for(int i=0; i<N; i++){
			q.enqueue(ar[i]);
		}
		
		return q;
		
	}
	
	public void exch(String[] a, int i, int j){
		String temp = a[i]; a[i] = a[j]; a[j]= temp;
	}
	
	public boolean less(String v, String u, int d){
		return v.substring(d).compareTo(u.substring(d))<0;
	}
	
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("2000_randstrings.txt"));
			Ex_5_1_11 ob = new Ex_5_1_11(scan);
			scan.close();
			
		} catch(Exception e){
			e.printStackTrace();
		}
	}
	
	

}
