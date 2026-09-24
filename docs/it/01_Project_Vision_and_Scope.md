# Project Vision and Scope

> **Progetto:** Maranello AI  
> **Versione:** 2.0  
> **Tipo documento:** Project Vision & Scope  
> **Stato:** Final  
> **Autore:** Marco Saccani  
> **Ultimo aggiornamento:** Settembre 2026

---

# Indice

1. Project Vision
   - 1.1 Nome del progetto
   - 1.2 Panoramica del progetto
   - 1.3 Contesto aziendale
   - 1.4 Problema di business
   - 1.5 Soluzione realizzata
   - 1.6 Esempi di richieste
   - 1.7 Obiettivi del progetto
   - 1.8 Valore del progetto
   - 1.9 Stakeholder
   - 1.10 Vision Statement

2. Project Scope
   - 2.1 Ambito del progetto
   - 2.2 Componenti del sistema
   - 2.3 Funzionalità incluse
   - 2.4 Architettura generale
   - 2.5 Deliverable del progetto
   - 2.6 Funzionalità escluse
   - 2.7 Vincoli del progetto
   - 2.8 Criteri di successo
   - 2.9 Evoluzioni future

---

# 1. Project Vision

## 1.1 Nome del progetto

**Maranello AI**

Maranello AI è un assistente AI enterprise dimostrativo progettato per supportare il reparto **Quality & Manufacturing Operations** di un produttore automotive fittizio di alta gamma.

Il nome e il contesto del progetto richiamano il distretto industriale di Maranello, ma l'azienda, i dati, le policy, le procedure e gli scenari utilizzati sono completamente fittizi.

Il progetto non è affiliato, sponsorizzato o approvato da Ferrari N.V. o da altre aziende realmente esistenti.

Questa scelta permette di rappresentare un caso d'uso automotive realistico mantenendo una separazione chiara tra il progetto dimostrativo e qualsiasi organizzazione o informazione aziendale reale.

---

## 1.2 Panoramica del progetto

Maranello AI realizza una piattaforma conversazionale capace di comprendere richieste formulate in linguaggio naturale e utilizzare autonomamente gli strumenti necessari per produrre una risposta supportata dalle fonti disponibili.

Il sistema integra in un'unica applicazione tre capacità principali:

- consultazione della documentazione aziendale mediante Retrieval-Augmented Generation (RAG);
- analisi di dati strutturati mediante un Python Data Agent dedicato;
- combinazione di conoscenza documentale e risultati quantitativi per richieste Hybrid.

L'utente interagisce esclusivamente attraverso una chat React e non deve conoscere la struttura interna del sistema né selezionare manualmente il componente da utilizzare.

La decisione viene gestita dal Large Language Model attraverso native function calling.

Il modello può:

- rispondere direttamente quando non è necessario utilizzare una fonte aziendale;
- utilizzare il motore RAG per consultare la Knowledge Base;
- delegare un'analisi quantitativa al Python Data Agent;
- utilizzare entrambi gli strumenti quando la domanda richiede dati e policy.

Il progetto adotta un'architettura modulare a microservizi composta principalmente da:

- React Frontend;
- Node.js Backend;
- OpenAI Responses API;
- RAG Engine;
- ChromaDB;
- Python Data Agent;
- Manufacturing Dataset.

L'obiettivo è dimostrare un pattern architetturale enterprise nel quale il Large Language Model svolge principalmente una funzione di ragionamento, orchestrazione e sintesi, mentre documenti e dati rimangono affidati a componenti specializzati.

---

## 1.3 Contesto aziendale

Il reparto **Quality & Manufacturing Operations** opera in un contesto nel quale le decisioni richiedono frequentemente l'utilizzo combinato di conoscenza procedurale e dati produttivi.

Le informazioni rilevanti appartengono principalmente a due categorie.

### Documentazione aziendale

Le attività operative sono supportate da documenti quali:

- policy di qualità;
- procedure di gestione delle non conformità;
- procedure relative alla qualità dei fornitori;
- procedure di rilavorazione e scarto;
- regole di escalation produttiva;
- standard e linee guida operative.

In un'organizzazione reale, queste informazioni possono essere distribuite tra repository differenti e risultare difficili da individuare rapidamente.

Maranello AI rappresenta questo scenario attraverso una Knowledge Base aziendale fittizia e controllata, progettata specificamente per il progetto.

### Dati di produzione

Parallelamente, il reparto utilizza dati strutturati relativi ai processi produttivi.

Tra le informazioni rappresentate nel Manufacturing Dataset sono presenti:

