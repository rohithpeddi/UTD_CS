package DirectedGraphs;

//Solves the problem of reachability

public class DirectedDFS {
	
	public boolean[] marked;
	
	/************* CONSTRUCTORS **************/
	//For a single source
	public DirectedDFS(Digraph G, int s){
		marked = new boolean[G.V()];
		dfs(G,s);
	}
	//For a list of sources
	public DirectedDFS(Digraph G, Iterable<Integer> sources){
		marked = new boolean[G.V()];
		for(int s:sources)
			if(!marked[s]) dfs(G,s);
	}
	
	/************* DEPTH FIRST SEARCH FOR DIGRAPH **************/
	
	public void dfs(Digraph G, int v){
		marked[v] = true;
		for(int w: G.adj(v))
			if(!marked[w]) dfs(G,w);
	}
	
	/************* UTILITY METHODS **************/
	
	public boolean marked(int v){
		return marked[v];
	}

}
