package DirectedGraphs;

import java.awt.Color;
import java.io.File;
import java.util.Scanner;
import java.util.Stack;

import UndirectedGraphs.Bag;
import UndirectedGraphs.Queue;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

public class Ex_4_2_19 extends Digraph{
	
	private boolean[] marked;
	private int[] edgeTo;
	private boolean isConnected;
	private int count;
	private boolean changeColor;
	private int distance[];
	public Stack<Integer> revPost;
	
	private int V,E;
	private Bag<Integer>[] adj;
	
	
	public Ex_4_2_19(Scanner scan){
		super(scan);
		StdOut.println("Entered into constructor!");
		this.V = super.V(); this.E= super.E();
		this.adj = super.adj;
		revPost = new Stack<Integer>();
		StdOut.println("Assigned values in constructor!"+V+":"+E+":"+adj.length);
		
		marked = new boolean[V]; edgeTo = new int[V]; distance = new int[V];
		for(int i=0; i<V;i++){
			if(!marked[i]){
				bfs(i); changeColor=true;
			}
		}
		
		StdOut.println("Assigned values in bfs!");
		isConnected();
	}
	
	public void isConnected(){
		for(boolean x:marked){
			if(x== false) isConnected = false;
		}
		isConnected = true;
	}
	
	public void bfs(int u){
		Queue<Integer> q = new Queue<Integer>();
		q.enqueue(u); marked[u]=true;
		int checker =1; count=1;
		while(!q.isEmpty()){
			StdOut.println(q.toString());
			int v= q.dequeue();
			revPost.push(v);			
			checker--;
			for(int w: adj(v)){				
				if(!marked[w]){
					edgeTo[w]=v; marked[w]=true;distance[w]=count;
					q.enqueue(w);
				}					
			}			
			if(checker == 0) {checker = q.size(); count++;}
		}
	}
	
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("tinyDG.txt"));
			StdOut.println("Entered!");
			Ex_4_2_19 ob = new Ex_4_2_19(scan);
			StdOut.println("Entered!");
			StdOut.print(ob.revPost.toString());
		} catch (Exception e) {
			StdOut.print("Exception raised: "+ e.getMessage());
		}
	}

}
