/**
 * 
 */
package StringSorts;

import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*****************************************
 * LINKED LIST SORT -  3 WAY STRING QUICK SORT
 * 
 * 
 * 
 ****************************************/

public class Ex_5_1_16 {
	
	private Node first=null,last=null;
	
	/***************NODE IMPLEMENTATION*****************/
	
	private class Node{
		String data;
		Node prev,next;
		
		public Node(String data){
			this.data = data;
		}
	}
	
	/***************TAKE RANDOM INPUT AND CREATE A LIST*****************/
	
	public Ex_5_1_16(Scanner scan){
		
		int N = Integer.parseInt(scan.nextLine());
		Node current = null;
		while(scan.hasNextLine()){
			if(first == null) {first = new Node(scan.nextLine());last=first;current=first;continue;}
			String str = scan.nextLine();
			Node newlast = new Node(str);
			current.next = newlast; 
			last = newlast;
			newlast.prev = current;		
			current = current.next;
		}
		
		//checking whether input is taken or not 
		/*
		Node naive = first;
		while(naive!=null){
			StdOut.println(naive.data);
			naive = naive.next;
		}
		*/
		//sending the first and last references to the sort method
		
		sort(first,last,0);	
		
		//printing all values after sorting
		StdOut.println("----------------------------------");
		Node naive1 = first;
		while(naive1!=null){
			StdOut.println(naive1.data);
			naive1 = naive1.next;
		}
	}
	
	public int charAt(String st, int d){
		if(d<st.length()) return st.charAt(d);
		else return -1;
	}
	
	public void sort(Node lo, Node hi,int d){
		
		if((lo==null || hi==null)) return;		
		Node fcurrent = lo,lcurrent = hi;		
		if(fcurrent == lcurrent || lcurrent.next == fcurrent ) {return;} 
		
		//Printing the set of values from lo to hi
		StdOut.println("Sorting between:"+ d+"--->");		
		for(Node i=lo; i!=hi; i = i.next){
			StdOut.print(i.data+" ");
			if(i.next==hi) StdOut.print(i.data+" ");
		}		
		StdOut.println("");
		
		//Algorithm starts 
		
		//If lo==hi then there is only one value so return that value and terminate rec loop
		
		Node current = fcurrent.next;
		String partition = lo.data;
		int comp = charAt(partition,d);
		StdOut.println("current is on: "+ current.data+", Partition:"+partition+ ", comp:"+comp);
		if(comp<0) return;
		
		while(current!=null){
			String st = current.data;
			if(charAt(st,d)<comp) { exch(current,fcurrent);fcurrent = fcurrent.next;current = current.next;}
			else if(charAt(st,d)>comp) {exch(current,lcurrent); lcurrent = lcurrent.prev;}
			else {current = current.next;}	
			if( current == lcurrent.next) break;
		}
		
		StdOut.println("\n");
		
		sort(lo,fcurrent.prev,d);
		
		if(lcurrent.next != fcurrent) {
			StdOut.println("Sorting equal case");
			sort(fcurrent,lcurrent,d+1);
		}
		
		StdOut.println("lcurrent is on:"+lcurrent.data);
		sort(lcurrent.next,hi,d);		
	}
	
	public void exch(Node n1, Node n2){
		StdOut.println("Exchanging:"+n1.data+","+ n2.data);
		String temp = n1.data; n1.data = n2.data; n2.data = temp;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner (new File("2000_randstrings.txt"));
			Ex_5_1_16 ob = new Ex_5_1_16(scan);
		} catch(Exception e){
			e.printStackTrace();
		}
	}
	
	

}
