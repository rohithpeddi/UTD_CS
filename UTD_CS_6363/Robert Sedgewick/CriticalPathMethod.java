package ShortestPaths;

import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

/**********************************************
 * Critical Path Method for parallel precedence
 * constrained job scheduling 
 * 
 * Create an edge weighted DAG with source s and sink t
 * and two vertices for each job that has to be performed 
 * connect all start edges to source and end edges to sink
 * for constraints add zero weight edges from end to start
 * of two jobs.
 * 
 * Time : V+E (Longest Path method is used)
 * 
 **********************************************/

public class CriticalPathMethod {
	
	public static void main(String args[]){
		
		try{
			
			Scanner scan = new Scanner(new File("250verts.txt"));
			int N = Integer.parseInt(scan.nextLine());
			EdgeWeightedDigraph G = new EdgeWeightedDigraph(2*N+2);
			
			int s = 2*N, t = 2*N+1;
			
			for(int i=0; i<N; i++){
				
				String[] str = scan.nextLine().split(" ");
				double duration = Double.parseDouble(str[0]);
				G.addEdge(new DirectedEdge(s,i,0.0));
				G.addEdge(new DirectedEdge(i+N,t,0.0));
				G.addEdge(new DirectedEdge(i,i+N,duration));
				
				for(int j=1; j<str.length; j++){
					int successor = Integer.parseInt(str[i]);
					G.addEdge(new DirectedEdge(i+N,successor,0.0));
				}
			}			
			
			AcyclicLP lp = new AcyclicLP(G,s);
			
			StdOut.println("Start times:");
			for(int i=0; i<N; i++){
				StdOut.printf("%4d: %5.1f \n", i,lp.distTo(i));
			}
			
			StdOut.printf("Finish time: %5.1f \n", lp.distTo(t));
			
		} catch(Exception e){
			StdOut.println("Found exception:" + e.getMessage());
		}
		
	}

}
