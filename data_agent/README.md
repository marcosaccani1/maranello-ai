# Maranello AI — Python Data Agent

The Python Data Agent is the deterministic analytical microservice of Maranello AI.

It is responsible for answering manufacturing-data questions that require structured numerical analysis rather than Knowledge Base retrieval.

The service is implemented with Python, FastAPI and Pandas and is called by the Node.js orchestration Backend when the LLM selects the manufacturing-data analysis tool.

The Data Agent does not independently decide whether a request should use RAG or data analysis. Autonomous tool selection remains the responsibility of the LLM orchestration layer in the Node.js Backend.

---

# Responsibilities

The Data Agent is responsible for:

- loading the synthetic Manufacturing Dataset;
- applying deterministic data-cleaning rules;
- interpreting supported analytical questions;
- calculating manufacturing KPIs;
- performing grouped analyses;
- calculating monthly defect-rate trends;
- generating chart images when required;
- returning structured analytical results to the Node.js Backend;
- caching the prepared dataset for reuse across analytical requests;
- managing the lifecycle of generated chart files.

The current analytical model is intentionally deterministic.

Natural-language questions are mapped to validated analytical operations instead of executing arbitrary LLM-generated Python code.

This design improves predictability, testability and operational safety while preserving a natural-language analytical interface through the main Maranello AI conversational system.

---

# Architecture

The Data Agent follows the high-level flow:

    Analytical request
          ↓
    FastAPI /api/analysis
          ↓
    DataAnalysisService
          ↓
    QuestionInterpreter
          ↓
    DatasetRepository
          ↓
    Prepared Pandas DataFrame
          ↓
    Deterministic Analysis
          ↓
    Optional Chart Generation
          ↓
    Structured Analysis Response

The main application components are located under:

    data_agent/app/

The current structure includes:

    app/
    ├── api/
    │   └── routes.py
    ├── core/
    │   └── config.py
    ├── models/
    │   └── analysis.py
    ├── services/
    │   ├── analysis_service.py
    │   ├── chart_cleanup_service.py
    │   ├── chart_service.py
    │   ├── data_analysis_service.py
    │   ├── data_cleaner.py
    │   ├── data_loader.py
    │   ├── dataset_repository.py
    │   └── question_interpreter.py
    └── main.py

---

# Dataset

By default, the service reads:

    data/manufacturing_quality_data.csv

The dataset is synthetic and was created specifically for the Maranello AI project.

It represents manufacturing production batches and contains dates, production dimensions, quality metrics, supplier information and intentionally dirty records used to exercise the cleaning pipeline.

The current project dataset contains approximately 2,000 rows.

The Data Agent must not be interpreted as processing real Ferrari manufacturing data or real corporate information.

---

# Dataset Preparation and Cache

Dataset access is encapsulated by `DatasetRepository`.

The repository uses a lazy per-process cache.

On the first analytical request:

    CSV
     ↓
    DataLoader
     ↓
    DataCleaner
     ↓
    Prepared Pandas DataFrame
     ↓
    DatasetRepository cache

Subsequent analytical requests reuse the prepared dataset rather than reading and cleaning the CSV again.

This removes repeated disk I/O and deterministic preparation work from every `POST /api/analysis` request.

The repository also provides explicit reload behavior for cases in which the source dataset must be refreshed.

A failed reload does not invalidate the existing valid cache. The previously valid cache and its prepared dataset remain available.

The repository protects its cached source DataFrame from accidental mutation by downstream analytical operations.

The cache is local to the running Data Agent process and is not a distributed cache.

---

# Deterministic Analysis

The Data Agent supports validated analytical operations over the Manufacturing Dataset.

These include:

- global manufacturing KPIs;
- grouped defect-rate analysis;
- production-line analysis;
- shift analysis;
- supplier analysis;
- component-category analysis;
- vehicle-model analysis;
- plant analysis;
- operator-team analysis;
- monthly defect-rate trends.

The `QuestionInterpreter` maps supported natural-language questions to the corresponding deterministic analytical operation.

