# Supplier Quality Procedure

> **Document ID:** SQP-001  
> **Version:** 1.0  
> **Owner:** Supplier Quality & Manufacturing Operations  
> **Classification:** Internal  
> **Effective Date:** 2025-01-01  
> **Review Cycle:** Annual  
> **Status:** Active

---

## 1. Purpose

This procedure defines the requirements for monitoring, evaluating, investigating, and escalating quality issues associated with externally supplied components used in manufacturing operations.

The objective is to ensure that supplier-related quality deviations are identified using reliable evidence and managed consistently according to their severity, recurrence, and operational impact.

---

## 2. Scope

This procedure applies to suppliers and supplied components associated with production batches within the Quality & Manufacturing Operations scope.

Supplier quality evaluation may consider:

- manufacturing defects;
- component-related non-conformities;
- rework;
- scrap;
- recurring defect patterns;
- inspection failures;
- production disruption associated with supplied components.

---

## 3. Supplier Quality Principles

Supplier quality management shall follow these principles:

1. supplier performance must be evaluated using validated data;
2. isolated observations should not automatically result in supplier escalation;
3. recurring quality problems require investigation;
4. defect severity must be considered together with defect frequency;
5. safety-critical issues require immediate review regardless of historical performance;
6. supplier-related conclusions must distinguish correlation from confirmed causation;
7. corrective actions must be documented and their effectiveness verified.

---

## 4. Supplier Performance Indicators

Supplier quality performance should be evaluated using available manufacturing indicators.

Relevant indicators include:

- Defect Rate;
- defective units;
- Rework Rate;
- Scrap Rate;
- recurring defect categories;
- affected component categories;
- failed inspections;
- number of affected production batches;
- persistence of quality issues over time.

No individual KPI should be interpreted without considering the production context and quality of the underlying data.

---

## 5. Supplier Defect Rate

### 5.1 Definition

Supplier Defect Rate represents the percentage of produced units identified as defective within production batches associated with a specific supplier.

It is calculated as:

```text
Supplier Defect Rate (%) =
(total defective units associated with supplier /
 total units produced in associated batches) × 100
```

### 5.2 Performance Thresholds

The following thresholds are used for supplier quality monitoring:

| Supplier Defect Rate | Classification | Required Action |
|---|---|---|
| `<= 2.0%` | Normal | Continue standard monitoring. |
| `> 2.0% and <= 3.0%` | Observation | Review supplier trend and affected component categories. |
| `> 3.0% and <= 4.0%` | Warning | Initiate formal supplier quality review. |
| `> 4.0%` | Critical | Initiate supplier escalation and corrective-action process. |

These thresholds apply to aggregated supplier performance over a meaningful production scope.

An isolated production batch must not automatically determine the overall supplier classification.

---

## 6. Minimum Evidence for Supplier Evaluation

Supplier performance should not be classified using an insufficient sample.

Before assigning a Warning or Critical classification based on aggregated performance, the Supplier Quality Engineer should consider:

- number of associated batches;
- total production volume;
- affected component categories;
- observation period;
- recurrence of defects.

When the available evidence is insufficient, the result should be reported as requiring additional monitoring rather than as a confirmed supplier performance issue.

---

## 7. Recurring Supplier Issues

A supplier-related issue should be considered recurring when similar quality deviations are observed repeatedly across:

- multiple production batches;
- multiple production dates;
- the same component category;
- different production lines using the same supplied component.

Three or more significant supplier-related quality events within a rolling 30-day period require formal supplier quality review.

Two consecutive monitored periods classified as Warning must also trigger formal supplier review.

---

## 8. Critical Supplier Events

Immediate supplier quality escalation is required when:

- Supplier Defect Rate exceeds 4.0% over a validated monitoring period;
- a safety-critical supplied component fails inspection;
- the same Major non-conformity repeatedly occurs after corrective action;
- supplier-related defects cause significant production disruption;
- supplier-related defects create substantial scrap or rework;
- evidence indicates loss of control in the supplier manufacturing process.

Critical supplier events must be communicated to the Quality Manager and Supplier Quality Engineer.

---

## 9. Supplier Quality Review

A formal supplier quality review should evaluate:

1. the supplier identifier;
2. affected component categories;
3. affected production batches;
4. production volume;
5. defect frequency;
6. defect categories;
7. Defect Rate;
8. Rework Rate;
9. Scrap Rate;
10. historical recurrence;
11. operational impact;
12. available evidence regarding root cause.

The review must distinguish between statistical association and confirmed supplier responsibility.

---

## 10. Supplier Corrective Action Request

When a supplier-related Major or Critical issue is confirmed, a Supplier Corrective Action Request may be initiated.

