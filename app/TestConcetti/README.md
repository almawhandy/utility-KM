INPUT : Il seguente script accetta un solo parametro. 

- path excel : Path che indica il file excel (.xls) che si vuole elaborare.

Il file excel dovrà presentare 4 colonne con valore : 

- CONCETTO : nome identificativo del concetto che si intende testare
- FRASE : porzione di testo in cui si vuole ricercare o meno il concetto
- ONTOLOGIA : Può essere un singolo valore oppure più valori separati da virgola
- RISULTATO ATTESO : Può assumere i valori OK/KO. OK se il concetto deve essere trovato nella frase, KO altrimenti. 

OUTPUT : L'output di questo script consiste nell'aggiornare il file excel passato in input. Nello specifico, verranno aggiunte le seguenti colonne:

- CONCETTO RILEVATO: nome identificativo del concetto che si sta analizzando
- RISULTATO : Può assumere i valori OK/KO a seconda dell'avvenuta rilevazione o meno del concetto nella frase, entrambi parametri forniti nel file excel di input

COMANDO DA ESEGUIRE : python testConcetti.py <path excel> 


ESEMPIO COMANDO : python testConcetti.py testConcetti.xls