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
public class Ex_5_2_2<Value> {
	
	private Node root;
	
	public Ex_5_2_2(Scanner scan){
		int N = Integer.parseInt(scan.nextLine());
		Integer i=0;
		while(scan.hasNextLine()){
			String st = scan.nextLine();
			put(st,(Value) i);
			i++;
		}
		StdOut.println("Done adding to the tree");
		StdOut.println(get("shore"));
		
		drawTST();
	}
	
	private class Node{
		char c; 
		Node left,mid,right;
		Object val;
	}
	
	public Value get(String key){
		Node x = get(root,key,0);
		if(x==null) return null;
		else return (Value)x.val;
	}
	
	private Node get(Node x, String key, int d){
		if(x==null) return null;
		if(d == key.length()) return x;
		
		char c = key.charAt(d);
		if(c<x.c) return get(x.left,key,d);
		else if(c>x.c) return get(x.right,key,d);
		else if(d<key.length()-1) return get(x.mid,key,d+1);
		else return x;
	}
	
	public void put(String key, Value val){
		root = put(root,key,val,0);
	}
	
	private Node put(Node x, String key, Value val, int d){
		char c = key.charAt(d);
		if(x==null){ x = new Node(); x.c = c;}
		
		if(c<x.c) x.left = put(x.left,key,val,d);
		else if(c>x.c) x.right = put(x.right,key,val,d);
		else if(d<key.length()-1) x.mid = put(x.mid,key,val,d+1);
		else x.val =val;
		return x;		
	}
	
	public void drawTST(){
		double lo=0.0,hi=1.0,or_x=0.5,or_y = 0.0;
		double level = 1;
		drawTST(root,level,lo,hi,or_x,or_y);
	}
	
	private void drawTST(Node x,double levelcount ,double lo, double hi, double or_x,double or_y){
		
		if(x==null) return;
		
		double length = hi-lo;
		double diff = 1.0/6.0;
		double fraction = length* diff;
		
		int i=0;
		
		if(x.left!=null){
			i=1;
			char c = x.left.c;
			double x1 = lo+(i*fraction);
			double y1 = levelcount/10.0;
			Point2D ob = new Point2D(x1,y1);
			StdOut.printf("x: %f and y:%f",x1,y1);
			StdOut.println("  "+c);
			ob.draw();
			StdDraw.text(ob.x(), ob.y(), "   "+c);
			
			StdDraw.setPenRadius(.001);
			StdDraw.line(or_x, or_y, ob.x(), ob.y());
		
			drawTST(x.left,levelcount+1,x1-fraction,x1+fraction,ob.x(),ob.y());
			
		} 
		
		if(x.right !=null){
			i=3;
			char c = x.right.c;
			double x1 = lo+(i*fraction);
			double y1 = levelcount/10.0;
			Point2D ob = new Point2D(x1,y1);
			StdOut.printf("x: %f and y:%f",x1,y1);
			StdOut.println("  "+c);
			ob.draw();
			StdDraw.text(ob.x(), ob.y(), "   "+c);
			
			StdDraw.setPenRadius(.001);
			StdDraw.line(or_x, or_y, ob.x(), ob.y());
		
			drawTST(x.right,levelcount+1,x1-fraction,x1+fraction,ob.x(),ob.y());
			
		} 
		
		if(x.mid !=null){
			i=5;
			char c = x.mid.c;
			double x1 = lo+(i*fraction);
			double y1 = levelcount/10.0;
			Point2D ob = new Point2D(x1,y1);
			StdOut.printf("x: %f and y:%f",x1,y1);
			StdOut.println("  "+c);
			ob.draw();
			StdDraw.text(ob.x(), ob.y(), "   "+c);
			
			StdDraw.setPenRadius(.001);
			StdDraw.line(or_x, or_y, ob.x(), ob.y());
		
			drawTST(x.mid,levelcount+1,x1-fraction,x1+fraction,ob.x(),ob.y());
		}
		
		return;
	}
	
	public static void main(String args[]){
		try{
			Scanner scan = new Scanner(new File("text.txt"));
			Ex_5_2_2 ob = new Ex_5_2_2(scan);
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
