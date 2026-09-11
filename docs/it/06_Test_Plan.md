# Test Plan

> **Progetto:** Maranello AI  
> **Versione:** 2.0  
> **Tipo documento:** Software Test Plan  
> **Stato:** Final  
> **Autore:** Marco Saccani  
> **Ultimo aggiornamento:** Settembre 2026  

---

# Indice

1. Introduzione
2. Ambito del testing
3. Strategia di test
4. Ambiente e dati di test
5. Verifiche del Python Data Agent
6. Test automatici del Backend
7. Verifiche RAG e Knowledge Base
8. Test dell'orchestrazione AI
9. Test delle API e della resilienza
10. Verifiche del Frontend
11. Test di integrazione Full-Stack
12. Test manuali e scenari di accettazione
13. Risultati delle attività di test
14. Sicurezza e verifiche di configurazione
15. Limitazioni e attività future
16. Criteri di accettazione finale
17. Conclusioni

---

# 1. Introduzione

## 1.1 Scopo del documento

Il presente documento descrive il piano di test **as-built** di **Maranello AI**, un assistente AI enterprise dimostrativo progettato per supportare il dipartimento **Quality & Manufacturing Operations** di un produttore automotive fittizio.

Maranello AI combina:

- un'interfaccia conversazionale React;
- un Backend Node.js ed Express responsabile dell'orchestrazione;
- un Large Language Model utilizzato tramite OpenAI Responses API;
- function calling per la selezione autonoma degli strumenti;
- Retrieval-Augmented Generation basato su una Knowledge Base aziendale fittizia;
- ChromaDB come vector database locale;
- un Python Data Agent basato su FastAPI e Pandas;
- un Manufacturing Dataset sintetico;
- generazione di grafici tramite Matplotlib;
- gestione dello stato conversazionale lato Backend.

Il Test Plan documenta le verifiche effettivamente applicate alla versione finale del sistema e distingue le attività realmente eseguite dalle possibili evoluzioni future del processo di Quality Assurance.

L'obiettivo non è descrivere un'infrastruttura di testing enterprise ipotetica, ma fornire evidenze riproducibili della qualità del software effettivamente sviluppato.

---

## 1.2 Obiettivi del Test Plan

Gli obiettivi principali sono:

| ID | Obiettivo |
|----|-----------|
| TP-OBJ-001 | Verificare il corretto funzionamento dei componenti principali di Maranello AI. |
| TP-OBJ-002 | Validare il comportamento del Python Data Agent e la correttezza delle analisi deterministiche. |
| TP-OBJ-003 | Verificare il retrieval della Knowledge Base tramite ChromaDB. |
| TP-OBJ-004 | Validare il routing autonomo dell'LLM mediante function calling. |
| TP-OBJ-005 | Verificare gli scenari RAG, Data Analysis e Hybrid. |
| TP-OBJ-006 | Verificare la continuità delle conversazioni tramite sessione. |
| TP-OBJ-007 | Verificare il comportamento bilingue italiano/inglese. |
| TP-OBJ-008 | Validare i contratti API utilizzati nell'architettura finale. |
| TP-OBJ-009 | Verificare la gestione controllata degli errori e delle dipendenze non disponibili. |
| TP-OBJ-010 | Verificare la generazione e la visualizzazione dei grafici. |
| TP-OBJ-011 | Verificare che Frontend, Backend, Data Agent e ChromaDB funzionino correttamente come sistema integrato. |
| TP-OBJ-012 | Fornire evidenze sufficienti per determinare la readiness del progetto rispetto ai requisiti del capstone. |

---

## 1.3 Natura del documento

Il presente Test Plan rappresenta lo stato finale delle attività di verifica eseguite sul progetto.

Di conseguenza, nel documento vengono utilizzate tre categorie principali:

### Automated Test

Test implementati nel repository ed eseguibili automaticamente.

### Manual Verification

Verifiche eseguite manualmente sul sistema integrato attraverso API o interfaccia React.

### Future Test

Attività considerate utili per un'eventuale evoluzione production-grade, ma non implementate nella versione corrente.

Questa distinzione evita di rappresentare come implementate attività di testing che appartengono esclusivamente a possibili evoluzioni future.

---

## 1.4 Relazione con gli altri documenti

Il Test Plan deve essere interpretato insieme alla documentazione tecnica del progetto.

| Documento | Relazione con il testing |
|-----------|--------------------------|
| Project Vision and Scope | Definisce scenario, obiettivi e valore di business. |
| Software Requirements Specification | Definisce i requisiti funzionali e non funzionali da verificare. |
| System Architecture Document | Descrive l'architettura as-built e le integrazioni sottoposte a test. |
| Data Model | Definisce dataset, Knowledge Base, stato conversazionale e strutture dati. |
| API Specification | Definisce gli endpoint e i contratti utilizzati nelle verifiche API. |
| Test Plan | Documenta strategia, test eseguiti, risultati e criteri di accettazione. |

Il flusso di tracciabilità è quindi:

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
    Automated Tests + Manual QA
            ↓
    Final Acceptance

---

## 1.5 Principi di verifica

Le attività di testing sono state progettate secondo i seguenti principi.

### Riproducibilità

Le verifiche deterministiche devono produrre risultati coerenti a parità di input e dataset.

### Isolamento

Quando possibile, le unità software vengono testate indipendentemente dalle dipendenze esterne.

### Regression Prevention

Le funzionalità critiche del Backend sono protette da test automatici per ridurre il rischio di regressioni durante il refactoring.

### Integration Validation

Le integrazioni tra servizi vengono verificate anche sul sistema realmente in esecuzione.

### Controlled Failure

L'indisponibilità di una dipendenza non deve produrre errori non gestiti o risposte ingannevoli.

### AI Grounding

Le risposte relative alle policy aziendali devono utilizzare la Knowledge Base quando necessario.

### Numerical Integrity

I risultati numerici devono essere derivati dal Manufacturing Dataset attraverso il Python Data Agent e non inventati dal modello linguistico.

### Scope Preservation

L'orchestrazione deve preservare il significato della domanda originale senza introdurre filtri, dimensioni o vincoli temporali non richiesti.

### Security by Design

Segreti, input, file generati e percorsi esposti devono essere gestiti in modo controllato.

---

# 2. Ambito del testing

## 2.1 Sistema sottoposto a test

L'architettura finale sottoposta a verifica è:

    User
      │
      ▼
    React Frontend
      │
      │ HTTP
      ▼
    Node.js / Express Backend
      │
      ├── Conversation Manager
      │
      ├── OpenAI Responses API
      │       │
      │       └── Native Function Calling
      │
      ├── search_knowledge_base
      │       │
      │       ▼
      │    ChromaDB
      │       │
      │       ▼
      │  Knowledge Base
      │
      └── analyze_manufacturing_data
              │
              ▼
          Python Data Agent
              │
              ├── Pandas
              ├── Manufacturing Dataset
              └── Matplotlib

Il Frontend comunica esclusivamente con il Backend Node.js.

Il Backend rappresenta il gateway applicativo e coordina l'accesso alle dipendenze interne.

---

## 2.2 Componenti inclusi

Le verifiche coprono i seguenti componenti:

- React Frontend;
- Node.js Backend;
- API Express;
- Conversation Manager;
- OpenAI Responses API integration;
- native function calling;
- tool `search_knowledge_base`;
- tool `analyze_manufacturing_data`;
- RAG pipeline;
- ChromaDB;
- Knowledge Base;
- OpenAI embedding integration;
- Python FastAPI Data Agent;
- Question Interpreter deterministico;
- Pandas analytics;
- Manufacturing Dataset;
- data cleaning;
- KPI calculation;
- grouped analysis;
- monthly trend analysis;
- Matplotlib chart generation;
- Chart Proxy;
- gestione degli errori;
- gestione delle sessioni;
- comportamento bilingue italiano/inglese.

---

## 2.3 Flussi funzionali inclusi

Il sistema deve essere verificato rispetto a quattro comportamenti principali.

### Conversational

Il modello può rispondere direttamente quando la richiesta non richiede informazioni aziendali o analisi numeriche.

    User
      ↓
    LLM
      ↓
    Answer

### RAG

Quando la domanda richiede informazioni contenute nella Knowledge Base:

    User
      ↓
    LLM
      ↓
    search_knowledge_base
      ↓
    ChromaDB
      ↓
    Knowledge Base Context
      ↓
    LLM
      ↓
    Answer

### Data Analysis

Quando la domanda richiede calcoli sui dati produttivi:

    User
      ↓
    LLM
      ↓
    analyze_manufacturing_data
      ↓
    Python Data Agent
      ↓
    Pandas Analysis
      ↓
    LLM
      ↓
    Answer

### Hybrid

Quando la domanda richiede contemporaneamente dati quantitativi e policy aziendali:

                       ┌── search_knowledge_base ── ChromaDB
    User ── LLM ───────┤
                       └── analyze_manufacturing_data ── Data Agent
                                       │
                                       ▼
                                    Results
                                       │
                                       ▼
                                      LLM
                                       │
                                       ▼
                                    Answer

Questi comportamenti non corrispondono a route HTTP separate.

La scelta viene effettuata autonomamente dal modello attraverso il meccanismo di function calling.

---

## 2.4 Componenti esclusi

Non fanno parte dell'ambito della versione corrente:

- sistemi ERP reali;
- sistemi MES reali;
- sensori industriali;
- hardware di produzione;
- database aziendali reali;
- dati produttivi reali;
- sistemi di autenticazione enterprise;
- Role-Based Access Control effettivamente implementato;
- infrastrutture cloud production-grade;
- sistemi di monitoring centralizzati;
- distributed tracing;
- load balancing;
- high availability;
- disaster recovery;
- penetration testing formale;
- certificazioni di sicurezza;
- verifiche normative formali.

Il progetto utilizza dati, documentazione e scenario aziendale fittizi a scopo dimostrativo.

---

## 2.5 Elementi non dichiarati come implementati

Il presente Test Plan non considera come attività completate:

- pipeline CI/CD dedicate al progetto finale;
- ambienti separati Test, Staging e Production;
- suite automatizzate End-to-End nel browser;
- test automatici di performance;
- load test;
- stress test;
- penetration test;
- accessibility audit formale;
- contract testing mediante framework dedicati;
- chaos engineering;
- test automatici di rollback;
- security scanning automatizzato come release gate;
- report automatici di test enterprise.

Queste attività possono costituire evoluzioni future, ma non vengono utilizzate come evidenza della qualità della versione corrente.

---

# 3. Strategia di test

## 3.1 Approccio generale

La strategia effettivamente adottata combina:

    Static Validation
            ↓
    Automated Tests
            ↓
    Component Verification
            ↓
    API Verification
            ↓
    Integration Testing
            ↓
    Manual Full-Stack QA
            ↓
    Acceptance Verification

L'obiettivo è verificare progressivamente il sistema partendo dalle componenti più deterministiche fino ai comportamenti che dipendono dal Large Language Model.

---

## 3.2 Static validation

Prima delle verifiche integrate vengono utilizzati gli strumenti di controllo statico previsti dai singoli componenti.

Per il Backend vengono verificati:

- TypeScript type checking;
- linting;
- build.

Per il Frontend vengono verificati:

- linting;
- build di produzione.

Per il codice Python vengono utilizzati controlli coerenti con la struttura e gli strumenti definiti nel progetto.

Queste verifiche permettono di intercettare errori sintattici, problemi di tipizzazione e problemi di qualità del codice prima dell'esecuzione del sistema completo.

---

## 3.3 Test automatici

La parte maggiormente automatizzata riguarda il Backend Node.js.

La suite finale comprende:

    15 test files
    86 automated tests

I test verificano moduli e comportamenti critici dell'orchestrazione, riducendo il rischio di regressioni.

L'esecuzione finale ha prodotto esito positivo per:

    Type Check    PASS
    Lint          PASS
    Tests         PASS
    Build         PASS

I dettagli delle aree coperte vengono documentati nelle sezioni successive.

---

## 3.4 Verifiche deterministiche

Il Python Data Agent è stato progettato per rendere deterministica la parte numerica del sistema.

Le verifiche riguardano principalmente:

- caricamento del CSV;
- data cleaning;
- rimozione dei duplicati;
- normalizzazione dei valori;
- gestione delle anomalie;
- calcolo dei KPI;
- aggregazioni;
- trend temporali;
- interpretazione delle dimensioni supportate;
- rifiuto di richieste analitiche ambigue o non supportate;
- generazione dei grafici.

La separazione tra orchestrazione AI e calcolo deterministico permette di verificare i risultati numerici indipendentemente dalla variabilità del modello linguistico.

---

## 3.5 Verifiche AI

Le funzionalità dipendenti dal modello non vengono valutate confrontando rigidamente l'intero testo della risposta.

Vengono invece verificati gli aspetti funzionali osservabili:

- strumento selezionato;
- presenza delle informazioni richieste;
- correttezza dei dati utilizzati;
- utilizzo della Knowledge Base quando necessario;
- utilizzo del Data Agent quando necessario;
- utilizzo combinato dei tool nei casi Hybrid;
- conservazione del contesto conversazionale;
- lingua della risposta;
- assenza di vincoli analitici non richiesti;
- comportamento in caso di dipendenze non disponibili.

Questo approccio tiene conto della natura non completamente deterministica della generazione linguistica mantenendo verificabili le decisioni architetturali critiche.

---

## 3.6 Verifiche di integrazione

Le verifiche di integrazione vengono eseguite con i servizi locali realmente avviati:

    React Frontend        :5173
    Node.js Backend       :3000
    Python Data Agent     :8001
    ChromaDB              :8000

Le integrazioni principali verificate sono:

    React
      ↓
    Node.js Backend
      ↓
    OpenAI Responses API

    Node.js Backend
      ↓
    ChromaDB

    Node.js Backend
      ↓
    Python Data Agent

    Python Data Agent
      ↓
    Manufacturing Dataset

    Python Data Agent
      ↓
    Generated Chart

    React
      ↓
    Node Chart Proxy
      ↓
    Python Chart

---

## 3.7 Negative e resilience testing

Sono state verificate anche condizioni anomale significative.

Tra queste:

- messaggio vuoto;
- messaggio composto esclusivamente da spazi;
- Data Agent non disponibile;
- Knowledge Base/ChromaDB non disponibile;
- richieste analitiche non supportate;
- richieste con scope ambiguo;
- accesso ai grafici attraverso il proxy controllato;
- validazione dei filename;
- protezione da path traversal nel Chart Proxy.

L'obiettivo è assicurare che un errore tecnico non venga trasformato in una risposta apparentemente valida ma non supportata dai dati.

---

## 3.8 Testing bilingue

