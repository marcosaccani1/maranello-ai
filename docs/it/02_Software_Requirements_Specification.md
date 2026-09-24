# Software Requirements Specification

> **Progetto:** Maranello AI  
> **Versione:** 2.0  
> **Tipo documento:** Software Requirements Specification (SRS)  
> **Stato:** Final  
> **Autore:** Marco Saccani  
> **Ultimo aggiornamento:** Settembre 2026

---

# Indice

1. Introduzione
   - 1.1 Scopo
   - 1.2 Obiettivi
   - 1.3 Natura dei requisiti
   - 1.4 Definizioni
   - 1.5 Riferimenti

2. Descrizione generale del sistema
   - 2.1 Visione del sistema
   - 2.2 Attori e componenti coinvolti
   - 2.3 Contesto operativo
   - 2.4 Assunzioni
   - 2.5 Vincoli

3. Requisiti funzionali
   - 3.1 Frontend
   - 3.2 Backend
   - 3.3 AI Orchestration
   - 3.4 Retrieval-Augmented Generation (RAG)
   - 3.5 Python Data Agent
   - 3.6 Gestione degli errori
   - 3.7 Funzionalità tecniche complementari

4. Requisiti non funzionali

5. Business Rules

6. Casi d'uso principali

7. Criteri di accettazione

8. Conclusioni

---

# 1. Introduzione

## 1.1 Scopo

Il presente documento descrive i requisiti software della versione finale di **Maranello AI**, un assistente AI enterprise dimostrativo progettato per supportare il reparto **Quality & Manufacturing Operations** di un produttore automotive fittizio.

La Software Requirements Specification definisce in maniera strutturata e verificabile:

- funzionalità richieste al sistema;
- comportamento dei principali componenti;
- requisiti di orchestrazione AI;
- requisiti relativi al Retrieval-Augmented Generation;
- requisiti del Python Data Agent;
- requisiti relativi all'interfaccia conversazionale;
- requisiti di integrazione;
- requisiti non funzionali;
- business rules;
- principali casi d'uso;
- criteri di accettazione.

Il documento rappresenta la specifica **as-built** della soluzione e descrive quindi i requisiti effettivamente applicabili all'implementazione finale.

I requisiti vengono mantenuti separati dai dettagli implementativi più approfonditi, documentati nel System Architecture Document, nel Data Model e nella API Specification.

---

## 1.2 Obiettivi

Maranello AI deve fornire un'unica esperienza conversazionale attraverso la quale l'utente possa accedere a conoscenza documentale e analisi quantitative senza selezionare manualmente il componente da utilizzare.

Gli obiettivi principali sono:

- fornire un'interfaccia conversazionale web semplice da utilizzare;
- comprendere richieste formulate in linguaggio naturale;
- supportare richieste in italiano e inglese;
- mantenere il contesto della conversazione durante la sessione;
- permettere al Large Language Model di decidere autonomamente se utilizzare strumenti specializzati;
- interrogare una Knowledge Base aziendale fittizia mediante RAG;
- analizzare dati manifatturieri strutturati mediante un Python Data Agent;
- generare KPI, confronti, trend e grafici;
- combinare informazioni documentali e risultati quantitativi;
- restituire risposte coerenti con le fonti disponibili;
- evitare la generazione di policy aziendali non supportate dalla Knowledge Base;
- evitare la generazione di risultati numerici non supportati dal Manufacturing Dataset;
- gestire in modo controllato gli errori delle principali dipendenze applicative.

Il comportamento generale può essere rappresentato come:

    User Question
          ↓
    Conversational Interface
          ↓
    Node.js Backend
          ↓
    LLM Orchestration
          ↓
    Tool Required?
       /       \
      No       Yes
      │         │
      │    Function Calling
      │       /       \
      │      /         \
      │     ▼           ▼
      │    RAG      Data Agent
      │      \         /
      │       \       /
      │        ▼     ▼
      │    Tool Results
      │         │
      └─────────┤
                ▼
        Response Synthesis
                ↓
              User

Il modello può utilizzare nessun tool, un singolo tool o più tool in funzione della richiesta.

---

## 1.3 Natura dei requisiti

La presente versione dell'SRS è stata riallineata all'implementazione finale del progetto.

I requisiti descrivono quindi capacità realmente appartenenti allo scope corrente e non funzionalità enterprise puramente ipotetiche.

Ogni requisito funzionale utilizza un identificativo univoco:

    RF-XXX

I requisiti non funzionali utilizzano:

    RNF-XXX

Le business rules utilizzano:

    BR-XXX

I criteri di accettazione utilizzano:

    AC-XXX

Le priorità utilizzate sono:

| Priorità | Significato |
|----------|-------------|
| Must Have | Requisito necessario per il corretto completamento dello scope corrente. |
| Should Have | Requisito importante ma non determinante per il funzionamento fondamentale del sistema. |

I requisiti vengono formulati utilizzando il termine **deve** anche quando la funzionalità risulta già implementata.

Questa scelta è intenzionale: una Software Requirements Specification descrive il comportamento richiesto al sistema, mentre lo stato di implementazione e le relative evidenze vengono verificati attraverso il Test Plan.

Non devono quindi essere interpretate come indicazioni di funzionalità future espressioni quali:

    il sistema deve

quando utilizzate all'interno della definizione formale di un requisito.

---

## 1.4 Definizioni

| Termine | Descrizione |
|---------|-------------|
| LLM | Large Language Model utilizzato per interpretazione, orchestrazione e sintesi della risposta. |
| AI Orchestration | Processo attraverso il quale l'LLM decide se e quali strumenti utilizzare per rispondere alla richiesta. |
| Function Calling | Meccanismo con cui il modello richiede al Backend l'esecuzione di uno strumento definito dall'applicazione. |
| Tool | Funzione applicativa resa disponibile al modello attraverso il meccanismo di function calling. |
| RAG | Retrieval-Augmented Generation, utilizzato per recuperare conoscenza documentale prima della generazione della risposta. |
| ChromaDB | Vector database locale utilizzato per la ricerca semantica nella Knowledge Base. |
| Embedding | Rappresentazione vettoriale utilizzata per confrontare semanticamente query e contenuti documentali. |
| Knowledge Base | Collezione di documenti aziendali fittizi relativi a Quality & Manufacturing Operations. |
| Data Agent | Microservizio Python responsabile dell'analisi deterministica del Manufacturing Dataset. |
| Manufacturing Dataset | Dataset CSV sintetico contenente informazioni relative ai batch produttivi. |
| Hybrid | Comportamento nel quale la risposta richiede sia evidenza quantitativa sia conoscenza documentale. |
| Conversation Manager | Componente Backend responsabile della gestione dello stato della conversazione. |
| Session ID | Identificativo della sessione conversazionale gestita dal Backend. |
| Chart Proxy | Endpoint Backend utilizzato per esporre al Frontend i grafici generati dal Data Agent. |
| As-Built | Documentazione riallineata al comportamento effettivamente implementato nella versione finale del software. |

---

## 1.5 Riferimenti

Il presente documento deve essere interpretato insieme agli altri documenti tecnici del progetto.

| Documento | Descrizione |
|-----------|-------------|
| `01_Project_Vision_and_Scope.md` | Definisce visione, business scenario e scope finale del progetto. |
| `03_System_Architecture.md` | Descrive l'architettura as-built e le responsabilità dei componenti. |
| `04_Data_Model.md` | Descrive Manufacturing Dataset, Knowledge Base e strutture dati principali. |
| `05_API_Specification.md` | Definisce le API e i contratti applicativi implementati. |
| `06_Test_Plan.md` | Descrive strategia di verifica, test eseguiti, risultati e criteri di accettazione. |

La relazione tra i documenti può essere sintetizzata come:

    Project Vision and Scope
             ↓
    Software Requirements Specification
             ↓
    System Architecture
             ↓
    Data Model + API Specification
             ↓
    Test Plan
             ↓
    Verification and Acceptance

---

# 2. Descrizione generale del sistema

## 2.1 Visione del sistema

Maranello AI è una piattaforma AI enterprise dimostrativa progettata per supportare il reparto **Quality & Manufacturing Operations**.

L'applicazione fornisce un'unica interfaccia conversazionale attraverso la quale l'utente può:

- consultare policy e procedure aziendali;
- analizzare dati produttivi;
- ottenere KPI;
- confrontare dimensioni produttive;
- analizzare trend temporali;
- generare grafici;
- combinare risultati numerici e conoscenza procedurale;
- continuare una conversazione mantenendo il contesto.

L'utente non deve conoscere l'architettura interna del sistema e non deve selezionare manualmente il servizio da utilizzare.

