import java.util.ArrayList;

public class Info {
        public int taxi_id;
        public String taxi_color;
        public Double taxi_x, taxi_y, client_x, client_y, distance;
        public ArrayList<Node> path;

        public Info(int taxi_id, String taxi_color, Double distance, Double taxi_x, Double taxi_y, Double client_x, Double client_y, ArrayList<Node> path) {
                this.taxi_id = taxi_id;
                this.taxi_color = taxi_color;
                this.distance = distance;
                this.taxi_x = taxi_x;
                this.taxi_y = taxi_y;
                this.client_x = client_x;
                this.client_y = client_y;
                this.path = path;
        }
}