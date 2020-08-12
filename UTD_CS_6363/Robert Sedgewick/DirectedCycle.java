package DirectedGraphs;

import java.util.Stack;

import ShortestPaths.DirectedEdge;
import ShortestPaths.EdgeWeightedDigraph;
import edu.princeton.cs.algs4.StdOut;

public class DirectedCycle {
	
	private boolean[] marked;
	private int[] edgeToDG;
	private DirectedEdge[] edgeToEWDG;
	Stack<Integer> cycleDG;
	Stack<DirectedEdge> cycleEWDG;
	private boolean[] onStack;
	
	/************* CONSTRUCTOR *****************/
	// with Edge weighted digraph as a parameter
	public DirectedCycle(EdgeWeightedDigraph G){
		StdOut.println("Entered DirectedCycle constructor");
		marked = new boolean[G.V()]; edgeToEWDG = new DirectedEdge[G.V()]; onStack = new boolean[G.V()];
		for(int i=0; i<G.V();i++){
			if(!marked[i]) dfsEWD(G,i);
		}
	}
	// with digraph as a parameter
	public DirectedCycle(Digraph G){
		marked = new boolean[G.V()]; edgeToDG = new int[G.V()]; onStack = new boolean[G.V()];
		for(int i=0; i<G.V();i++){
			if(!marked[i]) dfs(G,i);
		}
	}
	
	/************* DEPTH FIRST SEARCH *****************/
	//onStack represents the stack spaces dfs travels and that are called but not done yet
	
	public void dfs(Digraph G, int v){
		onStack[v] = true; marked[v] = true;
		for(int w:G.adj(v)){
			if(this.hasCycleDG()) return;
			else if(!marked[w]){
				edgeToDG[w] = v;
				dfs(G,w);
			}
			else{
				cycleDG = new Stack<Integer>();
				for(int i=v; i!=w; i = edgeToDG[i]){
					cycleDG.push(i);
				}
				cycleDG.push(w); cycleDG.push(v);
			}
		}
		
		onStack[v] = false;
	}
	
	//dfs for edgeweighteddigraph as a parameter 
	
	public void dfsEWD(EdgeWeightedDigraph G, int v){
		
		onStack[v] = true; marked[v] = true;
		for(DirectedEdge e:G.adj(v)){
			int w = e.to();
			StdOut.println("Entered dfsEWD: "+ v+":"+w);
			if(this.hasCycleEWDG()) return;
			else if(!marked[w]){
				edgeToEWDG[w] = e;
				dfsEWD(G,w);
			}
			else{
				StdOut.println(w);
				cycleEWDG = new Stack<DirectedEdge>();
				for(DirectedEdge ed=edgeToEWDG[v]; e!=null; e = edgeToEWDG[e.from()]){
					cycleEWDG.push(ed);
				}
				cycleEWDG.push(e);
			}
		}
		
		onStack[v] = false;
	}
	
	/************* UTILITY METHODS *****************/
	
	public boolean hasCycleDG(){
		return cycleDG !=null;
	}
	
	public boolean hasCycleEWDG(){
		return cycleEWDG !=null;
	}
	
	public Iterable<Integer> cycleDG(){
		return cycleDG;
	}
	
	public Iterable<DirectedEdge> cycleEWDG(){
		return cycleEWDG;
	}

}
