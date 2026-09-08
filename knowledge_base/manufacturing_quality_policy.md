# Manufacturing Quality Policy

> **Document ID:** MQP-001  
> **Version:** 1.0  
> **Owner:** Quality & Manufacturing Operations  
> **Classification:** Internal  
> **Effective Date:** 2025-01-01  
> **Review Cycle:** Annual  
> **Status:** Active

---

## 1. Purpose

This policy defines the quality standards, performance thresholds, monitoring requirements, and escalation criteria applicable to manufacturing operations.

The purpose of the policy is to ensure that production quality is continuously monitored and that deviations from expected performance are identified, investigated, and addressed consistently.

This policy applies to all production lines, shifts, vehicle models, manufacturing teams, and production batches included within the Quality & Manufacturing Operations scope.

---

## 2. Quality Principles

Manufacturing operations shall follow the following principles:

1. product quality takes priority over production volume;
2. quality deviations must be identified as early as possible;
3. production data must be reviewed using consistent quality indicators;
4. significant deviations require documented investigation;
5. repeated quality issues require escalation even when individual observations remain below critical thresholds;
6. decisions affecting product conformity must be traceable;
7. production shall not continue without review when critical quality conditions are identified.

---

## 3. Core Quality Indicators

The following indicators are used to monitor manufacturing quality:

- Defect Rate;
- Rework Rate;
- Scrap Rate;
- Quality Score;
- production-line downtime;
- recurring defect categories;
- supplier-related quality performance.

These indicators may be evaluated at batch, production-line, shift, vehicle-model, supplier, or time-period level.

---

## 4. Defect Rate

### 4.1 Definition

The Defect Rate represents the percentage of produced units identified as defective.

It is calculated as:

```text
Defect Rate (%) =
(defective_units / units_produced) × 100
```

### 4.2 Defect Rate Thresholds

The following thresholds apply:

| Defect Rate | Classification | Required Action |
|---|---|---|
| `<= 2.0%` | Normal | Continue standard monitoring. |
| `> 2.0% and <= 3.5%` | Warning | Perform quality review and monitor subsequent production. |
| `> 3.5%` | Critical | Initiate formal escalation and non-conformity assessment. |

A Critical classification does not automatically require permanent production shutdown.

The responsible Quality team must evaluate the affected batch, defect severity, recurrence, and potential customer impact before determining the appropriate operational response.

---

## 5. Rework Rate

### 5.1 Definition

The Rework Rate represents the percentage of produced units requiring corrective manufacturing operations before they can be accepted.

It is calculated as:

```text
Rework Rate (%) =
(rework_units / units_produced) × 100
```

### 5.2 Rework Thresholds

| Rework Rate | Classification | Required Action |
|---|---|---|
| `<= 1.5%` | Normal | Standard monitoring. |
| `> 1.5% and <= 3.0%` | Warning | Review the dominant defect category and production conditions. |
| `> 3.0%` | Critical | Initiate root-cause analysis and quality escalation. |

Repeated Warning classifications for the same production line during three consecutive monitored periods must be treated as a Critical condition.

---

## 6. Scrap Rate

### 6.1 Definition

The Scrap Rate represents the percentage of produced units that cannot be recovered through approved rework activities.

It is calculated as:

```text
Scrap Rate (%) =
(scrap_units / units_produced) × 100
```

### 6.2 Scrap Thresholds

| Scrap Rate | Classification | Required Action |
|---|---|---|
| `<= 0.5%` | Normal | Standard monitoring. |
| `> 0.5% and <= 1.0%` | Warning | Review scrap causes and affected components. |
| `> 1.0%` | Critical | Initiate quality escalation and documented investigation. |

Scrap associated with safety-critical components must be reviewed regardless of the overall Scrap Rate.

---

## 7. Quality Score

### 7.1 Definition

The Quality Score is an internal manufacturing quality indicator expressed on a scale from 0 to 100.

Higher values represent stronger overall quality performance.

### 7.2 Quality Score Thresholds

| Quality Score | Classification | Required Action |
|---|---|---|
| `>= 95` | Target | No corrective action required. |
| `>= 90 and < 95` | Acceptable | Continue monitoring. |
| `>= 85 and < 90` | Warning | Perform quality review. |
| `< 85` | Critical | Initiate formal investigation and escalation. |

A missing or invalid Quality Score must not be interpreted as acceptable performance.

The underlying data must be validated before a quality decision is made.

---

## 8. Production-Line Downtime

Production downtime is monitored as both an operational and quality-related indicator.

