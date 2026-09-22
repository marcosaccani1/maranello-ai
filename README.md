# Maranello AI

> Enterprise Hybrid AI Assistant for Manufacturing Quality & Operations, combining autonomous LLM orchestration, Retrieval-Augmented Generation and deterministic manufacturing data analysis.

---

## Disclaimer

Maranello AI is an entirely fictional project developed exclusively for educational, demonstration and portfolio purposes.

The project is **not affiliated with, endorsed by, or associated with Ferrari N.V. or any other automotive manufacturer**.

All company policies, procedures, operational scenarios and business documentation included in the project are fictional. The Manufacturing Dataset is synthetic and was created specifically for the project.

Any resemblance to real organizations, internal processes, datasets or business rules is purely coincidental.

---

# Overview

Maranello AI is an enterprise-oriented **Hybrid AI Assistant** designed for a fictional premium automotive manufacturer.

The system provides employees working in **Quality & Manufacturing Operations** with a single conversational interface capable of answering questions that require different types of enterprise information.

Instead of forcing the user to choose between separate applications for document search and data analysis, Maranello AI allows questions to be expressed directly in natural language.

The system can autonomously determine whether a request requires:

- a direct conversational response;
- enterprise knowledge retrieval through Retrieval-Augmented Generation;
- quantitative analysis of manufacturing data;
- or a combination of document retrieval and structured data analysis.

The core interaction model is:

    User Question
          ↓
    React Chat Interface
          ↓
    Node.js Backend
          ↓
    OpenAI Responses API
          ↓
    Autonomous Tool Selection
       /          \
      /            \
     ▼              ▼
    RAG        Python Data Agent
     │              │
     ▼              ▼
    Knowledge     Manufacturing
    Base          Dataset
      \             /
       \           /
        ▼         ▼
        LLM Synthesis
             ↓
        Final Answer

The user interacts only with the conversational interface.

The internal routing between AI capabilities is handled automatically by the system.

---

# Business Problem

Manufacturing organizations generate large amounts of both **unstructured knowledge** and **structured operational data**.

These two information sources are often accessed through completely different workflows.

Operational knowledge may be distributed across:

- manufacturing quality policies;
- non-conformity procedures;
- supplier quality procedures;
- rework and scrap procedures;
- production escalation policies.

At the same time, manufacturing performance is represented through structured information such as:

- production volumes;
- defective units;
- defect rates;
- rework rates;
- scrap rates;
- quality scores;
- downtime;
- cycle times;
- suppliers;
- production lines;
- shifts;
- component categories.

This creates a practical problem.

An employee may know **what happened** from operational data but still need to determine **what should happen according to company policy**.

For example:

    Which supplier has the highest defect rate,
    and how should that result be classified
    according to the Supplier Quality Procedure?

Answering this question requires two different forms of evidence:

    Manufacturing Dataset
            ↓
    Quantitative Evidence

            +

    Knowledge Base
            ↓
    Company Policy

            ↓

    Contextual Business Answer

Maranello AI was designed specifically to bridge this gap.

---

# Project Goals

The project demonstrates how multiple AI and data capabilities can be integrated behind a single enterprise conversational interface while maintaining clear architectural boundaries.

The main goals are to:

- provide a natural-language interface for manufacturing knowledge and data;
- support conversations in both Italian and English;
- automatically detect the language used by the user and respond accordingly;
- retrieve internal policies and procedures through semantic search;
- provide source-aware answers based on the enterprise Knowledge Base;
- calculate manufacturing KPIs from structured data;
- generate analytical charts directly from manufacturing data;
- autonomously select the appropriate AI tool for each request;
- combine RAG and quantitative analysis when both are required;
- preserve conversational context across multiple turns;
- reduce hallucination risk by separating the LLM from authoritative data sources;
- provide controlled behavior when internal dependencies are unavailable;
- demonstrate maintainable and testable enterprise AI architecture.

---

# Key Capabilities

## Autonomous AI Orchestration

Maranello AI uses the **OpenAI Responses API with native function calling**.

The Large Language Model is responsible for understanding the user's intent and deciding whether specialized tools are required.

The application exposes two primary tools to the model:

    search_knowledge_base

    analyze_manufacturing_data

Depending on the request, the model can follow four execution patterns:

| Mode | Tool Usage | Typical Scenario |
|------|------------|------------------|
| Direct | No tool | General conversational interaction |
| RAG | `search_knowledge_base` | Questions about company policies or procedures |
| Data Analysis | `analyze_manufacturing_data` | Questions about manufacturing KPIs or trends |
| Hybrid | Both tools | Questions requiring quantitative evidence and company policy |

There is no separate rule-based classifier that assigns the request to a predefined category before the model acts.

Tool selection is part of the LLM orchestration process itself.

---

## Retrieval-Augmented Generation

The system includes a local enterprise Knowledge Base containing fictional manufacturing policies and procedures.

Documents are indexed in **ChromaDB** and retrieved through semantic similarity.

The RAG pipeline enables the assistant to:

- retrieve relevant internal documentation;
- ground policy-related answers in enterprise knowledge;
- preserve source metadata;
- identify the document or section used in the answer;
- avoid inventing internal policies when supporting documentation is unavailable.

The final Knowledge Base contains **5 operational documents indexed into 149 chunks**.

---

## Manufacturing Data Analysis

Structured manufacturing analysis is delegated to a dedicated **Python FastAPI Data Agent**.

The service uses **Pandas** to clean and analyze a synthetic Manufacturing Dataset containing:

    2,000 production batch records
    20 attributes

The Data Agent supports:

- global manufacturing KPIs;
- defect-rate analysis;
- rework and scrap analysis;
- grouped comparisons;
- supplier analysis;
- production-line analysis;
- shift analysis;
- component-category analysis;
- vehicle-model analysis;
- plant analysis;
- operator-team analysis;
- monthly defect-rate trends;
- chart generation with Matplotlib.

Numerical results are calculated by the Data Agent rather than generated by the LLM.

---

## Deterministic Analytical Execution

The Python Data Agent intentionally does **not** execute arbitrary Python code generated by the Large Language Model.

Natural-language analytical requests are mapped to a controlled set of validated operations through a deterministic Question Interpreter.

This architectural decision prioritizes:

- security;
- reproducibility;
- predictability;
- testability;
- controlled analytical scope.

The LLM determines **when data analysis is required**, while the Python service controls **how the analysis is executed**.

This separation prevents the language model from becoming the source of quantitative truth.

---

## Hybrid Reasoning

Some business questions cannot be answered correctly using only documents or only structured data.

Maranello AI can combine both sources within the same interaction.

For example:

    Which supplier has the highest defect rate,
    and what does the Supplier Quality Procedure
    require for that level?

The orchestration layer can request:

    analyze_manufacturing_data
              +
    search_knowledge_base

The Data Agent provides the quantitative evidence.

The RAG Engine provides the relevant company procedure.

The LLM then synthesizes both results into a single contextual response.

---

## Multilingual Interaction

Maranello AI supports conversations in:

- Italian;
- English.

The user does not need to manually select a language.

The system identifies the language of the request and responds accordingly.

The RAG architecture also supports **cross-language semantic retrieval**.

The Knowledge Base is written in English, but an Italian query can retrieve the relevant English documentation and produce a final answer in Italian.

Example:

    Italian Question
          ↓
    Semantic Retrieval
          ↓
    English Knowledge Base
          ↓
    LLM Synthesis
          ↓
    Italian Answer

---

## Conversation Memory

The Backend maintains conversational state through a session-based Conversation Manager.

Each conversation is associated with a:

    sessionId

The Backend also maintains the previous OpenAI response reference and uses:

    previous_response_id

to preserve context across subsequent interactions.

This enables multi-turn conversations such as:

    User:
    Which supplier has the highest defect rate?

    Assistant:
    SUP-07 ...

    User:
    What does the policy say about that supplier?

The second request can be interpreted using the context established by the first interaction.

---

## Native Chart Rendering

Analytical requests can produce charts generated by the Python Data Agent using **Matplotlib**.

Charts follow a controlled application flow:

    Python Data Agent
          ↓
    Generated PNG
          ↓
    Node.js Chart Proxy
          ↓
    React Frontend
          ↓
    Native Chat Rendering

The browser does not communicate directly with the Python service.

The Node.js Backend exposes generated charts through:

    GET /api/charts/:filename

The Chart Proxy validates requested filenames and prevents arbitrary path traversal.

Generated chart files are managed by a dedicated `ChartCleanupService` in the Python Data Agent.

The default lifecycle configuration is:

    chart_retention_hours = 24.0
    chart_cleanup_interval_minutes = 60.0

The Data Agent performs:

    Application startup
            ↓
    Immediate cleanup
            ↓
    Periodic cleanup every 60 minutes
            ↓
    Graceful task cancellation on shutdown

Only application-managed chart files matching:

    monthly_defect_rate_*.png

are eligible for automatic deletion.

Files older than the configured retention period are removed, while unrelated files in the chart directory are left untouched.

This prevents generated PNG files from accumulating indefinitely during repeated analytical usage while keeping cleanup behavior scoped to files owned by the application.

The retention duration and cleanup interval can be configured through the Data Agent settings when a different runtime policy is required.

---

## Controlled Failure Handling

The application handles unavailable internal dependencies through controlled error boundaries.

Examples include:

- Python Data Agent unavailable;
- ChromaDB unavailable;
- invalid client requests;
- failures during tool execution.

When the Data Agent or Knowledge Base required by a request is unavailable, the Backend returns a controlled service error rather than allowing the LLM to fabricate the missing information.

This preserves the distinction between:

    Available Evidence
          ↓
    Supported Answer

and:

    Missing Dependency
          ↓
    Controlled Failure

rather than:

    Missing Dependency
          ↓
    Hallucinated Answer

---

# System Architecture

Maranello AI follows a distributed architecture in which each component has a clearly defined responsibility.

The final system consists of four main runtime services:

    React Frontend
    Node.js Backend
    ChromaDB
    Python Data Agent

The OpenAI API provides the external Large Language Model and embedding capabilities used by the application.

The high-level architecture is:

    ┌─────────────────────────────────────────────────────────────┐
    │                         User                                │
    └────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    React Frontend                           │
    │                                                             │
    │  Conversational UI                                         │
    │  Message State                                             │
    │  Loading / Error Handling                                  │
    │  Native Chart Rendering                                    │
    └────────────────────────────┬────────────────────────────────┘
                                 │
                                 │ HTTP
                                 ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                  Node.js Backend                            │
    │                                                             │
    │  REST API                                                   │
    │  Conversation Manager                                      │
    │  AI Orchestration                                          │
    │  Tool Execution                                            │
    │  RAG Connector                                             │
    │  Python Data Agent Connector                               │
    │  Chart Proxy                                               │
    │  Error Handling                                            │
    └───────────────┬──────────────────────┬──────────────────────┘
                    │                      │
                    │                      │
                    ▼                      ▼
    ┌──────────────────────────┐   ┌──────────────────────────────┐
    │      OpenAI API          │   │     Internal Services        │
    │                          │   │                              │
    │  Responses API           │   │   ChromaDB                  │
    │  Function Calling        │   │   Python Data Agent         │
    │  Embeddings              │   │                              │
    └──────────────────────────┘   └──────────────┬───────────────┘
                                                  │
                                    ┌─────────────┴─────────────┐
                                    │                           │
                                    ▼                           ▼
                          ┌───────────────────┐       ┌──────────────────────┐
                          │  Knowledge Base   │       │ Manufacturing       │
                          │                   │       │ Dataset             │
                          │  5 documents      │       │                     │
                          │  149 chunks       │       │ 2,000 rows         │
                          └───────────────────┘       │ 20 columns          │
                                                    └──────────────────────┘

