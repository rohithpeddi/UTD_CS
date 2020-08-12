/**
 * 
 */
package Tries;

import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

/*************************

 * @author rohith peddi

 *************************/
/*
 * Drawing a R-way Trie
 */
public class Ex_5_2_1<Value> {
	
	private static int R;
	private Node root;
	private Alphabet lcase;
	
	public Ex_5_2_1(Scanner scan){
		lcase = new Alphabet("abcdefghijklmnopqrstuvwxyz");
		R = lcase.R();
		int N = Integer.parseInt(scan.nextLine());
		Integer i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			put(st,(Value) i);
			i++;
		}
		StdOut.println("Done adding to the tree");
		StdOut.println(get("shore"));
		drawTrie();
	}
	
	private static class Node{
		Object val;
		Node[] next = new Node[R];
	}
	
	public char charAt(String key,int d){
		return key.charAt(d);
	}
	
	public Value get(String key){
		key = lcase.toChars(lcase.toIndices(key));
		Node x = get(root,key,0);
		if(x==null) return null;
		else return (Value)x.val;
	}
	
	private Node get(Node x, String key, int d){		
		if(x==null) return null;
		if(d == key.length()) return x;
		
		char c = charAt(key,d);	
		int index = lcase.toIndex(c);
		return get(x.next[index],key,d+1);
	}
	
	public void put(String key,Value val){
		StdOut.printf("Adding: %s and %s to the root",key,val);
		StdOut.println("");
		key = lcase.toChars(lcase.toIndices(key));
		root = put(root,key,val,0);
	}
	
	private Node put(Node x,String key, Value val,int d){
		if(x==null) x=new Node();
		if(d == key.length()) {x.val =val; return x;}
		
		char c = charAt(key,d);		
		int index = lcase.toIndex(c);
		x.next[index] = put(x.next[index],key,val,d+1);	
		return x;
	}
	
	public void drawTrie(){
		int count=1;
		double lo =0.0,hi=1.0;
		double or_x = (lo+hi/2.0), or_y = (double) count;
		drawTrie(root,count,lo,hi,or_x,or_y);
	}
	
	private void drawTrie(Node x, int levelcount, double lo, double hi,double or_x,double or_y){
		
		if(x==null) return;
		
		for(int i=0; i<R; i++){
			
			if(x.next[i]!=null){					
				StdDraw.setPenRadius(.005);
				char c = lcase.toChar(i);
				double length = hi-lo;
				double diff = 1.0/(2*Math.pow(R, levelcount));
				double fraction = length* diff;
				
				double x1 = lo+((2*i+1)*fraction);
				//StdOut.println(2*Math.pow(R, levelcount)+ ":"+ levelcount);
				double y1 = levelcount/10.0;
				
				Point2D ob = new Point2D(x1,y1);
				StdOut.printf("x: %f and y:%f",x1,y1);
				StdOut.println("");
				ob.draw();
				StdDraw.text(ob.x(), ob.y(), "   "+c);
				if(x!=root){
					StdDraw.setPenRadius(.001);
					StdDraw.line(or_x, or_y, ob.x(), ob.y());
				} else {
					StdDraw.setPenRadius(.001);
					StdDraw.line(0.5, 0.0, ob.x(), ob.y());
				}
				drawTrie(x.next[i],levelcount+1,x1-fraction,x1+fraction,ob.x(),ob.y());
			}
			
		}
		
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("text1.txt"));
			Ex_5_2_1 ob = new Ex_5_2_1(scan);
		} catch(Exception e){
			e.printStackTrace();
		}
	}
	

}
