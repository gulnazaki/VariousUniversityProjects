import java.io.*;

public class Villages {
    private int [] parentOfNode,rankOfNode;
    private int setsCount,newCon;

    // Method for 
    private int convInt(String inStr) {
        try {
            int returnInt = Integer.parseInt(inStr.trim());

            return returnInt;
        } catch (NumberFormatException nfe) { 
            System.out.println("NumberFormatException: " + nfe.getMessage());
            System.exit(1);
        }
        return 0;
    }

    public int getSets() {
        return setsCount;
    }

    public int getCons () {
        return newCon;
    }

    public void createArr (String numberOfNodes,String numberOfCon) {
        setsCount = convInt(numberOfNodes);
        newCon = convInt(numberOfCon);

    	if (setsCount < 0) {
    		throw new IllegalArgumentException();
    	}

    	parentOfNode = new int [setsCount+1];
    	rankOfNode = new int [setsCount+1];

    	for (int i = 0; i < setsCount; i++ ) {
    		parentOfNode[i] = i;
    		rankOfNode[i] = 0;
    	}
    }

    public int findParent (int pNode) {
        while (pNode != parentOfNode[pNode]) {
            parentOfNode[pNode] = parentOfNode[parentOfNode[pNode]];
            pNode = parentOfNode[pNode];
        }
        return pNode;
    }

    public void unionNodes (String fIn, String sIn) {
        int fParent,sParent;

        // Get the parent of each node
        fParent = findParent(convInt(fIn));
        sParent = findParent(convInt(sIn));

        // If node's parents are the same don't do anything
        if (fParent == sParent) {
        	return;
        }

        // Else union them by the rank of each node
        if (rankOfNode[fParent] > rankOfNode[sParent]) {
        	parentOfNode[sParent] = fParent;
        } else if (rankOfNode[fParent] < rankOfNode[sParent]) {
        	parentOfNode[fParent] = sParent;
        } else {
         	parentOfNode[fParent] = sParent;
         	rankOfNode[sParent]++;
        }
        setsCount--;
    } 

    private static int getSolution (int setsCount,int newCon) {
        if (newCon >= setsCount) {
            return 1;
        } else {
            return (setsCount-newCon);
        }
    }

    public static void main(String[] args) {
        String inStr [];

        boolean lineBreaker = true;
        String lineStr = null;

        Villages unionFind = new Villages();

        try {
            FileReader fileReader;

            if (args.length == 0){
                throw new IllegalArgumentException();
            } else {
                fileReader = new FileReader(args[0]);
            }

            BufferedReader bufferedReader = 
                new BufferedReader(fileReader);

            while((lineStr = bufferedReader.readLine()) != null) {
                if (lineBreaker) {
                    inStr = lineStr.split("\\s+");

                    unionFind.createArr(inStr[0],inStr[2]);

                    lineBreaker = false;
                } else {
                    inStr = lineStr.split("\\s+");

                    unionFind.unionNodes(inStr[0],inStr[1]);
                }
            }   

            bufferedReader.close();         
        }
        catch(FileNotFoundException notfoundE) {
            System.out.println(
                "FileNotFoundException: " + 
                args[0]);
            System.exit(1);
        }
        catch(IOException ioE) {
            System.out.println("IOException: " + ioE.getMessage());
            System.exit(1);
        }
        catch(IllegalArgumentException illegalE) {
            System.out.println("IllegalArgumentException: " + illegalE.getMessage());
            System.exit(1);
        }

        System.out.println(getSolution(unionFind.getSets(),unionFind.getCons()));
    }
}   
