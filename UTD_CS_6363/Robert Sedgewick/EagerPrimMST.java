package MinimumSpanningTrees;

import java.util.Iterator;

import UndirectedGraphs.Queue;

public class EagerPrimMST {
	
	private Edge[] edgeTo;
	private double[] distTo;
	private boolean[] marked;
	private IndexMinPQ<Double> pq;
	
	public EagerPrimMST(EdgeWeightedGraph G){
		edgeTo = new Edge[G.V()]; distTo = new double[G.V()];marked = new boolean[G.V()];
		pq = new IndexMinPQ<Double>(G.V());
		for(int i=0; i<G.V(); i++)
			distTo[i] = Double.POSITIVE_INFINITY;
		
		distTo[0] = 0.0;
		pq.insert(0, 0.0);
		while(!pq.isEmpty())
			visit(G,pq.delMin());
		
	}
	
	public void visit(EdgeWeightedGraph G, int v){
		marked[v] =true;
		for(Edge e: G.adj(v)){
			int w = e.other(v);
			if(marked[w]) continue;
			
			if(e.weight()< distTo[w]) {
				edgeTo[w] = e; distTo[w] = e.weight();
				if(pq.contains(w)) pq.change(w, distTo[w]);
				else pq.insert(w, distTo[w]);
			}					
		}
	}
	
	
	public Iterable<Edge> edges(){
		Queue<Edge> mst = new Queue<Edge>();
		for(int i=0; i<marked.length; i++){
			if(marked[i]==true){
				mst.enqueue(edgeTo[i]);
			}
		}
		return mst;
	}
	
	public double weight(){
		double total_weight = 0.0;
		Iterable<Edge> mst_edges = edges();
		Iterator<Edge> it = mst_edges.iterator();
		while(it.hasNext()){
			Edge e = it.next();
			total_weight+= e.weight();
		}
		return total_weight;
	}
	
	
	

}