The architecture intentionally prevents the browser and the LLM from directly accessing internal data sources.

The **Node.js Backend acts as the application boundary** between the conversational interface, the AI provider and the internal enterprise capabilities.

---

# Component Responsibilities

## React Frontend

The React application is responsible exclusively for the user-facing conversational experience.

Its main responsibilities are:

- capturing user messages;
- maintaining the visible conversation state;
- sending requests to the Backend;
- preserving the current `sessionId`;
- displaying assistant responses;
- showing loading and typing states;
- displaying controlled error messages;
- rendering analytical charts directly inside the conversation.

The Frontend does not contain RAG, AI routing or manufacturing analysis logic.

It communicates with the Node.js Backend as its application gateway.

---

## Node.js Backend

The Node.js Backend is the central application and orchestration layer.

It is responsible for:

- exposing REST endpoints;
- validating incoming requests;
- managing conversational sessions;
- interacting with the OpenAI Responses API;
- exposing tools to the Large Language Model;
- executing function calls requested by the model;
- communicating with ChromaDB;
- communicating with the Python Data Agent;
- returning tool outputs to the model;
- managing multi-round tool execution;
- synthesizing the final application response;
- tracking the tools used during each interaction;
- proxying generated charts;
- handling dependency failures.

The Backend is implemented using:

    Node.js
    Express
    TypeScript

---

## AI Orchestration Layer

AI orchestration is implemented using the **OpenAI Responses API and native function calling**.

The model receives the user request together with the available tool definitions.

It can then:

- respond directly;
- call the Knowledge Base tool;
- call the Manufacturing Data tool;
- call multiple tools;
- continue through additional tool-execution rounds when required.

The two primary application tools are:

    search_knowledge_base

    analyze_manufacturing_data

The LLM selects the required capabilities, but it does not execute them directly.

Every function call is intercepted and executed by the Node.js Backend.

---

## RAG Layer

The Retrieval-Augmented Generation layer provides access to fictional enterprise knowledge.

Its responsibilities include:

- generating semantic query embeddings;
- searching the configured ChromaDB collection;
- retrieving candidate document chunks;
- filtering candidates by semantic relevance;
- preserving source metadata;
- returning grounded enterprise context to the orchestration layer.

The RAG implementation uses:

    ChromaDB
    OpenAI text-embedding-3-small

The retriever does not automatically treat every returned nearest-neighbor candidate as relevant.

Candidate chunks are filtered using the configured maximum semantic distance:

    maxDistance = 0.70

A candidate is accepted only when it contains a valid finite distance and that distance is less than or equal to the configured threshold.

Candidates with:

- a distance greater than `0.70`;
- a missing distance;
- or an invalid distance

are excluded from the grounded context.

As a result, retrieval can legitimately return zero chunks when the Knowledge Base does not contain sufficiently relevant evidence. This is preferable to injecting weakly related policy text into the orchestration context.

The `0.70` threshold was selected through empirical validation against the current Knowledge Base and embedding model. Validation included relevant English and Italian queries, borderline manufacturing questions and clearly unrelated requests.

The threshold is therefore a project-specific calibration rather than a universal semantic-search constant. It should be re-evaluated if the Knowledge Base, chunking strategy or embedding model changes.

The Knowledge Base is stored locally and indexed before the application is used.

---

## Python Data Agent

The Python Data Agent is an independent FastAPI microservice responsible for structured manufacturing analysis.

Its responsibilities include:

- loading and preparing the Manufacturing Dataset;
- cleaning known data-quality issues;
- caching the prepared dataset for repeated analytical requests;
- interpreting supported analytical requests;
- calculating manufacturing KPIs;
- executing grouped analyses;
- calculating monthly trends;
- generating analytical summaries;
- generating PNG charts using Matplotlib;
- exposing generated charts to the Backend.

The service uses:

    Python
    FastAPI
    Pandas
    Matplotlib

Dataset access is managed through a dedicated `DatasetRepository`.

The repository uses lazy per-process caching:

    First analytical request
              ↓
    Load CSV from disk
              ↓
    Apply deterministic cleaning
              ↓
    Cache prepared DataFrame
              ↓
    Reuse for subsequent requests

This avoids repeating CSV loading and data-cleaning work for every `POST /api/analysis` request.

The prepared dataset is loaded only when first required by an analysis. Subsequent analyses reuse the cached prepared DataFrame for the lifetime of the Data Agent process.

An explicit `reload()` operation is available when the underlying dataset must be refreshed. Reloading rebuilds the prepared dataset, while a failed reload preserves the previously valid cached dataset instead of replacing it with an invalid state.

The repository also protects the cached source DataFrame from accidental mutation by analytical consumers.

This design is appropriate for the current synthetic dataset and Pandas-based analytical scope while removing unnecessary repeated disk I/O and cleaning overhead.

The Data Agent does not depend on the LLM to calculate numerical results.

---

## ChromaDB

ChromaDB acts as the local vector database for the enterprise Knowledge Base.

It stores the embedded chunks produced from the fictional manufacturing documentation and supports semantic retrieval during RAG interactions.

The application uses a dedicated collection configured through:

    CHROMA_COLLECTION

The final indexed Knowledge Base contains:

    5 source documents
    149 chunks

---

# Request Lifecycle

A standard conversational request follows this flow:

    1. User enters a question in the React interface.

    2. Frontend sends the request to:

       POST /api/chat

    3. Backend validates the request.

    4. Conversation Manager resolves or creates the session.

    5. Backend sends the request and available tool definitions
       to the OpenAI Responses API.

    6. The model determines whether a tool is required.

    7. If no tool is required:

       the model returns a direct response.

    8. If a tool is required:

       the Backend executes the requested function.

    9. Tool output is returned to the Responses API.

    10. The model can:

        - produce the final answer;
        - request another tool;
        - request additional tool execution.

    11. The Backend continues until a final response is produced
        or the configured tool-round limit is reached.

    12. The final response is returned to the React Frontend.

This creates a controlled orchestration loop:

    User
      ↓
    React
      ↓
    Node.js Backend
      ↓
    OpenAI Responses API
      ↓
    ┌───────────────────────────┐
    │     Function Call?        │
    └─────────────┬─────────────┘
             No   │   Yes
           ┌──────┘    └──────┐
           │                  │
           ▼                  ▼
    Direct Response       Execute Tool
                              │
                              ▼
                         Tool Output
                              │
                              ▼
                    OpenAI Responses API
                              │
                              └───────┐
                                      │
                              Additional Tool?
                                      │
                           ┌──────────┴──────────┐
                           │                     │
                          Yes                    No
                           │                     │
                           └─── Tool Loop        ▼
                                           Final Response
                                                │
                                                ▼
                                             React

---

# Hybrid Request Flow

A Hybrid request requires both structured manufacturing evidence and enterprise knowledge.

Example:

    Which supplier has the highest defect rate,
    and how is that result classified according
    to the Supplier Quality Procedure?

The orchestration flow can become:

    User Question
          ↓
    Node.js Backend
          ↓
    OpenAI Responses API
          ↓
    ┌───────────────────────────────┐
    │        Tool Selection         │
    └───────────────┬───────────────┘
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    analyze_manufacturing_   search_knowledge_
    data                     base
          │                   │
          ▼                   ▼
    Python Data Agent        ChromaDB
          │                   │
          ▼                   ▼
    Quantitative Result      Policy Context
          │                   │
          └─────────┬─────────┘
                    ▼
            LLM Final Synthesis
                    ↓
             Contextual Answer

This architecture allows the model to reason over evidence produced by different specialized systems without giving the model direct access to the underlying data sources.

---

# Conversation Lifecycle

Conversation continuity is managed at two levels.

## Application Session

The Backend maintains an in-memory conversation session identified by:

    sessionId

The `sessionId` is returned to the Frontend and reused for subsequent messages.

## OpenAI Response Continuity

The Backend also stores the latest OpenAI response identifier as:

    lastResponseId

When the conversation continues, this value is sent to the Responses API as:

    previous_response_id

The resulting flow is:

    First Request
         ↓
    New sessionId
         ↓
    OpenAI Response
         ↓
    lastResponseId stored
         ↓
    Second Request
         ↓
    Existing sessionId
         +
    previous_response_id
         ↓
    Contextual Response

Conversation state is intentionally maintained in memory in the current project scope.

Persistent distributed conversation storage is considered a future production enhancement.

---

# Technology Stack

The project uses different technologies according to the responsibility of each architectural layer.

| Layer | Technology | Responsibility |
|-------|------------|----------------|
| Frontend | React | Conversational web interface |
| Frontend Language | TypeScript | Typed client implementation |
| Frontend Tooling | Vite | Development and production build |
| Backend | Node.js | Application runtime |
| Backend Framework | Express | REST API and middleware |
| Backend Language | TypeScript | Typed orchestration implementation |
| AI Provider | OpenAI | LLM and embedding services |
| AI API | Responses API | Conversation and tool orchestration |
| Tool Integration | Native Function Calling | Autonomous tool selection |
| Vector Database | ChromaDB | Semantic Knowledge Base retrieval |
| Embeddings | `text-embedding-3-small` | Semantic representation |
| Data Agent | Python | Analytical runtime |
| Data API | FastAPI | Data Agent microservice |
| Data Processing | Pandas | Dataset cleaning and analysis |
| Visualization | Matplotlib | Server-side chart generation |
| Structured Dataset | CSV | Manufacturing batch data |
| Knowledge Base | Markdown | Fictional enterprise documentation |
| Backend Testing | Vitest | Automated Backend test suite |
| Version Control | Git / GitHub | Source control and project history |

The architecture deliberately avoids introducing additional orchestration frameworks where native platform capabilities are sufficient.

In particular, the final implementation does not require LangGraph or LangChain.js for the central tool-routing workflow.

---

# Repository Structure

The repository separates the application services, enterprise knowledge, structured data and technical documentation.

