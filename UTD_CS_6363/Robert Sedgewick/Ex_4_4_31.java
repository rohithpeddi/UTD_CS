package ShortestPaths;

import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.SingleGraph;

import MinimumSpanningTrees.IndexMinPQ;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

public class Ex_4_4_31 {
	
	private int[] vertorder;
	private double[] distTo;
	private IndexMinPQ<Double> pq;
	
	public Ex_4_4_31(int cap){
		
		vertorder = new int[cap]; distTo = new double[cap];
		for(int i=0; i<cap; i++){
			vertorder[i]=i; distTo[i] = Double.POSITIVE_INFINITY;
		}
		
		StdRandom.shuffle(vertorder);
		
		EdgeWeightedDigraph G = new EdgeWeightedDigraph(cap);
		
		for(int i=0; i<cap-1; i++){			
			DirectedEdge e = new DirectedEdge(vertorder[i],vertorder[i+1],StdRandom.random());
			//StdOut.println(vertorder[i]+":"+vertorder[i+1]+":"+e.weight());
			G.addEdge(e);
		}
		
		printGraph();
		
		distTo[vertorder[0]] = 0.0;
		
		for(int i=0; i<cap-1; i++){
			relax(G,vertorder[i]);
		}
		
	}
	
	public void relax(EdgeWeightedDigraph G, int v){
		//StdOut.println("Entered relax: "+ v+distTo[v]);
		for(DirectedEdge e: G.adj(v)){
			int w = e.to();
			if(distTo[w]> distTo[v]+e.weight()){				
				distTo[w]=distTo[v]+e.weight(); 		
			}
		}
		
	}
	
	private void printGraph(){
		Graph graph = new SingleGraph("LineGraph");
		graph.setStrict(false);
		graph.setAutoCreate( true );
		
		for(int i=0; i<distTo.length-1; i++){
			graph.addEdge(vertorder[i]+""+vertorder[i+1],vertorder[i]+"" , ""+vertorder[i+1],true).addAttribute("ui.label", vertorder[i]+""+vertorder[i+1]);;
		}
		
		for(Node node:graph){
			node.addAttribute("ui.label", node.getId());
		}
		
		graph.display();
	}
	
	public double dist(int i, int j){
		return Math.abs(distTo[i]-distTo[j]);
	}
	
	public static void main(String args[]){
		try{
		Ex_4_4_31 ob = new Ex_4_4_31(10);
		StdOut.println(ob.dist(5,6));	
		} catch(Exception e){
			StdOut.println("Found Exception: "+ e.getMessage());
			e.printStackTrace();
		}
	}
	

}
