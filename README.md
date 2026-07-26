# Maranello AI

> An enterprise AI Knowledge Management platform built with FastAPI, Streamlit and a provider-agnostic AI architecture.

---

## Disclaimer

This project is entirely fictional and has been developed exclusively for educational and portfolio purposes.

It is **not affiliated with, endorsed by, or associated with Ferrari N.V.** Any reference to Ferrari, company policies, internal documentation, business processes or datasets is purely fictional and intended solely to demonstrate software engineering, AI engineering and data engineering practices.

---

# Overview

Maranello AI is an enterprise-oriented AI platform designed to provide reliable, contextual and multilingual answers over an internal corporate knowledge base.

Unlike a traditional chatbot, the project has been designed following modern software engineering principles, with a strong focus on modularity, maintainability, scalability and testability.

The long-term objective is to simulate a production-ready enterprise AI platform capable of integrating multiple information sources while maintaining a clean and extensible architecture.

The application is being developed incrementally, with every feature following the same workflow:

- Design
- Implementation
- Testing
- Static Analysis
- Documentation
- Commit
- Push

Each increment represents a small, coherent and verifiable improvement to the project.

---

# Project Goals

The final application aims to provide the following capabilities:

- Answer questions in both Italian and English
- Automatically detect the user's language
- Search an enterprise knowledge base using Retrieval-Augmented Generation (RAG)
- Cite the source documents used to generate responses
- Query structured company data
- Coordinate multiple tools through an AI Agent
- Minimize hallucinations by relying on trusted information sources
- Expose REST APIs for external integrations
- Provide a modern and intuitive web interface
- Demonstrate production-level software engineering practices

---

# Key Features

## Current Features

### Backend

- FastAPI REST API
- Modular project architecture
- Configuration management
- Dependency Injection
- Structured logging
- Health monitoring endpoint
- Interactive Swagger documentation

### Frontend

- Streamlit chat interface
- Backend integration
- Modern conversational UI

### AI Layer

- Provider-agnostic AI Engine
- AI Provider Factory
- Mock LLM Provider
- OpenAI Responses API Provider
- Structured AI response model
- Environment-based provider selection
- Usage and latency tracking

### Quality Assurance

- Unit tests
- Integration tests
- Ruff static analysis
- Typed Python codebase
- Clean architecture principles

---

## Planned Features

The following capabilities will be implemented during future development phases.

### Knowledge Management

- Enterprise Knowledge Base
- Document ingestion pipeline
- Automatic document chunking
- Embedding generation
- Vector database
- Semantic retrieval

### Artificial Intelligence

- Retrieval-Augmented Generation (RAG)
- Prompt Management
- Conversation Memory
- LangGraph Agent
- Multi-tool orchestration

### Enterprise Features

- Structured Data Retrieval
- Authentication and Authorization
- Docker deployment
- CI/CD pipeline
- Monitoring and Observability

---

# Current Status

The project is currently under active development.

Completed components include:

| Component | Status |
|-----------|--------|
| Project Design | Completed |
| Technical Documentation | Completed |
| FastAPI Backend | Completed |
| Streamlit Frontend | Completed |
| REST API | Completed |
| AI Engine | Completed |
| Provider Factory | Completed |
| Mock Provider | Completed |
| OpenAI Provider | Completed |
| Structured AI Response | Completed |
| Configuration Management | Completed |
| Logging | Completed |
| Unit Tests | Completed |
| Integration Tests | Completed |
| Ruff Static Analysis | Completed |

Current development focus:

- Prompt Management
- Enterprise Knowledge Base

---

# High-Level Architecture

The current software architecture is illustrated below.

```text
                           +----------------------+
                           |        User          |
                           +----------------------+
                                      |
                                      |
                                      v
                           +----------------------+
                           | Streamlit Frontend   |
                           +----------------------+
                                      |
                                      |
                                      v
                           +----------------------+
                           |  FastAPI Backend     |
                           +----------------------+
                                      |
                                      |
                                      v
                           +----------------------+
                           |    Chat Service      |
                           +----------------------+
                                      |
                                      |
                                      v
                           +----------------------+
                           |      AI Engine       |
                           +----------------------+
                                      |
                          +-----------+-----------+
                          |                       |
                          |                       |
                          v                       v
                 +----------------+      Future Modules
                 | ProviderFactory|      (RAG, Tools...)
                 +----------------+
                          |
             +------------+------------+
             |                         |
             |                         |
             v                         v
    +----------------+       +----------------------+
    | Mock Provider  |       | OpenAI Provider      |
    +----------------+       +----------------------+
```

