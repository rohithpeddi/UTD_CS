import java.util.Scanner;


import edu.princeton.cs.algs4.StdOut;

public class Ex_3_2_33<Key extends Comparable<Key>,Value> {
	
	private Node root;
	
	private class Node{
		Key key; Value val; int N;
		Node left,right;
		Node(Key k, Value v, int N){
			this.key =k; this.val = v; this.N = N;
		}
	}
	
	public Value get(Key k){
		return get(root,k);
	}
	
	private Value get(Node x,Key k){
		if(x == null) return null;
		int cmp = k.compareTo(x.key);
		if(cmp<0) return get(x.left,k);
		else if(cmp>0) return get(x.right,k);
		else{return x.val;}
	}
	
	public void put(Key k, Value v){
		root = put(root,k,v);
	}
	
	private Node put(Node x, Key k,Value v){
		if(x == null) {x = new Node(k,v,1);return x;}
		int cmp = k.compareTo(x.key);
		if(cmp<0){x.left = put(x.left,k,v);}
		else if( cmp>0){x.right = put(x.right,k,v);}
		else { x.val = v;}
		x.N = size(x.left)+1+size(x.right);
		return x;
	}
	
	public int size(){
		return size(root);
	}
	
	private int size(Node x){
		if(x == null) return 0;
		else return x.N;
	}
	
	public Key select(int k){
		return select(root,k).key;
	}
	
	private Node select(Node x,int k){
		if(x==null) return null;
		int t = size(x.left);
		if(t>k) return select(x.left,k);
		else if(t<k) return select(x.right,k-t-1);
		else return x;
	}
	
	public int rank(Key key){
		return rank(root,key);
	}
	
	private int rank(Node x, Key key){
		if(x==null) return 0;
		int cmp = key.compareTo(x.key);
		if(cmp <0) return rank(x.left,key);
		else if(cmp>0) return 1+size(x.left)+rank(x.right,key);
		else return size(x.left);
	}
	
	public static void main(String args[]){
		Ex_3_2_33<String,Integer> ob = new Ex_3_2_33<String,Integer>();
		Scanner scan = new Scanner(System.in);
		try{
			StdOut.println("Please input keys:");
			String st = scan.nextLine();
			StdOut.println("Given input of strings is: "+ st);
			String delims = " ";
			String st1[]  = st.split(delims);
			for(int i=0; i<st1.length;i++){
				ob.put(st1[i], i); 
			}
			
			for(int i=0;i<st1.length;i++){
				if(i != ob.rank(ob.select(i))) {StdOut.print("False check "+i);break;}
				if(!st1[i].equals(ob.select(ob.rank(st1[i])))) {StdOut.print("False check ");break;}
				if(i== st1.length-1) {StdOut.print("Check successful");}
			}
			
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}
	
}
