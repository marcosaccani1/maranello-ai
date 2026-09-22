# API Specification

> **Progetto:** Maranello AI  
> **Versione:** 2.0  
> **Tipo documento:** API Specification  
> **Stato:** Final  
> **Autore:** Marco Saccani  
> **Ultimo aggiornamento:** Settembre 2026  

---

# Indice

1. Introduzione  
2. Obiettivi  
3. Architettura delle API  
4. Principi di progettazione  
5. Convenzioni generali  
6. Formato delle richieste e delle risposte  
7. Gestione degli errori  
8. Health Check API  
9. Backend API  
10. Chat API  
11. Chart Proxy API  
12. Python Data Agent API  
13. Sicurezza  
14. Logging e osservabilità  
15. Testing delle API  
16. Evoluzioni future  
17. Conclusioni  

---

# 1. Introduzione

Il presente documento descrive le API implementate nel sistema **Maranello AI**, definendone responsabilità, contratti di comunicazione, formati delle richieste e delle risposte, gestione degli errori e modalità di integrazione tra i diversi componenti applicativi.

Il documento rappresenta la specifica **as-built** delle API della versione finale del progetto e riflette quindi il comportamento effettivamente implementato.

Maranello AI adotta un'architettura distribuita composta principalmente da:

- frontend React;
- backend Node.js ed Express;
- AI Orchestrator basato su OpenAI Responses API e function calling;
- motore RAG integrato con ChromaDB;
- Python Data Agent basato su FastAPI e Pandas;
- Manufacturing Dataset in formato CSV;
- Knowledge Base documentale indicizzata nel vector database.

L'interfaccia conversazionale React utilizza il backend Node.js come unico punto di accesso applicativo.

Il frontend non comunica direttamente con il Python Data Agent, con ChromaDB o con OpenAI. Il backend agisce come livello di orchestrazione e coordina le dipendenze interne necessarie all'elaborazione delle richieste.

Le principali interfacce HTTP implementate sono:

| Componente | Tecnologia | Responsabilità |
|------------|------------|----------------|
| Backend API | Node.js ed Express | Espone i servizi utilizzati dal frontend e coordina l'elaborazione AI. |
| Chat API | Node.js ed Express | Gestisce le richieste conversazionali e mantiene la continuità della sessione. |
| Chart Proxy API | Node.js ed Express | Espone in modo controllato al frontend i grafici prodotti dal Data Agent. |
| Data Agent API | Python e FastAPI | Espone le funzionalità di analisi del Manufacturing Dataset. |
| Health Check API | Express e FastAPI | Consente di verificare lo stato operativo dei servizi applicativi. |

Le integrazioni con OpenAI e ChromaDB sono considerate dipendenze interne del backend e non vengono esposte direttamente al frontend.

---

## 1.1 Scope del documento

La specifica copre le API applicative implementate nella versione finale di Maranello AI.

In particolare vengono documentati:

- il contratto tra frontend React e backend Node.js;
- l'endpoint conversazionale principale;
- la gestione del `sessionId`;
- la struttura delle risposte generate dal backend;
- il recupero dei grafici tramite backend proxy;
- la comunicazione tra backend e Python Data Agent;
- gli endpoint di health check;
- la gestione degli errori applicativi e delle dipendenze non disponibili;
- i principi di sicurezza e separazione tra API pubbliche e servizi interni.

Le chiamate effettuate dal backend verso OpenAI e ChromaDB non costituiscono API pubbliche di Maranello AI e vengono pertanto descritte soltanto quando necessario per comprendere il flusso applicativo.

---

## 1.2 Contesto applicativo

Maranello AI è un assistente enterprise dimostrativo progettato per il dominio **Quality & Manufacturing Operations** di un produttore automobilistico premium fittizio.

Il sistema deve poter gestire differenti categorie di richieste attraverso una singola interfaccia conversazionale.

Una domanda dell'utente può richiedere:

- una risposta conversazionale;
- il recupero di informazioni dalla Knowledge Base;
- un'analisi quantitativa del Manufacturing Dataset;
- una combinazione di retrieval documentale e analisi strutturata.

La scelta degli strumenti non viene effettuata dal frontend e non viene determinata tramite una semplice regola statica sugli endpoint.

Il backend mette a disposizione dell'LLM gli strumenti applicativi disponibili e utilizza il **native function calling** per consentire al modello di selezionare autonomamente il percorso di elaborazione più appropriato.

---

# 2. Obiettivi

La progettazione delle API di Maranello AI persegue i seguenti obiettivi.

| ID | Obiettivo |
|----|-----------|
| API-OBJ-001 | Definire un contratto stabile tra frontend React e backend Node.js. |
| API-OBJ-002 | Utilizzare il backend come unico punto di accesso applicativo per il frontend. |
| API-OBJ-003 | Separare le API esposte al client dai servizi e dalle dipendenze interne. |
| API-OBJ-004 | Supportare richieste conversazionali, documentali, analitiche e ibride attraverso una singola Chat API. |
| API-OBJ-005 | Consentire all'LLM di selezionare autonomamente gli strumenti mediante function calling. |
| API-OBJ-006 | Mantenere la continuità conversazionale mediante un identificativo di sessione. |
| API-OBJ-007 | Standardizzare la comunicazione JSON tra i componenti applicativi. |
| API-OBJ-008 | Isolare il Python Data Agent dal frontend attraverso il backend Node.js. |
| API-OBJ-009 | Consentire il recupero sicuro dei grafici tramite un Chart Proxy dedicato. |
| API-OBJ-010 | Gestire in modo controllato indisponibilità e errori delle dipendenze interne. |
| API-OBJ-011 | Facilitare testing, debugging e manutenzione dei servizi. |
| API-OBJ-012 | Mantenere un'architettura estendibile verso future integrazioni e modalità di persistenza. |

---

## 2.1 Separazione delle responsabilità

Uno dei principi fondamentali della progettazione consiste nel mantenere separate le responsabilità dei diversi servizi.

Il frontend è responsabile della presentazione e dell'interazione con l'utente.

Il backend Node.js è responsabile della validazione delle richieste, della gestione della sessione, dell'orchestrazione AI, dell'esecuzione dei tool e della costruzione della risposta applicativa.

Il Python Data Agent è responsabile esclusivamente dell'analisi deterministica dei dati manifatturieri e della generazione degli eventuali grafici.

Il motore RAG è responsabile del retrieval delle informazioni dalla Knowledge Base indicizzata in ChromaDB.

L'LLM coordina il processo decisionale selezionando, tramite function calling, gli strumenti necessari alla richiesta corrente.

Questa separazione riduce l'accoppiamento tra i componenti e consente di modificare o sostituire un servizio senza modificare direttamente l'interfaccia utilizzata dal frontend.

---

## 2.2 API come boundary applicativo

Il backend Node.js costituisce il principale **application boundary** del sistema.

Dal punto di vista del frontend, le implementazioni interne utilizzate per produrre una risposta sono trasparenti.

Una richiesta può quindi richiedere:

```text
Frontend
    ↓
Backend
    ↓
LLM
```

oppure:

```text
Frontend
    ↓
Backend
    ↓
LLM
    ↓
RAG
    ↓
ChromaDB
```

oppure:

```text
Frontend
    ↓
Backend
    ↓
LLM
    ↓
Python Data Agent
    ↓
Manufacturing Dataset
```

oppure una combinazione dei due strumenti:

```text
Frontend
    ↓
Backend
    ↓
LLM
   ↙   ↘
 RAG   Data Agent
   ↘   ↙
Backend
    ↓
Frontend
```

In tutti i casi il contratto principale utilizzato dal frontend rimane invariato.

---

# 3. Architettura delle API

## 3.1 Panoramica

L'architettura API di Maranello AI distingue tra:

1. **API esposte al frontend**;
2. **API interne tra servizi**;
3. **integrazioni applicative verso servizi esterni o infrastrutturali**.

Il frontend comunica esclusivamente con il backend Node.js.

Il backend coordina l'elaborazione AI e, in funzione delle tool call richieste dall'LLM, può:

- interrogare il motore RAG;
- comunicare con ChromaDB;
- invocare il Python Data Agent;
- utilizzare direttamente il modello per una risposta conversazionale;
- combinare più strumenti nella stessa elaborazione.

Il seguente diagramma rappresenta il modello generale.

```mermaid
flowchart LR

    User["Utente"]

    FE["Frontend React"]

    BE["Backend API<br/>Node.js / Express"]

    AI["AI Orchestrator<br/>OpenAI Responses API"]

    RAG["RAG Module"]

    Chroma["ChromaDB"]

    DA["Python Data Agent<br/>FastAPI"]

    CSV["Manufacturing Dataset<br/>CSV"]

    Charts["Generated Charts<br/>PNG"]

    User --> FE

    FE -->|"HTTP / JSON"| BE

    BE --> AI

    AI -->|"search_knowledge_base"| RAG

    RAG --> Chroma

    AI -->|"analyze_manufacturing_data"| DA

    DA --> CSV

    DA --> Charts

    BE -->|"Chart Proxy"| DA

    BE --> FE
```

---

## 3.2 API esposte al frontend

Nella versione finale del progetto il frontend utilizza un insieme limitato di endpoint del backend.

Le principali interfacce applicative sono:

| Metodo | Endpoint | Responsabilità |
|--------|----------|----------------|
| POST | `/api/chat` | Invia un messaggio e riceve la risposta generata dal sistema. |
| GET | `/api/charts/:filename` | Recupera tramite backend proxy un grafico generato dal Python Data Agent. |
| GET | `/health` | Verifica lo stato operativo del backend Node.js. |

Il frontend non deve conoscere gli indirizzi interni di:

- Python Data Agent;
- ChromaDB;
- OpenAI.

Questa scelta mantiene il client indipendente dalla topologia interna dell'applicazione.

---

## 3.3 API interne

Il Python Data Agent espone un'API REST utilizzata dal backend Node.js.

Le principali interfacce interne sono:

| Metodo | Endpoint | Responsabilità |
|--------|----------|----------------|
| POST | `/api/analysis` | Esegue un'analisi sul Manufacturing Dataset a partire da una richiesta in linguaggio naturale. |
| GET | `/health` | Verifica lo stato operativo del Python Data Agent. |
| GET | `/` | Fornisce una risposta base del servizio. |
| GET | `/charts/:filename` | Espone i file PNG generati dal servizio analitico. |

L'endpoint `/api/analysis` non è utilizzato direttamente dal frontend.

La sua invocazione viene effettuata dal backend quando l'LLM seleziona il tool:

```text
analyze_manufacturing_data
```

Analogamente, i file disponibili tramite `/charts/:filename` non vengono referenziati direttamente dal frontend. Il backend espone il proprio Chart Proxy in modo da mantenere il Python Data Agent nascosto dietro il boundary applicativo.

---

## 3.4 Integrazioni interne non esposte come REST API applicative

Oltre alle API HTTP tra i componenti, il backend utilizza integrazioni interne necessarie all'esecuzione del sistema.

### OpenAI Responses API

Il backend utilizza OpenAI come motore di orchestrazione AI.

Il modello riceve il contesto conversazionale e la definizione degli strumenti disponibili.

I principali tool applicativi sono:

```text
search_knowledge_base
```

e:

```text
analyze_manufacturing_data
```

Il modello può scegliere di:

- non utilizzare alcun tool;
- utilizzare il RAG;
- utilizzare il Data Agent;
- utilizzare entrambi gli strumenti;
- effettuare ulteriori round di tool calling quando necessari alla costruzione della risposta.

Le tool call vengono eseguite dal backend e i risultati vengono restituiti al modello come output delle funzioni.

---

### ChromaDB

ChromaDB costituisce il vector database utilizzato dal modulo RAG.

L'accesso avviene dal backend attraverso il relativo client e non viene esposto direttamente al frontend.

Il flusso logico è:

```text
LLM
 ↓
search_knowledge_base
 ↓
RAG Module
 ↓
ChromaDB
 ↓
Relevant Chunks
 ↓
Backend
 ↓
LLM
```

Il risultato del retrieval viene quindi utilizzato dall'LLM per generare una risposta coerente con la documentazione interna disponibile.

---

## 3.5 Flusso di una richiesta conversazionale

Il flusso principale inizia quando l'utente invia un messaggio attraverso il frontend React.

```mermaid
sequenceDiagram

    participant User as Utente
    participant FE as Frontend React
    participant BE as Backend Node.js
    participant AI as OpenAI / AI Orchestrator
    participant RAG as RAG Module
    participant DA as Python Data Agent

    User->>FE: Inserisce una richiesta
    FE->>BE: POST /api/chat

    BE->>BE: Validazione input
    BE->>BE: Recupero / creazione sessione

    BE->>AI: Messaggio + contesto + tool disponibili

    alt Nessun tool necessario
        AI-->>BE: Risposta conversazionale
    else Knowledge Base necessaria
        AI-->>BE: search_knowledge_base
        BE->>RAG: Ricerca documentale
        RAG-->>BE: Chunk rilevanti + metadati
        BE->>AI: function_call_output
        AI-->>BE: Risposta finale
    else Analisi dati necessaria
        AI-->>BE: analyze_manufacturing_data
        BE->>DA: POST /api/analysis
        DA-->>BE: Metriche + insight + eventuale chart
        BE->>AI: function_call_output
        AI-->>BE: Risposta finale
    else Richiesta ibrida
        AI-->>BE: Multiple tool calls
        par Retrieval documentale
            BE->>RAG: Ricerca Knowledge Base
            RAG-->>BE: Contesto documentale
        and Analisi dati
            BE->>DA: POST /api/analysis
            DA-->>BE: Metriche + insight + eventuale chart
        end
        BE->>AI: Tool outputs
        AI-->>BE: Risposta sintetizzata
    end

    BE->>BE: Aggiornamento sessione
    BE-->>FE: JSON response
    FE-->>User: Testo + eventuale grafico
```

Il backend mantiene quindi un unico contratto conversazionale verso il frontend, indipendentemente dal percorso di elaborazione scelto dall'LLM.

---

## 3.6 Flusso del Chart Proxy

Quando il Python Data Agent produce un grafico, il file viene generato nel servizio Python.

Il backend converte il riferimento restituito dal Data Agent in un URL appartenente alla propria API.

Il frontend utilizza quindi:

```http
GET /api/charts/:filename
```

e non l'endpoint Python direttamente.

Il flusso è il seguente:

```mermaid
sequenceDiagram

    participant FE as Frontend React
    participant BE as Backend Node.js
    participant DA as Python Data Agent

    FE->>BE: GET /api/charts/:filename
    BE->>BE: Validazione filename
    BE->>DA: GET /charts/:filename
    DA-->>BE: PNG image
    BE-->>FE: PNG image
```

