package DirectedGraphs;

import java.io.File;
import java.util.Scanner;

import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.StdOut;

public class Ex_4_2_2 extends Digraph{
	
	public int V,E;
	public Bag<Integer>[] adj;
	
	public Ex_4_2_2(Scanner scan){
		super(scan);
		this.V = super.V(); this.E = super.E();
		this.adj = super.adj;
	}
	
	public String toString(){
		String str = "";
		str += "Vertices: "+ V+", Edges:"+E+"\n";
		for(int i=0; i<V;i++){
			str += i+":";
			for(int w:adj[i]){
				str+= w + " ";
			}
			str	+= "\n";
		}
		return str;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG2.txt"));
			Ex_4_2_2 ob = new Ex_4_2_2(scan);
			StdOut.println(ob.toString());
			ob.drawGraph();
		} catch (Exception e) {
			StdOut.print("Exception raised: "+ e.getMessage());
		}
	}

}
