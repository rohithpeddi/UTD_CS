package DirectedGraphs;

public class TransitiveClosure {
	
	private DirectedDFS[] all;
	
	public TransitiveClosure(Digraph G){
		all = new DirectedDFS[G.V()];
		for(int i=0; i<G.V();i++)
			all[i] = new DirectedDFS(G,i);
	}
	
	public boolean reachable(int v, int w){
		return all[v].marked(w);
	}

}
