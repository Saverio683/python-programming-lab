# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
# pylint: disable=invalid-name

import threading
import random
from tkinter import Button
from typing import List, Literal, Tuple
from breezypythongui import EasyFrame
from game import Cell, Snake, update_ranking, show_ranking

#costanti globali
ROWS = 20
COLS = 20
#durata dell'intervallo in secondi
TIME = 0.2
BACKGROUND_COLOR = '#09B5FF'

class Main(EasyFrame):
    '''
        This is the main class where the game window and its states are managed.
        ATTRIBUTES:
            -cells: array of cells, represents the game grid.
            -is_game_started: boolean value that holds monitors whether the game has started. The game can start 
            by clicking on the 'start' button or on a grid cell.
            -is_game_paused: keeps track of whether the game has been paused by clicking on the appropriate button
            -outcome: represents the result of the game, can be 'L' in case of defeat (lose), w in case
            of win (win) and '' if the game is in progress or has not yet started.
            -direction: the direction of the snake, indicated by the cardinal points.
            -seconds: is a counter that keeps track of the seconds elapsed since the start of the game.
            -apple_coordinates: the coordinates of the apple in the grid.
            -snake: is an instance of the Snake class, which keeps track of the snake's movements and state
            during the game.
    '''
    def __init__(self):
        EasyFrame.__init__(self, title='Snake', background='black', resizable=False)

        self.cells: List[List['Cell']] = [[Cell for _ in range(COLS)] for _ in range(ROWS)]
        self.is_game_started: bool = False
        self.is_game_paused: bool = False
        self.outcome: Literal['', 'W', 'L'] = ''
        self.direction: Literal['N', 'S', 'E', 'W']
        self.seconds: int = 0
        self.apple_coordinates: Tuple[int, int] = (None,None)
        self.snake: 'Snake' = None

        #Creating che GUI
        self.__build_window__()

        #Initialize the threads for rendering the grid and timer
        self.grid_thread = threading.Timer(TIME, self.__handle_game__)
        self.timer_thread = threading.Timer(1, self.__handle_game__)

    def __on_key_press__(self, key: str) -> None:
        '''
            Event that detects which direction key has been pressed and updates the direction state, only if
            a different key was pressed than the previous one, so as not to unnecessarily update 
            the direction attribute.
        '''
        if self.direction != key:
            match key:
                case 'N':
                    if self.direction != 'S':
                        self.direction = key
                case 'S':
                    if self.direction != 'N':
                        self.direction = key
                case 'W':
                    if self.direction != 'E':
                        self.direction = key
                case 'E':
                    if self.direction != 'W':
                        self.direction = key

    def __on_start_button_click__(self, x: int = None, y: int = None) -> None:
        '''
            Start button event. 
            The x and y attributes are passed when the user clicks on the grid to 
            place the serpende where he wants it, if he clicks the 'start' button instead then
            x and y will be generated later
        '''
        if not self.is_game_started:
            if self.outcome: #Delete the words 'game over' or 'you won'
                for r in range(ROWS):
                    for c in range(COLS):
                        self.cells[r][c].empty()
                self.outcome = ''
                return
            if self.username.getText() in ['Username', '', ' ']: #Username check
                self.error_message.config(foreground='red')
            else:
                if x and y:
                    self.__build_snake__(x, y)
                else:
                    self.__build_snake__()
                #Place the apple and reinitialize the game states
                self.__place_apple__()
                self.error_message.config(foreground=BACKGROUND_COLOR)
                self.is_game_started = True
                self.is_game_paused = False
                #Start threads
                self.__handle_game__()
                self.__start_timer__()
                
                #Remove the focus from the input of the username
                self.focus_set()

    def __on_pause_button_click__(self) -> None:
        '''
            Pause button event
        '''
        self.focus_set()
        if self.is_game_started: #Check if the game has started
            self.is_game_paused = not self.is_game_paused
            self.__handle_game__()

    def __start_timer__(self) -> None:
        '''
            This method starts the timer, managed by a thread that updates at 1s intervals
        '''
        if self.is_game_started:
            self.timer_thread = threading.Timer(1.0, self.__start_timer__) # Re-initiating the thread
            #the 'daemon' parameter should be set to True so when you close the Main window, the thread will also stop its life cycle
            self.timer_thread.daemon = True
            self.timer_thread.start()
            self.seconds += 1
            self.time_label['text'] = f'Time: {self.seconds}s'
        else:
            self.timer_thread.cancel() #stop timer
            self.seconds = 0

    def __handle_game__(self) -> None:
        '''
            This method manages the flow of the game.
            If the game is running it manages the thread that renders the grid periodically and updates it 
            as a result of snaemnte moves and apple placement.
            When the game is over, the user is saved and the leaderboard is updated and shown on the grid
            the words 'game over' or 'you won'.
        '''
        if self.is_game_started:  
            if self.is_game_paused:
                self.grid_thread.cancel() #pause the game rendering
            else:
                self.grid_thread = threading.Timer(TIME, self.__handle_game__) #Re-inizializzazione del thread
                self.grid_thread.daemon = True
                self.grid_thread.start()
                self.occupied_cells_label['text'] = f'Occupied cells: {len(self.snake.body)}'
                self.remained_cells_label['text'] = f'Remaining cells: {ROWS*COLS - (len(self.snake.body) + 200)}'
                self.snake.move(self.direction, self)
        else:
            update_ranking(self.username.getText(), len(self.snake.body)) #update the ranking
            self.grid_thread.cancel()
            self.occupied_cells_label['text'] = ''
            self.remained_cells_label['text'] = ''
            self.time_label['text'] = ''
            self.username.setText('Username')
            self.__draw_grid__(self.outcome == 'W') #Write 'game over' or 'you won' on the grid

    def __draw_grid__(self, is_victory: bool) -> None:
        '''
            This is the method that writes the writing of defeat or victory on the grid.
            First the grid is cleaned by erasing the apple and the snake.
        '''
        (x,y) = self.apple_coordinates
        self.cells[x][y].empty() #delete the apple and the snake
        for cell in self.snake.body:
            cell.empty()
        coordinates: List[Tuple[int, int]] = []
        if is_victory:
            coordinates = [
                [(2,5), (3,5), (4,5), (5,5), (6,5), (4,6), (2,7), (3,7), (4,7), (5,7), (6,7)],
                [(3,9), (4,9), (5,9), (6,9), (2,10), (4,10), (3,11), (4,11), (5,11), (6,11)],
                [(2,13), (3,13), (4,13), (5,13), (6,13)],
                [(10,1), (11,1), (12,1), (13,1), (14,2), (13,3), (12,3), (11,3), (10,3)],
                [(10,5), (11,5), (12,5), (13,5), (14,5)],
                [(10,7), (11,7), (12,7), (13,7), (14,7), (11,8), (12,9), (10,10), (11,10), (12,10), (13,10), (14,10)],
                [(10,12), (10,13), (10,14), (11,13), (12,13), (13,13), (14,13)],
                [(10,17), (10,18), (11,16), (12,16), (13,16), (14,17), (14,18), (11,19), (12,19), (13,19)]
            ]
        else:
            coordinates = [
                [(2,2), (2,3), (2,4), (3,1), (4,1), (5,1), (6,4), (6,2), (6,3), (6,4), (5,4), (4,4), (4,3)],
                [(3,6), (4,6), (5,6), (6,6), (2,7), (4,7), (3,8), (4,8), (5,8), (6,8)],
                [(2,10), (3,10), (4,10), (5,10), (6,10), (3,11), (4,12), (3,13), (2,14), (3,14), (4,14), (5,14), (6,14)],
                [(2,16), (3,16), (4,16), (5,16), (6,16), (2,17), (2,18), (4,17), (4,18), (6,17), (6,18)],
                [(10,2), (10,3), (11,1), (12,1), (13,1), (14,2), (14,3), (11,4), (12,4), (13,4)],
                [(10,6), (11,6), (12,6), (13,6), (14,7), (10,8), (11,8), (12,8), (13,8)],
                [(10,10), (11,10), (12,10), (13,10), (14,10), (10,11), (10,12), (12,11), (12,12), (14,11), (14,12)],
                [(10,14), (11,14), (12,14), (13,14), (14,14), (10,15), (10,16), (10,17), (12,15), (12,16), (12,17), (11, 17), (13,16), (14,17)]
            ]
        for char in coordinates:
            for (x,y) in char:
                self.cells[x][y].__set_bg__('green' if is_victory else 'red')

    def __place_apple__(self) -> None:
        '''
            Method that randomly places apple on the grid
        '''
        if not self.outcome: #the apple is placed only during the game
            x,y = None, None
            while True:
                #chose to use the 'choices' method of random rather than others because this method
                #can return a pair of equal values (x = y), and thus be able to place the apple in the diagonal
                x,y = random.choices(range(20), k=2)
                if not self.cells[x][y].is_snake_body: #check if the apple is not placed in the snake body
                    break
            self.cells[x][y].apple()
            self.apple_coordinates = (x,y)

    def __build_snake__(self, x: int = None, y: int = None):
        '''
            Method that places the snake on the grid.
            x and y are the coordinates of the button, if the user has decided to place the snake where he wants it.
        '''
        self.direction = 'W'
        snake_body: List['Cell'] = []
        snake_len = 10
        if not x and not y:
            x,y = random.choices(range(20), k=2)
        for c in reversed(range(y+1, y+snake_len)):
            if c > 19:
                snake_body.append(self.cells[x][c-20])
            else:
                snake_body.append(self.cells[x][c])
        snake_body.append(self.cells[x][y])
        self.snake = Snake(snake_body)

    def __build_grid__(self) -> None: 
        '''
            This method builds the grid
        '''
        for r in range(ROWS):
            for c in range(COLS):
                button = self.addButton('', r+3, c, command=lambda x=r, y=c: self.__on_start_button_click__(x, y))
                #definisco il bordo superiore e inferiore della griglia
                pady = (6,1) if r == 0 else (1,6) if r == 19 else 1
                button.grid(row=r+3, column=c, padx=1, pady=pady, sticky='nsew')
                button.config(height=1, width=1)
                self.cells[r][c] = Cell(button, r, c)

    def __build_window__(self) -> None:
        '''
            In this method all components of the game window are added.
            'panel1' contains the input for the username and the start and pause buttons.
            'panel2' is just for making space.
            'panel3' contains the 3 game labels and the button to show the leaderboard.
        '''
        self.bind('<Key>', self.__on_key_press_event__) #key press event
        self.configure(borderwidth=0, highlightthickness=0)
        self.__build_grid__()
        self.panel1 = self.addPanel(row=0, column=0, columnspan=20, background=BACKGROUND_COLOR)
        #empty panel
        self.addPanel(row=1, column=0, columnspan=20, background=BACKGROUND_COLOR).addLabel('', 1, 0, background=BACKGROUND_COLOR)
        self.panel3 = self.addPanel(row=23, column=0, columnspan=20, background=BACKGROUND_COLOR)

        self.username = self.panel1.addTextField('Username', 0, 0, sticky='W')
        self.start = self.panel1.addButton('Start', 0, 1, command=self.__on_start_button_click__)
        self.pause = self.panel1.addButton('Pause', 0, 2, command=self.__on_pause_button_click__)

        for widget in self.panel1.winfo_children(): #iterate through panel buttons
            if isinstance(widget, Button):
                widget.config(borderwidth=0, highlightthickness=1, highlightbackground='#000')

        #Blank label to place other elements correctly
        self.panel1.addLabel('', 0, 3, sticky='W', background=BACKGROUND_COLOR) 
        
        #label of the error message, in case of failure to enter the username
        self.error_message = self.panel1.addLabel('', 0, 20, background=BACKGROUND_COLOR, foreground=BACKGROUND_COLOR)
        #by default the label is 'invisible', that is, it has the text color as the background color in case of an error, it changes its color to red.
        self.error_message['text'] = 'Invalid username'

        #panel3 labels are blank until the game starts
        self.time_label = self.panel3.addLabel('', 0, 0, background=BACKGROUND_COLOR, foreground='white')
        self.occupied_cells_label = self.panel3.addLabel('', 0, 1, background=BACKGROUND_COLOR, foreground='white')
        self.remained_cells_label = self.panel3.addLabel('', 0, 2, background=BACKGROUND_COLOR, foreground='white')
        self.panel3.addLabel('', 0, 4, sticky='WE', background=BACKGROUND_COLOR, columnspan=20)
        self.panel3.addButton('Show ranking', 0, 20, command=self.__on_ranking_button_click__)

        #function that iterates over a panel's buttons to apply default styles to them
        #this function saves considerable lines of code and makes it more readable
        def configure_buttons(panel, background_color):
            for widget in panel.winfo_children():
                if isinstance(widget, Button):
                    widget.config(borderwidth=0, highlightthickness=1, highlightbackground='#000', fg='#000', background=background_color)

        configure_buttons(self.panel1, '#fff')
        configure_buttons(self.panel3, '#fff')

    def __on_key_press_event__(self, event) -> None:
        '''
            Event called when a key on the keyboard is pressed.
        '''
        key = event.keysym
        if key in ['w', 'a', 's', 'd']:
            match(key):
                case 'a':
                    self.__on_key_press__('W')
                case 'd':
                    self.__on_key_press__('E')
                case 'w':
                    self.__on_key_press__('N')
                case _: #S
                    self.__on_key_press__(key.upper())

    def __on_ranking_button_click__(self) -> None:
        '''
            This event shows the window containing the ranking
        '''
        if not self.is_game_started: #ranking cannot be opened if the current game
            result: str = ''
            data = show_ranking()
            for index, (score, username) in enumerate(data, start=1):
                result += f'{index}) {username}: {score}\n'
            result = result.rstrip('\n')
            self.messageBox('RANKING', result, 30)

def main():
    Main().mainloop()

if __name__ == '__main__':
    main()
