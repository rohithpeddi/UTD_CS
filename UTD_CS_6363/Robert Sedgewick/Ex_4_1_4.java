import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class Ex_4_1_4 extends Graph{
	
	private Bag<Integer>[] adj;
	
	public Ex_4_1_4(Scanner scan){
		super(scan);
		this.adj = super.adj;
	}	
	
	public boolean hasEdge(int v, int u){
		for(int w:adj[v])
			if(w == u) return true;
		
		return false;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG.txt"));
			Ex_4_1_4 ob = new Ex_4_1_4(scan);
			StdOut.print(ob.hasEdge(1, 0));
			
		} catch(Exception e){
			StdOut.print(e.getMessage());
		}
	}

}