Questa soluzione permette di:

- mantenere un singolo punto di accesso applicativo;
- evitare di esporre direttamente il microservizio Python;
- ridurre l'accoppiamento tra frontend e servizi interni;
- centralizzare la validazione delle richieste relative ai grafici;
- impedire l'utilizzo arbitrario di percorsi file attraverso la validazione del nome richiesto.

---

## 3.7 Gestione della sessione

La continuità conversazionale viene gestita mediante un identificativo denominato:

```text
sessionId
```

Alla prima richiesta il frontend può non fornire alcun `sessionId`.

Il backend crea quindi una nuova sessione e restituisce l'identificativo nella risposta.

Nelle richieste successive il frontend reinvia lo stesso identificativo.

Il backend utilizza il `sessionId` per:

- associare i messaggi appartenenti alla stessa conversazione;
- recuperare la cronologia applicativa;
- mantenere il riferimento all'ultima risposta OpenAI;
- supportare richieste contestuali successive;
- mantenere continuità semantica tra più turni.

La persistenza delle conversazioni nella versione corrente è **in-memory**.

Questa scelta è adeguata allo scope dimostrativo del progetto, ma implica che lo stato venga perso al riavvio del backend.

Una futura evoluzione enterprise potrebbe introdurre un database persistente o una cache distribuita.

---

## 3.8 Autonomous Tool Routing

Un elemento centrale dell'architettura API è l'assenza di endpoint separati lato frontend per RAG e Data Agent.

Il frontend non invia richieste del tipo:

```text
/api/rag
```

oppure:

```text
/api/data-analysis
```

per decidere quale modalità utilizzare.

Invia invece sempre la domanda dell'utente attraverso:

```http
POST /api/chat
```

La decisione sul percorso di elaborazione viene effettuata dal modello attraverso il meccanismo di function calling.

Questo consente alla stessa API di supportare:

| Tipologia richiesta | Comportamento |
|---------------------|---------------|
| Conversazionale | Risposta del modello senza tool applicativi. |
| Documentale | Utilizzo di `search_knowledge_base`. |
| Analitica | Utilizzo di `analyze_manufacturing_data`. |
| Ibrida | Utilizzo di entrambi i tool e sintesi finale dei risultati. |

L'API rimane quindi stabile mentre la logica di orchestrazione può evolvere indipendentemente.

---

## 3.9 Boundary di sicurezza

La separazione tra API pubbliche e interne costituisce anche un boundary di sicurezza.

Il frontend non riceve accesso diretto:

- alla chiave OpenAI;
- al Python Data Agent;
- al vector database;
- al filesystem utilizzato per i grafici;
- al Manufacturing Dataset;
- alla configurazione interna dei tool.

Le credenziali e gli URL dei servizi vengono gestiti lato server mediante variabili d'ambiente.

Il browser conosce esclusivamente l'URL del backend applicativo.

Questa architettura evita l'esposizione di credenziali sensibili e limita l'accoppiamento del client con l'infrastruttura interna.

---

# 4. Principi di progettazione

## 4.1 API minimali

Le API della versione finale di Maranello AI sono state mantenute intenzionalmente semplici.

L'obiettivo non è esporre un grande numero di endpoint specializzati, ma utilizzare pochi contratti chiari che riflettano direttamente le responsabilità dei componenti.

Il frontend utilizza principalmente:

```text
POST /api/chat
GET /api/charts/:filename
GET /health
```

Il backend utilizza il Python Data Agent principalmente attraverso:

```text
POST /api/analysis
GET /health
GET /charts/:filename
```

Questa scelta riduce:

- complessità dell'interfaccia;
- duplicazione della logica;
- accoppiamento tra frontend e servizi interni;
- superficie esposta;
- numero di contratti da mantenere.

---

## 4.2 Single Conversational Entry Point

Tutte le richieste conversazionali vengono inviate attraverso:

```http
POST /api/chat
```

Il frontend non deve decidere in anticipo se la richiesta appartiene a:

- Knowledge Base;
- Manufacturing Dataset;
- conversazione generale;
- scenario ibrido.

La selezione viene effettuata successivamente dall'AI Orchestrator tramite function calling.

Il contratto HTTP rimane quindi indipendente dal percorso interno di elaborazione.

---

## 4.3 Backend as API Gateway

Il backend Node.js costituisce il punto di accesso principale dell'applicazione.

Il frontend non accede direttamente a:

- OpenAI;
- ChromaDB;
- Python Data Agent;
- Manufacturing Dataset;
- filesystem dei grafici.

Questo principio permette di centralizzare:

- validazione;
- gestione delle sessioni;
- error handling;
- orchestrazione;
- configurazione;
- sicurezza;
- routing verso i servizi interni.

---

## 4.4 Autonomous Routing

La selezione degli strumenti è responsabilità dell'LLM.

Gli strumenti applicativi principali sono:

```text
search_knowledge_base
analyze_manufacturing_data
```

Il backend non richiede al frontend campi come:

```text
intent
executionType
useRag
useDataAgent
selectedTool
```

Il comportamento viene determinato autonomamente dal modello sulla base della richiesta dell'utente e del contesto conversazionale.

---

## 4.5 Deterministic Data Analysis

Il Python Data Agent non esegue codice Python arbitrario generato dall'LLM.

Il backend inoltra al servizio analitico la richiesta naturale necessaria all'esecuzione del tool.

Il Data Agent utilizza quindi un **Question Interpreter deterministico** per mappare la domanda verso operazioni analitiche supportate.

Questo approccio evita:

- esecuzione arbitraria di codice;
- accesso incontrollato al filesystem;
- analisi non previste;
- comportamento difficilmente testabile;
- risultati non riproducibili.

L'architettura conserva comunque il comportamento agentico richiesto a livello di orchestrazione: è l'LLM a decidere **quando** utilizzare il Data Agent, mentre il servizio Python controlla **come** viene eseguita l'analisi.

---

## 4.6 Stateless HTTP e stateful conversation

Le singole chiamate HTTP rimangono indipendenti dal punto di vista del protocollo.

La continuità conversazionale viene invece mantenuta applicativamente tramite:

```text
sessionId
```

Questo permette di combinare:

- semplicità delle API REST;
- stato conversazionale;
- continuità con OpenAI Responses API.

---

## 4.7 Fail Fast

Gli input non validi vengono rifiutati prima dell'invocazione dell'AI Orchestrator.

Ad esempio, un messaggio:

- assente;
- vuoto;
- composto esclusivamente da spazi;

non deve generare una chiamata verso il modello.

Il backend restituisce invece:

```text
400 Bad Request
```

Questo evita elaborazioni inutili e mantiene prevedibile il comportamento dell'API.

---

## 4.8 Controlled Failure

Quando una dipendenza indispensabile non è disponibile, il backend non restituisce al frontend errori infrastrutturali grezzi.

Il sistema traduce il problema in una risposta controllata.

Esempi:

```text
Manufacturing data analysis is temporarily unavailable. Please try again later.
```

oppure:

```text
The company knowledge base is temporarily unavailable. Please try again later.
```

Il codice HTTP utilizzato per queste condizioni è:

```text
503 Service Unavailable
```

---

# 5. Convenzioni generali

## 5.1 Protocollo

Durante lo sviluppo locale le comunicazioni utilizzano HTTP.

Esempi:

```text
Frontend
    ↓ HTTP
Backend
```

```text
Backend
    ↓ HTTP
Python Data Agent
```

Le integrazioni con servizi esterni utilizzano HTTPS quando richiesto dal provider.

In un deployment pubblico, il backend dovrebbe essere esposto tramite HTTPS.

---

## 5.2 Formato dei payload

Le API applicative utilizzano principalmente:

```http
Content-Type: application/json
```

per request e response strutturate.

I grafici costituiscono un'eccezione perché vengono restituiti come contenuto immagine PNG.

---

## 5.3 Codifica

I payload testuali utilizzano codifica UTF-8.

Il sistema deve poter gestire correttamente contenuti in:

- italiano;
- inglese.

Questo requisito è particolarmente importante per la Chat API e per il Python Data Agent.

---

## 5.4 Naming Convention

L'implementazione finale utilizza convenzioni coerenti con l'ecosistema JavaScript/TypeScript.

I campi JSON utilizzano prevalentemente **camelCase**.

Esempi:

```text
sessionId
toolsUsed
chartUrl
```

Non viene utilizzata una conversione artificiale verso `snake_case` nel contratto tra frontend e backend.

---

## 5.5 Endpoint Naming

Gli endpoint utilizzano nomi semplici e descrittivi.

Esempi:

```text
/api/chat
/api/analysis
/api/charts/:filename
/health
```

La versione corrente non utilizza il prefisso:

```text
/api/v1
```

Il versionamento esplicito delle API potrà essere introdotto in futuro qualora vengano sviluppati contratti incompatibili.

---

## 5.6 Versionamento

Nell'implementazione corrente non viene utilizzato un versionamento esplicito tramite URL.

Pertanto:

```text
/api/chat
```

è corretto, mentre:

```text
/api/v1/chat
```

non appartiene alla versione as-built.

La decisione è coerente con lo scope del progetto, che dispone di un solo client React e di un unico contratto applicativo corrente.

Una futura versione enterprise potrebbe introdurre:

```text
/api/v1
/api/v2
```

quando necessario mantenere contemporaneamente più versioni incompatibili.

---

## 5.7 Session Identifier

Le sessioni vengono identificate tramite:

```text
sessionId
```

L'identificativo viene generato dal backend quando necessario.

Il client non deve generare:

```text
requestId
conversationId
executionId
```

per utilizzare la Chat API corrente.

---

## 5.8 Lingua

La lingua non viene dichiarata attraverso un campo dedicato della richiesta.

Il sistema rileva la lingua direttamente dal messaggio dell'utente.

Esempio:

```json
{
  "message": "Qual è il fornitore con il defect rate più alto?"
}
```

produce una risposta in italiano.

Analogamente:

```json
{
  "message": "Which supplier has the highest defect rate?"
}
```

produce una risposta in inglese.

La lingua rimane quindi una proprietà semantica del contenuto e non un parametro obbligatorio del contratto HTTP.

---

## 5.9 Date e timestamp

La Chat API corrente non richiede al frontend di inviare timestamp.

La gestione temporale necessaria ai servizi è responsabilità dei relativi componenti.

Il dataset utilizza date di produzione, ma tali date appartengono al dominio analitico e non al contratto generale della Chat API.

---

## 5.10 Paginazione

La versione corrente non espone endpoint pubblici che richiedano paginazione.

Non sono pertanto implementati parametri generali come:

```text
page
pageSize
sortBy
sortOrder
```

La paginazione può essere introdotta in futuro qualora vengano aggiunti endpoint che espongono collezioni persistenti.

---

## 5.11 Filtri analitici

Il frontend non invia direttamente un oggetto strutturato contenente filtri del Manufacturing Dataset.

La richiesta rimane in linguaggio naturale.

Esempio:

```text
Which supplier has the highest defect rate?
```

oppure:

```text
Show me the monthly defect rate trend.
```

Il Python Data Agent interpreta la richiesta attraverso il proprio Question Interpreter.

Questo mantiene l'interfaccia conversazionale indipendente dalla struttura interna del dataset.

---

# 6. Formato delle richieste e delle risposte

## 6.1 Principio generale

La versione finale non utilizza un unico envelope universale per tutte le API.

Ogni endpoint espone invece il contratto minimo necessario alla propria responsabilità.

Questo evita strutture artificiali contenenti campi che l'implementazione non utilizza, come:

```text
requestId
timestamp
executionId
metadata
language
```

quando tali informazioni non sono necessarie al client.

---

## 6.2 Chat Request

La richiesta principale del frontend utilizza la seguente struttura:

```json
{
  "message": "Which supplier has the highest defect rate?",
  "sessionId": "optional-session-id"
}
```

I campi sono:

| Campo | Tipo | Obbligatorio | Descrizione |
|------|------|-------------|-------------|
| `message` | String | Sì | Messaggio dell'utente in linguaggio naturale. |
| `sessionId` | String | No | Identificativo di una sessione già esistente. |

---

## 6.3 Nuova sessione

Per iniziare una nuova conversazione è sufficiente:

```json
{
  "message": "What is the critical defect rate threshold?"
}
```

Il backend crea automaticamente una nuova sessione.

Non è necessario inviare preventivamente un identificativo.

---

## 6.4 Sessione esistente

Per continuare una conversazione:

```json
{
  "message": "What would happen at 4.2%?",
  "sessionId": "existing-session-id"
}
```

Il backend utilizza il `sessionId` per recuperare il contesto applicativo associato.

---

## 6.5 Chat Response

La struttura della risposta è:

```json
{
  "sessionId": "session-id",
  "answer": "Generated answer",
  "toolsUsed": [
    "analyze_manufacturing_data"
  ],
  "chartUrl": "/api/charts/example.png"
}
```

Il campo:

```text
chartUrl
```

è opzionale.

---

## 6.6 Campi della Chat Response

| Campo | Tipo | Obbligatorio | Descrizione |
|------|------|-------------|-------------|
| `sessionId` | String | Sì | Identificativo della sessione corrente. |
| `answer` | String | Sì | Risposta finale prodotta dal sistema. |
| `toolsUsed` | Array of String | Sì | Tool applicativi utilizzati durante l'elaborazione. |
| `chartUrl` | String | No | URL del grafico disponibile attraverso il backend. |

---

## 6.7 `toolsUsed`

Il campo:

```text
toolsUsed
```

permette di osservare il percorso seguito dall'AI Orchestrator.

I tool principali sono:

```text
search_knowledge_base
analyze_manufacturing_data
```

Esempi:

### Risposta senza tool

```json
{
  "toolsUsed": []
}
```

### RAG

```json
{
  "toolsUsed": [
    "search_knowledge_base"
  ]
}
```

### Data Agent

```json
{
  "toolsUsed": [
    "analyze_manufacturing_data"
  ]
}
```

### Hybrid

```json
{
  "toolsUsed": [
    "search_knowledge_base",
    "analyze_manufacturing_data"
  ]
}
```

Il campo rappresenta gli strumenti effettivamente invocati e non una modalità selezionata preventivamente dal client.

---

## 6.8 Risposta RAG

Una risposta documentale può assumere una struttura come:

```json
{
  "sessionId": "session-id",
  "answer": "According to the Manufacturing Quality Policy, a defect rate above 3.5% is classified as Critical.",
  "toolsUsed": [
    "search_knowledge_base"
  ]
}
```

I riferimenti documentali vengono integrati nella risposta testuale prodotta dal modello.

La versione corrente non restituisce un array strutturato `sources` al frontend.

---

## 6.9 Risposta Data Agent

