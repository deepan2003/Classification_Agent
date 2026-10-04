import pandas as pd
from common import load_tickets, week_start

t = load_tickets()
a = pd.read_csv("data/agents.csv")
t = t[t.status.isin(["resolved", "closed"]) & t.resolved_at.notna()]
t = t.merge(a[["agent_id", "name", "team", "tier"]], on="agent_id", how="left")
t = t[t.tier == 1]                                   # policy: no volume ranking for Tier 2
t["week"] = week_start(t.resolved_at)
lb = t.groupby(["week", "agent_id", "name", "team"]).size().rename("closed").reset_index()
lb["rank"] = lb.groupby("week")["closed"].rank(ascending=False, method="min").astype(int)
lb = lb.sort_values(["week", "rank"], ascending=[False, True])
lb = lb[lb.week <= "2026-06-22"]          # drop partial weeks after the last full week
lb.to_csv("vireo/out/leaderboard.csv", index=False)
print(lb[lb.week == lb.week.max()].head(10))