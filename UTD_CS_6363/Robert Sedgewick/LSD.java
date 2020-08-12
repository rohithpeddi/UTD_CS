/**
 * 
 */
package StringSorts;

import java.io.File;
import java.io.PrintWriter;
import java.util.Scanner;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

/*************************

 * @author rohith peddi

 *************************/
public class LSD {
	
	/***************GENERATE RANDOM STRINGS*****************/
	
	public void randString(int N, int W){
		
		String s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		String n = "0123456789";
		
		try{
			
			PrintWriter pw = new PrintWriter(new File("2000_10strings.txt"));
			
			pw.println(N+"");
			pw.println(W+"");
			
			for(int i=0; i<N; i++){
				String str="";
				
				for(int j=0; j<W; j++){
					
					if(j==5 || j==6 ||j==2||j==1){
						int num = StdRandom.uniform(0, 9);
						str+= n.charAt(num);
					}
					else{
						int num = StdRandom.uniform(0, 26);
						str+= s.charAt(num);
					}
					
				}
				pw.println(str);
				StdOut.println(str);			
				
			}
			
			pw.flush();
			
		} catch(Exception e){
			e.printStackTrace();
		}
		
		
	}
	
	/***************CONSTRUCTOR*****************/
	
	public LSD(Scanner scan){
		
		int N = Integer.parseInt(scan.nextLine()),W = Integer.parseInt(scan.nextLine());
		
		String[] a = new String[N];int i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			a[i++]=st;
		}
		
		sort(a,W);
		
		for(int j=0; j<N; j++){
			StdOut.println(a[j]);
		}
		
	}
	
	/***************SORT IMPLEMENTATION*****************/
	
	public void sort(String[] a, int W){
		int N = a.length,R = 256;
		String[] aux = new String[N];
		
		for(int d = W-1; d>=0; d--){
			
			int[] count = new int[R+1];
			
			for(int i=0; i<N; i++){
				count[a[i].charAt(d)+1]++;
			}
			
			for(int r=0;r<R; r++ ){
				count[r+1]+=count[r];
			}
			
			for(int i=0;i<N; i++){
				aux[count[a[i].charAt(d)]++] = a[i];
			}
			
			for(int i=0; i<N; i++){
				a[i]=aux[i];
			}
			
		}
		
	}
	
	/***************MAIN METHOD*****************/
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("2000_10strings.txt"));
			LSD ob = new LSD(scan);
			scan.close();
			
		} catch(Exception e){
			e.printStackTrace();
		}
		
	}

}
