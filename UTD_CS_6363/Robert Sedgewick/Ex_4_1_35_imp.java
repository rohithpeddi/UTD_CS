import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

//Biconnectedness standard solution

public class Ex_4_1_35_imp {
	
	private int[] low;
	private int[] pre;
	private int count;
	private boolean[] articulation;
	
	public Ex_4_1_35_imp(Graph G){
		low = new int[G.V()]; pre = new int[G.V()]; articulation = new boolean[G.V()];
		for(int i=0; i<low.length;i++){
			low[i]=-1; pre[i]=-1;
		}
		
		for(int i=0; i<G.V();i++)
			if(pre[i] == -1)
				dfs(G,i,i);
	}
	
	public void dfs(Graph G, int u, int v){
		int children =0;
		pre[v] = count++;
		low[v] = pre[v];
		for(int w:G.adj(v)){
			if(pre[w]== -1){
				children++;
				dfs(G,v,w);
				
				low[v] = Math.min(low[v], low[w]);
				
				if(low[w]>=pre[v] && u!=v){
					articulation[v] = true;
				}
			}
			
			else if(w!=u){
				low[v] = Math.min(low[v], pre[w]);
			}
			
		}
		
		if( u==v && children>1){
			articulation[v] = true;
		}
	}
	
	public void printAT(){
		for(int i=0; i<articulation.length;i++){
			if(articulation[i] == true){
				StdOut.print(i+" ");
			}
		}
			
	}
	
	public static void main(String args[]){		
		try{
			Scanner scan = new Scanner(new File("tinyDG.txt"));			
			Graph gr = new Graph(scan);			
			Ex_4_1_35_imp ob = new Ex_4_1_35_imp(gr);	
			ob.printAT();
		} catch(Exception e){
			StdOut.print(e.getClass());
		}
	}

}
