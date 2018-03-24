
import java.awt.*;
import java.util.ArrayList;
import java.util.Random;

/**
 * Created by zw on 5/5/16.
 */
public class Creature extends Animal {

    private int energyLevel = 100;
    public boolean alive = true;
    private Mushroom nearestMushroom;
    private Strawberry nearestStrawberry;
    private Monster nearestMonster;
    private Creature nearestCreature;

    private int[] chomosone = new int[13];

    public Creature() {
        super();
        color = Color.gray;
        generateChomosoneRandomly();
    }

    public Creature(int col, int row) {
        super(col, row);
        color = Color.gray;
        generateChomosoneRandomly();
    }

    @Override
    public void display(Graphics g) {
        g.setColor(Color.WHITE);
        g.drawString("" + this.energyLevel, col * SimulationApp.sizeOfCell, row * SimulationApp.sizeOfCell);
        g.setColor(this.color);
        super.display(g);
    }


    private static void shuffle(int[] arr) {
        Random r = new Random();
        for (int i = arr.length - 1; i > 0; i--) {
            int index = r.nextInt(i + 1);
            // swap
            int tmp = arr[index];
            arr[index] = arr[i];
            arr[i] = tmp;
        }
    }

    public int getEnergyLevel() {
        return energyLevel;
    }

    public int[] getChomosone() {
        return chomosone;
    }

    public void setChomosone(int[] chomosone) {
        this.chomosone = chomosone;
    }

    private void generateChomosoneRandomly() {
        Random random = new Random();
        chomosone[0] = random.nextInt(2);
        chomosone[1] = random.nextInt(2);
        chomosone[2] = random.nextInt(4);
        chomosone[3] = random.nextInt(4);
        chomosone[4] = random.nextInt(4);
        chomosone[5] = random.nextInt(4);
        chomosone[6] = random.nextInt(5);

        // generate chomosone weight, ranges from 1 to 6;
        int[] weights = new int[6];
        for (int i = 0; i < weights.length; i++) {
            weights[i] = i + 1;
        }
        shuffle(weights);
        for (int i = 0; i < weights.length; i++) {
            chomosone[7 + i] = weights[i];
        }

//        setChomosone(new int[]{0,0,0,0,5,1,0,1,2,3,5,4,6});
    }