Unsupported or ambiguous analytical combinations are rejected instead of silently inventing an analysis.

This behavior keeps analytical execution bounded and testable.

---

# Chart Generation

Analyses that require visualization can generate PNG chart files through the chart service.

Generated charts are stored by default in:

    data_agent/generated_charts/

The FastAPI application exposes this directory through:

    /charts

The Node.js Backend retrieves generated charts from the Data Agent and proxies them through the main Backend API before they are rendered by the React frontend.

---

# Generated Chart Retention

Generated analytical charts have an explicit lifecycle managed by `ChartCleanupService`.

The default retention configuration is:

    chart_retention_hours = 24.0
    chart_cleanup_interval_minutes = 60.0

At application startup, the Data Agent:

1. ensures that the generated-chart directory exists;
2. performs an immediate cleanup of expired managed charts;
3. starts the periodic cleanup task.

During runtime, cleanup runs every 60 minutes by default.

During application shutdown, the background cleanup task is cancelled cleanly.

Only application-managed files matching:

    monthly_defect_rate_*.png

are eligible for automatic removal.

Unrelated files in the chart directory are not deleted by the cleanup service.

Both retention settings must be greater than zero.

---

# API

The service exposes the following HTTP interfaces.

## Root

    GET /

Returns basic service and environment information.

## Health

    GET /health

Returns the Data Agent health status.

Example response:

    {
      "status": "ok",
      "service": "maranello-ai-data-agent",
      "environment": "development"
    }

## Analysis

    POST /api/analysis

Receives an analytical natural-language question and returns a structured analysis response.

The request is processed by `DataAnalysisService`.

Validation and supported analytical behavior are defined by the Data Agent models, interpreter and deterministic analytical services.

`ValueError` and `FileNotFoundError` failures generated by the analytical pipeline are converted into:

    HTTP 400 Bad Request

## Generated Charts

    GET /charts/<filename>

Serves generated chart files from the configured chart directory.

In the complete Maranello AI application, chart access from the React frontend is mediated by the Node.js Backend chart proxy rather than requiring the frontend to communicate directly with the Python service.

---

# Configuration

Configuration is implemented with Pydantic Settings.

The current settings are defined in:

    app/core/config.py

The service reads optional environment configuration from:

    .env

Unknown environment variables are ignored.

The current settings include:

    service_name
    environment
    project_root
    dataset_path
    charts_directory
    chart_retention_hours
    chart_cleanup_interval_minutes

Default service values include:

    service_name = maranello-ai-data-agent
    environment = development

Default data paths resolve to:

    data/manufacturing_quality_data.csv
    data_agent/generated_charts/

Default chart lifecycle values are:

    chart_retention_hours = 24.0
    chart_cleanup_interval_minutes = 60.0

The standard local project setup can use these defaults without adding Data Agent-specific variables to the root `.env`.

---

# Requirements

The package requires:

    Python >= 3.12

Runtime dependencies declared in `pyproject.toml` include:

- FastAPI;
- Uvicorn;
- Pandas;
- Matplotlib;
- Pydantic;
- Pydantic Settings.

Development dependencies include:

- HTTPX;
- Pytest;
- pytest-cov;
- Ruff.

---

# Installation

From the repository root, create and activate a Python 3.12 virtual environment according to the main project setup instructions.

Install the Data Agent and its development dependencies with:

    python -m pip install -e "./data_agent[dev]"

The root project README contains the complete clean-clone installation sequence for all Maranello AI services.

---

# Running the Service

From the `data_agent` directory, with the Python environment activated, start the service with:

    uvicorn app.main:app --host 127.0.0.1 --port 8001

The default local Data Agent address is therefore:

    http://127.0.0.1:8001

Useful local endpoints include:

    http://127.0.0.1:8001/
    http://127.0.0.1:8001/health
    http://127.0.0.1:8001/docs

The interactive FastAPI documentation is provided automatically by FastAPI.

---

# Testing and Static Verification

The Data Agent includes unit and integration tests covering the analytical and service layers.

