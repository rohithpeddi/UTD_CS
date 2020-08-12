import java.util.Scanner;


import edu.princeton.cs.algs4.StdOut;

public class Ex_3_3_26 <Key extends Comparable<Key>,Value>{
	
	private static final boolean RED = true;
	private static final boolean BLACK = false;
	
	private Node root;
	
	private class Node{
		Key key; Value val; Node left,right; int N; boolean color;
		Node(Key k, Value v, int N, boolean color){
			this.key =k; this.val =v; this.N = N; this.color = color;
		}
	}
	
	//isRed() IMPLEMENTATION
	
	private boolean isRed(Node x){
		if(x==null) return false;
		else return x.color == RED;
	}
	
	//SIZE IMPLEMENTATION
	
	public int size(){
		return size(root);
	}
	
	private int size(Node x){
		if(x == null) return 0;
		else return x.N;
	}
	
	//ROTATE IMPLEMENTATIONS
	
	private Node rotateLeft(Node h){
		Node x = h.right; h.right = x.left; x.left =h;
		x.color = h.color; h.color =RED;
		x.N = h.N; h.N = size(h.left)+1+size(h.right);
		return x;
	}
	
	private Node rotateRight(Node h){
		Node x = h.left; h.left = x.right; x.right =h;
		x.color = h.color; h.color =RED;
		x.N = h.N; h.N = size(h.left)+1+size(h.right);
		return x;
	}
	
	//FLIPCOLORS IMPLEMENTATION
	
	private void flipColors(Node x){
		x.left.color =BLACK; x.right.color =BLACK; x.color =RED;
	}
	
	//GET IMPLEMENTATION

	public Value get(Key k){
		return get(root,k);
	}
	
	private Value get(Node x, Key k){
		if(x==null) return null;
		
		int cmp = k.compareTo(x.key);
		if(cmp<0) return get(x.left,k);
		else if(cmp>0) return get(x.right,k);
		else return x.val;
	}
	
	//PRINT IMPLEMENTATION
	

	public void printOrder(){		
		printOrder(root);
	}
	
	private void printOrder(Node x){		
		if(x == null) {StdOut.print("");return;}	
		
		printOrder(x.left); 		
		StdOut.print(x.key); if(x.color == RED && x!=root) {StdOut.print("-");}		
		printOrder(x.right);
		
	}
	
	// PUT IMPLEMENTATION
	
	public void put(Key k, Value v){
		Node current = root,prev=current;
		int ind=3,check=3;
		if(current == null) {root = new Node(k,v,1,RED);return;}
		//StdOut.println("Entering patch-1 in between !");
		while(current != null){		
			
			if(isRed(current.right) && !isRed(current.left)) {
				if(current == root) check=0;
				current = rotateLeft(current);
				if(check==0){root = current; check=3;}
			}
			if(isRed(current.left) && isRed(current.left.left)) {
				if(current == root) check=0;
				current = rotateRight(current);
				if(check==0){root = current; check=3;}
			}
			if(isRed(current.left) && isRed(current.right)) flipColors(current);
			prev = current;
			
			int cmp = k.compareTo(current.key);
			if(cmp <0) {current = current.left;ind=0;}
			else if(cmp>0) {current = current.right;ind=1;}
			else {current.val =v;return;}
		}
		
		//StdOut.println("Entered patch-2 in between !");
		
		if(ind==0){
			//StdOut.print("Entered-left part! Adding "+ k );
			prev.left = new Node(k,v,1,RED);
			prev.N = size(prev.left)+1+size(prev.right);
			return;
			}
		if(ind==1){
			//StdOut.print("Entered-right part ! Adding "+ k );
			prev.right = new Node(k,v,1,RED);
			prev.N = size(prev.left)+1+size(prev.right);
			return;
			}
		root = sizeCorrection(root,k);
	}
	
	private Node sizeCorrection(Node x, Key k){
		int cmp = k.compareTo(x.key);
		if(cmp<0) x.left = sizeCorrection(x.left,k);
		else if(cmp>0) x.right = sizeCorrection(x.right,k);
		else return x;
		
		x.N = size(x.left)+1+size(x.right);
		return x;
	}
		
	public static void main(String args[]){
		Ex_3_3_26<String,Integer> ob = new Ex_3_3_26<String,Integer>();
		Scanner scan = new Scanner(System.in);
		try{
			StdOut.println("Please input keys:");
			String st = scan.nextLine();
			StdOut.println("Given input of strings is: "+ st);
			String delims = " ";
			String st1[]  = st.split(delims);
			for(int i=0; i<st1.length;i++){
				//StdOut.println(i+":"+st1[i]);
				ob.put(st1[i], i); 
				//StdOut.println(i+":"+st1[i]);
				ob.printOrder();
				StdOut.println(" \n ");
			}
			
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}

}