Il Large Language Model determina autonomamente se la richiesta possa essere gestita direttamente oppure richieda uno o più strumenti.

I tool principali disponibili sono:

    search_knowledge_base

e:

    analyze_manufacturing_data

Il primo permette di recuperare informazioni dalla Knowledge Base.

Il secondo permette di delegare l'elaborazione quantitativa al Python Data Agent.

Il comportamento complessivo supporta quindi:

    Direct Response
    RAG
    Data Analysis
    Hybrid

La selezione non viene effettuata mediante un classificatore applicativo separato.

Il routing emerge dalle decisioni di function calling del modello e viene gestito dal Backend attraverso il ciclo di orchestrazione.

---

## 2.2 Attori e componenti coinvolti

Dal punto di vista dei requisiti, il sistema comprende un attore umano principale e diversi componenti software.

| Attore / Componente | Descrizione |
|---------------------|-------------|
| Utente | Interagisce con Maranello AI attraverso l'interfaccia conversazionale. |
| React Frontend | Gestisce chat, input, stato UI, errori e visualizzazione dei grafici. |
| Node.js Backend | Espone le API, mantiene lo stato conversazionale e orchestra i servizi. |
| Large Language Model | Interpreta la richiesta, decide l'utilizzo dei tool e sintetizza la risposta finale. |
| RAG Engine | Recupera contenuti rilevanti dalla Knowledge Base. |
| ChromaDB | Memorizza e ricerca semanticamente i chunk documentali. |
| Python Data Agent | Esegue analisi deterministiche sul Manufacturing Dataset. |
| Knowledge Base | Fornisce policy e procedure aziendali fittizie. |
| Manufacturing Dataset | Fornisce i dati strutturati utilizzati nelle analisi quantitative. |

I componenti software non vengono considerati utenti applicativi.

L'unico attore esterno principale è l'utente che interagisce con il sistema tramite il Frontend.

---

## 2.3 Contesto operativo

Il sistema viene eseguito come insieme di servizi separati.

La configurazione locale di riferimento comprende:

    React Frontend
    http://127.0.0.1:5173

    Node.js Backend
    http://127.0.0.1:3000

    ChromaDB
    http://127.0.0.1:8000

    Python Data Agent
    http://127.0.0.1:8001

Il Frontend comunica esclusivamente con il Backend applicativo.

Il flusso previsto è:

    Browser
       ↓
    React Frontend
       ↓
    Node.js Backend
       ↓
    ┌─────────────────────────────┐
    │                             │
    ▼                             ▼
    OpenAI API              Internal Services
                                  │
                         ┌────────┴────────┐
                         ▼                 ▼
                      ChromaDB       Python Data Agent

Il Browser non comunica direttamente con:

- OpenAI API;
- ChromaDB;
- Python Data Agent.

I grafici generati dal Data Agent vengono resi disponibili al Frontend attraverso il Chart Proxy del Backend.

---

## 2.4 Assunzioni

Il corretto funzionamento completo del sistema assume che:

- il Manufacturing Dataset sia disponibile localmente al Python Data Agent;
- la Knowledge Base sia disponibile nel repository;
- i documenti siano stati indicizzati nella collection ChromaDB configurata;
- ChromaDB sia in esecuzione e raggiungibile dal Backend;
- il Python Data Agent sia in esecuzione e raggiungibile dal Backend;
- il Backend disponga di una configurazione valida per il provider AI;
- le variabili d'ambiente richieste siano configurate;
- l'utente utilizzi un browser moderno;
- la connettività verso il provider AI sia disponibile quando richiesta;
- i servizi utilizzino porte compatibili con la configurazione applicativa.

L'indisponibilità di una dipendenza non deve causare la terminazione anomala dell'applicazione.

Quando una dipendenza necessaria alla richiesta non è disponibile, il sistema deve utilizzare il comportamento di errore controllato previsto.

---

## 2.5 Vincoli

La versione finale del progetto rispetta i seguenti vincoli.

### Frontend

Il client web utilizza:

    React
    TypeScript
    Vite

Il Frontend deve utilizzare il Backend come unico gateway verso i servizi applicativi.

### Backend

Il livello di orchestrazione utilizza:

    Node.js
    Express
    TypeScript

Il Backend è responsabile delle integrazioni con:

- provider AI;
- RAG;
- ChromaDB;
- Python Data Agent.

### AI Provider

L'orchestrazione utilizza la OpenAI Responses API e native function calling.

Le credenziali devono essere fornite attraverso variabili d'ambiente.

### RAG

Il sistema utilizza:

    ChromaDB

come vector database locale.

La Knowledge Base è costituita da documentazione fittizia creata per il progetto.

### Data Agent

Il servizio analitico utilizza:

    Python
    FastAPI
    Pandas
    DuckDB
    Matplotlib

Il Data Agent deve utilizzare il Manufacturing Dataset CSV come fonte riproducibile dei dati analitici.

Pandas viene utilizzato per il caricamento e il cleaning deterministico, mentre il dataset preparato viene materializzato in DuckDB per l'esecuzione delle query analitiche.

L'analisi deve essere controllata e deterministica.

Non è richiesta l'esecuzione arbitraria di codice Python generato dal Large Language Model.

### Data Source

Il Manufacturing Dataset deve:

- utilizzare formato CSV;
- contenere almeno 1000 record;
- includere date;
- includere categorie;
- includere metriche numeriche;
- contenere anomalie intenzionali utili a dimostrare il processo di data cleaning.

La versione finale utilizza un dataset di 2000 righe.

### Architecture

Il sistema deve mantenere una separazione tra:

- presentation layer;
- orchestration layer;
- retrieval layer;
- analytical layer;
- data sources.

Questa separazione costituisce uno dei vincoli architetturali fondamentali del progetto.

### Security

Le credenziali e i segreti non devono essere hardcoded nel codice sorgente.

Il file `.env` contenente valori reali deve essere escluso dal versionamento.

### Business Context

Il progetto deve utilizzare esclusivamente dati, documenti e policy fittizi o sintetici.

Non devono essere rappresentati come reali dati, policy o procedure appartenenti a Ferrari N.V. o ad altre aziende automotive realmente esistenti.

---

# 3. Requisiti funzionali

I requisiti funzionali descrivono i comportamenti che la versione corrente di Maranello AI deve garantire.

Ogni requisito è identificato attraverso un codice univoco `RF-XXX` e include:

- priorità;
- attore o componente responsabile;
- descrizione;
- input;
- output;
- criterio di accettazione.

---

## 3.1 Frontend

### RF-001 — Invio di una richiesta

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Utente |
| Descrizione | Il sistema deve consentire all'utente di inviare richieste testuali attraverso l'interfaccia conversazionale. |
| Input | Messaggio testuale |
| Output | Richiesta inviata al Backend |
| Criterio di accettazione | Un messaggio valido viene visualizzato nella conversazione e trasmesso al Backend attraverso la Chat API. |

---

### RF-002 — Validazione dell'input utente

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | React Frontend |
| Descrizione | Il Frontend deve impedire l'invio di richieste vuote o costituite esclusivamente da whitespace. |
| Input | Contenuto del composer |
| Output | Invio consentito oppure bloccato |
| Criterio di accettazione | Il comando di invio non produce una richiesta API quando il messaggio non contiene testo significativo. |

La validazione client-side costituisce una prima protezione dell'interfaccia e non sostituisce la validazione eseguita dal Backend.

---

### RF-003 — Visualizzazione della risposta

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | React Frontend |
| Descrizione | Il Frontend deve visualizzare nella conversazione la risposta restituita dal Backend. |
| Input | Risposta della Chat API |
| Output | Messaggio Assistant |
| Criterio di accettazione | Il contenuto testuale restituito dal Backend viene visualizzato correttamente nella conversazione. |

Il rendering deve preservare la struttura testuale necessaria alla leggibilità della risposta.

---

### RF-004 — Cronologia della conversazione

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | React Frontend |
| Descrizione | Il Frontend deve mantenere nello stato dell'applicazione i messaggi della conversazione corrente. |
| Input | Sequenza di messaggi User e Assistant |
| Output | Conversazione visualizzata |
| Criterio di accettazione | I messaggi precedenti della sessione corrente rimangono visibili durante l'interazione. |

La persistenza permanente della cronologia nel browser non costituisce un requisito della versione corrente.

---

### RF-005 — Indicatore di elaborazione

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | React Frontend |
| Descrizione | Durante l'elaborazione di una richiesta il Frontend deve mostrare uno stato visivo di loading/typing. |
| Input | Richiesta in elaborazione |
| Output | Indicatore visivo |
| Criterio di accettazione | L'indicatore viene mostrato durante l'attesa e rimosso quando la richiesta termina con successo o errore. |

