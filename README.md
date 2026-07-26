# Maranello AI

> An Enterprise AI Knowledge Assistant powered by FastAPI, LangGraph and Retrieval-Augmented Generation (RAG).

---

## Project Overview

Maranello AI is an advanced Enterprise AI Assistant designed to provide reliable, contextual and multilingual answers by leveraging an internal corporate knowledge base.

The goal of the project is to simulate a real-world enterprise AI platform that combines:

- Enterprise Knowledge Management
- Retrieval-Augmented Generation (RAG)
- AI Agents
- Structured Data Querying
- Multilingual Support
- REST APIs
- Modern Software Engineering practices

This repository is developed as a portfolio project to demonstrate software engineering, AI engineering and data engineering skills.

> **Disclaimer**
>
> This project is completely fictional and created for educational purposes only.
>
> It is **NOT affiliated with, endorsed by, or associated with Ferrari N.V.**
>
> Every document, policy and dataset contained in this repository has been entirely created for demonstration purposes.

---

# Objectives

The final application will be able to:

- Answer questions in Italian and English
- Detect the language automatically
- Search an enterprise Knowledge Base
- Cite the source documents used to generate responses
- Query structured company data
- Use an AI Agent to orchestrate different tools
- Prevent hallucinations by answering only with available information
- Provide a modern web interface
- Expose REST APIs

---

# Architecture

The target architecture is the following:

```text
                 +----------------+
                 |     User       |
                 +----------------+
                          |
                          |
                          ▼
                 +----------------+
                 |   Frontend UI  |
                 +----------------+
                          |
                          |
                          ▼
                 +----------------+
                 | FastAPI Backend|
                 +----------------+
                          |
                          ▼
                 +----------------+
                 | LangGraph Agent|
                 +----------------+
                    /          \
                   /            \
                  ▼              ▼
        +----------------+   +----------------+
        | RAG Pipeline   |   | Data Tools     |
        +----------------+   +----------------+
                |                    |
                ▼                    ▼
      +----------------+    +----------------+
      | Vector Database|    | Structured Data|
      +----------------+    +----------------+
                |
                ▼
      +----------------+
      | Knowledge Base |
      +----------------+
```

---

# Repository Structure

```text
maranello-ai/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
│
├── frontend/
│
├── knowledge_base/
│
├── data/
│
├── data_agent/
│
├── docs/
│   ├── en/
│   ├── it/
│   └── README.md
│
├── .env.example
├── .gitignore
└── README.md
```

---

# Current Status

## Documentation

- ✅ Project Vision & Scope
- ✅ Software Requirements Specification
- ✅ System Architecture
- ✅ Data Model
- ✅ API Specification
- ✅ Test Plan

## Backend

- ✅ FastAPI Bootstrap
- ✅ Configuration Management
- ✅ Logging
- ✅ Health Check Endpoint
- ✅ Swagger Documentation
- ✅ Integration Tests
- ✅ Ruff Static Analysis

## Planned Development

- ⏳ Streamlit Frontend
- ⏳ Enterprise Knowledge Base
- ⏳ Document Ingestion Pipeline
- ⏳ Embeddings
- ⏳ Vector Database
- ⏳ RAG Pipeline
- ⏳ LangGraph Agent
- ⏳ Structured Data Retrieval
- ⏳ Source Citations
- ⏳ Authentication
- ⏳ Docker Deployment

---

# Technology Stack

Current technologies:

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- Ruff

Planned technologies:

- LangChain
- LangGraph
- ChromaDB (or another Vector Database)
- OpenAI / Azure OpenAI
- Streamlit
- Docker

---

# Running the Backend

## Create the virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

## Start the backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

Health Endpoint

```
http://127.0.0.1:8000/api/v1/health
```

---

# Running Tests

From the backend folder:

```bash
python -m pytest
```

---

# Static Code Analysis

```bash
python -m ruff check .
```

---

# Documentation

Project documentation is available inside the **docs/** folder.

Currently available:

- Project Vision & Scope
- Software Requirements Specification
- System Architecture
- Data Model
- API Specification
- Test Plan

---

# Roadmap

- [x] Project Planning
- [x] Software Design
- [x] FastAPI Backend
- [x] Health Endpoint
- [x] Automated Tests
- [ ] Streamlit Frontend
- [ ] Knowledge Base
- [ ] Document Ingestion
- [ ] Embeddings
- [ ] Vector Database
- [ ] Retrieval Pipeline
- [ ] LangGraph Agent
- [ ] Conversation Memory
- [ ] Authentication
- [ ] Docker Deployment

---

# Development Workflow

Each feature follows the same workflow:

```text
Design
        ↓
Implementation
        ↓
Testing
        ↓
Static Analysis
        ↓
Commit
        ↓
Push
```

Each commit represents a small, coherent and verifiable project increment.

---

# Author

**Marco Saccani**

Data Engineer • AI Engineering Student

---

# License

License selection is currently under evaluation.

All trademarks and company names mentioned in this repository belong to their respective owners.