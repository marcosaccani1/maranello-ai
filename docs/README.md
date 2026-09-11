# Maranello AI Documentation

This directory contains the technical documentation for **Maranello AI**, an Enterprise Hybrid AI Assistant designed for a fictional premium automotive manufacturing scenario.

The documentation describes the project from business requirements and system architecture through data design, API contracts and final verification.

The current as-built documentation is maintained in Italian under:

    docs/it/

All documents reflect the final implemented architecture rather than the initial project prototype.

---

# Documentation Set

| Document | Description | Status |
|----------|-------------|--------|
| [01 — Project Vision and Scope](it/01_Project_Vision_and_Scope.md) | Business context, project objectives, stakeholders, scope, constraints and success criteria | Final |
| [02 — Software Requirements Specification](it/02_Software_Requirements_Specification.md) | Functional and non-functional requirements, business rules, use cases and acceptance criteria | Final |
| [03 — System Architecture](it/03_System_Architecture.md) | Final as-built architecture, components, orchestration flow and architectural decisions | Final |
| [04 — Data Model](it/04_Data_Model.md) | Manufacturing Dataset, Knowledge Base, conversation structures and application data models | Final |
| [05 — API Specification](it/05_API_Specification.md) | REST API contracts and communication between application services | Final |
| [06 — Test Plan](it/06_Test_Plan.md) | Testing strategy, automated verification, manual QA and final validation evidence | Final |

---

# Documentation Map

The documentation follows the logical progression of the project:

    Why does the system exist?
            ↓
    01 — Project Vision and Scope

    What must the system do?
            ↓
    02 — Software Requirements Specification

    How is the system structured?
            ↓
    03 — System Architecture

    How is information represented?
            ↓
    04 — Data Model

    How do the services communicate?
            ↓
    05 — API Specification

    How was the system verified?
            ↓
    06 — Test Plan

Together, these documents provide traceability from the original business problem to the final implemented and validated system.

---

# Final Architecture Covered by the Documentation

The documentation describes the final Maranello AI architecture:

    React Frontend
          ↓
    Node.js / Express Backend
          ↓
    OpenAI Responses API
          ↓
    Native Function Calling
       /              \
      ▼                ▼
    RAG            Python Data Agent
      │                │
      ▼                ▼
    ChromaDB        Pandas / Matplotlib
      │                │
      ▼                ▼
    Knowledge       Manufacturing
    Base            Dataset

The Backend autonomously orchestrates four possible execution patterns:

- Direct conversational response;
- Retrieval-Augmented Generation;
- structured manufacturing data analysis;
- Hybrid execution combining RAG and data analysis.

The documentation also covers:

- Italian and English conversational interaction;
- cross-language semantic retrieval;
- deterministic analytical execution;
- conversation state;
- native chart rendering;
- controlled dependency failures;
- automated testing;
- manual end-to-end QA;
- security and architectural boundaries.

---

# Documentation Language

The current final technical documentation is maintained in **Italian**.

The root project README is maintained in **English** to provide a portfolio-friendly public overview of the project, its architecture, installation procedure and engineering decisions.

An English version of the complete technical documentation may be introduced as a future enhancement, but it is not required by the current project scope.

---

# Documentation Status

The six primary technical documents are aligned with the final as-built implementation.

Current documentation status:

    Project Vision and Scope                Final
    Software Requirements Specification     Final
    System Architecture                     Final
    Data Model                              Final
    API Specification                       Final
    Test Plan                               Final

The remaining project-delivery activities are handled separately from the technical documentation and include:

- final presentation preparation;
- clean-clone verification;
- final repository and delivery packaging.

---

# Project Entry Point

For the complete project overview, installation instructions, runtime procedure, architecture summary and example use cases, return to the root:

    ../README.md