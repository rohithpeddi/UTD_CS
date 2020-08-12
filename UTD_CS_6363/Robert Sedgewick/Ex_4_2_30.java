package DirectedGraphs;

import java.io.File;
import java.util.Scanner;

import UndirectedGraphs.Queue;
import edu.princeton.cs.algs4.StdOut;

public class Ex_4_2_30 {
	
	private int[] inDegree;
	private Queue<Integer> sources;
	private boolean[] marked;
	private Digraph G;
	
	public Ex_4_2_30(Digraph G){
		
		inDegree = new int[G.V()]; marked = new boolean[G.V()];
		sources = new Queue<Integer>();
		this.G = G;
		computeInDegree();
		
		for(int i=0; i<G.V();i++){
			if(!marked[i]) {
				dfs(G,i);
				sources.enqueue(i);
			}
		}
		
		marked = new boolean[G.V()];
		StdOut.println(sources.toString());
		topSort(G);
	}
	
	public void topSort(Digraph G){
		StdOut.println("Entered topSort!");
		marked[0] = true;
		while(!sources.isEmpty()){
			int v = sources.dequeue();
			marked[v]=true;
			StdOut.print(v+" ");
			for(int w:G.adj(v)){
				inDegree[w]--;
				if(inDegree[w]==0) sources.enqueue(w);
			}			
		}		
	}
	
	public void dfs(Digraph G, int v){
		marked[v]=true;
		for(int w:G.adj(v)){
			if(!marked[w]){
				dfs(G,w);
			}
		}
	}
	
	public void computeInDegree(){
		
		for(int i=0; i<G.V(); i++){
			for(int w:G.adj(i)){
				inDegree[w]++;
			}
		}
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG2.txt"));
			
			Digraph G = new Digraph(scan);
			G.drawGraph();
			Ex_4_2_30 ob = new Ex_4_2_30(G);
			
		} catch (Exception e) {
			StdOut.print("Exception raised: "+ e.getMessage());
		}
	}

}
