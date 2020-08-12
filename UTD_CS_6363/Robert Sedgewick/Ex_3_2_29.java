/******************************************************************
 * CERTIFICATION- BINARY TREE CHECK - ORDER CHECK - EQUAL KEY CHECK
 ******************************************************************/

public class Ex_3_2_29<Key extends Comparable<Key>,Value> {
	
	private Node root;
	private int count;
	
	private class Node{
		Key key; Value val;
		Node left,right;
		int N;
		Node(Key k,Value v,int N){
			this.key = k; this.val = v;this.N = N;
		}
	}
	/************************************************************/
	// PUT IMPLEMENTATION RANDOM
	/************************************************************/
	public void put(Key k, Value v){
		if(count==0) {root = new Node(k,v,1);count+=2;return;}
		root = put(root,k,v,count);
		count++;
	}
	
	private Node put(Node x, Key k, Value v,int dif){
		if(x == null){ return new Node(k,v,1);}
		if(dif%2 == 0){ x.left = put(x.left,k,v,dif/2);} 
		else { x.right = put(x.right,k,v,dif/2);}
		x.N = size(x.left)+ size(x.right)+1;
		return x;
	}
	/************************************************************/
	// SIZE IMPLEMENTATION 
	/************************************************************/
	public int size(){
		return size(root);
	}
	
	private int size(Node x){
		if(x==null) return 0;
		else return x.N;
	}
	/************************************************************/
	// PRINT IMPLEMENTATION
	/************************************************************/
	public void printOrder(){
		String st = printOrder(root);
		StdOut.print(st);
	}
	
	private String printOrder(Node x){
		if(x== null) return "";
		String st = "";
		st = printOrder(x.left)+ x.val + printOrder(x.right);
		return st;
	}
	
	/************************************************************/
	// BINARY TREE CHECK IMPLEMENTATION
	/************************************************************/
	
	public boolean isBinaryTree(){
		Node st = isBinaryTree(root);
		return st== root;
	}
	
	private Node isBinaryTree(Node x){
		if(x==null) return x;
		int p = size(x.left)+1+size(x.right);
		if(x.N == p){
			Node r = isBinaryTree(x.left);Node q = isBinaryTree(x.right);
			if(r == x.left && q == x.right){return x;}
			else return null;
		} 
		return x;
	}
	
	/************************************************************/
	// ORDER CHECK IMPLEMENTATION
	/************************************************************/
	
	public boolean isOrdered(Key min, Key max){
		Node st = isOrdered(root,min,max);
		return st == root;
	}
	
	private Node isOrdered(Node x, Key min , Key max){
		StdOut.println("Entered !");
		if(x==null) return x;
		if(x.key.compareTo(min)>0 && x.key.compareTo(max)<0){
			StdOut.println("Entered-2 !");
			if(x.left != null){
				StdOut.println("Entered-3 !");
				if(x.key.compareTo(x.left.key)<0) {StdOut.println("Checked for: "+ x.key+ " and "+ x.left.key );return null;}
				if(x.right != null){
					StdOut.println("Entered-4 !");
					if(x.key.compareTo(x.right.key)>0){ StdOut.println("Checked for: "+ x.key+ " and "+ x.right.key );return null;}
				}
			}
			StdOut.println("Entered-5 !");
			Node p = isOrdered(x.left,min,max); Node q = isOrdered(x.right,min,max);
			if(p == x.left && q == x.right) {return x;}
			else {StdOut.print("culprit!"+ x.key+ "\n");return null;}
		} else {
			return null;
		}
	}
	
	/************************************************************/
	public static void main(String[] args){
		Ex_3_2_29<String,Integer> ob = new Ex_3_2_29<String,Integer>();
		Scanner scan = new Scanner(System.in);
		try{
			StdOut.println("Please input keys:");
			String st = scan.nextLine();
			StdOut.println("Given input of strings is: "+ st);
			String delims = " ";
			String st1[]  = st.split(delims);
			for(int i=0; i<st1.length;i++){
				ob.put(st1[i], i); ob.printOrder();StdOut.println(" \n ");
			}
			StdOut.print(ob.isBinaryTree()+" "+ob.isOrdered("A", "G"));
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}
}