- batch di produzione;
- date di produzione;
- plant;
- linee produttive;
- modelli di veicolo;
- turni;
- unità prodotte;
- unità difettose;
- categorie di difetto;
- rilavorazioni;
- scarti;
- downtime;
- cycle time;
- quality score;
- supplier;
- categorie di componente;
- stato delle ispezioni;
- team operativi.

Queste informazioni permettono di calcolare KPI e identificare trend o differenze tra le principali dimensioni produttive.

La separazione tra documentazione e dati costituisce il problema centrale affrontato dal progetto.

---

## 1.4 Problema di business

Maranello AI nasce per rappresentare tre criticità tipiche di un ambiente enterprise.

### Ricerca delle informazioni

La documentazione operativa può essere difficile da consultare quando:

- è distribuita tra fonti differenti;
- non è organizzata secondo una struttura uniforme;
- contiene procedure specialistiche;
- richiede tempo per individuare la sezione pertinente;
- utilizza terminologia specifica del dominio.

La conseguenza è un aumento del tempo necessario per ottenere una risposta operativa verificabile.

### Analisi dei dati

Le informazioni quantitative richiedono normalmente strumenti e competenze differenti rispetto a quelli utilizzati per consultare la documentazione.

Tra le attività analitiche rilevanti rientrano:

- calcolo dei KPI;
- analisi del defect rate;
- analisi del rework rate;
- analisi dello scrap rate;
- confronto tra linee produttive;
- confronto tra turni;
- valutazione dei supplier;
- confronto tra component category;
- analisi dei trend temporali;
- generazione di grafici.

L'utente può quindi conoscere la domanda di business senza necessariamente conoscere il codice o le operazioni analitiche necessarie per ottenere il risultato.

### Mancanza di integrazione

Il problema più significativo emerge quando una decisione richiede contemporaneamente dati e documentazione.

Per esempio, conoscere il defect rate di un supplier non è sempre sufficiente.

Può essere necessario determinare:

1. quale supplier presenta il valore più significativo;
2. quale valore è stato osservato;
3. quale procedura aziendale si applica;
4. come la procedura classifica tale valore;
5. quale comportamento operativo è previsto.

Senza integrazione, queste attività richiedono strumenti differenti e una successiva interpretazione manuale.

Maranello AI riduce questa frammentazione offrendo un unico punto di accesso conversazionale.

---

## 1.5 Soluzione realizzata

Maranello AI utilizza un Large Language Model come motore di orchestrazione.

L'LLM riceve la domanda dell'utente e decide autonomamente se siano necessari strumenti esterni.

Gli strumenti principali disponibili sono:

    search_knowledge_base

e:

    analyze_manufacturing_data

Il primo consente di recuperare conoscenza aziendale dalla Knowledge Base.

Il secondo delega l'elaborazione quantitativa al Python Data Agent.

Il sistema supporta quattro comportamenti principali.

### Risposta conversazionale diretta

Quando una domanda non richiede dati aziendali o documentazione interna, il modello può produrre una risposta senza utilizzare strumenti.

Il sistema evita quindi di interrogare inutilmente RAG o Data Agent.

### Modalità RAG

Quando la domanda riguarda policy o procedure aziendali, il modello utilizza:

    search_knowledge_base

Il processo comprende:

    User Question
          ↓
    LLM Tool Selection
          ↓
    RAG Connector
          ↓
    Embedding
          ↓
    ChromaDB
          ↓
    Relevant Knowledge Base Chunks
          ↓
    LLM
          ↓
    Grounded Answer

La Knowledge Base contiene esclusivamente documentazione fittizia creata per il progetto.

Il retrieval utilizza embedding semantici e mantiene informazioni relative alla provenienza dei contenuti recuperati.

L'obiettivo è evitare che una policy aziendale venga sostituita da conoscenza generale non verificata del modello.

### Modalità Data Analysis

Quando la richiesta richiede un'analisi quantitativa, il modello utilizza:

    analyze_manufacturing_data

Il Backend delega quindi la richiesta al Python Data Agent basato su FastAPI, Pandas e DuckDB.

Pandas viene utilizzato per il caricamento e il cleaning deterministico del dataset, mentre DuckDB costituisce il layer analitico embedded utilizzato per persistenza locale, filtering e aggregazioni.

Il Data Agent può:

- caricare e pulire il Manufacturing Dataset;
- materializzare il dataset preparato nel database DuckDB locale;
- calcolare KPI globali tramite query deterministiche;
- aggregare i risultati per dimensioni supportate;
- analizzare trend mensili;
- generare grafici tramite Matplotlib;
- restituire risultati strutturati al Backend.

L'interpretazione analitica è intenzionalmente deterministica.

Il servizio non esegue arbitrariamente codice Python generato dal Large Language Model, ma riconduce le richieste a operazioni analitiche supportate e validate.

