package hw6;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public class HashTable {

    class CollisionStatistics {

        String key;
        Integer linearProbeCollisions, quadraticProbeCollisions;

        public CollisionStatistics(String key){
            this.key = key;
        }

        public Integer getLinearProbeCollisions() {
            return linearProbeCollisions;
        }

        public void setLinearProbeCollisions(Integer linearProbeCollisions) {
            this.linearProbeCollisions = linearProbeCollisions;
        }

        public Integer getQuadraticProbeCollisions() {
            return quadraticProbeCollisions;
        }

        public void setQuadraticProbeCollisions(Integer quadraticProbeCollisions) {
            this.quadraticProbeCollisions = quadraticProbeCollisions;
        }

    }

    String[] linearProbingKeys, quadraticProbingKeys;
    int size, counter, R = 31;
    List<CollisionStatistics> collisionStatisticsList;

    public HashTable(){
        this.size = 53;
        this.counter = 0;
        this.linearProbingKeys = new String[size];
        this.quadraticProbingKeys = new String[size];
        this.collisionStatisticsList = new ArrayList<>();
    }

    public void resize(){

        int modifiedSize = fetchNextPrime(size * 2);
        List<String> previouslyAddedKeys = Arrays.asList(linearProbingKeys);

        System.out.println(" =================================================================================================== ");
        System.out.println("\n\n\n");
        System.out.println("Increasing hash table size to : " + modifiedSize + ", from current size : " + size);
        System.out.println("\n\n\n");
        System.out.println(" =================================================================================================== ");

        this.linearProbingKeys = new String[modifiedSize];
        this.quadraticProbingKeys = new String[modifiedSize];

        size = modifiedSize;

        this.counter = 0;
        for (String key: previouslyAddedKeys) {
            if (key != null) {
                insert(key);
            }
        }
    }

    public Integer fetchHash(String key){
        int hash = 0;
        for (int i = 0; i < key.length(); i++)
            hash = (R * hash + key.charAt(i)) % size;

        return (hash & 0x7fffffff) % size;
    }

    public int fetchNextPrime(int size){

        int[] primeArray = new int[]{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277};

        for (int i=0; i<primeArray.length; i++){
            if (primeArray[i]>size) return primeArray[i];
        }

        return size;
    }

    public boolean insert(String key){

        int hash = fetchHash(key), linearProbe = 1, quadraticProbe = 2;

        if (((double)counter/(double)size) > 0.5) {
            resize();
        }

        CollisionStatistics collisionStatistics = new CollisionStatistics(key);

        // ---------------------- LINEAR PROBING HASH TABLE INSERT -------------------------

        int probeCounter=0, currentIndex = hash;
        while (true) {
            if (linearProbingKeys[currentIndex] != null) {
                probeCounter++;
            } else if (probeCounter < 50){  // Hard Limit
                linearProbingKeys[currentIndex] = key;
                break;
            } else {
                System.out.println("Crossed the hard limit of 50 probes while inserting into table corresponding to linear probing");
                break;
            }
            currentIndex = (hash + (int) Math.pow(probeCounter, linearProbe)) % size;
        }

        collisionStatistics.setLinearProbeCollisions(probeCounter);
        String statistics = "WORD " + key + ", LINEAR PROBE " + probeCounter ;

        // ---------------------- QUADRATIC PROBING HASH TABLE INSERT -------------------------

        probeCounter=0; currentIndex = hash;
        while (true) {
            if (quadraticProbingKeys[currentIndex] != null) {
                probeCounter++;
            } else if (probeCounter < 50){  // Hard Limit
                quadraticProbingKeys[currentIndex] = key;
                break;
            } else {
                System.out.println("Crossed the hard limit of 50 probes while inserting into table corresponding to quadratic probing");
                break;
            }
            currentIndex = (hash + (int) Math.pow(probeCounter, quadraticProbe)) % size;
        }

        collisionStatistics.setQuadraticProbeCollisions(probeCounter);
        statistics += ", QUADRATIC PROBE : " + probeCounter;
        System.out.println(statistics);

        collisionStatisticsList.add(collisionStatistics);

        counter++;
        return (probeCounter > 0);

    }

    public void generateRandomWords(int number, String fileName){
        try {
            // Creation of file if not present
            File file = new File(fileName);
            BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(file));

            // Add randomly generated words to the file
            Random random = new Random();
            for (int i=0; i< number; i++){
                int characterLength = random.nextInt(5) + 3; // Considering words from length 3 to 8
                char[] word = new char[characterLength];
                for(int j = 0; j < word.length; j++) {
                    word[j] = (char)('a' + random.nextInt(26));
                }
                bufferedWriter.write(new String(word));
                bufferedWriter.newLine();
            }

            bufferedWriter.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void addWordsToHashTable(String fileName) {

        try {
            File file = new File(fileName);
            BufferedReader br = new BufferedReader(new FileReader(file));

            String string;
            while ((string = br.readLine()) != null) {
                insert(string);
            }

            printCollisionStatistics();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void printCollisionStatistics(){

        int linearProbeCollisions = 0, quadraticProbeCollisions = 0, insertSize = collisionStatisticsList.size();

        for (CollisionStatistics collisionStatistics : collisionStatisticsList) {
            linearProbeCollisions += collisionStatistics.getLinearProbeCollisions();
            quadraticProbeCollisions += collisionStatistics.getQuadraticProbeCollisions();
        }

        System.out.println("Total number of collisions incurred in inserting " + counter + " keys is, linear probe method : " + linearProbeCollisions + ", quadratic probe method " + quadraticProbeCollisions);

    }

    public void startUserSession(){
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
            while (true) {
                String input = br.readLine();
                if (input.equals("q")) {
                    System.out.println("EXITING THE SESSION");
                    break;
                }
                readKeyAndPrintStatistics(input);
            }
            br.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public void readKeyAndPrintStatistics(String key){

        int hash = fetchHash(key);
        boolean isFound = false;

        int probeCounter = 0, currentIndex = hash, linearProbe = 1, quadraticProbe = 2;
        while(true) {
            if (linearProbingKeys[currentIndex] != null && linearProbingKeys[currentIndex].equals(key)){
                isFound = true;
                break;
            } else if (linearProbingKeys[currentIndex] == null) {
                break;
            } else {
                probeCounter++;
                currentIndex = (hash + (int) Math.pow(probeCounter, linearProbe)) % size;
            }
        }

        String statistics = ( isFound ? "FOUND " : "NOT FOUND " ) + key + ", LINEAR PROBE " + probeCounter ;

        probeCounter = 0; currentIndex = hash;
        while(true && isFound) {
            if (quadraticProbingKeys[currentIndex].equals(key)){
                break;
            } else if (quadraticProbingKeys[currentIndex] == null) {
                break;
            } else {
                probeCounter++;
                currentIndex = (hash + (int) Math.pow(probeCounter, quadraticProbe)) % size;
            }
        }

        statistics += ", QUADRATIC PROBE " + probeCounter;

        System.out.println(statistics);
    }

    public static void main(String[] args) {

        HashTable hashTable = new HashTable();
        String hundredWords = "hundredWords", tenWords = "tenWords";

        hashTable.generateRandomWords(100, hundredWords);
        hashTable.generateRandomWords(10, tenWords);

        hashTable.addWordsToHashTable(hundredWords);
        hashTable.addWordsToHashTable(tenWords);

        System.out.println("\n\n");
        System.out.println("============================================================================================================================");

        System.out.println("Starting interactive SPELL CHECKER");
        System.out.println("ENTER q to EXIT");
        hashTable.startUserSession();


    }


}
