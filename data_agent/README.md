# Maranello AI — Python Data Agent

The Python Data Agent is the deterministic analytical microservice of Maranello AI.

It is responsible for answering manufacturing-data questions that require structured numerical analysis rather than Knowledge Base retrieval.

The service is implemented with Python and FastAPI. Pandas is used in the deterministic dataset loading and cleaning pipeline, while DuckDB provides the persistent local analytical storage and query layer.

The Data Agent is called by the Node.js orchestration Backend when the LLM selects the manufacturing-data analysis tool.

The Data Agent does not independently decide whether a request should use RAG or data analysis. Autonomous tool selection remains the responsibility of the LLM orchestration layer in the Node.js Backend.

---

# Responsibilities

The Data Agent is responsible for:

- automatically preparing the synthetic Manufacturing Dataset from CSV before normal worker startup;
- applying deterministic data-cleaning rules with Pandas during database preparation;
- materializing the prepared dataset into a local DuckDB database before workers start;
- starting the configured FastAPI worker processes only after preparation succeeds;
- validating at each worker startup that the analytical database has already been prepared;
- interpreting supported analytical questions;
- calculating manufacturing KPIs through deterministic read-only DuckDB queries;
- performing grouped analyses;
- calculating monthly defect-rate trends;
- generating chart images when required;
- returning structured analytical results to the Node.js Backend;
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
    DuckDBAnalysisRepository
          ↓
    DuckDB analytical queries
          ↓
    Deterministic Analysis
          ↓
    Optional Chart Generation
          ↓
    Structured Analysis Response

The normal startup path automatically prepares the analytical database once before any FastAPI worker is started:

    python -m app.commands.start_data_agent
        ↓
    Pre-worker preparation
        ↓
    DataLoader
        ↓
    DataCleaner
        ↓
    Prepared Pandas DataFrame
        ↓
    DuckDBDatasetStore.reload()
        ↓
    Local DuckDB database ready
        ↓
    Uvicorn starts configured worker processes
        ↓
    Per-worker read-only readiness validation
        ↓
    Runtime analytical queries

Dataset preparation remains separated from the worker lifecycle. The launcher completes the preparation phase before invoking Uvicorn, so no worker exists while the preparation writer is materializing the database. Workers never lazily initialize or rebuild DuckDB and use the prepared datastore only through read-only readiness checks and analytical queries.

The main application components are located under:

    data_agent/app/

The current structure includes:

    app/
    ├── api/
    │   └── routes.py
    ├── commands/
    │   ├── prepare_database.py
    │   └── start_data_agent.py
    ├── core/
    │   └── config.py
    ├── models/
    │   └── analysis.py
    ├── services/
    │   ├── chart_cleanup_service.py
    │   ├── chart_service.py
    │   ├── data_analysis_service.py
    │   ├── data_cleaner.py
    │   ├── data_loader.py
    │   ├── duckdb_analysis_repository.py
    │   ├── duckdb_dataset_store.py
    │   └── question_interpreter.py
    └── main.py

---

# Dataset

The source Manufacturing Dataset is:

    data/manufacturing_quality_data.csv

The dataset is synthetic and was created specifically for the Maranello AI project.

It represents manufacturing production batches and contains dates, production dimensions, quality metrics, supplier information and intentionally dirty records used to exercise the cleaning pipeline.

The current project dataset contains approximately 2,000 rows.

The Data Agent must not be interpreted as processing real Ferrari manufacturing data or real corporate information.

---

# DuckDB Analytical Data Layer

The Data Agent uses DuckDB as its embedded analytical storage and query layer.

The local analytical database is stored by default at:

    data/manufacturing_quality.duckdb

The database is a runtime artifact and is excluded from Git.

Its materialization lifecycle is managed by `DuckDBDatasetStore`. During normal service startup, `start_data_agent` automatically invokes the deterministic preparation phase and waits for it to complete before Uvicorn is allowed to create any worker process.

The normal startup pipeline is:

    Manufacturing CSV
          ↓
    python -m app.commands.start_data_agent
          ↓
    prepare_database()
          ↓
    DataLoader
          ↓
    DataCleaner
          ↓
    Prepared Pandas DataFrame
          ↓
    DuckDBDatasetStore.reload()
          ↓
    DuckDB analytical table ready
          ↓
    Uvicorn worker startup