Questa scelta migliora:

- sicurezza;
- riproducibilità;
- testabilità;
- prevedibilità dei risultati numerici.

### Modalità Hybrid

Le richieste più significative possono richiedere contemporaneamente evidenze quantitative e conoscenza procedurale.

In questi casi il modello può utilizzare entrambi gli strumenti:

    analyze_manufacturing_data
              +
    search_knowledge_base
              ↓
       LLM Synthesis
              ↓
        Final Answer

Un esempio è la valutazione di un supplier.

Il Data Agent può identificare il defect rate osservato, mentre la Knowledge Base fornisce le soglie della Supplier Quality Procedure.

Il modello combina quindi:

- evidenza numerica;
- policy applicabile;
- classificazione;
- eventuale procedura di escalation.

Questa capacità Hybrid rappresenta la caratteristica distintiva di Maranello AI rispetto a una semplice chat RAG o a un'interfaccia di analisi dati isolata.

---

## 1.6 Esempi di richieste

Gli esempi seguenti rappresentano scenari coerenti con le capacità implementate nella versione finale.

### Richieste documentali — RAG

| Richiesta | Componente principale |
|-----------|-----------------------|
| Qual è la soglia critica del defect rate secondo la Quality Policy? | RAG |
| Come deve essere gestita una non conformità? | RAG |
| Quali soglie utilizza la Supplier Quality Procedure? | RAG |
| Quando è necessaria un'escalation produttiva? | RAG |
| Quali regole si applicano a rework e scrap? | RAG |

### Richieste analitiche — Data Agent

| Richiesta | Componente principale |
|-----------|-----------------------|
| Qual è il defect rate complessivo? | Data Agent |
| Quale linea produttiva presenta il defect rate più elevato? | Data Agent |
| Quale supplier presenta il defect rate più elevato? | Data Agent |
| Confronta il defect rate tra i turni. | Data Agent |
| Mostrami il trend mensile del defect rate. | Data Agent |
| Genera il grafico del trend mensile del defect rate. | Data Agent |

### Richieste Hybrid

| Richiesta | Componenti principali |
|-----------|------------------------|
| Quale supplier presenta il defect rate più elevato e come viene classificato dalla Supplier Quality Procedure? | RAG + Data Agent |
| Analizza il defect rate e confrontalo con le soglie della Quality Policy. | RAG + Data Agent |
| Il valore osservato richiede un'escalation secondo la policy aziendale? | RAG + Data Agent |

### Richieste multi-turn

Maranello AI supporta inoltre riferimenti derivati dalla conversazione precedente.

Esempio:

    User:
    Which supplier has the highest defect rate?

    Assistant:
    SUP-07 ...

    User:
    What does the policy say about that supplier?

Il sistema mantiene il contesto della conversazione e può interpretare il riferimento:

    that supplier

utilizzando lo stato della sessione e la continuità fornita dalla Responses API.

---

## 1.7 Obiettivi del progetto

Gli obiettivi finali di Maranello AI sono:

| ID | Obiettivo |
|----|-----------|
| OBJ-01 | Centralizzare l'accesso conversazionale alla conoscenza aziendale. |
| OBJ-02 | Ridurre la complessità necessaria per reperire informazioni operative. |
| OBJ-03 | Rendere accessibili analisi quantitative tramite linguaggio naturale. |
| OBJ-04 | Integrare documentazione e dati all'interno della stessa esperienza utente. |
| OBJ-05 | Utilizzare un LLM per il routing autonomo tra differenti strumenti. |
| OBJ-06 | Dimostrare un'architettura AI modulare basata su servizi specializzati. |
| OBJ-07 | Fornire risposte RAG grounded nella Knowledge Base. |
| OBJ-08 | Garantire risultati numerici deterministici attraverso il Python Data Agent. |
| OBJ-09 | Supportare conversazioni in italiano e inglese. |
| OBJ-10 | Supportare conversazioni multi-turn mantenendo il contesto della sessione. |
| OBJ-11 | Integrare visualizzazioni grafiche direttamente nell'esperienza conversazionale. |
| OBJ-12 | Realizzare un progetto tecnicamente documentato e riutilizzabile come portfolio professionale. |

---

## 1.8 Valore del progetto

Maranello AI non rappresenta semplicemente un chatbot aziendale.

Il valore del progetto deriva dalla capacità di utilizzare una singola interfaccia conversazionale per accedere a capacità differenti mantenendo separate le responsabilità tecniche.

Dal punto di vista dell'utente, il sistema riduce la necessità di conoscere:

