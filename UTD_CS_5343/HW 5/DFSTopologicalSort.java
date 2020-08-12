package hw5;

import hw4.DijkstraSPT;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DFSTopologicalSort {

    class Digraph {

        int N;
        int[][] adjacencyMatrix;

        public Digraph(int N){
            this.N = N;
            this.adjacencyMatrix = new int[N][N];
        }

        public void addDirectedEdge(int v, int w){
            adjacencyMatrix[v][w] = 1;
        }

        public List<Integer> adj(int v){
            List<Integer> adjacencyList = new ArrayList<>();
            for(int i=0; i<N; i++){
                if(adjacencyMatrix[v][i] == 1) {
                    adjacencyList.add(i);
                }
            }
            return adjacencyList;
        }

        public int getN(){
            return N;
        }

        public int[][] getAdjacencyMatrix(){
            return adjacencyMatrix;
        }

        public String toString(){
            String str="";
            str+= "Vertices: "+ N+"\n";
            for(int i=0; i<N; i++){
                str+= i +":";
                for(int j=0; j<N; j++){
                    if (adjacencyMatrix[i][j] == 1) {
                        str += j + ", ";
                    }
                }
                str+="\n";
            }
            return str;
        }

    }

    class Top {

        int N, currentIndex;
        int[] outgoingEdgesCount, topologicalOrder;
        boolean[] marked;
        Digraph digraph;
        int[][] adjacencyMatrix;

        public Top(Digraph digraph){
            this.N = digraph.getN();
            this.currentIndex = N-1;
            this.digraph = digraph;
            this.adjacencyMatrix = digraph.getAdjacencyMatrix();
            topologicalOrder = new int[N];
            outgoingEdgesCount = new int[N];
            marked = new boolean[N];
            int[][] adjacencyMatrix = digraph.getAdjacencyMatrix();
            for (int i=0; i<N; i++){
                for (int j=0; j<N; j++){
                    if (adjacencyMatrix[i][j] == 1) {
                        outgoingEdgesCount[i]++;
                    }
                }
            }
        }

        public void topologicalSort(){

            while(true) {

                int v = fetchVertexWithNoOutgoingEdges();

                if (v == -1) {
                    System.out.println("Detected cycle in the graph, halting the procedure to find topological order");
                    break;
                }

                marked[v] = true;
                topologicalOrder[currentIndex] = v;
                currentIndex--;

                removeVertex(v);

            }

            printTopologicalOrder();

        }

        public void removeVertex(int v){

            for (int j=0; j<N; j++){
                if (adjacencyMatrix[j][v] == 1) {
                    outgoingEdgesCount[j]--;
                }
            }

        }

        public int fetchVertexWithNoOutgoingEdges(){
            for (int i=0; i<N; i++){
                if (outgoingEdgesCount[i] == 0 && !marked[i]){
                    return i;
                }
            }
            return -1;
        }

        public void printTopologicalOrder(){
            System.out.println("Topological Order : ");
            for (int i=0; i<N; i++){
                System.out.print( (i<N-1) ? topologicalOrder[i] + " ---> " : topologicalOrder[i]);
            }
        }

    }

    class Topological {

        int N, currentIndex;
        int[] topologicalOrder, topologicalOrderIndex;
        boolean[] marked, onStack;
        Digraph digraph;
        boolean hasCycle;

        public Topological(Digraph digraph){
            this.digraph = digraph;
            this.N = digraph.getN();
            this.currentIndex = N-1;
            this.topologicalOrder = new int[N];
            this.topologicalOrderIndex = new int[N];
            Arrays.fill(topologicalOrderIndex, -1);
            this.marked = new boolean[N];
            this.onStack = new boolean[N];
        }

        public void topologicalSort(){

            for (int i=0; i< N; i++){
                if (!marked[i]){
                    dfsTopologicalSort(0);
                }
            }

            if (hasCycle) {
                System.out.println("Directed Graph has cycle, Quit the process of topological sorting");
                System.out.println("Topologically ordered vertices till we find a cycle are");
            } else {
                System.out.println("Performed topological sorting on the graph and following are the vertices");
            }

            printTopologicalOrdering();

        }

        public void dfsTopologicalSort(int v){

            marked[v] = true; onStack[v] = true;

            for (int w : digraph.adj(v)){

                if (hasCycle) return;

                if (!marked[w]) {
                    dfsTopologicalSort(w);
                } else if (onStack[w]){
                    hasCycle = true;
                    return;
                }

            }

            topologicalOrder[v] = currentIndex;
            topologicalOrderIndex[currentIndex] = v;
            currentIndex--;

            onStack[v] = false;
        }

        public int[] getTopologicalOrderIndex(){
            return topologicalOrderIndex;
        }

        public void printTopologicalOrdering(){
            System.out.println(Arrays.toString(topologicalOrderIndex));
            System.out.println("---------------------------------------------------------------------------------------------------");
        }

    }

    public DFSTopologicalSort(int V){

        // Generate Acyclic DAG and produce topological ordering with DFS
        Digraph acyclicDigraph = generateAcyclicDigraph(V);
        System.out.println(acyclicDigraph.toString());
        Topological dagTopological = new Topological(acyclicDigraph);
        dagTopological.topologicalSort();

        // Generate Cyclic Graph and compute the topological ordering until it detects a cycle
        Digraph cyclicDigraph = generateCyclicDigraph(V);
        System.out.println(cyclicDigraph.toString());
        Topological cyclicTopological = new Topological(cyclicDigraph);
        cyclicTopological.topologicalSort();

    }

    public Digraph generateAcyclicDigraph(int V){
        Digraph acyclicDigraph = new Digraph(V);
        acyclicDigraph.addDirectedEdge(0,1);
        acyclicDigraph.addDirectedEdge(0,8);
        acyclicDigraph.addDirectedEdge(0,9);
        acyclicDigraph.addDirectedEdge(0,3);
        acyclicDigraph.addDirectedEdge(1,2);
        acyclicDigraph.addDirectedEdge(1,3);
        acyclicDigraph.addDirectedEdge(1,4);
        acyclicDigraph.addDirectedEdge(2,4);
        acyclicDigraph.addDirectedEdge(2,6);
        acyclicDigraph.addDirectedEdge(4,5);
        acyclicDigraph.addDirectedEdge(4,6);
        acyclicDigraph.addDirectedEdge(4,7);
        acyclicDigraph.addDirectedEdge(5,7);
        acyclicDigraph.addDirectedEdge(6,7);
        acyclicDigraph.addDirectedEdge(3,5);
        acyclicDigraph.addDirectedEdge(3,9);
        acyclicDigraph.addDirectedEdge(8,9);
        acyclicDigraph.addDirectedEdge(9,7);
        return acyclicDigraph;
    }

    public Digraph generateCyclicDigraph(int V){
        Digraph cyclicDigraph = new Digraph(V);
        cyclicDigraph.addDirectedEdge(0,1);
        cyclicDigraph.addDirectedEdge(0,8);
        cyclicDigraph.addDirectedEdge(9,0);
        cyclicDigraph.addDirectedEdge(0,3);
        cyclicDigraph.addDirectedEdge(1,2);
        cyclicDigraph.addDirectedEdge(1,3);
        cyclicDigraph.addDirectedEdge(1,4);
        cyclicDigraph.addDirectedEdge(2,4);
        cyclicDigraph.addDirectedEdge(2,6);
        cyclicDigraph.addDirectedEdge(4,5);
        cyclicDigraph.addDirectedEdge(4,6);
        cyclicDigraph.addDirectedEdge(4,7);
        cyclicDigraph.addDirectedEdge(5,7);
        cyclicDigraph.addDirectedEdge(6,7);
        cyclicDigraph.addDirectedEdge(3,5);
        cyclicDigraph.addDirectedEdge(3,9);
        cyclicDigraph.addDirectedEdge(8,9);
        return cyclicDigraph;
    }

    public Digraph randomCyclicDigraph(int V){
        Digraph cyclicDigraph = new Digraph(V);
        for (int i=0; i<V; i++){
            List<Integer> toVerticesList = new ArrayList<>();
            for (int j=0; j < V/2; j++){
                int toVertex = (int) (Math.random()*V);
                if (toVertex == i) continue;
                cyclicDigraph.addDirectedEdge(i, toVertex);
            }
        }
        return cyclicDigraph;
    }

    public static void main(String[] args) {
        DFSTopologicalSort dfsTopologicalSort = new DFSTopologicalSort(10);
    }

}
