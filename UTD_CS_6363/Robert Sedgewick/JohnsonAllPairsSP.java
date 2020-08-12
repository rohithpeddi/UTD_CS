package ShortestPaths;

public class JohnsonAllPairsSP {
	
	private DijkstraSP[] all;
	private EdgeWeightedDigraph Grew;
	private BellmanFordSP spt;
	private double[] distTo;
	
	public JohnsonAllPairsSP(EdgeWeightedDigraph G){
		
		all = new DijkstraSP[G.V()]; Grew = new EdgeWeightedDigraph(G.V());
		spt = new BellmanFordSP(G,0);
		distTo = spt.distTo;
		
		for(int i=0; i<G.V(); i++){
			
			for(DirectedEdge e:G.adj(i)){
				int w = e.to();
				double weightModified = e.weight()+distTo[i]-distTo[w];
				DirectedEdge ed = new DirectedEdge(i,w,weightModified);
				Grew.addEdge(ed);
			}
			
		}
		
		for(int i=0; i<G.V(); i++){
			all[i] = new DijkstraSP(Grew,i);
		}
		
	}
	
	public static void main(String args[]){
		
	}

}
