# Rework and Scrap Procedure

> **Document ID:** RSP-001  
> **Version:** 1.0  
> **Owner:** Quality & Manufacturing Operations  
> **Classification:** Internal  
> **Effective Date:** 2025-01-01  
> **Review Cycle:** Annual  
> **Status:** Active

---

## 1. Purpose

This procedure defines the requirements for evaluating, authorizing, performing, verifying, and documenting rework and scrap activities associated with manufacturing quality deviations.

The objective is to ensure that non-conforming units are managed consistently, that reworked products satisfy applicable quality requirements before release, and that scrap decisions remain controlled and traceable.

---

## 2. Scope

This procedure applies to:

- production batches;
- defective manufactured units;
- components requiring corrective processing;
- units undergoing rework;
- units classified as scrap;
- supplier-related defective components;
- quality deviations identified during inspection.

The procedure applies to all manufacturing operations within the Quality & Manufacturing Operations scope.

---

## 3. Definitions

### Rework

Rework is an approved manufacturing activity performed on a non-conforming unit with the objective of restoring it to applicable quality requirements.

A reworked unit must satisfy the same applicable acceptance requirements as a unit that did not require rework.

### Scrap

Scrap is the controlled disposition of a unit or component that cannot be economically, technically, or safely restored to applicable quality requirements through an approved rework process.

Scrapped units must not return to normal production flow.

---

## 4. Rework Principles

Rework activities shall follow these principles:

1. rework must be technically appropriate for the identified defect;
2. rework must not introduce additional uncontrolled quality risks;
3. affected units must remain traceable;
4. reworked units require verification before acceptance;
5. repeated rework patterns require investigation;
6. rework must not be used to conceal recurring manufacturing problems;
7. safety-critical characteristics require appropriate quality approval.

---

## 5. Rework Rate

### 5.1 Definition

The Rework Rate represents the percentage of produced units requiring approved corrective manufacturing operations.

It is calculated as:

```text
Rework Rate (%) =
(rework_units / units_produced) × 100
```

### 5.2 Rework Rate Thresholds

The following thresholds apply:

| Rework Rate | Classification | Required Action |
|---|---|---|
| `<= 1.5%` | Normal | Continue standard monitoring. |
| `> 1.5% and <= 3.0%` | Warning | Review defect categories and production conditions. |
| `> 3.0%` | Critical | Initiate root-cause analysis and quality escalation. |

These thresholds are consistent with the Manufacturing Quality Policy.

Three consecutive monitored periods classified as Warning for the same production line must be treated as a Critical condition.

---

## 6. Rework Authorization

Rework may be performed only when:

- the affected defect has been identified;
- an appropriate corrective operation exists;
- the rework activity does not create unacceptable additional risk;
- traceability can be maintained;
- required quality verification can be performed.

Rework involving safety-critical characteristics requires explicit Quality approval before the affected unit can be released.

---

## 7. Rework Execution

The rework process should identify:

- affected batch;
- affected unit or component where applicable;
- defect category;
- required corrective activity;
- responsible manufacturing team;
- date of rework;
- verification requirements.

Rework must be performed using approved manufacturing or quality instructions.

Uncontrolled or undocumented rework is not permitted.

---

## 8. Post-Rework Verification

Every reworked unit must undergo appropriate verification before acceptance.

Verification may include:

- visual inspection;
- dimensional inspection;
- functional testing;
- electrical testing;
- process verification;
- additional quality checks appropriate to the defect.

A reworked unit must not be considered acceptable solely because the corrective activity was completed.

Acceptance requires successful verification.

---

## 9. Repeated Rework

Repeated rework associated with the same:

- production line;
- defect category;
- vehicle model;
- component category;
- supplier;
- or production shift

must be evaluated as a potential systemic quality issue.

High rework volume may indicate that the underlying production process is not operating under adequate control.

Correcting individual units does not eliminate the requirement to investigate recurring causes.

---

## 10. Scrap Principles

A unit or component should be evaluated for scrap when:

- approved rework cannot restore conformity;
- rework would introduce unacceptable quality risk;
- repeated rework has failed;
- the component has suffered irreversible damage;
- applicable quality requirements cannot be verified;
- continued use would create a safety or reliability concern.

Scrap decisions must remain traceable.

---

## 11. Scrap Rate

### 11.1 Definition

The Scrap Rate represents the percentage of produced units permanently rejected from normal production flow.

It is calculated as:

```text
Scrap Rate (%) =
(scrap_units / units_produced) × 100
```

### 11.2 Scrap Rate Thresholds

| Scrap Rate | Classification | Required Action |
|---|---|---|
| `<= 0.5%` | Normal | Continue standard monitoring. |
| `> 0.5% and <= 1.0%` | Warning | Review scrap causes and affected components. |
| `> 1.0%` | Critical | Initiate documented investigation and quality escalation. |

