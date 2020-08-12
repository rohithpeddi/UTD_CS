import edu.princeton.cs.algs4.StdOut;

/******************************************************
 * INTERPOLATION SEARCH
   Rank is calculated using interpolation search in the symbol table
 * ****************************************************/

public class Ex_3_1_24 {
	
	public int cap =10,M=0;
	private Integer[] arkey = new Integer[cap];
	private String[] arval =  new String[cap];
	
	public boolean isEmpty(){return M==0;}
	public int size(){return M;}
	
	public void resize(){
		cap = 2*cap;
		Integer[] arkeyN = new Integer[cap];
		String[] arvalN =  new String[cap];
		
		for(int i=0;i<M;i++){
			arkeyN[i] = arkey[i]; arvalN[i] = arval[i];
		}		
		arkey = arkeyN; arval = arvalN;		
	}
	
	public int rank(Integer k){
		int lo = 0, hi= M-1;
		while(lo<=hi){
			if(lo==hi) return lo;
			double num = ( ((double)k-(double)arkey[lo]) / ((double) arkey[hi]-(double)arkey[lo]) );
			int node = lo+ (hi-lo)*(int) Math.floor(num);
			//StdOut.print(node+" "+ arkey[node]+" "+k+" ");
			int cmp = k.compareTo(arkey[node]);
			if(cmp<0){ hi = node-1;}
			else if(cmp>0){ lo= node+1;}
			else return node;
		}
		return 0;
	}
	
	public void put(Integer k,String v){
		if(isEmpty()){arkey[M]=k;arval[M]=v;M++; return;}
		int n = rank(k);
		if(k.compareTo(arkey[n])==0){arval[n]= v; return;}
		else if(n==0 && M==1){
			if(k.compareTo(arkey[n])>0){arkey[M]=k;arval[M]=v;M++;return;}
			else {
				arkey[M]=arkey[M-1];arval[M]=arval[M-1];
				arkey[n]=k;arval[n]=v;
			}
		}
		else{
			for(int j=M;j>n;j--){
				arkey[j]=arkey[j-1]; arval[j]=arval[j-1];
			}
			arkey[n]=k;arval[n]=v;
			M++; 
			if(M > (cap*3)/4) {resize();}
		}
		printOrder();
	}
	
	public String get(Integer k){
		int n = rank(k);
		if(k.compareTo(arkey[n])==0){ return arval[n];}
		else{return null;}
	}
	
	public void printOrder(){
		for(String x:arval){StdOut.print(x+" ");} StdOut.println(" ");
	}
	
	public void printrder(Ex_3_1_24 ob){
		for(int i=1; i<20;i++){
			StdOut.print(ob.get(i)+" ");
		}
	}
	
	public static void main(String args[]){
		Ex_3_1_24 ob =  new Ex_3_1_24();
		ob.put(1, "A-1");ob.put(24, "X-24");ob.put(4, "D-4");ob.put(3, "C-3");ob.put(20, "T-20");
		ob.put(7, "G-7");ob.put(21, "U-21");ob.put(22, "V-22");ob.put(11, "K-11");ob.put(12, "L-12");ob.put(10, "J-10");ob.put(19, "S-19");
		ob.put(13, "M-13");ob.put(14, "N-14");ob.put(15, "O-15");ob.put(16, "P-16");ob.put(17, "Q-17");ob.put(18, "R-18");
		ob.put(23, "W-23");ob.put(6, "F-6");ob.put(8, "H-8");ob.put(9, "I-9");ob.put(5, "E-5");ob.put(2, "B-2");
		ob.printOrder();
		ob.printrder(ob);
	}
	
	
	
}
