/**
 * 
 */
package Tries;


import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.Queue;
import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

//Ordered operations for TrieST

public class Ex_5_2_8<Value> {
	
	private static int R =256;
	private Node root;
	
	public Ex_5_2_8(Scanner scan){
		int N = Integer.parseInt(scan.nextLine());
		Integer i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			put(st,(Value) i);
			i++;
		}
		StdOut.println("Done adding to the tree");
		StdOut.println(select(9));
	}
	
	/******************NODE IMPLEMENTATION********************/
	//implemented as a static class, and uses static variable R
	private static class Node{
		Object val; //It has to be an object as java doesn't support generics 
		Node[] next = new Node[R];
		int N;
		int W;
	}
	
	/******************GET IMPLEMENTATION********************/
	
	public Value get(String key){
		Node x = get(root,key,0);
		if(x==null) return null;
		else return (Value)x.val;
	}
	
	private Node get(Node x, String key, int d){
		if(x==null) return null;
		if(d == key.length()) return x;
		char c = key.charAt(d);
		return get(x.next[c],key,d+1);
	}
	
	/******************PUT IMPLEMENTATION********************/
	
	public void put(String key,Value val){
		root = put(root, key, val,0);
	}
	
	private Node put(Node x, String key, Value val, int d){
		if(x==null) {x = new Node();x.N=1;x.W=0;}
		if(d == key.length()) {x.val = val; x.W++; return x;}
		char c = key.charAt(d);
		x.next[c] = put(x.next[c],key,val,d+1);
		int count=1,countW=0;
		for(char cc=0;cc<R;cc++){
			count+= size(x.next[cc]);
			countW+= words(x.next[cc]);
		}
		x.N = count;
		if(x.val !=null) countW++;
		x.W = countW;
		return x;
	}
	
	/******************WORD COUNT IMPLEMENTATION********************/
	
	public int words(){
		return root.W;
	}
	
	private int words(Node x){
		if(x==null) return 0;
		else return x.W;
	}
	
	/******************SIZE IMPLEMENTATION********************/
	
	public int size(){
		return root.N;
	}
	
	private int size(Node x){
		if(x==null) return 0;
		else return x.N;
	}
	
	/******************RANK IMPLEMENTATION********************/
	
	public Integer rank(String s){
		return rank(root,s,0,0);
	}
	
	private Integer rank(Node x,String s,int d,int count){
		if(x==null) return null;
		if(d == s.length() && x.val!=null) return count;
		char c = s.charAt(d);
		for(char cc=0; cc<c; cc++ ){
			if(x.next[cc]!=null) count+= words(x.next[cc]);
		}
		
		return rank(x.next[c],s,d+1,count);		
	}
	
	/******************SELECT IMPLEMENTATION********************/
	
	public String select(int i){
		return select(root,i,i,"");
	}
	
	private String select(Node x,int i,int d,String st){
		if(x==null) return null;
		if(x.val!=null) return st;
		
		//StdOut.println("In select before: "+ st+", i:"+i+", d:"+d);
		char c=0; int count=0;
		for(c=0; c<R; c++){
			if(x.next[c]!=null){
				count+= words(x.next[c]);
				if(count > i) break; 
			}
		}
		i= i-(count-words(x.next[c]));
		StdOut.println("In select: "+ st+", i:"+i+", d:"+d+", words:"+words(x.next[c]));
		return select(x.next[c],i,d,st+""+c);		
	}
	
	/******************KeysWithPrefix IMPLEMENTATION********************/
	
	public Iterable<String> keys(){
		return keysWithPrefix("");
	}
	
	private Iterable<String> keysWithPrefix(String pre){
		Queue<String> q = new Queue<String>();
		collect(get(root,pre,0),pre,q);		
		return q;
	}
	
	private void collect(Node x, String pre, Queue<String> q){
		if(x==null) return;
		if(x.val!=null) q.enqueue(pre);
		for(char c=0; c<R; c++){
			if(x.next[c]!=null){
				collect(x.next[c],pre+c,q);
			}
		}
	}
	
	/******************keysThatMatch IMPLEMENTATION********************/
	
	public Iterable<String> keysThatMatch(String pat){
		Queue<String> q = new Queue<String>();
		collect(root,"",pat,q);
		return q;
	}
	
	private void collect(Node x, String pre, String pat, Queue<String> q){
		int d = pre.length();
		if(x==null) return;
		if(d == pat.length() && x.val!=null) q.enqueue(pre);
		if(d==pat.length()) return;
		
		char next = pat.charAt(d);
		
		for(char c=0; c<R; c++){
			if(next == '.'|| next==c){
				collect(x.next[c],pre+c,pat,q);
			}
		}
	
	}
	
	/******************longestPrefixOf IMPLEMENTATION********************/
	
	public String longestPrefixOf(String s){
		int length = search(root,s,0,0);
		return  s.substring(0,length);
	}
	
	private int search(Node x, String s, int d, int length){
		if(x==null) return length;
		if(x.val!=null) length =d;
		if(d == s.length()) return length;
		char c= s.charAt(d);
		search(x.next[c],s,d+1,length);
		return length;
	}
	
	/******************DELETE IMPLEMENTATION********************/
	
	public void delete(String key){
		root = delete(root,key,0);
	}
	
	private Node delete(Node x, String key,int d){
		if(x==null) return x;
		if(d == key.length()){
			if(x.val!=null) x.val=null;
		} else {
			char c = key.charAt(d);
			x.next[c]= delete(x.next[c], key,d+1);
		}
		
		if(x.val!=null) return x;
		for(char c=0; c<R; c++){
			if(x.next[c]!=null) return x;
		}
		
		return null;
		
	}	
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("text.txt"));
			Ex_5_2_8 ob = new Ex_5_2_8(scan);
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
