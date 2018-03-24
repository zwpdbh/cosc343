import java.awt.*;
import java.util.ArrayList;
import java.util.Random;

/**
 * Created by zw on 5/5/16.
 */
public class Monster extends Animal {
    private Creature nearestCreature = null;

    public Monster() {
        super();
        color = Color.ORANGE;
    }

    public Monster(int col, int row) {
        super(col, row);
        color = Color.ORANGE;
    }

    @Override
    public void display(Graphics g) {
        super.display(g);
    }

    public void move() {
        // Before move, test if creature moved at my position, if so eat it.
        senseNearestCreature();

        Random random = new Random();
        if (random.nextInt(100) > 80) {
            return;
        }

        if (nearestCreature != null) {
            try {
                moveToDirection(actionOnNearestCreature());
            } catch (EmptyThingException e) {
                System.out.println(e);
                randomMove();
            }
        } else {
            randomMove();
        }
    }

    private Direction actionOnNearestCreature() {
        if (nearestCreature.col < this.col) {
            return Direction.LEFT;
        } else if (nearestCreature.col > this.col) {
            return Direction.RIGHT;
        } else if (nearestCreature.row < this.row) {
            return Direction.UP;
        } else {
            return Direction.DOWN;
        }

    }

    private void senseNearestCreature() {
        nearestCreature = null;
        ArrayList<Creature> nearCreatures = new ArrayList<>();
        for (int indexRow = row - 1; indexRow <= row + 1; indexRow++) {
            for (int indexCol = col - 1; indexCol < col + 1; indexCol++) {
                if (isValidMove(indexCol, indexRow)) {
                    if (SimulationGrid.creatureGrid[indexRow][indexCol] != null) {
                        nearCreatures.add(SimulationGrid.creatureGrid[indexRow][indexCol]);
                    }
                }
            }
        }

        if (nearCreatures.size() != 0) {
            int distance = 2;
            for (int i = 0; i < nearCreatures.size(); i++) {
                int row = nearCreatures.get(i).row;
                int col = nearCreatures.get(i).col;
                if (Math.abs(row - this.row) + Math.abs(col - this.col) < distance) {
                    nearestCreature = SimulationGrid.creatureGrid[row][col];
                    break;
                }
                nearestCreature = SimulationGrid.creatureGrid[row][col];
            }
        } else {
            nearestCreature = null;
        }
    }


    protected boolean moveToDirection(Direction direction) {
        boolean moveTo = false;

//        System.out.println(direction);
        switch (direction) {
            case RIGHT:
                if (isValidMove(this.col + 1, this.row)) {
                    moveTo = true;
                }
                break;
            case LEFT:
                if (isValidMove(this.col - 1, this.row)) {
                    moveTo = true;
                }
                break;
            case DOWN:
                if (isValidMove(this.col, this.row + 1)) {
                    moveTo = true;
                }
                break;
            case UP:
                if (isValidMove(this.col, this.row - 1)) {
                    moveTo = true;
                }
                break;
            default:
                moveTo = false;
                break;
        }
        // If can moveTo there, then update animalGrid
        if (moveTo) {
            SimulationGrid.monsterGrid[row][col] = null;
            switch (direction) {
                case RIGHT:
                    col++;
                    break;
                case LEFT:
                    col--;
                    break;
                case DOWN:
                    row++;
                    break;
                case UP:
                    row--;
                    break;
            }
            SimulationGrid.monsterGrid[row][col] = this;
        }
        return moveTo;
    }


    protected void randomMove() {
        Random r = new Random();
        boolean isNotValid = true;

        int direction = r.nextInt(4);
        while (isNotValid) {
            switch (Direction.values()[direction]) {
                case RIGHT:
                    if (!isValidMove(this.col + 1, this.row)) {
                        direction = r.nextInt(4);
                        continue;
                    }
                    break;
                case LEFT:
                    if (!isValidMove(this.col - 1, this.row)) {
                        direction = r.nextInt(4);
                        continue;
                    }
                    break;
                case DOWN:
                    if (!isValidMove(this.col, this.row + 1)) {
                        direction = r.nextInt(4);
                        continue;
                    }
                    break;
                case UP:
                    if (!isValidMove(this.col, this.row - 1)) {
                        direction = r.nextInt(4);
                        continue;
                    }
                    break;
            }
            isNotValid = false;
        }
        // after move, update animalGrid
        SimulationGrid.monsterGrid[row][col] = null;
        switch (Direction.values()[direction]) {
            case RIGHT:
                col++;
                break;
            case LEFT:
                col--;
                break;
            case DOWN:
                row++;
                break;
            case UP:
                row--;
                break;
        }
        SimulationGrid.monsterGrid[row][col] = this;
    }
}
