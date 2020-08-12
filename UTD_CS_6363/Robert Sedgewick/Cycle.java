//Differentiate Graph processing alorithms for graph creation algorithms
//To test whether a graph is acyclic

public class Cycle {
	
	private boolean[] marked;
	private boolean hasCycle;
	
	/*************** CONSTRUCTOR ****************/
	
	public Cycle(Graph G){
		marked = new boolean[G.V()];
		for(int v=0; v<G.V(); v++)
			if(!marked[v]) dfs(G,v,v);
	}
	
	//If w!=u and is marked, it conveys the presence of an inner loop 
	// If 1--2 then here u will be 2 and v is 1, w are vertices adjacent to v 
	// If w is only 2 i,e u then no cycle is formed but if it is other than 2 signifies the presence of cycle somewhere
	
	/*************** DEPTH FIRST SEARCH + hasCycle IMPLEMENTATION ****************/
	
	public void dfs(Graph G, int v, int u){
		marked[v] = true;
		for(int w:G.adj(v)){
			if(!marked[w]) 
				dfs(G,w,v);
			else if(w!=u) hasCycle =true;
		}			
	}
	
	/*************** UTILITY METHODS ****************/
	
	public boolean hasCycle(){
		return hasCycle;
	}

}
