package ShortestPaths;

import java.util.Scanner;

import UndirectedGraphs.Bag;

public class EdgeWeightedDigraph {
	
	private int V,E;
	private Bag<DirectedEdge>[] adj;
	
	public EdgeWeightedDigraph(int V){
		this.V = V; 
		adj = (Bag<DirectedEdge>[]) new Bag[V];
		for(int i=0; i<V; i++){
			adj[i] = new Bag<DirectedEdge>();
		}
	}
	
	public EdgeWeightedDigraph(Scanner scan){
		this(Integer.parseInt(scan.nextLine())); scan.nextLine();
		while(scan.hasNextLine()){
			String[] str = scan.nextLine().split(" ");
			int v = Integer.parseInt(str[0]),w = Integer.parseInt(str[1]);double weight = Double.parseDouble(str[2]);
			DirectedEdge e = new DirectedEdge(v,w,weight);
			addEdge(e);			
		}		
	}
	
	public void addEdge(DirectedEdge e){
		int v = e.from();
		adj[v].add(e);
		E++;
	}
	
	public Iterable<DirectedEdge> adj(int v){
		return adj[v];
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
			for(DirectedEdge e:adj[i]){
				int w = e.to(); double weight = e.weight();
				str+= "-("+w+","+weight+")";
			}			
			str+="\n";
		}		
		return str;
	}

}