The following thresholds apply to downtime associated with a production batch:

| Downtime | Classification | Required Action |
|---|---|---|
| `<= 45 minutes` | Normal | Standard monitoring. |
| `> 45 and <= 90 minutes` | Warning | Review operational cause. |
| `> 90 minutes` | Critical | Escalate to Manufacturing Operations and investigate the cause. |

Downtime greater than 180 minutes requires immediate management notification.

Extreme or implausible downtime values must first be validated to exclude data-quality issues before operational conclusions are drawn.

---

## 9. Recurring Quality Issues

A quality issue must be considered recurring when the same significant defect pattern appears repeatedly within the same:

- production line;
- supplier;
- component category;
- vehicle model;
- or production shift.

Repeated Warning conditions may require escalation even if no individual observation exceeds a Critical threshold.

The Quality team must evaluate both the severity and frequency of the observed issue.

---

## 10. Supplier-Related Quality Monitoring

Supplier performance must be monitored when manufacturing defects can reasonably be associated with externally supplied components.

Supplier-related analysis should consider:

- defect frequency;
- defect rate;
- affected component category;
- recurrence over time;
- scrap generated;
- rework generated;
- severity of the detected defects.

A supplier must not be classified as non-compliant solely on the basis of one isolated batch unless the issue involves a safety-critical or otherwise severe defect.

Detailed supplier escalation requirements are defined in the Supplier Quality Procedure.

---

## 11. Data Quality Requirements

Quality decisions must be based on validated production data.

Before calculating or interpreting manufacturing KPIs, analysts and automated systems must evaluate relevant data for:

- missing values;
- duplicate records;
- inconsistent categories;
- invalid numerical ranges;
- inconsistent date formats;
- abnormal outliers;
- logical inconsistencies between related fields.

Examples of logically invalid records include:

```text
defective_units > units_produced
quality_score > 100
```

Records containing significant data-quality issues must be corrected, excluded, or explicitly flagged before being used for operational decisions.

Automated cleaning must not silently modify data when the correct value cannot be determined with reasonable confidence.

---

## 12. Quality Escalation

A formal quality escalation must be initiated when one or more of the following conditions occur:

- Defect Rate exceeds 3.5%;
- Rework Rate exceeds 3.0%;
- Scrap Rate exceeds 1.0%;
- Quality Score is below 85;
- production-line downtime exceeds 90 minutes;
- repeated Warning conditions indicate a persistent quality problem;
- a safety-critical defect is identified;
- a significant supplier-related quality issue is detected.

The escalation must identify:

1. the affected production scope;
2. the relevant KPI or quality issue;
3. available supporting evidence;
4. immediate containment actions;
5. responsible stakeholders;
6. required follow-up activities.

Detailed operational escalation rules are defined in the Production Escalation Policy.

---

## 13. Responsibilities

### Quality Engineer

Responsible for:

- reviewing quality deviations;
- validating quality indicators;
- initiating non-conformity assessments;
- supporting root-cause analysis;
- documenting quality decisions.

### Manufacturing Supervisor

Responsible for:

- monitoring production conditions;
- coordinating operational containment;
- supporting investigations;
- implementing approved corrective actions.

### Supplier Quality Engineer

Responsible for:

- investigating supplier-related issues;
- evaluating supplier performance;
- coordinating supplier corrective actions;
- escalating recurring supplier quality problems.

### Quality Manager

Responsible for:

- reviewing Critical quality conditions;
- approving major quality decisions;
- coordinating cross-functional escalations;
- ensuring compliance with internal quality procedures.

---

## 14. Use of Automated Analytical Systems

Automated analytical systems, including Maranello AI, may support quality monitoring and decision-making by:

- calculating manufacturing KPIs;
- identifying trends and anomalies;
- retrieving applicable internal policies;
- highlighting conditions requiring review;
- generating analytical summaries.

Automated systems provide decision support and do not replace required human approval for critical manufacturing or quality decisions.

When data quality is insufficient, the system should explicitly communicate the limitation rather than present uncertain results as verified facts.

---

## 15. Related Documents

This policy should be interpreted together with:

- Non-Conformity Management Procedure;
- Supplier Quality Procedure;
- Rework and Scrap Procedure;
- Production Escalation Policy.

---

## 16. Document Control

| Field | Value |
|---|---|
| Document ID | MQP-001 |
| Version | 1.0 |
| Owner | Quality & Manufacturing Operations |
| Classification | Internal |
| Effective Date | 2025-01-01 |
| Review Cycle | Annual |
| Status | Active |