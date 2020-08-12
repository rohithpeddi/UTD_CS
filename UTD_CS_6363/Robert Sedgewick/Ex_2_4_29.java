public class Ex_2_4_29 {
	
	private int[] or;
	private int N;
	
	public boolean isEmpty(){
		return Nax==0;
	}
	
	public int size(){
		return Nax;
	}
	
	public void insert(int n){
		or[++N] = n;
		axor(n);
		inor(n);
	}
	
	public boolean less(int i, int j, int[] ar){
		return ar[i]<ar[j];
	}
	
	public void exch(int i, int j, int[] ar){
		int temp = ar[i]; ar[i]=ar[j];ar[j]=temp;
	}
	
	//Having a max heap
	/***************************************************************************/
	
	private int[] maxor;
	private int Nax;
	
	public void axor(int n){
		maxor[++Nax] = n;
		maxswim(Nax);
	}
	
	public void maxswim(int k){
		while(k>1 && (less(k/2,k,maxor))){
			exch(k/2,k,maxor);
			k=k/2;
		}
	}
	
	public int getmax(){
		return maxor[1];
	}
	
	public int del_max(){
		int max = maxor[1];
		change_minor(max);
		
		exch(1,Nax--,maxor);
		maxsink(1);
		return max;
	}
	
	public void maxsink(int k){
		while(2*k<=N){
			int j = 2*k;
			if(j<N && (less(j,j+1,maxor))) j++;
			if(!less(k,j,maxor)) break;
			exch(k,j,maxor);
			k=j;
		}
	}
	
	public void change_maxor(int min){
		for(int k = Nax; k> Nax/2;k--){
			if(maxor[k]==min){
				exch(k,Nax--,maxor);
				maxsink(k);
				return;
			}
		}
	}
	
	//Having a min heap
	/***************************************************************************/
	
	private int[] minor;
	private int Nin;
	
	public void inor(int n){
		minor[++Nin] = n;
		minswim(Nin);
	}
	
	public void minswim(int k){
		while(k>1 && !(less(k/2,k,minor))){
			exch(k/2,k,minor);
			k=k/2;
		}
	}
	
	public int getmin(){
		return minor[1];
	}
	
	public int del_min(){
		int min = minor[1];
		change_maxor(min);
		
		exch(1,Nin--,minor);
		minsink(1);
		return min;
	}
	
	public void minsink(int k){
		while(2*k<=N){
			int j = 2*k;
			if(j<N && (less(j+1,j,minor))) j++;
			if(less(k,j,minor)) break;
			exch(k,j,minor);
			k=j;
		}
	}
	
	public void change_minor(int max){
		for(int k = Nin; k> Nin/2;k--){
			if(maxor[k]==max){
				exch(k,Nin--,minor);
				minsink(k);
				return;
			}
		}
	}
	
	public static void main(String args[]){
		
	}
	
	
	
}