Una risposta analitica può essere rappresentata come:

```json
{
  "sessionId": "session-id",
  "answer": "SUP-07 has the highest defect rate at 2.99%.",
  "toolsUsed": [
    "analyze_manufacturing_data"
  ]
}
```

Il backend non espone al frontend l'intero payload interno restituito dal Python Data Agent.

L'AI Orchestrator utilizza il risultato analitico come input per generare la risposta finale.

---

## 6.10 Risposta con grafico

Quando l'analisi produce un grafico:

```json
{
  "sessionId": "session-id",
  "answer": "The monthly defect rate reached its highest level in April and May.",
  "toolsUsed": [
    "analyze_manufacturing_data"
  ],
  "chartUrl": "/api/charts/generated-chart.png"
}
```

Il frontend utilizza `chartUrl` per recuperare e visualizzare l'immagine.

---

## 6.11 Risposta ibrida

Una richiesta ibrida può utilizzare entrambi i tool.

Esempio concettuale:

```json
{
  "sessionId": "session-id",
  "answer": "SUP-07 has a defect rate of 2.99%. According to the Supplier Quality Procedure, this value falls within the Observation level.",
  "toolsUsed": [
    "analyze_manufacturing_data",
    "search_knowledge_base"
  ]
}
```

L'ordine degli elementi in `toolsUsed` riflette gli strumenti coinvolti ma non costituisce un contratto relativo all'ordine logico dell'esecuzione.

---

## 6.12 Separazione dagli output interni

La response pubblica non espone direttamente:

- response OpenAI completa;
- function call object;
- chunk ChromaDB;
- embedding;
- output Pandas completo;
- dataframe;
- percorsi filesystem;
- URL interno del Python Data Agent.

Il backend trasforma gli output interni in un contratto semplice utilizzabile dal frontend.

---

# 7. Gestione degli errori

## 7.1 Principio generale

La gestione degli errori è centralizzata nel backend Node.js per le richieste provenienti dal frontend.

Gli errori devono essere:

- intercettati;
- classificati;
- tradotti in status code HTTP appropriati;
- restituiti senza esporre informazioni sensibili;
- comprensibili dal frontend e dall'utente.

---

## 7.2 Input non valido

Una richiesta come:

```json
{
  "message": ""
}
```

non deve raggiungere l'AI Orchestrator.

Il backend restituisce:

```text
400 Bad Request
```

Lo stesso comportamento si applica quando `message`:

- non è presente;
- contiene soltanto whitespace;
- non soddisfa il contratto previsto.

---

## 7.3 Data Agent non disponibile

Se il backend tenta di utilizzare il Python Data Agent ma il servizio non è raggiungibile, la richiesta non viene trasformata in una risposta analitica inventata.

Il backend restituisce:

```text
503 Service Unavailable
```

con un messaggio controllato equivalente a:

```text
Manufacturing data analysis is temporarily unavailable. Please try again later.
```

Questo comportamento evita che un problema infrastrutturale venga confuso con un risultato analitico valido.

---

## 7.4 Knowledge Base non disponibile

Se la richiesta richiede il retrieval documentale e ChromaDB o la Knowledge Base non sono disponibili, il backend restituisce:

```text
503 Service Unavailable
```

con un messaggio controllato equivalente a:

```text
The company knowledge base is temporarily unavailable. Please try again later.
```

Il sistema non deve utilizzare informazioni inventate per simulare una risposta RAG.

---

## 7.5 Internal Server Error

Un errore applicativo inatteso viene gestito dal middleware centralizzato del backend.

Il client non deve ricevere direttamente:

- stack trace;
- eccezioni JavaScript;
- dettagli del client OpenAI;
- percorsi filesystem;
- variabili d'ambiente;
- API key;
- configurazione interna.

Il codice appropriato per un errore interno non classificato è:

```text
500 Internal Server Error
```

---

## 7.6 Errori del Python Data Agent

Il Data Agent utilizza FastAPI e valida le richieste ricevute dal backend.

Gli errori relativi a richieste analitiche non valide devono rimanere separati dagli errori infrastrutturali.

Esempi includono:

- richiesta non supportata;
- combinazione di più dimensioni di grouping non supportata;
- combinazione non supportata tra trend temporale e grouping;
- input non interpretabile nello scope analitico previsto.

Il Data Agent non deve eseguire automaticamente analisi differenti da quella richiesta per nascondere l'errore.

---

## 7.7 Nessuna informazione inventata

La gestione degli errori segue un principio fondamentale:

```text
Failure must not be converted into fabricated data.
```

Pertanto:

- un Data Agent non disponibile non produce KPI stimati;
- una Knowledge Base non disponibile non produce policy inventate;
- una richiesta analitica non supportata non viene trasformata silenziosamente in un'altra analisi;
- un grafico non disponibile non viene sostituito da un riferimento inesistente.

---

## 7.8 Error propagation

Il flusso generale è:

```text
Internal Dependency Error
          |
          v
Service / Connector
          |
          v
Backend Error Handling
          |
          v
Controlled HTTP Response
          |
          v
Frontend
```

Il frontend riceve quindi un errore applicativo controllato anziché il dettaglio tecnico della dipendenza che ha fallito.

---

## 7.9 Codici HTTP principali

I principali codici utilizzati dall'implementazione sono:

| HTTP | Significato | Utilizzo |
|------|-------------|----------|
| `200 OK` | Richiesta completata correttamente. | Chat, health check e analisi completate. |
| `400 Bad Request` | Input non valido. | Messaggio assente o vuoto e altre violazioni del contratto della richiesta. |
| `429 Too Many Requests` | Limite di richieste alla Chat API superato. | Protezione dell'endpoint `/api/chat` tramite rate limiting. |
| `500 Internal Server Error` | Errore applicativo inatteso. | Errore non classificato del backend. |
| `503 Service Unavailable` | Dipendenza necessaria temporaneamente non disponibile. | Data Agent, Knowledge Base o altra dipendenza critica non raggiungibile. |

Altri codici possono essere restituiti automaticamente dai framework quando applicabile, ma non costituiscono il contratto applicativo principale della versione corrente.

---

## 7.10 Resilienza delle dipendenze HTTP

Le comunicazioni HTTP del backend verso il Python Data Agent utilizzano un meccanismo condiviso di resilienza.

Le richieste dispongono di:

- timeout esplicito tramite `AbortController`;
- retry per errori di rete transitori;
- retry per risposte HTTP `5xx`;
- assenza di retry automatico per risposte HTTP `4xx`;
- backoff controllato tra i tentativi.

Lo stesso comportamento viene utilizzato sia dal client analitico sia dal Chart Client.

Il flusso può essere rappresentato come:

    Backend Request
          |
          v
    HTTP Attempt
          |
          +---- Success --------> Response
          |
          +---- Network / 5xx
          |          |
          |          v
          |       Backoff
          |          |
          |          v
          |        Retry
          |
          +---- 4xx ------------> No automatic retry
          |
          +---- Timeout --------> AbortController

Il retry non nasconde un'indisponibilità persistente. Quando i tentativi previsti non consentono di completare l'operazione, l'errore viene propagato al normale meccanismo di gestione controllata del backend.

Questa strategia riduce l'impatto di failure temporanei senza trasformare errori applicativi permanenti in retry inutili.

---

## 7.11 Frontend error handling

Quando la Chat API restituisce un errore, il frontend:

- interrompe lo stato di loading;
- mantiene utilizzabile l'interfaccia;
- mostra un messaggio di errore;
- non aggiunge una falsa risposta dell'assistente;
- consente all'utente di effettuare un nuovo tentativo.

La gestione dell'errore rimane quindi separata dal normale rendering dei messaggi conversazionali.

---

# 8. Health Check API

## 8.1 Panoramica

Maranello AI espone endpoint di health check per verificare rapidamente la disponibilità dei principali servizi applicativi.

Gli health check implementati riguardano:

- backend Node.js;
- Python Data Agent.

ChromaDB viene utilizzato come dipendenza infrastrutturale del modulo RAG, ma non viene esposto al frontend attraverso un health endpoint applicativo dedicato.

---

## 8.2 Backend Health Check

Il backend Node.js espone:

```http
GET /health
```

L'endpoint permette di verificare che il processo Express sia attivo e in grado di rispondere alle richieste HTTP.

Esempio di utilizzo locale:

```text
http://localhost:3000/health
```

Il controllo può essere utilizzato durante:

- sviluppo locale;
- troubleshooting;
- test di integrazione;
- verifica dell'avvio del servizio;
- future configurazioni di monitoring.

Il successo della richiesta indica la disponibilità del processo backend.

---

## 8.3 Data Agent Health Check

Il Python Data Agent espone:

```http
GET /health
```

sul proprio servizio FastAPI.

In ambiente locale:

```text
http://127.0.0.1:8001/health
```

L'endpoint consente di verificare la disponibilità del microservizio analitico senza avviare un'analisi completa.

Il backend può utilizzare questa informazione durante attività di troubleshooting o test, mentre il frontend non comunica direttamente con tale endpoint.

---

## 8.4 Separazione tra health e dependency availability

Un health check positivo del backend non implica necessariamente che tutte le dipendenze siano disponibili.

Ad esempio:

```text
Backend
    -> available

Python Data Agent
    -> unavailable
```

oppure:

```text
Backend
    -> available

ChromaDB
    -> unavailable
```

In entrambi i casi il processo Node.js può continuare a rispondere a `/health`, mentre una richiesta che necessita della dipendenza non disponibile può produrre:

```text
503 Service Unavailable
```

Questa separazione permette di distinguere:

- disponibilità del processo applicativo;
- disponibilità funzionale delle dipendenze.

---

## 8.5 Utilizzo nei test

Gli health endpoint vengono utilizzati per verificare che i servizi necessari siano avviati prima dei test end-to-end.

Il flusso locale può essere verificato attraverso:

```text
Node.js Backend
GET /health

Python Data Agent
GET /health

ChromaDB
service availability
```

Una volta disponibili i servizi, è possibile eseguire le richieste conversazionali complete attraverso il backend.

---

# 9. Backend API

## 9.1 Panoramica

Il backend Node.js rappresenta il punto di ingresso applicativo principale di Maranello AI.

Il frontend React comunica esclusivamente con questo componente.

Le principali responsabilità del backend sono:

- esposizione delle API utilizzate dal frontend;
- validazione degli input;
- gestione delle sessioni conversazionali;
- integrazione con OpenAI Responses API;
- esecuzione del ciclo di function calling;
- coordinamento del sistema RAG;
- comunicazione con il Python Data Agent;
- trasformazione dei riferimenti ai grafici;
- gestione centralizzata degli errori.

Il backend non esegue direttamente le analisi quantitative sul dataset e non implementa internamente il vector database.

---

## 9.2 Base URL locale

Durante lo sviluppo il backend viene eseguito sulla porta:

```text
3000
```

La base URL locale è quindi:

```text
http://127.0.0.1:3000
```

oppure, in modo equivalente:

```text
http://localhost:3000
```

Gli endpoint applicativi utilizzano il prefisso:

```text
/api
```

quando appartengono all'API utilizzata dal frontend.

---

## 9.3 Endpoint implementati

Gli endpoint principali del backend sono:

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `GET` | `/health` | Verifica la disponibilità del backend. |
| `POST` | `/api/chat` | Gestisce una richiesta conversazionale. |
| `GET` | `/api/charts/:filename` | Recupera un grafico tramite Chart Proxy. |

La versione finale non implementa endpoint pubblici dedicati a:

```text
GET /conversations/:id
DELETE /conversations/:id
GET /capabilities
```

La gestione della conversazione avviene internamente attraverso il `ConversationManager` e il `sessionId`.

---

## 9.4 Responsabilità del Backend API Layer

L'API layer riceve le richieste HTTP e delega l'elaborazione ai componenti applicativi appropriati.

Il flusso generale è:

```text
HTTP Request
    |
    v
Express Route
    |
    v
Controller / Service
    |
    v
Conversation + AI Orchestration
    |
    v
HTTP Response
```

La logica di business non viene concentrata direttamente nei route handler.

Questa separazione facilita:

- testing;
- gestione degli errori;
- manutenzione;
- evoluzione delle route;
- riutilizzo dei servizi applicativi.

---

## 9.5 Configurazione

Il backend Node.js utilizza configurazione tramite environment variables.

Le principali variabili supportate sono:

| Variabile | Default | Obbligatoria | Descrizione |
|-----------|---------|--------------|-------------|
| `NODE_ENV` | `development` | No | Ambiente applicativo. |
| `PORT` | `3000` | No | Porta HTTP del backend. |
| `DATA_AGENT_URL` | `http://127.0.0.1:8001` | No | Base URL del Python Data Agent. |
| `CHROMA_URL` | `http://127.0.0.1:8000` | No | URL del servizio ChromaDB. |
| `CHROMA_COLLECTION` | `maranello_ai_knowledge_base` | No | Collection utilizzata dal modulo RAG. |
| `OPENAI_API_KEY` | Nessuno | **Sì** | Credenziale utilizzata per accedere al provider OpenAI. |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | No | Modello utilizzato per gli embedding. |
| `LLM_MODEL` | `gpt-5-mini` | No | Modello utilizzato dall'AI Orchestrator. |
| `LLM_TEMPERATURE` | `0.0` | No | Temperatura configurata per il modello. |
| `LLM_TIMEOUT_SECONDS` | `30` | No | Timeout applicativo configurato per le operazioni LLM. |
| `CHAT_RATE_LIMIT_WINDOW_MINUTES` | `15` | No | Durata della finestra del rate limiter della Chat API. |
| `CHAT_RATE_LIMIT_MAX_REQUESTS` | `30` | No | Numero massimo di richieste consentite nella finestra configurata. |

`OPENAI_API_KEY` è l'unica variabile della tabella priva di un valore applicativo di fallback.

Durante l'inizializzazione il backend verifica che la chiave:

- sia presente;
- non sia una stringa vuota;
- non contenga esclusivamente whitespace.

Se il requisito non è soddisfatto, la configurazione fallisce immediatamente invece di consentire l'avvio di un backend incapace di utilizzare le funzionalità AI.

Il comportamento è intenzionale e segue un principio di **fail-fast configuration validation**.

Le variabili di rate limiting consentono invece di modificare la protezione di:

    POST /api/chat

senza modificare il codice applicativo.

La configurazione reale viene mantenuta fuori dal repository tramite `.env`.

I file `.env.example` documentano le variabili supportate senza contenere credenziali reali.

---

## 9.6 Dipendenze principali

Il backend comunica con:

| Dipendenza | Utilizzo |
|------------|----------|
| OpenAI API | Orchestrazione, generazione della risposta e function calling. |
| ChromaDB | Retrieval semantico della Knowledge Base. |
| Python Data Agent | Analisi quantitativa del Manufacturing Dataset. |

