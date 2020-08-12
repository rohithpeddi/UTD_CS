package DirectedGraphs;

import java.util.Scanner;

public class SymbolDigraph {
	
	private LinearProbingHashST<String,Integer> st;
	private String[] keys;
	private Digraph G;
	
	public SymbolDigraph(Scanner scan, String delim){		
		Scanner rescan = scan;
		st = new LinearProbingHashST<String,Integer>(16);
		while(rescan.hasNextLine()){
			String[] str = rescan.nextLine().split(delim);
			for(int i=0;i<str.length;i++)
				if(!st.contains(str[i]))
					st.put(str[i],st.size());
		}
		
		keys = new String[st.size()];
		for(String name:st.keys){
			keys[st.get(name)] = name;
		}
		
		G = new Digraph(st.size());
		while(scan.hasNextLine()){
			String[] str = scan.nextLine().split(delim);
			int v = st.get(str[0]);
			for(int i=1;i<str.length;i++){
				G.addEdge(v, st.get(str[i]));
			}
		}
		
	}
	
	public boolean contains(String s){return st.contains(s);}
	public int index(String s){return st.get(s);}
	public String name(int v){return keys[v];}
	public Digraph G(){return G;}
	
	
}
