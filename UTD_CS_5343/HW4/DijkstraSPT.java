package hw4;

import java.util.*;

public class DijkstraSPT {

    /**
     * DirectedEdge - represents a directed edge in the graph and stores properties corresponding to it
     */
    class DirectedEdge implements Comparable<DirectedEdge> {

        private final int v,w;
        private final double weight;

        public DirectedEdge(int v, int w, double weight){
            this.v = v;
            this.w = w;
            this.weight = weight;
        }

        public int getFrom(){
            return v;
        }

        public int getTo(){
            return w;
        }

        public double getWeight(){
            return weight;
        }

        public String toString(){
            return String.format("%d - %d , %2.4f", v,w,weight);
        }

        @Override
        public int compareTo(DirectedEdge that){
            if (this.weight > that.weight) return 1;
            else if (this.weight < that.weight) return -1;
            else return 0;
        }

    }

    /**
     * EdgeWeightedDigraph - Graph representation
     * Here we use adjacency lists to represent graphs
     */
    class EdgeWeightedDigraph {

        private int V, E;
        private List<DirectedEdge>[] adj;

        public EdgeWeightedDigraph(int V){
            this.V = V;
            adj = new List[V];
            for (int i=0; i<V; i++){
                adj[i] = new ArrayList<DirectedEdge>();
            }
        }

        public void addEdge(DirectedEdge edge){
            int v = edge.getFrom();
            adj[v].add(edge);
            E++;
        }

        public List<DirectedEdge> adj(int v){
            return adj[v];
        }

        public List<DirectedEdge> edges(){
            List<DirectedEdge> allEdges = new ArrayList<DirectedEdge>();
            for(int i=0; i<V; i++){
                for(DirectedEdge e:adj(i)){
                    allEdges.add(e);
                }
            }
            return allEdges;
        }

        public int V(){
            return V;
        }

        public int E(){
            return E;
        }

        public String toString(){
            String str="";
            str+= "Vertices: "+ V+", Edges:" +E+"\n";
            for(int i=0; i<V; i++){
                str+= i +":";
                for(DirectedEdge e:adj[i]){
                    int w = e.getTo(); double weight = e.getWeight();
                    str += String.format("-(%d, %2.2f)", w,weight);
                }
                str+="\n";
            }
            return str;
        }

    }

    /************************************************
     IndexMinPQ - Priority Queue which stores
     just the minimum corresponding to a vertex
     and a global minimum can be extracted in - O(logV)
     *************************************************/

    class IndexMinPQ<Key extends Comparable<Key>> {

        private int N;
        private int[] pq,qp;
        private Key[] keys;

        public IndexMinPQ(int cap){
            pq = new int[cap+1]; qp = new int[cap+1];
            keys = (Key[]) new Comparable[cap+1];
            for(int i=0; i<cap+1;i++)
                qp[i] =-1;
        }

        public boolean isEmpty(){return N==0;}
        public int size() { return N;}
        public boolean contains(int k){	return qp[k]!=-1;}

        public void insert(int k, Key key){
            N++; qp[k] = N; pq[qp[k]] = k;
            keys[k] = key;
            swim(N);
        }

        public void change(int k, Key key){
            Key current = keys[k];
            if(current.compareTo(key)>0){
                keys[k] = key; sink(k);
            } else if(current.compareTo(key)<0){
                keys[k] =key; swim(k);
            }
        }

        public Key min(){
            return keys[pq[1]];
        }

        public int delMin(){
            int indexOfMin = pq[1];
            exch(1,N--);
            sink(1);
            keys[pq[N+1]] = null;
            qp[pq[N+1]] = -1;
            return indexOfMin;
        }

        private boolean greater(int i, int j){
            return keys[pq[i]].compareTo(keys[pq[j]]) >0;
        }

        private void exch(int i, int j){
            int swap = pq[i]; pq[i]=pq[j]; pq[j]= swap;
            qp[pq[i]]=i; qp[pq[j]]=j;
        }

        private void swim(int k){
            while(k>1 && greater(k/2 , k)){
                exch(k/2,k); k = k/2;
            }
        }

        private void sink(int k){
            while(2*k<=N){
                int j = 2*k;
                if(j<N && greater(j,j+1)) j++;
                if(!greater(k,j)) break;
                exch(k,j);
                k=j;
            }
        }
    }

    /************************************************
     Dijkstra- Computes shortest path from a single
     source to all vertices - Relaxing edges is the
     core step of the dijkstra's algorithm
     Maximum number of edges pq can contain is E
     And for each extraction - finds minimum in logV
     Worst case - O(ElogV)
     *************************************************/

    class Dijkstra{

        public DirectedEdge[] edgeTo;
        public double[] distTo;
        public IndexMinPQ<Double> pq;

        public Dijkstra(EdgeWeightedDigraph G, int s){

            edgeTo = new DirectedEdge[G.V()];
            distTo = new double[G.V()];
            pq = new IndexMinPQ<Double>(G.V());

            Arrays.fill(distTo, Double.POSITIVE_INFINITY);
            distTo[s]=0;

            pq.insert(s,0.0);

            System.out.println("Dijkstra initiated");
            while(!pq.isEmpty()){
                relax(G,pq.delMin());
            }

        }

        public void relax(EdgeWeightedDigraph G, int v){
            for(DirectedEdge directedEdge : G.adj(v)){
                int w = directedEdge.getTo();
                if(distTo[w]>distTo[v]+directedEdge.getWeight()){
                    distTo[w] = distTo[v]+directedEdge.weight; edgeTo[w]=directedEdge;
                    if(pq.contains(w)) pq.change(w,distTo[w]);
                    else pq.insert(w,distTo[w]);
                }
            }
        }

        public double distTo(int v){ return distTo[v];}

        public boolean hasPathTo(int v){
            return distTo[v]<Double.POSITIVE_INFINITY;
        }

        public void printSPTEdges(){
            for(int i=0; i<edgeTo.length; i++){
                if (edgeTo[i]!=null) {
                    System.out.println(String.format("%d ---> %d , distance from source 0 : %2.2f ", edgeTo[i].getFrom(), i, distTo[i]));
                }
            }
        }

    }

    public DijkstraSPT(int V){

        EdgeWeightedDigraph edgeWeightedDigraph = new EdgeWeightedDigraph(V);
        for (int i=0; i<V; i++){
            List<Integer> toVerticesList = new ArrayList<>();
            for (int j=0; j < V/2; j++){
                int toVertex = (int) (Math.random()*V);
                if (toVerticesList.contains(toVertex) || toVertex==i) continue;
                double weight = Math.random()*10;
                DirectedEdge directedEdge = new DirectedEdge(i, toVertex, weight);
                edgeWeightedDigraph.addEdge(directedEdge);
                toVerticesList.add(toVertex);
            }
        }

        System.out.println("Created Edge Weighted Digraph is : ");
        System.out.println(edgeWeightedDigraph.toString());

        System.out.println("Running Dijkstra algorithm from the vertex 0 ");
        Dijkstra dijkstra = new Dijkstra(edgeWeightedDigraph, 0);

        System.out.println("Shortest path tree has the following edges");
        dijkstra.printSPTEdges();
    }

    public static void main(String[] args) {
        DijkstraSPT dijkstraSPT = new DijkstraSPT(20);
    }

}
