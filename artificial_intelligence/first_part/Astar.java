import java.io.*;
import java.util.Map;
import java.util.HashMap;
import java.util.HashSet;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.PriorityQueue;

public class Astar {
	public static void solve(int maxset, Client client, Taxi taxi, Nodes map, BufferedWriter stats, ArrayList<Info> results) throws IOException {
		Comparator<Node> comparator = new NodeComparator();
		PriorityQueue<Node> openSet = new PriorityQueue<Node>(maxset,comparator);
		HashSet<Node> closedSet = new HashSet<Node>();
		int iterations = 0, truemaxset = 0;

		openSet.add(taxi.getNode());
		taxi.getNode().setCameFrom(null);
		taxi.getNode().setGScore(0.0);
		taxi.getNode().setHeuristic(client);

		while(!openSet.isEmpty()){
			iterations++;
			Node current = openSet.poll();
			if(current.getPoint().equals(client.getNode().getPoint())) {
				findSolution(client,taxi,maxset,truemaxset,iterations, stats, results);
				return;
			}

			ArrayList<Node> neighbors = current.getNeighbors();
			
			for(Node neighbor : neighbors){
				if(closedSet.contains(neighbor)){
					continue;
				}

				Double tentativeGScore = current.getGScore() + current.getPoint().distance(neighbor.getPoint());
				if(openSet.contains(neighbor)){
					if(tentativeGScore >= neighbor.getGScore()){
						continue;
					} else {
						openSet.remove(neighbor);
					}
				}

				int setsize = openSet.size();
				if (setsize > truemaxset) truemaxset = setsize;
				if (setsize == maxset) removeWorst(openSet);

				neighbor.setCameFrom(current);
				neighbor.setGScore(tentativeGScore);
				neighbor.setHeuristic(client);
				openSet.add(neighbor);
			}

			closedSet.add(current);
		}

		stats.write("Taxi " + taxi.getId() + " failed to find a Solution\n\n");
	}

	private static void removeWorst(PriorityQueue<Node> openSet) {
		Double cost, worstCost = -0.1;
		Node worstNode = null;
		for (Node node : openSet) {
			cost = node.getGScore() + node.getHeuristic();
			if (cost > worstCost) {
				worstCost = cost;
				worstNode = node;
			}
		}
		openSet.remove(worstNode);
	}

	private static void findSolution(Client client, Taxi taxi, int maxset, int truemaxset, int iterations, BufferedWriter stats, ArrayList<Info> results) {
		Double fulldistance = client.getDistanceToFix() + taxi.getDistanceToFix() + client.getNode().getGScore();
		ArrayList<Node> path = reconstruct_path(taxi, client);
		String color = "green";

		for (Info result : results) {
			if (result.taxi_color.equals("green") && fulldistance < result.distance) {
				color = "green";
				result.taxi_color = "black";
			}
			else if (fulldistance > result.distance) {
				color = "black";
			}
		}

		Info result = new Info(taxi.getId(),color,fulldistance,taxi.getNode().getPoint().getX(),taxi.getNode().getPoint().getY(),client.getNode().getPoint().getX(),client.getNode().getPoint().getY(),path);
		results.add(result);

		try {
			String line;
			line = "Client:\t\t" + client.getNode().getPoint().getX() + "," + client.getNode().getPoint().getY() + "\n";
			stats.write(line);
			line = "Taxi:\t\t" + taxi.getNode().getPoint().getX() + "," + taxi.getNode().getPoint().getY() + "," + taxi.getId() + "\n";
			stats.write(line);
			line = "Max Set:\t" + maxset + "\n";
			stats.write(line);
			line = "True Max Set:\t" + truemaxset + "\n";
			stats.write(line);
			line = "Iterations:\t" + iterations + "\n";
			stats.write(line);
			line = "Full Distance:\t" + fulldistance + "\n";
			stats.write(line);
			stats.write("\n\n");
		}
		catch (IOException e) {
        	System.out.println("Problem with writing in file");
        	System.exit(-1);
        }
	}
	
	private static ArrayList<Node> reconstruct_path(Taxi taxi, Client client) {
		Node current = client.getNode();
		ArrayList<Node> total_path = new ArrayList<Node>();
		total_path.add(current);
		while(current != taxi.getNode()){
			Node new_current = current.getCameFrom();
			total_path.add(0,new_current);
			current = new_current;
		}
		return total_path;
	}
}

class NodeComparator implements Comparator<Node>
{
    @Override
    public int compare(Node a, Node b)
    {
    	double value = (a.getHeuristic() + a.getGScore()) - (b.getHeuristic() + b.getGScore());
    	return Double.compare(value,0.0);
    }
}