The high-level structure is:

    maranello-ai/
    │
    ├── frontend/
    │   ├── public/
    │   └── src/
    │       └── React conversational application
    │
    ├── backend/
    │   ├── src/
    │   │   ├── rag/
    │   │   │   ├── ingestionService.ts
    │   │   │   ├── ingest.ts
    │   │   │   ├── knowledgeLoader.ts
    │   │   │   ├── retrieverService.ts
    │   │   │   ├── textChunker.ts
    │   │   │   └── types.ts
    │   │   └── services/
    │   │       └── chromaClient.ts
    │   └── tests/
    │       └── Backend unit and integration tests
    │
    ├── data_agent/
    │   ├── app/
    │   │   ├── api/
    │   │   ├── core/
    │   │   ├── models/
    │   │   ├── services/
    │   │   └── main.py
    │   ├── generated_charts/
    │   ├── tests/
    │   └── pyproject.toml
    │
    ├── knowledge_base/
    │   ├── README.md
    │   ├── manufacturing_quality_policy.md
    │   ├── non_conformity_procedure.md
    │   ├── supplier_quality_procedure.md
    │   ├── rework_and_scrap_procedure.md
    │   └── production_escalation_policy.md
    │
    ├── data/
    │   └── vector_store/
    │
    ├── docs/
    │   ├── README.md
    │   ├── en/
    │   └── it/
    │       ├── 01_Project_Vision_and_Scope.md
    │       ├── 02_Software_Requirements_Specification.md
    │       ├── 03_System_Architecture.md
    │       ├── 04_Data_Model.md
    │       ├── 05_API_Specification.md
    │       └── 06_Test_Plan.md
    │
    ├── .env.example
    ├── .gitignore
    └── README.md

Backend tests are colocated with the Node.js service under:

    backend/tests/

Python Data Agent tests are colocated with the analytical service under:

    data_agent/tests/

The repository does not use a separate root-level test suite for the final architecture.

The Knowledge Base ingestion entry point is:

    backend/src/rag/ingest.ts

and is exposed through the Backend package script:

    npm run rag:ingest

The exact internal structure of each service follows its own modular organization.

For detailed architectural information, see:

    docs/it/03_System_Architecture.md

For data structures and dataset details, see:

    docs/it/04_Data_Model.md

For API contracts, see:

    docs/it/05_API_Specification.md

For testing strategy and evidence, see:

    docs/it/06_Test_Plan.md

---

# Prerequisites

Before running Maranello AI locally, install the following software:

- Git
- Node.js 22 or later
- npm
- Python 3.12 or later
- pip

An active OpenAI API key is also required for:

- LLM orchestration;
- native function calling;
- Knowledge Base embeddings;
- semantic retrieval.

The Node.js Backend explicitly requires:

    Node.js >= 22

through its `package.json` engine configuration.

The Python Data Agent explicitly requires:

    Python >= 3.12

through:

    data_agent/pyproject.toml

Before creating the Python virtual environment, verify the interpreter version:

    python3 --version

The reported version must be Python 3.12 or later.

On systems where `python3` points to an older interpreter, use an explicitly versioned executable such as:

    python3.12 --version

and use that same executable when creating the virtual environment.

ChromaDB is installed later inside the project Python virtual environment. A separate global ChromaDB installation is not required.

The final project was validated using:

    Node.js 24.15.0
    npm 11.12.1
    Python 3.12.13
    ChromaDB CLI 1.4.4

Using compatible versions that satisfy the declared requirements is recommended.

---

# Clone the Repository

Clone the repository and enter the project root:

    git clone https://github.com/marcosaccani1/maranello-ai.git
    cd maranello-ai

All commands in the following sections assume that the current directory is the repository root unless explicitly stated otherwise.

---

# Environment Configuration

Maranello AI uses environment variables for runtime configuration and sensitive credentials.

The repository provides:

    .env.example

Create the local environment file:

    cp .env.example .env

The root `.env` file configures the Node.js Backend and its external service integrations.

The React Frontend uses a default local Backend URL and therefore does not require a separate environment file for the standard local setup.

An optional Frontend environment template is provided at:

    frontend/.env.example

To override the default Frontend API URL, create:

    cp frontend/.env.example frontend/.env

The supported Frontend variable is:

    VITE_API_URL=http://127.0.0.1:3000

Then configure the required values inside:

    .env

A valid OpenAI API key is required:

    OPENAI_API_KEY=<your-openai-api-key>

`OPENAI_API_KEY` is a required Backend configuration value.

The Backend validates it during configuration loading and fails fast when the variable is missing, empty, or contains only whitespace. This prevents the application from starting with an incomplete AI provider configuration that would otherwise fail only when processing a user request.

The Backend supports the following environment variables:

    NODE_ENV
    PORT
    DATA_AGENT_URL
    CHROMA_URL
    CHROMA_COLLECTION
    OPENAI_API_KEY
    OPENAI_EMBEDDING_MODEL
    LLM_MODEL
    LLM_TEMPERATURE
    LLM_TIMEOUT_SECONDS
    CHAT_RATE_LIMIT_WINDOW_MINUTES
    CHAT_RATE_LIMIT_MAX_REQUESTS

The validated local configuration and defaults are:

    NODE_ENV=development
    PORT=3000
    DATA_AGENT_URL=http://127.0.0.1:8001
    CHROMA_URL=http://127.0.0.1:8000
    CHROMA_COLLECTION=maranello_ai_knowledge_base
    OPENAI_EMBEDDING_MODEL=text-embedding-3-small
    LLM_MODEL=gpt-5-mini
    LLM_TEMPERATURE=0.0
    LLM_TIMEOUT_SECONDS=30
    CHAT_RATE_LIMIT_WINDOW_MINUTES=15
    CHAT_RATE_LIMIT_MAX_REQUESTS=30

The Chat API rate-limit defaults therefore allow up to 30 requests within a 15-minute window.

The Python Data Agent also defines runtime settings for generated-chart lifecycle management:

    chart_retention_hours=24.0
    chart_cleanup_interval_minutes=60.0

These settings control how long managed chart PNG files are retained and how frequently the background cleanup task runs.

They are Data Agent settings rather than Node.js Backend variables. The current defaults are sufficient for the standard local setup, so no additional Data Agent environment configuration is required to run the project with the validated defaults.

The real `.env` file must remain local and must never be committed to Git.

---

# Local Service Ports

The validated local architecture uses:

| Service | Address |
|---------|---------|
| React Frontend | `http://localhost:5173` |
| Node.js Backend | `http://127.0.0.1:3000` |
| ChromaDB | `http://127.0.0.1:8000` |
| Python Data Agent | `http://127.0.0.1:8001` |

The React Frontend communicates with the Node.js Backend.

The Node.js Backend communicates internally with:

- OpenAI;
- ChromaDB;
- the Python Data Agent.

The browser does not require direct access to ChromaDB or the Python Data Agent.

---

# Install Dependencies

The Frontend, Backend and Python Data Agent use independent dependency environments.

---

## Backend Dependencies

From the repository root:

    cd backend
    npm install
    cd ..

The Backend dependency manifest is:

    backend/package.json

The Backend requires:

    Node.js >= 22

The same package also provides the Knowledge Base ingestion command:

    npm run rag:ingest

which will be used after ChromaDB has been started.

---

## Frontend Dependencies

From the repository root:

    cd frontend
    npm install
    cd ..

The Frontend dependency manifest is:

    frontend/package.json

---

## Python Data Agent Environment

The analytical microservice is located in:

    data_agent/

Its package configuration and dependencies are defined in:

    data_agent/pyproject.toml

The Data Agent requires:

    Python >= 3.12

Before creating the virtual environment, verify the Python interpreter:

    python3 --version

If the reported version is Python 3.12 or later, create the virtual environment from the repository root with:

    python3 -m venv .venv

If `python3` points to an older interpreter but Python 3.12 is installed, use the versioned executable instead:

    python3.12 --version
    python3.12 -m venv .venv

Activate the environment on macOS or Linux:

    source .venv/bin/activate

On Windows PowerShell:

    .venv\Scripts\Activate.ps1

Verify that the active environment uses a supported interpreter:

    python --version

The reported version must be Python 3.12 or later.

Upgrade pip:

    python -m pip install --upgrade pip

Install the Data Agent together with its development and testing dependencies:

    python -m pip install -e "./data_agent[dev]"

Install the ChromaDB CLI in the same virtual environment:

    python -m pip install chromadb

Verify that the ChromaDB CLI is available:

    chroma --version

This setup keeps the Python Data Agent and ChromaDB CLI isolated inside the project virtual environment.

The Data Agent installation command uses the actual `pyproject.toml` configuration. No separate `requirements.txt` is required.

Runtime dependencies include:

- FastAPI;
- Uvicorn;
- Pandas;
- Matplotlib;
- Pydantic;
- Pydantic Settings.

Development dependencies include:

- pytest;
- pytest-cov;
- Ruff;
- HTTPX.

---

# Installation Verification

The application components can be verified independently before startup.

## Backend

Enter:

    cd backend

Run:

    npm run typecheck
    npm run lint
    npm test
    npm run build

The validated project state passes all four checks.

The final Backend automated test suite contains:

    18 test files
    120 tests

Return to the repository root:

    cd ..

---

## Frontend

Enter:

    cd frontend

Run:

    npm run lint
    npm run build

Both checks pass in the validated project state.

Return to the repository root:

    cd ..

---

## Python Data Agent

With the Python virtual environment activated, run from the repository root:

    python -m pytest data_agent/tests
    ruff check data_agent

The Python project uses Ruff for static linting and code-quality verification.

Its linting and formatting configuration is defined in:

    data_agent/pyproject.toml

Both the automated test suite and Ruff checks pass in the validated project state.

---

# Installation Complete

After completing the previous steps, the local environment contains:

    Backend dependencies
            +
    Frontend dependencies
            +
    Python Data Agent
            +
    Development dependencies
            +
    Environment configuration

The application services can now be started independently.

The recommended runtime sequence is:

    ChromaDB
        ↓
    Knowledge Base Ingestion
        ↓
    Python Data Agent
        ↓
    Node.js Backend
        ↓
    React Frontend

The following section describes this startup procedure.

---

# Starting the Application

Maranello AI requires multiple processes to run simultaneously.

For local development, use separate terminal windows or terminal tabs.

The recommended startup order is:

    1. Activate Python environment
    2. Start ChromaDB
    3. Ensure the Knowledge Base is indexed
    4. Start Python Data Agent
    5. Start Node.js Backend
    6. Start React Frontend

Starting the infrastructure dependencies first makes service availability easier to verify before launching the user-facing application.

---

# Start ChromaDB

Activate the Python virtual environment if it is not already active.

On macOS or Linux:

    source .venv/bin/activate

On Windows PowerShell:

    .venv\Scripts\Activate.ps1

If ChromaDB has not yet been installed in the virtual environment, install it with:

    python -m pip install chromadb

Verify that the CLI is available:

    chroma --version

From the repository root, start the local ChromaDB server:

    chroma run --path ./data/vector_store --host 127.0.0.1 --port 8000

ChromaDB should become available at:

    http://127.0.0.1:8000

Keep this process running.

The Node.js Backend uses the configured value:

    CHROMA_URL=http://127.0.0.1:8000

to communicate with the vector database.

---

# Knowledge Base Indexing

Before RAG queries can be executed, the enterprise Knowledge Base must be indexed into ChromaDB.

The source documents are located in:

    knowledge_base/

The final Knowledge Base contains:

    manufacturing_quality_policy.md
    non_conformity_procedure.md
    supplier_quality_procedure.md
    rework_and_scrap_procedure.md
    production_escalation_policy.md

During indexing, the documents are:

    loaded
      ↓
    divided into chunks
      ↓
    converted into embeddings
      ↓
    stored in ChromaDB
      ↓
    enriched with source metadata