Durante l'elaborazione il sistema deve inoltre evitare invii concorrenti non intenzionali dalla stessa interfaccia.

---

### RF-006 — Visualizzazione dei grafici

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | React Frontend |
| Descrizione | Il Frontend deve visualizzare nativamente nella conversazione i grafici associati alle risposte analitiche. |
| Input | `chartUrl` restituito dal Backend |
| Output | Immagine del grafico integrata nella chat |
| Criterio di accettazione | Quando la risposta contiene un riferimento valido a un grafico, l'immagine viene visualizzata direttamente nella conversazione. |

Il Frontend deve utilizzare il riferimento esposto dal Backend e non deve accedere direttamente al filesystem o al servizio Python.

---

### RF-007 — Supporto bilingue dell'interfaccia conversazionale

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Utente |
| Descrizione | L'interfaccia conversazionale deve permettere l'utilizzo del sistema sia in italiano sia in inglese senza richiedere una selezione manuale della lingua. |
| Input | Richiesta in italiano o inglese |
| Output | Risposta nella lingua appropriata |
| Criterio di accettazione | Il sistema può ricevere richieste in entrambe le lingue e la risposta viene prodotta nella lingua della richiesta. |

La selezione della lingua della risposta viene gestita dall'orchestrazione AI; il Frontend non implementa un language selector obbligatorio.

---

### RF-008 — Gestione degli errori nel Frontend

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | React Frontend |
| Descrizione | Il Frontend deve gestire gli errori restituiti dal Backend senza interrompere il funzionamento dell'interfaccia. |
| Input | Risposta HTTP di errore o errore di comunicazione |
| Output | Messaggio di errore visibile |
| Criterio di accettazione | L'utente viene informato dell'errore e l'interfaccia rimane utilizzabile per richieste successive. |

---

## 3.2 Backend

### RF-009 — Esposizione della Chat API

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve esporre un endpoint REST per ricevere le richieste conversazionali provenienti dal Frontend. |
| Input | `POST /api/chat` |
| Output | Risposta conversazionale strutturata |
| Criterio di accettazione | Una richiesta valida viene accettata, elaborata e produce una risposta HTTP contenente almeno `sessionId`, `answer` e `toolsUsed`. |

Il contratto applicativo principale utilizza una struttura equivalente a:

    Request

    {
      "message": "user question",
      "sessionId": "optional-session-id"
    }

    Response

    {
      "sessionId": "session-id",
      "answer": "assistant answer",
      "toolsUsed": []
    }

Quando disponibile, la risposta può includere anche:

    "chartUrl": "/api/charts/example.png"

---

### RF-010 — Validazione delle richieste Backend

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve validare il contenuto della richiesta prima di avviare l'orchestrazione AI. |
| Input | Payload HTTP |
| Output | Richiesta valida oppure errore client |
| Criterio di accettazione | Un messaggio mancante, vuoto o composto esclusivamente da whitespace viene rifiutato con HTTP `400`. |

La validazione Backend è indipendente dalla validazione presente nel Frontend e protegge direttamente il contratto API.

---

### RF-011 — Gestione della sessione conversazionale

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve associare ogni conversazione a un `sessionId` e mantenere lo stato necessario alla continuità della sessione. |
| Input | Messaggio e `sessionId` opzionale |
| Output | Sessione nuova oppure sessione esistente aggiornata |
| Criterio di accettazione | In assenza di `sessionId` viene creata una nuova sessione; quando viene fornito un identificativo valido, la conversazione continua utilizzando lo stato associato. |

Lo stato viene mantenuto in-memory nella versione corrente.

La persistenza delle conversazioni oltre il ciclo di vita del Backend non costituisce un requisito corrente.

---

### RF-012 — Continuità tramite OpenAI Responses API

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve mantenere il riferimento necessario a continuare una conversazione multi-turn attraverso la Responses API. |
| Input | Stato della sessione e precedente identificativo della risposta |
| Output | Chiamata AI contestualizzata |
| Criterio di accettazione | Quando disponibile, il precedente response identifier viene utilizzato come `previous_response_id` nella successiva interazione con il modello. |

Il Conversation Manager mantiene il valore applicativo:

    lastResponseId

associato alla sessione.

Questo requisito permette scenari nei quali una domanda successiva contiene riferimenti contestuali come:

    that supplier

senza richiedere all'utente di ripetere esplicitamente tutte le informazioni precedenti.

---

### RF-013 — Integrazione con il Python Data Agent

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve poter invocare il Python Data Agent quando l'orchestrazione AI richiede un'analisi quantitativa. |
| Input | Domanda analitica |
| Output | Risultato strutturato dell'analisi |
| Criterio di accettazione | Il Backend trasmette la richiesta al Data Agent e rende il risultato disponibile al ciclo di orchestrazione AI. |

Quando il Data Agent produce un grafico, il Backend deve inoltre poter utilizzare il relativo riferimento per costruire il `chartUrl` destinato al Frontend.

---

### RF-014 — Integrazione con il RAG Engine

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve poter eseguire il retrieval dalla Knowledge Base quando l'orchestrazione AI richiede conoscenza documentale. |
| Input | Query documentale |
| Output | Contenuti rilevanti e relativi metadata |
| Criterio di accettazione | I contenuti recuperati da ChromaDB vengono restituiti al ciclo di orchestrazione e possono essere utilizzati per produrre la risposta finale. |

Il Backend deve mantenere le informazioni necessarie a identificare la provenienza dei contenuti recuperati.

---

### RF-015 — Chart Proxy

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve esporre i grafici generati dal Python Data Agent attraverso un endpoint controllato accessibile dal Frontend. |
| Input | `GET /api/charts/:filename` |
| Output | Immagine del grafico |
| Criterio di accettazione | Un filename valido consente al Frontend di recuperare il grafico attraverso il Backend senza comunicare direttamente con il Data Agent. |

Il Chart Proxy deve:

- validare il filename richiesto;
- impedire path traversal;
- recuperare il file dal servizio Python;
- restituire il contenuto dell'immagine al client.

Il flusso previsto è:

    Python Data Agent
          ↓
    Generated Chart
          ↓
    Node.js Chart Proxy
          ↓
    /api/charts/:filename
          ↓
    React Frontend

---

## 3.3 AI Orchestration

### RF-016 — Orchestrazione tramite OpenAI Responses API

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | Il sistema deve utilizzare il Large Language Model attraverso la OpenAI Responses API per interpretare la richiesta, decidere l'eventuale utilizzo di strumenti specializzati e sintetizzare la risposta finale. |
| Input | Messaggio utente e contesto conversazionale |
| Output | Risposta diretta oppure richiesta di esecuzione di uno o più tool |
| Criterio di accettazione | Una richiesta viene elaborata dal modello e può produrre direttamente una risposta oppure uno o più function call coerenti con gli strumenti disponibili. |

Il sistema non utilizza un classificatore applicativo separato per assegnare preventivamente categorie quali:

    Documentale
    Analitica
    Ibrida

La decisione emerge invece dal comportamento di tool calling del modello.

---

### RF-017 — Esposizione dei tool al modello

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve rendere disponibili al modello gli strumenti applicativi necessari per accedere alla Knowledge Base e al Manufacturing Dataset. |
| Input | Definizione dei tool e relativi schema |
| Output | Tool disponibili durante l'interazione con il modello |
| Criterio di accettazione | Il modello può richiedere l'esecuzione dei tool definiti dall'applicazione attraverso native function calling. |

I tool principali sono:

    search_knowledge_base

    analyze_manufacturing_data

`search_knowledge_base` rappresenta il boundary verso la conoscenza documentale.

`analyze_manufacturing_data` rappresenta il boundary verso l'analisi quantitativa.

Gli argomenti dei tool devono rispettare gli schema definiti dal Backend.

---

### RF-018 — Selezione autonoma degli strumenti

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Large Language Model |
| Descrizione | Il modello deve decidere autonomamente se la richiesta richiede l'utilizzo di nessun tool, del RAG, del Data Agent oppure di entrambi. |
| Input | Richiesta utente e contesto disponibile |
| Output | Decisione di tool calling |
| Criterio di accettazione | L'utente non deve selezionare manualmente il componente da utilizzare e il sistema può adottare Direct, RAG, Data Analysis o Hybrid in funzione della richiesta. |

