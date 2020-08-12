package hw1;

public class LinkedListSort {

    class Node {

        private Integer value;
        private Node next;

        public Node getNext(){
            return next;
        }

        public Integer getValue(){
            return value;
        }

        public void setNext(Node nextNode){
            this.next = nextNode;
        }

        public void setValue(Integer value){
            this.value = value;
        }

    }

    public Node head;
    public int listSize = 15;

    public LinkedListSort(){
        init();
    }

    void init(){
        head = new Node();
        Node currentNode = head;
        for (int i=1; i<=listSize; i++){
            currentNode.setValue((int) (Math.random()*100));
            if (i<listSize) {
                Node nextNode = new Node();
                currentNode.setNext(nextNode);
                currentNode = nextNode;
            }
        }
    }

    void trace(){
        Node currentNode = head;
        StringBuffer stringBuffer = new StringBuffer();
        while(currentNode != null) {
            stringBuffer.append(currentNode.getValue() + ", ");
            currentNode = currentNode.getNext();
        }
        System.out.println(stringBuffer.toString());
    }

    boolean isSorted(){

        Node currentNode = head;
        while(currentNode.getNext() != null) {
            if (currentNode.getNext().getValue() < currentNode.getValue()) return false;
            currentNode = currentNode.getNext();
        }

        return true;
    }

    void sort() throws Exception {

        if (head == null) throw new Exception("linked list is not properly initialised");

        Node startNode = head;
        Node startNodePrev = head;

        while(startNode != null){

            Node minNodePrev = startNodePrev;
            Node currentNode = startNode;

            // Finding the node before the minimum value node
            while(currentNode.getNext() != null){
                minNodePrev = currentNode.getNext().getValue() < minNodePrev.getNext().getValue() ? currentNode : minNodePrev;
                currentNode = currentNode.getNext();
            }

            // Found minimum value at the starting position,
            // No need to unlink and link, just increment the start pointer
            if (minNodePrev == startNodePrev) {
                startNodePrev = startNodePrev.getNext();
                startNode = startNodePrev.getNext();
            } else {
                Node minNode = minNodePrev.getNext();
                minNodePrev.setNext(minNode.getNext());

                minNode.setNext(startNode);

                // If minimum value has to be placed at the start
                if (startNode == head && startNodePrev == head) {
                    head = minNode;
                    startNodePrev = head;
                } else {
                    startNodePrev.setNext(minNode);
                    startNodePrev = startNodePrev.getNext();
                }

                startNode = startNodePrev.getNext();
            }

        }

    }

    public static void main(String[] args){

        LinkedListSort linkedListSort = new LinkedListSort();

        // Printing before sorting
        System.out.println("BEFORE SORTING : ");
        linkedListSort.trace();

        // Sort method call
        try {
            linkedListSort.sort();
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        // Printing after sorting
        System.out.println("AFTER SORTING : ");
        linkedListSort.trace();

        // Checking if linkedlist is sorted or not
        System.out.println("Is linked list sorted ? " + linkedListSort.isSorted());

    }


}