Il sistema viene verificato utilizzando richieste sia in italiano sia in inglese.

La lingua non viene inviata come parametro API separato.

Il comportamento atteso è:

    Italian question
          ↓
    Italian answer

    English question
          ↓
    English answer

Le verifiche bilingui interessano:

- richieste conversazionali;
- retrieval RAG;
- richieste numeriche;
- richieste Hybrid;
- continuità conversazionale.

---

## 3.9 Test della memoria conversazionale

La gestione dello stato viene verificata attraverso conversazioni multi-turn.

Il Backend conserva:

- `sessionId`;
- messaggi della conversazione;
- `lastResponseId`.

Quando disponibile, `lastResponseId` viene utilizzato con `previous_response_id` nelle successive chiamate alla OpenAI Responses API.

Un test significativo consiste nel verificare che un riferimento successivo possa essere interpretato utilizzando il contesto precedente.

Esempio:

    User:
    Which supplier has the highest defect rate?

    Assistant:
    SUP-07 ...

    User:
    What does the policy say about that supplier?

Il sistema deve poter interpretare il riferimento contestuale senza richiedere all'utente di ripetere l'identificativo del supplier.

---

## 3.10 Test della generazione dei grafici

Le verifiche relative ai grafici comprendono l'intero percorso:

    Analytical Question
            ↓
    Python Data Agent
            ↓
    Matplotlib
            ↓
    PNG File
            ↓
    Internal /charts/:filename
            ↓
    Backend Chart Proxy
            ↓
    /api/charts/:filename
            ↓
    React
            ↓
    Rendered Image

Il test non riguarda quindi soltanto la creazione del file, ma anche la sua corretta esposizione attraverso il Backend e la visualizzazione nell'interfaccia.

---

## 3.11 Criterio generale di successo

Una funzionalità viene considerata verificata quando:

1. i controlli statici applicabili risultano superati;
2. i test automatici relativi risultano superati;
3. le integrazioni necessarie sono operative;
4. il comportamento osservato corrisponde al requisito;
5. gli errori previsti vengono gestiti in modo controllato;
6. non vengono introdotte informazioni numeriche o aziendali prive di una fonte appropriata.

Il superamento di una singola suite non è sufficiente a dichiarare valido l'intero sistema.

Maranello AI viene considerato accettabile solo dopo la verifica congiunta dei componenti deterministici, dell'orchestrazione AI e dei principali flussi Full-Stack.

---

# 4. Ambiente e dati di test

## 4.1 Ambiente di esecuzione

Le verifiche finali di Maranello AI sono state eseguite principalmente in ambiente locale, utilizzando i componenti reali dell'architettura applicativa.

L'ambiente integrato comprende:

| Componente | Tecnologia | Porta locale |
|------------|------------|--------------|
| Frontend | React + Vite | `5173` |
| Backend | Node.js + Express | `3000` |
| Python Data Agent | FastAPI | `8001` |
| Vector Database | ChromaDB | `8000` |
| AI Provider | OpenAI API | Servizio esterno |

L'esecuzione locale permette di verificare il comportamento reale delle integrazioni tra i componenti senza introdurre ambienti Test, Staging o Production non presenti nella versione corrente.

---

## 4.2 Configurazione dei servizi

Per le verifiche Full-Stack devono essere disponibili i seguenti servizi:

    ChromaDB
        ↓
    Python Data Agent
        ↓
    Node.js Backend
        ↓
    React Frontend

Il Backend dipende inoltre dalla disponibilità dell'OpenAI API per le funzionalità di orchestrazione e generazione linguistica.

Le configurazioni sensibili vengono fornite tramite variabili d'ambiente e non sono memorizzate direttamente nel codice sorgente.

Tra le principali configurazioni utilizzate figurano:

- modello LLM;
- modello di embedding;
- URL del Data Agent;
- URL di ChromaDB;
- nome della collection ChromaDB;
- porta del Backend;
- credenziali del provider AI.

La configurazione effettiva viene caricata attraverso il file `.env`, mentre `.env.example` documenta le variabili richieste senza includere segreti reali.

---

## 4.3 Health check

Prima delle verifiche integrate viene controllata la disponibilità dei servizi principali.

### Node.js Backend

Endpoint:

    GET /health

Il risultato positivo conferma che il servizio HTTP del Backend è operativo.

### Python Data Agent

Endpoint:

    GET /health

Il risultato positivo conferma che il microservizio FastAPI è disponibile.

### ChromaDB

La disponibilità del servizio viene verificata prima delle operazioni RAG e dell'esecuzione delle verifiche che dipendono dalla Knowledge Base.

Il controllo delle dipendenze prima dei test permette di distinguere un difetto applicativo dall'indisponibilità di un servizio richiesto.

---

## 4.4 Manufacturing Dataset

Le verifiche analitiche utilizzano il Manufacturing Dataset sintetico realizzato specificamente per Maranello AI.

Il dataset contiene:

    2000 rows

di cui:

    1980 generated unique rows
    20 intentional exact duplicates

Ogni record rappresenta un batch produttivo.

Lo schema comprende 20 colonne:

| Campo |
|-------|
| `batch_id` |
| `production_date` |
| `plant` |
| `production_line` |
| `vehicle_model` |
| `shift` |
| `units_produced` |
| `defective_units` |
| `defect_category` |
| `rework_units` |
| `scrap_units` |
| `downtime_minutes` |
| `cycle_time_seconds` |
| `quality_score` |
| `supplier_id` |
| `component_category` |
| `inspection_status` |
| `temperature_c` |
| `operator_team` |
| `notes` |

Il dataset è completamente sintetico e non contiene dati produttivi reali.

---

## 4.5 Anomalie intenzionali del dataset

Il dataset è stato progettato includendo anomalie controllate per verificare il comportamento del processo di data cleaning.

Tra queste sono presenti:

| Anomalia | Quantità |
|----------|---------:|
| Duplicati esatti | 20 |
| `quality_score` mancanti | 20 |
| `supplier_id` mancanti | 15 |
| `downtime_minutes` mancanti | 19 |
| Date con formati differenti | 12 |
| `quality_score` non validi | 6 |
| Relazioni non valide tra quantità difettose e produzione | 6 |
| Outlier di downtime | 8 |
| Outlier di cycle time | 8 |
| Valori `shift` non normalizzati | 12 |
| Valori `production_line` non normalizzati | 10 |
| Valori `supplier_id` non normalizzati | 10 |

Queste anomalie permettono di verificare che il Data Agent non assuma implicitamente che il CSV sia già perfettamente pulito.

---

## 4.6 Relazioni sintetiche incorporate

Il dataset non è composto da valori completamente casuali.

Durante la generazione sono state introdotte relazioni controllate per produrre pattern analitici verificabili.

Tra le principali:

- defect probability di base pari a circa `1.5%`;
- incremento del rischio per `Line 3`;
- incremento del rischio durante il turno `Night`;
- incremento del rischio associato a `SUP-07`;
- incremento del rischio per la categoria `Electronics`;
- riduzione del `quality_score` all'aumentare di defect rate e downtime;
- maggiore downtime medio per `Line 3`;
- cycle time leggermente superiore durante il turno `Night`.

Queste relazioni forniscono un test oracle utile per verificare che le analisi aggregate siano in grado di evidenziare i pattern incorporati nel dataset.

---

## 4.7 Knowledge Base utilizzata nei test

Le verifiche RAG utilizzano la Knowledge Base fittizia inclusa nel progetto.

La base documentale comprende:

    knowledge_base/
    ├── README.md
    ├── manufacturing_quality_policy.md
    ├── non_conformity_procedure.md
    ├── supplier_quality_procedure.md
    ├── rework_and_scrap_procedure.md
    └── production_escalation_policy.md

I documenti rappresentano policy e procedure aziendali fittizie relative al dominio Quality & Manufacturing Operations.

La Knowledge Base viene utilizzata come fonte controllata per verificare:

- retrieval semantico;
- grounding delle risposte;
- recupero delle soglie;
- recupero delle procedure;
- source attribution;
- funzionamento delle richieste Hybrid;
- retrieval a partire da domande in italiano e inglese.

---

## 4.8 Dati e documenti come test oracle

Dataset e Knowledge Base svolgono due ruoli complementari.

Il Manufacturing Dataset permette di verificare:

    What happened?

La Knowledge Base permette di verificare:

    What should happen according to policy?

Il comportamento Hybrid combina entrambe le fonti:

    Manufacturing Dataset
             +
       Knowledge Base
             ↓
      Contextual Answer

Questa separazione permette di verificare indipendentemente correttezza numerica e correttezza procedurale.

---

# 5. Verifiche del Python Data Agent

## 5.1 Obiettivo

Il Python Data Agent rappresenta il componente responsabile delle analisi numeriche sui dati produttivi.

Le verifiche hanno l'obiettivo di assicurare che:

- il dataset venga caricato correttamente;
- le anomalie previste vengano gestite;
- i KPI siano calcolati correttamente;
- le aggregazioni siano coerenti;
- le richieste supportate vengano interpretate correttamente;
- le richieste ambigue vengano rifiutate quando necessario;
- i grafici vengano generati correttamente;
- i risultati siano riproducibili.

Il Data Agent adotta intenzionalmente un approccio deterministico e non esegue codice Python arbitrario generato dal modello linguistico.

---

## 5.2 API sottoposta a verifica

L'endpoint principale utilizzato dal Backend è:

    POST /api/analysis

La richiesta contiene la domanda analitica da interpretare.

Il Data Agent:

    Question
       ↓
    Question Interpreter
       ↓
    Dataset Analysis
       ↓
    Result
       ↓
    Optional Chart

Sono inoltre disponibili:

    GET /
    GET /health
    GET /charts/:filename

---

## 5.3 Data cleaning

Le verifiche sul processo di cleaning comprendono:

- rimozione dei duplicati;
- normalizzazione dei campi testuali;
- parsing delle date con formati differenti;
- gestione dei valori mancanti;
- identificazione dei valori `quality_score` non validi;
- gestione delle anomalie numeriche;
- conservazione controllata dei valori mancanti quando appropriato;
- identificazione delle relazioni non valide tra quantità produttive.

Un obiettivo importante è evitare che il cleaning nasconda automaticamente tutte le anomalie.

Quando un dato non può essere corretto in modo affidabile, il sistema deve trattarlo in maniera esplicita invece di inventare un valore.

---

## 5.4 KPI globali

Una delle verifiche principali riguarda il calcolo dei KPI globali sul dataset pulito.

I risultati di riferimento ottenuti sono:

| KPI | Risultato |
|-----|----------:|
| Total production | `164060` |
| Total defective units | `3272` |
| Defect rate | `1.99%` |
| Rework rate | `0.96%` |
| Scrap rate | `0.51%` |
| Average quality score | `95.82` |
| Average downtime | `33.04 min` |
| Average cycle time | `84.74 sec` |

Questi valori costituiscono un riferimento deterministico per le verifiche successive.

Una modifica al processo di cleaning o alle formule analitiche che alteri tali risultati deve essere analizzata per stabilire se rappresenti una modifica intenzionale oppure una regressione.

---

## 5.5 Analisi per linea produttiva

Il Data Agent supporta l'aggregazione per `production_line`.

Un risultato particolarmente significativo è:

    Line 3
    Defect rate ≈ 2.47%

Il risultato è coerente con la relazione sintetica incorporata durante la generazione del dataset, nella quale Line 3 presenta una probabilità di difetto superiore rispetto al baseline.

La verifica conferma quindi sia il funzionamento dell'aggregazione sia la capacità del dataset di produrre un pattern analitico osservabile.

---

## 5.6 Analisi per turno

Il Data Agent supporta l'aggregazione per `shift`.

Il turno maggiormente significativo è:

    Night
    Defect rate ≈ 2.35%

Il risultato è coerente con il rischio aggiuntivo introdotto intenzionalmente per il turno notturno.

---

## 5.7 Analisi per supplier

Il Data Agent supporta l'aggregazione per `supplier_id`.

Il risultato di riferimento principale è:

    SUP-07
    Defect rate ≈ 2.99%

SUP-07 è stato intenzionalmente configurato durante la generazione del dataset con un rischio di difetto superiore rispetto al baseline.

Questo risultato viene utilizzato anche nei test Hybrid, nei quali il valore quantitativo viene confrontato con le soglie definite nella Supplier Quality Procedure.

---

## 5.8 Analisi per component category

Il Data Agent supporta l'aggregazione per `component_category`.

Un risultato significativo è:

    Electronics
    Defect rate ≈ 2.49%

Anche questo risultato corrisponde a una relazione intenzionalmente incorporata nel dataset.

---

## 5.9 Dimensioni analitiche supportate

Il Question Interpreter riconosce richieste relative alle principali dimensioni:

- `production_line`;
- `shift`;
- `supplier_id`;
- `component_category`;
- `vehicle_model`;
- `plant`;
- `operator_team`.

Supporta inoltre:

- KPI globali;
- analisi temporale mensile;
- trend.

Il mapping tra linguaggio naturale e analisi viene eseguito in maniera deterministica.

---

## 5.10 Trend mensile

Il Data Agent supporta l'analisi temporale mensile del defect rate.

Il dataset copre dodici mesi:

    January 2025
          ↓
    December 2025

Tra i risultati di riferimento:

| Periodo | Defect rate |
|---------|------------:|
| Aprile 2025 | circa `2.10%` |
| Maggio 2025 | circa `2.10%` |
| Agosto 2025 | circa `1.78%` |

Aprile e maggio rappresentano i valori più elevati del periodo, mentre agosto presenta uno dei valori più bassi.

La verifica del trend mensile controlla:

- parsing delle date;
- ordinamento temporale;
- aggregazione mensile;
- calcolo del defect rate;
- generazione della serie utilizzata dal grafico.

---

## 5.11 Gestione delle richieste ambigue

Il Question Interpreter applica regole esplicite per evitare interpretazioni analitiche arbitrarie.

In particolare, vengono rifiutate richieste che richiedono contemporaneamente più dimensioni di grouping non supportate.

Esempio concettuale:

    Compare defect rate by supplier and production line.

Quando la richiesta richiede contemporaneamente due dimensioni che il contratto analitico non supporta, il sistema non sceglie arbitrariamente una delle due.

---

## 5.12 Combinazione di dimensione temporale e grouping

Il Data Agent evita inoltre di interpretare automaticamente richieste che combinano una dimensione temporale e una dimensione di grouping quando tale combinazione non è supportata dal relativo percorso analitico.

Questo comportamento protegge il sistema da analisi che potrebbero sembrare plausibili ma non corrispondere alla domanda dell'utente.

---

## 5.13 Default analysis

Quando una richiesta analitica è valida ma non identifica una dimensione specifica supportata, il Data Agent può utilizzare l'analisi globale come comportamento predefinito.