I comportamenti supportati sono:

    Direct
        nessun tool

    RAG
        search_knowledge_base

    Data Analysis
        analyze_manufacturing_data

    Hybrid
        search_knowledge_base
        +
        analyze_manufacturing_data

Il routing non deve dipendere da una selezione manuale effettuata nel Frontend.

---

### RF-019 — Esecuzione dei function call

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Quando il modello produce un function call, il Backend deve identificare il tool richiesto, validarne gli argomenti ed eseguire il componente applicativo corrispondente. |
| Input | Function call prodotto dal modello |
| Output | Risultato del tool |
| Criterio di accettazione | Un function call valido viene associato al tool corretto e il relativo risultato viene reso disponibile al modello. |

Il Backend mantiene il controllo dell'esecuzione.

Il Large Language Model non accede direttamente:

- a ChromaDB;
- al filesystem;
- al Manufacturing Dataset;
- al Python runtime;
- ai servizi interni.

---

### RF-020 — Restituzione dei tool output al modello

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il risultato di ogni tool eseguito deve essere restituito alla Responses API come output del function call corrispondente. |
| Input | Risultato prodotto dal tool |
| Output | Function call output inviato al modello |
| Criterio di accettazione | Il modello riceve il risultato del tool e può utilizzarlo per continuare il processo di orchestrazione. |

Il Backend utilizza il meccanismo previsto dalla Responses API per associare l'output al function call originario.

---

### RF-021 — Tool execution loop

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | L'orchestrazione deve supportare più round di tool execution quando necessari alla risoluzione della richiesta. |
| Input | Response contenente uno o più function call |
| Output | Nuova interazione con il modello oppure risposta finale |
| Criterio di accettazione | Il Backend continua il ciclo di esecuzione finché il modello produce una risposta finale oppure viene raggiunto il limite applicativo previsto. |

Il comportamento generale è:

    User Question
          ↓
    OpenAI Responses API
          ↓
    Function Call?
       /      \
      No      Yes
      │        │
      │    Execute Tool
      │        │
      │    Tool Output
      │        │
      │        └──────────┐
      │                   │
      │                   ▼
      │          OpenAI Responses API
      │                   │
      └───────────────────┤
                          ▼
                    Final Response

Il sistema deve applicare un limite al numero di round per evitare cicli di tool execution non terminanti.

---

### RF-022 — Esecuzione di più tool

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | Il sistema deve supportare l'esecuzione di più function call quando una richiesta richiede informazioni provenienti da capacità differenti. |
| Input | Uno o più function call |
| Output | Collezione dei risultati dei tool |
| Criterio di accettazione | Una richiesta Hybrid può utilizzare sia risultati quantitativi sia contenuti documentali prima della generazione della risposta finale. |

Quando più tool vengono richiesti nello stesso round, il Backend può eseguirli indipendentemente e restituire i relativi risultati al modello.

Una richiesta Hybrid non viene determinata da una categoria rigida assegnata prima dell'esecuzione.

È il modello a stabilire, sulla base della domanda, quali evidenze siano necessarie.

---

### RF-023 — Preservazione dello scope della richiesta analitica

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | Quando il modello delega una richiesta al Data Agent, deve preservare il significato e lo scope analitico espresso dall'utente senza introdurre arbitrariamente filtri o dimensioni non richiesti. |
| Input | Richiesta analitica dell'utente |
| Output | Argomento coerente per `analyze_manufacturing_data` |
| Criterio di accettazione | Il tool riceve una richiesta semanticamente coerente con la domanda originale e non vengono introdotti vincoli analitici non richiesti. |

Questo requisito è particolarmente importante per:

- dimensioni di raggruppamento;
- trend temporali;
- supplier;
- production line;
- shift;
- component category;
- vehicle model;
- plant;
- operator team.

---

### RF-024 — Selezione automatica della lingua

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Large Language Model |
| Descrizione | Il sistema deve riconoscere la lingua utilizzata dall'utente e produrre la risposta finale nella stessa lingua. |
| Input | Messaggio in italiano o inglese |
| Output | Risposta nella lingua della richiesta |
| Criterio di accettazione | Una domanda italiana produce una risposta italiana e una domanda inglese produce una risposta inglese. |

La lingua non viene selezionata manualmente attraverso l'interfaccia.

---

### RF-025 — Sintesi della risposta finale

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Large Language Model |
| Descrizione | Al termine dell'orchestrazione il modello deve sintetizzare una singola risposta utilizzando esclusivamente le evidenze applicabili alla richiesta. |
| Input | Domanda, contesto conversazionale ed eventuali tool output |
| Output | Risposta finale |
| Criterio di accettazione | L'utente riceve una risposta unica, comprensibile e coerente con i risultati prodotti dai componenti utilizzati. |

Nel comportamento Hybrid la risposta può combinare:

    quantitative evidence
             +
    company policy
             ↓
    contextual answer

Il modello non deve alterare arbitrariamente i valori numerici restituiti dal Data Agent né inventare policy non presenti nel contesto documentale recuperato.

---

## 3.4 Retrieval-Augmented Generation (RAG)

### RF-026 — Ricerca semantica nella Knowledge Base

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Il sistema deve effettuare retrieval semantico all'interno della Knowledge Base utilizzando ChromaDB. |
| Input | Query documentale |
| Output | Chunk documentali rilevanti |
| Criterio di accettazione | Una query coerente con il dominio recupera contenuti semanticamente pertinenti dalla collection configurata. |

Il retrieval utilizza embedding semantici per confrontare la query con i contenuti indicizzati.

---

### RF-027 — Utilizzo della Knowledge Base indicizzata

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Il sistema deve utilizzare la collection ChromaDB costruita a partire dalla Knowledge Base fittizia del progetto. |
| Input | Query semantica |
| Output | Risultati provenienti dai documenti indicizzati |
| Criterio di accettazione | I risultati recuperati appartengono ai documenti della Knowledge Base configurata. |

La Knowledge Base finale comprende cinque documenti operativi principali:

    manufacturing_quality_policy.md
    non_conformity_procedure.md
    supplier_quality_procedure.md
    rework_and_scrap_procedure.md
    production_escalation_policy.md

L'indicizzazione finale produce:

    149 chunks

---

### RF-028 — Recupero dei contenuti rilevanti

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Il sistema deve recuperare i chunk più rilevanti rispetto alla query ricevuta e renderli disponibili all'orchestrazione. |
| Input | Query documentale |
| Output | Contenuti recuperati |
| Criterio di accettazione | Il risultato del retrieval contiene contesto utilizzabile dal modello per rispondere alla richiesta documentale. |

Il retrieval deve fornire contesto documentale e non una risposta aziendale inventata autonomamente dal componente di ricerca.

---

### RF-029 — Metadata e attribuzione della fonte

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | I risultati del retrieval devono mantenere metadata sufficienti a identificare la provenienza del contenuto recuperato. |
| Input | Chunk recuperato |
| Output | Contenuto e metadata |
| Criterio di accettazione | Il modello riceve insieme al contenuto le informazioni necessarie per identificare il documento o la sezione di provenienza. |

Questi metadata permettono alla risposta finale di fare riferimento alle fonti aziendali utilizzate.

---

### RF-030 — Grounding delle risposte documentali

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | Le affermazioni relative a policy e procedure aziendali devono essere basate sui contenuti recuperati dalla Knowledge Base. |
| Input | Contesto RAG |
| Output | Risposta documentale grounded |
| Criterio di accettazione | Le informazioni aziendali presenti nella risposta sono coerenti con i contenuti recuperati e non vengono sostituite da policy inventate dal modello. |

La conoscenza generale del modello non costituisce una fonte valida per inventare regole interne dell'organizzazione fittizia.

---

### RF-031 — Attribuzione delle fonti nelle risposte RAG

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | Quando una risposta utilizza informazioni provenienti dalla Knowledge Base, il sistema deve rendere riconoscibile la fonte documentale utilizzata. |
| Input | Metadata dei risultati RAG |
| Output | Riferimento alla fonte nella risposta |
| Criterio di accettazione | Una risposta documentale identifica il documento o la sezione della Knowledge Base utilizzata come evidenza. |

---

### RF-032 — Gestione di informazioni documentali insufficienti

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | Quando i contenuti recuperati non supportano una risposta relativa a policy o procedure aziendali, il sistema non deve inventare l'informazione mancante. |
| Input | Contesto RAG insufficiente |
| Output | Risposta che segnala il limite informativo |
| Criterio di accettazione | Il sistema distingue l'assenza di evidenza documentale da una policy aziendale verificata. |

---

