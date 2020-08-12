import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class Ex_4_1_9 {
	
	private boolean[] marked;
	private int[] edgeTo;
	
	
	public Ex_4_1_9(Graph G){
		marked = new boolean[G.V()];
		edgeTo = new int[G.V()];
		for(int v=0; v<G.V();v++)
			if(!marked[v]) dfs(G,v);
	}
	
	private void dfs(Graph G, int v){
		marked[v] = true;
		boolean allMarked=true;
		//StdOut.println("Marked: "+ v);
		for(int w: G.adj(v)){
			//StdOut.println("Entered "+ w+ " adjacent to "+ v);
			if(!marked[w]) {
				allMarked = false;
				edgeTo[w]=v;
				dfs(G,w);
			}			
			else {
				//StdOut.println("Already marked: "+ w);
			}
		}
		if(allMarked) {StdOut.println("Vertex that can be removed:"+v);}
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG.txt"));
			Graph gr = new Graph(scan);
			Ex_4_1_9 ob = new Ex_4_1_9(gr);
		} catch(Exception e){
			StdOut.print(e.getMessage());
		}
	}
	

}
