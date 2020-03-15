import java.util.ArrayList;

public class Info {
        public int id;
        public String color;
        public Double start_x, start_y, end_x, end_y, distance;
        public ArrayList<Node> path;

        public Info(int id, String color, Double distance, Double start_x, Double start_y, Double end_x, Double end_y, ArrayList<Node> path) {
                this.id = id;
                this.color = color;
                this.distance = distance;
                this.start_x = start_x;
                this.start_y = start_y;
                this.end_x = end_x;
                this.end_y = end_y;
                this.path = path;
        }
}