The architecture has been intentionally designed to remain independent from any specific Large Language Model provider.

Every AI request is processed by the AI Engine, which delegates the execution to the configured provider through the Provider Factory. This design allows additional providers to be integrated without affecting the application layer.

---

# Design Principles

The project follows a set of architectural principles inspired by enterprise software development.

- Separation of Concerns
- Dependency Injection
- Provider Abstraction
- Configuration over Hardcoding
- Testability
- Incremental Development
- Clean Architecture
- Strong Typing
- Modular Components
- Maintainable Codebase

These principles guide every architectural decision made throughout the project.

---

# AI Architecture

One of the primary goals of Maranello AI is to remain independent from any specific Large Language Model provider.

For this reason, the AI layer has been designed around a provider-agnostic architecture where every component has a single responsibility.

```text
                    User Request
                          │
                          ▼
                   FastAPI Endpoint
                          │
                          ▼
                    Chat Service
                          │
                          ▼
                     AI Engine
                          │
                          ▼
                  Provider Factory
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
   Mock Provider                 OpenAI Provider
          │                               │
          └───────────────┬───────────────┘
                          ▼
                    AIResponse Model
```

The API layer never communicates directly with a language model.

Instead, every request is delegated to the AI Engine, which is responsible for:

- Selecting the configured provider
- Executing the request
- Normalizing the response
- Returning a structured AIResponse object

This approach offers several advantages:

- Loose coupling between business logic and LLM providers
- Easier testing through deterministic mock providers
- Simple integration of additional providers
- Better maintainability
- Easier migration between AI platforms

Current supported providers:

| Provider | Status |
|----------|--------|
| Mock Provider | Available |
| OpenAI Responses API | Available |

Planned providers:

| Provider | Planned |
|----------|----------|
| Azure OpenAI | Yes |
| Ollama | Yes |
| Google Gemini | Yes |

---

# Technology Stack

The project intentionally separates technologies according to their responsibilities.

## Backend

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic

## Frontend

- Streamlit

## Artificial Intelligence

- OpenAI Python SDK
- OpenAI Responses API

## Testing

- Pytest

## Code Quality

- Ruff

## Documentation

- Markdown
- Mermaid Diagrams (planned)

## Planned Technologies

- LangChain
- LangGraph
- ChromaDB
- Docker
- GitHub Actions

---

# Repository Structure

```text
maranello-ai/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── ai/
│   │   │   ├── providers/
│   │   │   ├── models/
│   │   │   ├── engine.py
│   │   │   └── factory.py
│   │   │
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   │
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/
│
├── knowledge_base/
│
├── data/
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

# Getting Started

## Clone the repository

```bash
git clone <repository-url>
cd maranello-ai
```

## Create a virtual environment

Linux / macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## Install project dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

---

# Environment Configuration

Create a local environment configuration file.

```bash
cp .env.example .env
```

The application supports multiple AI providers.

Only one provider can be active at a time.

---

## Mock Provider

Recommended for local development and automated testing.

```env
LLM_PROVIDER=mock
LLM_MODEL=mock-model
```

Characteristics:

- No API key required
- Deterministic responses
- Fast execution
- Ideal for automated tests

---

## OpenAI Provider

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-5-mini

OPENAI_API_KEY=your-api-key
```

Characteristics:

- Uses the OpenAI Responses API
- Supports real conversational responses
- Tracks latency and token usage
- Configurable through environment variables

The `.env` file contains secrets and **must never be committed**.

---

# Running the Project

## Start the Backend

```bash
cd backend

python -m uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

---

## Start the Frontend

Open another terminal.

```bash
cd frontend

