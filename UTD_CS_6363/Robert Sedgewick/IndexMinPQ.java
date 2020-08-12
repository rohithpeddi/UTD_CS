package MinimumSpanningTrees;

import edu.princeton.cs.algs4.StdOut;

public class IndexMinPQ<Key extends Comparable<Key>> {
	
	private int N; 
	private int[] pq,qp;
	private Key[] keys;
	
	public IndexMinPQ(int cap){
		pq = new int[cap+1]; qp = new int[cap+1];
		keys = (Key[]) new Comparable[cap+1];
		for(int i=0; i<cap+1;i++)
			qp[i] =-1;
	}
	
	public boolean isEmpty(){return N==0;}
	public int size() { return N;}
	public boolean contains(int k){	return qp[k]!=-1;}
	
	public void insert(int k, Key key){
		N++; qp[k] = N; pq[qp[k]] = k;
		keys[k] = key;
		swim(N);
	}
	
	public void change(int k, Key key){
		Key current = keys[k];
		if(current.compareTo(key)>0){
			keys[k] = key; sink(k);
		} else if(current.compareTo(key)<0){
			keys[k] =key; swim(k);
		}
	}
	
	public Key min(){
		return keys[pq[1]];
	}
	
	public int delMin(){
		int indexOfMin = pq[1];
		exch(1,N--);
		sink(1);
		keys[pq[N+1]] = null;
		qp[pq[N+1]] = -1;
		return indexOfMin;		
	}
	
	private boolean greater(int i, int j){
		//StdOut.println("In IndexMinPQ-->"+pq[i]+","+pq[j] +"      :    "+ keys[pq[i]]+":"+keys[pq[j]]  );
		return keys[pq[i]].compareTo(keys[pq[j]]) >0;
	}
	
	private void exch(int i, int j){
		int swap = pq[i]; pq[i]=pq[j]; pq[j]= swap;
		qp[pq[i]]=i; qp[pq[j]]=j;
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
