package DirectedGraphs;

import UndirectedGraphs.Queue;

public class DirectedPaths {
	
	public boolean[] marked;
	public int[] edgeTo;
	
	/************** CONSTRUCTOR ****************/
	
	//Default Digraph returns the DepthFirst path
	public DirectedPaths(Digraph G){
		marked = new boolean[G.V()]; edgeTo = new int[G.V()];
		for(int i=0; i<G.V();i++){
			if(!marked[i]) dfs(G,i);
		}
	}
	
	//Constructor with any string specified other than DEPTH gives 
	//Breadth first shortest path 
	public DirectedPaths(Digraph G, String st){
		if(st.equals("DEPTH")){
			marked = new boolean[G.V()]; edgeTo = new int[G.V()];
			for(int i=0; i<G.V();i++){
				if(!marked[i]) dfs(G,i);
			}
		} else {
			marked = new boolean[G.V()]; edgeTo = new int[G.V()];
			for(int i=0; i<G.V();i++){
				if(!marked[i]) bfs(G,i);
			}
		}
	}
	
	/************** DEPTH FIRST PATH ****************/
	
	public void dfs(Digraph G, int v){
		marked[v] = true;
		for(int w:G.adj(v))
			if(!marked[w]) {
				edgeTo[w]=v;
				dfs(G,w);
			}
	}
	
	/************** BREADTH FIRST PATH ****************/
	
	public void bfs(Digraph G, int u){
		Queue<Integer> q = new Queue<Integer>();
		q.enqueue(u);marked[u]= true;
		while(!q.isEmpty()){
			int v = q.dequeue(); 
			marked[v]= true;
			for(int w:G.adj(v)){
				if(!marked[w]){
					edgeTo[w]=v;
					q.enqueue(w);
				}
			}				
		}
	}
	

}
