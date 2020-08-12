import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;

public class Ex_3_1_1<Key extends Comparable<Key>, Value> {
	
	private Node first;
	private int N;
	
	public boolean isEmpty(){
		return N==0;
	}
	
	public int size(){
		return N;
	}
	
	private class Node{
		Key key;
		Value val;
		Node next;
		
		public Node(Key key, Value val, Node node){ // Node is always first for addition purposes
			this.key = key;
			this.val = val;
			this.next = node;
		}
	}
	
	public void insert(Key k, Value v){
		for(Node current = first; current != null; current = current.next){
			if(k.equals(current.key)){
				current.val = v; return;
			}
		}		
		Node current = first;
		
		for(current=first; current != null && k.compareTo(current.key)>=0; current = current.next){			
			if(current.next == null) {
				current.next = new Node(k,v,null); return;
			} else {
				if(k.compareTo(current.next.key)<0){
					if(current == first) {
						Node insNode = new Node(k,v,current.next);
						current.next = insNode;
						N++; 
						return;
						}
					break;
				}
			}
		}
		if(current == first) {first = new Node(k,v,first); N++; return;}
		Node insNode = new Node(k,v,current.next);
		current.next = insNode;
		N++; return;
	}
	
	public Value get(Key k){
		Value val = null ;
		for(Node current = first; current != null; current = current.next){
			if(k.equals(current.key)){
				val = current.val;
				return val;
			}
		}
		return val;
	}
	
	public void printOrder(){
		for(Node current= first; current != null; current = current.next){
			StdOut.print(current.val+"  ");
		}
	}
	/*
	public void init(Ex_3_1_1 ob){
		ob.insert("A+", 4.33);
		ob.insert("A", 4.00);
		ob.insert("A-", 3.67);
		ob.insert("B+", 3.33);
		ob.insert("B", 3.00);
		ob.insert("B-", 2.67);
		ob.insert("C+", 2.33);
		ob.insert("C", 2.00);
		ob.insert("C-", 1.67);
		ob.insert("D", 1.33);
		ob.insert("F", 1.00);				
	} */
	
	public static void main(String args[]){
		Ex_3_1_1<String, Double> ob = new Ex_3_1_1<String, Double>();
		
		ob.insert("A", 4.00);
		ob.insert("A-", 3.67);
		ob.insert("B+", 3.33);
		ob.insert("B", 3.00);
		ob.insert("B-", 2.67);
		ob.insert("C+", 2.33);
		ob.insert("C", 2.00);
		ob.insert("C-", 1.67);
		ob.insert("D", 1.33);
		ob.insert("F", 1.00);
		ob.insert("A+", 4.33);
		ob.printOrder();
		StdOut.println(" ");
		StdOut.println("Provide us with an input:");
		String scores = StdIn.readLine();
		StdOut.println("Given input is:"+ scores);
		String delims = " ";
		String[] score = scores.split(delims);
		for(String x:score){StdOut.print(x+" ");} StdOut.println(" ");
		Double sum=(double) 0,n = (double) score.length;
		for(int i=0; i<score.length;i++){
			Double p = (Double)ob.get(score[i]); StdOut.println(p+" ");
			sum += p;
		}
		StdOut.println("The GPA for  given string: "+ scores+"is: \n"+ (sum/n));
		
	}

}
