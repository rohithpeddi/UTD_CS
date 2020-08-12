package ShortestPaths;

import MinimumSpanningTrees.IndexMinPQ;

//Source sink shortest paths 

public class Ex_4_4_23 {
	
	private double[] distTo;
	private int V,E;
	private IndexMinPQ<Double> pq;
	private int source,sink;
	private int[] inDegree,outDegree;
	
	public Ex_4_4_23(EdgeWeightedDigraph G){
		distTo = new double[G.V()]; this.V =G.V(); pq = new IndexMinPQ<Double>(G.V());
		
		findPoles(G);
		
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		}
		
		distTo[source] = 0.0;
		
		pq.insert(source, 0.0);
		
		while(!pq.isEmpty()){
			relax(G,pq.delMin());
		}
		
	}
	
	private void findPoles(EdgeWeightedDigraph G){
		inDegree = new int[G.V()]; outDegree = new int[G.V()];
		
		for(int i=0; i<G.V(); i++){
			
			for(DirectedEdge e: G.adj(i)){
				int w = e.to();
				outDegree[i]++; inDegree[w]++; 
			}
			
		}
		
		for(int i=0; i<G.V(); i++){
			if(inDegree[i]==0 && outDegree[i]!=0 ) source = i;
			if(inDegree[i]!=0 && outDegree[i]==0 ) sink = i;
		}
			
		
	}
	
	private void relax(EdgeWeightedDigraph G, int v){
		
		for(DirectedEdge e: G.adj(v)){
			int w = e.to();
			if(distTo[w]>distTo[v]+e.weight()){
				distTo[w]=distTo[v]+e.weight();
				if(pq.contains(w)) pq.change(w, distTo[w]);
				else pq.insert(w, distTo[w]);
			}
		}
		
	}

}
