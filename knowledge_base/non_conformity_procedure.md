# Non-Conformity Management Procedure

> **Document ID:** NCP-001  
> **Version:** 1.0  
> **Owner:** Quality & Manufacturing Operations  
> **Classification:** Internal  
> **Effective Date:** 2025-01-01  
> **Review Cycle:** Annual  
> **Status:** Active

---

## 1. Purpose

This procedure defines the process for identifying, containing, investigating, managing, and closing manufacturing non-conformities.

The objective is to ensure that quality deviations are handled consistently, affected production is appropriately controlled, root causes are investigated, and corrective actions are documented and verified.

---

## 2. Scope

This procedure applies to non-conformities associated with:

- production batches;
- production lines;
- manufactured components;
- supplier-provided components;
- rework activities;
- inspection results;
- manufacturing processes;
- quality KPI deviations.

The procedure applies to all production lines and manufacturing teams within the Quality & Manufacturing Operations scope.

---

## 3. Definition of Non-Conformity

A non-conformity is any condition in which a product, component, process, production batch, or manufacturing result fails to satisfy an applicable quality requirement.

Examples include:

- excessive Defect Rate;
- excessive Rework Rate;
- excessive Scrap Rate;
- Quality Score below the required threshold;
- failed quality inspection;
- recurring defect patterns;
- safety-critical defects;
- significant supplier-related defects;
- production process deviations.

A data-quality anomaly alone does not automatically represent a manufacturing non-conformity.

The underlying production data must first be validated.

---

## 4. Non-Conformity Identification

A potential non-conformity may be identified through:

- routine quality inspection;
- automated KPI monitoring;
- manufacturing operator observation;
- supplier quality inspection;
- production-line monitoring;
- trend analysis;
- audit activities;
- automated analytical systems.

When a potential non-conformity is identified, the available evidence must be reviewed before a final classification is assigned.

---

## 5. Initial Data Validation

Before initiating a formal non-conformity based on analytical data, the responsible team must verify that the supporting data is sufficiently reliable.

The validation should consider:

- missing values;
- duplicate observations;
- invalid numerical values;
- inconsistent categorical values;
- incorrect date formats;
- abnormal outliers;
- logical inconsistencies.

For example:

```text
defective_units > units_produced
```

must be treated as a data-quality problem until the correct production values are verified.

Automated systems must not interpret obviously invalid data as confirmed manufacturing performance.

---

## 6. Non-Conformity Classification

Non-conformities are classified according to severity.

### Minor

A Minor non-conformity:

- has limited operational impact;
- does not affect safety-critical characteristics;
- can be contained locally;
- does not indicate a recurring systemic problem.

Typical response:

- document the issue;
- perform local correction;
- continue monitoring.

### Major

A Major non-conformity:

- exceeds an established quality threshold;
- affects multiple units or batches;
- requires structured investigation;
- may indicate a recurring manufacturing or supplier issue.

Typical response:

- initiate containment;
- assign investigation responsibility;
- perform root-cause analysis;
- define corrective actions.

### Critical

A Critical non-conformity:

- may affect product safety;
- presents significant customer risk;
- indicates severe process loss of control;
- involves repeated unresolved Major issues;
- requires immediate management attention.

Typical response:

- immediate containment;
- production escalation;
- management notification;
- formal investigation;
- documented authorization before normal production resumes.

---

## 7. Immediate Containment

When a Major or Critical non-conformity is confirmed, containment activities must begin without unnecessary delay.

Possible containment actions include:

- isolating the affected batch;
- preventing shipment or further processing;
- increasing inspection frequency;
- performing additional quality checks;
- temporarily holding related batches;
- separating suspected components;
- notifying relevant manufacturing personnel.

Containment is intended to control immediate risk.

It does not replace root-cause analysis or corrective action.

---

## 8. Batch Isolation

Affected production batches must remain traceable throughout the investigation.

The containment record should identify:

- batch identifier;
- production date;
- production line;
- vehicle model;
- shift;
- relevant defect category;
- affected supplier or component where applicable;
- inspection status;
- reason for isolation.

A batch must not be released solely because subsequent production appears normal.

Release requires appropriate quality verification.

---

## 9. Root-Cause Analysis

Major and Critical non-conformities require investigation of the underlying cause.

Root-cause analysis may consider:

- production equipment;
- manufacturing methods;
- materials;
- supplier components;
- operator activities;
- environmental conditions;
- process parameters;
- inspection methods;
- recurring historical patterns.

Appropriate investigation techniques may include:

- 5 Whys;
- Ishikawa analysis;
- Pareto analysis;
- trend analysis;
- comparison between production lines;
- comparison between shifts;
- supplier performance analysis.

