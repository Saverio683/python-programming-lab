# Snake Game Application

## Game Board and Snake Setup

Using the Python programming language, create an application with the following features:

- The game board consists of a grid with 20×20 white square cells, each of size 15×15.
- The game's protagonist is a snake initially represented by ten consecutive squares, each adjacent only to the previous and next one.
- All squares are blue except for the head, which is green, and the tail, which is yellow. The game progresses in steps.

## Game Mechanics

- At the start of a new game, a red cell is randomly placed on the game grid.
- On the first step, the snake moves one position in a randomly chosen direction—up, down, right, or left.
- In subsequent steps, the snake moves one position in the direction determined by the previous movement, unless the player decides to change the direction.
- If the snake's head "eats" a red cell, it grows by one cell.
- Once a cell is eaten, another red cell is randomly placed in an unoccupied cell on the game board.
- The player must try to direct the snake's movements to avoid touching other cells. Touching results in the player losing.
- The player wins by filling at least 50% of the game board with the snake.

## Class Definitions

- Define appropriate classes for managing the snake and the grid.
- Identify suitable instance attributes and methods for these classes.
- The class representing the snake should contain an advance() method that handles the snake's movement.

## Graphical Interface

- Define a suitable graphical interface using the `breezypythongui` module.
- Display the game grid and the snake.
- Clicking the GAME button starts the game, with steps marked by a timer lasting one-tenth of a second.
- Direction changes are determined by clicking on NORTH, EAST, SOUTH, or WEST buttons.
- Three labels track time, cells eaten, and cells needed for victory.
- Clicking the STOP button interrupts the game.

## Initial Configuration

- In the initial setup, position the snake randomly with all cells in the same row.
- Alternatively, the player can position it by clicking on the cell where the head is placed.
- The rest of the snake will be positioned further to the right in the same row.

## Circular Game Board

- Consider that the game board is horizontally circular, treating the first and last columns as consecutive.

## Score and Leaderboard

- At the end of the game, store the player's name and score in a file.
- Clicking the LEADERBOARD button displays the top 5 players.

## Project Preview

![Snake Game](https://i.imgur.com/4wsS1eU.png)