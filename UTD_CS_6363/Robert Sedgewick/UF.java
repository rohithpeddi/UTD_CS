package MinimumSpanningTrees;

public class UF {
	
	// To find all the connected components 
	// If p-q are connected some how then return without doing anything
	// else make their id's same 
	
	private int[] id;
	private int[] sz;
	private int count;
	
	public UF(int N){
		count = N; id = new int[N];sz = new int[N];
		for(int i=0; i<N; i++)
			id[i]=i;
		for(int i=0; i<N; i++)
			sz[i]=1;
	}
	
	public int count(){	return count;}
	public boolean connected(int p, int q){
		return find(p)==find(q);
	}
	
	public int find(int p){
		while(p!=id[p]) 
			p = id[p];
		return p;
	}
	
	public void union(int p, int q){
		int pID = find(p), qID = find(q);
		
		if(pID == qID) return;
		
		if(sz[pID]<sz[qID]) {
			id[pID] = qID; sz[qID] += sz[pID];
		} else {
			id[qID] = pID; sz[pID] += sz[qID];
		}
		
		count--;
	}

}
