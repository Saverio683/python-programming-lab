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
        La classe Cell serve a gestire la griglia di gioco.
        ATTRIBUTI:
            -r,c: stanno per row e column, sono le coordinate della cella nella griglia.
            -button: è il bottone che viene mostrato a video, è un'istanza della classe Button, la stessa che ritorna 
            il metodo addButton di EasyFrame.
            -is_snake_body: valore booleano che stabilisce se la cella compone il corpo del serpente.
            -is_apple: booleano per stabilire se la cella è la mela.
            -bg: il colore di background, bianco di default
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
        Classe per la gestione del serpente.
        ATTRIBUTI:
            -body: lista delle celle che lo compongono.
            La prima cella della lista è la coda, l'ultima sarà la testa.
    '''
    def __init__(self, body: List[Cell]):
        self.body = body
        self.body[0].tail()
        for cell in self.body[1:-1]:
            cell.body()
        self.body[-1].head()

    def move(self, next_direction: Literal['N', 'S', 'E', 'W'], master: EasyFrame) -> None:
        '''
            Questo metodo gestisce l'avanzamento del serpente.
            Per far avanzare il serpente si rimuove la coda e si aggiunge una nuova testa davanti quella precedente
        '''
        def get_next_head_coordinates(prev_head: Cell, next_direction: Literal['N', 'S', 'E', 'W']) -> Tuple[int, int]:
            '''
                Questa funzione serve a calcolare la posizione della nuova testa in base alla direzione
            '''
            r, c = prev_head.r, prev_head.c
            match next_direction:
                case 'N':
                    r -= 1
                    if r < 0: #il serpente tocca il bordo superiore della griglia
                        master.outcome = 'L'
                        master.is_game_started = False
                        r = 0
                case 'S':
                    r += 1
                    if r > 19: #tocca il bordo inferiore
                        master.outcome = 'L'
                        master.is_game_started = False
                        r = 19
                case 'E':
                    c = (c + 1) % 20
                case 'W':
                    c = (c - 1 + 20) % 20
            return r, c

        grid = master.cells
        #rimuovo la coda
        prev_tail = self.body[0]
        grid[prev_tail.r][prev_tail.c].empty()
        del self.body[0]

        #nuova coda
        self.body[0].tail()

        #la vecchia testa diventa body
        prev_head = self.body[-1]
        prev_head.body()

        #nuova testa
        r,c = get_next_head_coordinates(prev_head, next_direction)
        new_head = grid[r][c]
        self.body.append(new_head)

        if new_head.is_snake_body: #se il serpente tocca sé stesso
            master.outcome = 'L'
            master.is_game_started = False
            master.cells[r][c].head()
            return

        def eat_apple(r, c, curr_head) -> None:
            '''
                Con questa funzione verifico se è stata mangiata la mela.
                La testa attuale diventa body e la cella successiva diventa la nuova testa
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
                if len(self.body) >= 200: #verifico se il giocatore ha vinto
                    master.outcome = 'W'
                    master.is_game_started = False
                    return

        eat_apple(r, c, new_head)

        # Aggiorno la griglia
        grid[new_head.r][new_head.c] = new_head
        for cell in self.body:
            master.cells[cell.r][cell.c] = cell

def update_ranking(username, score):
    '''
        Questa funzione aggiunge i dati dell'ultima partita nel file di testo
    '''
    with open('ranking.txt', 'r+', encoding='utf-8') as file:
        record: str = f'{score}-{username}'
        #leggo tutte le righe del file
        lines: List[str] = file.readlines()

        #se il file è vuoto, inserisco il nuovo record direttamente
        if not lines:
            file.write(record)
            return

        #rimuovo il carattere di fine riga dalla riga finale del file
        last_line = lines[-1].rstrip('\n')

        lines[-1] = last_line + f'\n{record}'

        file.seek(0)
        file.writelines(lines)

def show_ranking() -> List[Tuple[str, str]]:
    '''
        Questa funzione ricalcola la classifica dei top 5 giocatori
    '''
    data: List[Tuple[int, str]] = []

    with open('ranking.txt', 'r', encoding='utf-8') as file:
        for line in file:
            punteggio, _, username = line.strip().partition('-')
            data.append((int(punteggio), username))

    result = sorted(data, key=lambda x: x[0], reverse=True)

    return result[:5]
