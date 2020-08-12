/**
 * 
 */
package Regex;

import java.util.Stack;

import edu.princeton.cs.algs4.Digraph;
import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

/*
 * One way legal RE 
 * 
 * Applies only for one parenthesis and immaturely return for 
 * double parenthesis leading to non proper initialization 
 * of the grpah produced.
 * 
 */

public class Ex_5_4_15 {
	
	private char re[];
	private int M; 
	private Digraph G;
	
	public Ex_5_4_15(String regexp){
		
		re = regexp.toCharArray();
		M = re.length; G = new Digraph(M+1);
		Stack<Integer> ops = new Stack<Integer>();
		int count=0;
		
		for(int i=0; i<M; i++){
			
			int lp =i;
			if(re[i]=='('|| re[i]=='|'){
				if(count>1){
					StdOut.println("Not a legal one");
					return;
				}
				
				if(count<1){
					ops.push(i);
					if(re[i]=='(') count++;
				}
			}
			
			else if(re[i]==')'){
				
				int or = ops.pop();
				if(re[or]=='|'){
					lp = ops.pop();count--;
					G.addEdge(lp, or+1);
					G.addEdge(or, i);
				}
				else lp=or;
				
			}
			
			if(i<M-1 && re[i+1]=='*'){
				G.addEdge(lp, i+1);
				G.addEdge(i+1, lp);
			}
			
			if(re[i]=='('|| re[i]=='*'|| re[i]==')'){
				G.addEdge(i, i+1);
			}
			
		}
		
	}

}
