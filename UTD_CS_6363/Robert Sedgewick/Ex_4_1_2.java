import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class Ex_4_1_2 {
	
	private Bag<Integer>[] adj;
	private int V,E;
	
	public Ex_4_1_2(int cap){
		//StdOut.println("Entered plain constructor");
		adj = (Bag<Integer>[]) new Bag[cap];
		this.V = cap;
		for(int v=0; v<V; v++)
			adj[v] = new Bag<Integer>();
	}
	
	public Ex_4_1_2(Scanner scan){		
		this(scan.nextInt());
		//StdOut.println("Entered scan constructor");
		E = scan.nextInt();
		while(scan.hasNextInt()){
			int v = scan.nextInt(),w=scan.nextInt();
			//StdOut.println("Adding:"+v+":"+w);
			addEdge(v,w);
		}
	}
	
	public int V(){return V;}
	public int E(){return E;}
	
	public void addEdge(int v, int w){
		adj[v].add(w);adj[w].add(v);
	}
	
	public String toString(){
		String s="Vertices:"+V+",Edges:"+E+"\n";
		for(int i=0; i<V;i++){
			s=s+i+":";
			for(int w:adj[i]){
				s+= w+" ";
			}
			s+="\n";
		}
		return s;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG.txt"));
			Ex_4_1_2 ob = new Ex_4_1_2(scan);
			String str = ob.toString();
			StdOut.print(str);
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}	

}
