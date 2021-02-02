## utility-KM

Utility KM comprende 3 servizi di supporto : 

* Estrazione label e query
* Test Entità
* Test Concetti

# Estrazione label e query

# Test Entità

INPUT : Il seguente servizio può essere richiamato al path /testEntita ed accetta due parametri da inserire nel body con le chiavi base64 ed endpoint. Il valore della chiave base64 deve corrispondere al base64 del file excel da analizzare mentre il valore endpoint deve corrispondere all'endpoint dove sarà invocato il servizio di analyzedDocument. 


Il file excel dovrà presentare 4 colonne con valore : 

- ENTITA : entità che si intende testare
- FRASE : porzione di testo in cui si vuole ricercare o meno l'entità
- TIPO : Indica la tipologia dell'entità (Person, Location, Organization)
- RISULTATO ATTESO : Può assumere i valori OK/KO. OK se il concetto deve essere trovato nella frase, KO altrimenti. 

OUTPUT : L'output di questo servizio sarà un base64 di un file excel. Nello specifico, al file excel passato in input, verranno aggiunte le seguenti colonne:

- ENTITA RILEVATA: Indica l'entità estratta dalla frase. Può essere vuota, contenere un singolo valore o contenere più valori separati da virgola (ordinati secondo una metrica di similarità). Esempio di funzionamento : 
	- se il risultato atteso è un OK e si ottiene un OK allora viene mostrata l'entità rilevata
	- se il risultato atteso è un OK e si ottiene un KO allora viene mostrata la lista delle entità rilevate ordinata per score
	- se il risultato atteso è un KO e si ottiene un OK allora viene mostrata l'entità rilevata
	- se il risultato atteso è un KO e si ottiene un KO non sarà riportata alcuna entità.
- RISULTATO : Può assumere i valori OK/KO a seconda dell'avvenuta rilevazione o meno dell'entità nella frase, entrambi parametri forniti nel file excel di input

# Test Concetti

INPUT : Il servizio può essere richiamato al path /testConcetti ed accetta due parametri da inserire nel body con le chiavi base64 ed endpoint. Il valore della chiave base64 deve corrispondere al base64 del file excel da analizzare mentre il valore endpoint deve corrispondere all'endpoint dove sarà invocato il servizio di analyzedDocument.

Il file excel dovrà presentare 4 colonne con valore :

- CONCETTO : nome identificativo del concetto che si intende testare
- FRASE : porzione di testo in cui si vuole ricercare o meno il concetto
- ONTOLOGIA : Può essere un singolo valore oppure più valori separati da virgola
- RISULTATO ATTESO : Può assumere i valori OK/KO. OK se il concetto deve essere trovato nella frase, KO altrimenti.

OUTPUT : L'output di questo servizio sarà un base64 di un file excel. Nello specifico, al file excel passato in input, verranno aggiunte le seguenti colonne:

- CONCETTO RILEVATO: nome identificativo del concetto che si sta analizzando
- RISULTATO : Può assumere i valori OK/KO a seconda dell'avvenuta rilevazione o meno del concetto nella frase, entrambi parametri forniti nel file excel di input