Il fallback globale deve comunque essere utilizzato soltanto quando non modifica il significato essenziale della richiesta.

---

## 5.14 Supporto bilingue

Il Question Interpreter è stato verificato con richieste in italiano e inglese.

Esempi concettuali equivalenti:

    Qual è il defect rate per supplier?

    What is the defect rate by supplier?

Entrambe le richieste devono essere associate alla dimensione:

    supplier_id

Lo stesso principio viene applicato alle altre dimensioni supportate.

---

## 5.15 Generazione dei grafici

Quando l'analisi produce una visualizzazione, il Data Agent utilizza Matplotlib in modalità server-side.

Il processo è:

    Analysis
       ↓
    Data Series
       ↓
    Matplotlib
       ↓
    PNG
       ↓
    generated_charts/

Ogni grafico viene salvato con un filename dedicato.

Il Data Agent restituisce quindi un riferimento al file attraverso:

    /charts/:filename

Il Backend trasforma successivamente tale riferimento nel percorso esposto al Frontend.

---

## 5.16 Verifica dei grafici temporali

Il trend mensile rappresenta uno dei principali casi di test della generazione grafica.

La verifica controlla che:

- il grafico venga effettivamente generato;
- il file PNG sia disponibile;
- i mesi siano ordinati cronologicamente;
- i valori rappresentati corrispondano ai risultati numerici;
- il riferimento al grafico sia incluso nella risposta del Data Agent;
- il Backend possa successivamente esporlo attraverso il Chart Proxy.

---

## 5.17 Determinismo

A parità di:

- dataset;
- processo di cleaning;
- domanda riconosciuta;
- dimensione analitica;

il risultato numerico del Data Agent deve rimanere stabile.

Questa proprietà è importante perché separa due categorie di comportamento:

    LLM orchestration
    potentially non-deterministic

    Data calculation
    deterministic

Il modello linguistico può variare la formulazione della risposta finale, ma non deve modificare i valori calcolati dal Data Agent.

---

## 5.18 Sicurezza dell'approccio analitico

Il Data Agent non utilizza `exec()` o meccanismi equivalenti per eseguire arbitrariamente codice Python generato dal modello.

L'utente esprime la richiesta in linguaggio naturale, ma l'esecuzione viene ricondotta a operazioni analitiche supportate e validate.

Il flusso è quindi:

    Natural Language Question
             ↓
    Deterministic Interpreter
             ↓
    Validated Analysis
             ↓
    Pandas
             ↓
    Result

Questa scelta riduce:

- rischio di arbitrary code execution;
- comportamento imprevedibile;
- difficoltà di testing;
- possibilità di manipolare direttamente il runtime;
- variabilità dei risultati numerici.

---

## 5.19 Valutazione complessiva del Data Agent

Le verifiche effettuate confermano che il Data Agent è in grado di:

- caricare il Manufacturing Dataset;
- gestire le anomalie previste;
- produrre KPI globali coerenti;
- effettuare aggregazioni sulle dimensioni supportate;
- identificare i pattern sintetici principali;
- analizzare il trend temporale;
- comprendere richieste analitiche in italiano e inglese;
- rifiutare combinazioni analitiche non supportate;
- generare grafici;
- fornire risultati deterministici al Backend.

Il componente soddisfa quindi il proprio ruolo architetturale di motore analitico controllato per Maranello AI.

---

# 6. Test automatici del Backend

## 6.1 Obiettivo

Il Backend Node.js rappresenta il principale punto di orchestrazione dell'architettura Maranello AI.

Le verifiche automatiche hanno l'obiettivo di proteggere da regressioni le responsabilità principali del servizio, tra cui:

- gestione delle richieste HTTP;
- validazione degli input;
- gestione delle conversazioni;
- orchestrazione AI;
- esecuzione dei tool;
- integrazione con il Data Agent;
- integrazione con la Knowledge Base;
- gestione dei grafici;
- trasformazione delle risposte;
- gestione controllata degli errori.

La suite automatizzata rappresenta quindi uno dei principali meccanismi di Quality Assurance del progetto.

---

## 6.2 Risultato complessivo

La suite finale del Backend comprende:

    Test files: 15
    Automated tests: 86

L'esecuzione finale ha prodotto:

    Type Check    PASS
    Lint          PASS
    Tests         PASS
    Build         PASS

Il risultato conferma che il Backend supera contemporaneamente:

- controllo statico TypeScript;
- controllo di qualità del codice;
- suite automatizzata;
- compilazione finale.

---

## 6.3 Strategia dei test Backend

I test sono progettati per verificare le singole responsabilità applicative mantenendo, quando possibile, le dipendenze esterne isolate.

La strategia generale è:

    Module
      ↓
    Controlled Dependencies
      ↓
    Test Input
      ↓
    Observable Behaviour
      ↓
    Assertion

Le dipendenze esterne possono essere sostituite o controllate durante i test quando l'obiettivo è verificare esclusivamente la logica del modulo.

Le verifiche Full-Stack con servizi reali vengono invece trattate separatamente nelle sezioni dedicate all'integrazione.

---

## 6.4 Validazione delle richieste Chat

L'endpoint principale del Backend è:

    POST /api/chat

Le verifiche comprendono la gestione del payload applicativo.

Una richiesta valida contiene:

    {
      "message": "user question"
    }

oppure, nelle conversazioni successive:

    {
      "message": "follow-up question",
      "sessionId": "existing-session-id"
    }

Il campo `sessionId` è opzionale nella prima richiesta.

---

## 6.5 Messaggio vuoto

Uno dei principali negative test verifica che il Backend non accetti un messaggio vuoto.

Input concettuale:

    {
      "message": ""
    }

Risultato atteso:

    HTTP 400

La richiesta non deve essere inoltrata all'orchestratore AI.

---

## 6.6 Messaggio composto da whitespace

La validazione deve inoltre impedire che una stringa contenente esclusivamente spazi venga considerata una domanda valida.

Esempio:

    {
      "message": "     "
    }

Risultato atteso:

    HTTP 400

Questa verifica viene applicata anche a livello di interfaccia, evitando quando possibile che una richiesta non valida raggiunga il Backend.

---

## 6.7 Conversation Manager

Il Conversation Manager gestisce lo stato applicativo delle sessioni.

Le verifiche riguardano:

- creazione di una nuova sessione;
- generazione del `sessionId`;
- recupero di una sessione esistente;
- memorizzazione dei messaggi;
- aggiornamento dello stato;
- conservazione del `lastResponseId`;
- gestione del numero massimo di messaggi previsto per sessione.

Il `sessionId` viene generato utilizzando un identificativo univoco.

---

## 6.8 Nuova conversazione

Quando una richiesta non contiene `sessionId`, il sistema deve creare una nuova sessione.

Il flusso atteso è:

    POST /api/chat
          ↓
    No sessionId
          ↓
    Create conversation
          ↓
    Generate sessionId
          ↓
    Process message
          ↓
    Return sessionId

Il client utilizza successivamente l'identificativo ricevuto per continuare la stessa conversazione.

---

## 6.9 Conversazione esistente

Quando il client invia un `sessionId` valido:

    Existing sessionId
          ↓
    Conversation Manager
          ↓
    Existing state
          ↓
    New message appended

Il sistema deve utilizzare il contesto della sessione esistente anziché creare una nuova conversazione indipendente.

---

## 6.10 OpenAI response continuity

Oltre allo stato applicativo interno, il Backend conserva il riferimento all'ultima risposta OpenAI quando disponibile.

Il valore:

    lastResponseId

viene utilizzato nelle chiamate successive come:

    previous_response_id

Il flusso è:

    First user message
          ↓
    OpenAI Responses API
          ↓
    response.id
          ↓
    lastResponseId

    Follow-up message
          ↓
    previous_response_id
          ↓
    OpenAI Responses API

Questo comportamento permette di mantenere la continuità della conversazione anche a livello del provider AI.

---

## 6.11 Chat Service

Il Chat Service coordina:

- sessione;
- orchestrazione;
- aggiornamento dello stato;
- trasformazione del risultato;
- gestione del grafico;
- risposta HTTP.

Le verifiche controllano che una risposta applicativa possa includere:

- `sessionId`;
- `answer`;
- `toolsUsed`;
- `chartUrl`, quando disponibile.

Il servizio deve inoltre aggiornare lo stato della conversazione soltanto in modo coerente con l'esecuzione completata.

---

## 6.12 Tool metadata

Il Backend mantiene informazioni sugli strumenti utilizzati durante l'elaborazione.

Il campo:

    toolsUsed

permette di distinguere scenari come:

    []

per una risposta diretta,

    ["search_knowledge_base"]

per una richiesta RAG,

    ["analyze_manufacturing_data"]

per una richiesta numerica,

oppure l'utilizzo di entrambi gli strumenti in una richiesta Hybrid.

Questa informazione è particolarmente utile durante le attività di testing perché rende osservabile la decisione dell'orchestratore.

---

## 6.13 Chart URL rewriting

Il Data Agent espone internamente i grafici attraverso:

    /charts/:filename

Il Frontend non deve utilizzare direttamente tale endpoint.

Il Chat Service trasforma quindi il riferimento interno nel percorso Backend:

    /api/charts/:filename

Le verifiche controllano che la risposta destinata al Frontend contenga il percorso corretto.

---

## 6.14 Chart Proxy

Il Backend espone:

    GET /api/charts/:filename

Il proxy recupera il grafico dal Python Data Agent e lo restituisce al client.

Le verifiche riguardano:

- presenza del filename;
- validazione del filename;
- forwarding della richiesta;
- propagazione controllata del risultato;
- gestione dei file non disponibili;
- protezione da percorsi non validi.

---

## 6.15 Protezione da path traversal

Il parametro `filename` non deve permettere al client di costruire percorsi arbitrari.

Input contenenti sequenze o strutture non compatibili con un filename valido devono essere rifiutati.

L'obiettivo è impedire scenari concettualmente equivalenti a:

    ../../some-file

Il Chart Proxy deve consentire esclusivamente l'accesso ai file grafici previsti dal contratto applicativo.

---

## 6.16 Gestione degli errori

Il Backend utilizza una gestione centralizzata degli errori.

Le verifiche assicurano che:

- gli errori previsti vengano trasformati in risposte HTTP controllate;
- i dettagli interni non vengano esposti inutilmente;
- l'indisponibilità di una dipendenza venga distinta da un input utente non valido;
- il sistema non restituisca una risposta AI inventata quando la fonte necessaria non è disponibile.

Questa caratteristica è particolarmente importante per RAG e analisi numeriche.

---

## 6.17 Valutazione complessiva dei test Backend

Il superamento dei 86 test automatici, insieme a type checking, linting e build, fornisce la principale evidenza automatizzata di stabilità della componente Node.js.

Le verifiche Full-Stack vengono utilizzate successivamente per validare le integrazioni che non possono essere completamente dimostrate attraverso test isolati.

---

# 7. Verifiche RAG e Knowledge Base

## 7.1 Obiettivo

Le verifiche RAG hanno l'obiettivo di assicurare che Maranello AI possa recuperare informazioni dalla Knowledge Base aziendale e utilizzarle come contesto per produrre risposte grounded.

Il flusso sottoposto a verifica è:

    User Question
          ↓
    LLM
          ↓
    search_knowledge_base
          ↓
    Embedding
          ↓
    ChromaDB
          ↓
    Relevant Chunks
          ↓
    LLM
          ↓
    Grounded Answer

---

## 7.2 Indicizzazione

La Knowledge Base finale comprende cinque documenti operativi principali.

Il processo di ingestion produce:

    Documents: 5
    Chunks: 149

I chunk vengono memorizzati nella collection ChromaDB configurata per Maranello AI.

Le verifiche assicurano che il processo di retrieval possa restituire:

- contenuto rilevante;
- documento sorgente;
- sezione di provenienza;
- contesto sufficiente alla generazione della risposta.

---

## 7.3 Modello di embedding

La versione finale utilizza:

    text-embedding-3-small

La scelta è stata effettuata dopo verifiche qualitative sul retrieval bilingue.

Una soluzione iniziale basata su embedding locali produceva risultati non sufficientemente affidabili per alcune query cross-language, in particolare quando:

    Question language = Italian
    Document language = English

La migrazione al modello di embedding OpenAI ha migliorato la qualità del retrieval multilingue.

Questo passaggio rappresenta anche un risultato significativo delle attività di debugging e testing del progetto.

---

## 7.4 Retrieval in inglese

Le verifiche RAG comprendono domande formulate nella stessa lingua principale dei documenti.

Esempio concettuale:

    What is the critical defect rate threshold?

Il sistema deve recuperare il contenuto rilevante della Manufacturing Quality Policy.

La risposta deve utilizzare la soglia documentata e non una soglia generata dal modello sulla base della propria conoscenza generale.

---

## 7.5 Retrieval cross-language

Una verifica fondamentale riguarda domande in italiano su documenti scritti in inglese.

Esempio:

    Qual è la soglia critica del defect rate?

Il sistema deve essere in grado di recuperare il contenuto inglese semanticamente equivalente e produrre una risposta in italiano.

Il test verifica contemporaneamente:

- embedding multilingue;
- retrieval semantico;
- grounding;
- comportamento bilingue.

---

## 7.6 Manufacturing Quality Policy

Un test di riferimento riguarda le soglie del defect rate.

La Knowledge Base definisce:

| Defect rate | Classificazione |
|-------------|-----------------|
| `<= 2.0%` | Normal |
| `> 2.0%` e `<= 3.5%` | Warning |
| `> 3.5%` | Critical |

Una domanda relativa alla soglia critica deve quindi identificare:

    defect rate > 3.5%

come condizione `Critical`.

Questa verifica è stata eseguita con successo durante la QA finale.

---

## 7.7 Supplier Quality Procedure

Le verifiche comprendono anche policy specifiche per i supplier.

Le soglie previste sono:

| Supplier defect rate | Classificazione |
|----------------------|-----------------|
| `> 2.0%` e `<= 3.0%` | Observation |
| `> 3.0%` e `<= 4.0%` | Warning |
| `> 4.0%` | Critical |

Queste soglie sono intenzionalmente differenti dalle soglie generali della Manufacturing Quality Policy.

La distinzione permette di verificare che il sistema recuperi la procedura appropriata rispetto al contesto della domanda.

---

## 7.8 Source attribution

Il sistema è istruito a mantenere l'attribuzione della fonte quando utilizza la Knowledge Base.

Le verifiche controllano che il contesto recuperato includa informazioni sufficienti per identificare:

- documento;
- sezione;
- contenuto rilevante.

Questo permette alla risposta finale di essere verificabile rispetto alla documentazione aziendale fittizia.

