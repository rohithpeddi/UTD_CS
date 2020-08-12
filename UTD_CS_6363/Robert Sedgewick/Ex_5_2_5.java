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
/*
 * Non recursive version of TrieST and TST
 */

public class Ex_5_2_5<Value> {
	
	private static int R =256;
	private Node root;
	
	public Ex_5_2_5(Scanner scan){
		int N = Integer.parseInt(scan.nextLine());
		Integer i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			put(st,(Value) i);
			i++;
		}
		//StdOut.println("Done adding to the tree");
		StdOut.println(get("shore"));
	}
	
	private static class Node{
		Object val; //It has to be an object as java doesn't support generics 
		Node[] next = new Node[R];
	}
	
	public Value get(String key){
		Node current = root; int d=0;
		//StdOut.println(current.next[key.charAt(d)]!=null);
		while(current!=null && d<key.length()){
			char c= key.charAt(d);
			System.out.println("d:"+d+",c:"+c);
			if(current.next[c]==null) return null;
			current = current.next[c]; d++;
		}
		
		return (Value) current.val;
	}
	
	public void put(String key, Value val){
		//StdOut.println("Adding: "+key+":"+val);
		
		if(root == null) root =new Node();
		
		Node current = root; int d=0;
		while(d<key.length()){
			
			char c = key.charAt(d);
			if(current.next[c]== null){
				current.next[c]= new Node(); 
				current = current.next[c];
				if(d == key.length()-1) {current.val =val;return;}
				d++;
			}
			else {
				current = current.next[c];
				if(d == key.length()-1) {current.val =val;return;}
				d++;
			}			
			
		}
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("text.txt"));
			Ex_5_2_5 ob = new Ex_5_2_5(scan);
		} catch(Exception e){
			e.printStackTrace();
		}
	}	
	

}
