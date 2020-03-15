import java.lang.Math;

public class Distance {
	public static Double calculate(Double long1, Double lat1, Double long2, Double lat2) {
		Double R = 6371000.0;
    	Double dLat = Math.toRadians(lat2-lat1);
    	Double dLong = Math.toRadians(long2-long1);
    	Double a = Math.sin(dLat/2) * Math.sin(dLat/2) +
               Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
               Math.sin(dLong/2) * Math.sin(dLong/2);
    	Double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    	Double distance = (R * c);
   		return distance;
	}
}