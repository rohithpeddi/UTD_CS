import edu.princeton.cs.algs4.StdOut;

/*************************************************
 * SELF ORGANISING SEARCH
 * ***********************************************/

public class Ex_3_1_22<Key extends Comparable<Key>,Value> {
	
	private int N=0,cap=10;
	private Key[] arkey= (Key[]) new Comparable[cap];
	private Value[] arval = (Value[]) new Object[cap];
	
	public boolean isEmpty(){return N==0;}
	
	public void resize(){
		cap =2*cap;
		Key[] arkeyN = (Key[]) new Comparable[cap];
		Value[] arvalN = (Value[]) new Object[cap];		
		for(int i=0; i<N;i++){
			arkeyN[i]=arkey[i]; arvalN[i]=arval[i];
		}
		arkey = arkeyN; arval = arvalN;		
	}
	
	public void put(Key k, Value v){
		if(isEmpty()){arkey[N] = k; arval[N] = v;N++; return;}
		for(int i=0; i<N;i++){
			if(k.compareTo(arkey[i])==0) {arval[i]=v; return;}
		}
		
		arkey[N] = k; arval[N] = v; N++;
		if(N> (cap*3)/4) resize();
	}
	
	public Value get(Key k){
		int i=0; Value val=null;
		for(i=0; i<N;i++){
			if(k.compareTo(arkey[i])==0){val = arval[i];break;}
		}
		if(val!=null){
			Key ke = arkey[i]; Value va = arval[i];
			for(int j=i;j>0;j--){
				arkey[j]= arkey[j-1];arval[j]=arval[j-1];
			}
			arkey[0]= ke; arval[0]= va;
		}
		return val;
	}
	
	public void printOrder(){
		for(Value x:arval){ StdOut.print(x+" ");} 
		StdOut.println("");
	}
	
	public void init(Ex_3_1_22<String, Integer> ob){
		ob.put("A", 1);ob.put("B", 2);ob.put("C", 3);ob.put("D", 4);ob.put("E", 5);
		ob.put("F", 6);ob.put("G", 7);ob.put("H", 8);ob.put("I", 9);ob.put("J", 10);
		ob.put("K", 11);ob.put("L", 12);ob.put("M", 13);ob.put("N", 14);ob.put("O", 15);
		ob.put("P", 16);ob.put("Q", 17);ob.put("R", 18);ob.put("S", 19);ob.put("T", 20);
	}
	
	public static void main(String args[]){
		Ex_3_1_22<String,Integer> ob = new Ex_3_1_22<String,Integer>();
		ob.init(ob);
		Integer n=0;
		n= ob.get("K");n=ob.get("S");n=ob.get("G");n=ob.get("C"); n= ob.get("E");
		ob.printOrder();
	}

}
