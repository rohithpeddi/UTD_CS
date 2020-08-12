package ShortestPaths;

/*********************************************************
 * FLOYD WARSHALL ALL PAIRS SP 
 * 
 * Define a distTo - nxn matrix and initialise all the 
 * non-diagonal values to infinity and diagonal values to 0.
 * and start relaxation in three nested loops
 * 
 * Outer loop goes from 1--> k ---> n
 * 	Middle loop goes from 1---> i ---> n
 * 	   Inner loop goes from 1---> j ---> n	
 * 
 ********************************************************/

public class FloydWarshall {
	
	private double[][] distTo;
	private DirectedEdge[][] edgeTo;
	private EdgeWeightedDigraph G;
	private boolean hasNegativeCycle;
	
	public FloydWarshall(EdgeWeightedDigraph G){
		
		distTo = new double[G.V()][G.V()]; this.G = G; edgeTo = new DirectedEdge[G.V()][G.V()];
		
		for(int i=0; i<G.V(); i++){
			for(int j=0; j<G.V(); j++){
				distTo[i][j] = Double.POSITIVE_INFINITY;
			}
		}
		
		for(int i=0; i<G.V(); i++){
			
			for(DirectedEdge e: G.adj(i)){
				int w = e.to();
				distTo[i][w] = e.weight();
				edgeTo[i][w] = e;
			}
			
		}
		

        // Floyd-Warshall updates
        for (int i = 0; i < G.V(); i++) {
            // compute shortest paths using only 0, 1, ..., i as intermediate vertices
            for (int v = 0; v < G.V(); v++) {
                if (edgeTo[v][i] == null) continue;  // optimization
                for (int w = 0; w < G.V(); w++) {
                    if (distTo[v][w] > distTo[v][i] + distTo[i][w]) {
                        distTo[v][w] = distTo[v][i] + distTo[i][w];
                        edgeTo[v][w] = edgeTo[i][w];
                    }
                }
                // check for negative cycle
                if (distTo[v][v] < 0.0) {
                    hasNegativeCycle = true;
                    return;
                }
            }
        }
			
		
		
	}

}
