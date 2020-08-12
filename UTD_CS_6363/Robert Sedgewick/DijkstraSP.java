package ShortestPaths;

import java.util.Stack;

import MinimumSpanningTrees.IndexMinPQ;
import UndirectedGraphs.Bag;

/*************************************************
 * DIJKSTRA ALGORITHM
 * 
 * To compute the shortest path tree in a 
 * edge weighted digraph with V vertices and E edges(non-negative)
 * 
 * Time : ElogV (worst case) 
 * Space : V 
 * 
 * For maintaining an IndexMin Priority Queue
 *************************************************/

public class DijkstraSP {
	
	private DirectedEdge[] edgeTo;
	private double[] distTo;
	private IndexMinPQ<Double> pq;

	
	public DijkstraSP(EdgeWeightedDigraph G, int s){
		edgeTo = new DirectedEdge[G.V()]; distTo = new double[G.V()]; pq = new IndexMinPQ<Double>(G.V());
		
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		} 
		distTo[s] =0;
		
		pq.insert(s, 0.0);
		
		while(!pq.isEmpty()){
			relax(G,pq.delMin());
		}		
	}
	
	public void relax(EdgeWeightedDigraph G, int v){
		
		for(DirectedEdge e: G.adj(v)){
			int w = e.to();
			
			if(distTo[w]> distTo[v]+e.weight()){
				
				distTo[w]=distTo[v]+e.weight(); edgeTo[w]=e;
				if(pq.contains(w)) pq.change(w, distTo[w]);
				else pq.insert(w, distTo[w]);
				
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
