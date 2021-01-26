INPUT : Il seguente script accetta un solo parametro. 

- path excel : Path che indica il file excel (.xls) che si vuole elaborare.

Il file excel dovrà presentare 4 colonne con valore : 

- ENTITA : entità che si intende testare
- FRASE : porzione di testo in cui si vuole ricercare o meno l'entità
- TIPO : Indica la tipologia dell'entità (Person, Location, Organization)
- RISULTATO ATTESO : Può assumere i valori OK/KO. OK se il concetto deve essere trovato nella frase, KO altrimenti. 

OUTPUT : L'output di questo script consiste nell'aggiornare il file excel passato in input. Nello specifico, verranno aggiunte le seguenti colonne:

- ENTITA RILEVATA: Indica l'entità estratta dalla frase. Può essere vuota, contenere un singolo valore o contenere più valori separati da virgola (ordinati secondo una metrica di similarità). Esempio di funzionamento : 
	- se il risultato atteso è un OK e si ottiene un OK allora viene mostrata l'entità rilevata
	- se il risultato atteso è un OK e si ottiene un KO allora viene mostrata la lista delle entità rilevate ordinata per score
	- se il risultato atteso è un KO e si ottiene un OK allora viene mostrata l'entità rilevata
	- se il risultato atteso è un KO e si ottiene un KO non sarà riportata alcuna entità.
- RISULTATO : Può assumere i valori OK/KO a seconda dell'avvenuta rilevazione o meno dell'entità nella frase, entrambi parametri forniti nel file excel di input




COMANDO DA ESEGUIRE : python testEntita.py <path excel> 


ESEMPIO COMANDO : python testEntita.py testEntita.xls