package ShortestPaths;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;

import MinimumSpanningTrees.IndexMinPQ;
import edu.princeton.cs.algs4.StdOut;

/******************************************************
 * CRITICAL EDGES:
 * 
 * Find the shortest path - take each edge in the path 
 * then run Dijkstra over it to get the shortest path
 * such that edgeTo[] of the other vertex shouldn't include
 * the vertex (u,v)
 * 
 ******************************************************/

public class Ex_4_4_37 {
	
	private double[] distTo;
	private IndexMinPQ<Double> pq;
	private DijkstraSP spt;
	private Iterable<DirectedEdge> spath;
	private EdgeWeightedDigraph G;
	private boolean reached;
	
	public Ex_4_4_37(EdgeWeightedDigraph G){
		
		flush(G); this.G = G;
		
	}
	
	public void pathDets(int i, int j){
		spt = new DijkstraSP(G,i);
		spath = spt.pathTo(j);
		
		DirectedEdge e = computeCriticalEdge();
		StdOut.println("original: "+spt.distTo(j));
		StdOut.println(e.from()+":"+e.to());
	}
	
	public DirectedEdge computeCriticalEdge(){
		
		Iterator<DirectedEdge> it = spath.iterator();
		DirectedEdge critical=null; Double max = Double.MIN_VALUE;
		while(it.hasNext()){
			
			DirectedEdge e = it.next();
			int v = e.from(), w = e.to();
			StdOut.println(v+":"+w);
			flush(G); distTo[v]=0.0; pq.insert(v, 0.0);
			while(!pq.isEmpty()){
				relax(G,pq.delMin(),v,w);
			}
			
			if(distTo[w]<Double.POSITIVE_INFINITY){
				if(distTo[w]>max) {
					max = distTo[w]; critical = e;
				}
			}
			
		}	
		StdOut.println("max:"+max);
		return critical;
		
	}
	
	private void relax(EdgeWeightedDigraph G, int v, int notfrom, int to){
		if(reached) return;
		for(DirectedEdge e: G.adj(v)){
			int w = e.to();
			StdOut.println("In relax: "+v+":"+w);
			if(distTo[w]>distTo[v]+e.weight()){
				if(v==notfrom && w == to){continue;}
				distTo[w]=distTo[v]+e.weight();
				if(pq.contains(w)) pq.change(w, distTo[w]);
				else pq.insert(w,distTo[w]);
				if(v==notfrom && w == to){reached = true;return;}
			}
		}
		
	}
	
	private void flush(EdgeWeightedDigraph G){
		int length = G.V(); reached = false;
		distTo = new double[length]; pq = new IndexMinPQ<Double>(length);
		for(int i=0; i<length; i++){
			distTo[i] = Double.POSITIVE_INFINITY;
		}
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyEWD.txt"));
			EdgeWeightedDigraph G =new EdgeWeightedDigraph(scan);
			Ex_4_4_37 ob = new Ex_4_4_37(G);
			ob.pathDets(2,5);
		}catch(Exception e){
			StdOut.println("Found exception: "+e.getMessage());
			e.printStackTrace();
		}
	}

}
