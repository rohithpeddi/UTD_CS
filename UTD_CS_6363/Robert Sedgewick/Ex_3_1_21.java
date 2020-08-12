
	/***********************************************************
	 * SEQUENTIAL SEARCH IMPLEMENTATION
	 * *********************************************************/

public class Ex_3_1_21<Key extends Comparable<Key>,Value>{
		
	private class Node{
		public Node(Key key, Value val, Node next){
			this.key = key;
			this.val = val;
			this.next = next;
		}
		Key key;
		Value val;
		Node next;
	}
	
	public int ref_counter=0;
	private Node first;
	private int N;
	
	public boolean isEmpty(){return N==0;}
	public int size(){return N;}
	
	public void insert(Key k, Value v){
		if(isEmpty()){ first = new Node(k,v,first);N++;return; }
		
		for(Node current = first; current != null; current = current.next){
			if(k.compareTo(current.key)==0){current.val = v; ++ref_counter; N++ ;return;}
		}		
		Node current = first;
		Node prev = first,ref=first;
		for(current = first; current != null; current = current.next){
			if(k.compareTo(current.key)<=0 && current == first){first = new Node(k,v,first);N++;return;}
			
			if(k.compareTo(current.key)<0){ref = prev; break;}
			
			if(current.next == null){current.next = new Node(k,v,null);N++;return;}
			prev = current;
			ref_counter+=4;
		}
		ref.next = new Node(k,v,current); N++;
		++ref_counter;
	}
	
	public Value check(Key k){
		for(Node current = first; current != null; current = current.next){
			if(k.compareTo(current.key)==0){return current.val;}
			++ref_counter;
		}
		return null;
	}
	
	
	/**************************************************************
	 * BINARY SEARCH IMPLEMENTATION
	 * ************************************************************/
	
	
	public int cap =10,M=0,counter=0;
	private Key[] arkey = (Key[]) new Comparable[cap];
	private Value[] arval = (Value[]) new Object[cap];
	
	public boolean isEmpty_BS(){return M==0;}
	public int size_BS(){return M;}
	
	public void resize(){
		cap = 2*cap;
		Key[] arkeyN = (Key[]) new Comparable[cap];
		Value[] arvalN = (Value[]) new Object[cap];
		
		for(int i=0;i<M;i++){
			arkeyN[i] = arkey[i]; arvalN[i] = arval[i];
			counter+=2;
		}		
		arkey = arkeyN; arval = arvalN;		
	}
	
	public int rank(Key k){
		int lo = 0, hi= M-1;
		while(lo<=hi){
			int mid = lo+ (hi-lo)/2;
			int cmp = k.compareTo(arkey[mid]);
			if(cmp<0){ hi = mid-1;}
			else if(cmp>0){ lo= mid+1;}
			else return mid;
			++counter;
		}
		return 0;
	}
	
	public void put(Key k,Value v){
		int n = rank(k);
		if(k.compareTo(arkey[n])==0){arval[n]= v; ++counter; return;}
		else{
			for(int j=M;j>n;j--){
				arkey[j]=arkey[j-1]; arval[j]=arval[j-1];
				counter+=2;
			}
			arkey[n]=k;arval[n]=v;
			M++; 
			if(M > (cap*3)/4) {resize();}
		}
	}
	
	public Value get(Key k){
		int n = rank(k);
		if(k.compareTo(arkey[n])==0){ return arval[n];}
		else{return null;}
	}
	
	public static void main(String args[]){
		
	}
	
}
