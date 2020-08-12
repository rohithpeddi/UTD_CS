package MinimumSpanningTrees;

import java.util.Iterator;

import edu.princeton.cs.algs4.StdOut;

public class MinPQ<Key extends Comparable<Key>> {
	
	private Key[] pq;
	private int N=0;
	
	public MinPQ(int cap){
		pq = (Key[]) new Comparable[cap+1];
	}
	
	public MinPQ(Iterable<Key> keys, int cap){
		this(cap);
		Iterator<Key> it  = keys.iterator();
		while(it.hasNext()){
			insert(it.next());
		}
	}
	
	public boolean isEmpty(){
		return N==0;
	}
	
	public int size(){
		return N;
	}
	
	public void insert(Key v){
		pq[++N] = v;
		swim(N);
	}
	
	public Key delMin(){
		Key max = pq[1];
		exch(1,N--);
		pq[N+1] = null;
		sink(1);
		return max;
	}
	
	private boolean greater(int i, int j){
		return pq[i].compareTo(pq[j])>0 ? true : false;
	}
	
	private void exch(int i, int j){
		Key v=pq [i]; pq[i]=pq[j]; pq[j]=v; 
	}
	
	private void swim(int k){
		while(k>1 && greater(k/2 , k)){
			exch(k/2,k); k = k/2;
		}
	}
	
	private void sink(int k){
		while(2*k<=N){
			int j = 2*k;
			if(j<N && greater(j,j+1)) j++;
			if(!greater(k,j)) break;
			exch(k,j);
			k=j;
		}
	}
	

}
