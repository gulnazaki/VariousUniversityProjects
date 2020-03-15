import java.io.*;

public class Client {
	private Node node;
	private Double distance_to_fix;

	public Client(String file, Nodes map) {
		BufferedReader in = null;
		try {
			in = new BufferedReader(new FileReader(file));
			in.readLine();
			String line = in.readLine();
			String[] chunks = line.split(",");
			Double x = Double.parseDouble(chunks[0]);
			Double y = Double.parseDouble(chunks[1]);
			Point temp = new Point(x,y);
			Double[] distance = new Double[]{ 0.0 };
			node = map.fixToClosest(temp,distance);
			distance_to_fix = distance[0];
		}
		catch (IOException e) {
        	System.out.println("Wrong Client Input File");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (in != null) in.close();
            } catch (IOException e) {}
        }
	}

	public Node getNode() {
		return node;
	}

	public Double getDistanceToFix() {
		return distance_to_fix;
	}
}