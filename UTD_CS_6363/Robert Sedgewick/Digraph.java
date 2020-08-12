package DirectedGraphs;

import java.awt.Color;
import java.util.Scanner;
import java.util.Stack;

import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

public class Digraph {
	
	private int V,E;
	public Bag<Integer>[] adj;
	public int[] inDegree,outDegree;
	
	/************* CONSTRUCTOR **************/
	
	public Digraph(int cap){
		this.V = cap; 
		adj = (Bag<Integer>[]) new Bag[cap];
		inDegree = new int[cap]; outDegree = new int[cap];
		for(int i=0; i<V;i++)
			adj[i] = new Bag<Integer>();
	}
	
	public Digraph(Scanner scan){
		this(Integer.parseInt(scan.nextLine()));
		this.E = Integer.parseInt(scan.nextLine());
		while(scan.hasNextLine()){
			String[] st = scan.nextLine().split("  ");
			int v = Integer.parseInt(st[0]); int w = Integer.parseInt(st[1]);
			addEdge(v,w);
		}
		
	}
	
	/************* UTILITY METHODS **************/
	
	public int V(){return V;}
	public int E(){return E;}
	
	public Iterable<Integer> adj(int v){
		return adj[v];
	}
	
	public boolean hasEdge(int v, int w){
		for(int i:adj(v)){
			if(i==w) return true;
		}
		return false;
	}
	
	/************* ADDING EDGE - DISALLOWING PARALLEL EDGES AND SELF LOOPS **************/
	
	public void addEdge(int v, int w){
		if(v != w){
			if(adj[v].contains(w)){ return;}
			adj[v].add(w); 
			outDegree[v]++; inDegree[w]++;
		}
		else return;
	}
	
	/************* REVERSE DIGRAPH **************/
	
	public Digraph reverse(Digraph G){
		Digraph rev = new Digraph(G.V());
		
		for(int i=0; i<G.V;i++)
			for(int w:adj(i))
				rev.addEdge(w, i);
		
		return rev;
	}
	
	/************** GRAPH VISUALIZATION **********/
	
	public void drawGraph(){
		
		int max = V;
		Point2D[] vertices = new Point2D[V];
		StdDraw.setPenRadius(.025);
		for(int i=0; i<V;i++){
			StdDraw.setPenColor(Color.blue);
			double x = ((double)i / (double)V);
			double y = ((double)(adj[i].size()) / (double)V);
			vertices[i] = new Point2D(x,y);
			//if(inDegree[i]==0) {StdDraw.setPenColor(Color.GREEN);StdDraw.textLeft(x, y, " SOURCE");}
			//if(outDegree[i]==0) {StdDraw.setPenColor(Color.RED);StdDraw.textLeft(x, y, " SINK");}
			StdDraw.textLeft(x, y, " "+i);
			vertices[i].draw();
		}
		
		StdDraw.setPenRadius(.005);StdDraw.setPenColor();
		
		for(int i=0; i<V; i++){
			if(adj[i].size()>0){
				for(int w: adj(i)){
					StdDraw.line(vertices[i].x(), vertices[i].y(), vertices[w].x(), vertices[w].y());
				}
			}
		}
		
	}
	
	/************** SOURCES AND SINKS **********/
	
	public Iterable<Integer> sources(){
		Stack<Integer> source = new Stack<Integer>();
		for(int i=0; i<V;i++){
			if(inDegree[i]==0) source.push(i);
		}
		return source;
	}
	
	public Iterable<Integer> sinks(){
		Stack<Integer> sink = new Stack<Integer>();
		for(int i=0; i<V;i++){
			if(outDegree[i]==0) sink.push(i);
		}
		return sink;
	}

}
