import java.io.*;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;

public class Nodes {
	private Map<Point, Node> map;
	public Nodes(String file) {
		map = new HashMap<Point, Node>();
		BufferedReader in = null;
        try {
            in = new BufferedReader(new FileReader(file));
            String line;
            int previd = -1;
            Node prevnode = null, node = null;
            Point point;
            in.readLine();

            while ((line = in.readLine()) != null) {
            	String[] chunks = line.split(",");
				Double x = Double.parseDouble(chunks[0]);
				Double y = Double.parseDouble(chunks[1]);
				point = new Point(x,y);
				int id = Integer.parseInt(chunks[2]);
				Node intersection = (Node)map.get(point);
				node = new Node(point);
				if (intersection != null) {
					for (Node neigh : node.getNeighbors()) intersection.addNeighbor(neigh);
					node = intersection;
				}
				if (id == previd) {
					node.addNeighbor(prevnode);
					prevnode.addNeighbor(node);
				}
           		map.put(point, node);

            	previd = id;
            	prevnode = node;
            }
        }
        catch (IOException e) {
        	System.out.println("Wrong Nodes Input File");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (in != null) in.close();
            } catch (IOException e) {}
        }
	}

	public Node fixToClosest(Point temp, Double[] min_dist) {
		Double distance;
		min_dist[0] = 100000000.0;
		Node closest_node = null;
		for (Point key : map.keySet() ) {
    		distance = temp.distance(key);
    		if (distance < min_dist[0]) {
    			min_dist[0] = distance;
    			closest_node = map.get(key);
    		}
    	}
    	return closest_node;	
	}
}

class Node {
	private Point point;
	private ArrayList<Node> neighbors;
	private Node cameFrom;
	private Double heuristic, gScore;

	public Node(Point point) {
		this.point = point;
		neighbors = new ArrayList<Node>();
	}

	public void addNeighbor(Node neighbor) {
		neighbors.add(neighbor);
	}

	public Point getPoint() {
		return point;
	}

	public ArrayList<Node> getNeighbors() {
		return neighbors;
	}

	public void setCameFrom(Node cameFrom) {
		this.cameFrom = cameFrom;
	}

	public Node getCameFrom() {
		return cameFrom;
	}

	public void setHeuristic(Client client) {
		heuristic = point.heuristic(client);
	}

	public Double getHeuristic() {
		return heuristic;
	}

	public void setGScore(Double gScore) {
		this.gScore = gScore;
	}

	public Double getGScore() {
		return gScore;
	}
}