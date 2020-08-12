/**
 * 
 */
package Regex;

import java.util.Stack;

import edu.princeton.cs.algs4.Bag;
import edu.princeton.cs.algs4.Digraph;
import edu.princeton.cs.algs4.DirectedDFS;
import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Non deterministic finite state automaton
 * 
 * construction for a given regexp and later it is 
 * used for checking whether the given string 
 * obeys this pattern or not 
 * 
 */

public class NFA {
	
	private char[] re; 			//match transitions
	private Digraph G;			//epsilon transitions
	private int M;				//number of states
	
	public NFA(String regexp){
		re = regexp.toCharArray();
		M = re.length; G = new Digraph(M+1);
		Stack<Integer> ops = new Stack<Integer>();
		
		for(int i=0; i<M; i++){
			
			int lp=i;
			
			if(re[i] == '(' || re[i]=='|')
				ops.push(i);
			else if(re[i]==')'){
				
				int or = ops.pop();
				if(re[or]=='|'){
					lp = ops.pop();
					G.addEdge(lp, or+1);
					G.addEdge(or, i);
				}
				else lp = or;
			}
			
			if(i<M-1 && re[i+1]=='*'){
				G.addEdge(lp, i+1);
				G.addEdge(i+1, lp);
			}			
			
			if(re[i]=='(' || re[i]=='*' || re[i]==')')
				G.addEdge(i, i+1);
			
		}
		
	}
	
	public boolean recognizes(String txt){
		
		Bag<Integer> pc = new Bag<Integer> ();
		DirectedDFS dfs = new DirectedDFS(G,0);
		
		for(int v=0; v<G.V(); v++)
			if(dfs.marked(v)) pc.add(v);
		
		StdOut.println("Added for: 0");
		
		for(int i=0; i<txt.length(); i++){ //compute NFA states for txt[i+1]
			
			Bag<Integer> match = new Bag<Integer>();
			
			StdOut.print(i+": ");
			for(int v:pc){
				StdOut.print(v+" ");
				if(v<M){
					if(re[v]==txt.charAt(i) || re[v]=='.'){
						match.add(v+1);
					}
				}
			}
			StdOut.println("");
			
			//StdOut.println("Added for: "+ match.toString());
			
			pc = new Bag<Integer>();
			dfs = new DirectedDFS(G,match);
			for(int v=0; v<G.V(); v++)
				if(dfs.marked(v)) pc.add(v);			
		}
		
		for(int v:pc)
			if(v==M) return true;		
		
		return false;
	}
	
	

}