---

## 7.9 Grounding

Una risposta RAG viene considerata corretta quando:

1. viene utilizzato `search_knowledge_base`;
2. il contenuto recuperato è pertinente;
3. la risposta non contraddice la fonte;
4. le soglie o procedure citate corrispondono alla Knowledge Base;
5. non vengono presentate come policy informazioni non supportate dai documenti.

---

## 7.10 Indisponibilità di ChromaDB

È stato verificato anche il comportamento con ChromaDB non disponibile.

Quando una richiesta necessita della Knowledge Base ma il servizio non può essere raggiunto, il sistema deve restituire un errore controllato equivalente a:

    HTTP 503

con un messaggio applicativo che comunica che la Knowledge Base aziendale è temporaneamente non disponibile.

Il sistema non deve sostituire la policy mancante con conoscenza generale del modello.

---

## 7.11 Risultato delle verifiche RAG

Le verifiche finali hanno confermato:

- corretta indicizzazione della Knowledge Base;
- disponibilità dei 149 chunk;
- retrieval in inglese;
- retrieval cross-language italiano → inglese;
- recupero delle soglie di qualità;
- recupero delle procedure supplier;
- source attribution;
- integrazione con l'orchestratore;
- gestione controllata dell'indisponibilità di ChromaDB.

Il componente RAG soddisfa quindi il proprio ruolo di fonte documentale controllata del sistema.

---

# 8. Test dell'orchestrazione AI

## 8.1 Obiettivo

L'orchestrazione AI rappresenta la caratteristica centrale dell'architettura Maranello AI.

Il Backend non utilizza una classificazione deterministica preliminare del tipo:

    if question == data:
        call Data Agent

oppure:

    if question == policy:
        call RAG

La decisione viene invece affidata al Large Language Model attraverso native function calling.

Le verifiche devono quindi assicurare che il modello selezioni gli strumenti coerenti con l'intento della richiesta.

---

## 8.2 Strumenti disponibili

L'orchestratore espone al modello due strumenti principali:

    search_knowledge_base

e:

    analyze_manufacturing_data

Il primo permette di recuperare informazioni documentali.

Il secondo permette di ottenere analisi quantitative dal Manufacturing Dataset.

Il modello può:

- non utilizzare alcun tool;
- utilizzare soltanto RAG;
- utilizzare soltanto il Data Agent;
- utilizzare entrambi.

---

## 8.3 OpenAI Responses API

L'orchestrazione utilizza la OpenAI Responses API.

Il flusso generale è:

    User Message
          ↓
    Responses API
          ↓
    Function Call?
       /       \
     No         Yes
     │           │
     ▼           ▼
    Final      Execute Tool
    Answer        │
                  ▼
             Tool Output
                  │
                  ▼
             Responses API
                  │
                  ▼
              Final Answer

Il ciclo può continuare per più round quando il modello richiede ulteriori strumenti prima di produrre la risposta finale.

---

## 8.4 Esecuzione dei tool

Quando il modello genera un function call, il Backend:

1. identifica il tool richiesto;
2. valida gli argomenti;
3. esegue il connettore corrispondente;
4. acquisisce il risultato;
5. costruisce un `function_call_output`;
6. restituisce il risultato al modello;
7. continua il ciclo di orchestrazione.

Il modello non accede direttamente a ChromaDB o al Data Agent.

Tutte le operazioni passano attraverso il Backend.

---

## 8.5 Tool multipli

L'orchestratore supporta più function call nello stesso ciclo.

Quando sono presenti più richieste di tool indipendenti, queste possono essere eseguite dal Backend prima della successiva sintesi del modello.

Questo comportamento è particolarmente importante per gli scenari Hybrid.

---

## 8.6 Scenario Conversational

Una richiesta generale che non necessita di dati aziendali può essere gestita direttamente dal modello.

Esempio concettuale:

    What can you help me with?

Comportamento atteso:

    toolsUsed = []

La risposta non deve utilizzare inutilmente ChromaDB o il Data Agent.

---

## 8.7 Scenario RAG

Una richiesta relativa a una policy deve attivare:

    search_knowledge_base

Esempio:

    What is the critical defect rate threshold according to the quality policy?

Comportamento atteso:

    toolsUsed:
    - search_knowledge_base

Il risultato deve essere basato sul contenuto recuperato.

---

## 8.8 Scenario Data Analysis

Una richiesta quantitativa deve utilizzare:

    analyze_manufacturing_data

Esempio:

    Which supplier has the highest defect rate?

Comportamento atteso:

    toolsUsed:
    - analyze_manufacturing_data

Il valore numerico deve provenire dal Data Agent.

---

## 8.9 Scenario Hybrid

Una richiesta che combina dati e policy deve utilizzare entrambe le fonti.

Esempio concettuale:

    Which supplier has the highest defect rate and how should that result be classified according to the supplier quality procedure?

Comportamento atteso:

    analyze_manufacturing_data
              +
    search_knowledge_base
              ↓
         Final Answer

Il modello deve combinare il risultato numerico con la procedura appropriata.

---

## 8.10 Verifica Hybrid su SUP-07

Uno degli scenari principali utilizzati durante la QA riguarda:

    SUP-07
    defect rate ≈ 2.99%

La Supplier Quality Procedure stabilisce:

    > 2.0% and <= 3.0%
    Observation

Di conseguenza, quando la richiesta specifica esplicitamente il contesto supplier, il risultato atteso è:

    SUP-07 ≈ 2.99%
          ↓
    Supplier Quality Procedure
          ↓
    Observation

La verifica ha confermato il corretto utilizzo della policy supplier-specific.

---

## 8.11 Distinzione tra policy generale e supplier-specific

Un aspetto importante emerso durante il testing è la necessità di distinguere:

    Manufacturing Quality Policy

da:

    Supplier Quality Procedure

Un valore vicino al `3%` può ricevere una classificazione differente a seconda della policy applicabile.

L'orchestratore deve quindi utilizzare il contesto semantico della domanda e non limitarsi a recuperare una soglia numerica genericamente simile.

---

## 8.12 Test della memoria conversazionale

È stata verificata la capacità di utilizzare riferimenti derivati dai turni precedenti.

Scenario:

    User:
    Which supplier has the highest defect rate?

    Assistant:
    SUP-07 ...

    User:
    What does the policy say about that supplier?

La seconda domanda contiene:

    that supplier

senza ripetere:

    SUP-07

La conversazione deve mantenere informazioni sufficienti affinché il sistema comprenda il riferimento.

La verifica ha avuto esito positivo.

---

## 8.13 Scenario conversazionale con soglia supplier

Un'ulteriore verifica multi-turn utilizza un valore esplicito.

Esempio:

    User:
    Consider a supplier defect rate of 3.2%.

    User:
    How should it be classified?

Secondo la Supplier Quality Procedure:

    > 3.0% and <= 4.0%
    Warning

Il sistema deve mantenere il valore dal contesto precedente e applicare la policy corretta.

---

## 8.14 Scenario bilingue con soglia critica

È stata verificata anche una richiesta in italiano relativa a una soglia supplier superiore al limite Critical.

Esempio concettuale:

    Un supplier presenta un defect rate del 4,2%.
    Come deve essere classificato e gestito?

La Supplier Quality Procedure prevede:

    > 4.0%
    Critical

La risposta deve essere prodotta in italiano e utilizzare il contenuto della Knowledge Base appropriato.

La verifica finale ha confermato il comportamento atteso.

---

## 8.15 Scope preservation

Durante lo sviluppo è stato individuato un comportamento rilevante: il modello poteva riformulare la domanda destinata al Data Agent aggiungendo vincoli non presenti nella richiesta originale.

Questo poteva trasformare, ad esempio, una semplice richiesta temporale in una combinazione di:

- trend;
- grouping;
- ulteriori filtri.

Il Question Interpreter deterministico poteva correttamente rifiutare la richiesta trasformata, anche se la domanda originale era valida.

La correzione ha riguardato le istruzioni dell'orchestratore e la descrizione del tool.

Il modello viene ora istruito a:

- preservare lo scope della domanda;
- non aggiungere filtri non richiesti;
- non aggiungere dimensioni analitiche;
- non aggiungere vincoli temporali;
- mantenere l'intento originale quando delega al Data Agent.

---

## 8.16 Test del monthly trend dopo la correzione

Dopo il miglioramento dello scope preservation è stata verificata direttamente una richiesta di trend mensile.

Il Data Agent ha correttamente:

- riconosciuto l'intento temporale;
- elaborato i dodici mesi;
- calcolato i defect rate mensili;
- prodotto il risultato;
- generato il grafico.

Questa verifica conferma che l'orchestratore non introduce più automaticamente dimensioni incompatibili nella richiesta analitica prevista dallo scenario testato.

---

## 8.17 Separazione delle responsabilità

Le verifiche confermano la seguente separazione:

    LLM
    decides what is needed

    RAG
    retrieves company knowledge

    Data Agent
    calculates numerical results

    LLM
    synthesizes the final response

Il modello linguistico non deve sostituire il Data Agent per i calcoli aziendali e non deve sostituire la Knowledge Base quando la domanda richiede una policy interna.

---

## 8.18 Criteri di successo del routing

Una decisione di routing viene considerata corretta quando:

| Tipo richiesta | Comportamento atteso |
|----------------|----------------------|
| Conversational | Nessun tool obbligatorio |
| Policy / procedure | `search_knowledge_base` |
| KPI / dati / trend | `analyze_manufacturing_data` |
| Data + policy | Entrambi i tool |

La formulazione testuale finale può variare, ma la selezione delle fonti deve rimanere coerente con l'intento.

---

## 8.19 Risultato complessivo dell'orchestrazione

Le verifiche finali hanno confermato il funzionamento dei principali comportamenti:

- risposta conversazionale diretta;
- routing RAG;
- routing Data Agent;
- routing Hybrid;
- function calling;
- gestione di più tool;
- sintesi dei tool output;
- continuità tramite `previous_response_id`;
- memoria conversazionale;
- comportamento bilingue;
- scope preservation;
- corretta separazione tra conoscenza documentale e calcolo numerico.

L'orchestrazione soddisfa quindi il requisito centrale del progetto: utilizzare il Large Language Model per decidere autonomamente quali capacità del sistema siano necessarie per rispondere alla richiesta dell'utente.

---

# 9. Test delle API e della resilienza

## 9.1 Obiettivo

Le verifiche API assicurano che i servizi di Maranello AI espongano esclusivamente i contratti previsti dall'architettura finale e che gli errori vengano gestiti in modo controllato.

Le API coinvolte sono suddivise tra:

- Node.js Backend;
- Python Data Agent.

Il Frontend comunica esclusivamente con il Backend Node.js.

Il Python Data Agent viene invece utilizzato come servizio interno dal Backend.

---

## 9.2 Endpoint del Backend

Gli endpoint applicativi principali esposti dal Backend sono:

| Metodo | Endpoint | Funzione |
|--------|----------|----------|
| `GET` | `/health` | Verifica disponibilità del Backend |
| `POST` | `/api/chat` | Interfaccia conversazionale principale |
| `GET` | `/api/charts/:filename` | Proxy dei grafici generati dal Data Agent |

Non sono utilizzati endpoint versionati del tipo:

    /api/v1/...

nella versione corrente.

---

## 9.3 Endpoint del Python Data Agent

Il servizio FastAPI espone:

| Metodo | Endpoint | Funzione |
|--------|----------|----------|
| `GET` | `/` | Informazioni base sul servizio |
| `GET` | `/health` | Verifica disponibilità |
| `POST` | `/api/analysis` | Esecuzione dell'analisi sul Manufacturing Dataset |
| `GET` | `/charts/:filename` | Esposizione interna dei grafici generati |

L'endpoint `/charts/:filename` non viene utilizzato direttamente dal Frontend.

---

## 9.4 Test di `POST /api/chat`

L'endpoint principale riceve un payload compatto.

Prima richiesta:

    {
      "message": "What is the critical defect rate threshold?"
    }

Richiesta successiva:

    {
      "message": "And what happens above that threshold?",
      "sessionId": "existing-session-id"
    }

Il Backend restituisce una risposta contenente almeno:

- `sessionId`;
- `answer`;
- `toolsUsed`;

e, quando necessario:

- `chartUrl`.

---

## 9.5 Risposta Chat

Esempio concettuale di risposta:

    {
      "sessionId": "generated-session-id",
      "answer": "Generated assistant response",
      "toolsUsed": [
        "search_knowledge_base"
      ]
    }

In presenza di un grafico:

    {
      "sessionId": "generated-session-id",
      "answer": "Generated assistant response",
      "toolsUsed": [
        "analyze_manufacturing_data"
      ],
      "chartUrl": "/api/charts/generated-chart.png"
    }

La risposta non utilizza un envelope artificiale con proprietà come:

- `success`;
- `request_id`;
- `timestamp`;
- `metadata`;
- `error`;

quando tali proprietà non fanno parte del contratto effettivamente implementato.

---

## 9.6 Validazione dell'input

È stato verificato che una richiesta priva di contenuto valido venga rifiutata.

Esempio:

    {
      "message": ""
    }

Risultato:

    HTTP 400

Lo stesso comportamento è previsto per stringhe contenenti esclusivamente whitespace.

Questo impedisce l'invocazione non necessaria dell'orchestratore e del provider AI.

---

## 9.7 Validazione lato Frontend e Backend

La protezione contro i messaggi vuoti è applicata su due livelli.

### Frontend

Il pulsante di invio viene disabilitato quando il contenuto non è valido.

### Backend

La richiesta viene nuovamente validata.

Il flusso è quindi:

    Empty input
       ↓
    Frontend validation
       ↓
    Request normally blocked

e, qualora la richiesta raggiunga comunque il Backend:

    Empty input
       ↓
    Backend validation
       ↓
    HTTP 400

La validazione Backend rimane necessaria perché il client non deve essere considerato una boundary di sicurezza affidabile.

---

## 9.8 Data Agent unavailable

È stato verificato il comportamento del sistema quando il Python Data Agent non è disponibile.

Scenario:

    User asks numerical question
            ↓
    LLM selects analyze_manufacturing_data
            ↓
    Backend calls Data Agent
            ↓
    Data Agent unavailable

Il Backend deve trasformare l'errore tecnico in una risposta controllata.

Risultato atteso:

    HTTP 503

Messaggio applicativo:

    Manufacturing data analysis is temporarily unavailable. Please try again later.

Il sistema non deve:

- inventare il KPI;
- calcolare autonomamente un valore tramite LLM;
- restituire una risposta apparentemente valida.

La verifica è stata completata con successo.

---

## 9.9 Knowledge Base unavailable

È stato verificato anche il comportamento con ChromaDB non disponibile.

