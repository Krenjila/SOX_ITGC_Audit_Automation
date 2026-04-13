# SOX ITGC Audit Automation
### Python-based compliance testing tool simulating Big 4 IT General Controls testing

---

## Executive Summary

This project simulates the IT General Controls (ITGC) testing workflow performed by Big 4 firms on every public company SOX engagement. Three core control domains are tested against a synthetic dataset of 5,000 enterprise users — detecting access violations, terminated user risks, and segregation of duties failures that could expose a company to fraud risk or a material weakness finding under Sarbanes-Oxley.

**700 control violations detected across 5,000 users (14% violation rate)**

---

## Why This Matters

Public companies are required under SOX (Sarbanes-Oxley Act) to maintain effective IT General Controls. When these controls fail, companies must disclose a **material weakness** in their SEC annual filing — damaging investor confidence and exposing the organization to regulatory scrutiny.

The three most common ITGC failures this tool detects:

- **Segregation of Duties violations** — one person holds both Initiator and Approver roles, enabling them to process and approve their own transactions with no oversight. A direct fraud risk.
- **Terminated users still accessing systems** — employees fired within the last 7 months whose accounts were never deprovisioned. Sensitive company data remains accessible to people no longer on the team.
- **Ghost accounts** — users terminated 2+ years ago with accounts still open. A critical information leakage risk — former employees retaining access to confidential systems long after leaving the organization.

---

## Control Test Results

| Control Domain | Findings | % of Users |
|---|---|---|
| Segregation of Duties | 315 | 6.3% |
| Terminated Still Active | 190 | 3.8% |
| Ghost Accounts | 195 | 3.9% |
| **Total** | **700** | **14.0%** |

---

## System Architecture

```
Python (generate_data.py)    → 5,000 synthetic enterprise users with injected violations
Python (control_tests.py)    → Three SQL control tests via SQLite
Python (excel_report.py)     → Automated audit workpaper — three color-coded Excel sheets
```

---

## Control Logic

**Segregation of Duties**
```sql
WHERE role = 'Initiator+Approver'
```

**Terminated Still Active**
```sql
WHERE status = 'Terminated'
AND last_login > termination_date
AND termination_date >= date('now', '-730 days')
```

**Ghost Accounts**
```sql
WHERE status = 'Terminated'
AND termination_date < date('now', '-730 days')
```

---

## Audit Workpaper Output

The automated Excel report (`sox_audit_workpaper.xlsx`) generates three color-coded sheets:

| Sheet | Color | Finding Type |
|---|---|---|
| SOD Violations | Pastel Blue | Segregation of Duties Violation |
| Terminated Still Active | Pastel Yellow | Terminated User Still Accessing System |
| Ghost Accounts | Pastel Green | Ghost Account — Inactive 2+ Years |

Each sheet includes: navy header row, generation date, finding type label, total findings count, and full user details for audit team review.

---

## Data Model

| Column | Description |
|---|---|
| user_id | Unique identifier |
| name | Employee name |
| department | HR, Finance, IT, Sales, Marketing, Legal, Operations, Procurement |
| status | Active / Terminated |
| hire_date | Date hired |
| termination_date | Date terminated (null if active) |
| last_login | Most recent system login |
| role | Initiator, Approver, Admin, Read-Only, Initiator+Approver |
| access_level | High, Medium, Low |
| manager_id | Approving manager |
| has_conflict | Boolean flag for injected violations |

---

## Injected Violations

| Violation Type | Count | Method |
|---|---|---|
| SOD conflicts | 315 | role set to 'Initiator+Approver' |
| Terminated still logging in | 190 | terminated 1–7 months ago, last_login within 7 days |
| Ghost accounts | 195 | terminated 2–4 years ago, account never closed |

---

## How to Run

```bash
# Install dependencies
pip3 install pandas faker openpyxl

# Generate synthetic user data
cd scripts
python3 generate_data.py

# Run control tests
python3 control_tests.py

# Generate audit workpaper
python3 excel_report.py
```

---

## Tech Stack

`Python` · `Pandas` · `SQLite` · `SQL` · `openpyxl` · `Faker`

---

## Project Structure

```
sox-itgc-testing/
├── data/
│   ├── users.csv                  ← 5,000 synthetic users
│   ├── sox_findings.db            ← SQLite database
│   └── sox_audit_workpaper.xlsx   ← generated audit workpaper
├── scripts/
│   ├── generate_data.py           ← synthetic data generation
│   ├── control_tests.py           ← SQL control tests
│   └── excel_report.py            ← automated Excel report
└── README.md
```

---

*Built by Krenjila Sharma — BS Computer Science & Business Analytics, Caldwell University*  
*Targeting Tech Risk & Analytics roles at Big 4 firms*
