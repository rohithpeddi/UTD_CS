import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class Ex_3_2_28<Key extends Comparable<Key>,Value> {
	
	private Node root;
	public String[] cacheArray = new String[10];
	private int count=0;
	
	private class Node{
		Key key; Value val;
		Node left,right;
		Node(){}
		Node(Key k,Value v){
			this.key =k; this.val = v;
		}
	}
	
	public Value get(Key k){
		String str = k+"";
		for(int i=0;i<10;i+=2){
			if(k.equals(cacheArray[i])) {return (Value) cacheArray[i+1];}
		}
		
		Node current = root;
		if(current == null) return null;
		while(current!=null){
			int cmp = k.compareTo(current.key);
			if(cmp<0) current = current.left;
			else if(cmp>0) current = current.right;
			else{
				Value va = current.val;
				note(current);
				return va;
			}
		}
		return null;
	}
	
	public void note(Node x){
		if(count==0){
		cacheArray[0] = x.key+"";
		cacheArray[1] = x.val+"";count =2;		
		} else{
			int N = count;
			if(count>=10){N=8;}
			for(int i=N-1;i>=0;i-- ){
				cacheArray[i+2]= cacheArray[i];
			}
			cacheArray[0] = x.key+"";
			cacheArray[1] = x.val+"";count +=2;	
		}
		for(String str:cacheArray){StdOut.print(str+" ");}StdOut.print("\n");
	}	
	
	public void put(Key k, Value v){
		Node current = root; if(current == null){root = new Node(k,v);return;}
		Node prev =current; int ind =0;
		while(current != null){
			prev = current;
			int cmp = k.compareTo(current.key);
			if(cmp<0){current = current.left;ind =0;}
			else if(cmp>0){current = current.right;ind =1;}
			else{current.val = v;}
		}
		
		if(ind==0){prev.left = new Node(k,v);return;}
		else{prev.right = new Node(k,v);return;}
	}
	
	public void printOrder(){
		String st = printOrder(root);
		StdOut.print(st+"\n");
	}
	
	private String printOrder(Node x){
		if(x==null) return "";
		String st = "";
		st = printOrder(x.left)+x.val+printOrder(x.right)+"";
		return st;
	}
	
	public static void main(String[] args){
		Ex_3_2_28<String,Integer> ob = new Ex_3_2_28<String,Integer>();
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
			for(int i=0; i<st1.length;i++){
				ob.get(st1[i]);StdOut.println(" \n ");
			}
			
			
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}

}
