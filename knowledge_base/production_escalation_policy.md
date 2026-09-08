# Production Escalation Policy

> **Document ID:** PEP-001  
> **Version:** 1.0  
> **Owner:** Quality & Manufacturing Operations  
> **Classification:** Internal  
> **Effective Date:** 2025-01-01  
> **Review Cycle:** Annual  
> **Status:** Active

---

## 1. Purpose

This policy defines the escalation framework used to manage significant manufacturing, quality, supplier, and production-line events.

The objective is to ensure that abnormal conditions are escalated consistently according to their severity, operational impact, recurrence, and potential risk.

The policy establishes escalation levels, triggering conditions, responsibilities, notification requirements, and criteria for returning to normal operations.

---

## 2. Scope

This policy applies to events associated with:

- manufacturing quality;
- production-line performance;
- production downtime;
- non-conforming batches;
- rework and scrap;
- supplier-related quality issues;
- recurring manufacturing problems;
- safety-critical defects;
- abnormal quality KPI performance.

It applies to all production lines, shifts, vehicle models, manufacturing teams, and suppliers included within the Quality & Manufacturing Operations scope.

---

## 3. Escalation Principles

Production escalation shall follow these principles:

1. escalation must be proportional to the severity and potential impact of the event;
2. product quality and safety take priority over production continuity;
3. Critical conditions require timely management visibility;
4. repeated Warning conditions may justify escalation even when individual events remain below Critical thresholds;
5. operational decisions must be based on validated information;
6. containment does not replace root-cause analysis;
7. escalation decisions and actions must remain traceable;
8. production may return to normal operation only after applicable risks have been adequately controlled.

---

## 4. Escalation Levels

Maranello AI Quality & Manufacturing Operations uses three operational escalation levels.

| Level | Classification | Description |
|---|---|---|
| Level 1 | Attention | Local deviation requiring increased monitoring or operational review. |
| Level 2 | Significant | Confirmed quality or operational issue requiring structured investigation and cross-functional involvement. |
| Level 3 | Critical | Severe condition requiring immediate containment, management notification, and formal escalation. |

The escalation level should reflect the most severe applicable condition.

---

## 5. Level 1 — Attention

Level 1 applies when a deviation requires additional monitoring but does not represent an immediate significant manufacturing risk.

Typical Level 1 triggers include:

- Defect Rate above 2.0% and up to 3.5%;
- Rework Rate above 1.5% and up to 3.0%;
- Scrap Rate above 0.5% and up to 1.0%;
- Quality Score between 85 and below 90;
- production-line downtime above 45 and up to 90 minutes;
- isolated non-critical quality deviation;
- emerging negative trend requiring observation.

### Required Actions

Level 1 actions may include:

- notify the responsible Quality Engineer;
- increase monitoring;
- review subsequent production;
- evaluate the dominant defect category;
- verify production conditions;
- document relevant observations.

Production may normally continue unless additional evidence indicates greater risk.

---

## 6. Level 2 — Significant

Level 2 applies when a confirmed manufacturing or quality issue requires structured investigation or coordinated action.

Typical Level 2 triggers include:

- repeated Level 1 conditions;
- three consecutive Warning periods for the same relevant KPI;
- recurring non-conformities;
- formal supplier quality review;
- repeated abnormal rework;
- significant scrap pattern;
- failed corrective action;
- repeated production disruption;
- a Major non-conformity.

### Required Actions

Level 2 requires:

1. notification of the Quality Engineer;
2. notification of the Manufacturing Supervisor;
3. documented containment where appropriate;
4. structured investigation;
5. assignment of responsible stakeholders;
6. root-cause analysis where required;
7. definition of corrective actions;
8. verification of corrective-action effectiveness.

The Quality Manager should be informed when the event has significant cross-functional impact.

---

## 7. Level 3 — Critical

Level 3 represents the highest escalation level.

It applies when a condition may create significant product, customer, safety, manufacturing, or business risk.

Typical Level 3 triggers include:

- Defect Rate above 3.5%;
- Rework Rate above 3.0%;
- Scrap Rate above 1.0%;
- Quality Score below 85;
- production-line downtime above 90 minutes when operationally significant;
- production-line downtime above 180 minutes;
- safety-critical defect;
- Critical non-conformity;
- Supplier Defect Rate above 4.0% over a validated monitoring period;
- repeated unresolved Major non-conformities;
- confirmed loss of manufacturing process control;
- ineffective corrective actions associated with significant risk.

### Required Actions

Level 3 requires:

1. immediate Quality notification;
2. immediate Manufacturing Operations notification;
3. Quality Manager notification;
4. containment of affected production where applicable;
5. identification and isolation of affected batches;
6. formal investigation;
7. root-cause analysis;
8. documented corrective actions;
9. verification before return to normal operation.

Additional management or supplier involvement may be required depending on the event.

---

## 8. Production Hold

A production hold may be required when continued production could increase quality, safety, or operational risk.

Conditions that may justify a production hold include:

- safety-critical defects;
- confirmed severe loss of process control;
- inability to determine the extent of affected production;
- repeated Critical defects;
- ineffective containment;
- inability to verify product conformity.

A Critical KPI threshold alone does not automatically require a complete production shutdown.

The Quality and Manufacturing teams must evaluate the specific risk and determine the appropriate containment response.

---

## 9. Downtime Escalation

Production-line downtime is classified as follows:

| Downtime | Classification | Escalation |
|---|---|---|
| `<= 45 minutes` | Normal | No escalation required. |
| `> 45 and <= 90 minutes` | Warning | Level 1 operational review. |
| `> 90 and <= 180 minutes` | Critical | Level 3 escalation when validated and operationally significant. |
| `> 180 minutes` | Severe Critical | Immediate Level 3 escalation and management notification. |

Before escalation, implausible downtime values must be checked for potential data-quality errors.

For example, an unusually large recorded downtime value should not automatically trigger operational action if the underlying record is demonstrably invalid.

---

## 10. Quality KPI Escalation Matrix

| KPI | Normal | Warning | Critical |
|---|---|---|---|
| Defect Rate | `<= 2.0%` | `> 2.0% and <= 3.5%` | `> 3.5%` |
| Rework Rate | `<= 1.5%` | `> 1.5% and <= 3.0%` | `> 3.0%` |
| Scrap Rate | `<= 0.5%` | `> 0.5% and <= 1.0%` | `> 1.0%` |
| Quality Score | `>= 90` | `>= 85 and < 90` | `< 85` |
| Downtime | `<= 45 min` | `> 45 and <= 90 min` | `> 90 min` |

The Manufacturing Quality Policy remains the authoritative source for KPI definitions and detailed quality requirements.

---

## 11. Recurring Warning Conditions

Repeated Warning conditions must not be treated indefinitely as isolated events.

Escalation to Level 2 is required when:

- the same KPI remains in Warning status for three consecutive monitored periods;
- the same significant defect category repeatedly affects the same production scope;
- the same production line repeatedly enters Warning status;
- corrective actions do not produce sustained improvement.

Recurring Warning conditions may be escalated to Level 3 when evidence indicates increasing severity or loss of process control.

---

## 12. Supplier Escalation

Supplier-related escalation must consider both manufacturing impact and supplier performance.

Level 2 supplier escalation may be appropriate when:

- Supplier Defect Rate enters Warning status;
- recurring supplier-related defects are identified;
- formal supplier quality review is required;
- supplier corrective actions are ineffective.

Level 3 supplier escalation is required when:

- Supplier Defect Rate exceeds 4.0% over a validated monitoring period;
- a supplied safety-critical component presents a confirmed quality issue;
- supplier-related defects create significant production or customer risk;
- repeated supplier corrective actions fail.

Detailed supplier requirements are defined in the Supplier Quality Procedure.

---

## 13. Non-Conformity Escalation

Confirmed non-conformities must be escalated according to their classification.

### Minor Non-Conformity

Normally managed locally unless recurrence indicates a systemic issue.

### Major Non-Conformity

Normally requires Level 2 escalation.

### Critical Non-Conformity

Requires Level 3 escalation.

The Non-Conformity Management Procedure defines the detailed investigation and closure process.

---

## 14. Data Validation Before Escalation