streamlit run app.py
```

The Streamlit interface will automatically open in your browser.

---

# API Documentation

Interactive Swagger documentation is automatically generated by FastAPI.

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

Health Endpoint

```text
GET /api/v1/health
```

The health endpoint can be used by monitoring systems and deployment platforms to verify that the application is running correctly.

---

# Testing

The project includes both unit and integration tests to ensure correctness, maintainability and long-term stability.

## Unit Tests

Unit tests validate the behavior of individual components in isolation.

Current coverage includes:

- AI Engine
- Provider Factory
- Mock Provider
- OpenAI Provider
- Business Logic

Run unit tests from the `backend` directory.

```bash
python -m pytest tests/unit
```

---

## Integration Tests

Integration tests verify the interaction between the API layer and the application services.

The integration test suite uses the Mock Provider to ensure deterministic behavior without requiring external API calls.

Run integration tests with:

```bash
python -m pytest tests/integration
```

---

## Run the Entire Test Suite

```bash
python -m pytest
```

---

# Code Quality

Static analysis is performed using Ruff.

Run all checks with:

```bash
python -m ruff check .
```

Future improvements include:

- Ruff automatic formatting
- Pre-commit hooks
- Test coverage reporting
- GitHub Actions quality gates

---

# Documentation

Project documentation is available inside the `docs/` directory.

Current documentation includes:

- Project Vision
- Software Requirements Specification
- Software Architecture
- API Specification
- Data Model
- Test Plan

Additional documentation will be added as the project evolves.

---

# Roadmap

Development is organized into incremental phases.

## Phase 1 — Foundation

Completed

- Repository setup
- Project documentation
- FastAPI backend
- Streamlit frontend
- Configuration management
- Logging
- REST API
- AI Engine
- Provider Factory
- Mock Provider
- OpenAI Provider
- Unit tests
- Integration tests

---

## Phase 2 — Prompt Management

In Progress

- Prompt Manager
- Prompt Templates
- Prompt Versioning

---

## Phase 3 — Knowledge Base

Planned

- Document Loader
- Document Validation
- Document Chunking
- Metadata Extraction
- Embedding Generation

---

## Phase 4 — Retrieval

Planned

- Vector Database
- Semantic Search
- Retriever
- Source Ranking

---

## Phase 5 — Retrieval-Augmented Generation

Planned

- RAG Pipeline
- Context Assembly
- Source Citation
- Hallucination Reduction

---

## Phase 6 — AI Agents

Planned

- LangGraph Agent
- Tool Orchestration
- Structured Data Retrieval
- Multi-step Reasoning

---

## Phase 7 — Enterprise Features

Planned

- Authentication
- Authorization
- Docker
- CI/CD Pipeline
- Monitoring
- Observability
- Deployment

---

# Development Workflow

Every feature follows the same development lifecycle.

```text
Requirements
        │
        ▼
Design
        │
        ▼
Implementation
        │
        ▼
Unit Testing
        │
        ▼
Integration Testing
        │
        ▼
Static Analysis
        │
        ▼
Documentation
        │
        ▼
Commit
        │
        ▼
Push
```

Each commit represents a single, coherent and verifiable project increment.

This approach helps maintain a clean Git history while ensuring that every change can be reviewed, tested and documented independently.

---

# Design Philosophy

Maranello AI is intentionally developed as an enterprise software project rather than a simple AI demo.

The architecture prioritizes:

- Separation of Concerns
- Dependency Injection
- Provider Abstraction
- Configuration over Hardcoding
- Clean Architecture
- Strong Typing
- Incremental Development
- Testability
- Maintainability
- Scalability

Every architectural decision is evaluated according to these principles.

---

# Future Vision

The long-term objective of Maranello AI is to evolve into a complete enterprise knowledge management platform capable of combining multiple AI capabilities within a unified architecture.

The final platform is expected to integrate:

- Enterprise Knowledge Base
- Retrieval-Augmented Generation
- AI Agents
- Structured Data Querying
- Multilingual Conversations
- REST APIs
- Modern Web Interface
- Monitoring
- CI/CD
- Cloud Deployment

The project is intentionally designed so that new capabilities can be introduced without major architectural changes.

---

# Contributing

This repository is currently maintained as a personal portfolio project.

At the moment external contributions are not planned.

Suggestions, feedback and discussions are always welcome.

---

# Author

**Marco Saccani**

Data Engineer and AI Engineering Student

This project is part of a personal portfolio focused on Artificial Intelligence, Data Engineering and modern Software Engineering practices.

---

# License

License selection is currently under evaluation.

All trademarks, company names and brands referenced within this repository belong to their respective owners.

This project is provided exclusively for educational and demonstration purposes.