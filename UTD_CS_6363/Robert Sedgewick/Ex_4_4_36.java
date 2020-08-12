package ShortestPaths;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;

import MinimumSpanningTrees.IndexMinPQ;
import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.StdOut;


/*****************************************************
 * NEIGHBOURS:
 * 
 * Implemented Dijkstra such that only those whose distances 
 * are less than 500 are allowed to be queued back in priority 
 * queue. 
 * 
 * 
 *****************************************************/

public class Ex_4_4_36 {
	
	private double[] distTo;
	private IndexMinPQ<Double> pq;
	private Bag<Integer> neighbours;
	private int range;
	
	public Ex_4_4_36(EdgeWeightedDigraph G, int s, int d){
		
		distTo = new double[G.V()]; pq = new IndexMinPQ<Double>(G.V());this.range =d;
		neighbours = new Bag<Integer>();
		
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		} 
		distTo[s] =0;
		
		pq.insert(s, 0.0);
		
		StdOut.println("Initialized constructor!");
		
		while(!pq.isEmpty()){
			relax(G,pq.delMin());
		}		
		
		StdOut.println("Done construction!");
		
		printVerts();
		
	}
	

	public void relax(EdgeWeightedDigraph G, int v){
		
		if(distTo[v]>range) return;
		
		for(DirectedEdge e: G.adj(v)){
			//StdOut.println("Entered: "+v);
			int w = e.to();
			if(distTo[w]> distTo[v]+e.weight()){	
				
				distTo[w]=distTo[v]+e.weight(); 
				//StdOut.println(v+":"+w+":"+distTo[w]);
				if(distTo[w]>range) continue;
				if(pq.contains(w)) pq.change(w, distTo[w]);
				else pq.insert(w, distTo[w]);
				
				if(!neighbours.contains(w)) neighbours.add(w);
				
			}
			
		}
		
	}
	
	public void printVerts(){
		Iterator<Integer> it= neighbours.iterator();
		while(it.hasNext()){
			StdOut.print(it.next()+" ");
		}
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("rome.txt"));
			EdgeWeightedDigraph G = new EdgeWeightedDigraph(scan);
			Ex_4_4_36 ob = new Ex_4_4_36(G,71,701);
			
		}catch(Exception e){
			StdOut.println("Found Exception: "+e.getMessage());
			e.printStackTrace();
		}
	}
	
}