- posizione dei documenti;
- struttura della Knowledge Base;
- linguaggi di query;
- codice Python;
- formule dei KPI;
- strumenti di visualizzazione;
- modalità di selezione dei servizi.

L'utente formula invece una domanda in linguaggio naturale.

Dal punto di vista architetturale:

    User
      ↓
    Conversational Interface
      ↓
    AI Orchestration
      ↓
    Appropriate Enterprise Capability

I principali benefici dimostrati dal progetto sono:

- accesso semplificato alla conoscenza;
- riduzione della frammentazione tra documenti e dati;
- analisi quantitative accessibili in linguaggio naturale;
- supporto decisionale basato su fonti controllate;
- integrazione tra evidenza numerica e procedure;
- esperienza bilingue;
- visualizzazione dei risultati;
- gestione della continuità conversazionale.

Dal punto di vista tecnico, il progetto dimostra l'integrazione di:

- Large Language Models;
- OpenAI Responses API;
- native function calling;
- Retrieval-Augmented Generation;
- semantic embeddings;
- ChromaDB;
- Python;
- FastAPI;
- Pandas;
- DuckDB;
- Matplotlib;
- Node.js;
- Express;
- React;
- TypeScript;
- REST API.

---

## 1.9 Stakeholder

Gli stakeholder rappresentano i principali profili che potrebbero beneficiare da un sistema equivalente in un contesto enterprise.

| Stakeholder | Interesse principale |
|-------------|----------------------|
| Quality Engineer | Consultazione delle procedure e analisi degli indicatori di qualità. |
| Manufacturing Engineer | Analisi di linee, turni, trend e anomalie produttive. |
| Supplier Quality Engineer | Valutazione delle performance dei supplier e consultazione delle relative procedure. |
| Production Manager | Supporto alla valutazione delle performance produttive e delle escalation. |
| Quality Manager | Accesso combinato a evidenze quantitative e policy di qualità. |
| AI / Software Engineer | Evoluzione, manutenzione e integrazione della piattaforma. |

Questi stakeholder rappresentano profili di riferimento del business scenario e non utenti reali del sistema dimostrativo.

La versione corrente non implementa autenticazione o Role-Based Access Control.

---

## 1.10 Vision Statement

La visione di Maranello AI è dimostrare come un assistente AI enterprise possa trasformare l'accesso alla conoscenza aziendale e l'analisi dei dati in un'unica esperienza conversazionale.

Il sistema riduce la complessità tecnologica percepita dall'utente delegando all'orchestratore AI la selezione delle capacità necessarie.

La visione architetturale può essere sintetizzata come:

    Ask one question
          ↓
    AI determines what is needed
          ↓
    Retrieve knowledge and/or analyze data
          ↓
    Combine verified evidence
          ↓
    Return one contextual answer

Il Large Language Model non viene utilizzato come unica fonte di verità.

Le responsabilità vengono invece separate:

    LLM
    reasoning, routing and synthesis

    Knowledge Base
    company policies and procedures

    Python Data Agent
    deterministic numerical analysis

    Backend
    orchestration and application state

    Frontend
    conversational user experience

Maranello AI rappresenta quindi una dimostrazione concreta di come RAG, tool calling, analisi strutturata dei dati e interazione conversazionale possano essere integrati in un'architettura coerente, verificabile ed estendibile.

---

# 2. Project Scope

## 2.1 Ambito del progetto

Maranello AI realizza un assistente AI enterprise dimostrativo per il dominio **Quality & Manufacturing Operations** di un produttore automotive fittizio.

Lo scope implementato comprende l'intero flusso necessario per consentire a un utente di:

- interagire con il sistema attraverso una chat;
- formulare richieste in italiano o inglese;
- consultare documentazione aziendale fittizia;
- analizzare un dataset manifatturiero strutturato;
- ottenere KPI e confronti quantitativi;
- richiedere trend temporali;
- visualizzare grafici;
- combinare risultati numerici e procedure aziendali;
- continuare una conversazione mantenendo il contesto.

L'utente non seleziona manualmente il servizio da utilizzare.

La scelta tra risposta diretta, RAG, Data Analysis e comportamento Hybrid viene effettuata autonomamente dal Large Language Model attraverso native function calling.

Lo scope finale può essere rappresentato come:

    User
      ↓
    React Conversational Interface
      ↓
    Node.js Backend
      ↓
    AI Orchestration
      ↓
    ┌──────────────────────┬─────────────────────────┐
    │                      │                         │
    ▼                      ▼                         ▼
    Direct Answer     Knowledge Retrieval      Data Analysis
                           │                         │
                           ▼                         ▼
                        ChromaDB              Python Data Agent
                           │                         │
                           ▼                         ▼
                    Knowledge Base           Manufacturing Dataset
    │                      │                         │
    └──────────────────────┴─────────────────────────┘
                           ↓
                    Response Synthesis
                           ↓
                         User

