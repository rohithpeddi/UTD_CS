public class Ex_2_4_21 {
	
	//Stack implementation
	
	private int[] ar;
	private int N;
	
	public void push(int n){
		ar[++N] = n;
	}
	
	public int pop(){
		int m = ar[N--];
		return m;
	}
	
	public boolean isEmpty(){
		return N==0;
	}
	
	public int size(){
		return N;
	}
	
	public void exch(int i, int j, int[] mar){
		int temp = ar[j];ar[j] = ar[i]; ar[i] = temp;
	}
	
	public boolean less(int i, int j , int[] mar){
		return mar[i]<mar[j];
	}
	
	public void swim(int k,int[] mar){
		while(k>1 && (less(k/2,k,mar))){
			exch(k/2,k,mar);
			k= k/2;
		}
	}
	
	public void sink(int k, int[] mar){
		while(2*k<= mar.length){
			int j = 2*k;
			if(j<N && less(j,j+1,mar)) j++;
			if(!less(k,j,mar)) break;
			exch(k,j,mar);
			k=j;
		}
	}
	
	//Queue implementation
	
	private int[] qar;
	private int M;
	
	public void enqueue(int n){
		qar[++M] = n;
	}
	
	public int dequeue(){
		int m = qar[1];
		for(int i=1;i<M;i++){
			qar[i]=qar[i+1];
		}
		M--;
		return m;
	}
	
	public boolean isqEmpty(){
		return M==0;
	}
	
	public int qsize(){
		return M;
	}
	
	public void qexch(int i, int j){
		int temp = qar[j];qar[j] = qar[i]; qar[i] = temp;
	}
	
	public boolean qless(int i, int j , int[] mar){
		return mar[i]<mar[j];
	}
	
	
	public static void main(String args[]){
		
	}
	
}
