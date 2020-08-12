package ShortestPaths;

public class DijkstraAllPairsSP {
	
	private DijkstraSP[] all;
	
	public DijkstraAllPairsSP(EdgeWeightedDigraph G){
		
		all = new DijkstraSP[G.V()];
		
		for(int i=0; i<G.V(); i++){
			all[i] = new DijkstraSP(G,i);
		}
		
	}
	
	public Iterable<DirectedEdge> path(int s, int t){
		return all[s].pathTo(t);
	}
	
	public double distTo(int s, int t){
		return all[s].distTo(t);
	}

}
