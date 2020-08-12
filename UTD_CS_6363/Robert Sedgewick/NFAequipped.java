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
 * NFA equipped with various shortcuts used int regex 
 */

public class NFAequipped {
	
	private char[] re; 			//match transitions
	private Digraph G;			//epsilon transitions
	private int M;				//number of states
	
	public NFAequipped(String regexp){
		re = regexp.toCharArray();
		M = re.length; G = new Digraph(M+1);
		Stack<Integer> ops = new Stack<Integer>();
		int count=0;
		
		for(int i=0; i<M; i++){
			
			int lp=i;
			
			if(re[i] == '(' || re[i]=='|'){
				if(re[i]=='(') count++;
				ops.push(i);
			}
			else if(re[i]==')'){
				
				int or = ops.pop();
				if(re[or]=='|'){
					int size = ops.size();
					int ar[] = new int[size-count];
					for(int j=ar.length; j>0; j--){
						lp = ops.pop();
						ar[j]=lp;
					}
					G.addEdge(lp, ar[0]+1);
					for(int j=1; j<ar.length; j--){
						G.addEdge(ar[i-1],ar[i]+1);
					}					
					G.addEdge(or, i);
				}
				else lp = or;
			}
			
			if(i<M-1 && (re[i+1]=='*'|| re[i+1]=='+')){
				G.addEdge(lp, i+1);
				G.addEdge(i+1, lp);
			}			
			
			if(re[i]=='(' || re[i]=='*' || re[i]==')'|| re[i]=='+')
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
					if(re[v]=='+'){
						
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
