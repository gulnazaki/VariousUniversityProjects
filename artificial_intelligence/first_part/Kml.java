import java.io.*;
import java.util.ArrayList;

public class Kml {
	public static void printFirst (BufferedWriter kml) throws IOException {
		String line;
                line = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"; //1st line
                kml.write(line);
                line = "\t<kml xmlns=\"http://earth.google.com/kml/2.1\">\n";//2nd line
                kml.write(line);
                line = "\t<Document>\n";
                kml.write(line);
                line = "\t\t<name>Taxi Routes</name>\n";
                kml.write(line);
                line = "\t\t<Style id=\"green\">\n";
                kml.write(line);
                line = "\t\t\t<LineStyle>\n";
                kml.write(line);
                line = "\t\t\t\t<color>ff009900</color>\n";
                kml.write(line);
                line = "\t\t\t\t<width>4</width>\n";
                kml.write(line);
                line = "\t\t\t</LineStyle>\n";
                kml.write(line);
                line = "\t\t</Style>\n";
                kml.write(line);
                line = "\t\t<Style id=\"red\">\n";
                kml.write(line);
                line = "\t\t\t<LineStyle>\n";
                kml.write(line);
                line = "\t\t\t\t<color>ff0000ff</color>\n";
                kml.write(line);
                line = "\t\t\t\t<width>4</width>\n";
                kml.write(line);
                line = "\t\t\t</LineStyle>\n";
                kml.write(line);
                line = "\t\t</Style>\n";
                kml.write(line);
	}

	public static void printMain(BufferedWriter kml, ArrayList<Info> results) throws IOException {
            for (Info result : results) {      
                String line;
                line = "\t\t<Placemark>\n";
                kml.write(line);
                line = "\t\t\t<name>Taxi "+result.taxi_id+"</name>\n";
                kml.write(line);
                line = "\t\t\t<styleUrl>#"+result.taxi_color+"</styleUrl>\n";
                kml.write(line);
                line = "\t\t\t<LineString>\n";
                kml.write(line);
                line = "\t\t\t\t<altitudeMode>relative</altitudeMode>\n";
                kml.write(line);
                line = "\t\t\t\t<coordinates>\n";
                kml.write(line);
                line = result.taxi_x+","+result.taxi_y+",0\n";
                kml.write("\t\t\t\t\t"+line);

                        for (Node node : result.path) {
                                line = node.getPoint().getX() + "," + node.getPoint().getY() + ",0\n";
                                kml.write("\t\t\t\t\t"+line);
                        }

                line = result.client_x+","+result.client_y+",0\n";
                kml.write("\t\t\t\t\t"+line);
                line = "\t\t\t\t</coordinates>\n";
                kml.write(line);
                line = "\t\t\t</LineString>\n";
                kml.write(line);
                line = "\t\t</Placemark>\n";
                kml.write(line);
            }    
        }

        public static void printLast (BufferedWriter kml) throws IOException {
                kml.write("\t</Document>\n");
                kml.write("</kml>\n");
                kml.close();
	}
}