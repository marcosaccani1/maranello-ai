# Software Requirements Specification

> **Progetto:** Maranello AI  
> **Versione:** 1.0  
> **Tipo documento:** Software Requirements Specification (SRS)  
> **Stato:** Draft  
> **Autore:** Marco Saccani  
> **Ultimo aggiornamento:** Luglio 2026

---

# Indice

1. Introduzione
2. Descrizione generale del sistema
3. Requisiti funzionali
4. Requisiti non funzionali
5. Business Rules
6. Casi d'uso principali
7. Criteri di accettazione

---

# 1. Introduzione

## 1.1 Scopo

Il presente documento descrive i requisiti software del progetto **Maranello AI**.

L'obiettivo è definire in maniera chiara, completa e verificabile tutte le funzionalità che il sistema dovrà implementare, costituendo il riferimento principale per le attività di progettazione, sviluppo e testing.

---

## 1.2 Obiettivi

Il sistema dovrà:

- fornire un'interfaccia conversazionale semplice da utilizzare;
- comprendere richieste formulate in linguaggio naturale;
- classificare automaticamente le richieste ricevute;
- interrogare una Knowledge Base aziendale tramite RAG;
- analizzare dati strutturati mediante un agente Python;
- integrare informazioni provenienti da più sorgenti;
- supportare italiano e inglese;
- restituire risposte affidabili e contestualizzate.

---

## 1.3 Definizioni

| Termine | Descrizione |
|----------|-------------|
| LLM | Large Language Model utilizzato come motore di orchestrazione. |
| RAG | Retrieval-Augmented Generation. |
| ChromaDB | Database vettoriale utilizzato per la ricerca semantica. |
| Data Agent | Microservizio Python dedicato all'analisi del dataset. |
| Knowledge Base | Collezione dei documenti aziendali. |
| Orchestrator | Backend incaricato di coordinare tutti i componenti. |

---

## 1.4 Riferimenti

Il presente documento fa riferimento ai seguenti documenti progettuali.

| Documento | Descrizione |
|------------|-------------|
| 01_Project_Vision_and_Scope.md | Visione generale del progetto |
| 03_System_Architecture.md | Architettura software |
| 04_Data_Model.md | Modello dati |
| 05_API_Design.md | Progettazione API |

---

# 2. Descrizione generale del sistema

## 2.1 Visione del sistema

Maranello AI è una piattaforma AI enterprise progettata per supportare il reparto Quality & Manufacturing Operations.

L'applicazione mette a disposizione un'unica interfaccia conversazionale capace di accedere sia alla documentazione aziendale sia ai dati produttivi.

L'utente non deve conoscere il funzionamento interno del sistema né scegliere manualmente quale componente utilizzare.

L'orchestratore AI identifica automaticamente la tipologia della richiesta e seleziona il flusso di elaborazione più appropriato.

---

## 2.2 Attori

| Attore | Descrizione |
|----------|-------------|
| Utente | Utilizza il sistema tramite la chat. |
| AI Orchestrator | Classifica la richiesta. |
| RAG Engine | Recupera documentazione aziendale. |
| Python Data Agent | Analizza il dataset. |
| Backend | Coordina tutti i servizi. |

---

## 2.3 Assunzioni

Si assume che:

- la Knowledge Base sia già indicizzata;
- il dataset sia disponibile localmente;
- il backend abbia accesso ai servizi AI;
- l'utente disponga di un browser moderno;
- tutte le API siano raggiungibili.

---

## 2.4 Vincoli

Il progetto dovrà rispettare i seguenti vincoli.

- utilizzo di React per il frontend;
- utilizzo di Node.js per il backend;
- utilizzo di Python per il Data Agent;
- utilizzo di ChromaDB come Vector Database;
- utilizzo di file CSV come sorgente dati;
- architettura a microservizi.

---

# 3. Requisiti funzionali

## 3.1 Frontend

### RF-001 — Invio di una richiesta

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Utente |
| Descrizione | Il sistema deve consentire l'invio di richieste testuali tramite la chat. |
| Input | Messaggio testuale |
| Output | Richiesta inoltrata al backend |
| Criterio di accettazione | Il messaggio compare nella conversazione e viene trasmesso al backend. |

