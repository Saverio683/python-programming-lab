# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
# pylint: disable=invalid-name
# pylint: disable=unnecessary-lambda-assignment

from dataclasses import dataclass
from tkinter import Button
from typing import List, Literal, Tuple
from breezypythongui import EasyFrame

ROWS = 20
COLS = 20

@dataclass
class Cell:
    '''
        The Cell class is used to manage the game grid.
        ATTRIBUTES:
            -r,c: stand for row and column, they are the coordinates of the cell in the grid.
            -button: is the button that is shown on the screen, it is an instance of the Button class, the same one that returns 
            EasyFrame's addButton method.
            -is_snake_body: boolean value that determines whether the cell makes up the body of the snake.
            -is_apple: boolean to determine whether the cell is the apple.
            -bg: the background color, white by default.
    '''
    def __init__(self, button, r, c):
        self.r: int = r
        self.c: int = c
        self.button: Button = button
        self.is_snake_body: bool = False
        self.is_apple: bool = False
        bg: str = 'white'
        self.button.configure(bg=bg, highlightthickness=0, bd=0)

    def empty(self) -> None:
        self.__set_bg__('white')
        self.is_apple = False
        self.is_snake_body = False

    def apple(self) -> None:
        self.__set_bg__('red')
        self.is_apple = True

    def tail(self) -> None:
        self.__set_bg__('yellow')
        self.is_snake_body = True

    def head(self) -> None:
        self.__set_bg__('green')
        self.is_snake_body = True
    
    def body(self) -> None:
        self.__set_bg__('blue')
        self.is_snake_body = True

    def __set_bg__(self, bg: str) -> None:
        self.button.configure(bg=bg)

@dataclass
class Snake:
    '''
        Snake management class.
        ATTRIBUTES:
            -body: list of cells that make it up.
            The first cell in the list is the tail, the last will be the head.
    '''
    def __init__(self, body: List[Cell]):
        self.body = body
        self.body[0].tail()
        for cell in self.body[1:-1]:
            cell.body()
        self.body[-1].head()

    def move(self, next_direction: Literal['N', 'S', 'E', 'W'], master: EasyFrame) -> None:
        '''
            This method handles the advancement of the snake.
            To advance the snake, the tail is removed and a new head is added in front of the previous one
        '''
        def get_next_head_coordinates(prev_head: Cell, next_direction: Literal['N', 'S', 'E', 'W']) -> Tuple[int, int]:
            '''
                This function is used to calculate the position of the new head based on the direction
            '''
            r, c = prev_head.r, prev_head.c
            match next_direction:
                case 'N':
                    r -= 1
                    if r < 0: #the snake touches the top edge of the grid
                        master.outcome = 'L'
                        master.is_game_started = False
                        r = 0
                case 'S':
                    r += 1
                    if r > 19: #it touches the inferior edge
                        master.outcome = 'L'
                        master.is_game_started = False
                        r = 19
                case 'E':
                    c = (c + 1) % 20
                case 'W':
                    c = (c - 1 + 20) % 20
            return r, c

        grid = master.cells
        #delete tail
        prev_tail = self.body[0]
        grid[prev_tail.r][prev_tail.c].empty()
        del self.body[0]

        #new tail
        self.body[0].tail()

        #old head becomes body
        prev_head = self.body[-1]
        prev_head.body()

        #new head
        r,c = get_next_head_coordinates(prev_head, next_direction)
        new_head = grid[r][c]
        self.body.append(new_head)

        if new_head.is_snake_body: #check if the snake eats itself
            master.outcome = 'L'
            master.is_game_started = False
            master.cells[r][c].head()
            return

        def eat_apple(r, c, curr_head) -> None:
            '''
                With this function I check whether the apple has been eaten.
                The current head becomes body and the next cell becomes the new head
            '''
            if grid[r][c].is_apple:
                curr_head.body()
                r, c = get_next_head_coordinates(curr_head, next_direction)
                new_head = grid[r][c]
                self.body.append(new_head)
                master.__place_apple__()
                eat_apple(r, c, new_head)
            else:
                curr_head.head()
                if len(self.body) >= 200: #check for victory
                    master.outcome = 'W'
                    master.is_game_started = False
                    return

        eat_apple(r, c, new_head)

        #Update grid
        grid[new_head.r][new_head.c] = new_head
        for cell in self.body:
            master.cells[cell.r][cell.c] = cell

def update_ranking(username, score):
    '''
        This function adds the data of the last match in the text file
    '''
    with open('ranking.txt', 'r+', encoding='utf-8') as file:
        record: str = f'{score}-{username}'
        lines: List[str] = file.readlines()

        if not lines:
            file.write(record)
            return

        last_line = lines[-1].rstrip('\n')

        lines[-1] = last_line + f'\n{record}'

        file.seek(0)
        file.writelines(lines)

def show_ranking() -> List[Tuple[str, str]]:
    '''
        This function calculates the ranking of the top 5 players again
    '''
    data: List[Tuple[int, str]] = []

    with open('ranking.txt', 'r', encoding='utf-8') as file:
        for line in file:
            punteggio, _, username = line.strip().partition('-')
            data.append((int(punteggio), username))

    result = sorted(data, key=lambda x: x[0], reverse=True)

    return result[:5]
