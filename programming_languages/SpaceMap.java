/* SpaceMap */
/* Melistas Thomas */
/* Patris Nikolas */

import java.io.*;
import java.util.ArrayList;
import java.util.Comparator;

// A cost comparator needed for the priority queue
class CompareCosts implements Comparator<Square> {
    @Override
    public int compare (Square x, Square y) {
        if (x.getCost() < y.getCost()) return -1;
        if (x.getCost() > y.getCost()) return 1;
        return 0;
    }	
}

// This is the position's class, we store cost and path so we can print it faster
class Square {
	private int x, y, cost;
	private String path;

	public Square(int x, int y, int cost, String path) {
		this.x = x;
		this.y = y;
		this.cost = cost;
		this.path = path;
	}

	public int getX() {
        return x;
    }
    public int getY() {
        return y;
    }
    public int getCost() {
        return cost;
    }

    public String getPath() {
        return path;
    }

    public char getSymbol(SpaceMap map) {
    	return map.getSymbol(x,y);
    }

    public int getCost(SpaceMap map) {
    	return map.getCost(x,y);
    }

    public void setCost(SpaceMap map, int cost) {
    	map.setCost(x,y,cost);
    }

    public boolean validNeighbour(SpaceMap map, char side) {
    	if (side == 'R') {
    		if (!map.inLimits(x,y+1) || map.getSymbol(x,y+1)=='X') return false;
    		if ((map.getCost(x,y+1) <= cost+1) && (map.getCost(x,y+1)!=0)) return false;
    	}
    	else if (side == 'L') {
    		if (!map.inLimits(x,y-1) || map.getSymbol(x,y-1)=='X') return false;
    		if ((map.getCost(x,y-1) <= cost+2) && (map.getCost(x,y-1)!=0)) return false;
    	}
       	else if (side == 'D') {
    		if (!map.inLimits(x+1,y) || map.getSymbol(x+1,y)=='X') return false;
    		if ((map.getCost(x+1,y) <= cost+1) && (map.getCost(x+1,y)!=0)) return false;
    	}
    	else if (side == 'U') {
    		if (!map.inLimits(x-1,y) || map.getSymbol(x-1,y)=='X') return false;
    		if ((map.getCost(x-1,y) <= cost+3) && (map.getCost(x-1,y)!=0)) return false;
    	}
    	return true;
    }
}

// Spacemap's class, we store the initial symbol map and a cost map so we can tell faster if path is ideal
public class SpaceMap {
	private char[][] map;
	private int[][] costmap;
	private int rows, columns, startX, startY;

	// Constructor, reads input file and creates maps and finds initial square
	public SpaceMap(String[] args) {
		BufferedReader in = null;
        try {
            in = new BufferedReader(new FileReader(args[0]));
            String line;
            ArrayList<String> lines = new ArrayList<String>();
            while ((line = in.readLine()) != null) {
                lines.add(line);
            }

            rows = lines.size();
            columns = lines.get(0).length();
            map = new char[rows][columns];
            costmap = new int[rows][columns];

			for (int i=0; i<rows; i++) {
                for (int j=0; j<columns; j++) {
                    map[i][j]=lines.get(i).charAt(j);
                    costmap[i][j]=0;
                    if (map[i][j]=='S') {
                        startX=i;
                        startY=j;
                    }
                }
            }
        }

        catch (IOException e) {
        	System.out.println("Wrong Input File");
        	System.exit(-1);
        }

        catch (ArrayIndexOutOfBoundsException a) {
        	System.out.println("Provide Input File");
        	System.exit(-1);
        }

        finally {
        	try {
            	if (in != null) in.close();
            } catch (IOException f) {}
        }
	}

	protected int getCost(int x, int y) {
		return costmap[x][y];
	}

	protected void setCost(int x, int y, int cost) {
		costmap[x][y] = cost;
	}

	protected char getSymbol(int x, int y) {
		return map[x][y];
	}

	public int getStartX() {
		return startX;
	}

	public int getStartY() {
		return startY;
	}

    protected boolean inLimits(int x, int y) {
    	if (x >= 0 && x < rows && y >= 0 && y < columns) return true;
    	else return false;
    }
}