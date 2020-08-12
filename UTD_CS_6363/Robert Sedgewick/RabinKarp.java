/**
 * 
 */
package SubstringSearch;

/*************************

 * @author rohith peddi

 *************************/

/******************************************************
 * RABIN KARP FINGERPRINT SUBSTRING SEARCH
 * 
 * Initially computes a skip array which tells us how far
 * should we skip in order to match the pattern elements 
 * 
 * Search always compares from right to left 
 * 
 * Time: O(N/M)
 * Space: Storage(true)
 * 
 ******************************************************/

public class RabinKarp {
	
	private String pat;
	private int M,R=256;
	private long RM,patHash,Q; // computing R^(M-1)%Q
	
	public RabinKarp(String pat){
		this.pat =pat; this.M = pat.length();
		this.Q = 997; //long random prime
		RM=1;
		for(int i=0; i<M; i++){
			RM = (R*RM)%Q;
		}
		
		patHash = hash(pat,M);
		
	}
	
	private long hash(String key, int M){
		long h=0; 
		for(int i=0;i<M; i++){
			h = (R*h + key.charAt(i)) %Q;
		}
		return h;
	}
	
	public boolean check(int i){
		return true;
	}
	
	public int search(String txt){
		int N = txt.length();
		long txtHash = hash(txt,M);
		if(patHash==txtHash) return 0;
		for(int i=M; i<N-M; i++){ //Remove leading digit, add trailing digit and check for match
			txtHash = (txtHash + Q - RM*txt.charAt(i-M)%Q) %Q;
			txtHash = (txtHash*R + txt.charAt(i))%Q;
			if(patHash==txtHash){
				if(check(i-M+1)) return i-M+1;
			}
		}
		return N;
	}
	
	
	
}
