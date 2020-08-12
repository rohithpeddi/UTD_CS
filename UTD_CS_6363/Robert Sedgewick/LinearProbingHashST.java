package DirectedGraphs;

import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class LinearProbingHashST<Key,Value>{
	
	public int N;
	public int M =16;
	public Key[] keys;
	public Value[] vals;
	
	public LinearProbingHashST(int M){
		this.M =M;
		keys = (Key[]) new Object[M];
		vals = (Value[]) new Object[M];
	}
	
	/*******************************************************
	 * HASH INT GENERATION
	 *******************************************************/
	
	public int hash(Key key){
		return (key.hashCode() & 0x7fffffff) % M; 
	}
	
	/*******************************************************
	 * RESIZE GENERATION
	 *******************************************************/
	
	public void resize(int cap){
		LinearProbingHashST<Key,Value> t = new LinearProbingHashST<Key,Value>(cap);
		for(int i=0; i<M; i++){
			if(keys[i] != null){
				t.put(keys[i], vals[i]);
			}
		}
		keys = t.keys; vals = t.vals; M = t.M;
	}
	
	/*******************************************************
	 * PUT IMPLEMENTATION
	 *******************************************************/
	
	public void put(Key key, Value val){
		if(N>= M/2) resize(2*M);
		
		int i;
		for(i=hash(key); keys[i]!=null; i= (i+1)%M)
			if(keys[i].equals(key)) {	vals[i] = val; return;	}
		
		keys[i] = key; vals[i] = val;
		N++;
	}
	
	/*******************************************************
	 * GET IMPLEMENTATION
	 *******************************************************/
	
	public Value get(Key key){
		for(int i=hash(key); keys[i] != null; i = (i+1)%M)
			if(keys[i].equals(key)) return vals[i];
		return null;
	}
	
	public boolean contains(Key key){
		return get(key) != null;
	}
	
	/*******************************************************
	 * DELETE IMPLEMENTATION
	 *******************************************************/
	
	public void delete(Key key){
		if(!contains(key)) return;
		
		int i= hash(key);
		while(!key.equals(keys[i]))
			i=(i+1)%M;
		
		keys[i] = null; vals[i] = null;
		
		i=(i+1)%M;
		while(keys[i] != null){
			Key keyToRedo = keys[i];
			Value valToRedo = vals[i];
			
			keys[i] = null; vals[i] = null; N--;
			
			put(keyToRedo,valToRedo);
			i=(i+1)%M;
			
		}
		N--;
		if(N>0 && N == M/8) resize(M/2); 
			
	}
	

	/*******************************************************
	 * PRINT ORDER IMPLEMENTATION
	 *******************************************************/
	public void printOrder(){
		for(int i=0; i<M;i++){
			if(keys[i]!=null) StdOut.print(keys[i]+" ");
			else StdOut.print(". ");
		}
	}
	
	/*******************************************************
	 * SIZE GENERATION
	 *******************************************************/
	
	public boolean isEmpty(){
		return N==0;
	}
	
	public int size(){
		if(isEmpty()) return 0;
		return N;
	}
	
	public static void main(String args[]){
		LinearProbingHashST<String,Integer> ob = new LinearProbingHashST<String,Integer>(4);
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
				ob.delete(st1[i]);
				StdOut.println(i+":"+ob.get(st1[i]));
				StdOut.println(" \n ");
			}
			
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}
	
}
