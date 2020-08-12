package MinimumSpanningTrees;

import java.awt.Color;
import java.util.Scanner;

import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

public class EdgeWeightedGraph {
	
	private final int V;
	private int E;
	public Bag<Edge>[] adj;
	
	/*************** CONSTRUCTORS ****************/
	
	public EdgeWeightedGraph(int V){
		this.V = V; this.E =0;
		adj = (Bag<Edge>[]) new Bag[V];
		for(int i=0; i<V;i++)
			adj[i] = new Bag<Edge>();
	}
		
	public EdgeWeightedGraph(Scanner scan){
		this(Integer.parseInt(scan.nextLine()));
		int edges = Integer.parseInt(scan.nextLine());
		while(scan.hasNextLine()){
			String[] str = scan.nextLine().split(" ");
			int v = Integer.parseInt(str[0]), w = Integer.parseInt(str[1]);
			double weight = Double.parseDouble(str[2]);
			Edge e = new Edge(v,w,weight);
			addEdge(e);
		}
	}
	
	public EdgeWeightedGraph(generateRandomEWG G){
		this(G.V());
		this.adj = G.adj;
		this.E = G.E();
	}
	
	/*************** DELETE EDGE IMPLEMENTATION ****************/
	
	public void deleteEdge(Edge e){
		int v= e.either(),w = e.other(v);
		adj[v].delete(e); adj[w].delete(e);
	}
	
	/*************** ADD EDGE IMPLEMENTATION ****************/
	
	public void addEdge(Edge e){
		int v = e.either(), w = e.other(v);
		adj[v].add(e); adj[w].add(e);
		E++;
	}
	
	/*************** UTILITY METHODS ****************/
	
	public int V(){return V;}
	public int E(){return E;}
	
	public Iterable<Edge> adj(int v){
		return adj[v];
	}
	
	public Iterable<Edge> edges(){
		int count=0;
		Bag<Edge> edges = new Bag<Edge>();
		for(int i=0; i<V;i++){
			for(Edge e: adj[i]){
				int w = e.other(i);
				if(i<w) {edges.add(e);count++;}
			}
		}
		StdOut.println(count);
		return edges;
	}
	
	/*************** DRAW GRAPH ****************/
	//Draws the graph, thickness depends on the number of vertices connected to it
	
	public void drawEWG(){
		
		Point2D[] vertices = new Point2D[V];
		
		StdDraw.setPenRadius(.02); StdDraw.setPenColor(Color.BLUE);
		
		for(int i=0; i<V;i++){
			double x = (double)i/25.0;
			double y = (double)adj[i].size()/25.0;
			vertices[i] = new Point2D(x,y);
			vertices[i].draw();
		}
		
		StdDraw.setPenRadius(.001); 
		
		for(int i=0; i<V; i++){
			for(Edge e:adj[i]){
				
				double x2 = (double)e.other(i)/25.0;
				double y2 = (double)adj[e.other(i)].size()/25.0;
				
				double weight = e.weight();
				
				if(x2< vertices[i].x()){
					
					StdDraw.setPenRadius((1.0-weight)/100.0);				
					
					StdDraw.line(vertices[i].x(), vertices[i].y(), x2, y2);		
				}
			}
		}
		
	}
	
	public String toString(){
		String str= "";
		str += "Number of vertices: "+ V+", Number of edges: "+E+"\n";
		for(int i=0; i<V; i++){			
			str +=  i+":";
			for(Edge e: adj[i]){
				int w = e.other(i); double weight = e.weight();
				str += "- ("+w+","+weight+")";
			}			
			str+= "\n";			
		}		
		
		return str;
	}
 
}