    public void moveBasedOnChomosone() {
        this.energyLevel--;
        if (this.energyLevel <= 0 || SimulationGrid.monsterGrid[this.row][this.col] != null) {
            alive = false;
            return;
        }

        boolean mushroomPresent = false;
        boolean strawberryPresent = false;

        mushroomPresent = senseMushroomPresent();
        strawberryPresent = senseStrawberryPresent();
        senseNearestMushroom();
        senseNearestStrawberry();
        senseNearestCreature();
        senseNearestMonster();


        int[] actionList = {0, 0, 0, 0, 0, 0};


        if (mushroomPresent && chomosone[0] != 1) {
            actionList[0] = 1;
        }
        if (strawberryPresent && chomosone[1] != 1) {
            actionList[1] = 1;
        }
        if (nearestMushroom != null && chomosone[2] != 3) {
            actionList[2] = 1;
        }
        if (nearestStrawberry != null && chomosone[3] != 3) {
            actionList[3] = 1;
        }
        if (nearestCreature != null && chomosone[4] != 3) {
            actionList[4] = 1;
        }
        if (nearestMonster != null && chomosone[5] != 3) {
            actionList[5] = 1;
        }

        int countAction = 0;
        for (int i = 0; i < actionList.length; i++) {
            countAction += actionList[i];
        }
        if (countAction != 0) {
            int index = -1;
            int weight = -1;
            // get the heaviest weight and its index
            for (int i = 0; i<actionList.length; i++) {
                if (actionList[i]!=0 && chomosone[i + 7] > weight) {
                    weight = chomosone[i+7];
                    index = i;
                }
            }
//            senseResult(this);
            if (index == -1) {
                System.out.println("index = -1");
                System.exit(1);
            }
//            else {
//                System.out.println("Choose action on index: " + index);
//                System.out.println("Its weight is: " + weight);
//                System.out.println("Associated chomoson: " + this.chomosone[index] + "\n");
//            }
            switch (index) {
                case 0:
                    if (chomosone[0] == 0 && mushroomPresent) {
                        this.energyLevel = 0;
                        this.alive = false;
                    } else if (chomosone[0] == 1) {
                        System.out.println("Ignore");
                        return;
                    }
                    break;
                case 1:
                    if (chomosone[1] == 0 && strawberryPresent) {
                        this.energyLevel += 4;
                        SimulationGrid.eatStrawberry(row, col);
                        if (this.energyLevel > 100) {
                            this.energyLevel = 100;
                        }
                    } else if (chomosone[1] == 1) {
                        System.out.println("Ignore");
                        return;
                    }
                    break;
                case 2:
                    if (chomosone[2] == 0) {
                        moveToDirection(moveTowardsNearestMushroom());
                    } else if (chomosone[2] == 1) {
                        moveToDirection(moveAwayFromNearestMushroom());
                    } else if (chomosone[2] == 2) {
                        randomMove();
                    } else if (chomosone[2] == 3) {
                        System.out.println("Ignore");
                        return;
                    }
                    break;
                case 3:
                    if (chomosone[3] == 0) {
                        moveToDirection(moveTowardsNearestStrawberry());
                    } else if (chomosone[3] == 1) {
                        moveToDirection(moveAwayFromNearestStrawberry());
                    } else if (chomosone[3] == 2) {
                        randomMove();
                    } else if (chomosone[3] == 3) {
                        System.out.println("Ignore");
                        return;
                    }
                    break;
                case 4:
                    if (chomosone[4] == 0) {
                        moveToDirection(moveTowardsNearestCreature());
                    } else if (chomosone[4] == 1) {
                        moveToDirection(moveAwayFromNearestCreature());
                    } else if (chomosone[4] == 2) {
                        randomMove();
                    } else if (chomosone[4] == 3) {
                        System.out.println("Ignore");
                        return;
                    }
                    break;
                case 5:
                    if (chomosone[5] == 0) {
                        moveToDirection(moveTowardsNearestMonster());
                    } else if (chomosone[5] == 1) {
                        moveToDirection(moveAwayFromNearestMonster());
                    } else if (chomosone[5] == 2) {
                        randomMove();
                    } else if (chomosone[5] == 3) {
                        System.out.println("Ignore");
                        return;
                    }
                    break;
                default:
                    randomMove();
                    break;
            }
        } else {        // move randomly or according to chomosone
            switch (chomosone[6]) {
                case 0:
                    randomMove();
                    break;
                case 1:
                    moveToDirection(Direction.UP);
                    break;
                case 2:
                    moveToDirection(Direction.RIGHT);
                    break;
                case 3:
                    moveToDirection(Direction.DOWN);
                    break;
                case 4:
                    moveToDirection(Direction.LEFT);
                    break;
                default:
                    randomMove();
                    break;
            }
        }
    }

    private void doChomosoneSix() {
        switch (chomosone[6]) {
            case 0:
                randomMove();
                break;
            case 1:
                moveToDirection(Direction.UP);
                break;
            case 2:
                moveToDirection(Direction.RIGHT);
                break;
            case 3:
                moveToDirection(Direction.DOWN);
                break;
            case 4:
                moveToDirection(Direction.LEFT);
                break;
            default:
                randomMove();
                break;
        }
    }


    public void move() {
        moveBasedOnChomosone();
    }


    /**
     * Movement about nearestCreature
     */
    // move away
    private Direction moveAwayFromNearestCreature() {
        if (nearestCreature.col < this.col && (this.col + 1 < SimulationGrid.numOfColumn)) {
            return Direction.RIGHT;
        } else if (nearestCreature.col > this.col && (this.col - 1 > 0)) {
            return Direction.LEFT;
        } else if (nearestCreature.row < this.row && (this.row + 1 < SimulationGrid.numOfRows)) {
            return Direction.DOWN;
        } else {
            return Direction.UP;
        }
    }

