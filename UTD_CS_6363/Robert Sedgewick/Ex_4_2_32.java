package DirectedGraphs;

import java.awt.Color;
import java.util.Scanner;

import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

//Random Digraphs 

public class Ex_4_2_32 {
	
	private int V,E;
	private Bag<Integer>[] adj;
	
	public void init(int V, int E){
		
		if(E<0 || E> V*(V-1)){
			StdOut.print("Check your input for edges it is exceeding the limit");
			return;
		}
		
		adj =(Bag<Integer>[]) new Bag[V];
		for(int i=0; i<V; i++){
			adj[i] =  new Bag<Integer>();
		}
		
		this.V = V; this.E = E;
		
		for(int i=0;i<E;i++){
			int v = StdRandom.uniform(0, V);
			int w = StdRandom.uniform(0, V);
			StdOut.println("Adding edges: "+ v+","+w);
			addEdge(v,w);
		}
		
	}
	
	public void addEdge(int v, int w){
		if(v==w) return;
		if(adj[v].contains(w)) return;
		adj[v].add(w);
	}
	
	public void drawGraph(){
		int max = V;
		Point2D[] vertices = new Point2D[V];
		StdDraw.setPenRadius(.025);
		for(int i=0; i<V;i++){
			StdDraw.setPenColor(Color.blue);
			double x = ((double)i / (double)V);
			double y = ((double)(adj[i].size()) / (double)V);
			vertices[i] = new Point2D(x,y);
			StdDraw.textLeft(x, y, " "+i);
			vertices[i].draw();
		}
		
		StdDraw.setPenRadius(.005);StdDraw.setPenColor();
		
		for(int i=0; i<V; i++){
			if(adj[i].size()>0){
				for(int w: adj[i]){
					StdDraw.line(vertices[i].x(), vertices[i].y(), vertices[w].x(), vertices[w].y());
				}
			}
		}
	}
	
	public static void main(String args[]){
		Scanner scan = new Scanner(System.in);
		StdOut.println("Enter the values for vertices and edges");
		int v = scan.nextInt(); int e = scan.nextInt();
		Ex_4_2_32 ob = new Ex_4_2_32();
		ob.init(v, e);
		ob.drawGraph();
	}

}