Il progetto dimostra quindi l'integrazione tra AI generativa, retrieval documentale e analisi strutturata dei dati all'interno di una singola esperienza conversazionale.

---

## 2.2 Componenti del sistema

L'architettura finale comprende i seguenti componenti principali.

### React Frontend

Il Frontend costituisce l'unico punto di interazione diretta dell'utente.

Le responsabilità principali comprendono:

- rendering della chat;
- gestione dei messaggi;
- input dell'utente;
- stato di loading/typing;
- visualizzazione delle risposte;
- gestione degli errori;
- mantenimento del `sessionId`;
- rendering dei grafici;
- comunicazione con il Backend.

Il Frontend non comunica direttamente con:

- OpenAI API;
- Python Data Agent;
- ChromaDB.

Tutte le richieste applicative passano attraverso il Backend Node.js.

### Node.js Backend

Il Backend Node.js ed Express rappresenta il gateway applicativo e il principale livello di orchestrazione.

Le responsabilità comprendono:

- esposizione delle REST API;
- validazione degli input;
- gestione delle conversazioni;
- integrazione con OpenAI Responses API;
- esposizione dei tool al modello;
- esecuzione dei function call;
- integrazione con ChromaDB;
- integrazione con il Python Data Agent;
- costruzione della risposta finale;
- gestione dei grafici tramite Chart Proxy;
- gestione centralizzata degli errori.

Il Backend mantiene inoltre lo stato conversazionale in-memory per la durata della sessione applicativa.

### AI Orchestration

Il Large Language Model viene utilizzato attraverso la OpenAI Responses API.

Il modello riceve la domanda dell'utente e può utilizzare due tool principali:

    search_knowledge_base

    analyze_manufacturing_data

La selezione viene effettuata attraverso native function calling.

Il modello può quindi:

- non utilizzare alcun tool;
- utilizzare il tool RAG;
- utilizzare il Data Agent;
- utilizzare entrambi.

Il Backend gestisce l'esecuzione dei tool e restituisce i relativi output al modello fino alla produzione della risposta finale.

### RAG Engine

Il componente RAG consente di recuperare informazioni dalla Knowledge Base aziendale fittizia.

Il flusso comprende:

    User Question
          ↓
    search_knowledge_base
          ↓
    Semantic Embedding
          ↓
    ChromaDB
          ↓
    Relevant Chunks
          ↓
    Source Metadata
          ↓
    LLM

Il retrieval utilizza il modello di embedding configurato per il progetto e supporta query in italiano e inglese.

### ChromaDB

ChromaDB viene utilizzato come vector database locale.

La Knowledge Base finale comprende cinque documenti operativi principali indicizzati in:

    149 chunks

Il vector database memorizza embedding e metadata necessari al retrieval semantico.

### Knowledge Base

La Knowledge Base contiene documentazione aziendale completamente fittizia creata specificamente per il progetto.

I documenti principali sono:

    knowledge_base/
    ├── README.md
    ├── manufacturing_quality_policy.md
    ├── non_conformity_procedure.md
    ├── supplier_quality_procedure.md
    ├── rework_and_scrap_procedure.md
    └── production_escalation_policy.md

I documenti definiscono policy e procedure coerenti con il business scenario di Quality & Manufacturing Operations.

### Python Data Agent

Il Data Agent è un microservizio FastAPI responsabile delle analisi quantitative.

Utilizza principalmente:

- Python;
- FastAPI;
- Pandas;
- DuckDB;
- Matplotlib.

Il componente:

- riceve una richiesta analitica dal Backend;
- interpreta la dimensione richiesta;
- utilizza il Manufacturing Dataset;
- esegue operazioni deterministiche di loading e cleaning tramite Pandas;
- materializza il dataset preparato nel database DuckDB locale;
- esegue KPI, aggregazioni e trend tramite query DuckDB controllate;
- genera grafici quando necessario;
- restituisce il risultato al Backend.

L'approccio è intenzionalmente deterministico.

Il servizio non esegue arbitrariamente codice Python generato dall'LLM.

### Manufacturing Dataset

Il dataset sintetico contiene:

    2000 rows
    20 columns

Ogni record rappresenta un batch produttivo.

Il dataset contiene:

- metriche numeriche;
- categorie;
- date;
- informazioni relative a linee e plant;
- supplier;
- component category;
- turni;
- indicatori di qualità;
- anomalie intenzionali;
- missing values;
- duplicati;
- outlier.