From the repository root, with the Python virtual environment activated, run:

    python -m pytest data_agent/tests
    ruff check data_agent

The final validated Data Agent baseline contains:

    80 automated tests

The validated project state produced:

    Pytest: 80 passed
    Ruff: All checks passed

The suite covers areas including:

- dataset loading;
- deterministic cleaning;
- question interpretation;
- global analysis;
- grouped analysis;
- monthly analysis;
- chart generation;
- API integration;
- real-dataset behavior;
- `DatasetRepository` lazy caching;
- reuse of the prepared dataset across analyses;
- explicit dataset reload;
- cache preservation after a failed reload;
- cached DataFrame protection;
- `ChartCleanupService`;
- managed chart retention;
- FastAPI startup cleanup;
- periodic cleanup;
- graceful cleanup-task cancellation during shutdown.

The validated test run also reported one `StarletteDeprecationWarning` originating from the installed FastAPI/Starlette testing dependency stack.

The warning does not represent a failing project test or an application runtime error.

---

# Scalability

The current implementation intentionally uses Pandas.

For the present synthetic dataset of approximately 2,000 rows, Pandas combined with the per-process `DatasetRepository` cache provides an appropriate balance of simplicity, transparency and analytical capability.

Caching removes repeated CSV loading and cleaning overhead, but it does not turn Pandas into a database or remove the memory implications of increasingly large datasets.

If the analytical dataset grows to hundreds of thousands or millions of rows, or if memory pressure becomes significant, the storage and query layer should be re-evaluated.

Potential evolution paths include:

- DuckDB for analytical SQL over tabular or columnar data such as CSV and Parquet;
- SQLite for lightweight embedded relational persistence and queries;
- an external database for larger production workloads, concurrency or deployment requirements.

A larger-scale architecture could push filtering and aggregation into the query engine before converting smaller analytical result sets into Pandas structures when necessary.

Conceptually:

    Current
    CSV
      ↓
    DatasetRepository
      ↓
    Prepared Pandas DataFrame
      ↓
    Deterministic Analysis

    Future larger-scale option
    Persistent / columnar data
      ↓
    DuckDB, SQLite or external database
      ↓
    SQL filtering and aggregation
      ↓
    Smaller analytical result set
      ↓
    Deterministic Analysis

DuckDB and SQLite are documented scalability options, not current runtime dependencies.

The deterministic analytical contract of the Data Agent can remain stable even if the underlying storage and query implementation changes.

---

# Scope Boundaries

The current Data Agent is designed for the educational, portfolio and local integration scope of Maranello AI.

It intentionally does not implement:

- arbitrary execution of LLM-generated Python code;
- distributed dataset caching;
- a production database;
- distributed background-job infrastructure;
- persistent chart object storage;
- horizontal scaling coordination;
- production authentication or authorization.

These are possible production-scale extensions rather than incomplete requirements of the current implementation.

---

# Relationship with the Maranello AI Backend

The Data Agent is not the conversational entry point of the application.

The expected production-style request path inside the project is:

    React Frontend
          ↓
    Node.js Backend
          ↓
    LLM Autonomous Tool Selection
          ↓
    Python Data Agent
          ↓
    Deterministic Manufacturing Analysis

The Node.js Backend owns:

- conversational state;
- OpenAI interaction;
- autonomous RAG versus Data Agent routing;
- function calling;
- inter-service resilience;
- public chat responses;
- chart proxying;
- Chat API rate limiting;
- request observability.

The Python Data Agent remains focused on deterministic manufacturing analytics and chart lifecycle management.

---

# Project Context

Maranello AI is a fictional enterprise-style manufacturing assistant created as an educational and portfolio project.

The Manufacturing Dataset, Knowledge Base and operational policies included in the repository are synthetic or project-authored materials.

They must not be interpreted as confidential, internal or operational data belonging to Ferrari or any other real automotive manufacturer.

For complete installation, architecture, API, testing and delivery documentation, refer to the root project README and the documents under:

    docs/