Il frontend rimane indipendente dalla disponibilità e dalla posizione di queste dipendenze.

---

# 10. Chat API

## 10.1 Endpoint

L'endpoint principale dell'applicazione è:

```http
POST /api/chat
```

Il suo obiettivo è ricevere una domanda in linguaggio naturale e restituire una risposta generata da Maranello AI.

---

## 10.2 Content Type

La richiesta utilizza:

```http
Content-Type: application/json
```

---

## 10.3 Request Body

La struttura della richiesta è:

```json
{
  "message": "Which supplier has the highest defect rate?",
  "sessionId": "optional-existing-session-id"
}
```

I campi supportati sono:

| Campo | Tipo | Obbligatorio | Descrizione |
|------|------|-------------|-------------|
| `message` | String | Sì | Testo della richiesta dell'utente. |
| `sessionId` | String | No | Identificativo della sessione esistente. |

Il client non invia direttamente:

- intent;
- tool;
- lingua;
- cronologia completa;
- tipo di analisi;
- filtri strutturati;
- execution mode.

---

## 10.4 Prima richiesta

La prima interazione può essere inviata senza `sessionId`.

Esempio:

```json
{
  "message": "Which supplier has the highest defect rate?"
}
```

Il backend:

1. valida il messaggio;
2. crea una nuova sessione;
3. genera un UUID;
4. invoca l'AI Orchestrator;
5. memorizza il risultato;
6. restituisce il nuovo `sessionId`.

---

## 10.5 Richiesta successiva

Le richieste successive possono riutilizzare il valore restituito.

Esempio:

```json
{
  "message": "What would happen if that supplier reached 3.2%?",
  "sessionId": "existing-session-id"
}
```

Il backend recupera lo stato della sessione e l'identificativo della precedente risposta OpenAI.

La continuazione con OpenAI utilizza logicamente:

```text
lastResponseId
       |
       v
previous_response_id
```

Questo consente al modello di risolvere riferimenti contestuali come:

```text
that supplier
```

senza richiedere al frontend di reinviare manualmente l'intera cronologia.

---

## 10.6 Validazione della richiesta

Il campo `message` deve contenere testo valido.

Sono rifiutate richieste con:

- campo assente;
- stringa vuota;
- stringa composta esclusivamente da whitespace.

Esempio non valido:

```json
{
  "message": "   "
}
```

Il backend restituisce:

```text
400 Bad Request
```

prima di invocare OpenAI.

---

## 10.7 Autonomous Tool Selection

Dopo la validazione, la richiesta viene inoltrata all'AI Orchestrator.

Il modello può selezionare:

```text
search_knowledge_base
```

oppure:

```text
analyze_manufacturing_data
```

oppure entrambi.

Il backend non utilizza un campo `executionType` fornito dal client per scegliere il percorso.

---

## 10.8 Tool: `search_knowledge_base`

Questo tool viene utilizzato quando la richiesta richiede informazioni presenti nella Knowledge Base.

Esempi:

    What is the critical defect rate threshold?

oppure:

    Secondo la Supplier Quality Procedure, cosa succede sopra il 4%?

Il backend esegue il retrieval tramite il modulo RAG.

ChromaDB restituisce un insieme di candidati semanticamente vicini alla query. Prima che questi risultati vengano utilizzati come contesto documentale, il `RetrieverService` applica un filtro di rilevanza basato sulla distanza restituita dal vector database.

La configurazione corrente utilizza:

    maxDistance = 0.70

I candidati con distanza superiore a `0.70` vengono esclusi.

Vengono inoltre esclusi risultati per i quali la distanza sia assente o non valida.

Il flusso può essere rappresentato come:

    User Query
        |
        v
    Query Embedding
        |
        v
    ChromaDB Top-K Candidates
        |
        v
    Distance Filtering
        |
        | maxDistance <= 0.70
        v
    Relevant Chunks
        |
        v
    function_call_output
        |
        v
    OpenAI Response

Il retrieval può quindi restituire anche **zero chunk** quando nessun candidato supera il criterio minimo di rilevanza.

Questo comportamento è intenzionale: il sistema evita di utilizzare automaticamente il nearest neighbor disponibile quando la sua similarità semantica non è sufficientemente forte da costituire un grounding affidabile.

La soglia `0.70` è stata calibrata empiricamente sul corpus documentale e sull'embedding model utilizzati da Maranello AI attraverso query:

- pertinenti in inglese;
- pertinenti in italiano;
- borderline;
- chiaramente estranee al dominio della Knowledge Base.

La soglia non viene considerata un valore universale. Un cambiamento significativo del corpus, della strategia di chunking o dell'embedding model richiederebbe una nuova calibrazione.

I chunk accettati vengono restituiti a OpenAI come:

    function_call_output

Il modello utilizza quindi esclusivamente il contesto documentale considerato sufficientemente pertinente per generare la risposta finale.

---

## 10.9 Tool: `analyze_manufacturing_data`

Questo tool viene utilizzato quando la richiesta richiede calcoli sul Manufacturing Dataset.

Esempi:

```text
Which supplier has the highest defect rate?
```

```text
Show me the monthly defect rate trend.
```

Il backend invoca:

```http
POST /api/analysis
```

sul Python Data Agent.

Il risultato analitico viene quindi fornito nuovamente al modello come output della tool call.

---

## 10.10 Richieste ibride

Il modello può invocare più tool nella stessa richiesta.

Esempio:

```text
Which supplier has the highest defect rate,
and according to the Supplier Quality Procedure,
what action should be taken?
```

In questo scenario vengono utilizzati:

```text
analyze_manufacturing_data
search_knowledge_base
```

Il backend può eseguire tool indipendenti in parallelo quando possibile.

I risultati vengono successivamente inviati al modello per la sintesi finale.

---

## 10.11 Tool execution loop

L'orchestrazione non è limitata necessariamente a una singola tool call.

Il flusso logico è:

    User Message
        |
        v
    OpenAI Response
        |
        +---- Final Answer
        |
        +---- Function Call
                  |
                  v
             Tool Execution
                  |
                  v
         function_call_output
                  |
                  v
             OpenAI Response

Il ciclo prosegue fino a quando:

- il modello restituisce una risposta finale;
- si verifica un errore che interrompe l'elaborazione;
- viene raggiunto il limite massimo di tool round previsto dal backend.

L'implementazione definisce:

    MAX_TOOL_ROUNDS = 5

Un **tool round** rappresenta un ciclo nel quale il modello richiede l'esecuzione di uno o più tool e il backend restituisce i relativi `function_call_output`.

Il backend consente quindi l'esecuzione di un massimo di cinque tool round per singola richiesta conversazionale.

Se, dopo il quinto round, il modello richiede un ulteriore ciclo di tool calling, l'orchestrazione viene interrotta con un errore controllato invece di proseguire indefinitamente.

Il limite costituisce un application boundary intenzionale che protegge il sistema da:

- loop agentici non terminanti;
- consumo incontrollato di chiamate verso il provider AI;
- esecuzioni ripetute dei servizi interni;
- crescita non controllata della latenza della richiesta.

La decisione non modifica il principio di **LLM-driven routing**: il modello continua a decidere autonomamente quali tool utilizzare e quando utilizzarli, ma opera entro un limite esplicito definito dall'applicazione.

---

## 10.12 Chat Response

Quando l'orchestrazione termina correttamente, la Chat API restituisce una response JSON con il seguente contratto pubblico:

    {
      "sessionId": "string",
      "answer": "string",
      "toolsUsed": [
        "string"
      ],
      "chartUrl": "string | null"
    }

### Campi

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `sessionId` | `string` | Identificativo della conversazione corrente. |
| `answer` | `string` | Risposta finale generata dall'AI Orchestrator. |
| `toolsUsed` | `string[]` | Tool applicativi effettivamente utilizzati durante l'orchestrazione. |
| `chartUrl` | `string \| null` | URL backend del grafico quando l'analisi ne produce uno; altrimenti `null`. |

Il contratto pubblico rimane intenzionalmente separato dai metadati interni di osservabilità.

In particolare, il backend raccoglie internamente informazioni come:

    requestId
    tokenUsage
    latency
    statusCode

ma questi valori non vengono aggiunti automaticamente al body JSON della Chat Response.

Il `requestId` viene invece esposto attraverso l'header HTTP:

    X-Request-Id

Esempio concettuale:

    HTTP/1.1 200 OK
    X-Request-Id: <request-id>
    Content-Type: application/json

    {
      "sessionId": "<session-id>",
      "answer": "...",
      "toolsUsed": [
        "search_knowledge_base"
      ],
      "chartUrl": null
    }

La distinzione tra `sessionId` e `requestId` è intenzionale:

- `sessionId` identifica la conversazione e può essere riutilizzato tra più richieste;
- `requestId` identifica una singola richiesta HTTP ed è utilizzato per osservabilità e troubleshooting.

Il token usage non fa parte del contratto pubblico:

    tokenUsage

rimane un metadato interno dell'orchestrazione e viene utilizzato dal livello di osservabilità del backend.

Questa separazione evita di accoppiare il frontend a informazioni operative e consente di evolvere logging, metriche e monitoraggio senza modificare inutilmente il contratto della Chat API.

### Esempio con Data Agent e grafico

    {
      "sessionId": "<session-id>",
      "answer": "The monthly defect rate...",
      "toolsUsed": [
        "analyze_manufacturing_data"
      ],
      "chartUrl": "/api/charts/monthly_defect_rate_<unique-id>.png"
    }

### Esempio con RAG

    {
      "sessionId": "<session-id>",
      "answer": "According to the Manufacturing Quality Policy...",
      "toolsUsed": [
        "search_knowledge_base"
      ],
      "chartUrl": null
    }

La presenza di `toolsUsed` permette al frontend e ai test di conoscere il percorso applicativo seguito senza esporre i dettagli interni delle function call del provider AI.

---

## 10.13 Esempio RAG

Request:

```json
{
  "message": "What is the critical defect rate threshold?"
}
```

Response concettuale:

```json
{
  "sessionId": "generated-session-id",
  "answer": "According to the Manufacturing Quality Policy, a defect rate above 3.5% is classified as Critical.",
  "toolsUsed": [
    "search_knowledge_base"
  ]
}
```

---

## 10.14 Esempio Data Agent

Request:

```json
{
  "message": "Which supplier has the highest defect rate?"
}
```

Response concettuale:

```json
{
  "sessionId": "generated-session-id",
  "answer": "SUP-07 has the highest defect rate at 2.99%.",
  "toolsUsed": [
    "analyze_manufacturing_data"
  ]
}
```

---

## 10.15 Esempio con grafico

Request:

```json
{
  "message": "Show me the monthly defect rate trend."
}
```

Response concettuale:

```json
{
  "sessionId": "generated-session-id",
  "answer": "The monthly defect rate reached its highest value in April and May and its lowest value in August.",
  "toolsUsed": [
    "analyze_manufacturing_data"
  ],
  "chartUrl": "/api/charts/generated-chart.png"
}
```

Il filename è generato dinamicamente e può cambiare tra esecuzioni.

---

## 10.16 Aggiornamento della sessione

Lo stato conversazionale viene aggiornato solamente dopo il completamento corretto della richiesta.

Il flusso è:

```text
Validate Request
      |
      v
AI Orchestration
      |
      v
Tool Execution
      |
      v
Final Answer
      |
      v
Update Session
```

Se l'elaborazione fallisce prima della produzione della risposta finale, il backend evita di salvare uno stato conversazionale parziale.

---

## 10.17 Risposta e lingua

La lingua della risposta viene determinata dal contenuto della richiesta.

Esempio:

```text
Qual è il defect rate di SUP-07?
```

produce una risposta in italiano.

```text
What is the defect rate of SUP-07?
```

produce una risposta in inglese.

Non è necessario inviare:

```json
{
  "language": "it"
}
```

o:

```json
{
  "language": "en"
}
```

---

# 11. Chart Proxy API

## 11.1 Panoramica

I grafici analitici vengono generati dal Python Data Agent tramite Matplotlib.

Il frontend non accede direttamente al servizio Python.

Il backend espone quindi un endpoint proxy dedicato.

La scelta del Chart Proxy costituisce una decisione architetturale intenzionale per mantenere il frontend disaccoppiato dal microservizio Python.

---

## 11.2 Endpoint

Il frontend recupera un grafico tramite:

```http
GET /api/charts/:filename
```

Il parametro:

```text
filename
```

identifica il file PNG generato dal Data Agent.

---

## 11.3 Flusso

Il flusso è:

```text
React Frontend
      |
      | GET /api/charts/:filename
      v
Node.js Backend
      |
      | validate filename
      |
      | GET /charts/:filename
      v
Python Data Agent
      |
      v
PNG Image
      |
      v
Node.js Backend
      |
      v
React Frontend
```

Il servizio Python espone internamente i file attraverso:

```http
GET /charts/:filename
```

mentre il frontend utilizza esclusivamente l'endpoint Node.js. Questo comportamento è coerente anche con l'architettura generale as-built documentata nel SAD. 

---

## 11.4 Riscrittura del riferimento

Il Python Data Agent può restituire un riferimento simile a:

```text
/charts/generated-file.png
```

Il backend lo trasforma nel riferimento pubblico:

```text
/api/charts/generated-file.png
```

La Chat API può quindi includere:

```json
{
  "chartUrl": "/api/charts/generated-file.png"
}
```

Il frontend non necessita di conoscere:

- `DATA_AGENT_URL`;
- porta `8001`;
- filesystem del Data Agent;
- directory utilizzata per i file generati.

---

## 11.5 Validazione del filename

Prima di inoltrare la richiesta, il backend valida il nome del file.

L'obiettivo è evitare l'utilizzo del parametro come percorso arbitrario.

Richieste che tentano di utilizzare:

```text
../
```

o altre forme di path traversal devono essere rifiutate.

Il proxy deve poter recuperare esclusivamente file appartenenti al formato previsto per i grafici generati.

---

## 11.6 Response

In caso di successo l'endpoint restituisce il contenuto dell'immagine PNG.

Il comportamento può essere rappresentato come:

```text
HTTP 200
Content-Type: image/png
```

Il frontend visualizza quindi direttamente l'immagine all'interno del messaggio dell'assistente.

---

## 11.7 Grafico non disponibile e resilienza del Chart Client

Quando il frontend richiede un grafico, il backend non accede direttamente al filesystem del Python Data Agent.

Il `ChartClient` effettua una richiesta HTTP verso il servizio Python utilizzando lo stesso meccanismo condiviso di resilienza adottato dal `DataAgentClient`.

