import java.io.*;
import java.util.Map;
import java.util.HashMap;

import com.ugos.jiprolog.engine.JIPEngine;
import com.ugos.jiprolog.engine.JIPQuery;
import com.ugos.jiprolog.engine.JIPSyntaxErrorException;
import com.ugos.jiprolog.engine.JIPTerm;
import com.ugos.jiprolog.engine.JIPTermParser;

public class Nodes {
	private Map<Long, Node> map;
	public Nodes(String file, JIPEngine jip, String first_time) throws JIPSyntaxErrorException {
		map = new HashMap<Long, Node>();
		BufferedReader in = null;
		BufferedWriter out = null;
        try {
            in = new BufferedReader(new FileReader(file));
			JIPTermParser parser = jip.getTermParser();
			JIPQuery jipQuery, jipQuery2, jipQuery3; 
			if (first_time.equals("yes")) {
				out = new BufferedWriter(new FileWriter("../nodes.pl"));
            }
            String line;
            Long prev_line_id = -1L, prev_id = -1L;
            in.readLine();

            while ((line = in.readLine()) != null) {
            	String[] chunks = line.split(",");
				Double x = Double.parseDouble(chunks[0]);
				Double y = Double.parseDouble(chunks[1]);
				Long line_id = Long.parseLong(chunks[2]);
				Long id = Long.parseLong(chunks[3]);
				if (map.get(id) == null) {
					Node node = new Node(x,y,id);
					map.put(id, node);
				}

				if (first_time.equals("yes")) {
					if (line_id.equals(prev_line_id)) {
						jipQuery = jip.openSynchronousQuery(parser.parseTerm("twoWay(" + line_id + ")."));
						jipQuery2 = jip.openSynchronousQuery(parser.parseTerm("oneWay(" + line_id + ")."));
						jipQuery3 = jip.openSynchronousQuery(parser.parseTerm("reverse(" + line_id + ")."));
    	    			if (jipQuery.nextSolution() != null) {
							line = "canGo(" + prev_id + "," + id + "," + line_id + ").\n";
							out.write(line);
							line = "canGo(" + id + "," + prev_id + "," + line_id + ").\n";
							out.write(line);
						}
						else if (jipQuery2.nextSolution() != null) {
							line = "canGo(" + prev_id + "," + id + "," + line_id + ").\n";
							out.write(line);
						}
						else if (jipQuery3.nextSolution() != null) {
							line = "canGo(" + id + "," + prev_id + "," + line_id + ").\n";
							out.write(line);
						}
					}
				}

            	prev_id = id;
            	prev_line_id = line_id;
            }
        }
        catch (IOException e) {
        	System.out.println("Wrong Nodes Input File");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (in != null) in.close();
            	if (out != null) out.close();
            } catch (IOException e) {}
        }
	}

	public Node fixToClosest(Double x, Double y, Double[] min_dist, JIPEngine jip) throws JIPSyntaxErrorException {
		Double distance;
		min_dist[0] = 100000000.0;
		Node closest_node = null;
		
		JIPTermParser parser = jip.getTermParser();
		JIPQuery jipQuery; 

		for (Node node : map.values() ) {
    		distance = Distance.calculate(x,y,node.getX(),node.getY());
    		if (distance < min_dist[0]) {
	    		jipQuery = jip.openSynchronousQuery(parser.parseTerm("valid(" + node.getId() + ")."));
    	    	if (jipQuery.nextSolution() == null) continue;
    			min_dist[0] = distance;
    			closest_node = node;
    		}
    	}
    	return closest_node;	
	}

	public Map<Long, Node> getMap() {
		return map;
	}
}

class Node {
	private Double x,y;
	Long id;
	private Node cameFrom;
	private Double heuristic, gScore, dist;

	public Node(Double x, Double y, Long id) {
		this.x = x;
		this.y = y;
		this.id = id;
	}

	public Double getX() {
		return x;
	}

	public Double getY() {
		return y;
	}

	public Long getId() {
		return id;
	}

	public void setCameFrom(Node cameFrom) {
		this.cameFrom = cameFrom;
	}

	public Node getCameFrom() {
		return cameFrom;
	}

	public void setHeuristic(Double heuristic) {
		this.heuristic = heuristic;
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

	public void setDist(Double dist) {
		this.dist = dist;
	}

	public Double getDist() {
		return dist;
	}

	public Double distance(Node a) {
		Double distance = Distance.calculate(x,y,a.getX(),a.getY());
		return distance;
	}
}