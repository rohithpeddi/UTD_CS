/**
 * 
 */
package SubstringSearch;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/*************************

 * @author rohith peddi

 *************************/

/*
 * Buffering in brute force 
 * 
 * Maintain a M character input stream 
 * and apply check for it 
 * 
 */

public class Ex_5_3_28 {
	
	private String pat;
	private int count;
	private List<Integer> occ;
	
	public Ex_5_3_28(String pat,Scanner scan){
		this.pat=pat; this.count=0;
		this.occ = new ArrayList<Integer>();
		searchAll(scan);
	}
	
	public int searchAll(Scanner scan){
		
		int M=pat.length();
		String txt = "";
		for(int i=0; i<M; i++){
			txt+= scan.nextLine();
		}
		
		if(txt.equals(pat)){
			occ.add(count++); 
		}
		
		while(scan.hasNextLine()){
			
			txt = txt.substring(1);
			txt+= scan.nextLine();
			
			int j=0;
			for(j=0; j<M; j++){
				if(txt.charAt(j)!=pat.charAt(j)){
					break;
				}
			}
			
			if(j==M) {occ.add(count++);}
			else count++;
			
		}	
		
		return count;
	}

}
