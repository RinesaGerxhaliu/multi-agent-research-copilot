# Clinical Analytics Dashboard – Data Governance Overview

Project: Healthcare Data Intelligence Program  
Last Updated: Week 12, 2024  
Primary Milestone: Week 16 – Production Release  

---

## 1. Data Classification

Owner: Compliance Officer  
Validation Target: Week 13  

Clinical data processed by the dashboard includes:

- Patient outcome metrics  
- Treatment records  
- Operational hospital KPIs  

All patient-related data is classified as PHI (Protected Health Information).

---

## 2. Data Protection Controls

### DG-01: Encryption Standards
Owner: Security Team  
Validation Target: Week 14  

Requirement:
- Encryption at rest  
- Encryption in transit (TLS 1.2+)  

Evidence:
Encryption enabled in staging environment.
Production validation pending.

---

### DG-02: Access Control Enforcement
Owner: Engineering Lead  
Validation Target: Week 13  

Requirement:
- Role-based access control (RBAC)  
- Restricted PHI access  
- Periodic access review  

Evidence:
RBAC implemented.
Formal access review report not yet issued.

---

## 3. Data Integrity Controls

### DG-03: Backup & Recovery
Owner: DevOps Lead  
Validation Target: Week 15  

Requirement:
- Daily database backups  
- Recovery validation test  

Evidence:
Backup automation configured.
Recovery test not yet documented.

---

## 4. Identified Data Risks

### R-DATA-01: Unauthorized PHI Access
Owner: Security Team  
Impact: High  

### R-DATA-02: Incomplete Access Review
Owner: Engineering Lead  
Impact: Medium  

### R-DATA-03: Backup Recovery Failure
Owner: DevOps Lead  
Impact: Medium  

---

## 5. Governance Rule

The Clinical Analytics Dashboard cannot be released unless:

- PHI encryption is validated  
- Access control review is documented  
- Backup recovery procedure is tested  

Any claim of full data governance compliance without documented validation must be flagged as:

"Not found in sources."
