# excel_report.py
# Generates a formatted SOX ITGC audit workpaper in Excel
# Three sheets: SOD Violations, Terminated Still Active, Ghost Accounts

import pandas as pd
import sqlite3
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import date

# ---------------------------------------------------------------------------
# Color constants
# ---------------------------------------------------------------------------
SOD_COLOR       = "AEC6CF"   # pastel blue   — SOD Violations
TERM_COLOR      = "FDFD96"   # pastel yellow — Terminated Still Active
GHOST_COLOR     = "C1E1C1"   # pastel green  — Ghost Accounts
HEADER_COLOR    = "2F4F8F"   # navy          — column headers
TITLE_COLOR     = "1C1C3A"   # near black    — report title

# ---------------------------------------------------------------------------
# Load findings from SQLite
# ---------------------------------------------------------------------------
def load_findings(db_path):
    conn = sqlite3.connect(db_path)
    findings = {
        "SOD Violations": pd.read_sql("""
            SELECT user_id, name, department, status,
                   termination_date, last_login, role, access_level
            FROM users WHERE role = 'Initiator+Approver'
        """, conn),
        "Terminated Still Active": pd.read_sql("""
            SELECT user_id, name, department, status,
                   termination_date, last_login, role, access_level
            FROM users WHERE status = 'Terminated'
            AND last_login > termination_date
            AND termination_date >= date('now', '-730 days')
        """, conn),
        "Ghost Accounts": pd.read_sql("""
            SELECT user_id, name, department, status,
                   termination_date, last_login, role, access_level
            FROM users WHERE status = 'Terminated'
            AND termination_date < date('now', '-730 days')
        """, conn),
    }
    conn.close()
    return findings

# ---------------------------------------------------------------------------
# Build one sheet
# ---------------------------------------------------------------------------
def build_sheet(ws, df, fill_color, sheet_title, finding_type):
    fill        = PatternFill("solid", fgColor=fill_color)
    header_fill = PatternFill("solid", fgColor=HEADER_COLOR)
    title_fill  = PatternFill("solid", fgColor=TITLE_COLOR)
