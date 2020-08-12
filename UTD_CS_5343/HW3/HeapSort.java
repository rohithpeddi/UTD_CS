package hw3;

import java.util.Arrays;

public class HeapSort {

    int[] heapArray;
    int heapSize;

    public HeapSort(int N){
        this.heapSize = N;
        heapArray = fetchCompleteTreeArray(generateRandomArray(N));
    }


    public int[] generateRandomArray(int N){

        int[] randomArray = new int[N+1];
        randomArray[0] = N;
        for (int i=1; i<=N; i++){
            boolean isRandomNullNode = (i < (int)(Math.random()*N + 1));
            if (!isRandomNullNode) {
                randomArray[i] = (int) (Math.random() * 100 + 1);
            } else {
                randomArray[i] = -1;
            }
        }

        System.out.println("Generated random array : " );
        System.out.println(Arrays.toString(randomArray));

        return randomArray;
    }

    public int[] fetchCompleteTreeArray(int[] treeArray){

        int number = (int) Arrays.stream(treeArray).filter(i -> i!=-1).count();

        int[] completeTreeArray = new int[number];

        for (int i=0, j=0; i< treeArray.length; i++){
            if (treeArray[i] != -1) {
                completeTreeArray[j++] = treeArray[i];
            }
        }

        completeTreeArray[0] = number-1;

        System.out.println("Generated complete tree array from random array : " );
        System.out.println(Arrays.toString(completeTreeArray));

        return completeTreeArray;
    }

    public void swap(int[] heapArray, int i, int j){
        int temp = heapArray[i];
        heapArray[i] = heapArray[j];
        heapArray[j] = temp;
    }

    // Using MaxHeap
    public void percolateUp(int[] heapArray, int index){
        while (true){
            if(heapArray[index] > heapArray[index/2] && index/2 >= 1 ){
                swap(heapArray, index, index/2);
                index = index/2;
            } else {
                break;
            }
        }
    }

    public void percolateDown(int[] heapArray, int index, int maxLength){
        while (index*2 <= maxLength){
            int maxChild = index*2;
            if ((index*2+1) <= maxLength){
                if (heapArray[index*2+1] > heapArray[index*2]) maxChild = index*2+1;
            }

            if (heapArray[index] < heapArray[maxChild]){
                swap(heapArray, index, maxChild);
                index = maxChild;
            } else {
                break;
            }
        }
    }

    public void heapify(int[] heapArray){
        for (int i=heapArray[0]/2; i>0; i--){
            percolateDown(heapArray, i, heapArray.length-1);
        }
    }

    public void sort(int[] heapArray){
        for (int i=0; i < heapArray[0]; i++){
            swap(heapArray, 1, heapArray[0]-i);
            percolateDown(heapArray, 1, heapArray[0]-i-1);
        }
    }

    public static void main(String[] args) {
        HeapSort heapSort = new HeapSort(20);
        int[] heapArray = heapSort.heapArray;

        System.out.println("Array before converting into a heap : " );
        System.out.println(Arrays.toString(heapArray));

        heapSort.heapify(heapArray);
        System.out.println("Array after converting into a heap : " );
        System.out.println(Arrays.toString(heapArray));

        heapSort.sort(heapArray);
        System.out.println("Array after sorting the heap : " );
        System.out.println(Arrays.toString(heapArray));

    }

}