Scenario:

    User asks policy question
            ↓
    LLM selects search_knowledge_base
            ↓
    Backend attempts retrieval
            ↓
    ChromaDB unavailable

Risultato atteso:

    HTTP 503

Messaggio applicativo:

    The company knowledge base is temporarily unavailable. Please try again later.

Il modello non deve sostituire la Knowledge Base con una risposta generata dalla propria conoscenza generale.

La verifica è stata completata con successo.

---

## 9.10 Importanza dei controlled failures

La gestione dei `503` rappresenta una verifica importante per un sistema AI enterprise.

Un errore tecnico deve essere preferibile a una risposta non verificabile.

La strategia adottata è:

    Required source available
            ↓
    Generate supported answer

    Required source unavailable
            ↓
    Controlled failure

e non:

    Required source unavailable
            ↓
    Guess an answer

Questo principio riduce il rischio di fornire informazioni aziendali o numeriche non supportate.

---

## 9.11 Chart Proxy API

Il Backend espone:

    GET /api/charts/:filename

Lo scopo è evitare che il Frontend dipenda direttamente dal microservizio Python.

Architettura:

    React
      ↓
    Node.js Backend
      ↓
    Python Data Agent

anziché:

    React
      ├── Node.js Backend
      └── Python Data Agent

Il proxy mantiene quindi una boundary applicativa unica verso il client.

---

## 9.12 Test del Chart Proxy

Le verifiche riguardano:

- validazione del parametro `filename`;
- costruzione corretta dell'URL del Data Agent;
- recupero dell'immagine;
- restituzione del contenuto al Frontend;
- gestione del file non disponibile;
- gestione dell'indisponibilità del Data Agent;
- protezione da filename non consentiti.

---

## 9.13 Path traversal protection

Il filename viene validato prima dell'accesso al servizio Python.

Input progettati per alterare il percorso richiesto devono essere rifiutati.

Esempio concettuale non consentito:

    ../../secret-file

Il Chart Proxy deve accettare soltanto filename compatibili con i grafici generati dal sistema.

Questa verifica evita che l'endpoint venga utilizzato come proxy generico verso risorse arbitrarie.

---

## 9.14 Test degli health endpoint

Prima delle verifiche integrate vengono controllati:

    GET /health

sul Backend e:

    GET /health

sul Data Agent.

L'obiettivo è confermare che i processi siano disponibili prima di attribuire eventuali errori alla logica applicativa.

Durante la QA finale entrambi i servizi hanno restituito correttamente lo stato operativo.

---

## 9.15 API tra Backend e Data Agent

La comunicazione interna avviene tramite:

    POST /api/analysis

Il Backend invia la domanda da analizzare al microservizio Python.

La verifica comprende:

- URL corretto;
- serializzazione JSON;
- gestione della risposta;
- gestione degli errori HTTP;
- acquisizione del risultato numerico;
- acquisizione dell'eventuale riferimento al grafico.

---

## 9.16 Contratto minimo e separazione delle responsabilità

Il contratto tra Node.js e Python viene mantenuto intenzionalmente semplice.

Il Backend:

- gestisce la conversazione;
- gestisce l'orchestrazione;
- gestisce l'LLM;
- seleziona il tool.

Il Data Agent:

- interpreta la richiesta analitica;
- esegue il calcolo;
- genera il grafico;
- restituisce il risultato.

Questa separazione facilita testing e debugging.

---

## 9.17 Risultato delle verifiche API

Le verifiche finali hanno confermato:

- disponibilità del Backend;
- disponibilità del Data Agent;
- funzionamento di `POST /api/chat`;
- generazione del `sessionId`;
- continuazione della sessione;
- rifiuto degli input vuoti;
- funzionamento di `POST /api/analysis`;
- funzionamento del Chart Proxy;
- gestione controllata del Data Agent non disponibile;
- gestione controllata di ChromaDB non disponibile;
- protezione del percorso dei grafici.

---

# 10. Verifiche del Frontend

## 10.1 Obiettivo

Il Frontend React rappresenta l'unico punto di interazione dell'utente con Maranello AI.

Le verifiche devono assicurare che l'interfaccia consenta di:

- inserire una domanda;
- inviare il messaggio;
- visualizzare il messaggio dell'utente;
- mostrare lo stato di elaborazione;
- visualizzare la risposta dell'assistente;
- mantenere la conversazione;
- mostrare eventuali errori;
- visualizzare i grafici prodotti dal Data Agent.

---

## 10.2 Stack sottoposto a verifica

Il Frontend finale utilizza:

- React;
- TypeScript;
- Vite.

La comunicazione applicativa avviene verso:

    VITE_API_URL

configurato per puntare al Backend Node.js.

In ambiente locale:

    http://127.0.0.1:3000

---

## 10.3 Verifiche statiche

Prima della QA manuale sono stati eseguiti:

    Frontend Lint    PASS
    Frontend Build   PASS

Il risultato conferma che il codice supera i controlli statici configurati e può produrre correttamente la build di produzione.

---

## 10.4 Rendering iniziale

All'avvio dell'applicazione vengono verificati:

- caricamento della pagina;
- presenza dell'header;
- presenza della conversazione;
- presenza del composer;
- presenza del campo di input;
- presenza del controllo di invio;
- assenza di errori bloccanti.

L'interfaccia deve risultare immediatamente utilizzabile.

---

## 10.5 Invio dei messaggi

Il flusso verificato è:

    User types message
          ↓
    Submit
          ↓
    User message rendered
          ↓
    Request to Backend
          ↓
    Loading state
          ↓
    Assistant response
          ↓
    Response rendered

Una singola azione di invio deve produrre una sola richiesta applicativa.

---

## 10.6 Messaggi vuoti

È stato verificato il comportamento con input:

- vuoto;
- composto esclusivamente da spazi.

In entrambi i casi il messaggio non deve essere inviato.

Il controllo di invio viene disabilitato quando l'input non contiene testo valido.

La verifica manuale del comportamento whitespace è stata completata con successo.

---

## 10.7 Stato di caricamento

Durante l'elaborazione della richiesta il Frontend mostra uno stato di loading/typing.

L'obiettivo è rendere evidente che:

- la richiesta è stata ricevuta;
- il sistema sta elaborando;
- non è necessario inviare nuovamente la domanda.

Durante questo stato l'interfaccia impedisce operazioni di invio incompatibili con l'elaborazione corrente.

---

## 10.8 Visualizzazione della risposta

Il contenuto dell'assistente deve preservare la leggibilità anche per risposte articolate.

Il rendering supporta testo multilinea attraverso la conservazione della formattazione necessaria.

Sono stati verificati:

- messaggi brevi;
- risposte RAG;
- risposte numeriche;
- risposte Hybrid;
- contenuto italiano;
- contenuto inglese.

---

## 10.9 Stato conversazionale

Il Frontend conserva il `sessionId` ricevuto dal Backend nello stato applicativo della conversazione corrente.

Flusso:

    First request
        ↓
    Backend returns sessionId
        ↓
    Frontend stores sessionId
        ↓
    Next request includes sessionId

Questo permette all'utente di continuare la conversazione senza gestire manualmente identificativi o contesto.

La persistenza oltre il ciclo corrente dell'applicazione non rappresenta un requisito della versione implementata.

---

## 10.10 Visualizzazione degli errori

Quando il Backend restituisce un errore applicativo, il Frontend deve:

- terminare lo stato di loading;
- mantenere stabile l'interfaccia;
- mostrare un feedback comprensibile;
- non esporre dettagli tecnici non necessari;
- consentire all'utente di inviare una nuova richiesta.

Sono stati verificati scenari derivati dall'indisponibilità dei servizi interni.

---

## 10.11 Rendering dei grafici

Quando la risposta Backend contiene:

    chartUrl

il Frontend costruisce il riferimento corretto e visualizza l'immagine.

Il flusso finale è:

    Backend response
          ↓
    chartUrl
          ↓
    Frontend URL resolution
          ↓
    GET /api/charts/:filename
          ↓
    Image rendered

Il browser non comunica direttamente con il Data Agent.

---

## 10.12 Test della risposta con grafico

Uno scenario di riferimento utilizza una richiesta temporale, ad esempio un'analisi mensile del defect rate.

Il risultato atteso comprende:

- risposta testuale;
- analisi numerica;
- `chartUrl`;
- grafico visibile nella conversazione.

La verifica è stata eseguita sull'intero sistema integrato.

---

## 10.13 Supporto bilingue

Non è presente un selettore manuale della lingua.

La lingua deriva dalla domanda dell'utente.

Sono stati verificati scenari in:

- italiano;
- inglese.

Il Frontend non deve modificare o tradurre autonomamente la risposta ricevuta dal Backend.

---

## 10.14 Responsive behaviour

L'interfaccia è stata progettata con layout adattabile e componenti compatibili con differenti dimensioni del viewport.

La versione corrente non include tuttavia un audit formale multi-browser o una matrice automatizzata di viewport.

Il responsive behaviour è pertanto considerato una verifica funzionale/manuale e non una suite certificata di compatibility testing.

---

## 10.15 Accessibility

Sono presenti controlli standard basati su elementi HTML interattivi, ma nella versione corrente non è stato eseguito un audit formale conforme a WCAG mediante strumenti dedicati.

L'accessibility testing avanzato viene quindi classificato come possibile evoluzione futura e non come attività completata.

---

## 10.16 Risultato delle verifiche Frontend

Le verifiche finali hanno confermato:

- build React valida;
- linting superato;
- caricamento dell'interfaccia;
- invio dei messaggi;
- blocco dell'input vuoto;
- gestione dello stato di loading;
- visualizzazione delle risposte;
- gestione della sessione;
- visualizzazione degli errori;
- rendering dei grafici;
- comunicazione esclusiva con il Backend Node.js.

---

# 11. Test di integrazione Full-Stack

## 11.1 Obiettivo

Le verifiche Full-Stack hanno l'obiettivo di assicurare che i componenti, già validati individualmente, funzionino correttamente quando vengono utilizzati insieme.

L'architettura sottoposta a test è:

    React Frontend
          ↓
    Node.js Backend
          ↓
    OpenAI Responses API
       /          \
      /            \
    RAG          Data Agent
     ↓               ↓
    ChromaDB       FastAPI
     ↓               ↓
    Knowledge      Dataset
    Base              ↓
                   Matplotlib

---

## 11.2 Servizi richiesti

Per la verifica completa vengono avviati:

    ChromaDB          :8000
    Python Data Agent :8001
    Node.js Backend   :3000
    React Frontend    :5173

È inoltre necessaria la configurazione valida del provider OpenAI.

---

## 11.3 Sequenza di avvio utilizzata

La sequenza operativa consigliata è:

    1. ChromaDB
    2. Python Data Agent
    3. Node.js Backend
    4. React Frontend

Prima dei test applicativi vengono verificati gli health endpoint dei servizi disponibili.

---

## 11.4 Test Full-Stack RAG

Scenario:

    User
      ↓
    React
      ↓
    POST /api/chat
      ↓
    Node Backend
      ↓
    OpenAI
      ↓
    search_knowledge_base
      ↓
    ChromaDB
      ↓
    Knowledge Base
      ↓
    OpenAI
      ↓
    Backend
      ↓
    React

Uno scenario di riferimento riguarda la soglia critica del defect rate.

Risultato atteso:

    Critical threshold > 3.5%

con contenuto coerente con la Manufacturing Quality Policy.

La verifica ha avuto esito positivo.

---

## 11.5 Test Full-Stack Data Analysis

Scenario:

    User
      ↓
    React
      ↓
    Backend
      ↓
    OpenAI
      ↓
    analyze_manufacturing_data
      ↓
    Python Data Agent
      ↓
    Manufacturing Dataset
      ↓
    Analysis
      ↓
    OpenAI
      ↓
    Final answer

Uno scenario di riferimento riguarda l'identificazione del supplier con defect rate più elevato.

Il risultato principale è:

    SUP-07
    ≈ 2.99%

La verifica ha avuto esito positivo.

---

## 11.6 Test Full-Stack con grafico

Scenario:

    User requests monthly trend
          ↓
    Backend orchestration
          ↓
    Data Agent
          ↓
    Monthly analysis
          ↓
    Matplotlib
          ↓
    PNG
          ↓
    Backend Chart Proxy
          ↓
    React
          ↓
    Visible chart

La verifica conferma contemporaneamente:

- routing;
- analisi;
- generazione del grafico;
- gestione del percorso;
- proxy;
- rendering React.

---

## 11.7 Test Full-Stack Hybrid

Uno scenario Hybrid richiede contemporaneamente:

- un valore calcolato;
- una policy documentale.

Esempio:

    Which supplier has the highest defect rate and how should it be classified according to the supplier quality procedure?

Il flusso richiede:

    Data Agent
       +
    RAG
       ↓
    LLM synthesis

Il risultato deve mantenere distinti:

- valore osservato;
- classificazione prevista dalla policy;
- fonte documentale.

---

## 11.8 Verifica SUP-07

Il risultato analitico:

    SUP-07 ≈ 2.99%

viene confrontato con la Supplier Quality Procedure:

    > 2.0% and <= 3.0%
    Observation

Risultato atteso:

    Observation

La verifica specifica della policy supplier ha avuto esito positivo.

---

## 11.9 Test della memoria Full-Stack

È stato eseguito anche un flusso multi-turn.

Prima richiesta:

    Which supplier has the highest defect rate?

Risultato:

    SUP-07

Seconda richiesta:

    What does the policy say about that supplier?

Il sistema deve utilizzare il contesto della conversazione per risolvere:

    that supplier

come:

    SUP-07

La verifica ha avuto esito positivo.

---

## 11.10 Test della classificazione Warning

È stato verificato un ulteriore scenario conversazionale con valore:

    3.2%

Secondo la Supplier Quality Procedure:

    > 3.0% and <= 4.0%
    Warning

Risultato atteso:

    Warning

La verifica ha confermato la corretta applicazione della soglia nel contesto conversazionale.

---

## 11.11 Test italiano Critical

È stato verificato uno scenario equivalente in lingua italiana con:

    4,2%

Secondo la Supplier Quality Procedure:

    > 4.0%
    Critical

Il risultato atteso comprende:

- classificazione `Critical`;
- risposta in italiano;
- contenuto procedurale coerente;
- utilizzo della Knowledge Base.

La verifica ha avuto esito positivo.

---

## 11.12 Failure test con Data Agent offline

Durante la verifica di resilienza il Data Agent è stato reso non disponibile.

Una richiesta numerica ha prodotto:

    HTTP 503

senza generare valori inventati.

Questo conferma il comportamento controllato della catena:

    React
      ↓
    Backend
      ↓
    Data Agent unavailable
      ↓
    Controlled error

