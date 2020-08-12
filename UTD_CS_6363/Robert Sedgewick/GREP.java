/**
 * 
 */
package Regex;

import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/
public class GREP {
	
	public static void main(String args[]){
		
		String regexp= "(.*"+ "(A*B|AC)D"+".*)";
		NFA nfa = new NFA(regexp);
		if(nfa.recognizes("ABCCBD"))
				StdOut.println("ABCCBD");		
		
	}

}
