/**
 * 
 */
package Tries;

import java.io.File;
import java.util.Scanner;


import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

//Eager version of size implementation 
//Taken care of empty strings in TST

public class Ex_5_2_10<Value> {
	
	private Node root;

	public Ex_5_2_10(Scanner scan){
		int N = Integer.parseInt(scan.nextLine());
		Integer i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			put(st,(Value) i);
			i++;
		}
		StdOut.println("Done adding to the tree");
		StdOut.println(size());
	}
	
	private class Node{
		char c; 
		Node left,right,mid;
		Value val;
		int N; //size variable added
	}
	
	public Value get(String key){
		Node x = get(root,key, 0);
		if(x==null) return null;
		else return (Value)x.val;
	}
	
	private Node get(Node x, String key, int d){		
		if(x == null) return null;
		char c = key.charAt(d);
		if(c<x.c) return get(x.left,key,d);
		else if(c>x.c) return get(x.right,key,d);
		else if(d<key.length()-1) return get(x.mid, key, d+1);
		else return x;
	}
	
	public int size(){
		return root.N;
	}
	
	private int size(Node x){
		if(x==null) return 0;
		else return x.N;
	}
	
	public void put(String key, Value val){
		root = put(root,key,val,0);
	}
	
	public Node put(Node x, String key, Value val, int d){
		if(key.equals("")) return x; // Taken care of empty strings 
		char c = key.charAt(d);
		if(x==null){x = new Node(); x.c=c;x.N=1;}
		if(c<x.c) x.left = put(x.left,key,val,d);
		else if(c>x.c) x.right = put(x.right,key,val,d);
		else if(d<key.length()-1) x.mid =  put(x.mid,key,val,d+1);
		else x.val = val;
		
		x.N = 1+ size(x.left)+size(x.mid)+size(x.right);
		return x;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("text.txt"));
			Ex_5_2_10 ob = new Ex_5_2_10(scan);
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
