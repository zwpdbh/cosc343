import java.awt.*;
import java.time.Year;

/**
 * Created by zw on 4/30/16.
 */
public class Mushroom extends Thing {
    private int foodValue;

    public Mushroom() {
        super();
        this.foodValue = 50;
        color = Color.blue;
    }

    public Mushroom(int col, int row) {
        super(col, row);
        this.foodValue = 50;
        color = Color.blue;
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