Scrap involving safety-critical components requires review regardless of the overall Scrap Rate.

---

## 12. Scrap Authorization

Scrap disposition should identify:

- affected batch;
- affected component or unit where applicable;
- reason for scrap;
- defect category;
- quantity;
- responsible authority;
- required traceability information.

Units designated as scrap must be physically or administratively controlled to prevent unintended return to production.

---

## 13. Relationship Between Defects, Rework, and Scrap

The following logical relationships should normally hold for production data:

```text
rework_units <= defective_units
scrap_units <= defective_units
defective_units <= units_produced
```

Depending on the manufacturing process, rework and scrap classifications may represent different dispositions of defective units.

Analytical systems must validate these relationships before calculating quality KPIs.

Values violating basic production constraints must be treated as potential data-quality issues.

---

## 14. Data Validation

Before performing Rework Rate or Scrap Rate analysis, the underlying data should be evaluated for:

- duplicated batches;
- missing production quantities;
- invalid unit counts;
- negative values;
- inconsistent categories;
- anomalous numerical values.

For example:

```text
units_produced = 80
defective_units = 87
```

is logically invalid and must not be interpreted as an actual Defect Rate without validation.

When reliable correction is not possible, the affected observation should be flagged or excluded from the relevant analysis and the limitation documented.

---

## 15. Trend Analysis

Rework and scrap should be monitored over time rather than evaluated exclusively at individual batch level.

Trend analysis should consider:

- monthly Rework Rate;
- monthly Scrap Rate;
- production-line performance;
- vehicle-model performance;
- component categories;
- defect categories;
- supplier associations;
- production shifts.

A persistent increase may justify investigation even before a Critical threshold is exceeded.

---

## 16. Supplier-Related Rework and Scrap

When rework or scrap appears associated with supplied components, the analysis should consider:

- supplier identifier;
- component category;
- affected production volume;
- defect recurrence;
- total rework;
- total scrap;
- severity.

Significant supplier-related patterns must be evaluated according to the Supplier Quality Procedure.

Statistical association alone does not establish supplier responsibility.

---

## 17. Escalation Requirements

Formal escalation is required when:

- Rework Rate exceeds 3.0%;
- Scrap Rate exceeds 1.0%;
- repeated Warning conditions occur;
- rework repeatedly fails;
- scrap involves safety-critical components;
- significant supplier-related rework or scrap is identified;
- a recurring pattern indicates potential process loss of control.

Escalation must follow the Production Escalation Policy where applicable.

---

## 18. Responsibilities

### Quality Engineer

Responsible for:

- evaluating rework eligibility;
- defining or verifying quality requirements;
- reviewing abnormal rework and scrap trends;
- initiating investigation when required;
- verifying reworked units where applicable.

### Manufacturing Supervisor

Responsible for:

- coordinating approved rework activities;
- maintaining production traceability;
- preventing unauthorized disposition;
- supporting containment and investigation.

### Supplier Quality Engineer

Responsible for:

- evaluating supplier-related rework and scrap;
- coordinating supplier corrective actions where required.

### Quality Manager

Responsible for:

- reviewing Critical rework or scrap conditions;
- approving significant quality dispositions where required;
- supporting escalation decisions.

---

## 19. Use of Maranello AI

Maranello AI may support rework and scrap management by:

- calculating Rework Rate;
- calculating Scrap Rate;
- comparing rates across production lines;
- identifying recurring patterns;
- analyzing trends over time;
- identifying supplier or component associations;
- retrieving applicable rework and scrap requirements;
- highlighting conditions exceeding documented thresholds.

For example, the system may calculate that a production line has a Rework Rate of 3.4% and retrieve this procedure to determine that the condition is classified as Critical.

Maranello AI provides analytical decision support and does not autonomously authorize physical rework, scrap disposition, or release of affected production.

---

## 20. Records and Traceability

Rework and scrap activities should preserve sufficient information to reconstruct:

- what happened;
- which production was affected;
- why the disposition was selected;
- what corrective activity was performed;
- how conformity was verified;
- who authorized the relevant decision.

Traceability must be maintained throughout the lifecycle of the affected production.

---

## 21. Related Documents

This procedure should be interpreted together with:

- Manufacturing Quality Policy;
- Non-Conformity Management Procedure;
- Supplier Quality Procedure;
- Production Escalation Policy.

---

## 22. Document Control

| Field | Value |
|---|---|
| Document ID | RSP-001 |
| Version | 1.0 |
| Owner | Quality & Manufacturing Operations |
| Classification | Internal |
| Effective Date | 2025-01-01 |
| Review Cycle | Annual |
| Status | Active |