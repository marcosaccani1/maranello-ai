# Project Vision and Scope

> **Progetto:** Maranello AI  
> **Versione:** 1.0  
> **Tipo documento:** Project Vision & Scope  
> **Stato:** Draft  
> **Autore:** Marco Saccani  
> **Ultimo aggiornamento:** Luglio 2026

---

# Indice

1. Project Vision
   - 1.1 Nome del progetto
   - 1.2 Panoramica
   - 1.3 Contesto aziendale
   - 1.4 Problema di business
   - 1.5 Soluzione proposta
   - 1.6 Esempi di richieste
   - 1.7 Obiettivi del progetto
   - 1.8 Valore del progetto
   - 1.9 Stakeholder
   - 1.10 Vision Statement

2. Project Scope
   - 2.1 Ambito del progetto
   - 2.2 Funzionalità incluse
   - 2.3 Funzionalità escluse
   - 2.4 Architettura generale
   - 2.5 Deliverable
   - 2.6 Criteri di successo
   - 2.7 Evoluzioni future

---

# 1. Project Vision

## 1.1 Nome del progetto

**Maranello AI**

Maranello AI è un assistente intelligente basato su Intelligenza Artificiale progettato per supportare il reparto **Quality & Manufacturing Operations** di un'azienda manifatturiera operante nel settore automotive di alta gamma.

Il progetto prende ispirazione dal distretto industriale di Maranello, senza fare riferimento ad alcuna azienda realmente esistente.

---

## 1.2 Panoramica del progetto

L'obiettivo del progetto è realizzare una piattaforma AI conversazionale capace di comprendere automaticamente la natura delle richieste formulate dagli utenti e scegliere autonomamente quale strumento utilizzare per produrre la risposta più corretta.

Il sistema integra in un'unica applicazione tre differenti capacità:

- consultazione della documentazione aziendale mediante Retrieval Augmented Generation (RAG);
- analisi di dati strutturati tramite un agente Python dedicato;
- combinazione dei risultati provenienti da entrambe le sorgenti.

L'utente interagisce esclusivamente attraverso una chat, senza dover conoscere la struttura interna del sistema né il funzionamento delle tecnologie utilizzate.

L'intero progetto è sviluppato seguendo un'architettura a microservizi con l'obiettivo di simulare un'applicazione enterprise moderna.

---

## 1.3 Contesto aziendale

Il reparto Quality & Manufacturing Operations gestisce quotidianamente due tipologie di informazioni.

### Documentazione aziendale

Le informazioni operative sono distribuite all'interno di numerosi documenti, tra cui:

- procedure operative;
- manuali di ispezione;
- standard qualitativi;
- procedure di escalation;
- policy interne;
- linee guida;
- documentazione fornitori;
- classificazione difetti;
- procedure di gestione delle non conformità;
- FAQ aziendali.

Questi documenti rappresentano il patrimonio informativo dell'azienda ma risultano spesso difficili da consultare rapidamente.

---

### Dati di produzione

Parallelamente vengono prodotti grandi volumi di dati strutturati relativi ai processi produttivi.

Tra questi:

- lotti di produzione;
- controlli qualità;
- componenti difettosi;
- rilavorazioni;
- scarti;
- linee produttive;
- turni;
- fornitori;
- tempi di fermo;
- costi della qualità;
- KPI produttivi;
- azioni correttive.

Queste informazioni vengono normalmente analizzate utilizzando strumenti differenti rispetto a quelli impiegati per consultare la documentazione.

La mancanza di integrazione tra dati e documenti rallenta il processo decisionale e aumenta il tempo necessario per ottenere informazioni affidabili.

---

## 1.4 Problema di business

L'azienda affronta principalmente tre criticità.

### Ricerca delle informazioni

La documentazione risulta difficile da consultare poiché:

- è distribuita in repository differenti;
- esistono documenti duplicati;
- sono presenti versioni obsolete;
- la terminologia non è uniforme;
- manca uno standard documentale condiviso.

Gli operatori impiegano tempo prezioso nella ricerca delle informazioni invece che nello svolgimento delle proprie attività.

---

### Analisi dei dati

L'analisi dei dati produttivi richiede competenze tecniche specifiche.

Le principali attività comprendono:

- calcolo di KPI;
- analisi dei trend;
- confronto tra linee produttive;
- confronto tra turni;
- identificazione di anomalie;
- valutazione dei fornitori;
- produzione di report;
- generazione di grafici.

Queste operazioni vengono generalmente svolte manualmente oppure utilizzando software dedicati.

---

### Mancanza di integrazione

L'aspetto più critico consiste nella separazione tra documentazione e dati.

Per rispondere a una singola domanda di business è spesso necessario:

- consultare procedure operative;
- analizzare dati numerici;
- confrontare i risultati;
- interpretare manualmente le informazioni.

