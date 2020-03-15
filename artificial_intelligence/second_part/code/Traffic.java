import java.io.*;

public class Traffic {
	public Traffic(String file, String first_time){
		if (first_time.equals("no")) return;
		BufferedReader in = null;
		BufferedWriter out = null;
		try {
			in = new BufferedReader(new FileReader(file));
			out = new BufferedWriter(new FileWriter("../traffic.pl"));
			String line;
			in.readLine();
			while ((line = in.readLine()) != null) {
            	String[] chunks = line.split(",",-1);
				int id = Integer.parseInt(chunks[0]);
				if (chunks.length == 3 && !(chunks[2].equals(""))) {
					String[] info = chunks[2].split("\\|");
					for (int i = 0; i < info.length; i++) {
						String[] hours = info[i].split("\\=");
						int time = Integer.parseInt(hours[0].split("-")[0].split(":")[0]);
						line = "traffic(" + id + "," + time + "," + hours[1] + ").\n";
						out.write(line);
						line = "traffic(" + id + "," + (time+1) + "," + hours[1] + ").\n";
						out.write(line);
					}
				}
			}
		}
		catch (IOException e) {
        	System.out.println("Wrong Traffic Input File");
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