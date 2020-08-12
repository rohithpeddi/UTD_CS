import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class Ex_4_1_11 {
	
	private boolean[] marked;
	private int[] edgeTo;
	
	public Ex_4_1_11(Graph G){
		marked = new boolean[G.V()]; edgeTo = new int[G.V()];
		for(int v=0; v<G.V(); v++)
			if(!marked[v]) bfs(G,v);
	}
	
	public void bfs(Graph G, int v){
		Queue<Integer> q = new Queue<Integer>();
		q.enqueue(v);
		marked[v]=true;
		while(!q.isEmpty()){
			int a = q.dequeue(); StdOut.println(a);
			for(int w:G.adj(a)){
				if(!marked[w]){ 
					marked[w]=true; edgeTo[w] = a;
					//StdOut.print(w+" ");					
					q.enqueue(w);
					StdOut.println(q.toString());
				}
			}
			StdOut.println("\n");
		}
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG.txt"));
			Graph gr = new Graph(scan);
			Ex_4_1_11 ob = new Ex_4_1_11(gr);
		} catch(Exception e){
			StdOut.print(e.getMessage());
		}
	}
	

}