### RF-033 — Cross-language retrieval

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Il sistema deve supportare il retrieval semantico quando la lingua della query differisce dalla lingua dei documenti indicizzati. |
| Input | Query in italiano o inglese |
| Output | Chunk semanticamente pertinenti |
| Criterio di accettazione | Una query italiana può recuperare correttamente contenuti pertinenti dalla Knowledge Base in inglese. |

La versione corrente della Knowledge Base utilizza documentazione operativa in inglese.

Il supporto bilingue non richiede quindi la duplicazione dei documenti in entrambe le lingue.

Il comportamento previsto è:

    Italian Question
          ↓
    Semantic Embedding
          ↓
    ChromaDB
          ↓
    English Knowledge Base Content
          ↓
    LLM
          ↓
    Italian Answer

Lo stesso sistema continua a supportare direttamente query formulate in inglese.

---

## 3.5 Python Data Agent

### RF-034 — Esposizione del servizio di analisi

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve esporre un servizio HTTP attraverso FastAPI per ricevere richieste analitiche dal Backend. |
| Input | Richiesta di analisi |
| Output | Risultato strutturato |
| Criterio di accettazione | Il Backend può inviare una richiesta al servizio Python e ricevere una risposta analitica valida. |

L'endpoint applicativo principale è:

    POST /api/analysis

Il servizio espone inoltre un health check utilizzabile per verificarne la disponibilità.

---

### RF-035 — Caricamento del Manufacturing Dataset

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve caricare il Manufacturing Dataset CSV utilizzato come fonte riproducibile per le analisi quantitative del progetto. |
| Input | Manufacturing Dataset |
| Output | Dataset preparato e disponibile nel layer analitico DuckDB |
| Criterio di accettazione | Il dataset viene caricato e pulito deterministicamente tramite Pandas e materializzato correttamente nel database DuckDB locale. |

La versione finale del dataset contiene:

    2000 rows
    20 columns

Ogni record rappresenta un batch produttivo.

---

### RF-036 — Data cleaning

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve applicare operazioni di cleaning controllate prima di utilizzare il dataset per le analisi. |
| Input | Dataset originale |
| Output | Dataset normalizzato per l'analisi |
| Criterio di accettazione | Le anomalie previste dal dataset vengono gestite in maniera coerente e riproducibile. |

Il processo deve gestire almeno:

- record duplicati;
- valori testuali non normalizzati;
- date con formati differenti;
- missing values;
- quality score non validi;
- record numericamente incoerenti;
- outlier previsti dal dataset.

Il processo di cleaning non deve alterare arbitrariamente i dati validi.

---

### RF-037 — Interpretazione deterministica delle richieste

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve interpretare la richiesta ricevuta riconducendola a una tipologia analitica supportata attraverso un Question Interpreter deterministico. |
| Input | Domanda analitica in linguaggio naturale |
| Output | Intento analitico validato |
| Criterio di accettazione | Una richiesta appartenente allo scope supportato viene associata in maniera deterministica all'analisi prevista. |

Il Question Interpreter supporta richieste in italiano e inglese.

Le principali categorie supportate sono:

    global KPI analysis
    grouped analysis
    monthly trend analysis

L'interpretazione non utilizza un secondo LLM per generare codice Python.

---

### RF-038 — Analisi KPI globali

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve calcolare i principali KPI globali del Manufacturing Dataset. |
| Input | Dataset pulito |
| Output | KPI globali |
| Criterio di accettazione | I KPI restituiti sono calcolati deterministicamente a partire dal dataset disponibile. |

I principali KPI supportati comprendono:

- total production;
- total defective units;
- defect rate;
- rework rate;
- scrap rate;
- average quality score;
- average downtime minutes;
- average cycle time seconds.

I valori numerici devono essere calcolati dal Data Agent e non dal Large Language Model.

---

### RF-039 — Grouped analysis

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve supportare il confronto del defect rate attraverso le principali dimensioni produttive previste dal progetto. |
| Input | Richiesta relativa a una dimensione supportata |
| Output | Risultati aggregati per gruppo |
| Criterio di accettazione | Il sistema produce un confronto coerente con la dimensione richiesta e ordina i risultati secondo il comportamento analitico previsto. |

Le dimensioni supportate sono:

    production_line
    shift
    supplier_id
    component_category
    vehicle_model
    plant
    operator_team

Una richiesta può quindi identificare, per esempio:

- la production line con defect rate più elevato;
- il supplier con defect rate più elevato;
- le differenze tra shift;
- le differenze tra component category;
- le differenze tra vehicle model;
- le differenze tra plant;
- le differenze tra operator team.

---

### RF-040 — Monthly trend analysis

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve supportare l'analisi temporale mensile del defect rate. |
| Input | Richiesta di trend temporale |
| Output | Serie mensile del defect rate |
| Criterio di accettazione | Il risultato contiene il trend mensile calcolato a partire dalle production date valide del dataset. |

L'analisi temporale corrente è focalizzata sul monthly trend.

Analisi temporali arbitrarie non costituiscono un requisito della versione corrente.

---

### RF-041 — Validazione dello scope analitico

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve rifiutare o segnalare richieste che combinano modalità analitiche non supportate dal Question Interpreter. |
| Input | Richiesta analitica |
| Output | Analisi valida oppure errore controllato |
| Criterio di accettazione | Il servizio non esegue un'analisi arbitraria quando la richiesta supera lo scope deterministico supportato. |

La versione corrente non supporta arbitrariamente:

- più dimensioni di raggruppamento nella stessa analisi;
- combinazione libera di grouped analysis e temporal analysis;
- query analitiche o SQL arbitrarie;
- esecuzione di codice Python fornito dall'utente;
- esecuzione di codice Python generato dal Large Language Model.

Questa limitazione è intenzionale e migliora:

- sicurezza;
- prevedibilità;
- riproducibilità;
- testabilità.

---

### RF-042 — Generazione dei grafici

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve poter generare un grafico quando la richiesta analitica supportata richiede una rappresentazione visuale. |
| Input | Risultato analitico |
| Output | Immagine PNG |
| Criterio di accettazione | Il servizio genera un file immagine valido e restituisce un riferimento utilizzabile dal Backend. |

La generazione utilizza:

    Matplotlib

con backend non interattivo adatto all'esecuzione server-side.

I grafici vengono salvati utilizzando filename distinti per evitare collisioni tra richieste.

---

### RF-043 — Esposizione dei grafici generati

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve rendere disponibili al Backend i grafici generati attraverso il proprio servizio HTTP. |
| Input | Filename del grafico |
| Output | Immagine corrispondente |
| Criterio di accettazione | Il Backend può recuperare un grafico valido e renderlo disponibile al Frontend attraverso il Chart Proxy. |

Il riferimento interno del Data Agent utilizza il percorso:

    /charts/:filename

Il Frontend non utilizza direttamente questo endpoint.

---

### RF-044 — Produzione del risultato analitico

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve restituire al Backend un risultato strutturato contenente le informazioni necessarie alla sintesi della risposta finale. |
| Input | Risultato dell'analisi |
| Output | Payload analitico strutturato |
| Criterio di accettazione | Il Backend riceve informazioni numeriche e descrittive sufficienti a restituire il risultato al ciclo di orchestrazione. |

Quando applicabile, il risultato deve includere anche il riferimento al grafico generato.

---

### RF-045 — Integrità dei risultati numerici

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | I risultati quantitativi devono derivare esclusivamente dal Manufacturing Dataset e dalle operazioni deterministiche implementate dal servizio. |
| Input | Dataset e richiesta analitica supportata |
| Output | Risultato quantitativo |
| Criterio di accettazione | Lo stesso dataset e la stessa analisi producono risultati numericamente riproducibili. |

Il Large Language Model può interpretare e spiegare il risultato, ma non costituisce la fonte dei valori numerici.

---

## 3.6 Gestione degli errori

### RF-046 — Gestione centralizzata degli errori Backend

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve intercettare gli errori applicativi e trasformarli in risposte HTTP controllate. |
| Input | Errore applicativo |
| Output | Risposta HTTP strutturata |
| Criterio di accettazione | Un errore gestito non causa la terminazione anomala del processo Backend e produce una risposta coerente verso il client. |

La gestione degli errori deve evitare di esporre dettagli interni non necessari all'utente.

---

### RF-047 — Gestione dell'indisponibilità del Data Agent

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Quando una richiesta richiede il Python Data Agent e il servizio non è disponibile, il Backend deve restituire un errore controllato. |
| Input | Data Agent non raggiungibile |
| Output | HTTP `503 Service Unavailable` |
| Criterio di accettazione | L'utente riceve un messaggio comprensibile che segnala la temporanea indisponibilità dell'analisi dati. |

