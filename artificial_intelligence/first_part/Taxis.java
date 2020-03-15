import java.io.*;
import java.util.ArrayList;

public class Taxis {
	private ArrayList<Taxi> taxiList;
	
	public Taxis(String file, Nodes map) {
		BufferedReader in = null;
		taxiList = new ArrayList<Taxi>();
		try {
			in = new BufferedReader(new FileReader(file));
			in.readLine();
			String line;
			while ((line = in.readLine()) != null) {
				String[] chunks = line.split(",");
				Double x = Double.parseDouble(chunks[0]);
				Double y = Double.parseDouble(chunks[1]);
				Integer id = Integer.parseInt(chunks[2]);
				Point temp = new Point(x,y);
				Node node = null;
				Double[] distance = new Double[]{ 0.0 };
				node = map.fixToClosest(temp,distance);
				Taxi taxi = new Taxi(node,distance[0],id);
				taxiList.add(taxi);
			}
		}
		catch (IOException e) {
        	System.out.println("Wrong Taxis Input File");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (in != null) in.close();
            } catch (IOException e) {}
        }
	}

	public ArrayList<Taxi> getTaxiList() {
		return taxiList;
	}
}

class Taxi {
	private Node node;
	private Double distance_to_fix;
	private Integer id;

	public Taxi(Node node, Double distance_to_fix, Integer id) {
		this.node = node;
		this.distance_to_fix = distance_to_fix;
		this.id = id;	
	}

	public Node getNode() {
		return node;
	}

	public Double getDistanceToFix() {
		return distance_to_fix;
	}

	public int getId() {
		return id;
	}
}