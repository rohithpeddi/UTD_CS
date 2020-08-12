package MinimumSpanningTrees;

public class Edge implements Comparable<Edge> {
	
	private final int v,w;
	private final double weight;
	
	public Edge(int v, int w, double weight){
		this.v = v; this.w=w; this.weight = weight;
	}
	
	public double weight(){return this.weight;}
	public int either(){	return v;}
	public int other(int o){
		if(o == v) return w;
		else if(o==w) return v;
		else throw new RuntimeException("Invalid choice of vertex!");		
	}

	@Override
	public int compareTo(Edge that) {
		if(this.weight<that.weight) return -1;
		else if(this.weight> that.weight) return 1;
		else return 0;
	}
	
	public String toString(){
		return String.format("%d - %d, weight: %0.2f ", v,w,weight);
	}

}
