package DirectedGraphs;

import java.io.File;
import java.util.Scanner;
import java.util.Stack;

import edu.princeton.cs.algs4.StdOut;

public class Ex_4_2_24 {
	
	Stack<Integer> revPost;
	private int[] topo_order;
	private Digraph G;
	
	public Ex_4_2_24(Digraph G){
		DepthFirstOrder order = new DepthFirstOrder(G);
		topo_order = new int[G.V()];
		this.G = G;
		revPost = order.reversePost;
	}
	
	public boolean isHamiltonianPath(){
		for(int i=0; i<topo_order.length-1; i++){
			if(!areConnected(topo_order[i],topo_order[i+1])) {return false;}
		}
		return true;
	}
	
	public boolean areConnected(int v, int w){
		for(int x:G.adj(v)){
			if(x==w) return true;
		}
		return false;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG3.txt"));
			Digraph G = new Digraph(scan);
			Ex_4_2_24 ob = new Ex_4_2_24(G);
			G.drawGraph();
			StdOut.println(ob.isHamiltonianPath());
		} catch (Exception e) {
			StdOut.print("Exception raised: "+ e.getMessage());
		}
	}
	

}
