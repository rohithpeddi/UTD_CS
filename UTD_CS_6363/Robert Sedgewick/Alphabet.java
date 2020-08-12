/**
 * 
 */
package Tries;

/*************************

 * @author rohith peddi

 *************************/
public class Alphabet {
	
	private char[] ar;
	private int N;
	
	public Alphabet(String s){
		N = s.length();
		ar = s.toCharArray();
	}
	
	public char toChar(int index){
		return ar[index];
	}
	
	public int toIndex(char c){
		for(int i=0; i<N; i++){
			if(ar[i]== c) return i; 
		}
		return 0;
	}
	
	public boolean contains(char c){
		for(int i=0; i<N; i++){
			if(ar[i]== c) return true; 
		}
		return false;
	}
	
	public int R(){
		return N;
	}
	
	public int lgR(){
		return  (int) ((int)Math.log(N)/Math.log(2));
	}
	
	public int[] toIndices(String s){
		int[] convert = new int[s.length()];
		for(int i=0; i<s.length(); i++){
			convert[i]= toIndex(s.charAt(i));
		}
		return convert;
	}
	
	public String toChars(int[] indices){
		String st="";
		
		for(int i=0; i<indices.length; i++){
			st+= toChar(indices[i]);
		}
		
		return st;
	}

}
