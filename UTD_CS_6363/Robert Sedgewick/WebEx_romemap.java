package ShortestPaths;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;

import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.SingleGraph;
import org.graphstream.ui.view.View;
import org.graphstream.ui.view.Viewer;

import edu.princeton.cs.algs4.StdOut;

public class WebEx_romemap {
	
	public WebEx_romemap(EdgeWeightedDigraph G){
		
		Graph graph = new SingleGraph("ROME MAP");
		graph.setStrict(false);
		graph.setAutoCreate( true );
		
		Iterator<DirectedEdge> it = G.edges().iterator();
			
		while(it.hasNext()){
			DirectedEdge e = it.next();
			int w= e.to(),v = e.from();
			//StdOut.println(v+":"+w+":"+e.weight());
			graph.addEdge(v+""+w, v+"", w+"",true).addAttribute("ui.label", e.weight()+"");
		}				
		
		for(Node node:graph){
			node.addAttribute("ui.label", node.getId());
		}
		
		Viewer viewer = graph.display();
		View view = viewer.getDefaultView();
		
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("rome.txt"));
			EdgeWeightedDigraph G = new EdgeWeightedDigraph(scan);
			WebEx_romemap ob = new WebEx_romemap(G);
			
		}catch(Exception e){
			StdOut.println("Found Exception: "+e.getMessage());
			e.printStackTrace();
		}
	}

}
