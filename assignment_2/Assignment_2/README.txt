My simulation settings:
The environment is a 30*30 grid.
Number of Strawberries = 50.
Number of Mushrooms = 20.
Number of Creatures = 50.
Number of Monsters = 30.
Crossover cut Chromosone index randomly from 1 to 5
Each creature has 5% chance to mutate, randomly happened from index 0 to 12.
Each creature and monster can detect its neighbor area consisted of 8 cells around it.
When there the time steps count down to zero and there is no survivor on the grid. It will restart the simulation process and the count of generation reset to 0.

The chromosone is an array index from 0 to 12.
The action value associated with chromosone[m] is begin from 0, such as
For chromosone index 5 which is action on nearest monster has possible action:
towards/away from/random/ignore 
then the associated value for chromosone [5] will be
0/1/2/3/


SimulationApp is the main excution class
// set the timer, change to 1000 will let the time steps cound down every 1 second.
private static final int DELAY = 10; 

// the environment virable to control the grid.
private int numOfRow = 30;
private int numOfColumn = 30;
private int numOfStrawberries = 50;
private int numOfMushrooms = 20;
private int numOfCreatures = 50;
private int numOfMonsters = 30;


FOR RUN THE SIMULATION
Just click the start button, it will automaticlly run the evolution for 200 generation.
(Ignore other buttons, they are for manulay run the simulation for debug)