---

## 11.13 Failure test con ChromaDB offline

È stato eseguito un test equivalente rendendo ChromaDB non disponibile.

Una richiesta documentale ha prodotto:

    HTTP 503

senza permettere all'LLM di sostituire la policy aziendale con una risposta non grounded.

---

## 11.14 Verifica dei confini architetturali

I test integrati confermano inoltre che il Frontend utilizza esclusivamente:

    Node.js Backend

e non comunica direttamente con:

- Python Data Agent;
- ChromaDB;
- OpenAI API.

Questo comportamento è coerente con l'architettura a gateway applicativo definita nel System Architecture Document.

---

## 11.15 Matrice delle integrazioni verificate

| Integrazione | Stato |
|--------------|-------|
| React → Node Backend | PASS |
| Node Backend → OpenAI | PASS |
| Node Backend → ChromaDB | PASS |
| Node Backend → Python Data Agent | PASS |
| Data Agent → Manufacturing Dataset | PASS |
| Data Agent → Matplotlib | PASS |
| Node Backend → Chart Proxy | PASS |
| React → Chart Proxy | PASS |
| OpenAI → RAG Tool | PASS |
| OpenAI → Data Analysis Tool | PASS |
| OpenAI → Hybrid Tool Usage | PASS |
| Conversation state across requests | PASS |

---

## 11.16 Valutazione complessiva dell'integrazione

Le verifiche Full-Stack dimostrano che i componenti principali funzionano non soltanto isolatamente, ma anche come sistema integrato.

Sono stati verificati con successo:

- flusso conversazionale;
- flusso RAG;
- flusso Data Agent;
- flusso Hybrid;
- memoria conversazionale;
- comportamento bilingue;
- generazione dei grafici;
- Chart Proxy;
- gestione degli errori;
- indisponibilità controllata delle dipendenze.

Questi risultati forniscono l'evidenza principale che l'architettura finale soddisfa il comportamento richiesto dal progetto.

---

# 12. Test manuali e scenari di accettazione

## 12.1 Obiettivo

Oltre ai test automatici e alle verifiche sui singoli componenti, la versione finale di Maranello AI è stata sottoposta a una sessione di Quality Assurance manuale sul sistema integrato.

L'obiettivo è verificare i principali scenari utente attraverso l'architettura reale:

    User
      ↓
    React Frontend
      ↓
    Node.js Backend
      ↓
    AI Orchestrator
      ↓
    RAG / Data Agent / Hybrid
      ↓
    Final Response

Le verifiche manuali sono particolarmente importanti per i comportamenti dipendenti dal Large Language Model, per i quali non è opportuno richiedere una corrispondenza testuale rigida della risposta.

Il criterio di valutazione considera invece:

- tool selezionati;
- dati utilizzati;
- policy recuperata;
- classificazione ottenuta;
- lingua della risposta;
- conservazione del contesto;
- presenza del grafico;
- comportamento in condizioni di errore.

---

## 12.2 Riepilogo degli scenari principali

Gli scenari di QA finale comprendono:

| ID | Scenario | Tipo | Esito |
|----|----------|------|-------|
| QA-01 | Recupero soglia critica dalla Quality Policy | RAG | PASS |
| QA-02 | Analisi mensile con generazione grafico | Data Analysis | PASS |
| QA-03 | Analisi SUP-07 e confronto generale | Hybrid | PASS |
| QA-04 | SUP-07 con Supplier Quality Procedure | Hybrid | PASS |
| QA-05 | Memoria conversazionale con valore `3.2%` | Multi-turn | PASS |
| QA-06 | Scenario italiano con valore `4.2%` | RAG / Multi-turn | PASS |
| QA-07 | Validazione whitespace nel Frontend | Negative | PASS |
| QA-08 | Payload Chat vuoto | API Negative | PASS |
| QA-09 | Data Agent non disponibile | Resilience | PASS |
| QA-10 | ChromaDB non disponibile | Resilience | PASS |

---

## 12.3 QA-01 — Critical defect threshold

### Obiettivo

Verificare che una domanda relativa alla soglia critica del defect rate utilizzi la Knowledge Base e restituisca il valore definito nella Manufacturing Quality Policy.

### Input concettuale

    What is the critical defect rate threshold according to the quality policy?

### Comportamento atteso

Il sistema deve utilizzare:

    search_knowledge_base

e recuperare la Manufacturing Quality Policy.

### Risultato atteso

    Defect rate > 3.5%
    Classification: Critical

### Esito

    PASS

La risposta è risultata coerente con la policy aziendale fittizia.

---

## 12.4 QA-02 — Monthly defect rate trend

### Obiettivo

Verificare l'intero percorso di analisi temporale, dalla richiesta dell'utente alla visualizzazione del grafico.

### Comportamento atteso

    User Question
          ↓
    analyze_manufacturing_data
          ↓
    Python Data Agent
          ↓
    Monthly Aggregation
          ↓
    Matplotlib Chart
          ↓
    Backend Chart Proxy
          ↓
    React Rendering

### Risultati di riferimento

Il dataset copre dodici mesi.

Tra i risultati osservati:

    April 2025 ≈ 2.10%
    May 2025   ≈ 2.10%
    August 2025 ≈ 1.78%

### Esito

    PASS

Sono stati verificati:

- routing verso il Data Agent;
- aggregazione mensile;
- risposta analitica;
- generazione del PNG;
- restituzione del `chartUrl`;
- esposizione tramite Chart Proxy;
- visualizzazione nell'interfaccia.

---

## 12.5 QA-03 — SUP-07 e classificazione generale

### Obiettivo

Verificare la combinazione tra risultato quantitativo e interpretazione documentale.

Il Data Agent identifica:

    SUP-07
    defect rate ≈ 2.99%

Durante le verifiche è stato osservato che una classificazione dipende dalla policy utilizzata.

La Manufacturing Quality Policy generale classifica un defect rate:

    > 2.0% and <= 3.5%

come:

    Warning

Questa verifica ha evidenziato l'importanza di specificare correttamente il contesto della policy.

### Esito

    PASS

Il comportamento è risultato tecnicamente coerente con la policy generale recuperata.

La verifica ha inoltre portato alla definizione di uno scenario più specifico dedicato alla Supplier Quality Procedure.

---

## 12.6 QA-04 — SUP-07 con Supplier Quality Procedure

### Obiettivo

Verificare la classificazione di SUP-07 utilizzando esplicitamente la procedura supplier-specific.

### Dato osservato

    SUP-07 defect rate ≈ 2.99%

### Supplier Quality Procedure

La procedura stabilisce:

    > 2.0% and <= 3.0%
    Observation

### Risultato atteso

    SUP-07 ≈ 2.99%
    Classification: Observation

### Esito

    PASS

La verifica conferma che il sistema può combinare correttamente:

- risultato numerico del Data Agent;
- contesto supplier;
- documento appropriato;
- soglia supplier-specific;
- classificazione finale.

---

## 12.7 QA-05 — Memoria conversazionale e soglia `3.2%`

### Obiettivo

Verificare che il sistema possa utilizzare un'informazione fornita in un turno precedente.

### Scenario concettuale

    User:
    Consider a supplier defect rate of 3.2%.

    User:
    How should it be classified according to the supplier procedure?

Il secondo turno deve mantenere il valore:

    3.2%

senza richiedere all'utente di ripeterlo.

### Supplier Quality Procedure

    > 3.0% and <= 4.0%
    Warning

### Risultato atteso

    Warning

### Esito

    PASS

La verifica conferma la continuità conversazionale e la corretta applicazione della policy.

---

## 12.8 QA-06 — Scenario italiano Critical

### Obiettivo

Verificare contemporaneamente:

- supporto della lingua italiana;
- retrieval della Supplier Quality Procedure;
- applicazione della soglia Critical;
- continuità del comportamento dell'orchestratore.

### Input concettuale

    Un supplier presenta un defect rate del 4,2%.
    Come deve essere classificato e gestito?

### Policy

    Supplier defect rate > 4.0%
    Classification: Critical

### Risultato atteso

La risposta deve:

- essere in italiano;
- classificare il valore come `Critical`;
- utilizzare la procedura supplier;
- descrivere l'escalation coerente con la Knowledge Base.

### Esito

    PASS

Il sistema ha inoltre recuperato correttamente il comportamento di escalation previsto per il livello critico.

---

## 12.9 QA-07 — Whitespace validation

### Obiettivo

Verificare che il Frontend non permetta l'invio di un messaggio privo di contenuto significativo.

### Input

Una stringa composta esclusivamente da spazi.

### Risultato atteso

    No request sent

Il controllo di invio deve rimanere disabilitato.

### Esito

    PASS

---

## 12.10 QA-08 — Empty Chat payload

### Obiettivo

Verificare che il Backend protegga autonomamente il contratto API anche quando la validazione Frontend viene bypassata.

### Input

    {
      "message": ""
    }

### Risultato atteso

    HTTP 400

### Esito

    PASS

La richiesta non viene trattata come una conversazione valida.

---

## 12.11 QA-09 — Data Agent unavailable

### Obiettivo

Verificare il comportamento di Maranello AI quando il servizio necessario per un'analisi quantitativa non è disponibile.

### Scenario

    Numerical Question
          ↓
    analyze_manufacturing_data
          ↓
    Data Agent unavailable

### Risultato atteso

    HTTP 503

con messaggio applicativo:

    Manufacturing data analysis is temporarily unavailable. Please try again later.

### Esito

    PASS

Il sistema non ha sostituito il risultato mancante con un valore generato dal modello.

---

## 12.12 QA-10 — ChromaDB unavailable

### Obiettivo

Verificare il comportamento quando la Knowledge Base non è raggiungibile.

### Scenario

    Policy Question
          ↓
    search_knowledge_base
          ↓
    ChromaDB unavailable

### Risultato atteso

    HTTP 503

con messaggio applicativo:

    The company knowledge base is temporarily unavailable. Please try again later.

### Esito

    PASS

Il sistema non ha utilizzato la conoscenza generale del modello per simulare una policy aziendale non recuperabile.

---

## 12.13 Valutazione degli scenari manuali

I dieci scenari principali della QA finale hanno prodotto:

    Executed scenarios: 10
    Passed scenarios:   10
    Failed scenarios:    0

Risultato:

    PASS RATE = 100%

Il valore si riferisce esclusivamente agli scenari manuali formalizzati nella presente sezione e non rappresenta una misura di code coverage.

---

# 13. Risultati delle attività di test

## 13.1 Obiettivo

La presente sezione consolida i risultati delle verifiche eseguite sulla versione finale di Maranello AI.

I risultati vengono distinti tra:

- controlli statici;
- test automatici;
- verifiche dei servizi;
- verifiche Full-Stack;
- scenari manuali;
- resilience testing.

---

## 13.2 Backend

Risultato finale:

| Verifica | Esito |
|----------|-------|
| TypeScript Type Check | PASS |
| Lint | PASS |
| Automated Test Suite | PASS |
| Build | PASS |

Suite automatizzata:

    Test files: 15
    Tests:      86
    Result:     PASS

Non sono presenti test falliti nella suite finale utilizzata per la validazione.

---

## 13.3 Frontend

Risultato finale:

| Verifica | Esito |
|----------|-------|
| Lint | PASS |
| Production Build | PASS |
| UI startup | PASS |
| Chat interaction | PASS |
| Loading state | PASS |
| Empty input prevention | PASS |
| Error rendering | PASS |
| Chart rendering | PASS |

Non viene dichiarata una suite automatizzata di unit test React quando non presente nella versione corrente.

---

## 13.4 Python Data Agent

Le verifiche hanno confermato il corretto comportamento delle funzionalità principali.

| Area | Esito |
|------|-------|
| Dataset loading | PASS |
| Duplicate handling | PASS |
| Data normalization | PASS |
| KPI calculation | PASS |
| Grouped analysis | PASS |
| Monthly analysis | PASS |
| Question interpretation | PASS |
| Unsupported combination handling | PASS |
| Chart generation | PASS |
| Health endpoint | PASS |

---

## 13.5 KPI di riferimento

I KPI finali utilizzati come riferimento sono:

| KPI | Valore |
|-----|-------:|
| Total production | `164060` |
| Total defective units | `3272` |
| Defect rate | `1.99%` |
| Rework rate | `0.96%` |
| Scrap rate | `0.51%` |
| Average quality score | `95.82` |
| Average downtime | `33.04 min` |
| Average cycle time | `84.74 sec` |

Questi valori permettono di verificare la stabilità delle elaborazioni deterministiche.

---

## 13.6 Pattern analitici verificati

I pattern principali osservati includono:

| Dimensione | Risultato significativo |
|------------|-------------------------|
| Production Line | Line 3 ≈ `2.47%` defect rate |
| Shift | Night ≈ `2.35%` defect rate |
| Supplier | SUP-07 ≈ `2.99%` defect rate |
| Component | Electronics ≈ `2.49%` defect rate |
| Monthly high | Aprile/Maggio ≈ `2.10%` |
| Monthly low | Agosto ≈ `1.78%` |

I risultati sono coerenti con le relazioni sintetiche incorporate intenzionalmente nel dataset.

---

## 13.7 RAG

Risultato finale:

| Verifica | Esito |
|----------|-------|
| Knowledge Base ingestion | PASS |
| 5 documents indexed | PASS |
| 149 chunks available | PASS |
| English retrieval | PASS |
| Italian cross-language retrieval | PASS |
| Quality policy retrieval | PASS |
| Supplier procedure retrieval | PASS |
| Source attribution | PASS |
| ChromaDB failure handling | PASS |

---

## 13.8 Orchestrazione

Risultato finale:

| Scenario | Esito |
|----------|-------|
| Direct conversational response | PASS |
| RAG routing | PASS |
| Data Agent routing | PASS |
| Hybrid routing | PASS |
| Multiple tool usage | PASS |
| Function output handling | PASS |
| Conversation continuity | PASS |
| Italian response | PASS |
| English response | PASS |
| Scope preservation | PASS |

---

## 13.9 Full-Stack

Le integrazioni principali risultano:

| Integrazione | Esito |
|--------------|-------|
| React → Node.js | PASS |
| Node.js → OpenAI | PASS |
| Node.js → ChromaDB | PASS |
| Node.js → Data Agent | PASS |
| Data Agent → CSV | PASS |
| Data Agent → Matplotlib | PASS |
| Node.js → Chart Proxy | PASS |
| React → Chart Proxy | PASS |
| RAG tool execution | PASS |
| Data tool execution | PASS |
| Hybrid execution | PASS |
| Session continuity | PASS |

---

## 13.10 Resilienza

Sono state verificate due dipendenze critiche.