The request should include:

- description of the problem;
- affected component;
- available supporting evidence;
- affected production scope;
- containment requirements;
- requested root-cause analysis;
- required corrective action;
- response deadline.

Unless otherwise determined by the Supplier Quality Engineer, the supplier should provide an initial containment response within **2 business days** and a documented corrective-action plan within **10 business days**.

---

## 11. Containment Requirements

Supplier-related containment may include:

- isolation of suspected components;
- increased incoming inspection;
- additional production inspection;
- temporary segregation of supplier inventory;
- verification of related batches;
- controlled replacement of affected components.

Containment requirements must be proportional to the severity and potential impact of the issue.

---

## 12. Verification of Corrective Actions

Supplier corrective actions must be verified before the issue is considered resolved.

Verification may include:

- monitoring subsequent batches;
- comparing supplier Defect Rate before and after corrective action;
- reviewing recurrence of the affected defect category;
- evaluating Rework Rate;
- evaluating Scrap Rate;
- performing additional component inspection.

If performance does not improve, the issue must remain open and may require further escalation.

---

## 13. Supplier Performance Recovery

A supplier previously classified as Warning or Critical may return to standard monitoring when:

- required corrective actions have been implemented;
- effectiveness has been verified;
- no unresolved Critical non-conformity remains;
- subsequent production demonstrates acceptable performance;
- the Supplier Quality Engineer approves return to standard monitoring.

A single compliant batch is not sufficient evidence of sustained recovery following a Critical supplier issue.

---

## 14. Data Quality Requirements

Supplier analysis must use validated manufacturing data.

Before calculating supplier performance, the analysis must account for:

- missing supplier identifiers;
- duplicated production records;
- inconsistent supplier identifier formatting;
- invalid production quantities;
- inconsistent component categories;
- abnormal numerical values.

For example:

```text
SUP-07
SUP-07 
```

must be normalized to the same supplier identifier before aggregated performance is calculated.

Records with missing supplier identifiers must not be automatically assigned to a supplier.

---

## 15. Supplier Comparison

When comparing suppliers, the analysis should consider differences in:

- production volume;
- number of associated batches;
- component category;
- production period;
- defect severity.

Ranking suppliers solely by total defective units may produce misleading conclusions when suppliers are associated with substantially different production volumes.

Rate-based metrics should therefore normally be preferred for comparative quality analysis.

---

## 16. Relationship with Non-Conformity Management

When a supplier-related quality issue results in a confirmed manufacturing non-conformity, the Non-Conformity Management Procedure must also be applied.

Supplier quality management does not replace internal containment responsibilities.

The manufacturing organization remains responsible for controlling affected production while supplier investigation is in progress.

---

## 17. Responsibilities

### Supplier Quality Engineer

Responsible for:

- monitoring supplier quality performance;
- evaluating supplier-related deviations;
- initiating supplier reviews;
- coordinating corrective actions;
- verifying effectiveness;
- approving return to standard monitoring.

### Quality Engineer

Responsible for:

- providing manufacturing quality evidence;
- identifying affected batches;
- supporting non-conformity classification;
- supporting root-cause analysis.

### Manufacturing Supervisor

Responsible for:

- implementing required operational containment;
- supporting traceability;
- coordinating affected production activities.

### Quality Manager

Responsible for:

- reviewing Critical supplier issues;
- approving major escalations;
- coordinating cross-functional decisions where required.

---

## 18. Use of Maranello AI

Maranello AI may support supplier quality activities by:

- calculating supplier-specific Defect Rates;
- comparing supplier performance;
- identifying recurring defect patterns;
- analyzing affected component categories;
- identifying suppliers associated with abnormal rework or scrap;
- retrieving applicable supplier quality rules;
- highlighting suppliers requiring review according to documented thresholds.

For example, Maranello AI may determine that a supplier has a Defect Rate above the applicable Warning threshold and retrieve this procedure to explain the required next action.

The system must clearly distinguish between:

```text
Statistical association
```

and:

```text
Confirmed supplier root cause
```

Maranello AI must not claim that a supplier caused a defect solely because the supplier is statistically associated with affected batches.

---

## 19. Related Documents

This procedure should be interpreted together with:

- Manufacturing Quality Policy;
- Non-Conformity Management Procedure;
- Rework and Scrap Procedure;
- Production Escalation Policy.

---

## 20. Document Control

| Field | Value |
|---|---|
| Document ID | SQP-001 |
| Version | 1.0 |
| Owner | Supplier Quality & Manufacturing Operations |
| Classification | Internal |
| Effective Date | 2025-01-01 |
| Review Cycle | Annual |
| Status | Active |