Sono inoltre presenti relazioni sintetiche controllate che permettono di ottenere pattern analitici verificabili.

---

## 2.3 Funzionalità incluse

Le funzionalità implementate vengono suddivise nelle seguenti macro-aree.

### Conversational Interface

Il sistema supporta:

- chat utente-assistente;
- messaggi multi-turn;
- stato di loading;
- gestione degli errori;
- visualizzazione dei grafici;
- conversazioni in italiano e inglese.

### Conversation Memory

Il Backend gestisce sessioni conversazionali attraverso:

- `sessionId`;
- storico dei messaggi;
- `lastResponseId`.

Quando disponibile, il riferimento all'ultima risposta viene utilizzato attraverso:

    previous_response_id

nelle chiamate successive alla Responses API.

Questo permette di mantenere la continuità della conversazione.

### Autonomous Tool Routing

L'LLM decide autonomamente quali capacità utilizzare.

Sono supportati:

    Direct
    RAG
    Data Analysis
    Hybrid

Non è presente una route HTTP separata per ciascun comportamento.

Il routing avviene internamente attraverso function calling.

### Knowledge Retrieval

Il sistema può:

- effettuare retrieval semantico;
- interrogare ChromaDB;
- recuperare chunk rilevanti;
- utilizzare metadata relativi alla fonte;
- rispondere utilizzando il contesto documentale;
- recuperare contenuti inglesi a partire da domande italiane.

### Data Analysis

Il Data Agent supporta:

- KPI globali;
- analisi per `production_line`;
- analisi per `shift`;
- analisi per `supplier_id`;
- analisi per `component_category`;
- analisi per `vehicle_model`;
- analisi per `plant`;
- analisi per `operator_team`;
- trend mensile.

Tra i KPI calcolati sono presenti:

- total production;
- defective units;
- defect rate;
- rework rate;
- scrap rate;
- average quality score;
- average downtime;
- average cycle time.

### Data Cleaning

Il Data Agent gestisce le anomalie introdotte intenzionalmente nel dataset.

Il processo comprende:

- rimozione dei duplicati;
- normalizzazione dei valori testuali;
- parsing di date con formati differenti;
- gestione dei missing values;
- gestione di quality score non validi;
- identificazione di record numericamente incoerenti;
- gestione controllata degli outlier.

### Chart Generation

Il Data Agent genera grafici PNG attraverso Matplotlib.

Il flusso finale è:

    Analytical Request
          ↓
    Python Data Agent
          ↓
    Matplotlib
          ↓
    Generated PNG
          ↓
    Backend Chart Proxy
          ↓
    React Frontend

Il Frontend non accede direttamente al microservizio Python.

### Hybrid Reasoning

Il sistema può utilizzare nello stesso processo:

    quantitative evidence
             +
    company policy

Per esempio:

    Supplier defect rate
             +
    Supplier Quality Procedure
             ↓
    Contextual Classification

Questo comportamento permette di trasformare un semplice KPI in una risposta contestualizzata rispetto alle regole aziendali.

### Multilingual Interaction

Il sistema supporta:

    Italian question
          ↓
    Italian answer

e:

    English question
          ↓
    English answer

Non viene richiesto all'utente di selezionare manualmente la lingua.

### Controlled Failure Handling

Quando una fonte necessaria non è disponibile, il sistema utilizza un errore controllato.

Sono gestiti in particolare:

- Data Agent unavailable;
- ChromaDB unavailable.

In questi casi il Backend restituisce una risposta HTTP controllata anziché permettere al modello di inventare dati o policy.

---

## 2.4 Architettura generale

L'architettura finale è composta da servizi con responsabilità separate.

    ┌──────────────────────────────┐
    │        React Frontend        │
    │   Conversational Interface  │
    └──────────────┬───────────────┘
                   │
                   │ HTTP
                   ▼
    ┌──────────────────────────────┐
    │     Node.js / Express        │
    │           Backend            │
    │                              │
    │ - REST API                   │
    │ - Conversation Manager       │
    │ - AI Orchestration           │
    │ - Tool Execution             │
    │ - Error Handling             │
    │ - Chart Proxy                │
    └──────────┬───────────┬───────┘
               │           │
               │           │
               ▼           ▼
    ┌────────────────┐   ┌────────────────────┐
    │    ChromaDB    │   │ Python Data Agent  │
    │                │   │      FastAPI       │
    │ Vector Store   │   │  Pandas + DuckDB   │
    └───────┬────────┘   │     Matplotlib     │
            │            └─────────┬──────────┘
            ▼                      │
    ┌────────────────┐             ▼
    │ Knowledge Base │   ┌────────────────────┐
    │                │   │ CSV Source Dataset │
    │ Fictional Docs │   │ + DuckDB Runtime   │
    └────────────────┘   └────────────────────┘

                   Node.js Backend
                          │
                          ▼
                  OpenAI Responses API
                          │
                          ▼
                Native Function Calling

