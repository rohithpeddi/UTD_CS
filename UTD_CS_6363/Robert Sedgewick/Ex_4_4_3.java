package ShortestPaths;

import java.io.File;
import java.util.Scanner;

import UndirectedGraphs.Bag;
import edu.princeton.cs.algs4.StdOut;

//Edgeweighted Dense Digraphs

public class Ex_4_4_3 {
	
	private int V,E;
	private DirectedEdge[][] adj;
	
	public Ex_4_4_3(int V){
		this.V = V; 
		adj = new DirectedEdge[V][V];
	}
	
	public Ex_4_4_3(Scanner scan){
		this(Integer.parseInt(scan.nextLine())); scan.nextLine();
		while(scan.hasNextLine()){
			String[] str = scan.nextLine().split(" ");
			int v = Integer.parseInt(str[0]),w = Integer.parseInt(str[1]);double weight = Double.parseDouble(str[2]);
			DirectedEdge e = new DirectedEdge(v,w,weight);
			addEdge(e);			
		}		
	}
	
	public void addEdge(DirectedEdge e){
		int v = e.from(),w = e.to();
		adj[v][w] = e;
		E++;
	}
	
	public Iterable<DirectedEdge> adj(int v){
		Bag<DirectedEdge> edges = new Bag<DirectedEdge>();
		for(int i=0; i<V; i++){
			if(adj[v][i]!=null)edges.add(adj[v][i]);
		}			
		return edges;
	}
	
	public Iterable<DirectedEdge> edges(){
		Bag<DirectedEdge> alledges = new Bag<DirectedEdge>();
		for(int i=0; i<V; i++){
			for(DirectedEdge e:adj(i)){
				alledges.add(e);
			}
		}
		return alledges;
	}
	
	public int V(){return V;}
	public int E(){return E;}
	
	public String toString(){
		String str="";
		str+= "Vertices: "+ V+", Edges:" +E+"\n";
		for(int i=0; i<V; i++){
			str+= i +":";
			for(DirectedEdge e:adj(i)){
				int w = e.to(); double weight = e.weight();
				str+= "-("+w+","+weight+")";
			}			
			str+="\n";
		}		
		return str;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyEWD.txt"));
			Ex_4_4_3 ob = new Ex_4_4_3(scan);
			StdOut.println(ob.toString());			
		} catch(Exception e){
			
		}	
		
	}
	
}
