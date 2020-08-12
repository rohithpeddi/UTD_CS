import java.io.*;
import java.util.*;

import edu.princeton.cs.algs4.*;

public class Implementation {
	
	private static int N=0;
	private static int[][] ar;	
	private static Stopwatch stw;
	
	public Implementation(){
		stw = new Stopwatch();
	}
	
	static class quickFind{
		private int id[];
		private int count;
		
		public quickFind(int N){
			count = N;
			id = new int[N];
			for(int i=0;i<N;i++){
				id[i] = i;
			}
		}
		
		public int count(){
			return count;
		}
		
		public boolean connected(int p,int q){
			return find(p)==find(q);
		}
		
		public int find(int n){
			return id[n];
		}
		
		public void union(int p,int q){
			int pID = find(p);
			int qID = find(q);
			
			if(pID==qID) return;
			
			for(int i=0;i<id.length;i++){
				if(id[i]==pID) id[i] = qID;
			}
			count--;
		}
		
	}
	
	static class quickUnion{
		private int id[];
		private int count;
		
		public quickUnion(int N){
			count = N;
			id = new int[N];
			for(int i=0;i<N;i++){
				id[i] = i;
			}
		}
		
		public int count(){
			return count;
		}
		
		public boolean connected(int p,int q){
			return find(p)==find(q);
		}
		
		public int find(int n){
			while(n!=id[n]) n = id[n];
			return n;
		}
		
		public void union(int p,int q){
			int pRoot = find(p);
			int qRoot = find(q);
			
			if(pRoot==qRoot) return;
			
			id[pRoot] = qRoot;
			count--;
		}	
	}
	
	class weightedQuickUnion{
		private int id[],sz[];
		private int count;
		
		public weightedQuickUnion(int N){
			count = N;
			id = new int[N];sz = new int[N];
			for(int i=0;i<N;i++){
				id[i] = i;sz[i] =1;
			}
		}
		
		public int count(){
			return count;
		}
		
		public boolean connected(int p,int q){
			return find(p)==find(q);
		}
		
		public int find(int n){
			while(n!=id[n]) n = id[n];
			return n;
		}
		
		public void union(int p,int q){
			int pRoot = find(p);
			int qRoot = find(q);
			
			if(pRoot==qRoot) return;
			
			if(sz[pRoot]>sz[qRoot]) { id[qRoot] = pRoot; sz[pRoot]+=sz[qRoot];}
			else { id[pRoot]= qRoot; sz[qRoot]+=sz[pRoot];}
			
			count--;
		}	
	}
	
	public static double tqf(quickFind qf){
		for(int i =0; i<N;i++){
			int p = ar[i][0]; int q = ar[i][1];
			if(qf.connected(p, q)) continue;
			qf.union(p, q);
		}		
		double timeqf = stw.elapsedTime();
		return timeqf;
	}
	
	public static double tqu(quickUnion qu){
		for(int i =0; i<N;i++){
			int p = ar[i][0]; int q = ar[i][1];
			if(qu.connected(p, q)) continue;
			qu.union(p, q);
		}	
		double timequ = stw.elapsedTime();
		return timequ;
	}
	
	public static double twqu(weightedQuickUnion wqu){
		for(int i =0; i<N;i++){
			int p = ar[i][0]; int q = ar[i][1];
			if(wqu.connected(p, q)) continue;
			wqu.union(p, q);
		}			
		double timetwqu = stw.elapsedTime();
		return timetwqu;
	}
	
	public static void main(String args[]){
		Scanner scan=null;
				
		for(int i=1;i<4;i++){
			try{
				if(i==1) scan = new Scanner(new File("tinyUF.txt"));
				else if(i==2) scan = new Scanner(new File("mediumUF.txt"));
				else if(i==3) scan = new Scanner(new File("largeUF.txt"));
			}	catch(Exception e){ StdOut.print("File Not Found");}
			
			N = scan.nextInt();
			
			quickFind qf = new quickFind(N);
			quickUnion qu = new quickUnion(N);
			weightedQuickUnion wqu = new Implementation().new weightedQuickUnion(N);
			ar = new int[N][2];
			int det =0;
			while(det<N){
				ar[det][0] = scan.nextInt();
				ar[det][1] = scan.nextInt();
				det++;
				}
			
			double timeqf = tqf(qf);
			double timequ = tqu(qu);
			double timewqu = twqu(wqu);
 			
			StdOut.println("For quickfind: "+timeqf+"\nFor quickUnion: "+timequ+"\nFor weightedQuickUnion: "+ timewqu);
 			}
			
			
			
		}
		
	}