---

### RF-002 — Visualizzazione della risposta

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Utente |
| Descrizione | Il sistema deve visualizzare la risposta restituita dal backend nella conversazione. |
| Input | Risposta del backend |
| Output | Messaggio AI visualizzato |
| Criterio di accettazione | La risposta viene mostrata senza perdita di formattazione. |

---

### RF-003 — Cronologia della conversazione

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Utente |
| Descrizione | La conversazione deve mantenere la cronologia dei messaggi durante la sessione. |
| Input | Sequenza dei messaggi |
| Output | Chat completa |
| Criterio di accettazione | I messaggi precedenti rimangono consultabili. |

---

### RF-004 — Indicatore di caricamento

| Campo | Valore |
|--------|--------|
| Priorità | Should Have |
| Attore | Utente |
| Descrizione | Durante l'elaborazione della richiesta deve essere mostrato un indicatore di caricamento. |
| Input | Richiesta inviata |
| Output | Loader |
| Criterio di accettazione | Il loader scompare automaticamente alla ricezione della risposta. |

---

### RF-005 — Visualizzazione dei grafici

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Utente |
| Descrizione | Il frontend deve visualizzare i grafici prodotti dal Data Agent. |
| Input | Immagine del grafico |
| Output | Grafico integrato nella chat |
| Criterio di accettazione | Il grafico è correttamente visualizzato senza download manuali. |

---

### RF-006 — Supporto bilingue

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Utente |
| Descrizione | L'interfaccia deve permettere l'utilizzo del sistema sia in italiano sia in inglese. |
| Input | Richiesta utente |
| Output | Risposta nella lingua appropriata |
| Criterio di accettazione | La risposta utilizza la stessa lingua della richiesta. |

---

## 3.2 Backend

### RF-007 — Ricezione delle richieste

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il backend deve ricevere le richieste provenienti dal frontend tramite API REST. |
| Input | Richiesta HTTP |
| Output | Richiesta inoltrata all'orchestratore AI |
| Criterio di accettazione | Ogni richiesta ricevuta viene elaborata senza perdita di informazioni. |

---

### RF-008 — Gestione della conversazione

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il backend deve mantenere il contesto della conversazione durante la sessione utente. |
| Input | Cronologia dei messaggi |
| Output | Conversazione contestualizzata |
| Criterio di accettazione | Le risposte tengono conto del contesto precedente. |

---

### RF-009 — Comunicazione con il modello AI

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il backend deve inviare il prompt al Large Language Model e riceverne la risposta. |
| Input | Prompt |
| Output | Risposta dell'LLM |
| Criterio di accettazione | La comunicazione avviene correttamente tramite API. |

---

### RF-010 — Comunicazione con il Data Agent

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il backend deve poter invocare il microservizio Python per le richieste analitiche. |
| Input | Richiesta di analisi |
| Output | Risultati dell'analisi |
| Criterio di accettazione | Il Data Agent restituisce correttamente dati e grafici. |

---

### RF-011 — Comunicazione con il motore RAG

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il backend deve interrogare il motore RAG quando richiesto dall'orchestratore. |
| Input | Query documentale |
| Output | Documenti rilevanti |
| Criterio di accettazione | I documenti recuperati vengono restituiti al backend. |

---

### RF-012 — Composizione della risposta finale

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il backend deve aggregare i risultati provenienti dai diversi componenti e costruire la risposta finale da inviare al frontend. |
| Input | Output dei servizi |
| Output | Risposta unica |
| Criterio di accettazione | L'utente riceve un'unica risposta coerente. |

---

# 3.3 AI Orchestrator

### RF-013 — Classificazione della richiesta

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | AI Orchestrator |
| Descrizione | L'LLM deve classificare automaticamente ogni richiesta identificandone la tipologia. |
| Input | Domanda dell'utente |
| Output | Categoria della richiesta |
| Criterio di accettazione | Ogni richiesta viene classificata come Documentale, Analitica oppure Ibrida. |

---