Embeddings are generated using:

    text-embedding-3-small

Before running the ingestion process, make sure that:

- ChromaDB is running on the configured `CHROMA_URL`;
- the root `.env` file is configured;
- `OPENAI_API_KEY` contains a valid API key.

From the repository root, enter the Backend directory:

    cd backend

Run the Knowledge Base ingestion command:

    npm run rag:ingest

The command executes the ingestion entry point:

    backend/src/rag/ingest.ts

which uses the existing RAG ingestion pipeline:

    Knowledge Base
          ↓
    KnowledgeLoader
          ↓
    TextChunker
          ↓
    OpenAI Embeddings
          ↓
    ChromaDB

The final validated ingestion result is:

    Documents loaded: 5
    Chunks indexed: 149
    ChromaDB collection: maranello_ai_knowledge_base

A successful execution produces output equivalent to:

    Starting Maranello AI Knowledge Base ingestion...
    Knowledge Base ingestion completed successfully.
    Documents loaded: 5
    Chunks indexed: 149
    ChromaDB collection: maranello_ai_knowledge_base

The ingestion pipeline uses an upsert operation when storing chunks in ChromaDB.

This allows the ingestion command to be executed again when the Knowledge Base must be rebuilt or updated without intentionally creating duplicate chunk identifiers.

Once indexing has completed successfully, the Knowledge Base does not need to be re-indexed before every application start unless:

- the vector store has been removed;
- the Knowledge Base documents have changed;
- the collection has been recreated;
- the embedding configuration has changed.

Return to the repository root when required:

    cd ..

---

# Start the Python Data Agent

Open a new terminal from the repository root.

Activate the Python virtual environment if it is not already active.

On macOS or Linux:

    source .venv/bin/activate

On Windows PowerShell:

    .venv\Scripts\Activate.ps1

Enter the Data Agent directory:

    cd data_agent

Start the FastAPI application using Uvicorn:

    uvicorn app.main:app --host 127.0.0.1 --port 8001

The service should become available at:

    http://127.0.0.1:8001

Keep this process running.

The Data Agent exposes a health endpoint at:

    GET /health

It can be verified from another terminal using:

    curl http://127.0.0.1:8001/health

A healthy service returns an HTTP 200 response and identifies the Maranello AI Data Agent as available.

The analytical API used internally by the Node.js Backend is exposed under:

    POST /api/analysis

Generated analytical charts are served internally under:

    /charts

The Node.js Backend reaches the Data Agent using:

    DATA_AGENT_URL=http://127.0.0.1:8001

The React Frontend does not communicate directly with this service.

---

# Start the Node.js Backend

Open another terminal.

From the repository root:

    cd backend

Start the Backend using the development script defined in `package.json`.

The expected development command is:

    npm run dev

The Backend should become available at:

    http://127.0.0.1:3000

The Backend health endpoint can then be used to verify the service.

The Backend requires access to:

    OpenAI API
    ChromaDB
    Python Data Agent

for the complete Hybrid AI functionality.

The service itself can remain operational when some internal dependencies are unavailable, allowing controlled dependency failures to be returned to the client.

---

# Start the React Frontend

Open another terminal.

From the repository root:

    cd frontend

Start the Vite development server:

    npm run dev

The application should become available at:

    http://127.0.0.1:5173

Open this address in a browser.

The user should now see the Maranello AI conversational interface.

---

# Local Runtime Checklist

A complete local environment should have the following services running:

    [ ] ChromaDB
        http://127.0.0.1:8000

    [ ] Python Data Agent
        http://127.0.0.1:8001

    [ ] Node.js Backend
        http://127.0.0.1:3000

    [ ] React Frontend
        http://127.0.0.1:5173

In addition:

    [ ] OPENAI_API_KEY is configured

    [ ] Knowledge Base is indexed

    [ ] Manufacturing Dataset is available

    [ ] Browser can reach the React application

---

# Verify the Services

Before testing the complete conversational workflow, verify the individual services.

## ChromaDB

Confirm that the ChromaDB process is running on:

    127.0.0.1:8000

## Python Data Agent

Verify:

    GET http://127.0.0.1:8001/health

Expected result:

    HTTP 200

## Node.js Backend

Verify the Backend health endpoint documented by the service.

Expected result:

    HTTP 200

## React Frontend

Open:

    http://127.0.0.1:5173

The conversational interface should load successfully.

---

# First End-to-End Verification

Once all services are running, the system can be verified through the React interface.

A useful first RAG request is:

    What is the critical defect-rate threshold
    according to the Manufacturing Quality Policy?

Expected behavior:

    React
      ↓
    Node.js Backend
      ↓
    search_knowledge_base
      ↓
    ChromaDB
      ↓
    Policy Context
      ↓
    Final Answer

A useful first analytical request is:

    Which supplier has the highest defect rate?

Expected behavior:

    React
      ↓
    Node.js Backend
      ↓
    analyze_manufacturing_data
      ↓
    Python Data Agent
      ↓
    Manufacturing Dataset
      ↓
    Final Answer

A useful Hybrid request is:

    Which supplier has the highest defect rate,
    and how should that result be classified
    according to the Supplier Quality Procedure?

Expected behavior:

    Data Analysis
          +
    Knowledge Retrieval
          ↓
    Final Contextual Answer

These three requests provide a quick verification of the three primary tool-enabled execution patterns:

    RAG
    Data Analysis
    Hybrid

---

# API Overview

The React Frontend is the primary user interface, but the Node.js Backend exposes REST endpoints that define the main application boundary.

The complete API contracts are documented in:

    docs/it/05_API_Specification.md

The following endpoints are the most relevant when running or testing the application.

---

## Chat API

The main conversational endpoint is:

    POST /api/chat

A request contains the user message and, when continuing an existing conversation, the current session identifier.

Example request:

    {
      "message": "Which supplier has the highest defect rate?",
      "sessionId": "optional-session-id"
    }

For a new conversation, `sessionId` can be omitted.

The Backend creates a new session and returns its identifier.

A successful response contains:

    {
      "sessionId": "generated-session-id",
      "answer": "assistant response",
      "toolsUsed": [
        "analyze_manufacturing_data"
      ]
    }

When an analytical request generates a chart, the response can also include:

    {
      "chartUrl": "/api/charts/example.png"
    }

The Frontend stores the returned `sessionId` and reuses it for subsequent messages in the same conversation.

---

## Chat Request Validation

The Backend validates the incoming message before starting AI orchestration.

Requests containing:

- a missing message;
- an empty message;
- whitespace-only content;

are rejected with:

    HTTP 400

The React Frontend also prevents empty messages from being submitted, but Backend validation remains authoritative for the API contract.

---

## Backend Health Check

The Node.js Backend exposes a health endpoint that can be used to verify that the application service is running.

The health check confirms the availability of the Backend process itself.

It does not necessarily guarantee that every external or internal dependency is currently available.

This distinction is important because Maranello AI is designed to keep the Backend operational even when a specialized dependency temporarily fails.

---

## Data Agent API

The Python Data Agent exposes its analytical endpoint at:

    POST /api/analysis

This endpoint is used internally by the Node.js Backend.

The React Frontend does not call it directly.

The service receives an analytical question and returns a structured result generated from the Manufacturing Dataset.

The Data Agent also exposes:

    GET /health

for service availability checks.

---

## Chart Endpoints

Generated analytical charts pass through two application boundaries.

The Python Data Agent internally exposes generated images through:

    /charts/:filename

The Node.js Backend exposes them to the Frontend through:

    GET /api/charts/:filename

The complete flow is:

    Python Data Agent
          ↓
    /charts/:filename
          ↓
    Node.js Backend
          ↓
    /api/charts/:filename
          ↓
    React Frontend

The Backend validates the requested filename before retrieving the chart from the Python service.

This prevents the browser from directly accessing the Data Agent and protects the chart-serving boundary against arbitrary path traversal.

---

# Example Use Cases

Maranello AI supports multiple interaction patterns through the same conversational interface.

The user does not manually select a mode.

The examples below illustrate the main behaviors implemented by the system.

---

## 1. Knowledge Base Question — RAG

Example:

    What is the critical defect-rate threshold
    according to the Manufacturing Quality Policy?

Expected orchestration:

    User Question
          ↓
    OpenAI Responses API
          ↓
    search_knowledge_base
          ↓
    ChromaDB
          ↓
    Manufacturing Quality Policy
          ↓
    LLM Synthesis
          ↓
    Answer + Source

According to the fictional Manufacturing Quality Policy used by the project, the defect-rate classification is:

| Defect Rate | Classification |
|-------------|----------------|
| `<= 2.0%` | Normal |
| `> 2.0% and <= 3.5%` | Warning |
| `> 3.5%` | Critical |

The important architectural characteristic is that these thresholds are retrieved from the Knowledge Base rather than generated from the model's general knowledge.

---

## 2. Global Manufacturing KPI — Data Analysis

Example:

    What is the overall defect rate?

Expected orchestration:

    User Question
          ↓
    analyze_manufacturing_data
          ↓
    Python Data Agent
          ↓
    Pandas
          ↓
    Manufacturing Dataset
          ↓
    KPI Result
          ↓
    Final Answer

The validated project dataset produces the following global KPIs:

| KPI | Value |
|-----|------:|
| Total Production | 164,060 |
| Total Defective Units | 3,272 |
| Defect Rate | 1.99% |
| Rework Rate | 0.96% |
| Scrap Rate | 0.51% |
| Average Quality Score | 95.82 |
| Average Downtime | 33.04 minutes |
| Average Cycle Time | 84.74 seconds |

These values are calculated by the Python Data Agent.

The LLM is responsible for presenting and explaining the result, but it is not the source of the numerical values.

---

## 3. Grouped Manufacturing Analysis

Example:

    Which supplier has the highest defect rate?

The Question Interpreter maps the request to the supported analytical dimension:

    supplier_id

The Data Agent calculates defect rates by supplier and sorts the result according to the analytical behavior defined by the service.

In the validated synthetic dataset:

    SUP-07
    defect rate: 2.99%

is the supplier with the highest defect rate.

Other supported grouped dimensions include:

    production_line
    shift
    supplier_id
    component_category
    vehicle_model
    plant
    operator_team

Examples include:

    Which production line has the highest defect rate?

    Compare defect rates by shift.

    Which component category has the highest defect rate?

    Compare quality performance by plant.

---

## 4. Monthly Trend Analysis

Example:

    Show me the monthly trend of the defect rate.

The Data Agent recognizes the request as a supported temporal analysis and aggregates the manufacturing data by month.

The validated dataset covers twelve months.

The observed defect-rate range includes:

    Highest monthly defect rate:
    2.10%

    Lowest monthly defect rate:
    1.78%

The analytical result can also produce a Matplotlib chart.

Expected flow:

    User Question
          ↓
    analyze_manufacturing_data
          ↓
    Monthly Aggregation
          ↓
    Matplotlib
          ↓
    PNG Chart
          ↓
    Chart Proxy
          ↓
    React Conversation

---

## 5. Hybrid Analysis

Hybrid requests are one of the central capabilities of Maranello AI.