Questo processo richiede tempo ed espone al rischio di errori interpretativi.

---

## 1.5 Soluzione proposta

Maranello AI introduce un unico punto di accesso alle informazioni aziendali.

L'utente può formulare domande in linguaggio naturale sia in italiano sia in inglese.

Il sistema utilizza un Large Language Model come motore di orchestrazione.

L'LLM non produce direttamente la risposta, ma decide quale componente del sistema deve essere eseguito.

Sono previste tre modalità operative.

### Modalità RAG

Quando la richiesta riguarda documentazione aziendale, il sistema interroga una Knowledge Base indicizzata tramite ChromaDB.

L'assistente recupera esclusivamente le informazioni realmente presenti nella documentazione e costruisce la risposta citando le fonti utilizzate.

Qualora non siano disponibili informazioni pertinenti, il sistema comunica esplicitamente l'assenza di documentazione evitando di generare contenuti non verificabili.

---

### Modalità Data Analysis

Quando la richiesta riguarda dati numerici o analisi statistiche, il backend delega l'elaborazione a un microservizio Python.

L'agente esegue automaticamente:

- caricamento del dataset;
- pulizia dei dati;
- analisi statistiche;
- calcolo dei KPI;
- produzione di grafici;
- generazione di insight.

I risultati vengono restituiti al backend che li presenta all'interno della chat.

---

### Modalità Ibrida

Le richieste più complesse richiedono contemporaneamente documentazione e dati.

In questi casi il sistema:

1. recupera le procedure aziendali pertinenti;
2. analizza il dataset;
3. confronta i risultati ottenuti;
4. genera una risposta unica supportata sia da evidenze documentali sia da analisi quantitative.

Questa rappresenta la caratteristica distintiva di Maranello AI rispetto ai tradizionali chatbot aziendali.

---

## 1.6 Esempi di richieste

Maranello AI è progettato per comprendere automaticamente la tipologia di richiesta formulata dall'utente e selezionare il componente più appropriato per elaborare la risposta.

Di seguito sono riportati alcuni esempi rappresentativi.

### Richieste documentali (RAG)

Queste richieste vengono soddisfatte interrogando esclusivamente la Knowledge Base aziendale.

| Richiesta | Componente utilizzato |
|-----------|-----------------------|
| Qual è la procedura per gestire una non conformità? | RAG |
| Come viene classificato un difetto critico? | RAG |
| Quali sono le responsabilità del Quality Manager? | RAG |
| Quando deve essere aperta una Corrective Action? | RAG |
| Qual è il processo di approvazione di una rilavorazione? | RAG |

---

### Richieste analitiche (Data Agent)

Queste richieste richiedono l'elaborazione del dataset produttivo.

| Richiesta | Componente utilizzato |
|-----------|-----------------------|
| Qual è il tasso medio di difetti dell'ultimo trimestre? | Data Agent |
| Quale linea produttiva presenta il maggior numero di scarti? | Data Agent |
| Mostrami il trend dei KPI qualità. | Data Agent |
| Confronta i turni di produzione. | Data Agent |
| Genera un grafico delle non conformità per mese. | Data Agent |

---

### Richieste ibride

Le richieste ibride richiedono contemporaneamente l'accesso alla documentazione e l'analisi dei dati.

| Richiesta | Componenti utilizzati |
|-----------|-----------------------|
| Le non conformità registrate rispettano la procedura aziendale? | RAG + Data Agent |
| Quali difetti stanno aumentando e quale procedura è prevista? | RAG + Data Agent |
| I tempi di rilavorazione rispettano gli standard interni? | RAG + Data Agent |
| Analizza gli scarti e suggerisci le procedure applicabili. | RAG + Data Agent |

---

## 1.7 Obiettivi del progetto

Il progetto nasce con l'obiettivo di dimostrare come differenti tecnologie di Intelligenza Artificiale possano essere integrate all'interno di un'unica piattaforma enterprise.

Gli obiettivi principali sono riportati nella tabella seguente.

| ID | Obiettivo |
|----|-----------|
| OBJ-01 | Centralizzare l'accesso alla documentazione aziendale. |
| OBJ-02 | Ridurre il tempo necessario per reperire informazioni operative. |
| OBJ-03 | Automatizzare l'analisi dei dati produttivi. |
| OBJ-04 | Consentire interrogazioni in linguaggio naturale. |
| OBJ-05 | Integrare documentazione e dati in un'unica risposta. |
| OBJ-06 | Dimostrare l'utilizzo di un'architettura AI a microservizi. |
| OBJ-07 | Realizzare un progetto riutilizzabile come portfolio professionale. |
| OBJ-08 | Garantire il supporto bilingue (Italiano e Inglese). |

---

## 1.8 Valore del progetto

Maranello AI non rappresenta semplicemente un chatbot aziendale.

