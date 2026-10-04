import pandas as pd

def load_tickets():
    t = pd.read_csv("data/tickets.csv")
    for c in ["created_at", "first_response_at", "resolved_at"]:
        t[c] = pd.to_datetime(t[c])
    # dedupe legacy re-imports: prefer current helpdesk row
    t["_p"] = (t.source_system != "helpdesk").astype(int)
    t = t.sort_values("_p").drop_duplicates("ticket_id").drop(columns="_p")
    # legacy resolved_at is UTC -> IST
    m = t.source_system == "legacy_fd"
    t.loc[m, "resolved_at"] += pd.Timedelta(hours=5, minutes=30)
    bad = (t.resolved_at < t.created_at).sum()
    print(f"[check] resolved_at < created_at after fix: {bad}")
    return t.reset_index(drop=True)

def week_start(s):
    return s.dt.to_period("W-SUN").dt.start_time