package MinimumSpanningTrees;

import java.util.Iterator;

import edu.princeton.cs.algs4.StdOut;

public class MaxPQ<Key extends Comparable<Key>>{
	
	private Key[] pq;
	private int N=0;
	
	public MaxPQ(int cap){
		pq = (Key[]) new Comparable[cap+1];
	}
	
	public boolean isEmpty(){return N==0;}
	public int size(){return N;}
	
	public MaxPQ(Iterable<Key> keys, int cap){
		this(cap);
		StdOut.println("Constructor MaxPQ:"+ cap);
		Iterator<Key> it  = keys.iterator();

		while(it.hasNext()){
			
			insert(it.next());

		}
	}
	
	public void insert(Key v){
		//StdOut.println("Inserting-"+N);
		pq[++N] = v;
		swim(N);
	}
	
	public boolean less(int i, int j){
		return pq[i].compareTo(pq[j])<0;
	}
	
	public void exch(int i, int j){
		Key swap = pq[i]; pq[i]= pq[j]; pq[j]=swap;
	}
	
	public Key delMax(){
		if(isEmpty()) throw new RuntimeException("priority queue is empty!");
		Key max = pq[1];
		exch(1,N--);
		sink(1);
		return max;
	}
	
	public void swim(int k){
		while(k>1 && less(k/2,k)){
			exch(k/2,k);
			k = k/2;
		}
	}
	
	public void sink(int k){
		while(2*k<=N){
			int j = 2*k;
			if(!less(k,j)) break;
			if(k<N && less(j,j+1)) j++;
			exch(k,j);
			k = j;
		}
	}

}
