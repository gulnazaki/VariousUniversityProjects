import java.io.*;

public class Lines {
	public Lines(String file, String first_time){
		if (first_time.equals("no")) return;
		BufferedReader in = null;
		BufferedWriter out = null;
		try {
			in = new BufferedReader(new FileReader(file));
			out = new BufferedWriter(new FileWriter("../lines.pl"));
			String line;
			in.readLine();
			while ((line = in.readLine()) != null) {
            	String[] chunks = line.split(",",-1);
				int id = Integer.parseInt(chunks[0]);
				String highway = chunks[1];

				if (highway.equals("motorway") || highway.equals("trunk") || highway.equals("primary") || highway.equals("secondary") || highway.equals("tertiary") || highway.equals("unclassified") || highway.equals("motorway_link") || highway.equals("trunk_link") || highway.equals("primary_link") || highway.equals("secondary_link") || highway.equals("tertiary_link") || highway.equals("track") || highway.equals("residential")) {
					if (chunks[3].equals("yes")) {
						line = "oneWay(" + id + ").\n";
						out.write(line);			
					}
					else if (chunks[3].equals("no")){
						line = "twoWay(" + id + ").\n";
						out.write(line);
					}
					else if (chunks[3].equals("-1")){
						line = "reverse(" + id + ").\n";
						out.write(line);
					}
					else {
						line = "twoWay(" + id + ").\n";
						out.write(line);
					}
				}
				if (chunks[4].equals("yes") || chunks[4].equals("24/7")) {
					line = "lit(" + id + ").\n";
					out.write(line);
				}
				/*int lanes = Integer.parseInt(chunks[5]);*/
				String maxspeed = chunks[6];
				if (maxspeed.equals("")) {
					if (highway.equals("motorway") || highway.equals("trunk") || highway.equals("motorway_link") || highway.equals("trunk_link")) {
						line = "maxspeed(" + id +  ",120).\n";
						out.write(line);
					}
					else if (highway.equals("primary") || highway.equals("secondary") || highway.equals("primary_link") || highway.equals("secondary_link")) {
						line = "maxspeed(" + id +  ",90).\n";
						out.write(line);
					}
					else if (highway.equals("tertiary") || highway.equals("unclassified") || highway.equals("tertiary_link")) {
						line = "maxspeed(" + id +  ",40).\n";
						out.write(line);
					}
					else if (highway.equals("residential") || highway.equals("track")) {
						line = "maxspeed(" + id +  ",20).\n";
						out.write(line);
					}
				}
				else{
					line = "maxspeed(" + id +  "," + maxspeed + ").\n";
					out.write(line);
				}
				/*String railway = chunks[7];
				String boundary = chunks[8];
				String access = chunks[9];
				String natural = chunks[10];
				String barrier = chunks[11];
				String tunnel = chunks[12];
				String bridge = chunks[13];
				String incline = chunks[14];
				String waterway = chunks[15];
				String busway = chunks[16];*/
				if (chunks[17].equals("yes")) {
					line = "toll(" + id + ").\n";
					out.write(line);
				}
			}
		}
		catch (IOException e) {
        	System.out.println("Wrong Lines Input File");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (in != null) in.close();
            	if (out != null) out.close();
            } catch (IOException e) {}
        }
	}
}