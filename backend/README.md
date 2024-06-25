# InquireMate Backend

## Descrizione del progetto
Software che si pone principalmente i seguanti scopi: 
- ricercare materiale da internet; 
- effettuare lo scraping; 
- fare embedding;
- restituire pezzi di testo, a seconda degli embedding fatti.

Il software al momento utilizza [*OpenAI*](https://openai.com/) per generare le risposte alle domande. Dunque, per poter utilizzare l'applicazione, è necessario disporre di una chiave API di OpenAI. Di seguito viene spiegato come utilizzarla.

Utilizza Chromadb, per salvare gli embedding.
## Installazione

### Prerequisiti:
- argparse==1.4.0
- chromadb==0.4.24
- python-dotenv==1.0.1
- fastapi==0.110.2
- googlesearch-python==1.2.3
- html2text==2024.2.26
- langchain==0.1.16
- lxml==5.2.1
- numpy==1.26.4
- openai==1.23.2
- pdfreader==0.1.12
- pypdf==4.0.0
- python==3.10.12
- sentence-transformers==2.7.0
- torch==2.2.2
- tqdm==4.66.2
- uvicorn==0.29.0

### Instruzione

#### Creazione dell'ambiente virtuale
Su **windows** digitare:
``` bash
py -m venv .venv
```
Su **iOS/Linux** digitare:
``` bash 
python3 -m venv .venv
```
#### Attivazione dell'ambiente virtuale
Su **windows** digitare:
``` bash
.venv\Scripts\activate
```
Su **iOS/Linux** digitare:
``` bash 
source .venv/bin/activate
```
#### Installazione dipendenze
Sul terminale digitare:
``` bash 
pip install -r requirements.txt
``` 
Nella cartella principale del progetto, creare un file `.env` ed all'interno scrivere:
```OPENAI_API_KEY=la_tua_chiave```
È necessario essere in possesso di una chiave OpenAI, la quale andrà sostituita a *la_tua_chiave*.

## Guida rapida
### Generare embedding e salvarli dentro al database
- far partire il file da terminale scrivendo: 
**Con Windows**
``` bash
.venv\Scripts\activate
py ChromaEmbeddings_embedding.py
```

**Con Linux/iOS**
``` bash
source .venv/bin/activate
python3 ChromaEmbeddings_embedding.py
```
Sono impostati dei parametri di base. Se si desidera personalizzarli è possibile scriverli da teminale, aggiungendo al codice precedente i seguenti comandi opzionali:
- `-mo nome_del_modello*`: utilizzare il modello preferito. **ATTENZIONE!** Se si desidera utilizzare un modello openai, scrivere `openai`;
- `-c *nome_della_collezione*`: sostituire il nome che vogliamo attribuie alla collezione;
- `-me *metadati*`: scrivere al posto di *metadati* una scrittura tipo: '{"user":"red", "theme":["music", "fantasy"]}'. Fare molto attenzione a dove vanno segnatti i simboli: ' e ";
- `-d *path_documenti.pdf*`: sostituire con il percorso ed il documento desiderato. Inserire anche l'estensione del documento, che sia pdf o txt. Non accetta altri formati;
- `--delete`: aggiugere True se si desidera eliminare la collezione in caso ne esista una con lo stesso nome.
  
**ATTENZIONE!** Segui l'ordine!

Il programma creerà un'oggetto ChromaEmbeddings e farà partire il metodo new_collection per creare gli embedding che verranno salvati su Chromadb.
- attendere la risposta dal terminale: ```Collection created successfully!```.
Verranno create tre cartelle:
- "chroma": all'interno c'è il database;
- "json": all'interno si trovera un file `collections.json` con tutte le collezioni che verranno generate [nella versione finale non sarà presente questa cartella];
- "log": presente i log.

### Interrogazione
- far partire il file da terminale scrivendo: 
**Con Windows**
``` bash
.venv\Scripts\activate
py ChromaEmbeddings_query.py
```

**Con Linux/iOS**
``` bash
source .venv/bin/activate
python3 ChromaEmbeddings_query.py
```
Sono impostati dei parametri di base. Se si desidera personalizzarli è possibile scriverli da teminale, aggiungendo al codice precedente i seguenti comandi opzionali:
- `-mo *nome_del_modello*`: utilizzare il modello preferito. **ATTENZIONE!** Se si desidera utilizzare un modello openai, scrivere `openai`. Assicurarsi che la collezione indicata esista;
- `-c *nome_della_collezione*`: sostituire il nome che vogliamo attribuie alla collezione;
- `-me metadati`: scrivere al posto di *metadati* una scrittura tipo: '{"user":"red", "theme":["music", "fantasy"]}'. Fare molto attenzione a dove vanno segnatti i simboli: ' e ";
- `-k`: numero degli ebedding che deve restituire.

**ATTENZIONE!** Segui l'ordine!

- sul terminale comparirà la scritta: ```Ask me!```;
- fare una domanda al terminale.

Il programma creerà un'oggetto ChromaEmbeddings ed inivierà la query al metodo query, il quale trasformerà in embedding l'interrogazione e la confronterà con gl embedding della collezione fornita.
Verrà restituito il file `json/results.json` dove saranno elencati i risultati.

### Web Scraping

#### Html2TextTransformer

Se si desidera estrapolare le informazioni da Internet, seguire i seguenti comandi:
**Con Windows**
``` bash
.venv\Scripts\activate
py ScrapingHtml2Text_prova.py
```

**Con Linux/iOS**
``` bash
source .venv/bin/activate
python3 ScrapingHtml2Text_prova.py
```
Aggiungere:
- `-n` seguito da un numero per specificare quanti url si desidera considerare;
- `--query` seguito dalla query desiderata.

In caso non si abbia specificato la query, attendere la scritta `Ask me!` e digitare la domanda/argomento che si desidera ricevere informazioni da internet.

A fine della procedura, verrà creato un file `json/ris_scraping.json` dove sarà presente il risultato dello scraping. Nel caso esista già, verrà sostituito.

#### BeautifulSoup

Alternativa alla precedente, pensata per l'estrapolazione d'informazione entrando nei collegamenti che sono presenti nella pagina.

**Con Windows**
``` bash
.venv\Scripts\activate
py ScrapingBeautifulSoup_prova.py
```

**Con Linux/iOS**
``` bash
source .venv/bin/activate
python3 ScrapingBeautifulSoup_prova.py
```

Aggiungere:
- -d *inserire_profondità*: partendo dal primo sito web, quanto profondo deve andare;
- --http *inserire_sito_web_iniziale*: sito web di partenza;
- --summary True: se si desidera generare un riassunto per ogni pagina scrapata con le chiamate Api a chatGPT;
- -lc True: per attivare LangChain, invece di usare direttamente BeautifulSoup.

### Web Service

Se si preferisse utilizzare le chiamate API per un'app web, è possibile utilizzare il file `web_service.py`, nel seguente modo:

Sul terminale, digitare:
```bash
uvicorn web_service:app
```
Questo farà avviare il backend. 

Per vedere il suo funzionamento, consiglio di utilizzare un programma come [Postman](https://www.postman.com/).
Su **Postman** o simili, selezionare 'POST' con url `http://127.0.0.1:8000/scraping`. Dentro Body selezionare raw e poi JSON.

Come corpo della chiamate come quella seguente: 
```
{
    "query": "Che cosa sono i buchi neri?",
    "n": 5
}
```
"query" è necessaria, a differenza di "n" (numero di pagine da scrapare), il quale ha di default 5.

A fine della procedura, verrà creato un file `json/ris_scraping.json` dove sarà presente il risultato dello scraping. Nel caso esista già, verrà sostituito.

**Altre chiamate api POST:**
`http://127.0.0.1:8000/scraping_bs`
Chiama la classe ScrapingBeautifulSoup, con contenuto della chiamata:
```
{
    "http": "https://www.3logic.it/",
    "d": 1,
    "summary": true,
    "lc": true
}
```
- "http": url da dove comincia lo scraping;
- "d": la profondità, consiglio di dare un numero relativamente basso [default = 0];
- "summary": riassunto della pagine tramite l'Api a ChatGPT [default = false];
- "lc": attivare o disattivare LangChain [default = false].

`http://127.0.0.1:8000/embedding`
Chiama la classe ScrapingHtml2Text, con contenuto della chiamata:
```
{
    "model": "BAAI/bge-small-en-v1.5",
    "collection": "collection",
    "metadata": {"user":"admin", "theme":["arte", "cucina"]},
    "path": "documents/doc.pdf",
    "delete": true
}
```
- "model": modello per far gli embedding [default = "BAAI/bge-small-en-v1.5"];
- "collection": nome della collezione [default = "collection"];
- "metadata": metadati/tag a quel libro, utile per quando si desidera andar ad interrogare il db [default = "{"user":"admin"}"];
- "path": percorso del file;
- "delete": nel caso si voglia eliminare la collezione nel caso esista già con lo stesso nome [default = False].

`http://127.0.0.1:8000/inquireMate/web_search`
Chiamate che effettua la ricerca e restituisce i primi n url tramite il metodo web_search della classe ScrapingBeautifulSoup, con contenuto della chiamata:
```
{
    "query": "Che cosa sono i buchi neri?",
    "n": 5
}
```
- "query": digitare una domanda da ricercare,
- "n": numero di url da restituire.

`http://127.0.0.1:8000/inquireMate/scraping_embedding`
Chimata che effettua lo scraping e gli embedding di un url. Restituisce un file con lo scraping. È pensata per esser effettuata dopo `/inquireMate/web_search`.
```
{
    "http": "https://www.3logic.it/"
    "d": 1
    "summary": True
    "lc": True
}
```
- "http": url della pagina dove effettuare lo scraping e gli embedding;
- "d": profondità della pagina web per lo scraping;
- "summary": se utilizzare l'api di OpenAi per effettuare il riassunto per ogni pagina web;
- "lc": attivare o meno langChain.

## Struttura del progetto
Il progetto presenta:
- **ChromaEmbeddings.py**: classe che consente di fare gli embedding dei documenti pdf o txt e di salvarli in chromadb;
- **ScrapingHtml2Text.py**: classe che estrapola le informazioni dalle n pagine web e li converte in un file json;
- **ScrapingBeautifulSoup.py**: classe per l'estrapolazione di informazioni da un sito web con profondità;
- **documents**: cartella dove si trovano i documenti a cui il programma fa riferimento per l'estrazione dell'informazione;
- **ChromaEmbeddings_embedding.py**: programma che richiama la classe per la creazione degli embedding;
- **ChromaEmbeddings_query.py**: programma che richiama la classe per interrogare il db, così da estrarre alcune frasi da chromadb riguardanti la query posta;
- **ScrapingHtml2Text_prova.py**: programma che fa il web sraping delle prime n pagine, in base alla domanda che gli viene fornita; 
- **ScrapingBeautifulSoup_prova.py**: programma che fa il web sraping di n profondità, in base al link che gli viene fornito; 
- **web_service.py**: programma per la gestione del backend per un'app web dello scraping;
- **utility.py**: variabili di default e funzioni richiamate esternamente;
- **log**: cartella che verrà creata dove sarenno presenti i vari log;
- **json**: cartella che verrà generata dove si troveranno i file json creati. Quindi <u>non</u> presente inizialmente.

## Open Issues
Al momento non è previsto l'utilizzo di più utenti. In quel caso, andrebbero utilizzati i Thread.