The standalone `python -m app.commands.prepare_database` command remains available when an explicit database rebuild is required without starting the service.

At worker startup, the application performs only a read-only readiness check and fails fast if the analytical database is unavailable or invalid.

Normal analytical requests never load or clean the source CSV and never rebuild the DuckDB database. `DuckDBAnalysisRepository` opens read-only connections for analytical execution.

The source CSV therefore remains the reproducible project data source, while DuckDB acts as the local query-oriented representation used by the analytical runtime.

This design avoids keeping the complete prepared analytical dataset as the primary in-memory query layer and prevents concurrent workers from attempting to initialize the same DuckDB file.

The DuckDB file can be rebuilt explicitly from the source dataset through the deterministic preparation command.

The database is intentionally treated as a generated local artifact rather than a source-controlled project asset.

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

`DuckDBAnalysisRepository` owns the query-oriented analytical operations against the prepared DuckDB dataset.

The repository executes controlled analytical SQL rather than arbitrary user-provided SQL or arbitrary LLM-generated Python code.

Unsupported or ambiguous analytical combinations are rejected instead of silently inventing an analysis.

This behavior keeps analytical execution bounded, reproducible and testable.

---

# Data Preparation and Analytical Query Separation

The architecture deliberately separates two different responsibilities.

Dataset preparation uses:

    CSV
      ↓
    DataLoader
      ↓
    DataCleaner
      ↓
    Pandas DataFrame

Analytical execution uses:

    DuckDB database
          ↓
    DuckDBAnalysisRepository
          ↓
    Controlled SQL aggregation
          ↓
    Analytical result models

Pandas therefore remains useful for deterministic ingestion and cleaning, but it is no longer the primary analytical query engine.

This separation provides a clearer boundary between source-data preparation and repeated analytical workloads.

---

# Chart Generation

Analyses that require visualization can generate PNG chart files through the chart service.

Generated charts are stored by default in:

    data_agent/generated_charts/

The FastAPI application exposes this directory through:

    /charts

The Node.js Backend retrieves generated charts from the Data Agent and proxies them through the main Backend API before they are rendered by the React frontend.

Chart generation consumes deterministic analytical results rather than performing independent business calculations.

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

The service interprets the analytical request and delegates supported calculations to `DuckDBAnalysisRepository`. It does not initialize, reload or rebuild the analytical database.

Database preparation is a separate pre-worker operation automatically orchestrated by the normal service launcher. The launcher completes preparation before Uvicorn creates the configured workers, and each worker then validates that the DuckDB analytical dataset already exists and is ready before accepting analytical traffic.

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

The current settings and startup environment include configuration for:

- service identity and environment;
- project paths;
- source dataset path;
- DuckDB database path;
- generated-chart directory;
- chart retention;
- chart cleanup interval;
- Data Agent worker count through `DATA_AGENT_WORKERS`.

Default service values include:

    service_name = maranello-ai-data-agent
    environment = development

The default source dataset resolves to:

    data/manufacturing_quality_data.csv

The default generated DuckDB database resolves to:

    data/manufacturing_quality.duckdb

Generated charts resolve to:

    data_agent/generated_charts/

Default chart lifecycle values are:

    chart_retention_hours = 24.0
    chart_cleanup_interval_minutes = 60.0

The standard local project setup uses one Data Agent worker by default. The root `.env.example` exposes:

    DATA_AGENT_WORKERS=1

Set this value to a positive integer when multiple local worker processes are required. The launcher validates the value before database preparation and worker startup.

---

# Requirements

The package requires:

    Python >= 3.12

Runtime dependencies declared in `pyproject.toml` include:

- FastAPI;
- Uvicorn;
- Pandas;
- DuckDB;
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

From the `data_agent` directory, with the Python environment activated, start the service through the automated launcher:

    python -m app.commands.start_data_agent

The launcher performs the startup sequence deterministically:

    1. validate the configured worker count;
    2. load and clean the source CSV;
    3. materialize the prepared dataset into DuckDB;
    4. verify that preparation completed successfully;
    5. invoke Uvicorn only after the writer phase has finished;
    6. start the configured FastAPI worker processes.

The default worker count is one. To run multiple workers, set `DATA_AGENT_WORKERS` to a positive integer, for example:

    DATA_AGENT_WORKERS=3 python -m app.commands.start_data_agent

