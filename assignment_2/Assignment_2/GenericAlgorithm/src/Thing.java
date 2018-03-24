import java.awt.*;
import java.util.Random;

/**
 * Created by zw on 4/30/16.
 */
public abstract class Thing {
    private boolean eaten = false;
    protected int col;
    protected int row;
    protected Color color;

    public Thing() {
        Random random = new Random();
        col  = random.nextInt(SimulationGrid.numOfColumn - 1);
        row = random.nextInt(SimulationGrid.numOfRows - 1);
    }

    public Thing(int col, int row) {
        this.col = col;
        this.row = row;
    }

    public abstract void display(Graphics g);

    public int getCol() {
        return col;
    }

    public void setCol(int col) {
        this.col = col;
    }

    public int getRow() {
        return row;
    }

    public void setRow(int row) {
        this.row = row;
    }


}