### Data Agent unavailable

    Result: PASS
    HTTP: 503

### ChromaDB unavailable

    Result: PASS
    HTTP: 503

In entrambi i casi il sistema adotta un comportamento fail-safe e non genera informazioni sostitutive non verificabili.

---

## 13.11 Stato dei difetti bloccanti

Al termine della QA documentata non risultano difetti bloccanti noti relativi ai principali scenari richiesti dal progetto.

Eventuali limitazioni della versione corrente vengono documentate separatamente e non vengono classificate automaticamente come difetti quando rappresentano funzionalità intenzionalmente escluse dallo scope.

---

## 13.12 Valutazione complessiva

Il risultato complessivo delle attività eseguite è:

    Backend automated tests     PASS
    Backend type check          PASS
    Backend lint                PASS
    Backend build               PASS
    Frontend lint               PASS
    Frontend build              PASS
    Data Agent verification     PASS
    RAG verification            PASS
    AI orchestration            PASS
    Full-Stack integration      PASS
    Manual QA scenarios         PASS
    Resilience scenarios        PASS

Sulla base delle verifiche eseguite, la versione corrente risulta tecnicamente idonea a proseguire verso la fase di finalizzazione documentale e preparazione della presentazione.

---

# 14. Sicurezza e verifiche di configurazione

## 14.1 Obiettivo

Le verifiche di sicurezza della versione corrente non costituiscono un penetration test formale.

L'obiettivo è verificare i principali controlli applicativi e di configurazione coerenti con lo scope del progetto:

- gestione dei segreti;
- validazione degli input;
- separazione dei servizi;
- protezione dei grafici;
- gestione controllata degli errori;
- riduzione dell'esecuzione arbitraria;
- esclusione degli artefatti locali dal repository.

---

## 14.2 Gestione dei segreti

Le credenziali del provider AI vengono fornite attraverso variabili d'ambiente.

Il codice non deve contenere:

    hardcoded API keys

Il repository utilizza:

    .env

per la configurazione locale e:

    .env.example

come template documentale.

Il file contenente i valori reali deve essere escluso dal versionamento.

---

## 14.3 Verifica `.gitignore`

La configurazione Git deve impedire il versionamento involontario di:

- `.env`;
- `node_modules`;
- build artifacts;
- directory `dist`;
- grafici generati;
- file temporanei;
- artefatti locali non necessari;
- `.DS_Store`.

Questa verifica riduce il rischio di pubblicare segreti o file runtime nel repository finale.

---

## 14.4 Rotazione delle credenziali

Durante lo sviluppo una credenziale del provider AI è stata potenzialmente esposta nel contesto di una verifica visiva.

La credenziale è stata quindi ruotata.

La chiave precedente non deve essere considerata valida né essere riportata nella documentazione finale.

Questo evento evidenzia l'importanza della rotazione immediata delle credenziali quando esiste anche soltanto il rischio di esposizione.

---

## 14.5 Secret verification

Prima della finalizzazione del repository viene verificata l'assenza di credenziali reali nei file destinati al commit.

L'obiettivo è confermare che:

- `.env` non venga tracciato;
- `.env.example` contenga esclusivamente placeholder;
- documentazione e codice non contengano API key reali;
- i file staged non contengano segreti noti.

La verifica deve essere ripetuta prima del commit documentale finale e prima della consegna.

---

## 14.6 Input validation

L'endpoint Chat valida il contenuto del messaggio.

Input non validi, come:

    ""

o contenuto esclusivamente whitespace, non devono essere trattati come richieste AI valide.

La validazione riduce:

- chiamate inutili al provider;
- input applicativi inconsistenti;
- comportamenti non previsti.

---

## 14.7 Chart Proxy security

Il Chart Proxy rappresenta un punto in cui un parametro controllato dal client viene utilizzato per richiedere una risorsa interna.

Per questo motivo il `filename` viene validato.

Il sistema deve impedire:

- path traversal;
- percorsi arbitrari;
- utilizzo del proxy verso risorse non previste.

Sono consentiti esclusivamente riferimenti compatibili con i grafici generati dal sistema.

---

## 14.8 Isolamento del Data Agent

Il Frontend non utilizza direttamente il Data Agent.

La comunicazione avviene secondo:

    Browser
       ↓
    Node.js Backend
       ↓
    Python Data Agent

Questo permette al Backend di mantenere il controllo sul contratto applicativo e riduce l'accoppiamento tra browser e servizi interni.

---

## 14.9 Isolamento di ChromaDB

Analogamente, il browser non accede direttamente a ChromaDB.

Il flusso è:

    Browser
       ↓
    Backend
       ↓
    RAG Connector
       ↓
    ChromaDB

Le operazioni sul vector database rimangono quindi interne al livello di orchestrazione.

---

## 14.10 Isolamento del provider AI

La OpenAI API key non viene esposta al Frontend.

Le chiamate al provider vengono effettuate esclusivamente dal Backend.

Architettura:

    React
      ↓
    Node.js Backend
      ↓
    OpenAI API

e non:

    React
      ↓
    OpenAI API

Questa separazione impedisce di distribuire la credenziale del provider nel codice client.

---

## 14.11 Deterministic Data Agent come controllo di sicurezza

La versione finale del Data Agent non esegue arbitrariamente codice Python prodotto dal Large Language Model.

Il modello seleziona il tool, ma il servizio Python interpreta la richiesta attraverso un insieme controllato di operazioni analitiche.

Il flusso è:

    LLM tool decision
          ↓
    Natural-language analytical request
          ↓
    Deterministic Question Interpreter
          ↓
    Validated Pandas operation

Questo approccio riduce il rischio associato all'esecuzione dinamica di codice generato.

---

## 14.12 Error disclosure

Gli errori destinati all'utente devono comunicare il problema senza esporre inutilmente:

- stack trace;
- configurazioni interne;
- credenziali;
- percorsi locali;
- dettagli sensibili delle dipendenze.

Le eccezioni applicative vengono gestite centralmente dal Backend.

---

## 14.13 Fail-safe behaviour

Per le informazioni aziendali e numeriche viene adottato un principio di fail-safe behaviour.

Se il Data Agent non è disponibile:

    return controlled error

Se la Knowledge Base non è disponibile:

    return controlled error

Il sistema non deve:

    fabricate replacement information

Questa caratteristica rappresenta sia una misura di resilienza sia una protezione contro risposte AI non grounded.

---

## 14.14 Dipendenze npm

Durante le verifiche delle dipendenze Backend sono state rilevate vulnerabilità moderate associate a dipendenze di sviluppo della toolchain di testing.

Non è stato applicato automaticamente:

    npm audit fix --force

poiché una correzione forzata può introdurre breaking changes o modifiche non controllate delle dipendenze.

La gestione scelta consiste nel:

- valutare la severità;
- distinguere dipendenze runtime e development;
- evitare aggiornamenti distruttivi non necessari;
- documentare il rischio residuo;
- prevedere aggiornamenti controllati futuri.

Le vulnerabilità moderate note non vengono rappresentate come inesistenti, ma non risultano bloccanti per lo scope dimostrativo corrente.

---

## 14.15 Limitazioni delle verifiche di sicurezza

Nella versione corrente non sono stati eseguiti formalmente:

- penetration test;
- SAST enterprise;
- DAST;
- dependency scanning come release gate automatizzato;
- container security scanning;
- threat modeling formale completo;
- OWASP assessment completo;
- security testing con strumenti specializzati;
- vulnerability remediation SLA.

Queste attività appartengono a un livello production-grade e vengono considerate possibili evoluzioni future.

---

## 14.16 Valutazione complessiva della sicurezza

Le verifiche eseguite confermano la presenza dei principali controlli coerenti con lo scope del progetto:

| Controllo | Stato |
|-----------|-------|
| API key tramite environment variable | PASS |
| `.env` escluso dal repository | PASS |
| `.env.example` senza segreti reali | PASS |
| Input Chat validation | PASS |
| Frontend senza provider API key | PASS |
| Data Agent non esposto direttamente al Frontend | PASS |
| ChromaDB non esposto direttamente al Frontend | PASS |
| Chart filename validation | PASS |
| Path traversal protection | PASS |
| Controlled dependency failures | PASS |
| Arbitrary LLM-generated Python execution evitata | PASS |
| Generated charts esclusi dal versionamento | PASS |

Le verifiche sono adeguate allo scope accademico e dimostrativo della versione corrente, pur non sostituendo un processo formale di security assessment necessario per un eventuale deployment enterprise reale.

---

# 15. Limitazioni e attività future

## 15.1 Obiettivo

Le verifiche documentate nelle sezioni precedenti dimostrano il corretto funzionamento dei requisiti principali di Maranello AI.

La versione corrente rimane tuttavia un progetto accademico e dimostrativo progettato per rappresentare un'architettura enterprise senza implementare tutte le caratteristiche che sarebbero necessarie per un deployment produttivo reale.

Le limitazioni descritte nella presente sezione non rappresentano automaticamente difetti.

Si tratta principalmente di funzionalità:

- intenzionalmente escluse dallo scope;
- non richieste per il completamento del progetto;
- considerate possibili evoluzioni future;
- appartenenti a un livello di maturità production-grade superiore a quello necessario per il capstone.

---

## 15.2 Automated Frontend Testing

La versione corrente verifica il Frontend attraverso:

- linting;
- production build;
- verifiche funzionali manuali;
- test Full-Stack.

Non è presente una suite automatizzata dedicata di:

- React unit test;
- component test;
- browser End-to-End test.

Una possibile evoluzione potrebbe introdurre strumenti dedicati per verificare automaticamente:

- rendering dei componenti;
- gestione dello stato;
- invio dei messaggi;
- loading state;
- error state;
- rendering dei grafici;
- conversazioni multi-turn.

---

## 15.3 End-to-End browser automation

I principali flussi utente sono stati verificati manualmente attraverso l'interfaccia React.

Non è presente una suite browser automation dedicata.

Una futura evoluzione potrebbe automatizzare scenari quali:

    Open application
          ↓
    Submit question
          ↓
    Wait for response
          ↓
    Validate answer
          ↓
    Validate chart
          ↓
    Submit follow-up
          ↓
    Validate conversation continuity

Questa automazione potrebbe essere utilizzata come regression suite prima dei rilasci.

---

## 15.4 Performance testing

La versione corrente non include benchmark formali relativi a:

- response time percentile;
- throughput;
- concurrent users;
- requests per second;
- CPU utilization;
- memory utilization;
- vector retrieval latency sotto carico;
- Data Agent throughput;
- LLM latency distribution.

Durante lo sviluppo è stato verificato che il sistema abbia tempi di risposta compatibili con l'utilizzo dimostrativo, ma questa osservazione non viene considerata un performance benchmark formale.

---

## 15.5 Load e stress testing

Non sono stati eseguiti test formali per determinare:

- numero massimo di utenti concorrenti;
- limite di richieste simultanee;
- comportamento sotto saturazione;
- limite operativo del Data Agent;
- limite operativo di ChromaDB;
- degradazione sotto elevato carico.

Tali verifiche diventerebbero necessarie prima di utilizzare un'architettura equivalente in un contesto produttivo reale.

---

## 15.6 Persistenza delle conversazioni

Il Conversation Manager utilizza uno stato in-memory.

Questo significa che:

- le conversazioni appartengono al processo Backend corrente;
- un riavvio del processo elimina lo stato;
- non è presente una persistenza distribuita;
- più istanze Backend non condividerebbero automaticamente la stessa sessione.

Una possibile evoluzione production-grade potrebbe utilizzare un datastore dedicato per la persistenza delle conversazioni.

La scelta in-memory è adeguata allo scope corrente e mantiene semplice la dimostrazione del comportamento multi-turn.

---

## 15.7 Autenticazione e autorizzazione

La versione corrente non implementa un sistema enterprise di:

- autenticazione;
- Single Sign-On;
- Role-Based Access Control;
- permission management;
- identity federation.

Il progetto è stato progettato in modo da poter evolvere verso una Knowledge Base con accesso differenziato per ruolo, ma tale controllo non viene rappresentato come funzionalità implementata.

Una futura versione potrebbe introdurre categorie come:

- Quality Engineer;
- Manufacturing Engineer;
- Supplier Quality Engineer;
- Production Manager;
- Administrator.

Il retrieval potrebbe quindi filtrare i documenti sulla base delle autorizzazioni associate all'utente.

---

## 15.8 Persistenza e lifecycle dei grafici

I grafici vengono generati come file PNG durante l'esecuzione delle analisi.

La versione corrente non implementa un lifecycle management avanzato per:

- retention;
- cleanup schedulato;
- object storage;
- versionamento;
- CDN;
- distribuzione multi-instance.

I file generati sono esclusi dal versionamento Git.

Una soluzione production-grade potrebbe utilizzare storage dedicato e politiche automatiche di scadenza.

---

## 15.9 Scalabilità del Backend

Il Backend è progettato secondo una separazione modulare delle responsabilità, ma la gestione in-memory delle conversazioni limita direttamente la scalabilità orizzontale senza ulteriori componenti.

Per una futura architettura distribuita potrebbero essere introdotti:

- persistent session store;
- shared cache;
- load balancer;
- multiple Backend instances;
- centralized logging;
- distributed tracing.

Queste caratteristiche non sono necessarie per la versione dimostrativa corrente.

---

## 15.10 Scalabilità del Data Agent

Il Python Data Agent carica e analizza un dataset CSV locale.

Questa soluzione è adeguata al Manufacturing Dataset dimostrativo.

In presenza di volumi enterprise reali potrebbe essere necessario utilizzare:

- database analitici;
- data warehouse;
- distributed processing;
- caching;
- pre-aggregazioni;
- query engine dedicati.

Il contratto a microservizio permette di sostituire in futuro l'implementazione analitica mantenendo il Backend relativamente indipendente dalla tecnologia utilizzata.

---

## 15.11 Scalabilità della Knowledge Base

ChromaDB viene utilizzato localmente per la versione corrente.

Una futura implementazione enterprise potrebbe richiedere:

- deployment distribuito;
- backup;
- replica;
- lifecycle degli embedding;
- versionamento dei documenti;
- document approval workflow;
- metadata filtering avanzato;
- access control;
- re-indexing automatizzato.

Il design corrente dimostra il pattern RAG senza introdurre infrastruttura non necessaria allo scope del progetto.

---

## 15.12 Valutazione AI automatizzata

Le verifiche AI correnti combinano:

- test automatici delle componenti deterministiche;
- osservazione dei tool utilizzati;
- QA manuale;
- confronto con dataset e Knowledge Base controllati.

Non è presente una piattaforma automatizzata di LLM evaluation basata su:

- golden dataset esteso;
- semantic similarity scoring;
- LLM-as-a-judge;
- hallucination scoring;
- retrieval precision;
- retrieval recall;
- answer relevance benchmark.

Una futura evoluzione potrebbe introdurre un evaluation dataset versionato con prompt, tool attesi, fonti attese e criteri di scoring.

---

## 15.13 Security testing avanzato

Come descritto nella sezione precedente, la versione corrente non comprende:

- penetration testing formale;
- SAST enterprise;
- DAST;
- security scanning automatizzato come release gate;
- formal threat modeling completo;
- vulnerability management workflow.

Queste attività sarebbero necessarie prima di un deployment enterprise reale.

---

## 15.14 CI/CD

Il progetto finale non dichiara come implementata una pipeline CI/CD completa.

Le verifiche finali vengono eseguite localmente attraverso gli strumenti disponibili nei singoli componenti.

Una possibile pipeline futura potrebbe automatizzare:

    Checkout
       ↓
    Install Dependencies
       ↓
    Lint
       ↓
    Type Check
       ↓
    Automated Tests
       ↓
    Build
       ↓
    Security Checks
       ↓
    Integration Tests
       ↓
    Release

La pipeline rappresenta un'evoluzione futura e non viene utilizzata come evidenza delle verifiche documentate nel presente Test Plan.

---

## 15.15 Containerizzazione

La versione finale non richiede Docker o Docker Compose per dimostrare il funzionamento del sistema.

I servizi vengono avviati direttamente nei rispettivi runtime.

Una futura containerizzazione potrebbe standardizzare:

- ambiente Node.js;
- ambiente Python;
- ChromaDB;
- configurazione di rete;
- startup dei servizi;
- deployment.

L'assenza di containerizzazione non impedisce il soddisfacimento dei requisiti funzionali del progetto.

---

## 15.16 Monitoring e observability

La versione corrente utilizza logging applicativo e health endpoint, ma non implementa una piattaforma completa di observability.

Possibili evoluzioni includono:

- centralized logging;
- metrics collection;
- dashboards;
- alerting;
- distributed tracing;
- token usage monitoring;
- LLM latency monitoring;
- tool failure metrics;
- retrieval quality metrics.

---

## 15.17 Testing su dati reali

Il Manufacturing Dataset è completamente sintetico.

Questo garantisce:

- assenza di dati aziendali riservati;
- riproducibilità;
- controllo dei pattern;
- possibilità di inserire anomalie intenzionali.

Di conseguenza, i risultati non devono essere interpretati come indicatori di un processo produttivo reale.

Un utilizzo enterprise richiederebbe ulteriori verifiche su dati autorizzati e controllati.

---

## 15.18 Evoluzione del Data Agent

L'assegnazione permette un approccio basato su pandas agent o interprete di codice.

Maranello AI adotta intenzionalmente un approccio deterministico.

Una possibile evoluzione potrebbe introdurre un sistema più flessibile capace di generare dinamicamente nuove analisi.

Tale evoluzione richiederebbe tuttavia controlli aggiuntivi relativi a:

- sandboxing;
- arbitrary code execution;
- resource limits;
- package access;
- filesystem access;
- network access;
- reproducibility;
- validation dei risultati.

La versione corrente privilegia sicurezza, testabilità e prevedibilità.

---

## 15.19 Sintesi delle limitazioni

| Area | Stato corrente | Possibile evoluzione |
|------|----------------|----------------------|
| Frontend testing | Manual + lint/build | Automated component/E2E tests |
| Performance | Non formalizzato | Benchmark e performance suite |
| Load testing | Non implementato | Concurrent load testing |
| Conversation persistence | In-memory | Persistent shared store |
| Authentication | Non implementata | Enterprise identity |
| Authorization | Non implementata | RBAC |
| Chart storage | Local | Managed object storage |
| Backend scaling | Single local instance | Horizontal scaling |
| Data processing | Local CSV/Pandas | Enterprise analytical platform |
| Vector DB | Local ChromaDB | Managed/distributed vector store |
| AI evaluation | Manual + functional | Automated evaluation framework |
| Security testing | Basic controls | Formal security assessment |
| CI/CD | Non implementata | Automated delivery pipeline |
| Containerization | Non richiesta | Docker-based deployment |
| Observability | Logging + health | Centralized observability |

---

# 16. Criteri di accettazione finale

## 16.1 Obiettivo

I criteri di accettazione finale stabiliscono quando Maranello AI può essere considerato tecnicamente completo rispetto allo scope del progetto.

L'accettazione non richiede l'assenza di qualsiasi possibile evoluzione futura.

Richiede invece che:

- i requisiti obbligatori siano implementati;
- i flussi principali funzionino;
- i test previsti per lo scope corrente siano superati;
- le limitazioni siano documentate;
- non siano presenti difetti bloccanti noti.

---

## 16.2 Architettura

| Criterio | Stato |
|----------|-------|
| React Frontend presente | PASS |
| Node.js Backend presente | PASS |
| Python Data Agent separato | PASS |
| ChromaDB presente | PASS |
| Knowledge Base presente | PASS |
| Manufacturing Dataset presente | PASS |
| AI Provider integrato | PASS |
| Architettura a microservizi rispettata | PASS |

---

## 16.3 Conversational Interface

| Criterio | Stato |
|----------|-------|
| Interfaccia chat React | PASS |
| Messaggi utente | PASS |
| Risposte assistant | PASS |
| Stato conversazionale | PASS |
| Loading/typing state | PASS |
| Gestione errori | PASS |
| Rendering grafici | PASS |
| Italiano | PASS |
| Inglese | PASS |

---

## 16.4 Autonomous AI routing

| Criterio | Stato |
|----------|-------|
| LLM decide autonomamente l'uso dei tool | PASS |
| Direct response supportata | PASS |
| RAG routing | PASS |
| Data Agent routing | PASS |
| Hybrid routing | PASS |
| Native function calling | PASS |
| Multiple tool execution | PASS |
| Final response synthesis | PASS |

Il requisito fondamentale di routing autonomo è quindi soddisfatto.

---

## 16.5 RAG

| Criterio | Stato |
|----------|-------|
| Knowledge Base locale | PASS |
| ChromaDB | PASS |
| Document ingestion | PASS |
| Chunking | PASS |
| Embedding | PASS |
| Semantic retrieval | PASS |
| Cross-language retrieval | PASS |
| Source attribution | PASS |
| Grounded policy answers | PASS |

---

## 16.6 Python Data Agent

| Criterio | Stato |
|----------|-------|
| Microservizio Python | PASS |
| FastAPI | PASS |
| Pandas | PASS |
| CSV loading | PASS |
| Data cleaning | PASS |
| KPI calculation | PASS |
| Trend analysis | PASS |
| Grouped analysis | PASS |
| Natural-language analytical requests | PASS |
| Chart generation | PASS |
| Narrative result integration | PASS |

L'approccio deterministico implementato soddisfa il ruolo richiesto al componente analitico mantenendo l'esecuzione controllata.

---

## 16.7 Manufacturing Dataset

| Criterio | Stato |
|----------|-------|
| Almeno 1000 righe | PASS |
| Dataset finale di 2000 righe | PASS |
| Date presenti | PASS |
| Categorie presenti | PASS |
| Metriche numeriche presenti | PASS |
| Anomalie intenzionali presenti | PASS |
| Duplicati presenti | PASS |
| Missing values presenti | PASS |
| Outlier presenti | PASS |
| Pattern analitici controllati | PASS |

---

## 16.8 Knowledge Base

| Criterio | Stato |
|----------|-------|
| Documentazione coerente con il business scenario | PASS |
| Policy qualità | PASS |
| Non-conformity procedure | PASS |
| Supplier quality procedure | PASS |
| Rework and scrap procedure | PASS |
| Production escalation policy | PASS |
| Contenuti fittizi e controllati | PASS |

---

## 16.9 API

| Criterio | Stato |
|----------|-------|
| `POST /api/chat` | PASS |
| Session management | PASS |
| `POST /api/analysis` | PASS |
| Backend health endpoint | PASS |
| Data Agent health endpoint | PASS |
| Chart Proxy | PASS |
| Input validation | PASS |
| Controlled errors | PASS |

---

## 16.10 Testing

| Criterio | Stato |
|----------|-------|
| Backend automated tests | PASS |
| 86 Backend tests superati | PASS |
| TypeScript type check | PASS |
| Backend lint | PASS |
| Backend build | PASS |
| Frontend lint | PASS |
| Frontend build | PASS |
| Data Agent verification | PASS |
| RAG verification | PASS |
| Orchestration verification | PASS |
| Full-Stack verification | PASS |
| Manual QA scenarios | PASS |
| Resilience verification | PASS |

---

## 16.11 Security baseline

| Criterio | Stato |
|----------|-------|
| Nessuna API key hardcoded | PASS |
| `.env` escluso dal versionamento | PASS |
| `.env.example` disponibile | PASS |
| Provider key non esposta al Frontend | PASS |
| Input validation | PASS |
| Chart filename validation | PASS |
| Path traversal protection | PASS |
| Controlled dependency failures | PASS |
| Arbitrary LLM-generated Python execution evitata | PASS |

---

## 16.12 Documentazione

La documentazione tecnica deve descrivere l'implementazione effettivamente realizzata.

I documenti principali comprendono:

- Project Vision and Scope;
- Software Requirements Specification;
- System Architecture Document;
- Data Model;
- API Specification;
- Test Plan;
- README finale.

Prima della consegna la documentazione deve essere verificata rispetto allo stato finale del repository.

---

## 16.13 Presentation readiness

Prima della consegna deve essere preparata una presentazione finale contenente almeno:

- business scenario;
- problema affrontato;
- valore della soluzione;
- architettura;
- routing autonomo dell'LLM;
- RAG;
- Python Data Agent;
- esempio RAG;
- esempio Data Analysis con grafico;
- esempio Hybrid;
- principali challenge tecniche;
- attività di debugging;
- risultati;
- GitHub repository.

La presentazione rappresenta una fase successiva alla chiusura della documentazione tecnica.

---

## 16.14 Clean clone acceptance

Prima della consegna finale deve essere eseguita un'ultima verifica partendo da un clone pulito del repository.

La procedura deve confermare che:

1. il repository possa essere clonato;
2. le dipendenze possano essere installate;
3. `.env.example` permetta di identificare la configurazione richiesta;
4. ChromaDB possa essere avviato;
5. la Knowledge Base possa essere indicizzata;
6. il Python Data Agent possa essere avviato;
7. il Backend Node.js possa essere avviato;
8. il Frontend React possa essere avviato;
9. gli health endpoint risultino disponibili;
10. una richiesta RAG funzioni;
11. una richiesta Data Analysis funzioni;
12. un grafico venga visualizzato.

Questa attività costituisce il final delivery verification e verrà eseguita dopo la finalizzazione del README.

---

## 16.15 Decisione di accettazione

Sulla base delle verifiche già completate:

    Core Architecture             PASS
    Backend                       PASS
    Python Data Agent             PASS
    RAG                           PASS
    AI Orchestration              PASS
    React Frontend                PASS
    Full-Stack Integration        PASS
    Automated Backend Tests       PASS
    Manual QA                     PASS
    Resilience                    PASS
    Security Baseline             PASS

Restano attività di finalizzazione relative principalmente a:

- completamento della documentazione;
- README finale;
- presentazione;
- clean clone verification;
- packaging della consegna.

Lo stato tecnico del software è quindi:

    SOFTWARE IMPLEMENTATION: ACCEPTED

mentre lo stato complessivo della consegna rimane subordinato al completamento delle attività finali documentali e di packaging.

---

# 17. Conclusioni

## 17.1 Sintesi

Il processo di testing di Maranello AI è stato progressivamente adattato all'architettura realmente implementata.

La strategia finale combina:

- static validation;
- test automatici;
- verifiche deterministiche;
- API testing;
- RAG testing;
- AI orchestration testing;
- resilience testing;
- Full-Stack testing;
- manual acceptance scenarios.

Questo approccio permette di verificare separatamente le componenti deterministiche e quelle dipendenti dal Large Language Model.

---

## 17.2 Principali evidenze

Le principali evidenze raccolte sono:

    Backend:
    15 test files
    86 automated tests
    Type Check PASS
    Lint PASS
    Build PASS

    Frontend:
    Lint PASS
    Build PASS

    Data Agent:
    KPI verification PASS
    Grouped analysis PASS
    Monthly analysis PASS
    Chart generation PASS

    RAG:
    5 documents
    149 chunks
    English retrieval PASS
    Cross-language retrieval PASS

    Orchestration:
    Direct PASS
    RAG PASS
    Data Analysis PASS
    Hybrid PASS
    Memory PASS
    Bilingual PASS

    Resilience:
    Data Agent unavailable PASS
    ChromaDB unavailable PASS

    Manual QA:
    10 scenarios executed
    10 scenarios passed

---

## 17.3 Qualità dell'architettura

Le attività di test hanno confermato la separazione delle responsabilità prevista dal progetto.

    LLM
    decides what is needed

    Knowledge Base
    provides company knowledge

    Data Agent
    provides numerical evidence

    Backend
    orchestrates the system

    Frontend
    provides the conversational experience

Questa separazione permette di limitare l'utilizzo del modello linguistico alle responsabilità per cui è appropriato, delegando dati e policy a fonti controllate.

---

## 17.4 Risultato finale

Non sono emersi difetti bloccanti noti nei principali flussi applicativi verificati.

Le limitazioni residue sono state documentate e riguardano principalmente funzionalità production-grade intenzionalmente escluse dallo scope corrente.

La versione finale soddisfa i principali obiettivi tecnici del progetto e risulta pronta per:

    Final Documentation Review
            ↓
    README Finalization
            ↓
    Presentation
            ↓
    Clean Clone Verification
            ↓
    Final Delivery

---

## 17.5 Considerazione finale

Maranello AI dimostra che un assistente AI enterprise può combinare efficacemente:

- ragionamento e orchestrazione tramite Large Language Model;
- conoscenza aziendale tramite Retrieval-Augmented Generation;
- analisi quantitativa tramite un servizio Python deterministico;
- memoria conversazionale;
- supporto bilingue;
- visualizzazione dei risultati;
- gestione controllata degli errori.

Le attività di testing confermano che questi elementi funzionano sia individualmente sia all'interno dell'architettura integrata.

Il Test Plan fornisce quindi una rappresentazione **as-built**, verificabile e coerente con lo stato finale del software.

---

## Stato del documento

| Informazione | Valore |
|--------------|--------|
| Documento | Test Plan |
| Versione | 2.0 |
| Stato | Final |
| Tipologia | As-Built Test Plan |
| Lingua | Italiano |
| Ultimo aggiornamento | Settembre 2026 |

---