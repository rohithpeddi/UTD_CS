package DirectedGraphs;

import java.io.File;
import java.util.Scanner;

import UndirectedGraphs.Queue;
import edu.princeton.cs.algs4.StdOut;

public class Ex_4_2_21 {
	
	private boolean[] marked;
	private int[] edgeTo;
	private int[] height;
	private int count,root;
	
	private int LCA;
	
	
	public Ex_4_2_21(Digraph G){
		marked = new boolean[G.V()]; edgeTo = new int[G.V()]; height = new int[G.V()];
		this.root =0; this.LCA = root;
		bfs(G,root);
	}
	
	private void bfs(Digraph G, int u){
		Queue<Integer> q = new Queue<Integer>();
		q.enqueue(u); marked[u]= true;
		int checker = 1; count=1;
		while(!q.isEmpty()){
			int v = q.dequeue(); 
			checker--;
			for(int w:G.adj(v)){
				if(!marked[w]){
					edgeTo[w]=v; marked[w]=true; height[w]=1;
					q.enqueue(w);
				}
			}
			if(checker == 0){
				checker = q.size(); count++;
			}
		}
	}
	
	private boolean reachable(int v){
		if(marked[v]) return true;
		return false;
	}
	
	public boolean isChild(int v, int w){
		int hv = height[v]; int hw = height[w];
		if(hv>hw){
			for( int i=v; i!=root; i = edgeTo[i]){
				if(i==w) return true;
			}
		}
		else{
			for( int i=w; i!=root; i = edgeTo[i]){
				if(i==v) return true;
			}
		}
		return false;
	}
	
	public boolean isRoot(int v, int w){
		if(v == root) return true;
		if(w == root) return true;
		return false;
	}
	
	public void LCA(int v, int w){
		if(v==w) {StdOut.println("Entered values are same!");return;}
		if(reachable(v) && reachable(w)){
			
			if(isRoot(v,w))	{StdOut.println("One is child of other - one value is root");return;}
			if(isChild(v,w)) {StdOut.println("One is child of other");return;} 		
			
			int hv = height[v]; int hw = height[w];
			if(hv>hw){
				for( int i=w; i!=root; i = edgeTo[i]){
					for(int j=v; j!=root; j= edgeTo[j] ){
						if(j == i) {LCA = j; return;}
					}
				}
			}
			else{
				for( int i=v; i!=root; i = edgeTo[i]){
					for(int j=w; j!=root; j= edgeTo[j] ){
						if(j == i) {LCA = j; return;}
					}
				}
			}
			
		}
		else StdOut.println("No common ancestor from root");
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG2.txt"));
			Digraph G = new Digraph(scan);
			Ex_4_2_21 ob = new Ex_4_2_21(G);
			G.drawGraph();
			ob.LCA(10,0);
			StdOut.print(ob.LCA);
		} catch (Exception e) {
			StdOut.print("Exception raised: "+ e.getMessage());
		}
	}

}
