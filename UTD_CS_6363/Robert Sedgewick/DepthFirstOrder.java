package DirectedGraphs;

import java.util.Stack;

import ShortestPaths.DirectedEdge;
import ShortestPaths.EdgeWeightedDigraph;
import UndirectedGraphs.Queue;

public class DepthFirstOrder {
	
	private boolean[] marked;
	
	Queue<Integer> pre, post;
	Stack<Integer> reversePost;
	
	/******************************************************
	 * CONSTRUCTOR with EdgeWeightedDigraph 
	 * and corresponding methods
	 * ***************************************************/
	
	public DepthFirstOrder(EdgeWeightedDigraph G){
		pre = new Queue<Integer>(); post = new Queue<Integer>();
		reversePost = new Stack<Integer>();
		
		marked = new boolean[G.V()];
		for(int i=0; i<G.V(); i++){
			if(!marked[i]) dfs(G,i);
		}
	}
	
	public void dfs(EdgeWeightedDigraph G, int v){
		marked[v] = true;
		pre.enqueue(v);
		for(DirectedEdge e:G.adj(v)){
			int w = e.to();
			if(!marked[w]) dfs(G,w);
		}
		
		post.enqueue(v); reversePost.push(v);
	}
	
	/******************************************************
	 * CONSTRUCTOR with Digraph 
	 * and corresponding methods
	 * ***************************************************/
	
	public DepthFirstOrder(Digraph G){
		pre = new Queue<Integer>(); post = new Queue<Integer>();
		reversePost = new Stack<Integer>();
		
		marked = new boolean[G.V()];
		for(int i=0; i<G.V(); i++){
			if(!marked[i]) dfs(G,i);
		}	
	}
	
	public void dfs(Digraph G, int v){
		marked[v] = true;
		pre.enqueue(v);
		for(int w:G.adj(v)){
			if(!marked[w]) dfs(G,w);
		}
		
		post.enqueue(v); reversePost.push(v);
	}
	
	// If the digraph is acyclic then reversePost gives the topologically sorted order
	// checking for cyclicality  before is must to return the sorted order
	
	public Iterable<Integer> topological(){
		return reversePost;
	}
	
	public Iterable<Integer> pre(){
		return pre;
	}
	
	public Iterable<Integer> post(){
		return post;
	}
	
	public Iterable<Integer> reversePost(){
		return reversePost;
	}

}
