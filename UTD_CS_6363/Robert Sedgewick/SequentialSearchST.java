public class SequentialSearchST<Key,Value> {
	
	private Node first;
	private int N=0;
	
	private class Node{
		Key key; Value val; Node next;
		Node(Key k,Value v){
			this.key = k; this.val =v;
		}
	}
	
	public boolean isEmpty(){
		return first==null;
	}
	
	/*******************************************************
	 * PUT IMPLEMENTATION
	 *******************************************************/
	
	public void put(Key k, Value v){
		Node current = first;
		if(isEmpty()) {
			first = new Node(k,v);N++;
			return;
		}
		Node prev = current;
		while(current != null){
			prev = current;
			current = current.next;
		}
		prev.next = new Node(k,v); N++;
		return;
	}
	
	/*******************************************************
	 * GET IMPLEMENTATION
	 *******************************************************/
	
	public Value get(Key k){
		Node current =first;
		if(isEmpty()) return null;
		else {
			while(current != null){
				if(current.key.equals(k)) return current.val;
				else current = current.next;
			}
		}
		return null;
	}
	
	/*******************************************************
	 * DELETE IMPLEMENTATION
	 *******************************************************/
	
	
	public void delete(Key k){
		Node current = first;
		if(isEmpty()) return;
		else{
			Node prev = current;
			while(current !=null){
				if(current.key.equals(k)) {
					if(current == first) {	first = first.next; N--;return;}
					prev.next = current.next;N--;
					return; 
				}
				prev = current;
				current = current.next;
			}
			return;
		}
	}
	
	/*******************************************************
	 * SIZE IMPLEMENTATION
	 *******************************************************/
	
	public int size(){
		return N;
	}
	
}
