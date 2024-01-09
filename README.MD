Utilizzando il linguaggio di programmazione Python, realizzare un'applicazione con le seguenti caratteristiche: 
- Il piano di gioco contiene una griglia costituita da 20×20 celle quadrate bianche, ciascuna di dimensione 15×15. 
- Il protagonista del gioco è un serpente che inizialmente è rappresentato da dieci quadrati consecutivi, ciascuno adiacente solo al precedente e al successivo. 
- I quadrati sono tutti azzurri esclusi la testa di colore verde e la coda di colore giallo. Il gioco procede per step.


1. Non appena si dà inizio ad una nuova partita nella griglia di gioco viene posizionata casualmente una cella rossa; 
al primo step il serpente avanza di una posizione secondo una direzione scelta a caso tra alto, basso, destra, sinistra.
Con tale terminologia (avanza di una posizione) si intende che ogni cella, a parte la testa, prende la posizione della cella che la precede. 
Nei successivi step il serpente avanza di una posizione secondo la direzione dettata dal movimento precedente 
a meno che la direzione non sia determinata dal giocatore che decide un cambiamento di direzione.


2. Se con la sua testa il serpente "mangia" una cella rossa, esso cresce di una cella. 
Non appena una cella viene mangiata, un'altra cella rossa viene posizionata in modo random in una cella non occupata del piano di gioco. 
Il giocatore deve cercare di direzionare i movimenti del serpente affinché la testa non tocchi mai nessuna delle altre celle che lo compongono. 
In tal caso il giocatore perde. Il giocatore vince se riesce a riempire col serpente almeno il 50% del piano di gioco.


3. Si definiscano opportune classi per la gestione del serpente e della griglia. 
Si identifichino pertanto opportuni attributi di istanza e metodi per tali classi. 
In particolare, la classe che rappresenta il serpente deve contenere un metodo avanza() che gestisce lo spostamento del serpente.


4. Definire un'opportuna interfaccia grafica per la gestione dell'applicazione utilizzando il modulo breezypythongui che mostri la griglia di gioco e il serpente. 
Al click di un bottone GIOCO il gioco comincia. 
Gli step del gioco sono scanditi da un timer in cui ogni scansione ha la durata di un decimo di secondo. 
I cambiamenti di direzione sono determinati dal click su 4 rispettivi bottoni NORD, EST, SUD, OVEST. 
Tre label tengono conto rispettivamente del tempo, delle celle mangiate e di quante celle mancano alla vittoria. 
Al click di un bottone STOP il gioco si interrompe.


5. Nella configurazione iniziale il serpente deve essere posizionato casualmente con tutte le celle nella stessa riga. 
In alternativa, il giocatore può posizionarlo cliccando nella cella nella quale viene posizionata la testa. 
Il resto del serpente sarà posizionato più a destra sulla stessa riga.


6. Si consideri che il piano di gioco è considerato orizzontalmente circolare, ovvero la prima colonna e l'ultima colonna sono considerate consecutive.


7. Alla fine del gioco, viene memorizzato in un file il nome del giocatore e il suo punteggio. Al click di un bottone CLASSIFICA, viene visualizzata la classifica dei primi 5 giocatori