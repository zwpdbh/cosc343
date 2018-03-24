import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

/**
 * Created by zw on 4/30/16.
 */
public class SimulationApp extends JPanel {
    public static void main(String[] args) {
        JFrame frame = new JFrame("GenericSimulation");
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        frame.getContentPane().add(new SimulationApp());
        frame.pack();
        frame.setVisible(true);
    }

    private DrawingPanel drawingPanel;
    private JPanel controlPanel;
    public static final int sizeOfCell = 25;

    private int windowSizeWidth = SimulationGrid.numOfColumn*sizeOfCell;
    private int windowSizeHeight = SimulationGrid.numOfRows*sizeOfCell;

    private SimulationGrid grid;
    private Timer timer;
    private static final int DELAY = 10;
    private JButton[] buttons = {new JButton("start"), new JButton("stop"), new JButton("next step"), new JButton("next G")};
    private JLabel showInfo = new JLabel("Epoch");
    private JLabel showSteps = new JLabel("Steps");

    private int timeSteps;


    private int numOfRow = 30;
    private int numOfColumn = 30;
    private int numOfStrawberries = 50;
    private int numOfMushrooms = 20;
    private int numOfCreatures = 50;
    private int numOfMonsters = 30;

    private int[][] nextGenerations;
    private int generation ;

    public SimulationApp() {

        // generate grid and set its size
        // int numOfRows, int numOfColumn, int numOfStrawberries, int numOfMushroom, int numOfCreatures, int numOfMonsters

        // this is the value control the steps every simulation needed
        timeSteps = 99;

        nextGenerations = new int[numOfCreatures][13];

        grid = new SimulationGrid(numOfRow, numOfColumn, numOfStrawberries, numOfMushrooms, numOfCreatures, numOfMonsters);

        windowSizeWidth = SimulationGrid.numOfColumn*sizeOfCell;
        windowSizeHeight = SimulationGrid.numOfRows*sizeOfCell;

        controlPanel = new JPanel();
        controlPanel.setLayout(new GridLayout(6,1));
        drawingPanel = new DrawingPanel();

        if (windowSizeHeight<100) {
            windowSizeHeight = 100;
        }
        controlPanel.setPreferredSize(new Dimension(100, windowSizeHeight));

        CustomListener actionListener = new CustomListener();
        for (JButton each: buttons) {
            each.addActionListener(actionListener);
            controlPanel.add(each);
        }
        controlPanel.add(showInfo);
        controlPanel.add(showSteps);
        add(controlPanel);
        add(drawingPanel);
        // set timer
        timer = new Timer(DELAY, actionListener);
        generation = 0;
        showInfo.setText("" + generation);
        showSteps.setText("" + 99);
    }


    private class DrawingPanel extends JPanel {
        public DrawingPanel() {
            setPreferredSize(new Dimension(windowSizeWidth, windowSizeHeight));
            setBackground(Color.lightGray);
        }

        public void paintComponent(Graphics g) {
            super.paintComponent(g);
            // draw the line of grid
            g.setColor(Color.gray);
            for (int i=1; i<SimulationGrid.numOfColumn; i++) {
                g.drawLine(i*SimulationApp.sizeOfCell, 0, i*SimulationApp.sizeOfCell,SimulationGrid.numOfRows*SimulationApp.sizeOfCell);
            }
            for (int i=1; i<SimulationGrid.numOfRows; i++) {
                g.drawLine(0, i*SimulationApp.sizeOfCell, SimulationGrid.numOfColumn*SimulationApp.sizeOfCell, i*SimulationApp.sizeOfCell);
            }
            // draw each object on grid

            for (Strawberry each: grid.getStrawberries()) {
                each.display(g);
            }
            for (Mushroom each: grid.getMushrooms()) {
                each.display(g);
            }
            for (Creature each: grid.getCreatures()) {
                each.display(g);
            }
            for (Monster each: grid.getMonsters()) {
                each.display(g);
            }
        }

    }