La richiesta dispone di:

- timeout esplicito tramite `AbortController`;
- retry per errori di rete transitori;
- retry per risposte HTTP `5xx`;
- backoff controllato tra i tentativi;
- nessun retry automatico per risposte HTTP `4xx`.

Il flusso può essere rappresentato come:

    Frontend
       |
       v
    GET /api/charts/:filename
       |
       v
    Backend Chart Proxy
       |
       v
    Filename Validation
       |
       v
    ChartClient
       |
       v
    HTTP Attempt
       |
       +---- Success ---------> Stream PNG
       |
       +---- Network / 5xx
       |          |
       |          v
       |       Backoff
       |          |
       |          v
       |        Retry
       |
       +---- 4xx -------------> No automatic retry
       |
       +---- Timeout ---------> AbortController

Se il grafico rimane non disponibile dopo la gestione prevista dal client, il backend propaga l'errore attraverso il normale meccanismo di gestione controllata.

Il retry è limitato alle condizioni considerate potenzialmente transitorie e non viene utilizzato per trasformare errori client permanenti in tentativi ripetuti.

La validazione del filename rimane precedente all'accesso al servizio Python, preservando la protezione contro path traversal e riferimenti non validi.

---

## 11.8 Runtime artifacts e retention

I grafici PNG sono artefatti runtime.

Non fanno parte del codice sorgente e non vengono versionati nel repository.

Il Data Agent genera filename univoci per evitare collisioni tra richieste differenti.

Il lifecycle dei grafici è gestito dal Python Data Agent attraverso `ChartCleanupService`.

La configurazione predefinita utilizza:

    chart_retention_hours = 24.0
    chart_cleanup_interval_minutes = 60.0

Il cleanup viene eseguito:

1. durante l'avvio del Data Agent;
2. periodicamente durante il lifecycle dell'applicazione;
3. con cancellazione controllata del background task durante lo shutdown.

Il servizio elimina esclusivamente i file runtime che rispettano il pattern gestito:

    monthly_defect_rate_*.png

e che hanno superato il periodo di retention configurato.

Il Chart Proxy non è responsabile della cancellazione dei file.

La separazione delle responsabilità è quindi:

    Python Data Agent
        |
        +---- Generate PNG
        |
        +---- Store Runtime Artifact
        |
        +---- Apply Retention Policy
        |
        v
    Backend Chart Proxy
        |
        +---- Validate Filename
        |
        +---- Retrieve Chart Resiliently
        |
        v
    React Frontend

Questa separazione mantiene il backend Node.js indipendente dal filesystem del Data Agent e impedisce contemporaneamente l'accumulo indefinito dei grafici generati.

In un deployment distribuito, lo storage locale potrebbe essere sostituito da object storage o blob storage senza modificare il contratto pubblico:

    GET /api/charts/:filename

---

# 12. Python Data Agent API

## 12.1 Panoramica

Il Python Data Agent rappresenta il microservizio analitico di Maranello AI.

Il servizio è implementato tramite:

- Python;
- FastAPI;
- Pandas;
- Matplotlib.

Il suo scopo è ricevere richieste analitiche dal backend Node.js, interpretarle attraverso una logica controllata e applicare operazioni deterministiche sul Manufacturing Dataset.

Il servizio non genera la risposta conversazionale finale destinata all'utente.

La responsabilità è invece suddivisa nel seguente modo:

```text
Python Data Agent
    -> computes facts, KPIs and analytical results

AI Orchestrator
    -> communicates the results to the user
```

Questa separazione mantiene distinta la produzione dei fatti numerici dalla generazione del linguaggio naturale.

---

## 12.2 Responsabilità

Il Data Agent è responsabile di:

- caricamento del Manufacturing Dataset;
- data cleaning;
- normalizzazione dei valori;
- gestione dei record duplicati;
- gestione delle anomalie previste nel dataset;
- interpretazione della richiesta analitica;
- calcolo dei KPI;
- aggregazioni per dimensione;
- analisi temporali;
- produzione di una sintesi analitica;
- generazione di grafici;
- esposizione dei grafici generati;
- health check del servizio.

Non è responsabile di:

- gestione delle conversazioni;
- retrieval della Knowledge Base;
- accesso a ChromaDB;
- scelta autonoma tra RAG e Data Agent;
- generazione della risposta conversazionale finale;
- gestione del frontend.

---

## 12.3 Base URL

Durante lo sviluppo locale il servizio utilizza la porta:

```text
8001
```

La base URL è:

```text
http://127.0.0.1:8001
```

oppure:

```text
http://localhost:8001
```

Il backend configura l'indirizzo attraverso la variabile:

```text
DATA_AGENT_URL
```

Esempio:

```text
DATA_AGENT_URL=http://127.0.0.1:8001
```

Il frontend non utilizza direttamente questo URL.

---

## 12.4 Endpoint implementati

Gli endpoint principali del Python Data Agent sono:

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `GET` | `/` | Verifica di base della disponibilità del servizio. |
| `GET` | `/health` | Health check del Data Agent. |
| `POST` | `/api/analysis` | Esegue un'analisi sul Manufacturing Dataset. |
| `GET` | `/charts/:filename` | Espone un grafico PNG precedentemente generato. |

La versione finale non implementa endpoint separati come:

```text
/api/v1/kpis/calculate
/api/v1/charts/generate
/api/v1/tables/generate
/api/v1/insights/generate
/api/v1/dataset/validate
/api/v1/dataset/metadata
```

Le relative responsabilità vengono gestite internamente dal servizio analitico oppure non appartengono allo scope finale.

---

## 12.5 Endpoint principale

L'endpoint analitico utilizzato dal backend è:

```http
POST /api/analysis
```

Questo endpoint riceve una richiesta analitica in linguaggio naturale.

L'AI Orchestrator non invia codice Python da eseguire.

Il Data Agent interpreta invece la richiesta e seleziona una delle analisi supportate.

---

## 12.6 Flusso della richiesta analitica

Il flusso logico è:

```text
Backend
   |
   | POST /api/analysis
   v
FastAPI
   |
   v
Request Validation
   |
   v
Question Interpreter
   |
   v
Analytics Engine
   |
   +---- KPI Calculation
   |
   +---- Grouped Analysis
   |
   +---- Monthly Trend
   |
   +---- Chart Generation
   |
   v
Structured Analysis Result
   |
   v
Backend
```

Il backend fornisce successivamente il risultato all'AI Orchestrator come output della tool call.

---

## 12.7 Request analitica

La richiesta contiene la domanda analitica necessaria al Data Agent.

Esempio concettuale:

```json
{
  "question": "Which supplier has the highest defect rate?"
}
```

oppure:

```json
{
  "question": "Show me the monthly defect rate trend."
}
```

La richiesta rimane intenzionalmente semplice.

Il backend non deve costruire manualmente strutture complesse contenenti:

- metriche;
- dimensioni;
- filtri;
- group by;
- sort;
- analysis type;
- chart configuration.

Questi elementi vengono determinati internamente dal Question Interpreter sulla base della domanda.

---

## 12.8 Question Interpreter

Il Question Interpreter converte la richiesta naturale in un'operazione analitica supportata.

La logica è deterministica.

Le principali categorie riconosciute sono:

- KPI globali;
- analisi per supplier;
- analisi per production line;
- analisi per shift;
- analisi per component category;
- analisi per vehicle model;
- analisi per plant;
- analisi per operator team;
- monthly defect rate trend.

Il sistema supporta richieste sia in italiano sia in inglese.

---

## 12.9 KPI globali

Il Data Agent può calcolare i seguenti KPI globali:

| KPI | Descrizione |
|-----|-------------|
| `total_production` | Totale delle unità prodotte. |
| `total_defective_units` | Totale delle unità difettose. |
| `defect_rate` | Percentuale complessiva di unità difettose. |
| `rework_rate` | Percentuale di unità sottoposte a rilavorazione. |
| `scrap_rate` | Percentuale di unità scartate. |
| `average_quality_score` | Quality score medio. |
| `average_downtime_minutes` | Downtime medio in minuti. |
| `average_cycle_time_seconds` | Cycle time medio in secondi. |

L'Analytics Engine utilizza Pandas per eseguire i calcoli sui dati puliti.

---

## 12.10 Analisi per dimensione

Il sistema può confrontare il defect rate per le seguenti dimensioni:

- `production_line`;
- `shift`;
- `supplier_id`;
- `component_category`;
- `vehicle_model`;
- `plant`;
- `operator_team`.

Esempio:

```text
Which production line has the highest defect rate?
```

Il sistema:

1. identifica `production_line` come dimensione;
2. aggrega unità prodotte e difettose;
3. calcola il defect rate;
4. ordina i risultati;
5. produce una sintesi.

---

## 12.11 Supplier Analysis

Una richiesta come:

```text
Which supplier has the highest defect rate?
```

viene interpretata come analisi per:

```text
supplier_id
```

Il risultato può evidenziare, ad esempio, il supplier con il valore più elevato nel dataset.

Il Data Agent restituisce esclusivamente il dato analitico.

L'interpretazione rispetto alle policy aziendali rimane responsabilità del RAG e dell'AI Orchestrator.

Pertanto:

```text
Supplier defect rate
        |
        v
Data Agent
```

e:

```text
Supplier quality threshold
        |
        v
Knowledge Base / RAG
```

sono due responsabilità separate.

---

## 12.12 Analisi temporale

Il Data Agent supporta il calcolo del:

```text
monthly defect rate trend
```

L'analisi aggrega i record sulla base del mese di produzione.

Il risultato permette di osservare l'andamento del defect rate nel periodo coperto dal dataset.

Una richiesta tipica è:

```text
Show me the monthly defect rate trend.
```

oppure:

```text
Mostrami l'andamento mensile del defect rate.
```

---

## 12.13 Generazione e retention dei grafici

Quando l'analisi supporta una rappresentazione grafica, il Data Agent può generare un'immagine PNG.

Il processo è:

    Analytical Result
          |
          v
    Matplotlib
          |
          v
    PNG Generation
          |
          v
    Unique Filename
          |
          v
    Runtime Chart Directory
          |
          v
    Chart Reference

Matplotlib viene utilizzato in modalità non interattiva.

I file generati sono artefatti runtime e non vengono versionati nel repository.

Per evitare una crescita indefinita della directory dei grafici, il Data Agent implementa una policy automatica di retention tramite `ChartCleanupService`.

La configurazione predefinita utilizza:

    chart_retention_hours = 24.0
    chart_cleanup_interval_minutes = 60.0

Di conseguenza, i grafici runtime appartenenti al pattern gestito dal servizio possono essere eliminati quando superano le 24 ore di età.

Il cleanup viene eseguito:

1. una prima volta durante l'avvio del Data Agent;
2. successivamente attraverso un task periodico eseguito durante il lifecycle dell'applicazione;
3. con intervallo predefinito di 60 minuti.

Il task periodico viene cancellato in modo controllato durante lo shutdown del servizio.

Le operazioni di scansione e rimozione dei file vengono eseguite senza bloccare il normale event loop dell'applicazione FastAPI.

Il cleanup è intenzionalmente limitato ai grafici generati dal Data Agent che rispettano il pattern:

    monthly_defect_rate_*.png

Il servizio non effettua quindi una cancellazione indiscriminata dei file presenti nella directory runtime.

Sono inoltre gestite condizioni quali:

- directory dei grafici non ancora esistente;
- file già rimosso durante il cleanup;
- configurazioni di retention o intervallo non valide.

Il lifecycle complessivo è:

    Data Agent Startup
          |
          v
    Immediate Cleanup
          |
          v
    Application Running
          |
          +---- Generate Runtime Charts
          |
          +---- Periodic Cleanup
          |         |
          |         v
          |    Remove Expired Charts
          |
          v
    Controlled Shutdown
          |
          v
    Cancel Cleanup Task

Questa strategia mantiene semplice la generazione server-side dei grafici e impedisce contemporaneamente l'accumulo indefinito degli artefatti runtime.

---

## 12.14 Chart Reference

Quando viene prodotto un grafico, il risultato analitico contiene un riferimento all'immagine.

Concettualmente:

```text
/charts/generated-chart.png
```

Il backend intercetta il riferimento e lo trasforma in:

```text
/api/charts/generated-chart.png
```

prima di restituirlo al frontend.

Il Data Agent non deve conoscere l'URL pubblico utilizzato dal browser.

---

## 12.15 Endpoint dei grafici

Il Python Data Agent espone i grafici tramite:

```http
GET /charts/:filename
```

L'endpoint restituisce il file PNG richiesto.

Non viene utilizzato direttamente dal frontend.

Il flusso effettivo è:

```text
Frontend
   |
   | GET /api/charts/:filename
   v
Node Backend
   |
   | GET /charts/:filename
   v
Python Data Agent
```

---

## 12.16 Data Cleaning e DatasetRepository

Il Manufacturing Dataset viene gestito attraverso un componente dedicato denominato `DatasetRepository`.

Il repository incapsula:

- caricamento del CSV;
- data cleaning;
- preparazione del DataFrame;
- caching del dataset preparato;
- reload esplicito della sorgente.

La pipeline di cleaning comprende:

- rimozione dei duplicati esatti;
- normalizzazione dei valori testuali;
- normalizzazione dei turni;
- normalizzazione delle linee produttive;
- normalizzazione degli identificativi dei supplier;
- parsing delle date in formato misto;
- gestione dei quality score fuori intervallo;
- preservazione controllata dei valori mancanti;
- identificazione dei record con relazioni numeriche incoerenti;
- gestione delle anomalie intenzionalmente presenti nel dataset.

La pulizia viene applicata in modo deterministico e riproducibile.

Il dataset preparato non viene tuttavia ricostruito a ogni richiesta `POST /api/analysis`.

Il caricamento utilizza una strategia **lazy per processo**:

    First Analysis Request
            |
            v
    DatasetRepository.get()
            |
            v
    Cache available?
       /         \
     No           Yes
     |             |
     v             |
    Load CSV       |
     |             |
     v             |
    Clean Data     |
     |             |
     v             |
    Cache Prepared DataFrame
       \          /
        \        /
         v      v
       Analysis

Alla prima analisi il repository:

1. legge il Manufacturing Dataset;
2. esegue la pipeline di cleaning;
3. memorizza il DataFrame preparato in memoria.

Le richieste successive riutilizzano il dataset preparato senza ripetere `pd.read_csv` e l'intera pipeline di cleaning.

Questo elimina il costo di I/O e preparazione precedentemente associato a ogni richiesta analitica.

Il repository espone inoltre un'operazione esplicita di `reload()` per ricostruire la cache quando necessario.

Il reload viene gestito in modo transazionale: se il nuovo caricamento o cleaning fallisce, il dataset precedentemente disponibile rimane utilizzabile invece di sostituire la cache con uno stato non valido.

