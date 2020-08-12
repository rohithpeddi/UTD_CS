package ShortestPaths;

import java.util.Scanner;

import MinimumSpanningTrees.IndexMinPQ;

// Weights on vertices not on edges - so convert them into weights on edges corresponding

public class Ex_4_4_22 {
	
	private double[] distTo;
	private IndexMinPQ<Double> pq;
	private int V,E;
	private EdgeWeightedDigraph G;
	private double[] vweight;
	
	//Takes from a file respective vertex weights and also directed edges 
	// and constructs a new Digraph with the following vertices and edges given 
	
	public Ex_4_4_22(Scanner scan){
		
		int V = Integer.parseInt(scan.nextLine());
		vweight = new double[V]; 
		
		distTo = new double[V]; this.V =V; pq = new IndexMinPQ<Double>(V);
		
		for(int i=0; i<V; i++){			
			String[] str = scan.nextLine().split(" "); 
			vweight[i] = Double.parseDouble(str[1]);
		}
		
		EdgeWeightedDigraph Gr = new EdgeWeightedDigraph(V);
		
		while(scan.hasNextLine()){
			String[] st = scan.nextLine().split(" ");
			int v = Integer.parseInt(st[0]),w = Integer.parseInt(st[1]); 
			
			DirectedEdge e = new DirectedEdge(v,w,vweight[v]+vweight[w]);
			G.addEdge(e);			
		}
		
		this.G =Gr;
		
		runSPT(Gr);
		
	}
	
	private void runSPT(EdgeWeightedDigraph G){
		
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		}
		
		distTo[0] =0.0;
		pq.insert(0, 0.0);
		
		while(!pq.isEmpty()){
			relax(G,pq.delMin());
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
