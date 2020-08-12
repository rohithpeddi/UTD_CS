import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

public class Ex_3_2_41_great<Key extends Comparable<Key>,Value> {
	
	private Key[] akey;
	private int count = 0;
	private int[] aleft;
	private int[] aright;
	
	Ex_3_2_41_great(int cap){
		akey = (Key []) new Comparable[cap];
		aleft = new int[cap]; aright = new int[cap];
	}
	
	public void put(Key k){
		akey[count] = k;		
		
		int cmp = akey[count].compareTo(akey[0]);
		insert(cmp,0);
			
		count ++;
	}
	
	public void insert(int cmp,int ind){
		if(cmp<0){
			if(aleft[ind]==0){aleft[ind] = count; return;}
			else{
				insert(akey[count].compareTo(akey[aleft[ind]]),aleft[ind]);
			}
		} 
		else if(cmp>0){
			if(aright[ind]==0){aright[ind] = count; return;}
			else{
				insert(akey[count].compareTo(akey[aright[ind]]),aright[ind]);
			}
		}
		else {return;}
	}
	
	public void printOrder(){
		for(int i=0;i<count;i++){StdOut.print("aleft["+i+"]"+":"+aleft[i]+",");}StdOut.println("\n");
		for(int i=0;i<count;i++){StdOut.print("aright["+i+"]"+":"+aright[i]+",");}
	}
	
	public static void main(String args[]){
		Ex_3_2_41_great<String,Integer> ob = new Ex_3_2_41_great<String,Integer>(10);
		Scanner scan = new Scanner(System.in);
		try{
			StdOut.println("Please input keys:");
			String st = scan.nextLine();
			StdOut.println("Given input of strings is: "+ st);
			String delims = " ";
			String st1[]  = st.split(delims);
			for(int i=0; i<st1.length;i++){
				ob.put(st1[i]); 
			}
			ob.printOrder();
		} catch(Exception e){
			StdOut.println("Exception raised: "+ e.getMessage());
		}
	}
	
}