Example:

    Which supplier has the highest defect rate,
    and how should that result be classified
    according to the Supplier Quality Procedure?

This request requires two independent sources of truth.

The quantitative part requires:

    analyze_manufacturing_data

The policy part requires:

    search_knowledge_base

The validated analytical result identifies:

    SUP-07
    defect rate: 2.99%

The fictional Supplier Quality Procedure defines:

| Supplier Defect Rate | Classification |
|----------------------|----------------|
| `> 2.0% and <= 3.0%` | Observation |
| `> 3.0% and <= 4.0%` | Warning |
| `> 4.0%` | Critical |

Therefore, a supplier defect rate of:

    2.99%

falls within the:

    Observation

classification according to the Supplier Quality Procedure.

The final answer can therefore combine:

    Data Agent
    "SUP-07 has the highest defect rate at 2.99%."

                +

    Knowledge Base
    "A supplier defect rate above 2.0% and up to 3.0%
    is classified as Observation."

                ↓

    Hybrid Answer

This demonstrates why the system uses separate authoritative sources for quantitative evidence and enterprise policy.

---

## 6. Cross-Language RAG

The enterprise Knowledge Base is written in English, but the user can interact with Maranello AI in Italian.

Example:

    Qual è la soglia critica del defect rate
    secondo la Manufacturing Quality Policy?

Expected flow:

    Italian Query
          ↓
    OpenAI Embedding
          ↓
    ChromaDB Semantic Retrieval
          ↓
    English Knowledge Base
          ↓
    Retrieved Policy Context
          ↓
    LLM Synthesis
          ↓
    Italian Answer

The user does not need to translate the request or manually select a language.

This capability was validated after adopting multilingual semantic embeddings through:

    text-embedding-3-small

---

## 7. Multi-Turn Conversation

Maranello AI maintains conversational context across subsequent requests.

Example first message:

    Which supplier has the highest defect rate?

The system can identify:

    SUP-07

The user can then ask:

    What does the policy say about that supplier?

without repeating the supplier identifier.

The Backend uses the existing:

    sessionId

and the OpenAI Responses API continuity mechanism through:

    previous_response_id

to preserve the conversational context.

Expected conceptual flow:

    Message 1
    "Which supplier has the highest defect rate?"
          ↓
    SUP-07 identified
          ↓
    Conversation State
          ↓
    Message 2
    "What does the policy say about that supplier?"
          ↓
    "that supplier" → SUP-07
          ↓
    Knowledge Base Retrieval
          ↓
    Contextual Answer

---

## 8. Chart Generation

A supported analytical request can explicitly request a visual representation.

Example:

    Generate a chart showing the monthly defect-rate trend.

The Data Agent:

    1. interprets the request;
    2. calculates the monthly aggregation;
    3. generates the chart with Matplotlib;
    4. saves the result as a unique PNG;
    5. returns the chart reference to the Backend.

The Backend converts the internal reference:

    /charts/example.png

into:

    /api/charts/example.png

The React Frontend then renders the image directly inside the conversation.

No manual file download is required.

---

# Controlled Failure Scenarios

Maranello AI distinguishes between an unavailable source and an answer that can legitimately be generated without that source.

When required evidence is unavailable, the application fails explicitly rather than silently replacing the missing evidence with model-generated information.

---

## Data Agent Unavailable

Consider the request:

    Which supplier has the highest defect rate?

This question requires the Manufacturing Dataset.

If the Python Data Agent is unavailable, the Backend returns a controlled:

    HTTP 503 Service Unavailable

The user receives an error indicating that manufacturing data analysis is temporarily unavailable.

The model is not allowed to invent a supplier or defect rate.

Conceptually:

    Analytical Question
          ↓
    Data Agent Required
          ↓
    Data Agent Unavailable
          ↓
    Controlled 503
          ↓
    No Fabricated KPI

---

## Knowledge Base Unavailable

Consider:

    What is the critical defect-rate threshold
    according to company policy?

This request requires the Knowledge Base.

If ChromaDB is unavailable, the Backend returns a controlled:

    HTTP 503 Service Unavailable

The application does not replace the unavailable internal policy with the model's general knowledge.

Conceptually:

    Policy Question
          ↓
    RAG Required
          ↓
    ChromaDB Unavailable
          ↓
    Controlled 503
          ↓
    No Fabricated Policy

---

## Invalid User Request

Empty and whitespace-only messages are rejected before AI orchestration begins.

Expected result:

    HTTP 400

This validation exists both in the React interface and at the Backend API boundary.

---

# Sources of Truth

Maranello AI intentionally separates generative reasoning from authoritative information.

| Information Type | Source of Truth |
|------------------|-----------------|
| Company policies | Knowledge Base |
| Company procedures | Knowledge Base |
| Manufacturing KPIs | Manufacturing Dataset through Data Agent |
| Defect-rate comparisons | Manufacturing Dataset through Data Agent |
| Monthly trends | Manufacturing Dataset through Data Agent |
| Charts | Python Data Agent |
| Tool selection | Large Language Model |
| Final natural-language synthesis | Large Language Model |

This distinction is a fundamental design principle.

The LLM is responsible for:

- understanding the request;
- selecting tools;
- integrating evidence;
- maintaining conversational reasoning;
- generating the final natural-language response.

The LLM is not considered the authoritative source for:

- fictional internal company policies;
- fictional internal procedures;
- manufacturing KPI values;
- structured analytical results.

---

# Manufacturing Dataset

The structured analytical component uses a synthetic manufacturing dataset created specifically for Maranello AI.

The dataset contains:

    2,000 rows
    20 columns

Each row represents a production batch.

The schema includes:

    batch_id
    production_date
    plant
    production_line
    vehicle_model
    shift
    units_produced
    defective_units
    defect_category
    rework_units
    scrap_units
    downtime_minutes
    cycle_time_seconds
    quality_score
    supplier_id
    component_category
    inspection_status
    temperature_c
    operator_team
    notes

The dataset intentionally contains controlled data-quality issues in order to demonstrate a realistic cleaning workflow.

These include:

- duplicate records;
- missing values;
- mixed date formats;
- inconsistent text values;
- invalid quality scores;
- numerical inconsistencies;
- downtime outliers;
- cycle-time outliers.

The Data Agent applies deterministic cleaning rules before analytical calculations are performed.

The synthetic data also contains meaningful relationships designed to make analytical queries non-trivial.

Examples include differences associated with:

- production lines;
- shifts;
- suppliers;
- component categories;
- downtime behavior.

The dataset is fictional and must not be interpreted as representing the production performance of any real automotive manufacturer.

---

# Enterprise Knowledge Base

The RAG component uses a fictional internal Knowledge Base created specifically for the project.

It contains five operational documents:

    manufacturing_quality_policy.md

    non_conformity_procedure.md

    supplier_quality_procedure.md

    rework_and_scrap_procedure.md

    production_escalation_policy.md

Together, these documents define the fictional operating rules used by Maranello AI when answering company-policy questions.

The Knowledge Base allows the system to distinguish between:

    What happened?
          ↓
    Manufacturing Dataset

and:

    What should happen according to policy?
          ↓
    Knowledge Base

The Hybrid architecture can combine both perspectives when required.

The Knowledge Base is written in English and indexed into ChromaDB as:

    149 chunks

with source metadata preserved for retrieval and final answer attribution.

All policies and procedures are fictional and exist solely for demonstration purposes.

---

# Testing and Quality Assurance

Maranello AI was developed with a strong focus on verification, reproducibility and controlled integration between components.

Testing is performed at multiple levels:

    Static Verification
           +
    Automated Testing
           +
    Integration Verification
           +
    Manual End-to-End QA

The complete testing strategy and detailed evidence are documented in:

    docs/it/06_Test_Plan.md

---

## Backend Automated Testing

The Node.js Backend includes an automated test suite covering the main application and orchestration components.

The final validated Backend test suite contains:

    18 test files
    120 tests

All tests pass in the validated project state.

The test suite covers areas including:

- request validation;
- conversation management;
- AI orchestration and native function calling;
- bounded tool execution through `MAX_TOOL_ROUNDS`;
- tool execution and multi-round token-usage aggregation;
- RAG integration boundaries and semantic-distance filtering;
- acceptance and rejection behavior around the `maxDistance = 0.70` threshold;
- Python Data Agent integration boundaries;
- resilient inter-service HTTP requests;
- request timeouts through `AbortController`;
- retries for transient network failures and HTTP `5xx` responses;
- backoff behavior and non-retry behavior for HTTP `4xx` responses;
- Data Agent client behavior;
- chart client and chart-proxy handling;
- required OpenAI credential validation and fail-fast configuration;
- Chat API rate limiting;
- structured request observability;
- request ID propagation;
- HTTP status, latency, tool-usage and token-usage observability metadata;
- controlled error behavior;
- application services.

The Backend test suite is executed using:

    Vitest

From the Backend directory, the project provides npm scripts for automated verification.

The exact scripts defined in the final `package.json` should be used during clean-clone verification.

The complete Backend quality workflow includes:

    Type Checking
         ↓
    Linting
         ↓
    Automated Tests
         ↓
    Production Build

The final validated implementation successfully passes all four stages.

---

## Frontend Verification

The React Frontend is validated independently from the Backend.

The final quality workflow includes:

    Linting
       ↓
    Production Build

Both checks pass in the validated project state.

The Frontend was also manually verified against the running Backend to confirm:

- message submission;
- empty-input prevention;
- loading state;
- conversation rendering;
- session continuity;
- error rendering;
- native chart rendering.

---

# Manual End-to-End QA

Automated tests are complemented by manual scenarios executed against the complete running system.

These scenarios validate behaviors that depend on multiple runtime components and real AI orchestration.

The final manual QA campaign includes:

    10 scenarios
    10 passed

The scenarios cover the principal system capabilities.

---

## RAG Verification

A policy request was used to confirm that the model correctly invokes:

    search_knowledge_base

and retrieves the relevant company policy from ChromaDB.

Example:

    What is the critical defect-rate threshold
    according to the Manufacturing Quality Policy?

Expected result:

    > 3.5%
    Critical

with the relevant Knowledge Base source identified.

---

## Data Analysis Verification

Analytical requests were used to confirm that the model correctly invokes:

    analyze_manufacturing_data

and that numerical results originate from the Python Data Agent.

Validated examples include:

    overall defect rate

    supplier comparison

    production-line comparison

    monthly defect-rate trend

The validated overall defect rate is:

    1.99%

The validated highest supplier defect rate is:

    SUP-07
    2.99%

---

## Hybrid Verification

Hybrid scenarios verify that both specialized capabilities can contribute to the same answer.

Example:

    Which supplier has the highest defect rate,
    and how is it classified according
    to the Supplier Quality Procedure?

The expected evidence is:

    Data Agent
        ↓
    SUP-07 = 2.99%

        +

    RAG
        ↓
    Supplier Quality Procedure

        ↓

    Observation

This scenario verifies that numerical evidence and policy interpretation remain separated until final synthesis.

---

## Conversation Memory Verification

Multi-turn behavior was manually verified.

Example:

    User:
    Which supplier has the highest defect rate?

    Assistant:
    SUP-07 ...

    User:
    What does the policy say about that supplier?

