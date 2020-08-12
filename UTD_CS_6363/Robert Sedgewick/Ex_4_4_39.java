package ShortestPaths;

import java.util.Stack;

import MinimumSpanningTrees.IndexMinPQ;
import MinimumSpanningTrees.MinPQ;

/*******************************************************
 * LAZY DIJKSTRA SP
 * 
 * Instead of using Index Min priority queue we use 
 * normal priority queue and a marked function to verify
 * whether a particular edge is relaxed or not 
 * 
 ******************************************************/

public class Ex_4_4_39 {
	
	private DirectedEdge[] edgeTo;
	private double[] distTo;
	private MinPQ<DirectedEdge> pq;
	private boolean[] marked;

	
	public Ex_4_4_39(EdgeWeightedDigraph G, int s){
		edgeTo = new DirectedEdge[G.V()]; distTo = new double[G.V()]; 
		pq = new MinPQ<DirectedEdge>(G.E()); marked = new boolean[G.V()];
		
		
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		} 
		distTo[s] =0;
		relax(G,s);
		
		while(!pq.isEmpty()){
			
			DirectedEdge e = pq.delMin();
			int w = e.to();
			if(!marked[w]) relax(G, w);
			
		}
		
				
	}
	
	  private void relax(EdgeWeightedDigraph G, int v) {
	        marked[v] = true;
	        for (DirectedEdge e : G.adj(v)) {
	            int w = e.to();
	            if (distTo[w] > distTo[v] + e.weight()) {
	                distTo[w] = distTo[v] + e.weight();
	                edgeTo[w] = e;
	                pq.insert(e);
	            }
	        }
	  }
	
	public double distTo(int v){ return distTo[v];}
	
	public boolean hasPathTo(int v){
		return distTo[v]<Double.POSITIVE_INFINITY;
	}
	
	public Stack<DirectedEdge> pathTo(int v){
		
		if(!hasPathTo(v)) return null;
		
		Stack<DirectedEdge> path = new Stack<DirectedEdge>();
		for(DirectedEdge e = edgeTo[v]; e != null; e = edgeTo[e.from()]){
			path.push(e);
		}
		
		return path;
		
	}

}
