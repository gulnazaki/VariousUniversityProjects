import java.util.ArrayList;
import java.io.*;

public class Taxibeat {
	public static void main(String[] args) {
		Nodes map = null;
		Client client = null;
		Taxis taxis = null;
		int maxset = 0;
		BufferedWriter stats = null, kml = null;
		ArrayList<Info> results = new ArrayList<Info>();
		String filepath = null;

		try {
			map = new Nodes(args[2]);
			client = new Client(args[0],map);
			taxis = new Taxis(args[1],map);
			maxset = Integer.parseInt(args[3]);
			filepath = args[4];
		}
		catch (ArrayIndexOutOfBoundsException a) {
        	System.out.println("Usage: Taxibeat <client> <taxis> <nodes> <max search set> <ours | given>");
        	System.exit(-1);
        }

        try {
			String file = filepath + "/" + maxset + ".stats";
			stats = new BufferedWriter(new FileWriter(file));
			file = filepath + "/" + maxset + ".kml";
			kml = new BufferedWriter(new FileWriter(file));
					
        	ArrayList<Taxi> taxiList = taxis.getTaxiList();
        	Kml.printFirst(kml);
        	for (Taxi taxi : taxiList) {
        		Astar.solve(maxset,client,taxi,map,stats, results);
        	}
        	Kml.printMain(kml, results);
        	Kml.printLast(kml);
		}
		catch (IOException e) {
        	System.out.println("Problem with writing in file");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (stats != null) stats.close();
            	if (kml != null) kml.close();
            } catch (IOException e) {}
        }
	}
}