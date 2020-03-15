import java.io.*;
import java.util.PriorityQueue;
import java.util.Comparator;

public class TaxiRank {
	private int k;
	private Comparator<TaxiStats> comparator1, comparator2;
	private PriorityQueue<TaxiStats> rank1, rank2;
	
	public TaxiRank(int k) {
		this.k = k;
		comparator1 = new Taxi1Comparator();
		comparator2 = new Taxi2Comparator();
		rank1 = new PriorityQueue<TaxiStats>(k,comparator1);
		rank2 = new PriorityQueue<TaxiStats>(k,comparator2);
	}

	public void addTo (TaxiStats stat) {
		rank1.add(stat);
		rank2.add(stat);
	}

	public void printFirst (BufferedWriter rankfile) throws IOException {
		String line;
		TaxiStats stat;
		for (int i = 0; i < k; i++) {
			stat = rank1.poll();
			if (stat == null) break;
			line = stat.id + " -> " + String.format("%.2f",stat.distance/1000.0) + "km\n";
			rankfile.write(line);
		}
		line = "\n\n";
		rankfile.write(line);
	}

	public void printSecond (BufferedWriter rankfile) throws IOException {
		String line;
		TaxiStats stat;
		for (int i = 0; i < k; i++) {
			stat = rank2.poll();
			if (stat == null) break;
			line = stat.id + " -> " + stat.rating + "\n";
			rankfile.write(line);
		}
		line = "\n\n";
		rankfile.write(line);
	}
}

class Taxi1Comparator implements Comparator<TaxiStats>
{
    @Override
    public int compare(TaxiStats a, TaxiStats b)
    {
    	double value = a.distance - b.distance;
    	return Double.compare(value,0.0);
    }
}

class Taxi2Comparator implements Comparator<TaxiStats>
{
    @Override
    public int compare(TaxiStats a, TaxiStats b)
    {
    	double value = b.rating - a.rating;
    	return Double.compare(value,0.0);
    }
}