La separazione permette di mantenere indipendenti:

- esperienza utente;
- orchestrazione;
- retrieval;
- analisi numerica;
- persistenza vettoriale;
- provider AI.

---

## 2.5 Deliverable del progetto

I deliverable tecnici comprendono:

### Source Code

Repository contenente:

- `frontend/`;
- `backend/`;
- `data_agent/`;
- Knowledge Base;
- Manufacturing Dataset;
- test;
- configurazioni;
- documentazione.

### Frontend

Applicazione React contenente:

- interfaccia chat;
- gestione dello stato;
- loading indicator;
- error handling;
- rendering delle risposte;
- rendering dei grafici.

### Backend

Servizio Node.js contenente:

- REST API;
- Conversation Manager;
- AI orchestration;
- OpenAI integration;
- RAG connector;
- Data Agent connector;
- Chart Proxy;
- error handling.

### Python Data Agent

Microservizio FastAPI contenente:

- data loading;
- data cleaning;
- Question Interpreter;
- KPI calculation;
- grouped analysis;
- monthly trend analysis;
- chart generation.

### Manufacturing Dataset

Dataset CSV sintetico con almeno 1000 righe, realizzato nella versione finale con:

    2000 rows

e anomalie intenzionali utilizzate per dimostrare il processo di cleaning.

### Knowledge Base

Documentazione aziendale fittizia relativa al dominio Quality & Manufacturing Operations.

### Technical Documentation

La documentazione tecnica principale comprende:

- Project Vision and Scope;
- Software Requirements Specification;
- System Architecture Document;
- Data Model;
- API Specification;
- Test Plan;
- README finale.

La documentazione tecnica principale è mantenuta in italiano, mentre codice, identificatori tecnici, API e documentazione interna al codice utilizzano convenzioni tecniche in inglese.

### Final Presentation

La consegna finale prevede una presentazione PDF/PPTX contenente:

- business problem;
- valore della soluzione;
- architettura;
- autonomous routing;
- RAG;
- Data Agent;
- screenshot dell'applicazione;
- scenario RAG;
- scenario Data Analysis con grafico;
- scenario Hybrid;
- challenge tecniche;
- debugging;
- risultati;
- riferimento al repository GitHub.

La presentazione viene finalizzata dopo la chiusura della documentazione tecnica.

---

## 2.6 Funzionalità escluse

Le seguenti funzionalità non fanno parte dell'implementazione finale corrente:

- autenticazione enterprise;
- Single Sign-On;
- Role-Based Access Control effettivo;
- database aziendali reali;
- integrazione ERP;
- integrazione MES;
- integrazione con sensori industriali;
- dati produttivi reali;
- modifica automatica dei sistemi di produzione;
- esecuzione di azioni operative sui macchinari;
- approvazione automatica di non conformità;
- modifica automatica delle policy;
- persistent conversation database;
- distributed session management;
- deployment cloud production-grade;
- high availability;
- disaster recovery;
- distributed tracing;
- centralized monitoring platform;
- browser E2E automation;
- formal performance testing;
- formal penetration testing;
- CI/CD completo dedicato al progetto finale.

L'esclusione mantiene il progetto focalizzato sulla dimostrazione dell'architettura AI Hybrid.

---

## 2.7 Vincoli del progetto

Il progetto è stato sviluppato rispettando diversi vincoli tecnici e di dominio.

### Fictional Business Context

Il sistema non utilizza dati aziendali riservati o documentazione interna di aziende reali.

Dataset e Knowledge Base sono stati creati specificamente per il progetto.

### Local Architecture

I principali servizi applicativi vengono eseguiti localmente durante sviluppo, testing e dimostrazione.

### External AI Provider

Le funzionalità di orchestrazione e embedding dipendono dalla disponibilità del provider OpenAI e da una configurazione API valida.

### Controlled Analytical Scope

Il Data Agent supporta un insieme definito di analisi.

Non esegue arbitrariamente qualsiasi operazione Python richiesta dall'utente.

Questa scelta rappresenta un vincolo intenzionale orientato a:

- sicurezza;
- stabilità;
- riproducibilità;
- testabilità.

### In-Memory Conversation State

Lo stato conversazionale viene mantenuto in memoria dal Backend.

Un riavvio del servizio elimina le sessioni attive.

### Synthetic Data

Le analisi hanno valore dimostrativo e non rappresentano performance produttive reali.

### Local Vector Database