Il comportamento deve impedire al modello di sostituire arbitrariamente il risultato mancante con valori inventati.

---

### RF-048 — Gestione dell'indisponibilità di ChromaDB

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Quando una richiesta richiede la Knowledge Base e ChromaDB non è disponibile, il Backend deve restituire un errore controllato. |
| Input | ChromaDB non raggiungibile |
| Output | HTTP `503 Service Unavailable` |
| Criterio di accettazione | L'utente riceve un messaggio comprensibile che segnala la temporanea indisponibilità della Knowledge Base. |

Il sistema non deve inventare policy o procedure per compensare l'indisponibilità del retrieval.

---

### RF-049 — Gestione degli errori di comunicazione con servizi esterni

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve gestire gli errori di comunicazione con le dipendenze applicative senza interrompere in modo anomalo il servizio. |
| Input | Errore di rete, timeout o errore del servizio |
| Output | Errore applicativo controllato |
| Criterio di accettazione | La richiesta termina in modo controllato e il Backend rimane disponibile per richieste successive. |

---

### RF-050 — Gestione degli errori nel ciclo di orchestrazione

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | AI Orchestration |
| Descrizione | Gli errori prodotti durante l'esecuzione dei tool devono essere propagati in modo controllato attraverso il livello applicativo. |
| Input | Errore durante tool execution |
| Output | Risposta di errore controllata |
| Criterio di accettazione | Un tool non disponibile o non eseguibile non viene silenziosamente sostituito da una risposta non supportata. |

---

## 3.7 Funzionalità tecniche complementari

### RF-051 — Health Check del Backend

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve esporre un endpoint di health check per verificare che il servizio applicativo sia in esecuzione. |
| Input | Richiesta HTTP |
| Output | Stato del servizio |
| Criterio di accettazione | Il servizio risponde correttamente quando il processo Backend è operativo. |

L'health check verifica la disponibilità del servizio Backend e non implica necessariamente la disponibilità di tutte le dipendenze esterne.

---

### RF-052 — Health Check del Data Agent

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve esporre un endpoint di health check per verificare la disponibilità del microservizio Python. |
| Input | Richiesta HTTP |
| Output | Stato del servizio |
| Criterio di accettazione | Il servizio restituisce uno stato positivo quando FastAPI è operativo. |

---

### RF-053 — Tracciamento dei tool utilizzati

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Backend deve mantenere per ogni risposta l'elenco dei tool effettivamente utilizzati durante il ciclo di orchestrazione. |
| Input | Function call eseguiti |
| Output | `toolsUsed` |
| Criterio di accettazione | La risposta della Chat API contiene un elenco coerente con i tool realmente eseguiti. |

Esempi possibili:

    []

    ["search_knowledge_base"]

    ["analyze_manufacturing_data"]

    ["search_knowledge_base", "analyze_manufacturing_data"]

Questo campo rappresenta il comportamento effettivo dell'orchestrazione e sostituisce la necessità di una categoria di routing rigida.

---

### RF-054 — Conversione del riferimento al grafico

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Quando il Data Agent restituisce un riferimento interno a un grafico, il Backend deve convertirlo nel riferimento esposto attraverso il Chart Proxy. |
| Input | Riferimento `/charts/:filename` del Data Agent |
| Output | `chartUrl` Backend |
| Criterio di accettazione | Il Frontend riceve un URL relativo al Backend utilizzabile per recuperare il grafico. |

Il mapping applicativo segue il principio:

    Data Agent
    /charts/example.png

            ↓

    Backend
    /api/charts/example.png

---

### RF-055 — Protezione del Chart Proxy

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Node.js Backend |
| Descrizione | Il Chart Proxy deve validare il filename richiesto prima di recuperare una risorsa dal Data Agent. |
| Input | Parametro `filename` |
| Output | Immagine valida oppure errore controllato |
| Criterio di accettazione | Filename non validi o tentativi di path traversal non consentono l'accesso arbitrario a percorsi differenti da quelli previsti. |

---

### RF-056 — Configurazione tramite environment variables

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Attore | Sistema |
| Descrizione | I valori configurabili e i segreti applicativi devono essere forniti attraverso environment variables anziché essere hardcoded nel codice sorgente. |
| Input | Configurazione ambiente |
| Output | Configurazione runtime |
| Criterio di accettazione | API key e principali endpoint/configurazioni vengono caricati dall'ambiente e i valori sensibili reali non sono presenti nel repository versionato. |

Tra le configurazioni principali rientrano:

    OPENAI_API_KEY
    OPENAI_EMBEDDING_MODEL
    LLM_MODEL
    LLM_TEMPERATURE
    LLM_TIMEOUT_SECONDS
    PORT
    DATA_AGENT_URL
    CHROMA_URL
    CHROMA_COLLECTION

Il repository deve fornire configurazioni di esempio senza includere credenziali reali.

---

# 4. Requisiti non funzionali

I requisiti non funzionali definiscono le caratteristiche qualitative e i vincoli tecnici che la versione corrente di Maranello AI deve rispettare.

---

## RNF-001 — Manutenibilità

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Il sistema deve essere organizzato secondo una struttura modulare che mantenga separate le principali responsabilità applicative. |
| Criterio di accettazione | Frontend, Backend, RAG e Python Data Agent mantengono responsabilità chiaramente separate e il codice è organizzato in moduli specializzati. |

---

## RNF-002 — Separazione delle responsabilità

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Presentation layer, orchestration layer, retrieval layer e analytical layer devono rimanere separati. |
| Criterio di accettazione | Il Frontend non esegue retrieval o analisi dati e il Large Language Model non accede direttamente alle sorgenti applicative. |

---

## RNF-003 — Usabilità

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | L'interazione principale deve avvenire attraverso un'unica interfaccia conversazionale senza richiedere all'utente conoscenza dell'architettura interna. |
| Criterio di accettazione | L'utente può formulare una richiesta in linguaggio naturale senza selezionare manualmente RAG, Data Agent o modalità Hybrid. |

---

## RNF-004 — Sicurezza delle credenziali

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | API key e altri valori sensibili non devono essere hardcoded nel codice sorgente o inclusi nel repository versionato. |
| Criterio di accettazione | I valori sensibili vengono caricati attraverso environment variables e il file `.env` reale è escluso dal versionamento. |

Il repository può includere un file `.env.example` contenente esclusivamente placeholder e configurazioni non sensibili.

---

## RNF-005 — Esecuzione locale

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | La soluzione deve poter essere eseguita in ambiente locale attraverso i servizi che compongono l'architettura. |
| Criterio di accettazione | ChromaDB, Python Data Agent, Node.js Backend e React Frontend possono essere avviati localmente e utilizzati come sistema integrato. |

La containerizzazione non costituisce un requisito della versione corrente.

---

## RNF-006 — Supporto bilingue

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Il sistema deve supportare interazioni conversazionali in italiano e inglese. |
| Criterio di accettazione | Domande formulate in italiano e inglese vengono elaborate correttamente e ricevono una risposta nella lingua appropriata. |

Il supporto bilingue deve applicarsi anche a scenari nei quali la query e la documentazione recuperata utilizzano lingue differenti.

---

## RNF-007 — Riproducibilità delle analisi

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Le analisi quantitative devono essere deterministiche e riproducibili a parità di dataset e tipologia di analisi. |
| Criterio di accettazione | La stessa analisi eseguita sullo stesso dataset produce gli stessi risultati numerici. |

---

## RNF-008 — Controllo dell'esecuzione Python

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Il Data Agent non deve eseguire arbitrariamente codice Python generato dal Large Language Model o fornito dall'utente. |
| Criterio di accettazione | Le richieste vengono ricondotte esclusivamente alle operazioni analitiche supportate dal Question Interpreter deterministico. |

---

## RNF-009 — Grounding documentale

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Le informazioni relative a policy e procedure aziendali devono essere supportate dalla Knowledge Base. |
| Criterio di accettazione | Le risposte documentali utilizzano contenuti recuperati dal RAG e rendono identificabile la relativa fonte. |

---

## RNF-010 — Integrità dei risultati quantitativi

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | I valori quantitativi presentati come risultati delle analisi manifatturiere devono provenire dal Python Data Agent. |
| Criterio di accettazione | KPI, confronti e trend vengono calcolati dal Data Agent attraverso query DuckDB deterministiche sul dataset preparato e non inventati dal modello. |

---

## RNF-011 — Resilienza applicativa

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | L'indisponibilità di una dipendenza necessaria non deve causare la terminazione anomala dell'applicazione. |
| Criterio di accettazione | L'indisponibilità controllata di Data Agent o ChromaDB produce una risposta HTTP gestita e il Backend rimane operativo. |