Il progetto dimostra come un sistema AI moderno possa diventare uno strumento decisionale capace di combinare differenti sorgenti informative.

I principali benefici attesi sono:

- riduzione dei tempi di ricerca delle informazioni;
- miglioramento della qualità delle decisioni;
- maggiore accessibilità alla documentazione;
- automazione delle analisi ripetitive;
- supporto decisionale basato su dati e procedure;
- riduzione del rischio di interpretazioni errate;
- incremento dell'efficienza operativa.

Dal punto di vista tecnico il progetto dimostra inoltre l'integrazione di tecnologie moderne quali:

- Large Language Models;
- Retrieval Augmented Generation (RAG);
- Vector Database;
- Python Data Analysis;
- Microservizi;
- REST API;
- React;
- Node.js.

---

## 1.9 Stakeholder

Il progetto coinvolge differenti categorie di stakeholder.

| Stakeholder | Ruolo |
|--------------|--------|
| Quality Engineer | Consulta procedure e analizza indicatori di qualità. |
| Production Manager | Monitora le performance produttive. |
| Quality Manager | Supporta il processo decisionale. |
| Manufacturing Engineer | Analizza anomalie e trend produttivi. |
| System Administrator | Gestisce l'infrastruttura applicativa. |
| AI Developer | Sviluppa ed evolve il sistema. |

---

## 1.10 Vision Statement

La visione del progetto è quella di realizzare una piattaforma di Intelligenza Artificiale capace di trasformare la consultazione della documentazione aziendale e l'analisi dei dati in un'unica esperienza conversazionale.

Maranello AI mira a ridurre la complessità tecnologica percepita dagli utenti finali, consentendo loro di ottenere informazioni affidabili semplicemente formulando domande in linguaggio naturale.

Il progetto rappresenta inoltre una dimostrazione concreta di come un'architettura AI moderna possa integrare differenti strumenti specialistici mantenendo un'esperienza utente semplice, intuitiva e coerente.

---

# 2. Project Scope

## 2.1 Ambito del progetto

Il progetto prevede la progettazione e lo sviluppo di un sistema software composto da più componenti indipendenti, integrati attraverso un'architettura a microservizi.

L'applicazione consentirà agli utenti di:

- interrogare una Knowledge Base aziendale;
- analizzare un dataset manifatturiero;
- ottenere grafici e KPI;
- ricevere risposte contestualizzate;
- utilizzare il sistema sia in italiano sia in inglese;
- interagire mediante una chat web.

Il sistema deciderà automaticamente quale componente utilizzare in funzione della richiesta ricevuta.

---

## 2.2 Componenti del sistema

L'architettura sarà composta dai seguenti moduli principali.

| Componente | Responsabilità |
|------------|----------------|
| Frontend React | Interfaccia utente conversazionale. |
| Backend Node.js | Orchestrazione delle richieste e integrazione dei servizi. |
| Large Language Model | Classificazione delle richieste e generazione delle risposte. |
| Knowledge Base | Archiviazione della documentazione aziendale. |
| ChromaDB | Ricerca semantica dei documenti. |
| Python Data Agent | Analisi del dataset e generazione di grafici. |
| Dataset CSV | Fonte dati per le analisi quantitative. |

---

## 2.3 Funzionalità incluse

Il progetto comprenderà:

- chat conversazionale;
- supporto bilingue;
- Retrieval Augmented Generation;
- analisi dati automatica;
- generazione di grafici;
- orchestrazione AI;
- gestione della cronologia della conversazione;
- visualizzazione delle fonti documentali;
- gestione degli errori;
- architettura a microservizi.

---

## 2.4 Architettura generale

L'architettura di Maranello AI è progettata secondo un modello a microservizi, in cui ogni componente è responsabile di una specifica funzionalità.

Il frontend rappresenta l'unico punto di contatto con l'utente, mentre il backend svolge il ruolo di orchestratore dell'intero sistema.

Il Large Language Model analizza ogni richiesta ricevuta e determina quale componente debba essere utilizzato per produrre la risposta più appropriata.

L'architettura prevede tre possibili flussi di esecuzione:

- consultazione della Knowledge Base tramite Retrieval-Augmented Generation (RAG);
- analisi del dataset tramite il Python Data Agent;
- utilizzo combinato di entrambe le componenti per rispondere a richieste ibride.

L'obiettivo è garantire una chiara separazione delle responsabilità, elevata manutenibilità e possibilità di estendere il sistema con nuovi strumenti senza modificare l'architettura principale.

---

## 2.5 Deliverable del progetto

Al termine dello sviluppo il progetto comprenderà i seguenti deliverable.