ChromaDB viene utilizzato localmente e non rappresenta un deployment distribuito production-grade.

---

## 2.8 Criteri di successo

Il progetto viene considerato tecnicamente riuscito quando sono soddisfatti i seguenti criteri.

| ID | Criterio | Stato |
|----|----------|-------|
| SC-01 | Interfaccia conversazionale React funzionante | PASS |
| SC-02 | Backend Node.js funzionante | PASS |
| SC-03 | Python Data Agent separato e operativo | PASS |
| SC-04 | Manufacturing Dataset con almeno 1000 righe | PASS |
| SC-05 | Knowledge Base coerente con il business scenario | PASS |
| SC-06 | Retrieval RAG tramite ChromaDB | PASS |
| SC-07 | Routing autonomo tramite LLM function calling | PASS |
| SC-08 | Analisi quantitativa deterministica tramite DuckDB, con preparazione dati tramite Pandas | PASS |
| SC-09 | Generazione dei grafici | PASS |
| SC-10 | Scenario RAG verificato | PASS |
| SC-11 | Scenario Data Analysis verificato | PASS |
| SC-12 | Scenario Hybrid verificato | PASS |
| SC-13 | Conversazione multi-turn verificata | PASS |
| SC-14 | Supporto italiano/inglese verificato | PASS |
| SC-15 | Controlled failure del Data Agent | PASS |
| SC-16 | Controlled failure di ChromaDB | PASS |
| SC-17 | Test automatici Backend superati | PASS |
| SC-18 | Build Backend e Frontend superate | PASS |
| SC-19 | Documentazione tecnica as-built | PASS |

Restano separate dai criteri di successo del software le attività finali di consegna:

- README finale;
- presentazione;
- clean clone verification;
- packaging finale.

---

## 2.9 Evoluzioni future

L'architettura è stata progettata in modo da consentire evoluzioni successive senza modificare il principio fondamentale di separazione delle responsabilità.

### Authentication and RBAC

Una futura versione potrebbe introdurre:

- autenticazione;
- Single Sign-On;
- Role-Based Access Control;
- metadata filtering della Knowledge Base.

I documenti recuperabili potrebbero dipendere dal ruolo dell'utente.

### Persistent Conversation Memory

Lo stato in-memory potrebbe essere sostituito da un datastore persistente per supportare:

- riavvio dei servizi;
- conversazioni di lunga durata;
- più istanze Backend;
- cronologia utente.

### Enterprise Data Sources

Il Manufacturing Dataset locale potrebbe essere sostituito o integrato con:

- SQL database;
- data warehouse;
- lakehouse;
- MES;
- ERP;
- API aziendali.

Il Data Agent manterrebbe il ruolo di boundary analitica.

### Advanced Analytics

Il motore analitico potrebbe essere esteso con:

- analisi multidimensionali;
- anomaly detection;
- forecasting;
- statistical testing;
- root cause analysis;
- predictive quality;
- comparative dashboards.

### Controlled Code Interpreter

Una futura versione potrebbe introdurre un interprete Python più flessibile.

Tale capacità richiederebbe:

- sandboxing;
- resource limits;
- filesystem restrictions;
- network restrictions;
- code validation;
- execution timeout;
- result validation.

La versione corrente evita intenzionalmente arbitrary code execution.

### Advanced RAG

La pipeline RAG potrebbe essere estesa con:

- metadata filtering;
- document versioning;
- hybrid search;
- reranking;
- automated ingestion;
- document approval workflow;
- role-aware retrieval;
- retrieval evaluation framework.

### Observability

Una versione production-grade potrebbe introdurre:

- centralized logging;
- metrics;
- dashboards;
- distributed tracing;
- alerting;
- LLM token monitoring;
- tool usage metrics;
- retrieval quality monitoring.

### Automated Testing

Il processo QA potrebbe essere esteso con:

- Frontend unit testing;
- component testing;
- browser E2E automation;
- automated LLM evaluation;
- performance testing;
- load testing;
- security scanning.

### Deployment

Una futura evoluzione potrebbe prevedere:

- containerizzazione;
- Docker Compose;
- cloud deployment;
- CI/CD;
- managed vector database;
- object storage per i grafici;
- horizontal scaling.

Queste evoluzioni non sono necessarie per dimostrare gli obiettivi della versione corrente, ma mostrano come l'architettura possa essere estesa verso un contesto enterprise più completo.

---

## Stato del documento

| Informazione | Valore |
|--------------|--------|
| Documento | Project Vision and Scope |
| Versione | 2.0 |
| Stato | Final |
| Tipologia | As-Built Vision & Scope |
| Lingua | Italiano |
| Ultimo aggiornamento | Settembre 2026 |

---