import javax.xml.stream.Location;
import java.util.ArrayList;
import java.util.Random;

/**
 * Created by zw on 5/5/16.
 */
public class SimulationGrid {
    public static int numOfRows;
    public static int numOfColumn;

    public static Creature[][] creatureGrid;
    public static Monster[][] monsterGrid;
    public static Mushroom[][] mushroomGrid;
    public static Strawberry[][] strawberryGrid;

    private static ArrayList<Mushroom> mushrooms;
    private static ArrayList<Strawberry> strawberries;
    private static ArrayList<Creature> creatures;
    private static ArrayList<Monster> monsters;

    private int numOfMushroom;
    private int numOfStrawberries;
    private int numOfCreatures;
    private int numOfMonsters;


    public SimulationGrid(int numOfRows, int numOfColumn, int numOfStrawberries, int numOfMushroom, int numOfCreatures, int numOfMonsters) {
        SimulationGrid.numOfRows = numOfRows;
        SimulationGrid.numOfColumn = numOfColumn;

        this.numOfStrawberries = numOfStrawberries;
        this.numOfMushroom = numOfMushroom;
        this.numOfCreatures = numOfCreatures;
        this.numOfMonsters = numOfMonsters;

        monsterGrid = new Monster[numOfRows][numOfColumn];
        mushroomGrid = new Mushroom[numOfRows][numOfColumn];
        creatureGrid = new Creature[numOfRows][numOfColumn];
        strawberryGrid = new Strawberry[numOfRows][numOfColumn];

        mushrooms = new ArrayList<>();
        strawberries = new ArrayList<>();
        creatures = new ArrayList<>();
        monsters = new ArrayList<>();

        setMushroomGrid();
        setStrawberryGrid();
        setCreatureGrid();
        setMonsterGrid();

    }

    private void setMushroomGrid() {
        for (int count = 0; count<numOfMushroom; count++) {
            boolean notSet = true;
            while (notSet) {
                Random random = new Random();
                int col = random.nextInt(numOfColumn);
                int row = random.nextInt(numOfRows);

                if (mushroomGrid[row][col] == null) {
                    Mushroom m = new Mushroom(col, row);
                    mushrooms.add(m);
                    mushroomGrid[row][col] = m;
                    notSet = false;
                }
            }
        }
    }

    private void setStrawberryGrid() {
        for (int count = 0; count<numOfStrawberries; count++) {
            boolean notSet = true;
            while (notSet) {
                Random random = new Random();
                int col = random.nextInt(numOfColumn);
                int row = random.nextInt(numOfRows);


                if (strawberryGrid[row][col] == null && mushroomGrid[row][col] == null) {
                    Strawberry s = new Strawberry(col, row);
                    strawberries.add(s);
                    strawberryGrid[row][col] = s;
                    notSet = false;
                }
            }
        }
    }

    private void setMonsterGrid() {
        for (int count = 0; count<numOfMonsters; count++) {
            boolean notSet = true;
            while (notSet) {
                Random random = new Random();
                int col = random.nextInt(numOfColumn);
                int row = random.nextInt(numOfRows);


                if (monsterGrid[row][col] == null) {
                    Monster m = new Monster(col, row);
                    monsters.add(m);
                    monsterGrid[row][col] = m;
                    notSet = false;
                }
            }
        }
    }

    private void setCreatureGrid() {
        for (int count = 0; count<numOfCreatures; count++) {
            boolean notSet = true;
            while (notSet) {
                Random random = new Random();
                int col = random.nextInt(numOfColumn);
                int row = random.nextInt(numOfRows);


                if (creatureGrid[row][col] == null) {
                    Creature c = new Creature(col, row);
                    creatures.add(c);
                    creatureGrid[row][col] = c;
                    notSet = false;
                }
            }
        }
    }


    protected static void eatCreature(int row, int col) {
        for (int i=0; i<creatures.size();i++) {
            if (creatures.get(i).row == row && creatures.get(i).col == col) {
                creatures.remove(i);
                creatureGrid[row][col] = null;
//                System.out.println("Creature left: " + creatures.size());
                break;
            }
        }
    }

    protected static void eatMushroom(int row, int col) {
        for (int i=0; i<mushrooms.size();i++) {
            if (mushrooms.get(i).row == row && mushrooms.get(i).col == col) {
                mushrooms.get(i).reduceFoodValue();
                if (mushrooms.get(i).getFoodValue()<0) {
                    mushrooms.remove(i);
                    mushroomGrid[row][col] = null;
                }
            }
        }
    }


    protected static void eatStrawberry(int row, int col) {
        for (int i=0; i<strawberries.size();i++) {
            if (strawberries.get(i).row == row && strawberries.get(i).col == col) {
                strawberries.get(i).reduceFoodValue();
                if (strawberries.get(i).getFoodValue()<0) {
                    strawberries.remove(i);
                    strawberryGrid[row][col] = null;
                }
            }
        }
    }


    public ArrayList<Mushroom> getMushrooms() {
        return mushrooms;
    }

    public ArrayList<Strawberry> getStrawberries() {
        return strawberries;
    }

    public ArrayList<Creature> getCreatures() {
        return creatures;
    }

    public ArrayList<Monster> getMonsters() {
        return monsters;
    }

    public void setNumOfMushroom(int numOfMushroom) {
        this.numOfMushroom = numOfMushroom;
    }

    public void setNumOfStrawberries(int numOfStrawberries) {
        this.numOfStrawberries = numOfStrawberries;
    }

    public void setNumOfCreatures(int numOfCreatures) {
        this.numOfCreatures = numOfCreatures;
    }

    public void setNumOfMonsters(int numOfMonsters) {
        this.numOfMonsters = numOfMonsters;
    }

    public void getRidOfDeadCreature() {
        for (int i=0; i<creatures.size(); i++) {
            if (!creatures.get(i).alive || creatures.get(i).getEnergyLevel()<=0) {
                int row = creatures.get(i).row;
                int col = creatures.get(i).col;
                creatureGrid[row][col] = null;
                creatures.remove(i);
//                System.out.println("Creature die, " + creatures.size() + " left.\n");
            }
        }
    }
}
