import edu.princeton.cs.algs4.StdOut;

public class Ex_3_3_33<Key extends Comparable<Key>,Value> {
	
	private Node root;
	private static final boolean RED = true;
	private static final boolean BLACK = false;
	
	private class Node{
		Key key;Value val; int N; boolean color;Node left,right;
		Node(Key key,Value val, int N, boolean color){
			this.key = key; this.val = val; this.N = N; this.color = color;
		}
	}
	
	private boolean isRed(Node x){
		if(x==null) return false;
		else return x.color;
	}
	
	/*************************************************
	 * ROTATION IMPLEMENTATION
	 *************************************************/
	
	private Node rotateLeft(Node h){
		Node x = h.right;
		h.right = x.left;
		x.left = h;
		x.color = h.color;
		h.color = RED;
		x.N = h.N;
		h.N = 1+ size(h.left)+size(h.right);
		return x;
	}
	
	private Node rotateRight(Node h){
		Node x = h.left;
		h.left = x.right;
		x.right = h;
		x.color = h.color;
		h.color =RED;
		x.N = h.N;
		h.N = 1+ size(h.left)+ size(h.right);
		return x;
	}
	

	/*************************************************
	 * SIZE IMPLEMENTATION
	 *************************************************/
	
	public int size(){
		return size(root);
	}
	
	private int size(Node x){
		if(x == null) return 0;
		else return x.N;
	}
	

	/*************************************************
	 * FLIPCOLOR IMPLEMENTATION
	 *************************************************/
	
	private void flipColors(Node h){
		h.color = RED;
		h.left.color = BLACK;
		h.right.color = BLACK;
	}	

	/*************************************************
	 * PUT IMPLEMENTATION
	 *************************************************/
	
	public void put(Key k, Value v){
		root = put(root,k,v);
	}
	
	private Node put(Node x, Key k, Value v){
		if(x == null) return new Node(k,v,1,RED);
		
		int cmp = k.compareTo(x.key);
		if(cmp<0) x.left = put(x.left,k,v);
		else if(cmp>0) x.right = put(x.right,k,v);
		else x.val = v;
		
		if(isRed(x.right) && !isRed(x.left)) x = rotateLeft(x);
		if(isRed(x.left) && isRed(x.left.left)) x = rotateRight(x);
		if(isRed(x.left) && isRed(x.right)) flipColors(x);
		
		x.N = size(x.left) + 1 + size(x.right);
		return x;
	}
	
	/*************************************************
	 * GET IMPLEMENTATION
	 *************************************************/
	
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

	/*************************************************
	 * PRINT IMPLEMENTATION
	 *************************************************/
	
	public void printOrder(){
		//StdOut.println("Entered public print");
		printOrder(root);
	}
	
	private void printOrder(Node x){
		
		if(x == null) {StdOut.print("");return;}	
		
		printOrder(x.left); 		
		StdOut.print(x.key); if(x.color == RED && x!=root) {StdOut.print("-");}		
		printOrder(x.right);
		
	}
	
	/**************************************************
	 * CERTIFICATION IMPLEMENTATION
	 **************************************************/
	
	public boolean is23(){
		return is23(root);
	}
	
	private boolean is23(Node x){
		if(x==null) return true;
		
		if(isRed(x.left) && isRed(x.right)) return false;
		else if(isRed(x.right)) return false;
		else {
			if(is23(x.left) && is23(x.right)) return true;
			else return false;
		}
	}
	
	private boolean isBalanced() { 
        int black = 0;
        Node x = root;
        while (x != null) {
            if (!isRed(x)) black++;
            x = x.left;
        }
        return isBalanced(root, black);
    }

    private boolean isBalanced(Node x, int black) {
        if (x == null) return black == 0;
        if (!isRed(x)) black--;
        return isBalanced(x.left, black) && isBalanced(x.right, black);
    }
    
    /******************************************************
     * TEST CLIENT
     ******************************************************/
    
    public static void main(String args[]){
    	
    }
	

}