### RF-014 — Routing verso il motore RAG

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | AI Orchestrator |
| Descrizione | Le richieste documentali devono essere inoltrate al motore RAG. |
| Input | Richiesta documentale |
| Output | Invocazione del motore RAG |
| Criterio di accettazione | Il backend richiama esclusivamente il servizio RAG. |

---

### RF-015 — Routing verso il Data Agent

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | AI Orchestrator |
| Descrizione | Le richieste analitiche devono essere inoltrate esclusivamente al Python Data Agent. |
| Input | Richiesta analitica |
| Output | Invocazione del Data Agent |
| Criterio di accettazione | Nessuna interrogazione della Knowledge Base viene eseguita. |

---

### RF-016 — Routing ibrido

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | AI Orchestrator |
| Descrizione | Le richieste ibride devono attivare sia il motore RAG sia il Data Agent. |
| Input | Richiesta ibrida |
| Output | Attivazione di entrambi i servizi |
| Criterio di accettazione | Entrambi i componenti vengono eseguiti prima della generazione della risposta. |

---

### RF-017 — Selezione automatica della lingua

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | AI Orchestrator |
| Descrizione | Il sistema deve rilevare automaticamente la lingua della richiesta. |
| Input | Messaggio dell'utente |
| Output | Lingua della risposta |
| Criterio di accettazione | La risposta viene prodotta nella stessa lingua utilizzata dall'utente. |

---

### RF-018 — Generazione della risposta finale

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | AI Orchestrator |
| Descrizione | L'LLM deve integrare i risultati ottenuti dai servizi specializzati producendo una risposta chiara, coerente e contestualizzata. |
| Input | Output dei componenti |
| Output | Risposta finale |
| Criterio di accettazione | La risposta integra correttamente tutte le informazioni disponibili. |

---

# 3.4 Retrieval-Augmented Generation (RAG)

### RF-019 — Ricerca semantica nella Knowledge Base

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Il sistema deve effettuare ricerche semantiche all'interno della Knowledge Base utilizzando ChromaDB. |
| Input | Query dell'utente |
| Output | Documenti pertinenti |
| Criterio di accettazione | I documenti restituiti risultano coerenti con la richiesta. |

---

### RF-020 — Recupero dei documenti rilevanti

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Il sistema deve recuperare i documenti più rilevanti rispetto alla query ricevuta. |
| Input | Query documentale |
| Output | Lista di documenti |
| Criterio di accettazione | Vengono recuperati esclusivamente i documenti più pertinenti. |

---

### RF-021 — Utilizzo esclusivo della Knowledge Base

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Le risposte riguardanti procedure aziendali devono essere generate esclusivamente utilizzando i documenti presenti nella Knowledge Base. |
| Input | Documenti recuperati |
| Output | Contesto documentale |
| Criterio di accettazione | Nessuna informazione aziendale viene inventata dal modello. |

---

### RF-022 — Citazione delle fonti

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Ogni risposta documentale deve riportare i riferimenti ai documenti utilizzati. |
| Input | Documenti recuperati |
| Output | Elenco delle fonti |
| Criterio di accettazione | Le fonti sono sempre visibili all'utente. |

---

### RF-023 — Gestione delle informazioni mancanti

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | RAG Engine |
| Descrizione | Se la Knowledge Base non contiene informazioni sufficienti, il sistema deve dichiararlo esplicitamente. |
| Input | Risultato della ricerca |
| Output | Messaggio informativo |
| Criterio di accettazione | Il sistema non genera informazioni non supportate dalla documentazione. |

---

### RF-024 — Supporto bilingue della Knowledge Base

| Campo | Valore |
|--------|--------|
| Priorità | Should Have |
| Attore | RAG Engine |
| Descrizione | Il sistema deve interrogare documenti in italiano e in inglese senza differenze di comportamento. |
| Input | Query utente |
| Output | Documenti nella lingua appropriata |
| Criterio di accettazione | La ricerca funziona correttamente indipendentemente dalla lingua utilizzata. |

---

# 3.5 Python Data Agent

### RF-025 — Caricamento del dataset

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve caricare automaticamente il dataset CSV richiesto per l'analisi. |
| Input | Dataset CSV |
| Output | DataFrame |
| Criterio di accettazione | Il dataset viene caricato senza errori. |

