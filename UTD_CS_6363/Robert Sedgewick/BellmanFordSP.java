package ShortestPaths;

import java.util.Stack;

import DirectedGraphs.DirectedCycle;
import UndirectedGraphs.Queue;
import edu.princeton.cs.algs4.StdOut;

/*********************************************************
 * BELLMAN FORD ALGORITHM FOR SHORTEST PATHS - QUEUE BASED
 * 
 * with the variaable cost we are measuring how frequently 
 * relax operation is being performed and at regular intervals 
 * it is checked for finding a negative cycle 
 * 
 * Time : EV 
 * Space : V (worst case)
 * Restriction : No negative cycles 
 *********************************************************/

public class BellmanFordSP {
	
	public double[] distTo;
	private DirectedEdge[] edgeTo;
	private Queue<Integer> queue;
	private boolean[] onQ;
	private int cost;
	private Iterable<DirectedEdge> cycle;
	
	public BellmanFordSP(EdgeWeightedDigraph G, int s){
		StdOut.println("Entered constructor");
		distTo = new double[G.V()]; edgeTo = new DirectedEdge[G.V()]; onQ = new boolean[G.V()];
		queue = new Queue<Integer>();cost =0; 
		
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		}
		distTo[s] = 0.0; onQ[s] = true;
		StdOut.println("Done Initialization!");
		
		queue.enqueue(s);
		
		while(!queue.isEmpty() && !this.hasNegativeCycle()){
			int v = queue.dequeue();
			onQ[v] = false;
			relax(G,v);
		}
		
	}
	
	public void relax(EdgeWeightedDigraph G, int v){
		//StdOut.println("Entered relax:"+ v);
		for(DirectedEdge e:G.adj(v)){
			int w = e.to();			
			if(distTo[w]> distTo[v]+e.weight()){
				//StdOut.println("distTo[v]: "+ distTo[v]);
				distTo[w]= distTo[v]+e.weight();
				//StdOut.println("distTo[w]: "+ distTo[w]+":"+v+","+w);
				edgeTo[w] = e;				
				if(!onQ[w]){
					queue.enqueue(w);
					onQ[w]=true;
				}				
			}			
			if(cost++ % G.V() ==0){
				findNegativeCycle();
			}			
		}		
	}
	
	public void findNegativeCycle(){
		//StdOut.println("Entered findNegativeCycle");
		int V = edgeTo.length;
		EdgeWeightedDigraph spt = new EdgeWeightedDigraph(V);
		
		for(int i=0; i<V; i++){
			if(edgeTo[i]!=null){
				spt.addEdge(edgeTo[i]);
			}
		}
		
		DirectedCycle cyclefinder = new DirectedCycle(spt);
		
		if(cyclefinder.hasCycleEWDG()){ cycle = cyclefinder.cycleEWDG();StdOut.println(spt.toString());}
	}
	
	public boolean hasNegativeCycle(){
		return cycle != null;
	}
	
	public Iterable<DirectedEdge> negativeCycle(){
		return cycle;
	}
	
	public double distTo(int v){
		return distTo[v];
	}
	
	public boolean hasPathTo(int v){
		return distTo[v]<Double.POSITIVE_INFINITY;
	}
	
	public Iterable<DirectedEdge> pathTo(int v){
		Stack<DirectedEdge> path = new Stack<DirectedEdge>();
		
		for(DirectedEdge e= edgeTo[v]; e!=null; e = edgeTo[e.from()]){
			path.push(e);
		}		
		
		return path;
	}

}
