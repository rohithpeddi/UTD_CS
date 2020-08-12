import java.util.Arrays;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

/**************************************
 * PERFECT BALANCE TREE GENERATOR
 **************************************/

public class Ex_3_2_25<Key extends Comparable<Key>,Value> {
	
	private Node root;
	public Key[] keys_main,keys_sorted;
	private int count =0;
	
	private class Node{
		Key key; Value val;
		Node left,right;
		Node(Key k, Value v){
			this.key = k; this.val= v;
		}
	}
	
	public void put(Key k, Value v){
		Node current = root; if(current == null){root = new Node(k,v);return;}
		Node prev = current;int ind =3;
		while(current != null){
			prev = current;
			int cmp = k.compareTo(current.key);
			if(cmp<0){current = current.left; ind=0;}
			else if(cmp>0){current = current.right; ind =1;}
			else {
				current.val = v;
			}
		}
		if(ind == 0){prev.left = new Node(k,v);return;}
		else{prev.right = new Node(k,v);return;}
	}
	
	public void arrange(Key[] keys){
		Key[] order = (Key[]) new Comparable[keys.length];
		Arrays.sort(keys);
		keys_main = keys;
		for(Key x: keys_main){StdOut.print(x+" ");}StdOut.println(" \n ");
		
		keys_sorted = order;
		int lo =0,hi = keys.length-1;
		arrangeR(lo,hi);
		
		for(Key x: keys_sorted){StdOut.print(x+" ");}StdOut.println(" \n ");
		
		for(int i=0; i<keys_sorted.length;i++){
			put(keys_sorted[i],null); printOrder();StdOut.println(" \n ");
		}
		
		return;
	}
	
	private void arrangeR(int lo, int hi){
		int mid = lo + (hi-lo)/2 ; 
		if(lo==hi){keys_sorted[count++] = keys_main[mid]; return;}
		if(lo<hi){
			if(hi-lo ==1) {keys_sorted[count++] = keys_main[lo];keys_sorted[count++] = keys_main[hi]; return;}
			keys_sorted[count++] = keys_main[mid]; arrangeR(lo,mid-1);arrangeR(mid+1,hi); return;
		}
		if(count == keys_main.length) return;		
	}
	
	public void printOrder(){
		String st = printOrder(root);
		StdOut.print(st);
	}
	
	private String printOrder(Node x){
		if(x== null) return "";
		String st = "";
		st = printOrder(x.left)+ x.key + printOrder(x.right);
		return st;
	}
	
	public static void main(String args[]){
		Ex_3_2_25<String,Integer> ob = new Ex_3_2_25<String,Integer>();
		Scanner scan = new Scanner(System.in);
		try{
			StdOut.println("Please input keys:");
			String st = scan.nextLine();
			StdOut.println("Given input of strings is: "+ st);
			String delims = " ";
			String st1[]  = st.split(delims);
			ob.arrange(st1);
			
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}
	
	// Q W E R T Y U I O P

}
