package ShortestPaths;

import java.util.Iterator;
import java.util.Stack;

import MinimumSpanningTrees.IndexMinPQ;

/******************************************************
 *	Shortest path between two subsets of vertices 
 *	consider the subset of vertices - 
 *
 *	Add two new vertices - source and a sink 
 *	Add a zero weighted edge from each vertex in one subset to 
 *	source and also from each vertex in other set to a sink 
 *
 *	Then determine the shortest path from source to the sink using Dijkstra
 *	Time: O(ElogV)
 *
 ******************************************************/

public class Ex_4_4_25 {
	
	private double[] distTo; 
	private DirectedEdge[] edgeTo;
	private IndexMinPQ<Double> pq;
	private int V;
	
	public Ex_4_4_25(EdgeWeightedDigraph G, Iterable<Integer> S, Iterable<Integer> T){
		
		distTo = new double[G.V()+2]; pq = new IndexMinPQ<Double>(G.V()+2); this.V =G.V();
		edgeTo = new DirectedEdge[V+2];
		
		Iterator<Integer> itS = S.iterator(); Iterator<Integer> itT = T.iterator();
		
		int source = V, sink = V+1;  
		
		while(itS.hasNext()){
			int v = itS.next();
			DirectedEdge e = new DirectedEdge(source,v,0.0);
			G.addEdge(e);
		}
		
		while(itT.hasNext()){
			int v = itT.next();
			DirectedEdge e = new DirectedEdge(v,sink,0.0);
			G.addEdge(e);
		}
		
		for(int i=0; i<V+2; i++){
			distTo[i]= Double.POSITIVE_INFINITY;
		}
		
		distTo[V]=0.0;
		
		pq.insert(source, 0.0);
		
		while(!pq.isEmpty()){
			relax(G,pq.delMin());
		}
		
	}
	
	private void relax(EdgeWeightedDigraph G, int v){
		
		for(DirectedEdge e: G.adj(v)){
			
			int w = e.to();
			if(distTo[w]>distTo[v]+e.weight()){
				distTo[w]=distTo[v]+e.weight(); edgeTo[w]=e;
				if(pq.contains(w)){ pq.change(w, distTo[w]);}
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
