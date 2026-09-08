# Maranello AI Knowledge Base

## Overview

This directory contains the fictional internal documentation used by the Retrieval-Augmented Generation (RAG) component of Maranello AI.

The Knowledge Base represents the qualitative information available to employees working in the Quality & Manufacturing Operations domain of a fictional premium automotive manufacturer.

The documents are designed to complement the quantitative information contained in the manufacturing dataset located in:

```text
data/manufacturing_quality_data.csv
```

While the dataset describes what happened during manufacturing operations, the Knowledge Base defines the policies, procedures, thresholds, responsibilities, and escalation rules required to interpret those events.

---

## Purpose

The Knowledge Base enables Maranello AI to answer questions related to internal manufacturing and quality procedures without relying on the general knowledge of the Large Language Model.

The RAG system will retrieve relevant sections from these documents and provide them as contextual evidence to the AI orchestrator.

The Knowledge Base supports questions such as:

- What is the maximum acceptable defect rate?
- When must a production line be escalated?
- How should a non-conforming batch be handled?
- When is supplier quality review required?
- What are the rules for rework and scrap?
- Which actions are required when quality KPIs exceed their thresholds?

---

## Knowledge Base Documents

The Knowledge Base is organized into the following documents.

### Manufacturing Quality Policy

```text
manufacturing_quality_policy.md
```

Defines:

- manufacturing quality objectives;
- defect-rate thresholds;
- quality-score requirements;
- KPI classification levels;
- monitoring responsibilities.

### Non-Conformity Management Procedure

```text
non_conformity_procedure.md
```

Defines:

- identification of non-conforming batches;
- containment procedures;
- investigation requirements;
- corrective actions;
- closure criteria.

### Supplier Quality Procedure

```text
supplier_quality_procedure.md
```

Defines:

- supplier quality monitoring;
- supplier performance thresholds;
- supplier review criteria;
- escalation requirements;
- corrective-action expectations.

### Rework and Scrap Procedure

```text
rework_and_scrap_procedure.md
```

Defines:

- conditions for rework;
- scrap authorization;
- traceability requirements;
- quality verification after rework;
- escalation thresholds.

### Production Escalation Policy

```text
production_escalation_policy.md
```

Defines:

- operational escalation levels;
- production-line intervention criteria;
- downtime thresholds;
- quality escalation conditions;
- responsibilities during critical manufacturing events.

---

## Relationship with Structured Data

The Knowledge Base intentionally does not contain production observations or historical KPI values.

Those values are stored in the manufacturing dataset and analyzed by the Python Data Agent.

This separation allows Maranello AI to distinguish between:

```text
"What happened?"
        ↓
Structured Data / Data Agent
```

and:

```text
"What should happen according to company policy?"
        ↓
Knowledge Base / RAG
```

Some questions require both sources.

For example:

```text
"Line 3 had a defect rate of 4.2% last month.
According to company policy, what action should be taken?"
```

The system must:

1. use the Data Agent to calculate or verify the actual defect rate;
2. use the RAG system to retrieve the applicable quality threshold;
3. combine both results;
4. explain the required action to the user.

---

## Document Design

The documents contained in this Knowledge Base are intentionally structured using clear headings and relatively self-contained sections.

This structure supports the future RAG ingestion pipeline by enabling documents to be divided into meaningful chunks while preserving the context required for semantic retrieval.

Documents may include metadata such as:

- document identifier;
- version;
- owner;
- effective date;
- classification;
- review cycle.

These metadata can later be stored alongside document chunks in ChromaDB and returned as source information during retrieval.

---

## Source Attribution

The RAG system should preserve source metadata during document ingestion.

Retrieved information should allow the final response to identify the document used as evidence.

A future retrieval result may therefore contain information such as:

```text
Document: Manufacturing Quality Policy
Section: Defect Rate Thresholds
Version: 1.0
```

This improves:

- traceability;
- explainability;
- debugging;
- user confidence;
- verification of AI-generated responses.

---

## Language

The initial Knowledge Base is maintained in English.

Maranello AI is designed to accept questions in both Italian and English.

The language used by the user does not determine the language of the underlying source document.

The AI layer is responsible for interpreting the retrieved context and producing the final answer in the same language used by the user.

For example:

```text
User:
"Qual è il limite massimo accettabile per il defect rate?"

Knowledge Base:
English documentation

Assistant:
Italian response with source attribution
```

---

## Scope

The Knowledge Base is limited to fictional internal information relevant to Quality & Manufacturing Operations.

The initial scope includes:

- manufacturing quality;
- non-conformity management;
- supplier quality;
- rework and scrap;
- production escalation.

Topics outside this scope should not be presented as if they were supported by internal documentation.

---

## Disclaimer

All documents contained in this Knowledge Base are fictional and have been created exclusively for educational, demonstration, and portfolio purposes.

They do not represent actual policies, procedures, thresholds, operational practices, or confidential information belonging to Ferrari N.V. or any other automotive manufacturer.