/**
 * 
 */
package SubstringSearch;

/*************************

 * @author rohith peddi

 *************************/

/*
 * To find any one of the k patterns present in the 
 * text string or not 
 * 
 */

public class Ex_5_3_20 {
	
	private String[] pat;
	private int M,R=256;
	private long RM,Q; // computing R^(M-1)%Q
	private long[] patHash;
	
	public Ex_5_3_20(String[] pat){
		this.pat =pat; this.M = pat[0].length();
		this.Q = 997; //long random prime
		RM=1;
		for(int i=0; i<M; i++){
			RM = (R*RM)%Q;
		}
		
		for(int i=0; i<pat.length; i++){
			patHash[i] = hash(pat[i],M);
		}
		
	}
	
	private long hash(String key, int M){
		long h=0; 
		for(int i=0;i<M; i++){
			h = (R*h + key.charAt(i)) %Q;
		}
		return h;
	}
	
	public boolean check(long txtHash){
		for(int i=0; i<pat.length; i++){
			if(patHash[i]==txtHash) return true;
		}
		return false;
	}
	
	public int search(String txt){
		int N = txt.length();
		long txtHash = hash(txt,M);
		if(check(txtHash)) return 0;
		for(int i=M; i<N-M; i++){ //Remove leading digit, add trailing digit and check for match
			txtHash = (txtHash + Q - RM*txt.charAt(i-M)%Q) %Q;
			txtHash = (txtHash*R + txt.charAt(i))%Q;
			if(check(txtHash)){
				return i-M+1;
			}
		}
		return N;
	}

}