Automated or analytical escalation decisions must use validated data.

Before using a KPI as the basis for escalation, relevant data should be evaluated for:

- duplicates;
- missing values;
- invalid quantities;
- inconsistent categories;
- inconsistent dates;
- extreme outliers;
- logical inconsistencies.

For example:

```text
units_produced = 70
defective_units = 78
```

must not be interpreted as a valid Critical Defect Rate.

The record must first be investigated as a potential data-quality problem.

When uncertainty remains, Maranello AI should identify the condition as requiring data validation rather than automatically presenting it as a confirmed operational escalation.

---

## 15. Escalation Communication

An escalation communication should contain sufficient information for stakeholders to understand the event.

Where available, it should include:

- affected production scope;
- relevant production line;
- affected batch or batches;
- date or monitoring period;
- relevant KPI;
- measured value;
- applicable threshold;
- defect category;
- supplier or component association;
- escalation level;
- immediate containment;
- responsible stakeholders;
- next required action.

---

## 16. Responsibilities

### Quality Engineer

Responsible for:

- validating quality-related escalation triggers;
- evaluating affected production;
- initiating non-conformity activities where required;
- supporting investigation and corrective actions.

### Manufacturing Supervisor

Responsible for:

- coordinating operational response;
- implementing containment;
- controlling affected production;
- supporting investigation.

### Supplier Quality Engineer

Responsible for:

- managing supplier-related escalation;
- coordinating supplier containment and corrective actions;
- monitoring supplier recovery.

### Quality Manager

Responsible for:

- reviewing Level 3 quality events;
- coordinating significant cross-functional escalation;
- approving major quality decisions where required;
- ensuring appropriate follow-up.

---

## 17. Return to Normal Operation

An escalated condition may return to normal monitoring only when applicable requirements have been satisfied.

Depending on severity, this may require:

- successful containment;
- validated production data;
- completed investigation;
- implemented corrective actions;
- verified effectiveness;
- acceptable subsequent production;
- appropriate Quality approval.

A temporary improvement in one production batch is not necessarily sufficient to close a recurring or Critical issue.

---

## 18. Use of Maranello AI

Maranello AI may support escalation management by:

- calculating manufacturing KPIs;
- identifying values exceeding documented thresholds;
- detecting recurring patterns;
- analyzing historical production performance;
- retrieving applicable escalation rules;
- identifying potentially affected suppliers, lines, shifts, or components;
- generating evidence-based escalation summaries.

For example:

```text
User question:
"What was the defect rate for Line 3 last month,
and does it require escalation?"
```

Maranello AI may:

1. use the Data Agent to clean and analyze the production dataset;
2. calculate the validated Defect Rate for Line 3;
3. use the RAG system to retrieve the applicable threshold;
4. compare the calculated result with this policy;
5. explain the applicable escalation level and required action.

Maranello AI provides decision support and must not independently authorize:

- production shutdown;
- production restart;
- release of isolated batches;
- closure of Critical non-conformities;
- final safety-critical decisions.

---

## 19. Escalation Example

Consider a validated monthly analysis with the following result:

```text
Production Line: Line 3
Defect Rate: 3.8%
```

The Manufacturing Quality Policy defines a Defect Rate above 3.5% as Critical.

According to this Production Escalation Policy, the condition therefore requires Level 3 escalation.

The expected response includes:

- Quality notification;
- Manufacturing Operations notification;
- Quality Manager notification;
- evaluation of affected production;
- appropriate containment;
- formal investigation;
- corrective-action planning.

The analytical result alone does not determine whether a complete production shutdown is necessary.

That decision requires evaluation of the specific operational and quality risk.

---

## 20. Related Documents

This policy should be interpreted together with:

- Manufacturing Quality Policy;
- Non-Conformity Management Procedure;
- Supplier Quality Procedure;
- Rework and Scrap Procedure.

---

## 21. Document Control

| Field | Value |
|---|---|
| Document ID | PEP-001 |
| Version | 1.0 |
| Owner | Quality & Manufacturing Operations |
| Classification | Internal |
| Effective Date | 2025-01-01 |
| Review Cycle | Annual |
| Status | Active |