    private Direction moveTowardsNearestCreature() {
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


    /**
     * Movement about nearestMonster
     */
    // move away
    private Direction moveAwayFromNearestMonster() throws EmptyThingException {

        if (nearestMonster.col < this.col && (this.col + 1 < SimulationGrid.numOfColumn)) {
            return Direction.RIGHT;
        } else if (nearestMonster.col > this.col && (this.col - 1 > 0)) {
            return Direction.LEFT;
        } else if (nearestMonster.row < this.row && (this.row + 1 < SimulationGrid.numOfRows)) {
            return Direction.DOWN;
        } else {
            return Direction.UP;
        }

    }

    // move towards
    private Direction moveTowardsNearestMonster() throws EmptyThingException {
        if (nearestMonster.col < this.col) {
            return Direction.LEFT;
        } else if (nearestMonster.col > this.col) {
            return Direction.RIGHT;
        } else if (nearestMonster.row < this.row) {
            return Direction.UP;
        } else {
            return Direction.DOWN;
        }

    }

    /**
     * Movement about Strawberry
     */
    // move towards
    private Direction moveTowardsNearestStrawberry() throws EmptyThingException {
        if (nearestStrawberry.col < this.col) {
            return Direction.LEFT;
        } else if (nearestStrawberry.col > this.col) {
            return Direction.RIGHT;
        } else if (nearestStrawberry.row < this.row) {
            return Direction.UP;
        } else {
            return Direction.DOWN;
        }

    }

    // move away
    private Direction moveAwayFromNearestStrawberry() throws EmptyThingException {
        if (nearestStrawberry.col < this.col && (this.col + 1 < SimulationGrid.numOfColumn)) {
            return Direction.RIGHT;
        } else if (nearestStrawberry.col > this.col && (this.col - 1 > 0)) {
            return Direction.LEFT;
        } else if (nearestStrawberry.row < this.row && (this.row + 1 < SimulationGrid.numOfRows)) {
            return Direction.DOWN;
        } else {
            return Direction.UP; //creature could stuck at the left corner of grid, when there is a mushroom at (1,0)
        }

    }


    /**
     * movement about Mushroom========================================================
     */
    // move away
    private Direction moveAwayFromNearestMushroom() throws EmptyThingException {
        if (nearestMushroom.col < this.col && (this.col + 1 < SimulationGrid.numOfColumn)) {
            return Direction.RIGHT;
        } else if (nearestMushroom.col > this.col && (this.col - 1 > 0)) {
            return Direction.LEFT;
        } else if (nearestMushroom.row < this.row && (this.row + 1 < SimulationGrid.numOfRows)) {
            return Direction.DOWN;
        } else {
            return Direction.UP; //creature could stuck at the left corner of grid, when there is a mushroom at (1,0)
        }
    }

    // move towards
    private Direction moveTowardsNearestMushroom() throws EmptyThingException {
        if (nearestMushroom.col < this.col) {
            return Direction.LEFT;
        } else if (nearestMushroom.col > this.col) {
            return Direction.RIGHT;
        } else if (nearestMushroom.row < this.row) {
            return Direction.UP;
        } else {
            return Direction.DOWN; //creature could stuck at the left corner of grid, when there is a mushroom at (1,0)
        }
    }

    /**
     * Mushroom=========================================================================
     */

    protected boolean moveToDirection(Direction direction) {
        boolean moveTo = false;

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
            SimulationGrid.creatureGrid[row][col] = null;
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
            SimulationGrid.creatureGrid[row][col] = this;
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
        SimulationGrid.creatureGrid[row][col] = null;
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
        SimulationGrid.creatureGrid[row][col] = this;
        //System.out.println("Creature is random moving");
    }


    /**
     * Sense Nearest Monster=============================================================
     */
    private void senseNearestMonster() {
        nearestMonster = null;
        ArrayList<Monster> nearMonsters = new ArrayList<>();
        for (int indexRow = row - 1; indexRow <= row + 1; indexRow++) {
            for (int indexCol = col - 1; indexCol <= col + 1; indexCol++) {
                if (isValidMove(indexCol, indexRow)) {
                    if (SimulationGrid.monsterGrid[indexRow][indexCol] != null) {
                        nearMonsters.add(SimulationGrid.monsterGrid[indexRow][indexCol]);
                    }
                }
            }
        }

        if (nearMonsters.size() != 0) {
            int distance = 2;
            for (int i = 0; i < nearMonsters.size(); i++) {
                int row = nearMonsters.get(i).row;
                int col = nearMonsters.get(i).col;
                if (Math.abs(row - this.row) + Math.abs(col - this.col) < distance) {
                    nearestMonster = SimulationGrid.monsterGrid[row][col];
                    break;
                }
                nearestMonster = SimulationGrid.monsterGrid[row][col];
            }
        } else {
            nearestMonster = null;
        }
    }

    /**
     * Sense nearest Creature=============================================================
     */
    private void senseNearestCreature() {
        nearestCreature = null;
        ArrayList<Creature> nearCreatures = new ArrayList<>();
        for (int indexRow = row - 1; indexRow <= row + 1; indexRow++) {
            for (int indexCol = col - 1; indexCol < col + 1; indexCol++) {
                if (indexCol == this.col && indexRow == this.row) {
                    continue;
                }
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

    private void senseNearestStrawberry() {
        nearestStrawberry = null;
        ArrayList<Strawberry> nearestStrawberries = new ArrayList<>();

        for (int indexRow = row - 1; indexRow <= row + 1; indexRow++) {
            for (int indexCol = col - 1; indexCol <= col + 1; indexCol++) {
                if (indexCol == this.col && indexRow == this.row) {
                    continue;
                }
                if (isValidMove(indexCol, indexRow)) {
                    if (SimulationGrid.strawberryGrid[indexRow][indexCol] != null) {
                        nearestStrawberries.add((Strawberry) SimulationGrid.strawberryGrid[indexRow][indexCol]);
                    }
                }
            }
        }

        if (nearestStrawberries.size() != 0) {
            int distance = 2;
            for (int i = 0; i < nearestStrawberries.size(); i++) {
                int row = nearestStrawberries.get(i).row;
                int col = nearestStrawberries.get(i).col;
                if (Math.abs(row - this.row) + Math.abs(col - this.col) < distance) {
                    nearestStrawberry = (Strawberry) SimulationGrid.strawberryGrid[row][col];
                    break;
                }
                nearestStrawberry = (Strawberry) SimulationGrid.strawberryGrid[row][col];
            }
        } else {
            nearestStrawberry = null;
        }
    }

    /**
     * Sense nearest Mushroom and Strawberry=====================================
     */
    private void senseNearestMushroom() {
        nearestMushroom = null;
        ArrayList<Mushroom> nearestMushrooms = new ArrayList<>();

        for (int indexRow = row - 1; indexRow <= row + 1; indexRow++) {
            for (int indexCol = col - 1; indexCol <= col + 1; indexCol++) {
                if (indexCol == this.col && indexRow == this.row) {
                    continue;
                }
                if (isValidMove(indexCol, indexRow)) {
                    if (SimulationGrid.mushroomGrid[indexRow][indexCol] != null) {
                        nearestMushrooms.add(SimulationGrid.mushroomGrid[indexRow][indexCol]);
                    }
                }
            }
        }

        if (nearestMushrooms.size() != 0) {
            int distance = 2;
            for (int i = 0; i < nearestMushrooms.size(); i++) {
                int row = nearestMushrooms.get(i).row;
                int col = nearestMushrooms.get(i).col;
                if (Math.abs(row - this.row) + Math.abs(col - this.col) < distance) {
                    nearestMushroom = SimulationGrid.mushroomGrid[row][col];
                    break;
                }
                nearestMushroom = SimulationGrid.mushroomGrid[row][col];
            }
        } else {
            nearestMushroom = null;
        }

    }


    /**
     * sense PRESENT mushroom and strawberry
     */
    private boolean senseStrawberryPresent() {
        if (SimulationGrid.strawberryGrid[this.row][this.col] != null) {
            if (SimulationGrid.strawberryGrid[this.row][this.col] instanceof Strawberry) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    private boolean senseMushroomPresent() {
        if (SimulationGrid.mushroomGrid[this.row][this.col] != null) {
            if (SimulationGrid.mushroomGrid[this.row][this.col] instanceof Mushroom) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    public void printOutChromosone() {
        for (int i = 0; i < chomosone.length; i++) {
            System.out.print(chomosone[i] + " ");
        }
    }

    private String printOutPosition(Thing t) {
        return ("<" + t.col + "," + t.row + ">");
    }

    private void senseResult(Thing t) {
        if (nearestMushroom != null) {
            System.out.println("Nearest Mushroom: " + printOutPosition(t));
        }
        if (nearestStrawberry != null) {
            System.out.println("Nearest Strawberry: " + printOutPosition(t));
        }
    }

    private void setCertainChomosones(int[] chomo) {
        for (int i = 0; i < chomo.length; i++) {
            this.chomosone[i] = chomo[i];
        }
    }
}
