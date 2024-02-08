# Snake Game Application

Using the Python programming language, create an application with the following features:

- The game board consists of a grid with 20×20 white square cells, each of size 15×15.
- The game's protagonist is a snake initially represented by ten consecutive squares, each adjacent only to the previous and next one.
- All squares are blue except for the head, which is green, and the tail, which is yellow. The game progresses in steps.

    - At the start of a new game, a red cell is randomly placed on the game grid.
    - On the first step, the snake moves one position in a randomly chosen direction—up, down, right, or left. The term "moves one position" means that each cell, except the head, takes the position of the preceding cell. In subsequent steps, the snake moves one position in the direction determined by the previous movement, unless the player decides to change the direction.

    - If the snake's head "eats" a red cell, it grows by one cell. Once a cell is eaten, another red cell is randomly placed in an unoccupied cell on the game board. The player must try to direct the snake's movements so that the head never touches any of the other cells. In that case, the player loses. The player wins if they manage to fill at least 50% of the game board with the snake.

    - Define appropriate classes for managing the snake and the grid. Identify suitable instance attributes and methods for these classes. In particular, the class representing the snake should contain an advance() method that handles the snake's movement.

    - Define a suitable graphical interface for managing the application using the `breezypythongui` module, showing the game grid and the snake. Clicking the GAME button starts the game. The game steps are marked by a timer where each scan lasts one-tenth of a second. Direction changes are determined by clicking on four respective buttons: NORTH, EAST, SOUTH, WEST. Three labels keep track of time, cells eaten, and how many cells are needed for victory. Clicking the STOP button interrupts the game.

    - In the initial configuration, the snake must be randomly positioned with all cells in the same row. Alternatively, the player can position it by clicking on the cell where the head is placed. The rest of the snake will be positioned further to the right in the same row.

    - Consider that the game board is considered horizontally circular, meaning the first column and the last column are considered consecutive.

    - At the end of the game, the player's name and score are stored in a file. Clicking the RANKING button displays the top 5 players.
