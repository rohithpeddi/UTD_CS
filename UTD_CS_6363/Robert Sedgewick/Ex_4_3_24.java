package MinimumSpanningTrees;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;

import UndirectedGraphs.Queue;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

//Reverse delete algorithm 

public class Ex_4_3_24 {
	
	private boolean[] marked;
	private int V,E;
	private EdgeWeightedGraph G;
	private MaxPQ<Edge> pq;
	private boolean isCyclic;
	private Queue<Edge> mst;
	
	public Ex_4_3_24(EdgeWeightedGraph G){
		
		marked = new boolean[G.V()]; 
		this.V = G.V();this.E =G.E(); this.G =G;
				
		pq = new MaxPQ<Edge>(G.edges(),E);
		
		StdOut.println("Entering the DFS Cycle implementation:"+ G.V());
		
		reverseDelete();
		
		printmst();
	}
	
	public void printmst(){
		StdOut.println("Entered printmst");
		
		Iterable<Edge> edges = mst;
		Iterator<Edge> it = edges.iterator();
		while(it.hasNext()){
			Edge e = it.next();
			int v = e.either(),w = e.other(v);
			double x1 = (double)v/V;
			double y1 = (double)G.adj[v].size()/V;
			double x2 = (double)w/V;
			double y2 = (double)G.adj[w].size()/V;
			StdDraw.setPenRadius(0.01);
			Point2D x = new Point2D(x1,y1); x.draw();
			Point2D y = new Point2D(x2,y2); y.draw();
			StdDraw.setPenRadius((1.0-e.weight())/250.0);
			StdDraw.line(x1,y1, x2, y2);
			StdOut.println(e.either()+"-"+ e.other(e.either())+","+e.weight());
		}
		
	}
	
	// Max priority Queue implemented and delete operation is carried until
	// the PQ is empty, and checked for noncyclic natue of the edge - if yes then added to mst 
	
	public void reverseDelete(){
		
		StdOut.println("Entered reverse delete");
		
		mst = new Queue<Edge>();
		
		while(!pq.isEmpty()){
			
			Edge e = pq.delMax();
			if(noncyclic(e)) {mst.enqueue(e);}
			else {G.deleteEdge(e);}
		}
		
	}
	
	
	//Checking for noncyclic nature of an edge - it is a bridge or not, if bridge put it in the queue 
	// else remove that edge in the initial graph
	public boolean noncyclic(Edge e){
		
		StdOut.println("Entered noncyclic: "+ e.either()+"-"+ e.other(e.either()));
		
		isCyclic = false;
		flushMarked();
		int v = e.either(), w = e.other(v); 
		StdOut.println("Entering DFS");
		dfs(G,v,v,w);
		StdOut.println("Completed DFS: isCyclic-"+isCyclic);
		if(isCyclic) return false;
		else return true;
		
	}
	
	
	//Check whether a cycle exists with the particular edge 
	//Terminate the path from the particular edge and move back to the original index 
	public void dfs(EdgeWeightedGraph G, int v, int notfrom, int to){
		
		StdOut.println("DFS: v- "+ v+", notfrom: "+notfrom+", to: "+to);
		
		if(v == to){marked[v]= true; return;}
		
		marked[v]  =true;
		for(Edge e:G.adj(v)){
			int w = e.other(v);
			if(!marked[w]){
				dfs(G,w,notfrom,to);
				if(w == to) dfs(G,v,notfrom,to);
			} else if(w == to && v!= notfrom){
				isCyclic = true;
			} else {
				continue;
			}			
		}	
		
	}
	
	//flushes the entered marked indices by changing them to default
	public void flushMarked(){
		StdOut.println("Entering flushmarked");
		for(int i=0; i<G.V(); i++){
			StdOut.println("Entered:"+i);
			marked[i] = false;
		}		
		StdOut.println("Entering flushmarked");
	}
	
	public static void main(String args[]){
		try{
			Scanner scan =  new Scanner(new File("250verts.txt"));
			EdgeWeightedGraph G = new EdgeWeightedGraph(scan);
			Ex_4_3_24 ob = new Ex_4_3_24(G);			
			
		} catch(Exception e){
			StdOut.print("Exception: "+ e.getMessage());
		}
	}
	
}