Il repository protegge inoltre il DataFrame memorizzato da modifiche accidentali da parte delle analisi consumer.

---

## 12.17 Dataset read-only e lifecycle

Il Manufacturing Dataset viene utilizzato come sorgente analitica in sola lettura.

Il Data Agent:

- legge il CSV sorgente quando il `DatasetRepository` deve inizializzare o ricaricare la cache;
- normalizza i dati in memoria;
- conserva il dataset preparato per le analisi successive;
- calcola risultati senza modificare il file CSV sorgente.

Le normali richieste analitiche sono quindi prive di effetti persistenti sul dataset.

Il lifecycle può essere sintetizzato come:

    Source CSV
        |
        v
    Load + Clean
        |
        v
    Prepared In-Memory Dataset
        |
        +---- Analysis Request 1
        |
        +---- Analysis Request 2
        |
        +---- Analysis Request N
        |
        +---- Explicit reload()
                    |
                    v
               Load + Clean
                    |
                    v
             Refreshed Cache

La cache è locale al processo del Python Data Agent e non costituisce una persistenza distribuita.

Per il dataset corrente, composto da circa 2.000 record, questo approccio mantiene Pandas semplice ed efficace eliminando al tempo stesso il caricamento ripetuto per richiesta.

Per volumi significativamente maggiori, il livello di accesso ai dati potrebbe essere sostituito da un motore query-oriented senza modificare il contratto HTTP del Data Agent.

---

## 12.18 No Arbitrary Code Execution

Il Data Agent non esegue codice Python arbitrario generato dall'LLM.

Non viene utilizzato un flusso del tipo:

```text
User Question
    |
    v
LLM generates Python
    |
    v
exec(...)
```

L'approccio adottato è invece:

```text
User Question
    |
    v
LLM chooses Data Agent
    |
    v
Question Interpreter
    |
    v
Predefined Analytical Operation
    |
    v
Pandas
```

La decisione è intenzionale e migliora:

- sicurezza;
- testabilità;
- riproducibilità;
- prevedibilità;
- controllo dello scope.

---

## 12.19 Agentic Responsibility

L'assenza di esecuzione arbitraria di codice non elimina la natura agentica del sistema.

La responsabilità è divisa tra due livelli.

### AI Orchestrator

Decide:

```text
WHEN should the Data Agent be used?
```

### Python Data Agent

Decide, entro il proprio insieme di operazioni consentite:

```text
HOW should the supported analysis be executed?
```

Questa separazione permette di conservare il routing autonomo richiesto dal progetto senza introdurre esecuzione non controllata sul sistema host.

---

## 12.20 Scope Validation

Il Question Interpreter supporta soltanto combinazioni analitiche implementate.

Una richiesta che tenta di combinare contemporaneamente dimensioni incompatibili viene rifiutata in modo controllato.

Ad esempio, il servizio non deve inventare una strategia per:

```text
group simultaneously by supplier, plant,
production line, model and operator team
```

se tale combinazione non appartiene alle analisi previste.

Analogamente, una richiesta che combina analisi temporale e grouping non supportato non viene reinterpretata automaticamente.

---

## 12.21 Preservazione dello scope

Durante l'integrazione è importante che la domanda ricevuta dal Data Agent mantenga lo scope originale dell'utente.

Il prompt dell'AI Orchestrator istruisce quindi il modello a non aggiungere autonomamente:

- filtri temporali;
- dimensioni;
- supplier;
- linee produttive;
- altre condizioni non richieste.

Il flusso desiderato è:

```text
User Scope
    |
    v
Tool Call
    |
    v
Same Analytical Scope
```

e non:

```text
User Scope
    |
    v
LLM adds assumptions
    |
    v
Different Analysis
```

Questa protezione riduce interpretazioni analitiche errate.

---

## 12.22 Response analitica

Il Data Agent restituisce al backend un risultato strutturato contenente le informazioni prodotte dall'analisi.

A seconda della tipologia di richiesta, il risultato può includere:

- identificazione dell'analisi eseguita;
- KPI;
- risultati aggregati;
- andamento temporale;
- sintesi testuale;
- riferimento a un grafico.

Non tutti gli elementi sono presenti in ogni risposta.

Il payload interno del Data Agent non costituisce il contratto pubblico del frontend.

---

## 12.23 Sintesi analitica

Il Data Agent produce una sintesi dei risultati numerici.

Questa sintesi ha lo scopo di fornire all'AI Orchestrator informazioni facilmente utilizzabili durante la generazione della risposta finale.

Esempio concettuale:

```text
SUP-07 has the highest defect rate at 2.99%.
```

oppure:

```text
Line 3 has the highest production-line defect rate.
```

La sintesi deve essere basata sui valori effettivamente calcolati.

---

## 12.24 Separazione tra facts e policy

Il Data Agent è responsabile dei fatti derivati dal dataset.

Esempio:

```text
SUP-07 defect rate = 2.99%
```

Il RAG è responsabile delle informazioni documentali.

Esempio:

```text
Supplier defect rate between 2.0% and 3.0%
= Observation
```

L'AI Orchestrator può combinare i due risultati.

```text
Data Agent Fact
        +
Knowledge Base Policy
        |
        v
Hybrid Answer
```

Questa separazione evita di incorporare policy aziendali statiche nella logica analitica.

---

## 12.25 Error handling

Il Data Agent deve produrre errori controllati quando:

- la richiesta non appartiene allo scope supportato;
- vengono richieste combinazioni analitiche incompatibili;
- si verifica un errore durante il caricamento o l'analisi dei dati;
- non è possibile generare il grafico richiesto.

Gli errori non devono:

- produrre valori inventati;
- modificare silenziosamente la richiesta;
- eseguire un'analisi diversa da quella richiesta senza segnalarlo;
- esporre percorsi filesystem sensibili.

---

## 12.26 Data Agent unavailable

Se il microservizio non è raggiungibile, la responsabilità di tradurre l'errore verso il frontend appartiene al backend Node.js.

Il backend restituisce:

```text
503 Service Unavailable
```

con un messaggio controllato:

```text
Manufacturing data analysis is temporarily unavailable. Please try again later.
```

Il frontend non riceve direttamente errori di connessione verso la porta `8001`.

---

## 12.27 Health Check

Il Data Agent espone:

```http
GET /health
```

L'endpoint viene utilizzato per verificare che il microservizio FastAPI sia disponibile.

Non avvia un'analisi completa.

---

## 12.28 Root Endpoint

Il servizio espone inoltre:

```http
GET /
```

come endpoint base.

Può essere utilizzato per una verifica semplice del servizio durante sviluppo e troubleshooting.

Il normale flusso applicativo utilizza invece:

```text
/api/analysis
/health
/charts/:filename
```

---

## 12.29 Sicurezza

Il Data Agent è progettato come servizio interno.

Il frontend non deve poter dipendere direttamente dalla sua posizione o configurazione.

Tra i principi applicati:

- nessuna chiave OpenAI nel servizio analitico;
- nessuna esecuzione arbitraria di codice;
- dataset utilizzato in sola lettura;
- output limitati alle operazioni previste;
- nomi dei grafici generati dal sistema;
- nessun percorso filesystem esposto al frontend;
- configurazione del servizio separata dal client.

---

## 12.30 Testabilità

La natura deterministica del Data Agent permette di testare direttamente:

- cleaning del dataset;
- KPI globali;
- aggregazioni;
- ranking;
- trend mensili;
- Question Interpreter;
- richieste italiane;
- richieste inglesi;
- generazione dei grafici;
- combinazioni non supportate;
- error handling.

A parità di dataset e richiesta, il motore analitico deve produrre risultati coerenti e riproducibili.

---

## 12.31 Vantaggi dell'approccio

La soluzione adottata offre i seguenti vantaggi:

- utilizzo dell'ecosistema Pandas;
- separazione dell'analytics dal backend;
- risultati numerici deterministici;
- maggiore sicurezza;
- assenza di arbitrary code execution;
- buona testabilità;
- indipendenza dal frontend;
- supporto bilingue;
- generazione server-side dei grafici;
- possibilità di estendere le analisi senza modificare il contratto della Chat API.

---

## 12.32 Conclusione

Il Python Data Agent costituisce il livello specializzato per l'elaborazione quantitativa di Maranello AI.

Il backend utilizza un solo punto di ingresso analitico:

```http
POST /api/analysis
```

mentre il Data Agent mantiene internamente la responsabilità di interpretare la domanda, selezionare un'analisi supportata ed eseguirla tramite operazioni Pandas controllate.

Questo approccio sostituisce il design iniziale basato su numerosi endpoint analitici separati e riflette l'architettura effettivamente implementata.

---

# 13. Sicurezza

## 13.1 Panoramica

La sicurezza delle API di Maranello AI è stata progettata in funzione dello scope dimostrativo del progetto e dell'architettura effettivamente implementata.

La versione corrente non implementa autenticazione utente, Single Sign-On o Role-Based Access Control.

Le principali misure di sicurezza riguardano invece:

- protezione delle credenziali;
- isolamento dei servizi interni;
- validazione degli input;
- protezione dei percorsi dei grafici;
- controllo dell'esecuzione analitica;
- gestione sicura degli errori;
- separazione tra frontend e dipendenze interne.

---

## 13.2 Autenticazione

La versione corrente non richiede autenticazione per utilizzare la Chat API.

Non sono implementati:

```text
OAuth 2.0
OpenID Connect
JWT
Single Sign-On
Role-Based Access Control
```

Questa scelta è coerente con la natura accademica e dimostrativa del progetto.

L'introduzione di autenticazione e autorizzazione costituisce una possibile evoluzione futura.

---

## 13.3 Protezione delle credenziali

Le credenziali non vengono memorizzate direttamente nel codice sorgente.

In particolare:

```text
OPENAI_API_KEY
```

viene caricata tramite variabile d'ambiente.

Il repository contiene un file:

```text
.env.example
```

con i nomi delle variabili necessarie ma senza valori sensibili reali.

Il file:

```text
.env
```

è escluso dal version control.

---

## 13.4 Nessuna API key nel frontend

Il frontend React non contiene e non riceve la chiave OpenAI.

Il flusso corretto è:

```text
React Frontend
      |
      v
Node.js Backend
      |
      v
OpenAI API
```

e non:

```text
React Frontend
      |
      v
OpenAI API
```

Questo impedisce l'esposizione della credenziale all'interno del bundle distribuito al browser.

---

## 13.5 Isolamento dei servizi interni

Il frontend comunica esclusivamente con il backend Node.js.

Non accede direttamente a:

- Python Data Agent;
- ChromaDB;
- Manufacturing Dataset;
- filesystem dei grafici;
- OpenAI API.

Il backend costituisce quindi il boundary applicativo tra browser e infrastruttura interna.

---

## 13.6 Validazione della Chat API

Il backend valida l'input prima dell'elaborazione.

In particolare, `message` deve essere:

- presente;
- una richiesta valida secondo il contratto applicativo;
- non vuoto;
- non composto esclusivamente da whitespace.

Una richiesta non valida viene rifiutata prima dell'invocazione del modello.

Questo riduce:

- chiamate inutili al provider AI;
- comportamento ambiguo;
- input non previsti nel flusso applicativo.

---

## 13.7 Protezione del Chart Proxy

L'endpoint:

```http
GET /api/charts/:filename
```

valida il nome del file prima di inoltrare la richiesta al Python Data Agent.

La validazione impedisce di utilizzare il parametro come percorso filesystem arbitrario.

Pattern come:

```text
../
```

non devono consentire l'accesso a file esterni alla directory prevista.

Questo protegge il sistema da tentativi di path traversal.

---

## 13.8 Sicurezza del Data Agent

Il Python Data Agent non esegue codice Python arbitrario prodotto dall'LLM.

Il modello non può fornire direttamente:

```python
exec(...)
```

oppure:

```python
eval(...)
```

o codice equivalente da eseguire sul sistema host.

Il Data Agent utilizza esclusivamente operazioni analitiche predefinite e validate.

Questa decisione riduce il rischio di:

- arbitrary code execution;
- accesso non autorizzato ai file;
- lettura di variabili d'ambiente;
- modifica accidentale del dataset;
- comportamento non deterministico;
- abuso del runtime Python.

---

## 13.9 Dataset read-only

Il Manufacturing Dataset viene trattato come sorgente analitica.

Le API non implementano operazioni di modifica del CSV.

Il Data Agent può:

```text
read
clean in memory
aggregate
calculate
visualize
```

ma non modifica il dataset sorgente durante una normale richiesta analitica.

---

## 13.10 Errori e informazioni sensibili

Le risposte di errore non devono esporre:

- API key;
- variabili d'ambiente;
- stack trace;
- percorsi filesystem;
- dettagli interni del client OpenAI;
- configurazione ChromaDB;
- informazioni non necessarie sull'infrastruttura.

Gli errori tecnici vengono tradotti in messaggi controllati prima di essere restituiti al frontend.

---

## 13.11 Configurazione tramite ambiente e fail-fast

La configurazione sensibile o dipendente dall'ambiente viene mantenuta fuori dal codice sorgente.

Tra le principali variabili del backend:

    OPENAI_API_KEY
    OPENAI_EMBEDDING_MODEL
    LLM_MODEL
    LLM_TEMPERATURE
    LLM_TIMEOUT_SECONDS
    PORT
    DATA_AGENT_URL
    CHROMA_URL
    CHROMA_COLLECTION
    CHAT_RATE_LIMIT_WINDOW_MINUTES
    CHAT_RATE_LIMIT_MAX_REQUESTS

`OPENAI_API_KEY` costituisce una configurazione obbligatoria.

Il backend applica una strategia **fail-fast**: se la variabile è assente, vuota oppure contiene esclusivamente whitespace, la configurazione viene considerata non valida e il servizio non procede con un normale avvio applicativo.

Il comportamento desiderato è:

    Backend Startup
          |
          v
    Read Environment
          |
          v
    OPENAI_API_KEY valid?
       /          \
     Yes           No
      |             |
      v             v
    Continue     Fail Fast

Questa scelta evita di avviare un'istanza apparentemente funzionante che fallirebbe soltanto alla prima richiesta che necessita del provider AI.

Le configurazioni non sensibili possono utilizzare valori di default quando previsto dall'applicazione.

Le credenziali reali rimangono escluse dal repository tramite `.env`, mentre i file `.env.example` documentano esclusivamente le variabili supportate.

---

## 13.12 Rate limiting della Chat API

L'endpoint:

    POST /api/chat

può generare chiamate verso il provider AI e verso servizi interni. Per questo motivo il backend applica un rate limiter dedicato prima dell'esecuzione della logica conversazionale a pagamento.

