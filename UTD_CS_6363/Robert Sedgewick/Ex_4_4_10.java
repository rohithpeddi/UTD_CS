package ShortestPaths;

import java.io.File;
import java.math.BigDecimal;
import java.util.Scanner;
import java.util.Stack;

import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.SingleGraph;

import MinimumSpanningTrees.IndexMinPQ;
import edu.princeton.cs.algs4.StdOut;

public class Ex_4_4_10 {
	
	private double[] distTo;
	private IndexMinPQ<Double> pq;
	private int V,E;
	private EdgeWeightedDigraph G;
	private Stack<DirectedEdge> spt;
	
	public Ex_4_4_10(EdgeWeightedDigraph G, int s){
		
		distTo = new double[G.V()]; pq = new IndexMinPQ<Double>(G.V());
		spt = new Stack<DirectedEdge>(); this.G =G; this.V=G.V();this.E =G.E();
		
		for(int i=0; i<G.V(); i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		}
		distTo[s]=0.0;
		
		pq.insert(s, 0.0);
		while(!pq.isEmpty()){
			relax(G,pq.delMin());
		}
		
		findSPT();
	}
	
	private void findSPT(){
		for(int i=0; i<G.V(); i++){
			for(DirectedEdge e:G.adj(i)){
				int w = e.to();
				double diff = Math.abs(distTo[w]- distTo[i]);
				diff = Math.round(diff*100)/100.0;
				BigDecimal dc = new BigDecimal(diff+"");
				BigDecimal ec = new BigDecimal(e.weight()+"");
				StdOut.println("Entered: "+i+"-"+w+":"+dc+"-"+ec);
				if(dc.equals(ec)) spt.push(e);
			}
		}
	}
	
	public void printSPT(){
		
		Graph graph = new SingleGraph("SPT");
		graph.setStrict(false);
		graph.setAutoCreate( true );
		
		for(int i=0; i<G.V(); i++){
			for(DirectedEdge e:G.adj(i)){
				int v = e.from(),w = e.to();
				StdOut.println("Entered: "+i+"-"+w+":"+G.V());
				if(spt.contains(e)){
					graph.addEdge(v+""+w, v+"",w+"",true).addAttribute("ui.style", "fill-color:rgb(0,0,255);");
				} else {
					graph.addEdge(v+""+w, v+"",w+"",true).addAttribute("ui.style", "fill-color:rgb(0,0,0);");
				}
			}
		}
		
		for(Node n:graph) {
			n.addAttribute("ui.label", n.getId());
		}
		
		
		graph.display();
	}
	
	private void relax(EdgeWeightedDigraph G, int v){
		
		for(DirectedEdge e: G.adj(v)){
			int w = e.to();
			if(distTo[w]>distTo[v]+e.weight()){
				distTo[w]=distTo[v]+e.weight();
				if(pq.contains(w)) pq.change(w, distTo[w]);
				else pq.insert(w, distTo[w]);
			}
		}
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyEWD.txt"));
			EdgeWeightedDigraph G =new EdgeWeightedDigraph(scan);
			Ex_4_4_10 ob = new Ex_4_4_10(G,0);
			ob.printSPT();
		}catch(Exception e){
			StdOut.println("Found exception: "+e.getMessage());
			e.printStackTrace();
		}
	}

}