The second request correctly resolves the contextual reference:

    that supplier

to the supplier identified in the previous interaction.

This validates the combination of:

    sessionId
        +
    Conversation Manager
        +
    previous_response_id

---

## Multilingual Verification

Both Italian and English interactions were manually tested.

The system successfully supports:

    Italian → Italian response

    English → English response

Cross-language RAG was also verified:

    Italian query
        ↓
    English Knowledge Base
        ↓
    Italian answer

---

## Chart Verification

Monthly trend analysis was used to verify the complete chart pipeline:

    User Request
        ↓
    Python Data Agent
        ↓
    Matplotlib
        ↓
    PNG
        ↓
    Node.js Chart Proxy
        ↓
    React Frontend

The generated chart is rendered directly inside the conversation.

---

## Resilience Verification

Dependency failure scenarios were explicitly tested.

### Python Data Agent unavailable

A request requiring manufacturing analysis produces a controlled:

    HTTP 503

instead of fabricated analytical data.

### ChromaDB unavailable

A request requiring company knowledge produces a controlled:

    HTTP 503

instead of fabricated policy information.

After the controlled error, the Node.js Backend remains available for subsequent requests.

---

# Quality Commands

The project uses service-specific quality commands rather than a single repository-wide command.

## Backend

From:

    backend/

the final quality workflow includes:

    npm run typecheck
    npm run lint
    npm test
    npm run build

These commands were successfully executed against the validated project state.

---

## Frontend

From:

    frontend/

the final quality workflow includes:

    npm run lint
    npm run build

These commands were successfully executed against the validated project state.

---

## Python Data Agent

From the repository root, with the Python virtual environment activated, the final quality workflow includes:

    python -m pytest data_agent/tests

    ruff check data_agent

The final validated Data Agent test suite contains:

    80 automated tests

The automated suite covers areas including:

- dataset loading and deterministic cleaning;
- analytical question interpretation;
- manufacturing KPI calculations;
- grouped and monthly analyses;
- chart generation;
- API behavior;
- `DatasetRepository` lazy caching;
- reuse of the prepared dataset across multiple analyses;
- explicit dataset reload behavior;
- preservation of the previously valid cache when a reload fails;
- protection of the cached dataset from accidental analytical mutation;
- `ChartCleanupService` retention behavior;
- cleanup restricted to application-managed `monthly_defect_rate_*.png` files;
- safe behavior when the chart directory is absent;
- FastAPI lifespan cleanup at startup;
- periodic chart cleanup during runtime;
- graceful cleanup-task cancellation during application shutdown.

These commands were successfully executed against the validated project state.

The final validation produced:

    Pytest: 80 passed
    Ruff: All checks passed

The test execution also reported one `StarletteDeprecationWarning` originating from the installed FastAPI/Starlette testing dependency stack. It does not represent a failing project test or an application runtime error.

---

# Security

Maranello AI is an educational and portfolio project rather than a production deployment, but security boundaries were considered throughout the architecture.

---

## Secret Management

Sensitive configuration must not be hardcoded in source code.

The OpenAI API key is provided through:

    OPENAI_API_KEY

inside the local:

    .env

configuration file.

The real `.env` file is excluded from Git.

The repository provides:

    .env.example

with placeholders and non-sensitive configuration values.

Before final delivery, repository hygiene includes verifying that no real API key or other sensitive value is tracked by Git.

The Backend treats `OPENAI_API_KEY` as required configuration.

At startup, the value is trimmed and validated. If the variable is missing, empty or contains only whitespace, configuration loading fails immediately rather than allowing the application to start in a partially configured state.

This fail-fast behavior makes configuration errors explicit before a paid AI request can be attempted.

---

## LLM Isolation

The Large Language Model does not receive direct access to:

- the filesystem;
- the Manufacturing Dataset;
- the Python runtime;
- ChromaDB;
- internal application services.

Instead, it can request execution only through explicitly defined application tools.

The main boundaries are:

    search_knowledge_base

and:

    analyze_manufacturing_data

The Node.js Backend remains responsible for executing these capabilities.

Conceptually:

    LLM
     │
     │ Function Call
     ▼
    Node.js Backend
     │
     ├── Controlled RAG Access
     │
     └── Controlled Data Analysis Access

This prevents the model from becoming an unrestricted execution layer.

---

## Deterministic Python Execution

The Python Data Agent does not execute arbitrary user-provided or LLM-generated Python code.

Instead:

    Natural-Language Question
              ↓
    Deterministic Question Interpreter
              ↓
    Supported Analytical Operation
              ↓
    Pandas Analysis

Unsupported combinations are rejected or handled through controlled behavior.

This reduces the execution surface of the analytical service.

---

## Frontend Isolation

The React Frontend communicates with the Node.js Backend rather than directly with internal services.

The browser does not directly access:

    OpenAI API
    ChromaDB
    Python Data Agent

This keeps credentials, orchestration and internal service topology outside the client application.

---

## Chart Proxy Protection

Generated chart access is mediated by the Node.js Backend.

The public application route is:

    GET /api/charts/:filename

The Backend validates the filename before requesting the corresponding resource from the Python Data Agent.

This prevents arbitrary path traversal through the chart endpoint.

---

## Chat API Protection

The conversational endpoint:

    POST /api/chat

is protected by application-level rate limiting.

The validated default policy allows:

    30 requests
    per 15-minute window

The policy is configurable through:

    CHAT_RATE_LIMIT_WINDOW_MINUTES
    CHAT_RATE_LIMIT_MAX_REQUESTS

When the configured limit is exceeded, the Backend returns:

    HTTP 429 Too Many Requests

The limiter is applied before the request reaches the paid AI orchestration path, preventing excessive requests from unnecessarily invoking the model.

This protection is intentionally lightweight and appropriate for the current project scope. It does not replace user authentication, role-based authorization, enterprise identity controls or distributed rate limiting, which remain production-oriented extensions.

---

# Resilience

Maranello AI treats specialized AI capabilities as dependencies that can fail independently.

The Backend therefore distinguishes between:

    Backend Availability

and:

    Dependency Availability

For example, the Backend can remain operational even if:

- ChromaDB is temporarily unavailable;
- the Python Data Agent is temporarily unavailable.

When a required dependency fails, the application returns a controlled error instead of silently producing unsupported information.

This behavior is particularly important for an AI system because graceful degradation must not become:

    unavailable evidence
          ↓
    fabricated evidence

The desired behavior is:

    unavailable evidence
          ↓
    explicit controlled failure

---

## Bounded Agentic Execution

The autonomous tool-calling loop is explicitly bounded.

The Backend defines:

    MAX_TOOL_ROUNDS = 5

Each round may allow the model to request one or more supported tools, but execution cannot continue indefinitely.

If the maximum number of tool-calling rounds is reached before a final assistant answer is produced, orchestration stops with a controlled error.

This protects the application from unbounded agentic loops, excessive dependency calls and uncontrolled AI API consumption while preserving autonomous routing within a defined execution boundary.

---

## Resilient Inter-Service HTTP

Backend communication with the Python Data Agent uses a shared resilient HTTP request mechanism.

The mechanism provides:

- explicit request timeouts through `AbortController`;
- retries for transient network failures;
- retries for transient HTTP `5xx` responses;
- backoff between retry attempts;
- no automatic retry for HTTP `4xx` responses;
- controlled failure after the configured attempts are exhausted.

The same mechanism is reused by the Data Agent analysis client and the chart client, avoiding duplicated network-resilience behavior.

The distinction between transient and non-transient failures is intentional. Server-side or network failures may succeed on a later attempt, while client-side `4xx` responses normally indicate a request that should not be repeated automatically.

Together, bounded agentic execution and resilient dependency communication reduce the risk that temporary failures or repeated model tool requests become uncontrolled execution.

---

# Architectural Decisions

Several architectural decisions shaped the final implementation of Maranello AI.

These decisions reflect the project's focus on modularity, safety, testability and enterprise-oriented software engineering.

---

## ADR-01 — Node.js as the Orchestration Backend

The initial project prototype explored a Python/FastAPI application backend.

The final architecture moved the central orchestration responsibility to:

    Node.js
    Express
    TypeScript

Python remains responsible for specialized manufacturing analytics through an independent FastAPI microservice.

This separation creates a clear distinction between:

    Application Orchestration
            ↓
    Node.js Backend

and:

    Structured Data Analysis
            ↓
    Python Data Agent

The original Python backend prototype was preserved separately in Git history rather than remaining part of the final application architecture.

---

## ADR-02 — Native OpenAI Function Calling

The final orchestration layer uses:

    OpenAI Responses API
        +
    Native Function Calling

instead of introducing an additional agent orchestration framework.

The model receives explicit tool definitions and autonomously determines when they should be used.

This keeps the central orchestration flow relatively small and transparent while still supporting:

- direct responses;
- RAG;
- data analysis;
- Hybrid interactions;
- multiple function calls;
- multiple tool-execution rounds.

Frameworks such as LangGraph are therefore not required by the current architecture.

---

## ADR-03 — LLM Routing Instead of a Separate Classifier

Maranello AI does not use a separate classifier that assigns each request to rigid categories such as:

    Document
    Analytical
    Hybrid

Instead, routing emerges from the model's function-calling decisions.

The model can choose:

    no tool
    one tool
    multiple tools

based on the evidence required to answer the user's question.

This avoids duplicating intent interpretation between a classifier and the orchestration model.

---

## ADR-04 — Deterministic Data Agent

A general-purpose Python execution agent could provide greater analytical flexibility.

However, the final implementation deliberately uses a deterministic analytical service.

The trade-off is:

    Less Arbitrary Flexibility

            for

    Greater Security
    Greater Reproducibility
    Greater Predictability
    Greater Testability

This is especially appropriate for the project's manufacturing quality scenario, where analytical results should remain reproducible.

---

## ADR-05 — Dedicated Python Microservice

Manufacturing analytics remain isolated in a Python service because the Python data ecosystem provides appropriate tools for:

    Pandas
    Matplotlib
    data cleaning
    analytical processing

The Node.js Backend therefore does not reproduce analytical logic.

Instead:

    Node.js
      ↓
    HTTP Boundary
      ↓
    Python FastAPI
      ↓
    Pandas / Matplotlib

This creates a polyglot architecture in which each runtime is used for the responsibility it handles best.

---

## ADR-06 — ChromaDB as a Local Vector Store

The project uses:

    ChromaDB

as the vector database for the fictional enterprise Knowledge Base.

This supports a self-contained local demonstration environment while preserving a realistic RAG architecture.

The vector store can be rebuilt from the source Knowledge Base when required.

---

## ADR-07 — OpenAI Multilingual Embeddings

Cross-language retrieval is an important requirement because:

    User Questions
        Italian or English

while:

    Knowledge Base
        English

During development, local embedding approaches were evaluated for this retrieval scenario.

The final implementation uses:

    text-embedding-3-small

to provide stronger semantic retrieval across Italian and English.

This allows an Italian query to retrieve relevant English enterprise documentation without maintaining duplicate translated Knowledge Base files.

---

## ADR-08 — Backend Chart Proxy

The React Frontend does not communicate directly with the Python Data Agent to retrieve generated charts.

