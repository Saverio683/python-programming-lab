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
TIME = 0.1
BACKGROUND_COLOR = '#09B5FF'

class Main(EasyFrame):
    '''
        Questa è la classe principale dove viene gestita la finestra del gioco e i suoi stati.
        ATTRIBUTI:
            -cells: matrice di celle, rappresenta la griglia di gioco.
            -is_game_started: valore booleano che tiene monitora se è iniziata la partita. La partita può iniziare 
            cliccando sul tasto 'start' o su una cella della griglia.
            -is_game_paused: tiene conto se il gioco è stato messo in pausa, cliccando sull'apposito bottone
            -outcome: rappresenta il risultato della partita, può essere 'L' in caso di sconfiffa (lose), w in caso
            di vittoria (win) e '' se la partita è in corso o non è ancora iniziata.
            -direction: il verso di direzione del serpente, indicato dai punti cardinali.
            -seconds: è un contatore che tiene conto dei secondi trascorsi dall'inizio della partita.
            -apple_coordinates: le coordinate della mela nella griglia.
            -snake: è un'istanza della classe Snake, che tiene traccia dei movimenti e dello stato del serpente
            durante la partita.
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

        #costruzione della schermata
        self.__build_window__()

        #inizializzo i thread per il rendering della griglia e del timer
        self.grid_thread = threading.Timer(TIME, self.__handle_game__)
        self.timer_thread = threading.Timer(1, self.__handle_game__)

    def __on_key_press__(self, key: str) -> None:
        '''
            Evento che rileva quale tasto di direzione è stato premuto e aggiorna lo stato della direzione, solo se
            si è premuto un tasto diverso da quello precedente, in modo da non aggiornare inutilmente 
            l'attributo direction.
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
            Evento del bottone start. 
            Gli attributi x e y vengono passati quando l'utente clicca sulla griglia per 
            posizionare il serpende dove vuole lui, se clicca invece il tasto 'start' allora
            x e y verranno generati successivamente
        '''
        if not self.is_game_started:
            if self.outcome: #cancello la scritta 'game over' o 'hai vinto'
                for r in range(ROWS):
                    for c in range(COLS):
                        self.cells[r][c].empty()
                self.outcome = ''
                return
            if self.username.getText() in ['Inserisci username', '', ' ']: #check dell'username
                self.error_message.config(foreground='red')
            else:
                if x and y:
                    self.__build_snake__(x, y)
                else:
                    self.__build_snake__()
                #posiziono la mela e reinizializzo gli stati della partita
                self.__place_apple__()
                self.error_message.config(foreground=BACKGROUND_COLOR)
                self.is_game_started = True
                self.is_game_paused = False
                #avvio i thread
                self.__handle_game__()
                self.__start_timer__()
                
                # Rimuovo il focus dall'input dell'username
                self.focus_set()

    def __on_pause_button_click__(self) -> None:
        '''
            Evento del tasto pausa
        '''
        if self.is_game_started: #check se la partita è iniziata
            self.is_game_paused = not self.is_game_paused
            self.__handle_game__()

    def __start_timer__(self) -> None:
        '''
            Questo metodo avvia il timer, gestito da un thread che si aggiorna a intervalli di 1s
        '''
        if self.is_game_started:
            self.timer_thread = threading.Timer(1.0, self.__start_timer__) # Re-inizializzazione del thread
            #il parametro 'daemon' và settato a True così quando si chiude la finestra del Main, anche il thread
            #interromperà il suo ciclo di vita
            self.timer_thread.daemon = True
            self.timer_thread.start()
            self.seconds += 1
            self.time_label['text'] = f'Tempo: {self.seconds}s'
        else:
            self.timer_thread.cancel() #fermo il timer
            self.seconds = 0

    def __handle_game__(self) -> None:
        '''
            Questo metodo gestisce il flusso di gioco.
            Se la partita è in corso gestisce il thread che renderizza la griglia periodicamente e la aggiorna 
            in seguito agli spostamenti del serpemnte e al posizionamento della mela.
            A partita conclusa viene salvato l'utente e viene aggiornata la classifica e viene mostrata sulla griglia
            la scritta 'game over' o 'hai vinto'.
        '''
        if self.is_game_started:  
            if self.is_game_paused:
                self.grid_thread.cancel() #metto in pausa il rendering
            else:
                self.grid_thread = threading.Timer(TIME, self.__handle_game__) #Re-inizializzazione del thread
                self.grid_thread.daemon = True
                self.grid_thread.start()
                self.occupied_cells_label['text'] = f'Celle occupate: {len(self.snake.body)}'
                self.remained_cells_label['text'] = f'Celle rimanenti: {ROWS*COLS - (len(self.snake.body) + 200)}'
                self.snake.move(self.direction, self)
        else:
            update_ranking(self.username.getText(), len(self.snake.body)) #aggiorno la classifica
            self.grid_thread.cancel()
            self.occupied_cells_label['text'] = ''
            self.remained_cells_label['text'] = ''
            self.time_label['text'] = ''
            self.username.setText('Inserisci username')
            self.__draw_grid__(self.outcome == 'W') #Scrivo 'game over' o 'hai vinto' sulla griglia

    def __draw_grid__(self, is_victory: bool) -> None:
        '''
            Questo è il metodo che scrive sulla griglia la scritta di sconfitta o vittoria.
            Prima la griglia viene pulita cancellando la mela e il serpente.
        '''
        (x,y) = self.apple_coordinates
        self.cells[x][y].empty() #cancello la mela
        for cell in self.snake.body: #cancello il serpente
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
            Metodo che posiziona randomicamente la mela sulla griglia
        '''
        if not self.outcome: #la mela viene posizionata solo durante la partita
            x,y = None, None
            while True:
                #si è scelto di usare il metodo 'choices' di random piuttosto che altri, perché questo metodo
                #può ritornare una coppia di valori uguali (x = y), e quindi poter posizonare la mela nella diagonale
                x,y = random.choices(range(20), k=2)
                if not self.cells[x][y].is_snake_body: #check se la mela non viene posizionata nel corpo del serpente
                    break
            self.cells[x][y].apple()
            self.apple_coordinates = (x,y)

    def __build_snake__(self, x: int = None, y: int = None):
        '''
            Metodo che posiziona il serpente sulla griglia.
            x e y sono le coordinate del bottone, se l'utente ha deciso di posizionare il serpente dove vuole lui.
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
            Questo metodo crea la griglia
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
            In questo metodo vengono aggiunti tutti i componenti della finestra di gioco.
            'panel1' contiene l'input per lo username e i tasti start e pausa.
            'panel2' contiene i 4 tasti direzionali.
            'panel3' contiene i 3 label della partita e il tasto per mostrare la classifica.
        '''
        self.bind('<Key>', self.__on_key_press_event__)
        self.configure(borderwidth=0, highlightthickness=0)
        self.__build_grid__()
        self.panel1 = self.addPanel(row=0, column=0, columnspan=20, background=BACKGROUND_COLOR)
        self.panel2 = self.addPanel(row=1, column=0, columnspan=20, background=BACKGROUND_COLOR)
        self.panel3 = self.addPanel(row=23, column=0, columnspan=20, background=BACKGROUND_COLOR)

        self.username = self.panel1.addTextField('Inserisci username', 0, 0, sticky='W')
        self.start = self.panel1.addButton('Start', 0, 1, command=self.__on_start_button_click__)
        self.pause = self.panel1.addButton('Pausa', 0, 2, command=self.__on_pause_button_click__)

        for widget in self.panel1.winfo_children():
            if isinstance(widget, Button):
                widget.config(borderwidth=0, highlightthickness=1, highlightbackground='#000')

        self.panel1.addLabel('', 0, 3, sticky='W', background=BACKGROUND_COLOR)
        
        self.error_message = self.panel1.addLabel('', 0, 20, background=BACKGROUND_COLOR, foreground=BACKGROUND_COLOR)
        self.error_message['text'] = 'Devi inserire il tuo username per giocare'

        self.panel2.addButton('↑', 0, 10, command = lambda: self.__on_key_press__('N'))
        for i in range(0, 8):
            self.panel2.addLabel('', 1, i, sticky='E', background=BACKGROUND_COLOR)
        self.panel2.addButton('←', 1, 9, command = lambda: self.__on_key_press__('W'))
        self.panel2.addButton('→', 1, 11, command = lambda: self.__on_key_press__('E'))
        for i in reversed(range(11, 20)):
            self.panel2.addLabel('', 1, i, sticky='W', background=BACKGROUND_COLOR)
        self.panel2.addButton('↓', 2, 10, command = lambda: self.__on_key_press__('S'))

        self.time_label = self.panel3.addLabel('', 0, 0, background=BACKGROUND_COLOR, foreground='white')
        self.occupied_cells_label = self.panel3.addLabel('', 0, 1, background=BACKGROUND_COLOR, foreground='white')
        self.remained_cells_label = self.panel3.addLabel('', 0, 2, background=BACKGROUND_COLOR, foreground='white')
        self.panel3.addLabel('', 0, 4, sticky='WE', background=BACKGROUND_COLOR, columnspan=20)
        self.panel3.addButton('Mostra classifica', 0, 20, command=self.__on_ranking_button_click__)

        def configure_buttons(panel, background_color):
            for widget in panel.winfo_children():
                if isinstance(widget, Button):
                    widget.config(borderwidth=0, highlightthickness=1, highlightbackground='#000', fg='#000', background=background_color)

        configure_buttons(self.panel1, '#fff')
        configure_buttons(self.panel2, '#FFC300')
        configure_buttons(self.panel3, '#fff')

    def __on_key_press_event__(self, event) -> None:
        '''
        Evento chiamato quando un tasto della tastiera viene premuto.
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
                case _:
                    self.__on_key_press__(key.upper())

    def __on_ranking_button_click__(self) -> None:
        '''
            Quest'evento mostra la finestra contenente la classifica
        '''
        if not self.is_game_started: #la classifica non si può aprire con la partita in corso
            result: str = ''
            data = show_ranking()
            for (score, username) in data:
                result += f'{username}: {score}\n'
            result = result.rstrip('\n')
            self.messageBox('CLASSIFICA', result)

def main():
    Main().mainloop()

if __name__ == '__main__':
    main()
