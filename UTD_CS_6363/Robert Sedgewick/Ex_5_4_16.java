/**
 * 
 */
package Regex;

import java.util.Stack;

import edu.princeton.cs.algs4.Digraph;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Multiway or in NFA creation 
 * i,e processes things such as 
 *  A|B|C|D|E
 *  
 */

public class Ex_5_4_16 {
	
	private char[] re; 			//match transitions
	private Digraph G;			//epsilon transitions
	private int M;				//number of states
	
	public Ex_5_4_16(String regexp){
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
			
			if(i<M-1 && re[i+1]=='*'){
				G.addEdge(lp, i+1);
				G.addEdge(i+1, lp);
			}			
			
			if(re[i]=='(' || re[i]=='*' || re[i]==')')
				G.addEdge(i, i+1);
			
		}
		
	}

}
