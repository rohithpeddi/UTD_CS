package ShortestPaths;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;
import java.util.Stack;

import MinimumSpanningTrees.IndexMinPQ;
import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

// Multisource shortest paths 
// Works for few values and doesn't for few figure out what's wrong later

public class Ex_4_4_24 {
	
	private double[] distTo;
	private IndexMinPQ<Double> pq;
	private LinearProbingHashST<Integer,Integer> ht;
	private LinearProbingHashST<Integer,Stack<Integer>> gt;
	
	public Ex_4_4_24(EdgeWeightedDigraph G, Iterable<Integer> sources){
		
		distTo = new double[G.V()]; pq = new IndexMinPQ<Double>(G.V());
		StdOut.println(G.V());
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		}
		Iterator<Integer> it = sources.iterator();	
		ht = new LinearProbingHashST<Integer,Integer> (G.V());
		gt = new LinearProbingHashST<Integer,Stack<Integer>>(G.V());
		
		int count =0;
		while(it.hasNext()){
			int v = it.next();
			StdOut.print(v+" ");
			distTo[v] = 0.0; pq.insert(v, 0.0); ht.put(v, v);
			Stack<Integer> st = new Stack<Integer>();
			gt.put(v, st);
			count++;
		}
		
		
		while(!pq.isEmpty()){
			relax(G,pq.delMin());
		}		
		
		printSF(G,sources);
		
	}
	
	private void relax(EdgeWeightedDigraph G, int v){
		for(DirectedEdge e: G.adj(v)){
			int w = e.to();
			
			if(distTo[w]> distTo[v]+e.weight()){
				StdOut.println(v+":"+w);
				distTo[w]=distTo[v]+e.weight();
				if(pq.contains(w)) pq.change(w, distTo[w]);
				else pq.insert(w, distTo[w]);
				
				int source = ht.get(v);
				if(ht.contains(w)){ht.delete(w);ht.put(w, source);}
				else ht.put(w, source);
			}
		}
	}
	
	private void printSF(EdgeWeightedDigraph G, Iterable<Integer> sources){
		
		for(int i=0; i<G.V(); i++){
			int source = ht.get(i);
			Stack<Integer> st = gt.get(source);
			st.push(i);
		}
		
		Iterator<Integer> it = sources.iterator();
		while(it.hasNext()){
			int v = it.next();
			Stack<Integer> st = gt.get(v);
			StdOut.println("Source "+v+ ": "+ st);
		}
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("8verts.txt"));
			EdgeWeightedDigraph G =new EdgeWeightedDigraph(scan);
			Bag<Integer> bg = new Bag<Integer>();
			for(int i=0; i<3; i++){
				int v = StdRandom.uniform(1,8);
				bg.add(v);
			}
			Iterator<Integer> it = bg.iterator();
			while(it.hasNext()){StdOut.print(it.next()+" ");}
			Ex_4_4_24 ob = new Ex_4_4_24(G,bg);
		}catch(Exception e){
			StdOut.println("Found exception: "+e.getMessage());
			e.printStackTrace();
		}
	}
	
	

}