La configurazione predefinita utilizza:

    CHAT_RATE_LIMIT_WINDOW_MINUTES = 15
    CHAT_RATE_LIMIT_MAX_REQUESTS = 30

Il limite predefinito è quindi di **30 richieste per finestra di 15 minuti**, secondo la chiave utilizzata dal middleware di rate limiting.

Quando il limite viene superato, il backend restituisce:

    429 Too Many Requests

con una risposta controllata equivalente a:

    Too many chat requests. Please try again later.

Il rate limiter viene applicato prima del `ChatService`, impedendo che una richiesta già limitata raggiunga l'AI Orchestrator e generi una chiamata non necessaria al provider.

Il middleware utilizza gli header standard del rate limiting e non utilizza i legacy headers.

I valori della finestra e del numero massimo di richieste sono configurabili tramite environment variables.

Il rate limiting rappresenta una protezione applicativa di base contro abuso accidentale o consumo eccessivo della Chat API, ma non sostituisce:

- autenticazione;
- autorizzazione;
- quote persistenti per identità;
- controllo dei costi per utente;
- policy enterprise di API management.

---

## 13.13 Limitazioni di sicurezza correnti

La versione corrente non implementa ancora meccanismi enterprise come:

- autenticazione degli utenti;
- autorizzazione per ruolo;
- OAuth 2.0 / OpenID Connect;
- API key service-to-service;
- quote persistenti associate a un'identità autenticata;
- Web Application Firewall;
- distributed identity;
- secret manager esterno;
- API gateway enterprise.

Queste funzionalità non vengono considerate implementate e costituiscono possibili evoluzioni future.

La baseline corrente comprende invece:

- configurazione sensibile tramite environment variables;
- fail-fast sulla configurazione OpenAI obbligatoria;
- isolamento delle dipendenze interne dal frontend;
- validazione degli input;
- protezione del Chart Proxy;
- Data Agent deterministico senza arbitrary code execution;
- rate limiting della Chat API;
- gestione controllata degli errori.

---

# 14. Logging e osservabilità

## 14.1 Panoramica

Il backend implementa un livello di osservabilità strutturata per la Chat API con l'obiettivo di rendere tracciabile il comportamento delle richieste senza modificare il contratto pubblico utilizzato dal frontend.

Per ogni richiesta conversazionale vengono raccolte informazioni utili a comprendere:

- identificativo della richiesta;
- esito HTTP;
- latenza;
- strumenti utilizzati;
- consumo di token OpenAI.

Questi dati appartengono all'osservabilità interna del backend e non vengono aggiunti indiscriminatamente alla response pubblica.

---

## 14.2 Request ID

Ogni richiesta alla Chat API viene associata a un identificativo di richiesta.

Il valore consente di correlare la richiesta HTTP con le informazioni registrate dal middleware di osservabilità.

Il backend restituisce inoltre l'identificativo attraverso l'header:

    X-Request-Id

Il flusso è:

    POST /api/chat
          |
          v
    Generate Request ID
          |
          v
    Request Processing
          |
          v
    Structured Observability
          |
          +---- requestId
          |
          +---- statusCode
          |
          +---- latency
          |
          +---- toolsUsed
          |
          +---- tokenUsage
          |
          v
    HTTP Response
          |
          v
    X-Request-Id

Il request ID è un metadato di osservabilità e non sostituisce il `sessionId`.

I due identificativi hanno responsabilità differenti:

| Identificativo | Responsabilità |
|----------------|----------------|
| `sessionId` | Mantiene la continuità della conversazione tra più richieste. |
| `requestId` | Identifica una singola richiesta HTTP per osservabilità e troubleshooting. |

---

## 14.3 Logging strutturato della Chat API

Il middleware di osservabilità registra informazioni strutturate relative all'elaborazione della richiesta.

Tra i dati disponibili rientrano:

- `requestId`;
- status code HTTP;
- latenza della richiesta;
- tool applicativi utilizzati;
- token usage associato all'orchestrazione AI.

Questo consente di distinguere, ad esempio, una richiesta che ha utilizzato soltanto il RAG da una richiesta analitica o ibrida.

Il logging strutturato facilita:

- troubleshooting;
- analisi delle failure;
- verifica del routing agentico;
- analisi della latenza;
- osservazione del consumo del provider AI.

Le informazioni sensibili, come `OPENAI_API_KEY`, non devono essere incluse nei log.

---

## 14.4 Tool observability

Il sistema mantiene l'informazione relativa ai tool effettivamente utilizzati durante l'orchestrazione.

I tool principali sono:

    search_knowledge_base
    analyze_manufacturing_data

L'informazione viene utilizzata internamente dall'osservabilità e continua inoltre a essere restituita al frontend tramite il campo pubblico:

    toolsUsed

Esempio:

    {
      "toolsUsed": [
        "search_knowledge_base",
        "analyze_manufacturing_data"
      ]
    }

Questo rende possibile osservare il percorso agentico senza richiedere al client di conoscere i dettagli interni delle function call OpenAI.

---

## 14.5 Token usage

L'AI Orchestrator raccoglie il token usage restituito dal provider per ogni round della Responses API.

Il modello interno utilizza tre valori:

    inputTokens
    outputTokens
    totalTokens

Il consumo viene **aggregato su tutti i round OpenAI appartenenti alla stessa orchestrazione**.

Questo è particolarmente importante per le richieste che utilizzano tool calling.

Ad esempio:

    OpenAI Round 1
        input:  100
        output: 20

    Tool Execution

    OpenAI Round 2
        input:  200
        output: 30

produce un consumo aggregato:

    inputTokens  = 300
    outputTokens = 50
    totalTokens  = 350

Il sistema non considera quindi soltanto la chiamata finale al modello, ma anche i round intermedi necessari all'esecuzione dei tool.

Se il provider non restituisce informazioni di usage per un determinato round, l'orchestratore gestisce l'assenza senza interrompere l'elaborazione.

---

## 14.6 Separazione tra osservabilità interna e API pubblica

Il token usage viene mantenuto come informazione interna.

La response pubblica della Chat API continua a utilizzare il contratto:

    {
      "sessionId": "...",
      "answer": "...",
      "toolsUsed": [],
      "chartUrl": "..."
    }

e non viene estesa con:

    tokenUsage

Questa separazione evita di accoppiare il frontend a metadati operativi che appartengono al backend.

Il flusso logico è:

    AI Orchestrator
          |
          +---- Public Chat Result --------> Frontend
          |
          +---- Observability Metadata ----> Backend Logging

La stessa elaborazione produce quindi sia il risultato applicativo destinato al client sia i metadati necessari all'osservabilità, mantenendo separati i due contratti.

---

## 14.7 Status code e latenza

Il middleware registra l'esito HTTP e la latenza della richiesta.

Questo permette di distinguere richieste:

- completate correttamente;
- rifiutate dalla validazione;
- limitate dal rate limiter;
- fallite durante l'elaborazione.

L'osservabilità non è limitata esclusivamente alle richieste `200 OK`.

Anche condizioni come:

    400 Bad Request

e:

    429 Too Many Requests

vengono tracciate con le informazioni applicabili alla richiesta.

Quando una richiesta viene interrotta prima dell'esecuzione dell'AI Orchestrator, i metadati relativi a tool e token possono naturalmente non essere disponibili.

---

## 14.8 Health checks e dependency-aware errors

Gli endpoint:

    GET /health

del backend e del Data Agent permettono di verificare la disponibilità dei rispettivi processi.

Il backend distingue inoltre le indisponibilità delle dipendenze necessarie alla richiesta.

### Data Agent

    Manufacturing data analysis is temporarily unavailable. Please try again later.

### Knowledge Base

    The company knowledge base is temporarily unavailable. Please try again later.

Queste condizioni vengono rappresentate attraverso:

    503 Service Unavailable

La combinazione tra status code, request ID e logging strutturato migliora il troubleshooting rispetto a un errore interno generico.

---

## 14.9 Limiti dell'osservabilità corrente

La versione corrente implementa una baseline concreta di osservabilità applicativa, ma non costituisce una piattaforma enterprise completa.

Sono implementati:

- request ID;
- header `X-Request-Id`;
- logging strutturato della Chat API;
- status code;
- latenza;
- tool usage;
- token usage aggregato sui round OpenAI.

Non sono invece implementati:

- distributed tracing;
- OpenTelemetry;
- Prometheus;
- Grafana;
- centralized log aggregation;
- dashboard operative;
- alerting enterprise;
- persistenza storica centralizzata delle metriche.

Questi elementi costituiscono possibili evoluzioni per un deployment distribuito o production-grade.

---

# 15. Testing delle API

## 15.1 Strategia di testing

Maranello AI utilizza una strategia di testing multilivello per verificare separatamente:

- componenti deterministici;
- servizi applicativi;
- client HTTP;
- orchestrazione AI;
- retrieval RAG;
- middleware;
- contratti API;
- lifecycle del Python Data Agent;
- integrazione tra i componenti principali.

La suite automatizzata è stata ampliata anche per coprire i miglioramenti introdotti dopo la revisione architetturale del progetto.

---

## 15.2 Baseline automatizzata verificata

La baseline corrente verificata comprende:

| Componente | Test superati |
|------------|---------------|
| Node.js Backend | 120 |
| Python Data Agent | 80 |
| **Totale** | **200** |

Per il backend Node.js la suite è distribuita su:

    18 test files

e il quality gate verificato comprende:

    npm run typecheck
    npm run lint
    npm test
    npm run build

Tutti questi controlli risultano superati nella baseline corrente.

Per il Python Data Agent il quality gate verificato comprende:

    ruff check app tests
    pytest

Anche questi controlli risultano superati nella baseline corrente.

Durante pytest può comparire uno `StarletteDeprecationWarning` proveniente dall'integrazione tra le versioni installate di FastAPI/Starlette TestClient e httpx. Il warning non corrisponde a un test fallito e non modifica l'esito della suite.

---

## 15.3 DatasetRepository

I test del `DatasetRepository` verificano il nuovo lifecycle del Manufacturing Dataset.

Sono coperti scenari quali:

- caricamento iniziale lazy;
- esecuzione del cleaning una sola volta durante la preparazione della cache;
- riutilizzo del dataset preparato nelle analisi successive;
- stato del repository prima del primo caricamento;
- reload esplicito;
- mantenimento della cache precedente quando un reload fallisce;
- protezione del dataset cached da modifiche accidentali.

È inoltre verificato che più analisi possano riutilizzare lo stesso dataset preparato senza ripetere caricamento e cleaning a ogni richiesta.

---

## 15.4 Chart retention

La suite del Data Agent verifica il comportamento del `ChartCleanupService`.

I test coprono:

- identificazione dei grafici scaduti;
- rimozione dei soli file appartenenti al pattern gestito;
- preservazione dei file non interessati dal cleanup;
- gestione della directory assente;
- gestione race-safe di file già rimossi;
- validazione della configurazione di retention.

Sono presenti inoltre test di integrazione sul lifecycle FastAPI per verificare l'avvio del meccanismo di cleanup e la gestione del relativo background task.

---

## 15.5 AI Orchestrator

I test dell'AI Orchestrator verificano:

- risposta finale senza tool;
- utilizzo del Knowledge Base tool;
- utilizzo del Data Agent tool;
- orchestrazione con tool calling;
- propagazione dei risultati dei tool;
- raccolta dei tool effettivamente utilizzati;
- aggregazione del token usage;
- limite massimo dei tool round.

Il limite:

    MAX_TOOL_ROUNDS = 5

è verificato esplicitamente.

La suite controlla che, quando il modello continua a richiedere tool oltre il limite consentito, l'orchestrazione venga interrotta invece di entrare in un ciclo indefinito.

---

## 15.6 Resilienza HTTP

Il componente condiviso utilizzato per le richieste HTTP resilienti è coperto da test dedicati.

Sono verificati:

- successo al primo tentativo;
- retry su risposte `5xx`;
- assenza di retry su risposte `4xx`;
- retry su errori di rete transitori;
- esaurimento dei tentativi disponibili;
- restituzione dell'ultima risposta `5xx` dopo l'esaurimento dei retry;
- timeout tramite `AbortController`;
- validazione della configurazione.

Sono inoltre presenti test specifici per:

- `DataAgentClient`;
- `ChartClient`.

In questo modo la policy di timeout/retry/backoff viene verificata sia a livello del componente condiviso sia nei client che la utilizzano.

---

## 15.7 RAG relevance filtering

I test del `RetrieverService` verificano il filtro di rilevanza introdotto sui risultati ChromaDB.

Sono coperti:

- risultati con distanza inferiore alla soglia;
- risultato esattamente sulla soglia;
- esclusione dei risultati oltre soglia;
- esclusione delle distanze mancanti;
- esclusione delle distanze non valide;
- possibilità di ottenere zero risultati rilevanti;
- validazione del valore configurato per `maxDistance`.

La configurazione corrente utilizza:

    maxDistance = 0.70

Oltre ai test automatizzati, la soglia è stata validata empiricamente sul corpus corrente con query pertinenti e non pertinenti in inglese e italiano.

---

## 15.8 Environment configuration e fail-fast

I test della configurazione verificano il requisito obbligatorio:

    OPENAI_API_KEY

Sono coperti almeno i casi:

- variabile presente e valida;
- variabile assente;
- valore vuoto;
- valore composto esclusivamente da whitespace.

L'obiettivo è garantire che una configurazione OpenAI non valida venga rilevata durante l'inizializzazione anziché soltanto alla prima richiesta AI.

---

## 15.9 Rate limiting

I test di integrazione della Chat API verificano il rate limiter utilizzando una configurazione controllata.

La suite verifica che:

1. le richieste entro il limite vengano accettate;
2. la richiesta che supera il limite riceva `429 Too Many Requests`;
3. una richiesta già limitata non raggiunga il `ChatService`.

Il terzo punto è particolarmente importante perché dimostra che il rate limiter viene applicato prima dell'esecuzione della parte potenzialmente a pagamento della pipeline AI.

---

## 15.10 Structured observability

I test di integrazione verificano il middleware di osservabilità della Chat API.

Sono coperti:

- generazione del request ID;
- header `X-Request-Id`;
- registrazione dell'esito della richiesta;
- registrazione della latenza;
- registrazione dei tool utilizzati;
- registrazione del token usage;
- osservabilità delle richieste valide;
- osservabilità delle richieste `400 Bad Request`;
- osservabilità delle richieste `429 Too Many Requests`.

È inoltre verificato che il token usage rimanga un metadato interno e non venga aggiunto al contratto pubblico restituito al frontend.

---

## 15.11 Token usage multi-round

La suite dell'AI Orchestrator verifica esplicitamente l'aggregazione del consumo su più round OpenAI.