| Deliverable | Descrizione |
|-------------|-------------|
| Frontend Web | Interfaccia conversazionale sviluppata in React. |
| Backend API | Servizio Node.js responsabile dell'orchestrazione. |
| Python Data Agent | Microservizio dedicato all'analisi dei dati. |
| Knowledge Base | Collezione di documenti aziendali indicizzati tramite ChromaDB. |
| Dataset | Dataset realistico relativo alle attività di Quality & Manufacturing Operations. |
| Documentazione tecnica | Documentazione completa del progetto in italiano e inglese. |
| Repository GitHub | Repository contenente codice, documentazione e istruzioni di installazione. |

---

## 2.6 Funzionalità escluse

Per mantenere il progetto focalizzato sugli obiettivi prefissati, alcune funzionalità non saranno incluse nella prima versione.

Tra queste:

- autenticazione e gestione utenti;
- integrazione con database aziendali reali;
- aggiornamento automatico della Knowledge Base;
- gestione dei permessi basata sui ruoli;
- caricamento dinamico di documenti da parte degli utenti;
- supporto multi-tenant;
- integrazione con sistemi ERP o MES;
- notifiche automatiche;
- dashboard amministrative.

Queste funzionalità potranno essere considerate come possibili evoluzioni future.

---

## 2.7 Vincoli del progetto

Lo sviluppo del progetto dovrà rispettare i seguenti vincoli.

### Vincoli funzionali

- Il sistema dovrà essere in grado di comprendere richieste formulate sia in italiano sia in inglese.
- Le risposte relative alle procedure aziendali dovranno essere generate esclusivamente utilizzando le informazioni presenti nella Knowledge Base.
- Le analisi numeriche dovranno essere eseguite esclusivamente sul dataset fornito.
- Il sistema dovrà distinguere automaticamente tra richieste documentali, analitiche e ibride.

### Vincoli tecnologici

Il progetto utilizzerà le seguenti tecnologie principali.

| Componente | Tecnologia |
|------------|------------|
| Frontend | React |
| Backend | Node.js |
| AI Orchestrator | OpenAI API |
| Vector Database | ChromaDB |
| Data Analysis | Python |
| Librerie Python | Pandas, Matplotlib |
| Dataset | CSV |
| Versionamento | Git & GitHub |

---

## 2.8 Criteri di successo

Il progetto sarà considerato completato con successo quando saranno soddisfatti i seguenti criteri.

### Obiettivi funzionali

- L'utente potrà porre domande in linguaggio naturale.
- Il sistema selezionerà automaticamente il componente corretto.
- Le richieste documentali utilizzeranno il motore RAG.
- Le richieste analitiche utilizzeranno il Python Data Agent.
- Le richieste ibride utilizzeranno entrambe le componenti.
- I grafici saranno visualizzati direttamente all'interno dell'interfaccia.
- Le fonti documentali saranno riportate nelle risposte generate tramite RAG.

---

### Obiettivi qualitativi

Il progetto dovrà dimostrare:

- modularità dell'architettura;
- semplicità di utilizzo;
- separazione delle responsabilità tra i componenti;
- facilità di manutenzione;
- possibilità di estensione futura;
- documentazione completa;
- codice leggibile e ben organizzato.

---

## 2.9 Evoluzioni future

L'architettura è stata progettata per poter essere estesa senza modificare il nucleo dell'applicazione.

Tra le possibili evoluzioni future si individuano:

- integrazione con database SQL;
- connessione a sistemi ERP e MES;
- autenticazione tramite provider esterni;
- gestione di ruoli e permessi;
- supporto a documenti PDF caricati dinamicamente;
- dashboard manageriali;
- generazione automatica di report PDF;
- pianificazione di analisi periodiche;
- integrazione con strumenti di Business Intelligence;
- utilizzo di modelli AI specializzati per differenti domini aziendali.

---

# Conclusioni

Maranello AI nasce con l'obiettivo di dimostrare come un'architettura basata su Intelligenza Artificiale possa semplificare l'accesso alla conoscenza aziendale e migliorare il processo decisionale attraverso l'integrazione tra documentazione e dati.

Il progetto non si limita allo sviluppo di un semplice chatbot, ma propone una piattaforma modulare capace di orchestrare differenti strumenti specializzati all'interno di un'unica esperienza conversazionale.

Grazie all'utilizzo di Retrieval-Augmented Generation, analisi dati tramite Python e orchestrazione mediante Large Language Model, Maranello AI rappresenta un esempio concreto di applicazione enterprise delle moderne tecnologie di Intelligenza Artificiale.

La struttura modulare adottata consente inoltre di estendere facilmente il sistema con nuovi servizi, rendendo il progetto un'ottima base sia per finalità didattiche sia per possibili sviluppi professionali futuri.

---

## Stato del documento

| Informazione | Valore |
|--------------|--------|
| Documento | Project Vision and Scope |
| Versione | 1.0 |
| Stato | Draft |
| Lingua | Italiano |
| Prossimo documento | 02_Software_Requirements_Specification.md |

---