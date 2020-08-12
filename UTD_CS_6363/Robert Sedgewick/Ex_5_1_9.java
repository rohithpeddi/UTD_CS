/**
 * 
 */
package StringSorts;

import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/

//LSD Implementation of variable length strings

public class Ex_5_1_9 {
	
	public Ex_5_1_9(Scanner scan){
		
		int N = Integer.parseInt(scan.nextLine());
		
		String[] a = new String[N];int i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			a[i++]=st;
		}
		
		sort(a,6);
		
		//for(int j=0; j<N; j++){ StdOut.println(a[j]);}
		
	}
	
	private int charAt(String st, int d){
		if(d<st.length()) return st.charAt(d);
		else return -1;
	}
	
	public void sort(String[] a, int W){
		
		int N = a.length,R=256;
		String[] aux = new String[N];
		
		for(int d=W-1; d>=0; d--){
			
			StdOut.println("she sells sea shells on the sea shore ");
			
			for(int i=0; i<N; i++){
				StdOut.print(a[i]+" ");
			}
			StdOut.println("\n");
			
			int[] count = new int[R+2];
			
			for(int i=0; i<N; i++){
				count[charAt(a[i],d)+2]++;
			}
			
			for(int i=0; i<R+2; i++){
				StdOut.print(count[i]+" ");
			}
			StdOut.println("");
			
			for(int r=0;r<R; r++ ){
				count[r+1]+=count[r];
			}
			
			for(int i=0; i<R+2; i++){
				StdOut.print(count[i]+" ");
			}
			StdOut.println("\n");
			
			for(int i=0;i<N; i++){
				aux[count[charAt(a[i],d)+1]++] = a[i];
			}
			
			for(int i=0; i<N; i++){
				a[i]=aux[i];
			}
		}
		
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("text.txt"));
			Ex_5_1_9 ob = new Ex_5_1_9(scan);
			scan.close();
			
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