Preparation still runs exactly once in the launcher process before Uvicorn is invoked. Individual workers never initialize or rebuild the database; they perform only a read-only readiness check before accepting analytical traffic.

If preparation fails, Uvicorn is not started and therefore no worker process is created.

For maintenance or an explicit database rebuild without starting the service, the preparation command remains available separately:

    python -m app.commands.prepare_database

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

    python -m ruff check data_agent/app data_agent/tests

Then run:

    cd data_agent
    python -m pytest tests
    cd ..

The DuckDB implementation and automated startup lifecycle include coverage for areas including:

- dataset loading;
- deterministic cleaning;
- question interpretation;
- DuckDB dataset creation and refresh;
- DuckDB schema and prepared-data persistence;
- global KPI analysis;
- grouped analysis;
- monthly analysis;
- null handling and analytical edge cases;
- unsupported analytical dimensions;
- chart generation;
- API integration;
- real-dataset behavior;
- `ChartCleanupService`;
- managed chart retention;
- FastAPI startup cleanup;
- periodic cleanup;
- graceful cleanup-task cancellation during shutdown;
- worker-count validation;
- exactly-once preparation before multi-worker startup;
- prevention of worker startup when preparation fails;
- concurrent read-only access from multiple isolated worker processes to a prepared temporary DuckDB database.

The complete Data Agent suite currently contains 91 passing automated tests.

The installed FastAPI/Starlette testing dependency stack may also report a `StarletteDeprecationWarning` related to its test-client implementation. This warning does not represent a failing project test or an application runtime error.

---

# Scalability

The current implementation uses DuckDB as an embedded analytical query engine.

This is an intentional architectural improvement over using a prepared Pandas DataFrame as the primary analytical runtime.

For the current synthetic dataset of approximately 2,000 rows, either approach would be computationally sufficient. DuckDB was introduced primarily to establish a more scalable and query-oriented data-access boundary rather than because the current dataset requires database-scale performance.

The current architecture allows:

- persistent local storage of the prepared analytical dataset;
- SQL-based filtering and aggregation;
- analytical work to remain outside the conversational Backend;
- deterministic and testable queries;
- the source CSV to remain the reproducible project source;
- the analytical database to be regenerated as a local runtime artifact;
- future dataset growth without coupling business analysis directly to an in-memory DataFrame cache.

Conceptually:

    Source CSV
        ↓
    Deterministic preparation
        ↓
    DuckDB
        ↓
    Controlled analytical SQL
        ↓
    Structured analytical results

For larger production deployments, further evolution could include:

- Parquet or other columnar source formats;
- externally managed analytical databases;
- cloud data warehouses or lakehouse platforms;
- distributed storage and compute;
- scheduled or event-driven ingestion pipelines.

DuckDB remains an embedded single-process analytical engine in the current project. It is not presented as a substitute for every production-scale database architecture.

The deterministic analytical contract of the Data Agent can remain stable even if the underlying storage implementation evolves further.

---

# Scope Boundaries

The current Data Agent is designed for the educational, portfolio and local integration scope of Maranello AI.

It intentionally does not implement:

- arbitrary execution of LLM-generated Python code;
- arbitrary user-provided SQL execution;
- a remote production database;
- distributed background-job infrastructure;
- persistent chart object storage;
- horizontal scaling coordination;
- production authentication or authorization.

DuckDB is implemented as the local embedded analytical data layer.

The generated DuckDB database is a runtime artifact and is not committed to the repository.

More advanced distributed or externally managed data platforms remain possible production-scale extensions rather than incomplete requirements of the current implementation.

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
    DuckDB-backed Deterministic Manufacturing Analysis

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

The Python Data Agent remains focused on deterministic manufacturing analytics, local analytical-data management and chart lifecycle management.

---

# Project Context

Maranello AI is a fictional enterprise-style manufacturing assistant created as an educational and portfolio project.

The Manufacturing Dataset, Knowledge Base and operational policies included in the repository are synthetic or project-authored materials.

They must not be interpreted as confidential, internal or operational data belonging to Ferrari or any other real automotive manufacturer.

For complete installation, architecture, API, testing and delivery documentation, refer to the root project README and the documents under:

    docs/
