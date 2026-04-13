# control_tests.py
# Runs three SOX ITGC control tests against the synthetic user dataset
# Tests: Terminated Still Active, Ghost Accounts, SOD Violations

import sqlite3
import pandas as pd

def run_tests(csv_path, db_path):
    # Load CSV into SQLite
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql("users", conn, if_exists="replace", index=False)

    tests = {
        "Terminated Still Active": """
            SELECT 
                user_id, name, department, status,
                termination_date, last_login, role, access_level
            FROM users
            WHERE status = 'Terminated'
            AND last_login > termination_date
        """,
        "Ghost Accounts": """
            SELECT 
                user_id, name, department, status,
                termination_date, last_login, role, access_level
            FROM users
            WHERE status = 'Terminated'
            AND termination_date < date('now', '-730 days')
        """,
        "SOD Violations": """
            SELECT 
                user_id, name, department, status,
                termination_date, last_login, role, access_level
            FROM users
            WHERE role = 'Initiator+Approver'
        """
    }

    findings = {}
    for test_name, query in tests.items():
        result = pd.read_sql(query, conn)
        findings[test_name] = result
        print(f"{test_name}: {len(result)} findings")

    print(f"\nTotal findings: {sum(len(v) for v in findings.values())}")
    conn.close()
    return findings

if __name__ == "__main__":
    findings = run_tests("../data/users.csv", "../data/sox_findings.db")
