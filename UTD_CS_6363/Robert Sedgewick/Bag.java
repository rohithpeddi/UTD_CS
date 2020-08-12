import java.util.Iterator;

public class Bag<Item extends Comparable<Item>> implements Iterable<Item> {
	
	private Node first;
	private int N;
	
	/************NODE CLASS************/
	
	private class Node{
		Item item; Node next;
		Node(Item k){
			this.item =k;
		}
	}
	
	/************isEmpty() IMPLEMENTATION************/
	
	private boolean isEmpty(){
		return N==0;
	}
	
	public int size(){return N;}
	
	/************	CONTAINS ************/
	
	public boolean contains(Item item){
		Node current = first;
		if(isEmpty()) return false;
		while(current != null){
			if(current.item.equals(item)){
				return true;
			}
			current = current.next;
		}
		return false;
	}
	
	
	/************ADD IMPLEMENTATION************/
	
	public void add(Item k){
		Node current = first;
		if(isEmpty()) { first = new Node(k);N++;return;}
		Node oldfirst = first;
		first = new Node(k);
		first.next = oldfirst;
		N++;
		return;		
	}
	
	/*********  DELETE IMPLEMENTATION ****************/
	
	public void delete(Item k){
		Node current = first;
		if(isEmpty()) return;
		
		Node previous = current;
		while(current != null){
			if(current.item.compareTo(k)==0) break;
			previous = current;			
			current = current.next;
		}
		
		if(current == first){first = first.next;return;}
		if(current == null) return;
		
		previous.next = current.next;
	}
	
	/************ITERATOR IMPLEMENTATION************/
	//returns an iterable list 
	public Iterator<Item> iterator(){
		return new ListIterator();
	}
	
	/************LIST ITERATOR CLASS ************/
	//making the datastructure iterable and returns an iterable list 
	private class ListIterator implements Iterator<Item>{

		private Node current = first;
		
		public boolean hasNext(){
			return current != null;
		}
		
		public Item next(){
			Item item = current.item;
			current = current.next;
			return item;
		}
		
		public void remove(){
			return;
		}
		
	}
}