---

## RNF-012 — Controllo del ciclo di orchestrazione

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Il ciclo di tool execution deve essere limitato per evitare iterazioni non terminanti. |
| Criterio di accettazione | L'orchestratore applica un numero massimo configurato o definito di round di tool execution. |

---

## RNF-013 — Estendibilità del Backend

| Campo | Valore |
|-------|--------|
| Priorità | Should Have |
| Descrizione | L'architettura del Backend deve consentire l'introduzione di ulteriori tool o servizi senza richiedere una riprogettazione dell'interfaccia conversazionale. |
| Criterio di accettazione | Le integrazioni AI e i connector sono separati dalla logica del Frontend. |

---

## RNF-014 — Estendibilità del Data Agent

| Campo | Valore |
|-------|--------|
| Priorità | Should Have |
| Descrizione | Il Data Agent deve essere organizzato in modo da consentire l'aggiunta futura di nuove tipologie di analisi controllate. |
| Criterio di accettazione | Interpretazione della domanda, caricamento/cleaning dei dati, analisi e generazione dei grafici mantengono responsabilità separate. |

---

## RNF-015 — Protezione del boundary applicativo

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Il Frontend non deve accedere direttamente alle dipendenze interne dell'architettura. |
| Criterio di accettazione | OpenAI, ChromaDB e Python Data Agent vengono raggiunti attraverso il Backend e non direttamente dal Browser. |

---

## RNF-016 — Controllo degli errori

| Campo | Valore |
|-------|--------|
| Priorità | Must Have |
| Descrizione | Gli errori applicativi devono essere gestiti attraverso boundary controllati senza esporre dettagli interni non necessari all'utente. |
| Criterio di accettazione | Gli errori previsti vengono convertiti in risposte applicative comprensibili e non causano crash del processo. |

---

# 5. Business Rules

Le Business Rules definiscono i principi che devono governare il comportamento applicativo indipendentemente dal singolo componente tecnico.

| ID | Regola |
|----|--------|
| BR-001 | Le policy e le procedure aziendali devono provenire dalla Knowledge Base fittizia del progetto. |
| BR-002 | Il sistema non deve inventare policy, procedure o soglie aziendali non supportate dalla Knowledge Base. |
| BR-003 | I risultati quantitativi relativi alla produzione devono derivare esclusivamente dal Manufacturing Dataset attraverso il Python Data Agent. |
| BR-004 | L'utente non deve selezionare manualmente il componente necessario alla risposta. |
| BR-005 | L'LLM deve poter decidere autonomamente se utilizzare nessun tool, RAG, Data Agent o entrambi. |
| BR-006 | Una richiesta che necessita sia di evidenza quantitativa sia di conoscenza documentale deve poter utilizzare entrambi i tool. |
| BR-007 | Le risposte basate sulla Knowledge Base devono rendere riconoscibile la fonte documentale utilizzata. |
| BR-008 | Il sistema deve rispondere nella lingua utilizzata dall'utente tra italiano e inglese. |
| BR-009 | Il Data Agent deve utilizzare esclusivamente analisi appartenenti allo scope deterministico supportato. |
| BR-010 | Il Data Agent non deve eseguire arbitrary Python code generato dal modello o fornito dall'utente. |
| BR-011 | L'orchestrazione non deve introdurre arbitrariamente filtri o dimensioni analitiche non richiesti dall'utente. |
| BR-012 | Il modello può spiegare i risultati numerici ma non deve sostituire o alterare arbitrariamente i valori prodotti dal Data Agent. |
| BR-013 | Quando una fonte necessaria non è disponibile, il sistema deve utilizzare un comportamento di errore controllato invece di inventare l'informazione mancante. |
| BR-014 | Il Frontend deve utilizzare il Node.js Backend come unico gateway applicativo. |
| BR-015 | Dataset, policy, procedure e business scenario devono essere presentati come fittizi o sintetici e non come informazioni appartenenti ad aziende reali. |

---

# 6. Casi d'uso principali

I casi d'uso seguenti rappresentano le principali modalità di utilizzo verificate per la versione corrente.

| ID | Caso d'uso | Componenti principali |
|----|------------|------------------------|
| UC-001 | Consultazione di una policy o procedura aziendale | Frontend, Backend, AI Orchestration, RAG, ChromaDB |
| UC-002 | Analisi di KPI produttivi globali | Frontend, Backend, AI Orchestration, Python Data Agent |
| UC-003 | Confronto del defect rate per dimensione produttiva | Frontend, Backend, AI Orchestration, Python Data Agent |
| UC-004 | Analisi del trend mensile | Frontend, Backend, AI Orchestration, Python Data Agent |
| UC-005 | Generazione e visualizzazione di un grafico | Frontend, Backend, Chart Proxy, Python Data Agent |
| UC-006 | Analisi Hybrid di dati e documentazione | Frontend, Backend, AI Orchestration, RAG, Python Data Agent |
| UC-007 | Conversazione in italiano | Frontend, Backend, AI Orchestration |
| UC-008 | Conversazione in inglese | Frontend, Backend, AI Orchestration |
| UC-009 | Cross-language retrieval | AI Orchestration, RAG, ChromaDB |
| UC-010 | Conversazione multi-turn | Frontend, Conversation Manager, OpenAI Responses API |
| UC-011 | Gestione dell'indisponibilità del Data Agent | Frontend, Backend |
| UC-012 | Gestione dell'indisponibilità di ChromaDB | Frontend, Backend |

---

## 6.1 UC-001 — Consultazione di una policy aziendale

**Esempio**

    Qual è la soglia critica del defect rate secondo la Quality Policy?

**Flusso principale**

    User
      ↓
    Frontend
      ↓
    Backend
      ↓
    LLM
      ↓
    search_knowledge_base
      ↓
    ChromaDB
      ↓
    Knowledge Base
      ↓
    LLM Synthesis
      ↓
    Answer with source

**Risultato atteso**

La risposta utilizza la Manufacturing Quality Policy e restituisce la soglia documentata senza inventare regole aggiuntive.

---

## 6.2 UC-002 — Analisi di KPI produttivi

**Esempio**

    Qual è il defect rate complessivo?

**Flusso principale**

    User
      ↓
    Frontend
      ↓
    Backend
      ↓
    LLM
      ↓
    analyze_manufacturing_data
      ↓
    Python Data Agent
      ↓
    DuckDBAnalysisRepository
      ↓
    Deterministic DuckDB Query
      ↓
    Tool Result
      ↓
    Final Answer

**Risultato atteso**

Il valore quantitativo viene calcolato dal Data Agent utilizzando il Manufacturing Dataset.

---

## 6.3 UC-003 — Confronto per dimensione produttiva

**Esempio**

    Quale supplier presenta il defect rate più elevato?

**Flusso principale**

Il Question Interpreter identifica:

    supplier_id

come dimensione analitica e il Data Agent calcola il defect rate aggregato per supplier.

**Risultato atteso**

Il sistema restituisce il confronto e identifica il supplier con il valore più elevato sulla base del dataset.

---

## 6.4 UC-004 — Analisi del trend mensile

**Esempio**

    Mostrami il trend mensile del defect rate.

**Flusso principale**

Il Data Agent identifica la richiesta temporale e calcola il defect rate aggregato per mese.

**Risultato atteso**

Il sistema restituisce la serie temporale mensile coerente con le production date valide.

---

## 6.5 UC-005 — Generazione e visualizzazione di un grafico

**Esempio**

    Genera il grafico del trend mensile del defect rate.

**Flusso principale**

    User Request
         ↓
    Python Data Agent
         ↓
    Monthly Analysis
         ↓
    Matplotlib
         ↓
    PNG
         ↓
    Data Agent /charts/:filename
         ↓
    Backend /api/charts/:filename
         ↓
    React Frontend

**Risultato atteso**

Il grafico viene visualizzato direttamente nella conversazione senza richiedere un download manuale.

---

## 6.6 UC-006 — Analisi Hybrid

**Esempio**

    Quale supplier presenta il defect rate più elevato e come viene classificato dalla Supplier Quality Procedure?

**Flusso principale**

    User Question
          ↓
    AI Orchestration
       /          \
      ▼            ▼
    Data Agent     RAG
      │            │
      ▼            ▼
    Supplier KPI   Supplier Quality Procedure
       \           /
        \         /
         ▼       ▼
        LLM Synthesis
             ↓
       Contextual Answer

**Risultato atteso**

