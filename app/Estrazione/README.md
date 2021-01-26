INPUT : Il seguente script accetta massimo 3 parametri. L'unico parametro non obbligatorio è la lista di concetti, qualora fosse mancante o vuota verranno analizzati tutti i concetti presenti nell'ontologia. I parametri sono : 

- path lista concetti : Path relativo ad un file .txt che può essere vuoto o può contenere più concetti separati da virgola
- path ontologia : Path relativo all'ontologia che si intende analizzare
- path excel : Path dove si andrà a salvare il file excel .xlsx di output

OUTPUT : In output verrà creato un file excel nel path specificato in input che avrà le seguenti colonne : 

- CONCETTO : nome identificativo del concetto
- LISTA DI LABEL : Lista di label associate al concetto
- QUERY : Query relativa al concetto 

COMANDO DA ESEGUIRE : python extract_info.py <path lista concetti> <path ontologia> <path excel>


ESEMPIO COMANDO : python extract_info.py listaConcetti.txt Gdf.owl result.xlsx