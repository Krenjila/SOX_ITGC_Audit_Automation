# generate_data.py
# Generates 5,000 synthetic users with intentional SOX ITGC violations

import pandas as pd
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()
random.seed(42)

N_USERS = 5000
DEPARTMENTS = ["HR", "Finance", "Sales", "Marketing", "IT",
               "Legal", "Operations", "Procurement"]
ROLES = ["Initiator", "Approver", "Admin", "Read-Only"]

def rand_date_active():
    # Hired sometime in the last 3 years
    return date.today() - timedelta(days=random.randint(30, 1095))

def rand_last_login():
    # Logged in sometime in the last 30 days
    return date.today() - timedelta(days=random.randint(0, 30))

def generate_users():
    users = []

    for i in range(1, N_USERS + 1):
        user = {
            "user_id": i,
            "name": fake.name(),
            "department": random.choice(DEPARTMENTS),
            "status": "Active",
            "hire_date": rand_date_active(),
            "termination_date": None,
            "last_login": rand_last_login(),
            "role": random.choice(ROLES),
            "access_level": random.choice(["High", "Medium", "Low"]),
            "manager_id": random.randint(1, 100),
            "has_conflict": False
        }
        users.append(user)

    # ----------------------------------------------------------------
    # Inject Violation 1 — Segregation of Duties (~315 users, 45%)
    # Pick 315 random users and give them conflicting roles
    # ----------------------------------------------------------------
    sod_targets = random.sample(range(len(users)), 315)
    for idx in sod_targets:
        users[idx]["role"] = "Initiator+Approver"
        users[idx]["has_conflict"] = True

    # ----------------------------------------------------------------
    # Inject Violation 2 — Terminated but still logging in (~190 users)
    # Fired 1-7 months ago but last_login is within the last 7 days
    # ----------------------------------------------------------------
    remaining = [i for i in range(len(users)) if not users[i]["has_conflict"]]
    term_active_targets = random.sample(remaining, 190)
    for idx in term_active_targets:
        days_ago = random.randint(30, 210)
        users[idx]["status"] = "Terminated"
        users[idx]["termination_date"] = date.today() - timedelta(days=days_ago)
        users[idx]["last_login"] = date.today() - timedelta(days=random.randint(0, 7))
        users[idx]["has_conflict"] = True

    # ----------------------------------------------------------------
    # Inject Violation 3 — Ghost accounts (~195 users)
    # Terminated 2-4 years ago, account never closed
    # ----------------------------------------------------------------
    remaining = [i for i in range(len(users)) if not users[i]["has_conflict"]]
    ghost_targets = random.sample(remaining, 195)
    for idx in ghost_targets:
        days_ago = random.randint(730, 1460)
        users[idx]["status"] = "Terminated"
        users[idx]["termination_date"] = date.today() - timedelta(days=days_ago)
        users[idx]["last_login"] = date.today() - timedelta(days=random.randint(400, 800))
        users[idx]["has_conflict"] = True

    return pd.DataFrame(users)

if __name__ == "__main__":
    users = generate_users()
    users.to_csv("../data/users.csv", index=False)

    total_violations = users["has_conflict"].sum()
    print(f"Generated {len(users)} users")
    print(f"Total violations: {total_violations} ({total_violations/len(users)*100:.1f}%)")
    print(f"  SOD conflicts:        {(users['role'] == 'Initiator+Approver').sum()}")
    print(f"  Terminated+Active:    {190}")
    print(f"  Ghost accounts:       {195}")

