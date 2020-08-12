package DirectedGraphs;

public class Topological {
	
	private Iterable<Integer> order;
	
	public Topological(Digraph G){
		
		DirectedCycle cyclefinder = new DirectedCycle(G);
		if(!cyclefinder.hasCycleDG()){
			DepthFirstOrder dfs = new DepthFirstOrder(G);
			order = dfs.reversePost();
		}
		
	}
	
	public Iterable<Integer> order(){
		return order;
	}
	
	public boolean isDAG(){
		return order == null;
	}
	
}