The investigation must distinguish correlation from confirmed causation.

---

## 10. Corrective Actions

Corrective actions must address the identified or most probable root cause.

Examples include:

- production parameter adjustment;
- equipment maintenance;
- operator instruction;
- additional inspection;
- supplier corrective action;
- process redesign;
- component replacement;
- revised quality control.

Each corrective action should identify:

1. the action to be performed;
2. the responsible person or team;
3. the expected completion date;
4. the verification method;
5. the resulting status.

---

## 11. Verification of Effectiveness

A corrective action cannot be considered complete solely because it has been implemented.

Its effectiveness must be verified.

Verification may include:

- monitoring subsequent batches;
- comparing defect rates before and after the action;
- reviewing Quality Score trends;
- checking recurrence of the defect category;
- verifying supplier performance;
- performing additional inspections.

If the problem persists, the investigation must be reopened or escalated.

---

## 12. Recurring Non-Conformities

Repeated quality deviations must be evaluated collectively rather than as isolated events.

A recurring condition may exist when:

- the same defect category repeatedly affects the same production line;
- the same supplier is repeatedly associated with quality deviations;
- the same shift consistently exhibits abnormal performance;
- corrective actions fail to prevent recurrence;
- Warning conditions continue across multiple monitoring periods.

Repeated Minor or Warning conditions may therefore justify Major classification or formal escalation.

---

## 13. Supplier-Related Non-Conformities

When evidence indicates that a non-conformity may be associated with a supplied component, the Supplier Quality Engineer must be involved.

The investigation should consider:

- supplier identifier;
- component category;
- affected batches;
- recurrence;
- defect severity;
- scrap and rework impact.

Supplier-related corrective actions must follow the Supplier Quality Procedure.

---

## 14. Rework and Scrap

When affected units may be recovered through rework, all activities must follow the Rework and Scrap Procedure.

Reworked units must be inspected again before being accepted.

Units that cannot be restored to applicable quality requirements must be evaluated for scrap according to the applicable procedure.

---

## 15. Escalation Criteria

A non-conformity must be escalated when:

- a Critical quality condition is identified;
- a safety-critical defect is detected;
- Defect Rate exceeds the Critical threshold defined by the Manufacturing Quality Policy;
- Rework Rate exceeds the Critical threshold;
- Scrap Rate exceeds the Critical threshold;
- Quality Score falls below the Critical threshold;
- the same significant issue repeatedly occurs;
- corrective actions are ineffective;
- a significant supplier-related issue is identified.

Operational escalation must follow the Production Escalation Policy.

---

## 16. Non-Conformity Closure

A non-conformity may be closed only when:

1. the affected production scope has been identified;
2. containment has been completed where required;
3. the issue has been investigated;
4. required corrective actions have been implemented;
5. effectiveness has been verified;
6. required documentation has been completed;
7. no unresolved Critical risk remains.

Closure must be traceable and approved by the appropriate Quality authority.

---

## 17. Responsibilities

### Quality Engineer

Responsible for:

- validating the quality issue;
- classifying the non-conformity;
- coordinating investigation;
- documenting findings;
- verifying corrective actions.

### Manufacturing Supervisor

Responsible for:

- implementing containment;
- supporting investigation;
- coordinating production activities;
- implementing approved operational corrections.

### Supplier Quality Engineer

Responsible for:

- managing supplier-related investigations;
- coordinating supplier corrective actions;
- monitoring supplier performance.

### Quality Manager

Responsible for:

- reviewing Critical non-conformities;
- approving significant quality decisions;
- supporting cross-functional escalation;
- approving closure where required.

---

## 18. Use of Maranello AI

Maranello AI may support non-conformity management by:

- detecting KPI deviations;
- identifying abnormal manufacturing patterns;
- analyzing historical production data;
- retrieving applicable quality procedures;
- identifying potentially recurring issues;
- supporting investigation with quantitative evidence.

Maranello AI provides decision support.

It must not autonomously approve:

- release of isolated production batches;
- closure of Major or Critical non-conformities;
- safety-critical decisions;
- final root-cause conclusions where human validation is required.

When supporting data is incomplete or unreliable, the system should clearly indicate the limitation.

---

## 19. Related Documents

This procedure should be interpreted together with:

- Manufacturing Quality Policy;
- Supplier Quality Procedure;
- Rework and Scrap Procedure;
- Production Escalation Policy.

---

## 20. Document Control

| Field | Value |
|---|---|
| Document ID | NCP-001 |
| Version | 1.0 |
| Owner | Quality & Manufacturing Operations |
| Classification | Internal |
| Effective Date | 2025-01-01 |
| Review Cycle | Annual |
| Status | Active |