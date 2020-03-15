/* Moredeli */
/* Melistas Thomas */
/* Patris Nikolas */

import java.util.Comparator;
import java.util.PriorityQueue;

public class Moredeli {
    // Main function
    public static void main(String[] args) {
        // Create our spacemap from input file and initialise delivery-alien-boy position
        SpaceMap map = new SpaceMap(args);
		Square start = new Square(map.getStartX(),map.getStartY(),0,"");
        
        // Create comparator for our priority queue based on cost
        Comparator<Square> comparator = new CompareCosts();
        PriorityQueue<Square> Q = new PriorityQueue<Square>(1,comparator);
        // Insert initial state in queue and mark start position's cost in map so we can't visit it again with a bigger cost
        Q.offer(start);
        start.setCost(map,0);

        while (!Q.isEmpty()) {
        	// Select position with smallest cost
        	Square curr = Q.poll();
        	// If we are at end print cost and path
        	if (curr.getSymbol(map) == 'E') {
        		System.out.println(curr.getCost() + " " + curr.getPath());
        		break;
        	} else {
        		// If neighbor is valid (in limits,not an obstacle and not visited with a smaller cost) mark it visited with the cost needed and insert it in priority queue
        		if (curr.validNeighbour(map,'R')) {
        			Square next = new Square(curr.getX(),curr.getY()+1,curr.getCost()+1,curr.getPath()+"R");
        			next.setCost(map,curr.getCost()+1);
        			Q.offer(next);
        		}
        		if (curr.validNeighbour(map,'L')) {
        			Square next = new Square(curr.getX(),curr.getY()-1,curr.getCost()+2,curr.getPath()+"L");
        			next.setCost(map,curr.getCost()+2);
        			Q.offer(next);
        		}
        		if (curr.validNeighbour(map,'D')) {
        			Square next = new Square(curr.getX()+1,curr.getY(),curr.getCost()+1,curr.getPath()+"D");
        			next.setCost(map,curr.getCost()+1);
        			Q.offer(next);
        		}
        		if (curr.validNeighbour(map,'U')) {
        			Square next = new Square(curr.getX()-1,curr.getY(),curr.getCost()+3,curr.getPath()+"U");
        			next.setCost(map,curr.getCost()+3);
        			Q.offer(next);
        		}
        	}
        }
    }
}