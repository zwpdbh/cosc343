import sun.net.www.content.text.Generic;

import java.awt.*;
import java.util.ArrayList;
import java.util.Random;

/**
 * Created by zw on 4/30/16.
 */
public class Animal extends Thing {

    public Animal() {
        super();
    }

    public Animal(int col, int row) {
        super(col, row);
    }

    public void display(Graphics g) {
        g.setColor(this.color);
        g.fillOval(col * SimulationApp.sizeOfCell, row * SimulationApp.sizeOfCell, SimulationApp.sizeOfCell, SimulationApp.sizeOfCell);
    }


    protected boolean isValidMove(int col, int row) {
        if (col >= 0 && col < SimulationGrid.numOfColumn && row >= 0 && row < SimulationGrid.numOfRows) {
            return true;
        } else {
            return false;
        }
    }
}
