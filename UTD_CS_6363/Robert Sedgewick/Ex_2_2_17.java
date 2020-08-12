package Mergesort;

public class Ex_2_2_17<Item> {
	
	private Node first;
	private int N;
	
	private class Node{
		Item item;
		Node next;
	}
	
	public Node add(Item i, Node bef){
		Node current = new Node();
		bef.next = current;
		current.item = i;
		return current;
	}
	
	public void init(int i){
		
	}
	
	public static void main(String args[]){
		
	}
	
}