---

### RF-026 — Pulizia dei dati

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il sistema deve individuare e gestire dati mancanti, duplicati e valori inconsistenti prima dell'analisi. |
| Input | Dataset |
| Output | Dataset pulito |
| Criterio di accettazione | Le anomalie vengono gestite automaticamente o segnalate. |

---

### RF-027 — Calcolo dei KPI

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il sistema deve calcolare automaticamente i principali KPI del processo produttivo. |
| Input | Dataset |
| Output | KPI |
| Criterio di accettazione | I KPI vengono restituiti correttamente. |

---

### RF-028 — Analisi statistiche

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il sistema deve produrre statistiche descrittive e confronti tra differenti gruppi di dati. |
| Input | Dataset |
| Output | Statistiche |
| Criterio di accettazione | Le statistiche risultano coerenti con il dataset analizzato. |

---

### RF-029 — Generazione di grafici

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il sistema deve generare grafici a supporto dell'analisi. |
| Input | Dataset |
| Output | Grafici |
| Criterio di accettazione | I grafici vengono prodotti automaticamente e restituiti al frontend. |

---

### RF-030 — Produzione degli insight

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Python Data Agent |
| Descrizione | Il Data Agent deve produrre una sintesi testuale dei risultati dell'analisi. |
| Input | Risultati numerici |
| Output | Insight descrittivi |
| Criterio di accettazione | L'utente riceve una spiegazione comprensibile dei risultati ottenuti. |

---

# 3.6 Gestione degli errori

### RF-031 — Gestione degli errori applicativi

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il sistema deve intercettare gli errori generati dai servizi interni e fornire un messaggio comprensibile all'utente. |
| Input | Eccezione applicativa |
| Output | Messaggio di errore |
| Criterio di accettazione | L'applicazione non termina in modo anomalo e informa correttamente l'utente. |

---

### RF-032 — Gestione dei timeout

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Il sistema deve gestire eventuali timeout nella comunicazione con i servizi esterni. |
| Input | Timeout |
| Output | Messaggio informativo |
| Criterio di accettazione | Il timeout viene gestito senza compromettere la stabilità dell'applicazione. |

---

### RF-033 — Gestione dell'indisponibilità dei servizi

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Se uno dei servizi non è disponibile, il sistema deve informare l'utente senza interrompere l'applicazione. |
| Input | Servizio non disponibile |
| Output | Notifica di errore |
| Criterio di accettazione | L'utente riceve una comunicazione chiara sull'errore riscontrato. |

---

# 3.7 Logging

### RF-034 — Logging delle richieste

| Campo | Valore |
|--------|--------|
| Priorità | Should Have |
| Attore | Backend |
| Descrizione | Il sistema deve registrare tutte le richieste elaborate. |
| Input | Richiesta utente |
| Output | Record di log |
| Criterio di accettazione | Ogni richiesta viene registrata con timestamp. |

---

### RF-035 — Logging degli errori

| Campo | Valore |
|--------|--------|
| Priorità | Must Have |
| Attore | Backend |
| Descrizione | Tutti gli errori applicativi devono essere registrati. |
| Input | Eccezione |
| Output | Record di log |
| Criterio di accettazione | Gli errori risultano consultabili nei log di sistema. |

---

### RF-036 — Logging del routing AI

| Campo | Valore |
|--------|--------|
| Priorità | Should Have |
| Attore | AI Orchestrator |
| Descrizione | Il sistema deve registrare quale componente è stato selezionato per ogni richiesta (RAG, Data Agent o Hybrid). |
| Input | Decisione dell'orchestratore |
| Output | Record di log |
| Criterio di accettazione | È possibile ricostruire il flusso di elaborazione di ogni richiesta. |

---

# 4. Requisiti non funzionali

