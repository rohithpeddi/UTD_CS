import java.io.File;
import java.util.Scanner;

import edu.princeton.cs.algs4.Queue;
import edu.princeton.cs.algs4.StdOut;

public class Database {
	
	public LinearProbingHashST<String,Queue<String>> film;
	public LinearProbingHashST<String,Queue<String>> actor;
	
	private Scanner scan =null;
	
	/***************** CONSTRUCTOR ******************/
	//Adding all the values to the database in the constructor itself
	
	public Database(){
		
		film = new LinearProbingHashST<String,Queue<String>>(16);
		actor = new LinearProbingHashST<String,Queue<String>>(16);
		String delims = "/";
		
		try{
			scan =  new Scanner(new File("movies.txt"));
			while(scan.hasNextLine()){
				
				String line = scan.nextLine();				
				String[] details = line.split(delims);
				String movie_name = details[0];
				
				for(int i=1;i<details.length;i++){						
					String cast_details = details[i];
					
					if(!film.contains(movie_name)) film.put(movie_name, new Queue<String>());
					if(!actor.contains(cast_details)) actor.put(cast_details, new Queue<String>()); 
					
					film.get(movie_name).enqueue(cast_details);
					actor.get(cast_details).enqueue(movie_name);	
					if(i==details.length-1) StdOut.println(cast_details);
				}
			}
			
		} catch(Exception e){
			StdOut.println("Exception raised! : "+ e.getMessage());
		}
	}
	
	public static void main(String args[]){
		Database ob = new Database();
	}

}