    private class CustomListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == timer) {
                updateMove();
                timeSteps--;
                showSteps.setText(""+timeSteps);
                if (timeSteps<=0 || grid.getCreatures().size()<=5) {
                    timer.stop();
                    buttons[3].doClick();
                    buttons[0].doClick();
                }
            } else {
                JButton button = (JButton) e.getSource();
                String text = button.getText().toLowerCase();
                if (text.equals("start")) {
                    printChromosones();
                    timer.start();
                } else if (text.equals("stop")) {
                    timer.stop();
                } else if (text.equals("next step")) {
                    timer.stop();
                    updateMove();
                } else if (text.equals("next g")) {
                    grid.getRidOfDeadCreature();
                    grid.getRidOfDeadCreature();
                    if (grid.getCreatures().size()<=1) {
                        System.out.println("No two survivor to produce offspring, restart.");
                        grid = new SimulationGrid(numOfRow, numOfColumn, numOfStrawberries, numOfMushrooms, numOfCreatures, numOfMonsters);
                        generation = 0;
                    } else {
                        produceNextGeneration();
                        generation++;
                        if (generation>=200) {
                            System.out.println("Total 100 generation simulation finished");
                            System.exit(1);
                        }
                        grid = new SimulationGrid(numOfRow, numOfColumn, numOfStrawberries, numOfMushrooms, numOfCreatures, numOfMonsters);
                        for (int i=0; i<grid.getCreatures().size();i++) {
                            grid.getCreatures().get(i).setChomosone(nextGenerations[i]);
                        }
                    }
                    showInfo.setText("" + generation);
                    timeSteps = 99;
                    showSteps.setText("" + timeSteps);
                }
            }

            repaint();
        }
    }

    private void updateMove() {
        grid.getRidOfDeadCreature();
        for (Creature each : grid.getCreatures()) {
            each.move();
        }
        grid.getRidOfDeadCreature();
        for (Monster each : grid.getMonsters()) {
            each.move();
        }
        grid.getRidOfDeadCreature();
    }


    /**The GA part*/
    private void produceNextGeneration() {
        double[] eachNormalizedFitness = normalizeFitnessOfSurvivingCreature();

        for (int i=0; i<numOfCreatures; i++) {
            // choose parents based on fitness;
            Creature best = pickCreatureBasedOnFitness(eachNormalizedFitness);

            Creature secondBest = pickCreatureBasedOnFitness(eachNormalizedFitness);

            Random r = new Random();
            int c = r.nextInt(6) + 1;
            for (int index=0; index<=c;index++) {
                nextGenerations[i][index] = best.getChomosone()[index];
            }
            for (int index=c+1; index<nextGenerations[i].length; index++) {
                nextGenerations[i][index] = secondBest.getChomosone()[index];
            }

            int littleChance = r.nextInt(100);
            // have 5% chance mutate
            if (littleChance<5) {
                int index = r.nextInt(13);
                if (index<=1) {
                    if (nextGenerations[i][index] == 1) {
                        nextGenerations[i][index] = 0;
                    } else if (nextGenerations[i][index] == 0) {
                        nextGenerations[i][index] = 1;
                    }
                }
                if (index>=2 && index<=5) {
                    nextGenerations[i][index] = r.nextInt(4);
                }
                if (index>=7) { // mutate on weight
                    int indexA = r.nextInt(6) + 7;
                    int indexB = r.nextInt(6) + 7;
                    while (indexA==indexB) {
                        indexB = r.nextInt(6) + 7;
                    }

                    int tmp = nextGenerations[i][indexA];
                    nextGenerations[i][indexA] = nextGenerations[i][indexB];
                    nextGenerations[i][indexB] = tmp;
                }
            }
        }
    }

    private double[] normalizeFitnessOfSurvivingCreature() {
        // get all creatures fitness an normalize it.
        double totalFit = 0;

        System.out.println("Before normalize");
        int[] eachCreatureFitness = new int[grid.getCreatures().size()];
        for (int i=0; i<grid.getCreatures().size();i++) {
            Creature c = grid.getCreatures().get(i);
            System.out.print(c.getEnergyLevel() + " ");
            eachCreatureFitness[i] = grid.getCreatures().get(i).getEnergyLevel();
            totalFit += eachCreatureFitness[i];
        }

        System.out.format("\nThe average fitness of survivors in generation %d are %.2f / %d = %.2f", generation, totalFit, grid.getCreatures().size(), totalFit/grid.getCreatures().size());

        // normalize it
        System.out.println("\nAfter normalize");
        double[] normalizedEachFitness = new double[eachCreatureFitness.length];
        for (int i=0; i<eachCreatureFitness.length;i++) {
            normalizedEachFitness[i] = eachCreatureFitness[i]/totalFit;
            System.out.format("%.3f ", normalizedEachFitness[i]);
        }
        System.out.println();

        return normalizedEachFitness;
    }

    private Creature pickCreatureBasedOnFitness(double[] normalizedEachFitness) {
        Random r = new Random();
        double p = r.nextDouble();
        double cumulativeProbability = 0.0;

        int chosenOneIndex = 0;
        for (int i=0; i<normalizedEachFitness.length;i++) {
            cumulativeProbability += normalizedEachFitness[i];
            if (p < cumulativeProbability) {
                chosenOneIndex = i;
                break;
            }
        }
        return grid.getCreatures().get(chosenOneIndex);
    }

    private void printChromosones() {
        for (int i=0; i<grid.getCreatures().size(); i++) {
            grid.getCreatures().get(i).printOutChromosone();
            System.out.println();
        }
        System.out.println("");
    }


}
