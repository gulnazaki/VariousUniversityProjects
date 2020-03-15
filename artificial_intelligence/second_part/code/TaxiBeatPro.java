import java.util.ArrayList;
import java.io.*;

import com.ugos.jiprolog.engine.JIPEngine;
import com.ugos.jiprolog.engine.JIPQuery;
import com.ugos.jiprolog.engine.JIPSyntaxErrorException;
import com.ugos.jiprolog.engine.JIPTerm;
import com.ugos.jiprolog.engine.JIPTermParser;

public class TaxiBeatPro {
	public static void main(String[] args) throws JIPSyntaxErrorException, IOException {
		Nodes map = null;
		Client client = null;
		Taxis taxis = null;
		int maxset = 0;
		int k = 0;
		BufferedWriter stats = null, kml = null, rankfile = null;
		ArrayList<Info> results = new ArrayList<Info>();
		String filepath = null, first_time = null;

		JIPEngine jip = new JIPEngine();
		JIPTermParser parser = jip.getTermParser();
		JIPQuery jipQuery; 

		try {
			maxset = Integer.parseInt(args[5]);
			k = Integer.parseInt(args[6]);
			filepath = "../" + args[7];
			first_time = args[8];

			jip.consultFile("../rules.pl");

			new Lines(args[3],first_time);
			jip.consultFile("../lines.pl");
			new Traffic(args[4],first_time);
			jip.consultFile("../traffic.pl");
			map = new Nodes(args[2],jip,first_time);
			jip.consultFile("../nodes.pl");
			client = new Client(args[0],map,jip,first_time);
			jip.consultFile("../client.pl");
			taxis = new Taxis(args[1],map,jip,first_time);
			jip.consultFile("../taxis.pl");
		}
		catch (ArrayIndexOutOfBoundsException a) {
        	System.out.println("Usage: Taxibeat <client> <taxis> <nodes> <lines> <traffic> <max search set> <k> <ours | given> <first time>");
        	System.exit(-1);
        }

        try {
			String file = filepath + "/" + maxset + ".stats";
			stats = new BufferedWriter(new FileWriter(file));
			file = filepath + "/" + maxset + ".kml";
			kml = new BufferedWriter(new FileWriter(file));
			file = filepath + "/" + maxset + ".rank";
			rankfile = new BufferedWriter(new FileWriter(file));

			TaxiRank rank = new TaxiRank(k);
					
        	ArrayList<Taxi> taxiList = taxis.getTaxiList();
        	Kml.printFirst(kml);

        	for (Taxi taxi : taxiList) {
        		jipQuery = jip.openSynchronousQuery(parser.parseTerm("suitableTaxi(" + taxi.getId() + ")."));
        		if (jipQuery.nextSolution() != null) {
        			Astar.solve(maxset,taxi.getNode(),client.getCurrent(),map.getMap(),stats,results,taxi.getId(),taxi.getDTF(),client.getDTFC(),jip,rank);
        		}
        	}
        	Astar.solve(maxset,client.getCurrent(),client.getDestination(),map.getMap(),stats,results,0,client.getDTFC(),client.getDTFD(),jip,rank);
        	Kml.printMain(kml, results);
        	Kml.printLast(kml);
        	rank.printFirst(rankfile);
        	rank.printSecond(rankfile);
		}
		catch (IOException e) {
        	System.out.println("Problem with writing in file");
        	System.exit(-1);
        }
        finally {
        	try {
            	if (stats != null) stats.close();
            	if (kml != null) kml.close();
            	if (rankfile != null) rankfile.close();
            } catch (IOException e) {}
        }
	}
}