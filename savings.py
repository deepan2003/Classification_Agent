import pandas as pd
from common import load_tickets

t = load_tickets()
t = t[t.created_at >= "2025-01-01"]
months = (t.created_at.max() - t.created_at.min()).days / 30.4
quarters = months / 3

transfers = t.transfers.sum()
transfer_cost = transfers * 305

target = {"chat": 15, "voice": 120, "social": 240, "email": 480}   # minutes
mins = (t.first_response_at - t.created_at).dt.total_seconds() / 60
breach = mins > t.channel.str.lower().map(target)
breach_cost = breach.sum() * 350

print(f"Transfers: {transfers} -> Rs {transfer_cost:,.0f} total, Rs {transfer_cost/quarters:,.0f}/quarter")
print(f"SLA breaches: {breach.sum()} -> Rs {breach_cost:,.0f} total, Rs {breach_cost/quarters:,.0f}/quarter")

# SCENARIO: state your assumption, backed by your evaluate.py accuracy
cut = 0.30
print(f"If transfers fall {cut:.0%}: saves Rs {transfer_cost*cut/quarters:,.0f}/quarter")