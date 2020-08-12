package MinimumSpanningTrees;

import java.awt.Color;
import java.util.Iterator;
import java.util.Scanner;

import UndirectedGraphs.Queue;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

public class LazyPrimMST {
	
	public boolean[] marked;
	public Queue<Edge> mst;
	public MinPQ<Edge> pq;
	
	public LazyPrimMST(EdgeWeightedGraph G){
		marked = new boolean[G.V()];
		mst = new Queue<Edge>(); pq = new MinPQ<Edge>(G.E());
		
		visit(G,0);
		
		while(!pq.isEmpty()){
			Edge e = pq.delMin();
			int v = e.either(), w = e.other(v);
			if(marked[v] && marked[w]) continue;
			mst.enqueue(e);
			if(!marked[w]) visit(G,w);
			if(!marked[v]) visit(G,v);
		}
		
		drawGraph(G);
		
	}
	
	public void visit(EdgeWeightedGraph G, int v){
		marked[v] = true; 
		for(Edge e:G.adj(v)){
			int w = e.other(v);
			if(!marked[w]) pq.insert(e);			
		}
	}
	
	public Iterable<Edge> edges(){return mst;}
	
	public double weight(){
		double total_weight = 0.0;
		Iterable<Edge> mst_edges = edges();
		Iterator<Edge> it = mst_edges.iterator();
		while(it.hasNext()){
			Edge e = it.next();
			total_weight+= e.weight();
		}
		return total_weight;
	}
	
	public void drawGraph(EdgeWeightedGraph G){
		int V = G.V();
		Iterable<Edge> mst_edges = edges();
		Iterator<Edge> it = mst_edges.iterator();
		StdDraw.setPenColor(Color.green);
		while(it.hasNext()){
			Edge e = it.next();
			int v = e.either();
			int w = e.other(v);
			double x1 = (double)v/V;
			double y1 = (double)G.adj[v].size()/V;
			double x2 = (double)w/V;
			double y2 = (double)G.adj[w].size()/V;
			StdDraw.setPenRadius((1.0-e.weight())/250.0);
			
			StdDraw.line(x1,y1, x2, y2);
		}
	}
	
	public static void main(String args[]){
		int V=1,E=1;
		
		StdOut.println("Enter the values of vertices and edges");
		try{
			Scanner scan = new Scanner(System.in);
			V = scan.nextInt();E = scan.nextInt();			
		} catch(Exception e){
			StdOut.print(e.getMessage());
		}
		
		generateRandomEWG G = new generateRandomEWG(V,E);
		G.drawEWG();
		EdgeWeightedGraph ewg = new EdgeWeightedGraph(G);
		LazyPrimMST ob = new LazyPrimMST(ewg);
	}
}


