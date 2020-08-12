package ShortestPaths;

import java.util.Stack;

/**********************************************
 * ACYCLIC LONGEST PATH
 * 
 * For edge weighted digraphs without cycles in it 
 * shortest path tree can be found in linear time
 * It also handles negative edges 
 * Also solves problems for longest paths (**)
 * 
 * Modified from AcyclicSP, by initialising all the 
 * values to negative infinity, and changing the relaxation 
 * criteria from greater to lesser !! 
 * 
 * Time : E+V  
 **********************************************/


public class AcyclicLP {
	
	private DirectedEdge[] edgeTo;
	private double[] distTo;
	
	public AcyclicLP(EdgeWeightedDigraph G, int s ){
		edgeTo = new DirectedEdge[G.V()]; distTo = new double[G.V()];
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.NEGATIVE_INFINITY;
		}
		distTo[s] =0.0;
		
		Topological top = new Topological(G);
		
		for(int v: top.order()){
			relax(G,v);
		}
		
	}
	
	public void relax(EdgeWeightedDigraph G, int v){
		
		for(DirectedEdge e: G.adj(v)){
			int w = e.to();
			if(distTo[w]< distTo[v]+e.weight()){				
				distTo[w]=distTo[v]+e.weight(); edgeTo[w] =e;			
			}
		}
		
	}
	
	public double distTo(int v){	return distTo[v];}
	
	public boolean hasPathTo(int v)	{	return distTo[v]>Double.NEGATIVE_INFINITY;}
	
	public Iterable<DirectedEdge> pathTo(int v){
		
		Stack<DirectedEdge> path = new Stack<DirectedEdge>();
		
		for(DirectedEdge e= edgeTo[v]; e!=null; e = edgeTo[e.from()]){
			path.push(e);
		}		
		
		return path;
	}
	
}
