//For finding the number of connected components in the graph
public class CC {
	
	private boolean[] marked;
	private int[] id;
	private int count;
	
	/*************** CONSTRUCTOR ****************/
	
	public CC(Graph G){
		marked = new boolean[G.V()]; id = new int[G.V()];
		for(int v=0; v<G.V();v++){
			if(!marked[v]){
				dfs(G,v); count++;
			}
		}
	}
	
	/*************** DEPTH FIRST SEARCH + ID IMPLEMENTATION ****************/
	
	public void dfs(Graph G, int v){
		marked[v] = true; id[v] = count;
		for(int w:G.adj(v)){
			if(!marked[w]){
				dfs(G,w);
			}
		}		
	}
	
	/*************** UTILITY METHODS ****************/
	
	public int id(int v){return id[v];}
	
	public boolean connected(int v, int w){return id[v]==id[w];}
	
	public int count(){return count;}

}
