package MinimumSpanningTrees;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;
import java.util.Stack;

import UndirectedGraphs.Queue;
import edu.princeton.cs.algs4.StdOut;

//Prims and Kruskal algorithm for connected components 

public class Ex_4_3_22 {
	
	private int[] id;
	private boolean[] marked;
	private MinPQ<Edge> pq;
	private Queue<Queue> minsf;
	private Queue<Edge> mst;
	private int V,E,count=1,comps=0;
	private EdgeWeightedGraph G;
	
	public Ex_4_3_22(EdgeWeightedGraph G){
		
		minsf = new Queue<Queue>();
		id = new int[G.V()]; marked = new boolean[G.V()]; 
		this.V = G.V(); this.E = G.E(); this.G =G;
		
		StdOut.println("Entering DFS!");
		
		for(int i=0; i<V; i++){
			if(!marked[i]) {
				dfs(G,i); 
				count++;
			}
		}
		
		flushMarked();		
		
		StdOut.println("Finished DFS! with count:"+count);
		StdOut.println("Entering MSF!");
		
		for(int i=1; i<count; i++){
			Iterable<Edge> pack = packageEdges(i);
			StdOut.println("comps:"+ comps);
			pq = new MinPQ<Edge>(pack,comps); mst = new Queue<Edge>();
			
			visit(G,0);
			
			while(!pq.isEmpty()){
				Edge e = pq.delMin();
				int v = e.either(), w = e.other(v);
				if(marked[v] && marked[w]) continue;
				mst.enqueue(e);
				if(!marked[w]) visit(G,w);
				if(!marked[v]) visit(G,v);
			}	
			
			minsf.enqueue(mst);
			
		}
		StdOut.println("Finished MSF!");
		enlist();
		
	}
	
	//Prints all the msts in the spanning forest 
	public void enlist(){
		
		Iterable<Queue> root = minsf;
		Iterator<Queue> itroot  = minsf.iterator();
		while(itroot.hasNext()){
			Iterable<Edge> child = itroot.next();
			Iterator<Edge> itchild = child.iterator();
			while(itchild.hasNext()){
				Edge e = itchild.next();
				StdOut.println(e.either()+"-"+ e.other(e.either())+","+ e.weight());
			}
		}
		
	}
	
	//Constructing a minimum spanning tree for those connected components
	public void visit(EdgeWeightedGraph G, int v){
		marked[v] = true; 
		for(Edge e:G.adj(v)){
			int w = e.other(v);
			if(!marked[w]) pq.insert(e);			
		}
	}
	
	//get an iterable object with the edges of a particular id 
	public Iterable<Edge> packageEdges(int comp_id){
		
		comps=1;
		Stack<Edge> st = new Stack<Edge>();
		for(int i=0 ; i<V; i++){
			if(id[i]==comp_id){
				for(Edge e:G.adj(i)){
					int w = e.other(i);
					if(i<w) {st.push(e);comps++;}
				}
			}
		}
		
		return st;
		
	}
	
	//depth first search for computing the connected components given by id's
	public void dfs(EdgeWeightedGraph G, int v){
		
		marked[v] = true; id[v] = count;
		for(Edge e:G.adj(v)){
			int w = e.other(v); 
			if(!marked[w]) dfs(G,w);
		}
		
	}
	
	//flushes the boolean array of markings for reusing it 
	public void flushMarked(){
		
		
		for(int i=0; i<marked.length; i++)
			marked[i] = false;
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan =  new Scanner(new File("250verts.txt"));
			EdgeWeightedGraph G = new EdgeWeightedGraph(scan);
			Ex_4_3_22 ob = new Ex_4_3_22(G);			
			
		} catch(Exception e){
			StdOut.print("Exception: "+ e.getMessage());
		}
	}

}
