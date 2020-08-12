package ShortestPaths;

import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

/***********************************************
 * ARBITRAGE:
 * 
 * Negative cycle detection problem in edge weighted digraphs
 * 
 * 
 ***********************************************/

public class Arbitrage {
	
	public static void main(String args[]){
		
		try{
			Scanner scan = new Scanner(new File("rates.txt"));
			int V = Integer.parseInt(scan.nextLine());
			String[] name = new String[V];
			StdOut.println("V:"+V);
			EdgeWeightedDigraph G = new EdgeWeightedDigraph(V);
			
			for(int i=0; i<V; i++){				
				String[] str = scan.nextLine().split("  ");
				name[i] = str[0];
				StdOut.println("name[]:"+name[i]);
				for(int j=1; j<str.length; j++){
					double rate = Double.parseDouble(str[j]);
					DirectedEdge e = new DirectedEdge(i,j-1, - Math.log(rate));
					G.addEdge(e);
				}
				
			}
			
			StdOut.println("Done with creation of graph");
			BellmanFordSP sp = new BellmanFordSP(G,0);
			StdOut.println("Bellman- Ford is run on the graph");
			if(sp.hasNegativeCycle()){
				double stake =1000.0;
				
				for(DirectedEdge e: sp.negativeCycle()){
					StdOut.printf("%10.5f %s", stake, name[e.from()]);
					stake*= Math.exp(-e.weight());
					StdOut.printf(" = %10.5f %s \n", stake,name[e.to()]);
				}
				
			}
			else {
				StdOut.println("No arbitrage opportunity");
			}
			
		} catch (Exception e){
			StdOut.println("Found exception"+e.getMessage());
		}
		
		
	}

}
