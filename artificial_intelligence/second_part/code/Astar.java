import java.io.*;
import java.util.HashSet;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Map;
import java.util.HashMap;

import com.ugos.jiprolog.engine.JIPEngine;
import com.ugos.jiprolog.engine.JIPQuery;
import com.ugos.jiprolog.engine.JIPSyntaxErrorException;
import com.ugos.jiprolog.engine.JIPTerm;
import com.ugos.jiprolog.engine.JIPTermParser;

public class Astar {
	public static void solve(int maxset, Node start, Node end, Map<Long, Node> map, BufferedWriter stats, ArrayList<Info> results, int id, Double sd, Double ed, JIPEngine jip, TaxiRank rank) throws JIPSyntaxErrorException, IOException {
		JIPTermParser parser = jip.getTermParser();
		JIPQuery jipQuery; 
		JIPTerm term;
	
		Comparator<Node> comparator = new NodeComparator();
		PriorityQueue<Node> openSet = new PriorityQueue<Node>(maxset,comparator);
		HashSet<Node> closedSet = new HashSet<Node>();
		int iterations = 0, truemaxset = 0;
		Double b_s = 1 / 120.0;

		start.setCameFrom(null);
		start.setGScore(0.0);
		start.setDist(0.0);
		start.setHeuristic(start.distance(end)*b_s);
		openSet.add(start);

		while(!openSet.isEmpty()){
			iterations++;
			Node current = openSet.poll();
			if(current.getId().equals(end.getId())) {
				if (id != 0) {
					jipQuery = jip.openSynchronousQuery(parser.parseTerm("rating(X," + id + ")."));
					term = jipQuery.nextSolution();
					Double rating = Double.valueOf(term.getVariablesTable().get("X").toString());
					TaxiStats stat = new TaxiStats(end.getGScore(),end.getDist(),rating,id);
					rank.addTo(stat);
				}

				findSolution(start,end,maxset,truemaxset,iterations,stats,results,id,end.getDist(),sd,ed);
				return;
			}

			jipQuery = jip.openSynchronousQuery(parser.parseTerm("canMoveFromTo(" + current.getId() + ",Y,S)."));
			term = jipQuery.nextSolution();
			while (term != null) {
				String neighbor_id = String.format("%.0f",Double.valueOf(term.getVariablesTable().get("Y").toString()));
				Node neighbor = map.get(Long.parseLong(neighbor_id));
				if(closedSet.contains(neighbor)){
					term = jipQuery.nextSolution();
					continue;
				}

				Double tentativeGScore = current.getGScore() + current.distance(neighbor) / Double.valueOf(term.getVariablesTable().get("S").toString());
				Double dist = current.getDist() + current.distance(neighbor);
				if(openSet.contains(neighbor)){
					if(tentativeGScore >= neighbor.getGScore()){
						term = jipQuery.nextSolution();
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
				neighbor.setDist(dist);
				neighbor.setHeuristic(neighbor.distance(end)*b_s);
				openSet.add(neighbor);
				term = jipQuery.nextSolution();
			}

			closedSet.add(current);
		}

		if (id == 0) stats.write("Failed to find a Solution from Client's current location to Destination\n\n");

		else stats.write("Taxi " + id + " failed to find a Solution\n\n");
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

	private static void findSolution(Node start, Node end, int maxset, int truemaxset, int iterations, BufferedWriter stats, ArrayList<Info> results, int id, Double distance, Double sd, Double ed) {
		Double fulldistance = sd + ed + distance;
		ArrayList<Node> path = reconstruct_path(start,end);
		String color = "green";

		if (id == 0) color = "red";
		else {
			for (Info result : results) {
				if (result.color.equals("green") && fulldistance < result.distance) {
					color = "green";
					result.color = "black";
				}
				else if (fulldistance > result.distance) {
					color = "black";
				}
			}
		}

		Info result = new Info(id,color,fulldistance,start.getX(),start.getY(),end.getX(),end.getY(),path);
		results.add(result);

		try {
			String line;
			if (id != 0) {
				line = "Client:\t\t" + end.getX() + "," + end.getY() + "\n";
				stats.write(line);
				line = "Taxi:\t\t" + start.getX() + "," + start.getY() + "," + id + "\n";
				stats.write(line);
			}
			else {
				line = "Client:\t\t" + start.getX() + "," + start.getY() + "\n";
				stats.write(line);
				line = "Destination:\t\t" + end.getX() + "," + end.getY() + "\n";
				stats.write(line);
			}
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
	
	private static ArrayList<Node> reconstruct_path(Node start, Node end) {
		Node current = end;
		ArrayList<Node> total_path = new ArrayList<Node>();
		total_path.add(current);
		while(current != start){
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