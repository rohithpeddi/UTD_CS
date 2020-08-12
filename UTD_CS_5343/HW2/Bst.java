package hw2;

import java.util.Arrays;
import java.util.List;
import java.util.Stack;

public class Bst {

    class Node {
        private Integer value;
        private Node left, right;

        public Node(Integer value){
            this.value = value;
        }

        public Integer getValue(){
            return value;
        }

        public void setValue(Integer value){
            this.value = value;
        }

        public Node getRight() {
            return right;
        }

        public void setRight(Node right) {
            this.right = right;
        }

        public Node getLeft() {
            return left;
        }

        public void setLeft(Node left) {
            this.left = left;
        }
    }

    public Node root;

    public Bst(List<Integer> values){
        init(values);
    }

    // Initialize the binary search tree with a set of values
    void init(List<Integer> values){
        for (Integer value: values) {
            insertToBst(root, value);
        }
    }

    public void insertToBst(Node node, Integer value){

        if (node == null && node == root) {
            root = new Node(value);
            return;
        }

        if (node.getValue() >= value) {
            if (node.getLeft() == null) {
                node.setLeft(new Node(value));
                return;
            }
            insertToBst(node.getLeft(), value);
        } else {
            if (node.getRight() == null){
                node.setRight(new Node(value));
                return;
            }
            insertToBst(node.getRight(), value);
        }

    }

    public void deleteNodeInBstPredecessor(Integer value){
        deleteNodeInBstPredecessor(root, value);
    }

    /**
     * Changes the following pointers
     *  1. Predecessors left is attached to predecessor parent
     *  2. Left and right children of node to be deleted are attached to predecessor
     * @param node
     * @return predecessor
     */
    public Node fetchModifiedPredecessor(Node node){
        Node predecessorParent = node.getLeft();
        Node predecessor = predecessorParent.getRight();

        if (predecessor == null) {
            predecessor = predecessorParent;
        } else {
            while (predecessor.getRight() != null){
                predecessorParent = predecessor;
                predecessor = predecessor.getRight();
            }

            predecessorParent.setRight(predecessor.getLeft());
        }

        predecessor.setRight(node.getRight());
        predecessor.setLeft(node.getLeft());

        return predecessor;
    }

    /**
     * Pointers to be considered
     *  1. parent of the parentNode,
     *  2. parent of predecessor,
     *  3. predecessor
     * @param parentNode
     * @param value
     */
    public void deleteNodeInBstPredecessor(Node parentNode, Integer value){

        // Case where the value to be deleted is root
        if (parentNode.getValue().equals(value)){
            root = fetchModifiedPredecessor(parentNode);
            return;
        }

        // Check left side of the tree
        if (parentNode.getValue() > value){
            if (parentNode.getLeft() != null) {
                // Parent node's left child is the required node to be deleted
                if (parentNode.getLeft().getValue().equals(value)){
                    Node toBeDeleted = parentNode.getLeft();
                    parentNode.setLeft(toBeDeleted.getLeft() == null ? toBeDeleted.getRight() : fetchModifiedPredecessor(toBeDeleted));
                    return;
                }
                // Else find the node in left branch
                deleteNodeInBstPredecessor(parentNode.getLeft(), value);
            }
        } else {
            // Check right side of the tree
            if (parentNode.getRight() != null) {
                // Parent node's right child is the required node to be deleted
                if (parentNode.getRight().getValue().equals(value)){
                    Node toBeDeleted = parentNode.getRight();
                    parentNode.setRight(toBeDeleted.getLeft() == null ? toBeDeleted.getRight() : fetchModifiedPredecessor(toBeDeleted));
                    return;
                }
                // Else find the node in the right branch
                deleteNodeInBstPredecessor(parentNode.getRight(), value);
            }
        }

    }

    // Inorder traversal using recursion
    public void inorderTraversalBstRecursive(Node node){

        if (node == null) return;

        inorderTraversalBstRecursive(node.getLeft());
        System.out.print(node.getValue() + ", ");
        inorderTraversalBstRecursive(node.getRight());

    }

    // Inorder traversal of binary search tree using stack
    public void inorderTraversalBst() throws Exception {

        if (root == null) throw new Exception("linked list is not properly initialised");

        Stack<Node> valueStack = new Stack<>();
        StringBuilder inorderTraversal = new StringBuilder();

        valueStack.push(root);
        Node currentNode = root;

        while(!valueStack.isEmpty()){

            if (currentNode != null){
                if (currentNode.getLeft() != null) {
                    valueStack.push(currentNode.getLeft());
                }
                currentNode = currentNode.getLeft();
            } else {
                Node topNode = valueStack.pop();
                inorderTraversal.append(topNode.getValue() + ", ");
                if (topNode.getRight() != null){
                    valueStack.push(topNode.getRight());
                    currentNode = topNode.getRight();
                }
            }

        }

        System.out.println(inorderTraversal.toString());

    }

    public static void main(String[] args) {

        System.out.println("Values added to BST : \n100, 50, 200, 150, 300, 25, 75, 12, 37, 125, 175, 250, 320, 67, 87, 94, 89, 92, 88");

        List<Integer> valuesToBeAdded = Arrays.asList(100, 50, 200, 150, 300, 25, 75, 12, 37, 125, 175, 250, 320, 67, 87, 94, 89,92,88);
        Bst binarySearchTree = new Bst(valuesToBeAdded);

        try {
            System.out.println("Inorder traversal before deletion");
            //binarySearchTree.inorderTraversalBstRecursive(binarySearchTree.root);
            binarySearchTree.inorderTraversalBst();

            // Use predecessor
            System.out.println("Deleting node with value 100");
            binarySearchTree.deleteNodeInBstPredecessor(100);

            System.out.println("Inorder traversal after deletion");
            //binarySearchTree.inorderTraversalBstRecursive(binarySearchTree.root);
            binarySearchTree.inorderTraversalBst();

        } catch (Exception e){
            e.printStackTrace();
        }

    }

}
