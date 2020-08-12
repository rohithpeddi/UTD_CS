package MinimumSpanningTrees;

import java.awt.Color;
import java.util.Scanner;

import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

public class generateRandomEWG {
	
	private int V,E;
	public Bag<Edge>[] adj;
	
	/*************** CONSTRUCTOR ****************/
	//Calls random generator and draw graph
	
	public generateRandomEWG(int V, int E){
		this.V = V; this.E =E; 
		adj = (Bag<Edge>[]) new Bag[V];
		for(int i=0; i<V;i++)
			adj[i] = new Bag<Edge>();
		generateRandomEdges();
	}
	
	/*************** RANDOM EDGE GENERATOR ****************/
	//Generates random edges and adds them to the adjacency list of edges
	
	public void generateRandomEdges(){
		for(int i=0; i<E;i++){
			int v = StdRandom.uniform(0, V),w = StdRandom.uniform(0, V);
			double weight = StdRandom.uniform();
			Edge e = new Edge(v,w,weight);
			adj[v].add(e);adj[w].add(e);
		}
	}
	
	/*************** DRAW GRAPH ****************/
	//Draws the graph, thickness depends on the number of vertices connected to it
	
	public void drawEWG(){
		
		Point2D[] vertices = new Point2D[V];
		
		StdDraw.setPenRadius(.02); StdDraw.setPenColor(Color.BLUE);
		
		for(int i=0; i<V;i++){
			double x = (double)i/V;
			double y = (double)adj[i].size()/(V*V/2);
			vertices[i] = new Point2D(x,y);
			vertices[i].draw();
			StdDraw.text(x, y, "  "+i+"");
		}
		
		StdDraw.setPenRadius(.001); 
		
		for(int i=0; i<V; i++){
			for(Edge e:adj[i]){
				
				double x2 = (double)e.other(i)/V;
				double y2 = (double)adj[e.other(i)].size()/(V*V/2);
				
				double weight = e.weight();
				
				if(x2< vertices[i].x()){
					
					StdDraw.setPenRadius((1.0-weight)/100.0);				
					
					StdDraw.line(vertices[i].x(), vertices[i].y(), x2, y2);		
				}
			}
		}
		
	}
	
	/*************** UTILITY METHODS ****************/
	//Returns the number of edges and vertices 
	
	public int V(){return V;}
	public int E(){return E;}
	
	public Iterable<Edge> adj(int v){
		return adj[v];
	}
	
	public Iterable<Edge> edges(){
		Bag<Edge> edges = new Bag<Edge>();
		for(int i=0; i<V;i++){
			for(Edge e: adj[i]){
				int v = e.either(),w = e.other(v);
				if(v<w) edges.add(e);
			}
		}
		return edges;
	}
	
	/*************** MAIN METHOD ****************/
	
	
	public static void main(String args[]){
		
		int V=1,E=1;
		
		StdOut.println("Enter the values of vertices and edges");
		try{
			Scanner scan = new Scanner(System.in);
			V = scan.nextInt();E = scan.nextInt();			
		} catch(Exception e){
			StdOut.print(e.getMessage());
		}
		
		generateRandomEWG ob = new generateRandomEWG(V,E);
	}
	

}