La risposta combina il valore quantitativo calcolato dal Data Agent con le soglie recuperate dalla Supplier Quality Procedure.

---

## 6.7 UC-007 — Conversazione bilingue

**Esempio italiano**

    Qual è la soglia critica del defect rate?

**Risultato atteso**

La risposta viene prodotta in italiano.

**Esempio inglese**

    What is the critical defect-rate threshold?

**Risultato atteso**

La risposta viene prodotta in inglese.

---

## 6.8 UC-008 — Cross-language retrieval

La Knowledge Base operativa è in inglese.

Il sistema deve comunque supportare una query italiana come:

    Quali soglie utilizza la Supplier Quality Procedure?

Il retrieval semantico deve poter recuperare i contenuti inglesi pertinenti.

Il modello deve quindi sintetizzare la risposta in italiano.

---

## 6.9 UC-009 — Conversazione multi-turn

**Prima richiesta**

    Which supplier has the highest defect rate?

Il Data Agent identifica il supplier rilevante.

**Richiesta successiva**

    What does the policy say about that supplier?

Il sistema deve utilizzare il contesto della conversazione per interpretare:

    that supplier

senza richiedere all'utente di ripetere l'identificativo.

---

## 6.10 UC-010 — Controlled failure del Data Agent

Quando una richiesta necessita di analisi quantitativa ma il Python Data Agent non è disponibile:

    Analytical Request
          ↓
    Data Agent unavailable
          ↓
    HTTP 503
          ↓
    Controlled Error

Il sistema non deve inventare il risultato quantitativo mancante.

---

## 6.11 UC-011 — Controlled failure della Knowledge Base

Quando una richiesta necessita della Knowledge Base ma ChromaDB non è disponibile:

    RAG Request
         ↓
    ChromaDB unavailable
         ↓
    HTTP 503
         ↓
    Controlled Error

Il sistema non deve inventare la policy aziendale mancante.

---

# 7. Criteri di accettazione

I criteri di accettazione verificano che l'implementazione finale soddisfi lo scope funzionale definito dal presente documento.

| ID | Criterio | Stato |
|----|----------|-------|
| AC-001 | L'utente può interagire con il sistema attraverso una chat React. | PASS |
| AC-002 | Il Frontend impedisce l'invio di richieste vuote o costituite esclusivamente da whitespace. | PASS |
| AC-003 | Il Backend espone `POST /api/chat`. | PASS |
| AC-004 | Il Backend rifiuta richieste con messaggio vuoto attraverso HTTP `400`. | PASS |
| AC-005 | Il sistema crea e mantiene un `sessionId` per la conversazione. | PASS |
| AC-006 | La conversazione multi-turn mantiene il contesto tra richieste successive. | PASS |
| AC-007 | Il sistema utilizza `previous_response_id` quando disponibile. | PASS |
| AC-008 | L'LLM decide autonomamente se utilizzare i tool disponibili. | PASS |
| AC-009 | Una richiesta può essere gestita senza tool quando non sono necessarie fonti specializzate. | PASS |
| AC-010 | Le richieste documentali possono utilizzare `search_knowledge_base`. | PASS |
| AC-011 | Le richieste analitiche possono utilizzare `analyze_manufacturing_data`. | PASS |
| AC-012 | Una richiesta Hybrid può utilizzare entrambi i tool. | PASS |
| AC-013 | Il Backend supporta il ciclo function call → tool execution → function call output → risposta successiva. | PASS |
| AC-014 | Il RAG utilizza ChromaDB per il retrieval semantico. | PASS |
| AC-015 | La Knowledge Base operativa è indicizzata e utilizzabile dal sistema. | PASS |
| AC-016 | Il retrieval mantiene informazioni relative alla fonte documentale. | PASS |
| AC-017 | Una query italiana può recuperare contenuti pertinenti dalla Knowledge Base inglese. | PASS |
| AC-018 | Le risposte documentali utilizzano la Knowledge Base come fonte delle policy aziendali. | PASS |
| AC-019 | Il Python Data Agent utilizza il Manufacturing Dataset CSV. | PASS |
| AC-020 | Il Data Agent applica il processo di cleaning previsto. | PASS |
| AC-021 | Il Data Agent utilizza un Question Interpreter deterministico. | PASS |
| AC-022 | Il Data Agent calcola KPI globali attraverso query DuckDB deterministiche. | PASS |
| AC-023 | Il Data Agent supporta grouped analysis per le dimensioni previste. | PASS |
| AC-024 | Il Data Agent supporta il monthly trend del defect rate. | PASS |
| AC-025 | Il Data Agent non esegue arbitrary LLM-generated Python code. | PASS |
| AC-026 | Il Data Agent può generare grafici PNG tramite Matplotlib. | PASS |
| AC-027 | Il Backend espone i grafici attraverso `/api/charts/:filename`. | PASS |
| AC-028 | Il Frontend visualizza i grafici direttamente nella conversazione. | PASS |
| AC-029 | Il sistema supporta richieste e risposte in italiano. | PASS |
| AC-030 | Il sistema supporta richieste e risposte in inglese. | PASS |
| AC-031 | L'indisponibilità del Data Agent viene gestita attraverso HTTP `503`. | PASS |
| AC-032 | L'indisponibilità di ChromaDB viene gestita attraverso HTTP `503`. | PASS |
| AC-033 | Il Backend rimane operativo dopo un errore applicativo controllato. | PASS |
| AC-034 | Le credenziali reali non sono hardcoded nel codice sorgente. | PASS |
| AC-035 | Il file `.env` reale è escluso dal versionamento. | PASS |
| AC-036 | Il Backend restituisce `toolsUsed` coerente con gli strumenti eseguiti. | PASS |
| AC-037 | I test automatici del Backend risultano superati. | PASS |
| AC-038 | Type checking, linting e build del Backend risultano superati. | PASS |
| AC-039 | Linting e build del Frontend risultano superati. | PASS |
| AC-040 | Gli scenari manuali RAG, Data Analysis, Hybrid, multi-turn e bilingue risultano verificati. | PASS |

I dettagli relativi alle evidenze di test, ai test automatici e agli scenari QA sono documentati nel:

    06_Test_Plan.md

Le attività finali di delivery non modificano lo stato dei requisiti software già verificati.

Restano gestite separatamente:

- finalizzazione del README;
- presentazione finale;
- clean clone verification;
- packaging della consegna.

---

# 8. Conclusioni

La presente Software Requirements Specification descrive i requisiti della versione finale **as-built** di Maranello AI.

Il sistema soddisfa l'obiettivo principale di fornire un'unica interfaccia conversazionale capace di integrare:

- Large Language Model;
- autonomous tool routing;
- Retrieval-Augmented Generation;
- ChromaDB;
- Knowledge Base aziendale fittizia;
- Python Data Agent;
- preparazione deterministica dei dati tramite Pandas;
- analisi deterministica tramite DuckDB;
- Manufacturing Dataset sintetico;
- generazione di grafici tramite Matplotlib;
- conversation memory;
- supporto italiano/inglese;
- controlled failure handling.

L'architettura mantiene una separazione chiara tra:

    Frontend
        user experience

    Backend
        orchestration and application state

    Large Language Model
        reasoning, tool selection and synthesis

    RAG
        enterprise knowledge retrieval

    Python Data Agent
        deterministic numerical analysis

    Data Sources
        fictional Knowledge Base
        synthetic Manufacturing Dataset

Una caratteristica fondamentale della soluzione è che il Large Language Model non costituisce l'unica fonte di verità.

Le informazioni aziendali vengono recuperate dalla Knowledge Base, mentre i risultati quantitativi vengono calcolati dal Python Data Agent.

Il modello mantiene invece il ruolo di:

- interpretazione della richiesta;
- selezione degli strumenti;
- orchestrazione;
- integrazione delle evidenze;
- sintesi della risposta finale.

La versione corrente dimostra quindi un'architettura Hybrid AI nella quale capacità generative, retrieval documentale e analisi strutturata dei dati collaborano mantenendo boundary applicativi distinti e verificabili.

Le funzionalità production-grade non appartenenti allo scope corrente, quali autenticazione enterprise, RBAC, persistenza distribuita, observability avanzata, containerizzazione e CI/CD dedicato, rimangono possibili evoluzioni future e non vengono considerate requisiti implementati della versione corrente.

---

## Stato del documento

| Informazione | Valore |
|--------------|--------|
| Documento | Software Requirements Specification |
| Versione | 2.0 |
| Stato | Final |
| Tipologia | As-Built Software Requirements Specification |
| Lingua | Italiano |
| Ultimo aggiornamento | Settembre 2026 |

---