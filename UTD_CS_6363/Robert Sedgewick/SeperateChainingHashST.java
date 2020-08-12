public class SeperateChainingHashST<Key,Value> {
	
	public int N=0; 
	public int M;
	public SequentialSearchST<Key,Value>[] st;
	
	public SeperateChainingHashST(){
		this(997);
	}
	
	public SeperateChainingHashST(int M){
		this.M =M; 
		st = (SequentialSearchST<Key,Value>[]) new SequentialSearchST[M];
		for(int i=0; i<M; i++)
			st[i] = new SequentialSearchST();
	}
	
	public boolean isEmpty(){
		return N==0;
	}
	
	/*******************************************************
	 * HASH IMPLEMENTATION
	 *******************************************************/	
	public int hash(Key key){
		return (key.hashCode() & 0x7fffffff) % M;
	}
	
	/*******************************************************
	 * GET IMPLEMENTATION
	 *******************************************************/
	
	public Value get(Key key){
		return (Value) st[hash(key)].get(key);
	}
	
	/*******************************************************
	 * PUT IMPLEMENTATION
	 *******************************************************/
	
	public void put(Key key, Value val){
		st[hash(key)].put(key, val); 
		N++;
	}
	
	/*******************************************************
	 * DELETE IMPLEMENTATION
	 *******************************************************/
	
	public void delete(Key key){
		st[hash(key)].delete(key);
		N--;
	}
	
	public static void main(String args[]){
		SeperateChainingHashST<String,Integer> ob = new SeperateChainingHashST<String,Integer>();
		Scanner scan = new Scanner(System.in);
		try{
			StdOut.println("Please input keys:");
			String st = scan.nextLine();
			StdOut.println("Given input of strings is: "+ st);
			String delims = " ";
			String st1[]  = st.split(delims);
			for(int i=0; i<st1.length;i++){
				//StdOut.println(i+":"+st1[i]);
				ob.put(st1[i], i);
				ob.delete(st1[i]);
				StdOut.println(i+":"+ob.get(st1[i]));
				StdOut.println(" \n ");
			}
			
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}
	
}
	
	

