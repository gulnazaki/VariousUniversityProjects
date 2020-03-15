import java.io.*;
import com.ugos.jiprolog.engine.JIPEngine;
import com.ugos.jiprolog.engine.JIPSyntaxErrorException;

public class Client {
	private Node current, destination;
	private Double distance_to_fix_c, distance_to_fix_d;

	public Client(String file, Nodes map, JIPEngine jip, String first_time) throws JIPSyntaxErrorException {
		BufferedReader in = null;
		BufferedWriter out = null;
		try {
			in = new BufferedReader(new FileReader(file));
			in.readLine();
			String line = in.readLine();
			String[] chunks = line.split(",");
			Double c_x = Double.parseDouble(chunks[0]);
			Double c_y = Double.parseDouble(chunks[1]);
			Double d_x = Double.parseDouble(chunks[2]);
			Double d_y = Double.parseDouble(chunks[3]);
			if (first_time.equals("yes")); {
				out = new BufferedWriter(new FileWriter("../client.pl"));
				line = "currtime(" + chunks[4].split(":")[0] + ").\n";
				out.write(line);
				line = "persons(" + chunks[5] + ").\n";
				out.write(line);
				line = "language(" + chunks[6] + ").\n";
				out.write(line);
				line = "luggage(" + chunks[7] + ").\n";
				out.write(line);
			}
			Double[] distance = new Double[]{ 0.0 };
			current = map.fixToClosest(c_x,c_y,distance,jip);
			distance_to_fix_c = distance[0];

			destination = map.fixToClosest(d_x,d_y,distance,jip);
			distance_to_fix_d = distance[0];
		}
		catch (IOException e) {
        	System.out.println("Wrong Client Input File");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (in != null) in.close();
            	if (out != null) out.close();
            } catch (IOException e) {}
        }
	}

	public Node getCurrent() {
		return current;
	}

	public Node getDestination() {
		return destination;
	}

	public Double getDTFC() {
		return distance_to_fix_c;
	}

	public Double getDTFD() {
		return distance_to_fix_d;
	}
}