package ShortestPaths;

public class DirectedEdge implements Comparable<DirectedEdge>{
	
	private final int v,w;
	private final double weight;
	
	public DirectedEdge(int v, int w, double weight){
		this.v = v; this.w = w; this.weight = weight;
	}
	
	public int to(){
		return w;
	}
	
	public int from(){
		return v;
	}
	
	public double weight(){
		return weight;
	}
	
	public String toString(){
		return String.format("%d - %d , %2.4f", v,w,weight);
	}

	@Override
	public int compareTo(DirectedEdge that) {
		if(this.weight > that.weight ) return 1;
		else if(this.weight < that.weight) return -1;
		else return 0;
	}

}