Un caso di test equivalente a:

    Round 1
    input_tokens  = 100
    output_tokens = 20

    Round 2
    input_tokens  = 200
    output_tokens = 30

deve produrre:

    inputTokens  = 300
    outputTokens = 50
    totalTokens  = 350

Questo impedisce di sottostimare il consumo delle richieste agentiche considerando soltanto l'ultima chiamata al provider.

---

## 15.12 Chat API integration tests

I test di integrazione della Chat API verificano scenari quali:

- risposta conversazionale valida;
- propagazione di un `sessionId` esistente;
- rifiuto di un messaggio mancante;
- rifiuto di un `sessionId` con tipo non valido;
- rate limiting;
- raccolta dei dati di osservabilità.

La suite verifica contemporaneamente il contratto HTTP pubblico e il comportamento dei middleware applicativi.

---

## 15.13 Data Agent analytical regression

Le analisi del Data Agent sono verificate anche rispetto ai KPI attesi del dataset preparato.

La baseline analitica corrente comprende:

    total_production = 164060
    defective_units = 3272
    defect_rate = 1.99
    rework_rate = 0.96
    scrap_rate = 0.51
    average_quality_score = 95.82
    average_downtime_minutes = 33.04
    average_cycle_time_seconds = 84.74

Il mantenimento di questi valori dopo l'introduzione del `DatasetRepository` dimostra che l'ottimizzazione del lifecycle del dataset non ha modificato il risultato analitico atteso.

---

## 15.14 Test manuali e full-stack

Oltre alle suite automatizzate, il progetto è stato verificato attraverso scenari end-to-end rappresentativi.

Tra questi:

### RAG

    When should a production issue be escalated according to company policy?

Il sistema utilizza la Knowledge Base e produce una risposta grounded nelle policy aziendali simulate.

### Data Agent

    Show me the monthly defect rate trend.

Il sistema utilizza il Data Agent, produce la sintesi analitica e rende disponibile il grafico mensile.

### Conversation memory

Una richiesta successiva può fare riferimento a un'entità già introdotta nella conversazione, ad esempio:

    What about that supplier?

Il backend mantiene il contesto tramite `sessionId` e stato conversazionale server-side.

---

## 15.15 Obiettivo della suite

La suite non verifica soltanto il comportamento nominale delle API.

La baseline corrente copre anche failure mode e application boundary introdotti per rendere l'architettura più robusta:

- dataset I/O ripetuto;
- accumulo dei grafici runtime;
- tool loop non terminanti;
- failure HTTP transitorie;
- retrieval semanticamente debole;
- configurazione OpenAI mancante;
- abuso o consumo eccessivo della Chat API;
- osservabilità insufficiente delle richieste agentiche.

L'obiettivo è mantenere l'architettura testabile e verificabile anche quando vengono introdotte protezioni operative che non modificano il normale contratto utente.

---

# 16. Evoluzioni future

## 16.1 Principio generale

L'architettura corrente soddisfa il perimetro funzionale del progetto e include una serie di protezioni operative introdotte durante la fase di hardening.

Le evoluzioni descritte in questo capitolo rappresentano possibili estensioni per scenari con:

- dataset significativamente più grandi;
- più utenti concorrenti;
- deployment distribuito;
- requisiti enterprise di sicurezza;
- requisiti avanzati di osservabilità;
- nuove sorgenti documentali o analitiche.

Le funzionalità indicate come future non devono essere interpretate come già implementate nella versione corrente.

---

## 16.2 Evoluzione del layer analitico oltre Pandas

Il Data Agent corrente utilizza Pandas.

Questa scelta rimane appropriata per il Manufacturing Dataset del progetto, composto da circa 2.000 record, e mantiene coerenza con i requisiti dell'assignment.

L'introduzione del `DatasetRepository` elimina inoltre il precedente costo di caricamento e cleaning ripetuto per ogni richiesta, consentendo di riutilizzare il DataFrame preparato durante il lifecycle del processo.

Per dataset dell'ordine di centinaia di migliaia o milioni di record, oppure quando il dataset non può essere mantenuto efficientemente in memoria, il layer di accesso ai dati dovrebbe essere rivalutato.

Possibili evoluzioni includono:

### DuckDB

DuckDB rappresenterebbe una naturale evoluzione per workload analitici locali o embedded.

Potrebbe consentire:

- query SQL direttamente sui dati tabellari;
- aggregazioni efficienti;
- minore dipendenza dal caricamento completo del dataset in memoria;
- utilizzo efficace di formati analitici come Parquet;
- mantenimento di un deployment relativamente semplice.

### SQLite

SQLite potrebbe essere valutato quando siano utili:

- persistenza locale strutturata;
- query SQL;
- indicizzazione;
- gestione di dataset relazionali di dimensione moderata.

Per workload prevalentemente OLAP e analitici, DuckDB sarebbe generalmente il candidato più naturale tra le due opzioni; SQLite rimane una possibile alternativa per scenari maggiormente orientati alla persistenza relazionale embedded.

### Database esterno

Per scenari multiutente o distribuiti potrebbe diventare appropriato un database esterno gestito.

Il percorso evolutivo può essere rappresentato come:

    Current Dataset
    ~2,000 rows
         |
         v
    Pandas
    + DatasetRepository
         |
         | dataset growth /
         | memory pressure
         v
    DuckDB / SQLite
         |
         | distributed scale /
         | multi-user requirements
         v
    External Data Platform

Nessuna di queste migrazioni è implementata nella versione corrente.

La scelta intenzionale è mantenere Pandas per il perimetro attuale e definire chiaramente il punto nel quale un motore query-oriented diventerebbe architetturalmente preferibile.

---

## 16.3 Persistenza distribuita delle conversazioni

Il `ConversationManager` corrente mantiene lo stato conversazionale in memoria.

Per un deployment distribuito o multi-instance, una possibile evoluzione sarebbe utilizzare uno storage condiviso, ad esempio:

- Redis;
- database relazionale;
- session store dedicato.

Questo consentirebbe di mantenere la continuità delle sessioni anche tra più istanze del backend.

---

## 16.4 Autenticazione e autorizzazione

La Chat API dispone attualmente di rate limiting, ma non implementa autenticazione degli utenti.

Una futura versione production-grade potrebbe introdurre:

- OAuth 2.0;
- OpenID Connect;
- Single Sign-On;
- JWT validation;
- Role-Based Access Control;
- API key per integrazioni service-to-service.

L'autenticazione permetterebbe inoltre di applicare quote e policy di utilizzo per identità anziché affidarsi esclusivamente alla chiave utilizzata dal rate limiter.

---

## 16.5 API management e protezione perimetrale

In un deployment enterprise il backend potrebbe essere posizionato dietro:

- API gateway;
- reverse proxy gestito;
- Web Application Firewall;
- policy centralizzate di rate limiting;
- request size limits;
- IP filtering;
- network policy.

Il rate limiting applicativo corrente rappresenta una baseline, non sostituisce un layer perimetrale enterprise.

---

## 16.6 Osservabilità centralizzata

La versione corrente implementa già:

- request ID;
- `X-Request-Id`;
- logging strutturato;
- status code;
- latenza;
- tool usage;
- token usage aggregato.

Le evoluzioni future riguardano quindi la **centralizzazione e distribuzione** dell'osservabilità, non la sua introduzione di base.

Possibili estensioni includono:

- OpenTelemetry;
- distributed tracing;
- Prometheus;
- Grafana;
- centralized log aggregation;
- dashboard operative;
- alerting;
- analisi storica dei costi e dei token.

Questo permetterebbe di correlare una singola richiesta tra backend, Data Agent, vector database e provider AI.

---

## 16.7 Persistenza delle metriche AI

Il token usage viene attualmente raccolto per la richiesta e utilizzato nell'osservabilità del backend.

Una futura evoluzione potrebbe persistere metriche quali:

- input tokens;
- output tokens;
- total tokens;
- modello utilizzato;
- tool utilizzati;
- latenza;
- costo stimato;
- request ID;
- timestamp.

Questo consentirebbe analisi storiche su consumo e performance senza modificare il contratto pubblico della Chat API.

---

## 16.8 Evoluzione della Knowledge Base

La Knowledge Base corrente utilizza documenti locali controllati e ChromaDB.

Possibili evoluzioni includono:

- ingestion incrementale;
- versionamento documentale;
- document lifecycle management;
- metadati più ricchi;
- filtri per categoria o versione;
- re-indexing selettivo;
- supporto a repository documentali esterni.

Ogni modifica significativa del corpus o dell'embedding model dovrebbe inoltre prevedere una nuova calibrazione del relevance threshold utilizzato dal retriever.

---

## 16.9 Evoluzione del relevance filtering

La soglia corrente:

    maxDistance = 0.70

è stata calibrata empiricamente sul corpus e sull'embedding model attuali.

Con una Knowledge Base più ampia potrebbe essere utile introdurre:

- benchmark di retrieval più estesi;
- evaluation dataset dedicato;
- metriche Precision@K e Recall@K;
- reranking;
- threshold specifici per dominio;
- hybrid search semantica e keyword-based.

La soglia non dovrebbe essere considerata immutabile rispetto all'evoluzione del corpus.

---

## 16.10 Chart storage distribuito

La versione corrente implementa già una retention automatica locale dei grafici runtime.

Per deployment multi-instance o containerizzati, una futura evoluzione potrebbe sostituire lo storage locale con:

- object storage;
- blob storage;
- URL firmati;
- CDN;
- lifecycle policy gestite dall'infrastruttura.

In questo scenario la retention potrebbe essere delegata al servizio di storage invece che al filesystem locale del Data Agent.

---

## 16.11 Dataset refresh automatizzato

Il `DatasetRepository` espone un meccanismo esplicito di reload.

La versione corrente non implementa un refresh automatico del Manufacturing Dataset.

In uno scenario con dati aggiornati dinamicamente si potrebbero introdurre:

- invalidazione temporale della cache;
- refresh schedulato;
- refresh event-driven;
- versionamento del dataset;
- controllo della data di modifica della sorgente.

Qualunque strategia dovrebbe mantenere la proprietà attuale per cui un refresh fallito non invalida un dataset precedentemente utilizzabile.

---

## 16.12 Scalabilità orizzontale

Per aumentare il numero di utenti concorrenti potrebbero essere introdotti:

- più backend instance;
- più Data Agent instance;
- session storage condiviso;
- load balancing;
- storage grafici condiviso;
- metriche e tracing distribuiti.

Questa evoluzione richiederebbe di rivedere le componenti che oggi mantengono stato locale al processo.

---

## 16.13 CI/CD

Una pipeline CI/CD potrebbe automatizzare:

- backend type checking;
- backend lint;
- backend test;
- backend build;
- Data Agent lint;
- Data Agent test;
- frontend lint;
- frontend build;
- dependency checks;
- build degli artefatti;
- deployment.

La suite automatizzata corrente costituisce la base per introdurre questi quality gate in pipeline.

---

## 16.14 Evoluzione dei provider AI

L'architettura potrebbe essere ulteriormente astratta per supportare provider AI differenti.

Una possibile evoluzione sarebbe introdurre un'interfaccia applicativa dedicata al provider per separare maggiormente:

- orchestrazione;
- tool calling;
- token usage;
- conversation continuation;
- modello AI specifico.

Qualunque migrazione dovrebbe preservare il principio fondamentale del sistema:

> il modello decide autonomamente, entro application boundary espliciti, quali capacità utilizzare per rispondere alla richiesta.

---

## 16.15 Principio evolutivo

Le evoluzioni future non richiedono di abbandonare l'architettura corrente.

I principali boundary sono già separati:

    React Frontend
          |
          v
    Node.js Backend
          |
          +---- AI Orchestration
          |
          +---- RAG / ChromaDB
          |
          +---- Python Data Agent

Questo consente di evolvere separatamente:

- presentation layer;
- orchestration layer;
- retrieval layer;
- analytical layer;
- persistence layer;
- observability layer;
- security layer.

La versione corrente privilegia semplicità, testabilità e coerenza con il perimetro del progetto, mantenendo un percorso esplicito verso requisiti di scala e sicurezza superiori.

---

# 17. Conclusioni

La API Specification finale di Maranello AI descrive l'architettura **as-built** del sistema e sostituisce le ipotesi progettuali definite nelle prime fasi del progetto.

La versione finale utilizza un insieme limitato e chiaro di API.

### Backend Node.js

```text
GET  /health
POST /api/chat
GET  /api/charts/:filename
```

### Python Data Agent

```text
GET  /
GET  /health
POST /api/analysis
GET  /charts/:filename
```

Il frontend React comunica esclusivamente con il backend Node.js.

La Chat API rappresenta il singolo punto di ingresso conversazionale e non richiede al client di specificare quale strumento utilizzare.

L'AI Orchestrator utilizza OpenAI Responses API e native function calling per scegliere autonomamente tra:

```text
search_knowledge_base
```

e:

```text
analyze_manufacturing_data
```

o per combinarli all'interno della stessa richiesta.

La continuità conversazionale viene mantenuta tramite `sessionId` e OpenAI response identifiers.

Il Python Data Agent utilizza un approccio deterministico basato su Pandas, evitando l'esecuzione arbitraria di codice generato dal modello.

I grafici vengono prodotti tramite Matplotlib e distribuiti al frontend attraverso il Chart Proxy del backend.

La gestione degli errori distingue gli errori di input dalle indisponibilità delle dipendenze e utilizza risposte controllate per impedire la propagazione di dettagli infrastrutturali al client.

L'architettura risultante soddisfa gli obiettivi principali del progetto:

- singola interfaccia conversazionale;
- routing autonomo dell'LLM;
- Retrieval-Augmented Generation;
- analisi di dati strutturati;
- supporto bilingue;
- memoria conversazionale;
- visualizzazione dei grafici;
- separazione tra servizi;
- configurazione sicura tramite environment variables;
- comportamento testabile e riproducibile.

La semplicità del contratto pubblico consente inoltre di evolvere RAG, Data Agent e orchestrazione AI senza richiedere modifiche sostanziali al frontend.

Maranello AI mantiene quindi una separazione chiara tra:

```text
User Experience
      |
      v
Application Orchestration
      |
      +------ Knowledge Retrieval
      |
      +------ Data Analysis
```

fornendo una base coerente per una possibile evoluzione futura verso un sistema enterprise più persistente, sicuro, osservabile e scalabile.

---

## Stato del documento

| Informazione | Valore |
|--------------|--------|
| Documento | API Specification |
| Versione | 2.0 |
| Stato | Final |
| Tipologia | As-Built API |
| Lingua | Italiano |
| Ultimo aggiornamento | Settembre 2026 |

---