| ID | Requisito | Priorità |
|----|-----------|-----------|
| RNF-001 | Il sistema deve essere facilmente manutenibile grazie a un'architettura modulare. | Must Have |
| RNF-002 | L'interfaccia utente deve essere intuitiva e utilizzabile senza formazione specifica. | Must Have |
| RNF-003 | Le API Key devono essere archiviate esclusivamente tramite variabili d'ambiente. | Must Have |
| RNF-004 | L'applicazione deve poter essere eseguita in ambiente locale. | Must Have |
| RNF-005 | Il sistema deve supportare sia la lingua italiana sia quella inglese. | Must Have |
| RNF-006 | Il codice deve essere organizzato secondo principi di separazione delle responsabilità. | Must Have |
| RNF-007 | Il backend deve poter integrare nuovi strumenti AI senza modificare il frontend. | Should Have |
| RNF-008 | L'architettura deve consentire l'aggiunta di nuovi microservizi. | Should Have |
| RNF-009 | Le risposte documentali devono riportare le fonti utilizzate. | Must Have |
| RNF-010 | L'applicazione deve risultare facilmente distribuibile mediante container Docker. | Should Have |

---

# 5. Business Rules

| ID | Regola |
|----|---------|
| BR-001 | Le procedure aziendali devono provenire esclusivamente dalla Knowledge Base. |
| BR-002 | Il sistema non deve inventare procedure o policy aziendali. |
| BR-003 | Le analisi statistiche devono utilizzare esclusivamente il dataset disponibile. |
| BR-004 | Le richieste ibride devono coinvolgere sia il motore RAG sia il Data Agent. |
| BR-005 | Ogni risposta documentale deve riportare le fonti utilizzate. |
| BR-006 | Il sistema deve rispondere nella stessa lingua utilizzata dall'utente. |
| BR-007 | L'utente non deve scegliere manualmente quale componente utilizzare. |
| BR-008 | L'orchestrazione deve essere completamente automatica. |

---

# 6. Casi d'uso principali

| ID | Caso d'uso | Componenti coinvolti |
|----|------------|----------------------|
| UC-001 | Consultazione di una procedura aziendale | Frontend, Backend, RAG |
| UC-002 | Analisi di KPI produttivi | Frontend, Backend, Data Agent |
| UC-003 | Generazione di grafici | Frontend, Backend, Data Agent |
| UC-004 | Analisi combinata dati e documentazione | Frontend, Backend, RAG, Data Agent |
| UC-005 | Conversazione bilingue | Frontend, Backend, AI Orchestrator |
| UC-006 | Gestione degli errori | Backend |

---

# 7. Criteri di accettazione

Il progetto sarà considerato conforme ai requisiti quando saranno soddisfatti i seguenti criteri.

| ID | Criterio |
|----|----------|
| AC-001 | L'utente può interagire tramite una chat web. |
| AC-002 | Il sistema identifica automaticamente la tipologia della richiesta. |
| AC-003 | Le richieste documentali attivano il motore RAG. |
| AC-004 | Le richieste analitiche attivano il Python Data Agent. |
| AC-005 | Le richieste ibride utilizzano entrambi i servizi. |
| AC-006 | Le risposte documentali riportano le fonti. |
| AC-007 | I grafici vengono visualizzati correttamente nell'interfaccia. |
| AC-008 | Il sistema supporta italiano e inglese. |
| AC-009 | L'applicazione gestisce gli errori senza interrompere la sessione utente. |
| AC-010 | Tutti i requisiti Must Have risultano implementati. |

---

# Conclusioni

Il presente documento definisce i requisiti funzionali e non funzionali del progetto **Maranello AI**, costituendo il riferimento principale per le successive attività di progettazione, implementazione e verifica.

La Software Requirements Specification rappresenta il collegamento tra la visione del progetto e la sua realizzazione tecnica, garantendo che ogni componente del sistema sia sviluppato in modo coerente con gli obiettivi definiti nel documento **Project Vision and Scope**.

I requisiti descritti saranno utilizzati come riferimento per la progettazione dell'architettura software, per la definizione dei casi di test e per la validazione finale del sistema.

---

## Stato del documento

| Informazione | Valore |
|--------------|--------|
| Documento | Software Requirements Specification |
| Versione | 1.0 |
| Stato | Draft |
| Lingua | Italiano |
| Prossimo documento | 03_System_Architecture.md |

---