import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

//AVL TREES (Great Code)

public class Ex_3_3_32_great<Key extends Comparable<Key>,Value> {
	
	private Node root;
	
	private class Node{
		Key key; Value val;Node left,right; int height;
		Node(Key k, Value v, int height){
			this.key = k; this.val = v; this.height = height;
		}
	}
	
	//PUT IMPLEMENTATION
	
	public void put(Key k, Value v){
		root = put(root,k,v);
	}
	
	private Node put(Node x, Key k, Value v){
		if(x == null) return new Node(k,v,0);
		
		int cmp = k.compareTo(x.key);
		if(cmp<0){
			x.left = put(x.left,k,v);
            if( height( x.left ) - height( x.right ) == 2 ){
                if( k.compareTo( x.left.key ) < 0 ) x = rotateRight( x );
                else x = rotateLeftRight( x);
            }
		}		
		else if(cmp>0){
			x.right = put(x.right,k,v);
			if( height( x.right ) - height( x.left ) == 2 ){
                if( k.compareTo( x.right.key ) > 0 ) x = rotateLeft( x );
                else x = rotateRightLeft( x );
			}
		}
		else ;
		
		x.height = max( height( x.left ), height( x.right ) ) + 1;
        return x;
		
	}	
	
	//ROTATIONS IMPLEMENTATION
	
	 private Node rotateRight( Node h ){
	     Node x = h.left; h.left = x.right;x.right =h;
	     h.height = max( height( h.left ), height( h.right ) ) + 1;
	     x.height = max( height( x.left ), h.height ) + 1;
	     return x;
	 }
	
	 private Node rotateLeft( Node h ){
	     Node x = h.right;h.right = x.left; x.left = h;
	     h.height = max( height( h.left ), height( h.right ) ) + 1;
	     x.height = max( height( x.right ), h.height ) + 1;
	     return x;
	 }

     private Node rotateLeftRight( Node x ){
         x.left = rotateLeft( x.left );
         return rotateRight( x );
     }

     private Node rotateRightLeft( Node x ){
         x.right = rotateRight( x.right );
         return rotateLeft( x );
     }
     
     //HEIGHT IMPLEMENTATION
     
     public int height(){
    	 return height(root);
     }
     
     private int height(Node x){    	 
         return x == null ? -1 : x.height;       
     }
     
     //MAX IMPLEMENTATION
     
     private int max( int lhs, int rhs )
     {
         return lhs > rhs ? lhs : rhs;
     }
     
     //PRINT IMPLEMENTATION
     
     public void printOrder(){
    	 printOrder(root);
     }
     
     private void printOrder( Node t ){       
    	 if(t == null) {StdOut.print("");return;}
         printOrder( t.left );
         System.out.print( t.key+" " );
         printOrder( t.right );       
     }
	
     public static void main(String args[]){
    	Ex_3_3_32_great<String,Integer> ob = new Ex_3_3_32_great<String,Integer>();
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
