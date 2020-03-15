public class Point {
	private Double x,y;

	public Point(Double x, Double y) {
		this.x = x;
		this.y = y;
	}

	public Double getX() {
		return x;
	}

	public Double getY() {
		return y;
	}

	public Double distance(Point a) {
		Double distance = Distance.calculate(x,y,a.getX(),a.getY());
		return distance;
	}

	public Double heuristic(Client client) {
		Double distance = Distance.calculate(x,y,client.getNode().getPoint().getX(),client.getNode().getPoint().getY());
		return distance;
	}

	@Override
    public boolean equals(Object o) {
        if (((Point) o).x.equals(x) && ((Point) o).y.equals(y)) {
        	return true;
        }
        return false;
    }

    @Override 
    public int hashCode() {
    	return ((Double.valueOf(0.5*(x.hashCode() + y.hashCode())*(x.hashCode() + y.hashCode() + 1))).hashCode() + y.hashCode());
	}
}