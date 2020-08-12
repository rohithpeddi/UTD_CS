/**
 * 
 */
package Tries;

import java.io.File;
import java.io.PrintWriter;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

//Number of unique substrings 

public class Ex_5_2_15<Value> {
	
	private Node root;
	
	/*****************CONSTRUCTOR IMPLEMENTATION********************/
	
	public Ex_5_2_15(Scanner scan){
		Integer i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			//StdOut.println(st);
			put(st,(Value) i);
			i++;
		}
		StdOut.println("Done adding to the tree");
		StdOut.println(root.W);
	}
	
	/*****************NODE IMPLEMENTATION********************/
	
	private class Node{
		char c; 
		Node left,right,mid;
		Value val;
		int N; //size variable added
		int W; //words in the subtree
	}
	
	/*****************GET IMPLEMENTATION********************/
	
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
	
	/*****************SIZE IMPLEMENTATION********************/
	
	public int size(){
		return root.N;
	}
	
	private int size(Node x){
		if(x==null) return 0;
		else return x.N;
	}
	
	/*****************WORDS IMPLEMENTATION********************/
	
	public int words(){
		return root.W;
	}
	
	private int words(Node x){
		if(x==null) return 0;
		else return x.W;
	}
	
	/*****************PUT IMPLEMENTATION********************/
	
	public void put(String key, Value val){
		root = put(root,key,val,0);
	}
	
	public Node put(Node x, String key, Value val, int d){
		if(key.equals("")) return x; // Taken care of empty strings 
		char c = key.charAt(d);
		if(x==null){x = new Node(); x.c=c;x.N=1;x.W=0;}
		if(c<x.c) x.left = put(x.left,key,val,d);
		else if(c>x.c) x.right = put(x.right,key,val,d);
		else if(d<key.length()-1) x.mid =  put(x.mid,key,val,d+1);
		else {x.val = val;x.W++;}
		
		x.N = 1+ size(x.left)+size(x.mid)+size(x.right);
		x.W = words(x.left)+words(x.mid)+words(x.right);
		if(x.val!=null) x.W++;
		//StdOut.println("word count: "+ x.W);
		return x;
	}
	
	/*****************MAIN IMPLEMENTATION********************/
	
	public static void main(String args[]){
		try{
			StdOut.println("Enter string to find the number of distinct substrings!");
			Scanner scan=null;
			scan = new Scanner(System.in);
			String st = scan.nextLine();
			
			StdOut.println(st);
			
			char[] ar = st.toCharArray();
			
			PrintWriter pw = new PrintWriter("distinctsubstrings.txt");
			
			for(int i=1; i<=ar.length; i++){
				for(int j=0; j<=ar.length-i; j++){
					pw.println(st.substring(j, j+i));
				}
			}
			
			pw.close();
			
			scan = new Scanner(new File("distinctsubstrings.txt"));
			Ex_5_2_15 ob = new Ex_5_2_15(scan);
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