Instead:

    Python Data Agent
          ↓
    Node.js Backend
          ↓
    React Frontend

The Backend rewrites the internal chart reference and exposes:

    /api/charts/:filename

This preserves the Backend as the single application gateway for the browser.

---

## ADR-09 — In-Memory Conversation State

The current implementation stores conversational session state in memory.

This is sufficient for the local educational and portfolio scope of the project.

A production deployment could replace this with distributed persistence such as a database or cache without changing the main conversational contract.

Persistent distributed conversation storage is therefore considered a future enhancement rather than an incomplete requirement.

---

## ADR-10 — Prepared Dataset Cache

The Python Data Agent uses a dedicated `DatasetRepository` to lazily load, clean and cache the prepared Manufacturing Dataset once per process.

Repeated analytical requests reuse the prepared dataset instead of repeating CSV loading and deterministic cleaning.

An explicit reload operation is available when the source dataset must be refreshed, and a failed reload preserves the previously valid cache.

This decision removes unnecessary repeated disk I/O and preparation work while retaining the Pandas-based analytical architecture required by the current project scope.

---

## ADR-11 — Bounded Agentic Tool Execution

Autonomous LLM tool execution is bounded through:

    MAX_TOOL_ROUNDS = 5

The model remains responsible for deciding whether and which supported tools to invoke, but orchestration cannot continue through an unlimited sequence of tool-calling rounds.

If the execution boundary is reached before a final assistant response is produced, the Backend terminates orchestration with a controlled error.

This preserves autonomous routing while protecting the application from unbounded loops and uncontrolled dependency or AI API consumption.

---

## ADR-12 — Resilient Inter-Service HTTP

Communication from the Node.js Backend to the Python Data Agent uses a shared resilient HTTP mechanism.

The mechanism provides explicit timeouts through `AbortController`, retries transient network failures and HTTP `5xx` responses, applies backoff between attempts and does not automatically retry HTTP `4xx` responses.

The same behavior is reused by both analytical requests and chart retrieval.

Centralizing this policy avoids duplicated resilience logic and gives internal service failures consistent behavior.

---

## ADR-13 — RAG Relevance Threshold

Semantic nearest-neighbor retrieval is not treated as sufficient evidence by itself.

The RAG retriever applies:

    maxDistance = 0.70

and accepts only candidates with a valid finite semantic distance less than or equal to that threshold.

Retrieval may therefore return zero chunks when no sufficiently relevant Knowledge Base evidence is available.

The threshold was empirically calibrated against the current English Knowledge Base, multilingual query behavior and the configured embedding model. It is project-specific and should be re-evaluated if the corpus, chunking strategy or embedding model changes.

---

## ADR-14 — Managed Chart Retention

Generated analytical PNG files have an explicit lifecycle managed by the Python Data Agent.

The default policy retains application-managed charts for 24 hours and performs cleanup every 60 minutes.

Cleanup runs once during application startup and periodically during runtime, while shutdown cancels the background task cleanly.

Only files matching:

    monthly_defect_rate_*.png

are eligible for automatic removal.

This prevents generated artifacts from accumulating indefinitely without allowing the cleanup mechanism to delete unrelated files.

---

## ADR-15 — Chat API Hardening and Observability

The conversational API includes lightweight application-level protection and request observability appropriate to the current project scope.

The Backend:

- requires a valid non-empty `OPENAI_API_KEY` at startup;
- rate-limits Chat API requests, with a default policy of 30 requests per 15-minute window;
- assigns a request ID to each Chat API request;
- returns the identifier through `X-Request-Id`;
- records structured request metadata including status, latency and tools used;
- aggregates OpenAI token usage across all orchestration rounds;
- keeps operational token metadata internal rather than exposing it in the public Chat API response.

Authentication, RBAC, distributed rate limiting and centralized observability infrastructure remain production-scale extensions rather than implemented project features.

---

# Development Workflow

Maranello AI was developed incrementally using a repeatable engineering workflow.

Each significant feature followed the sequence:

    Requirements
        ↓
    Design
        ↓
    Implementation
        ↓
    Testing
        ↓
    Static Verification
        ↓
    Refactoring
        ↓
    Documentation
        ↓
    Commit
        ↓
    Push

The objective was to keep each development increment:

- understandable;
- testable;
- reviewable;
- reversible;
- documented.

Git commits were kept focused on coherent project changes rather than treating the repository as a single final code dump.

---

# Git History and Project Evolution

The repository history reflects the evolution of the architecture.

Major project milestones include:

- repository and documentation foundation;
- synthetic manufacturing dataset creation;
- fictional enterprise Knowledge Base creation;
- Python Data Agent implementation;
- Node.js orchestration Backend;
- ChromaDB RAG integration;
- multilingual semantic retrieval;
- OpenAI native function calling;
- React conversational Frontend;
- full-stack integration;
- chart proxy;
- automated testing;
- manual QA;
- resilience improvements;
- as-built documentation.

An earlier Python/FastAPI and Streamlit prototype was intentionally removed from the final `main` architecture after the project requirements were refined.

The prototype remains preserved in Git history for traceability.

This evolution demonstrates the transition from an initial AI application prototype to the final Hybrid AI architecture.

---

# Engineering Principles

The final architecture follows several recurring engineering principles:

- Separation of Concerns
- Explicit Application Boundaries
- Configuration over Hardcoding
- Strong Typing
- Deterministic Data Processing
- Reproducible Analytics
- Controlled Tool Execution
- Source-Grounded AI Responses
- Graceful Failure Handling
- Modular Components
- Testability
- Maintainability
- Incremental Development

These principles are applied pragmatically according to the scope of the project rather than being treated as claims of full production readiness.

Maranello AI is designed as an enterprise-oriented engineering demonstration, while production capabilities outside the project scope are documented explicitly as future enhancements.

---

# Documentation

Maranello AI includes a structured technical documentation set describing the project from business requirements to implementation and verification.

The documentation is located in:

    docs/

The final as-built technical documentation is available under:

    docs/it/

and contains six primary documents.

| Document | Purpose | Status |
|----------|---------|--------|
| `01_Project_Vision_and_Scope.md` | Business vision, objectives, stakeholders and project scope | Final |
| `02_Software_Requirements_Specification.md` | Functional and non-functional requirements, business rules, use cases and acceptance criteria | Final |
| `03_System_Architecture.md` | As-built system architecture and architectural decisions | Final |
| `04_Data_Model.md` | Manufacturing dataset, Knowledge Base and application data structures | Final |
| `05_API_Specification.md` | REST API contracts and service communication | Final |
| `06_Test_Plan.md` | Testing strategy, automated verification and manual QA evidence | Final |

The documentation set is aligned with the final implementation rather than the original prototype architecture.

---

## Documentation Map

Different documents answer different project questions.

    Why does the system exist?
            ↓
    01_Project_Vision_and_Scope.md

    What must the system do?
            ↓
    02_Software_Requirements_Specification.md

    How is the system structured?
            ↓
    03_System_Architecture.md

    How is information represented?
            ↓
    04_Data_Model.md

    How do services communicate?
            ↓
    05_API_Specification.md

    How was the system verified?
            ↓
    06_Test_Plan.md

The root README provides the entry point for installation, execution and high-level project understanding.

---

# Project Status

The Maranello AI implementation and final validation activities are complete.

The final application includes:

| Component | Status |
|-----------|--------|
| Business scenario definition | Completed |
| Synthetic Manufacturing Dataset | Completed |
| Dataset cleaning pipeline | Completed |
| Fictional enterprise Knowledge Base | Completed |
| Consolidated Knowledge Base PDF | Completed |
| Knowledge Base chunking and indexing | Completed |
| ChromaDB integration | Completed |
| Multilingual semantic retrieval | Completed |
| Python FastAPI Data Agent | Completed |
| Pandas analytical engine | Completed |
| Matplotlib chart generation | Completed |
| Node.js / Express Backend | Completed |
| Conversation Manager | Completed |
| OpenAI Responses API integration | Completed |
| Native function calling | Completed |
| Autonomous tool routing | Completed |
| RAG execution | Completed |
| Structured data analysis | Completed |
| Hybrid tool execution | Completed |
| Multi-turn conversation | Completed |
| React conversational Frontend | Completed |
| Native chart rendering | Completed |
| Backend chart proxy | Completed |
| Controlled dependency failures | Completed |
| Backend automated test suite | Completed |
| Frontend quality verification | Completed |
| Python quality verification | Completed |
| Manual end-to-end QA | Completed |
| As-built technical documentation | Completed |
| Final project presentation | Completed |
| Clean-clone validation | Completed |

The project is therefore ready for final delivery.

The remaining activity is the external submission and packaging of the required project artifacts.

---

# Current Project Scope

Maranello AI is designed as an educational, portfolio and engineering demonstration project.

The implemented scope focuses on:

- Hybrid AI orchestration;
- Retrieval-Augmented Generation;
- structured manufacturing analysis;
- multilingual interaction;
- conversational context;
- deterministic analytical execution;
- chart generation;
- service-oriented architecture;
- automated testing;
- controlled dependency failures;
- technical documentation.

The project demonstrates these capabilities in a local development environment.

It should not be interpreted as a complete production deployment for a real automotive organization.

---

# Intentional Scope Boundaries

Several capabilities commonly required by a production enterprise platform are intentionally outside the current implementation scope.

These include:

- user authentication;
- role-based authorization;
- persistent conversation storage;
- distributed session management;
- production secrets management;
- enterprise identity integration;
- centralized log aggregation and observability platforms;
- distributed tracing;
- production monitoring and alerting;
- automated CI/CD;
- container orchestration;
- high availability;
- horizontal scaling;
- distributed or identity-aware rate limiting;
- enterprise audit logging;
- production cloud deployment.

The current implementation nevertheless includes targeted application-level hardening appropriate to the project scope, including fail-fast OpenAI credential validation, Chat API rate limiting, controlled tool execution boundaries and protected chart access.

Their presence does not turn the project into a production enterprise platform: authentication, authorization, centralized operational infrastructure and distributed controls would still be required for that evolution.

These scope boundaries do not affect the core Hybrid AI scenario demonstrated by the project.

---

# Future Improvements

The architecture was designed so that additional capabilities can be introduced without fundamentally changing the conversational contract.

Potential future improvements include the following.

## Authentication and Authorization

Introduce enterprise identity management and access control.

Possible evolution:

    User
      ↓
    Authentication
      ↓
    Role / Permissions
      ↓
    Authorized Knowledge and Data Access

This would allow different categories of employees to access only the documents and analytical capabilities appropriate to their role.

---

## Persistent Conversation Storage

The current Conversation Manager stores session state in memory.

A production evolution could introduce persistent storage using:

    Redis
    relational database
    document database

depending on deployment and scalability requirements.

This would enable:

- session recovery;
- multiple Backend instances;
- longer-lived conversations;
- conversation history;
- distributed deployments.

---

## Production Knowledge Management

The current Knowledge Base is intentionally small and static.

A production implementation could introduce:

- document upload workflows;
- automatic ingestion;
- document versioning;
- incremental re-indexing;
- document lifecycle management;
- access-controlled retrieval;
- metadata filtering;
- retrieval evaluation.

