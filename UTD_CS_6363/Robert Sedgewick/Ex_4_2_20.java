package DirectedGraphs;

import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class Ex_4_2_20 extends DirectedDFS {
	
	private boolean[] marked;
	private boolean isConnected;
	private boolean isEulerian;
	private Digraph G;
	
	public int[] inDegree, outDegree;
	
	
	public Ex_4_2_20(Digraph G){
		super(G,0);
		this.marked = super.marked; this.G =G;
		inDegree = new int[G.V()]; outDegree = new int[G.V()];
		if(isConnected()) isEulerian();
		StdOut.println("the given digraph is "+isEulerian+"ly eulerian");
	}
	
	public boolean isConnected(){
		StdOut.println("Entered isConnected analysis");
		for(int i=0; i<G.V();i++){
			if(marked[i] == false) {isConnected = false;return false;}
		}
		isConnected = true;
		return true;
	}
	
	public boolean isEulerian(){
		StdOut.println("Entered isEulerian analysis");
		
		for( int i=0; i<G.V();i++){
			for(int w:G.adj(i)){
				inDegree[w]++; outDegree[i]++;
			}
		}
		
		for(int i=0; i<G.V();i++){
			if(inDegree[i]!= outDegree[i]){
				isEulerian = false; return false;
			}
		}
		isEulerian = true;
		return true;
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG3.txt"));
			StdOut.println("Entered!");
			Digraph G = new Digraph(scan);
			G.drawGraph();
			Ex_4_2_20 ob = new Ex_4_2_20(G);
			StdOut.println("Entered!");
		} catch (Exception e) {
			StdOut.print("Exception raised: "+ e.getMessage());
		}
	}
	
	

}
