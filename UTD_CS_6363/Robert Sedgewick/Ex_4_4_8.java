package ShortestPaths;

import java.io.File;
import java.util.Scanner;
import java.util.Stack;

import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.StdOut;

public class Ex_4_4_8 {
	
	private DijkstraSP[] all;
	
	public Ex_4_4_8(EdgeWeightedDigraph G){
		all = new DijkstraSP[G.V()];
		
		for(int i=0; i<G.V(); i++){
			all[i] = new DijkstraSP(G,i);
		}
		double max= Double.NEGATIVE_INFINITY;
		
		for(int i=0; i<G.V(); i++){
			for(int j=0; j<G.V(); j++){
				Stack<DirectedEdge> bg= all[i].pathTo(j);
				if(bg.size()>max) max = bg.size();
			}
		}
		
		StdOut.println("Diameter: "+max);
			
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyEWD.txt"));
			EdgeWeightedDigraph G =new EdgeWeightedDigraph(scan);
			Ex_4_4_8 ob = new Ex_4_4_8(G);
		}catch(Exception e){
			StdOut.println("Found exception: "+e.getMessage());
			e.printStackTrace();
		}
	}

}
