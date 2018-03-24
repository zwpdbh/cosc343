import java.awt.*;

/**
 * Created by zw on 4/30/16.
 */
public class Strawberry extends Thing{

    private int foodValue;

    public Strawberry() {
        super();
        this.foodValue = 100;
        color = Color.red;
    }

    public Strawberry(int col, int row) {
        super(col, row);
        this.foodValue = 100;
        color = Color.red;
    }


    public void display(Graphics g) {
        g.setColor(Color.WHITE);
        g.drawString(""+this.foodValue, col*SimulationApp.sizeOfCell, row*SimulationApp.sizeOfCell);
        g.setColor(this.color);
        g.fillRect(col*SimulationApp.sizeOfCell, row*SimulationApp.sizeOfCell, SimulationApp.sizeOfCell, SimulationApp.sizeOfCell);
//        g.drawOval(col*SimulationApp.sizeOfCell, row*SimulationApp.sizeOfCell, SimulationApp.sizeOfCell, SimulationApp.sizeOfCell);
    }

    public void reduceFoodValue() {
        this.foodValue--;
    }

    public int getFoodValue() {
        return foodValue;
    }
}
