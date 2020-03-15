import java.io.*;
import java.util.ArrayList;
import com.ugos.jiprolog.engine.JIPEngine;
import com.ugos.jiprolog.engine.JIPSyntaxErrorException;

public class Taxis {
	private ArrayList<Taxi> taxiList;
	
	public Taxis(String file, Nodes map, JIPEngine jip, String first_time) throws JIPSyntaxErrorException {
		BufferedReader in = null;
		BufferedWriter out = null;
		taxiList = new ArrayList<Taxi>();
		try {
			in = new BufferedReader(new FileReader(file));
			if (first_time.equals("yes")) {
				out = new BufferedWriter(new FileWriter("../taxis.pl"));
			}
			in.readLine();
			String line;
			while ((line = in.readLine()) != null) {
				String[] chunks = line.split(",");
				Double x = Double.parseDouble(chunks[0]);
				Double y = Double.parseDouble(chunks[1]);
				Integer id = Integer.parseInt(chunks[2]);
				
				if (first_time.equals("yes")) {
					if (chunks[3].equals("yes")) {
						line = "available(" + id + ").\n";
						out.write(line);
					}
					String max_capacity = chunks[4].split("-")[1];
					line = "capacity(" + max_capacity + "," + id +").\n";
					out.write(line);
					String[] languages = chunks[5].split("\\|");
					for (int i = 0; i < languages.length; i++) {
						line = "language(" + languages[i] + "," + id + ").\n";
						out.write(line);
					}
					line = "rating(" + Double.parseDouble(chunks[6]) + "," + id + ").\n";
					out.write(line);
					if (chunks[7].equals("yes")) {
						line = "longDistance(" + id + ").\n";
						out.write(line);
					}
					line = "type(" + chunks[8].split("	")[0] + "," + id +").\n";
					out.write(line);
				}

				Double[] distance = new Double[]{ 0.0 };
				Node node = map.fixToClosest(x,y,distance,jip);
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
            	if (out != null) out.close();
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

	public Double getDTF() {
		return distance_to_fix;
	}

	public int getId() {
		return id;
	}
}