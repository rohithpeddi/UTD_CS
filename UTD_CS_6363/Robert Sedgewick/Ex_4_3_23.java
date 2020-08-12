package MinimumSpanningTrees;

import UndirectedGraphs.Queue;

//Forms a cycle and deletes the maximum weight edge in that cycle 
//Add edge and check whether a cycle is formed by it each time - if a cycle is formed 
//delete the maximum edge and start adding again.

//----> For checking circularity condition ---> check Ex_4_3_24

public class Ex_4_3_23 {
	
	private int[] edgeTo;
	private boolean[] marked;
	private int V,E;
	private Queue<Edge> mst;
	private EdgeWeightedGraph G;
	
	public Ex_4_3_23(EdgeWeightedGraph G){
		edgeTo = new int[G.V()]; marked = new boolean[G.V()];
		this.V =G.V(); this.E = G.E();
		mst = new Queue<Edge>();
		
		for(int i=0; i<V; i++){
			if(!marked[i]) dfs(G,i);
		}
		
	}
	
	public void dfs(EdgeWeightedGraph G, int v){
		
		marked[v] = true;
		for(Edge e:G.adj(v)){
			int w = e.other(v);
			if(!marked[w]){
				edgeTo[w] = v; dfs(G,w);
				mst.enqueue(e);
			} else if(marked[w]){
				delMaxWeightEdge(v,w);
			}
			
		}
		
	}
	
	public Edge getEdge(int v, int w){
		
		for(Edge e:G.adj(v)){
			int p = e.other(v);
			if(p==w) return e;
		}
		return null;
	}
	
	public void delMaxWeightEdge(int v, int w){
		
		Queue<Edge> path = new Queue<Edge>();
		
		for(int i=w; i!=v;i=edgeTo[i]){
			path.enqueue(getEdge(i,edgeTo[i]));
		}
		
		Edge last = getEdge(v,w);
		path.enqueue(last);
		
		MaxPQ<Edge> pq = new MaxPQ<Edge>(path, path.size());
		Edge delete = pq.delMax();		
		
		
		deleteEdge(delete);
		
	}
	
	public void deleteEdge(Edge e){
		
	}

}