---

## Extended Data Agent

The deterministic Data Agent could be extended with additional validated analytical operations.

Examples include:

- configurable time windows;
- multi-dimensional analysis;
- anomaly detection;
- statistical comparisons;
- forecasting;
- richer chart types;
- additional manufacturing KPIs;
- root-cause analysis workflows.

The deterministic execution model could remain in place while expanding the set of supported operations.

### Data Scalability

The current analytical implementation intentionally uses Pandas.

For the present project scope, the Manufacturing Dataset contains approximately 2,000 rows and the prepared dataset is cached once per Data Agent process through `DatasetRepository`. At this scale, Pandas provides a simple, transparent and appropriate analytical runtime while remaining aligned with the project requirements.

The current implementation therefore does not introduce an additional SQL analytical engine.

If the dataset grows to hundreds of thousands or millions of rows, or if keeping the prepared dataset in memory creates significant RAM pressure, the data-access layer should be re-evaluated.

A future evolution could move filtering and aggregation closer to the storage layer through:

- DuckDB for analytical SQL workloads over tabular files such as CSV or Parquet;
- SQLite for lightweight persistent relational workloads;
- or an external database when deployment, concurrency or data volume requires a dedicated data platform.

A possible evolution would be:

    Current architecture
    CSV
      ↓
    DatasetRepository
      ↓
    Prepared Pandas DataFrame
      ↓
    Deterministic Analysis

    Larger-scale architecture
    Persistent / columnar data
      ↓
    DuckDB, SQLite or external database
      ↓
    SQL filtering and aggregation
      ↓
    Smaller analytical result set
      ↓
    Deterministic Analysis

This migration would preserve the deterministic analytical contract of the Data Agent while avoiding the requirement to load an increasingly large source dataset entirely into process memory.

DuckDB and SQLite are therefore documented as scalability paths rather than implemented runtime dependencies.

---

## Persistent Analytical Artifacts

Generated charts are currently intended for conversational use.

A future implementation could introduce:

- persistent chart storage;
- analytical report generation;
- exportable dashboards;
- historical analysis artifacts;
- report sharing.

---

## Observability

The current Backend includes application-level structured observability for the conversational request path.

Each Chat API request is assigned a request identifier. The identifier is propagated through the request lifecycle and returned to the client through:

    X-Request-Id

Structured request records capture operational metadata including:

- request ID;
- HTTP status code;
- request latency;
- tools used during orchestration;
- OpenAI token usage.

Token usage is collected from the OpenAI Responses API and accumulated across every orchestration round, including intermediate tool-calling rounds.

The tracked values are:

    inputTokens
    outputTokens
    totalTokens

These values are retained as internal observability metadata and are not exposed in the public Chat API response consumed by the React Frontend.

The observability middleware also records requests that terminate before successful AI orchestration, including validation failures and rate-limited requests such as HTTP 400 and HTTP 429 responses.

This provides lightweight request-level visibility without coupling the public API contract to operational telemetry.

The current implementation does not include a centralized observability platform. A production evolution could export the existing structured telemetry to centralized infrastructure and extend it with:

- centralized log aggregation;
- service and business metrics;
- distributed tracing;
- dashboards and alerting;
- retrieval-quality metrics;
- dependency health monitoring;
- long-term latency and token-usage analysis.

---

## Containerization

The current project is designed to run locally as separate services.

A future deployment could containerize:

    React Frontend
    Node.js Backend
    ChromaDB
    Python Data Agent

and orchestrate them through Docker Compose or a production container platform.

Containerization is intentionally treated as a deployment enhancement rather than a requirement of the current implementation.

---

## CI/CD

Automated quality checks could be integrated into a CI/CD pipeline.

A future pipeline could execute:

    Backend Type Check
            ↓
    Backend Lint
            ↓
    Backend Tests
            ↓
    Backend Build
            ↓
    Frontend Lint
            ↓
    Frontend Build
            ↓
    Deployment

The current repository already separates these quality operations so that they can later be automated.

---

# Business Value

Maranello AI demonstrates how a conversational AI system can reduce the separation between enterprise documentation and operational data.

Traditional workflows may require an employee to:

    search documentation
            +
    inspect operational reports
            +
    calculate KPIs
            +
    interpret company procedures
            +
    manually combine the results

Maranello AI instead provides:

    Natural-Language Question
            ↓
    Autonomous Evidence Selection
            ↓
    Enterprise Knowledge
            +
    Manufacturing Data
            ↓
    Contextual Answer

Potential business benefits of this architecture include:

- faster access to internal procedures;
- reduced time spent searching documentation;
- easier access to manufacturing KPIs;
- consistent interpretation of operational policies;
- lower technical barriers to data exploration;
- unified access to structured and unstructured information;
- improved contextual decision support.

The project does not claim to automate manufacturing decisions.

Its purpose is to demonstrate how AI can assist users by retrieving, calculating and combining relevant evidence.

---

# Engineering and Portfolio Value

Maranello AI was intentionally developed as more than a minimal conversational AI demonstration.

The project combines several software engineering, AI engineering and data engineering disciplines within a single architecture:

    Full-Stack Development
            +
    AI Orchestration
            +
    Retrieval-Augmented Generation
            +
    Vector Search
            +
    Data Engineering
            +
    Data Analysis
            +
    Microservices
            +
    API Design
            +
    Testing
            +
    Technical Documentation

From an engineering perspective, the project demonstrates experience with:

- React and TypeScript;
- Node.js and Express;
- Python and FastAPI;
- Pandas;
- Matplotlib;
- OpenAI Responses API;
- native LLM function calling;
- embedding models;
- ChromaDB;
- Retrieval-Augmented Generation;
- REST APIs;
- multi-service integration;
- deterministic analytical processing;
- conversational state;
- resilience patterns;
- automated testing;
- Git-based incremental development;
- structured software documentation.

The architecture also demonstrates the ability to decide where generative AI should be used and where deterministic software should remain authoritative.

---

# Key Engineering Lesson

One of the central design principles demonstrated by Maranello AI is that an enterprise AI application should not delegate every responsibility to the Large Language Model.

The final architecture deliberately separates:

    Language Understanding
            ↓
            LLM

    Tool Selection
            ↓
            LLM

    Policy Evidence
            ↓
       Knowledge Base

    Numerical Evidence
            ↓
       Python Data Agent

    Data Processing
            ↓
          Pandas

    Final Explanation
            ↓
            LLM

This separation allows generative reasoning to be used where it provides value while keeping authoritative information and deterministic calculations under application control.

---

# Project Evolution

Maranello AI evolved significantly during development.

The initial prototype explored:

    FastAPI Backend
          +
    Streamlit Frontend
          +
    Provider-Abstraction Layer

As the final requirements and architecture were refined, the system evolved into:

    React Frontend
          +
    Node.js / Express Backend
          +
    OpenAI Native Function Calling
          +
    ChromaDB RAG
          +
    Python FastAPI Data Agent

The previous prototype was removed from the final `main` architecture while being preserved in Git history for traceability.

This evolution reflects an important part of the engineering process:

    Requirements
        ↓
    Architectural Evaluation
        ↓
    Refactoring
        ↓
    Final As-Built Architecture

The final architecture is therefore the result of iterative design rather than an attempt to preserve early implementation decisions after the requirements changed.

---

# Final Validation

Before final delivery, Maranello AI was validated from a fresh repository clone using only the installation and execution procedure documented in this README.

The clean-clone validation confirmed the complete setup workflow:

    Clone Repository
          ↓
    Configure Environment
          ↓
    Install Backend Dependencies
          ↓
    Install Frontend Dependencies
          ↓
    Create Python 3.12 Virtual Environment
          ↓
    Install Python Data Agent Dependencies
          ↓
    Install ChromaDB CLI
          ↓
    Start ChromaDB
          ↓
    Index Knowledge Base
          ↓
    Start Python Data Agent
          ↓
    Start Node.js Backend
          ↓
    Start React Frontend
          ↓
    Execute End-to-End Verification

The clean environment successfully verified:

- Node.js Backend dependency installation and startup;
- React Frontend dependency installation and startup;
- Python 3.12 Data Agent environment creation;
- ChromaDB CLI installation and local server startup;
- Knowledge Base ingestion with 5 documents and 149 indexed chunks;
- Python Data Agent health and analytical execution;
- Node.js Backend health and orchestration;
- React conversational interface;
- Retrieval-Augmented Generation;
- manufacturing data analysis;
- monthly defect-rate analysis with native chart rendering;
- Hybrid execution combining structured data and Knowledge Base evidence;
- multi-turn conversation memory;
- autonomous LLM tool selection without a separate rule-based classifier.

The final quality checks executed successfully include:

    Backend
    18 test files
    120 tests
    TypeScript type checking
    ESLint verification
    Production build

    Frontend
    ESLint verification
    Production build

    Python Data Agent
    80 automated tests
    Ruff verification

    Automated Backend + Data Agent baseline
    200 tests

During clean-clone validation, the setup documentation was also improved to explicitly verify the Python interpreter version and document the ChromaDB CLI installation procedure.

The analytical orchestration instructions were additionally refined after end-to-end testing showed that a supported manufacturing request could trigger unnecessary clarification. The final behavior was revalidated using the request:

    Show me the monthly defect rate trend.

The system now autonomously invokes the Manufacturing Data Agent, calculates the monthly trend and renders the resulting chart without requiring unnecessary additional input.

A final Hybrid validation used:

    Which supplier has the highest defect rate,
    and how should that result be classified
    according to the Supplier Quality Procedure?

The system correctly combined structured manufacturing analysis and Knowledge Base retrieval, identifying:

    SUP-07
    defect rate: 2.99%
    classification: Observation

Conversation continuity was then verified with:

    What does the policy require for that supplier?

The system correctly resolved the contextual reference to SUP-07 and retrieved the corresponding Supplier Quality Procedure requirements.

The clean-clone procedure therefore confirms that the repository can be installed, started and exercised from a fresh environment using the documented setup instructions.

---

# Author

**Marco Saccani**

Data Engineer and AI Engineering Student

Maranello AI was developed as part of a Master's final project and as a portfolio project focused on the intersection of:

- Artificial Intelligence;
- Data Engineering;
- Software Engineering;
- enterprise AI architecture.

---

# License and Usage

Maranello AI is currently provided as an educational and portfolio project.

Unless a dedicated license file is added to the repository, no open-source license should be assumed.

The source code, synthetic dataset and fictional documentation are provided for demonstration and educational purposes within the scope of the project.

All third-party technologies, libraries, trademarks and product names remain the property of their respective owners.

---

# Final Disclaimer

Maranello AI is a fictional system.

It is not affiliated with, endorsed by, sponsored by, or associated with Ferrari N.V. or any other automotive manufacturer.

The project does not contain real internal automotive company data, confidential documents, proprietary manufacturing processes or authentic company policies.

The Manufacturing Dataset is synthetic.

The Knowledge Base and all internal procedures are fictional.

Any resemblance to real organizations, business processes, operational thresholds or internal documentation is coincidental.

The project exists exclusively to demonstrate software engineering, AI engineering and data engineering concepts.