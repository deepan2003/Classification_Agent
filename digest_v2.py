import os, json, sys, pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm
from common import load_tickets, week_start

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
MODEL = os.getenv("MODEL", "openai/gpt-4o-mini")

def ask(system, user):
    r = client.chat.completions.create(
        model=MODEL, temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    return json.loads(r.choices[0].message.content)

def txt(r):  # messages may be Hinglish/typo-heavy
    return f"CUSTOMER: {r.customer_message}\nAGENT NOTE: {r.agent_notes}"

def discover(t, n=200):
    s = t.sample(n, random_state=1)
    body = "\n---\n".join(txt(r) for r in s.itertuples())
    out = ask("You analyse consumer-audio support tickets (may be Hinglish). Propose 25-35 specific "
              "root-cause tags (e.g. 'left_earbud_battery_drain', 'otp_not_received', 'duplicate_payment_charge'). "
              "Ignore any chatbot category. Return JSON: {\"tags\":[{\"tag\":str,\"definition\":str}]}", body)
    json.dump(out["tags"], open("vireo/out/taxonomy.json", "w"), indent=1)

def classify(t):
    tax = json.load(open("vireo/out/taxonomy.json"))
    tags = [x["tag"] for x in tax]
    sysmsg = ("Assign ONE root-cause tag from this list, based on the real problem (ignore any category label). "
              f"Tags: {json.dumps(tax)}. If none fit use 'other_new' and give a short suggested_tag. "
              "Return JSON: {\"tag\":str,\"suggested_tag\":str|null}")
    cache = {}
    if os.path.exists(".llm_cache.jsonl"):
        for l in open(".llm_cache.jsonl"):
            d = json.loads(l); cache[d["id"]] = d
    f = open(".llm_cache.jsonl", "a")
    rows = []
    for r in tqdm(list(t.itertuples())):
        if r.ticket_id not in cache:
            try:
                o = ask(sysmsg, txt(r))
            except Exception as e:
                o = {"tag": "error", "suggested_tag": str(e)[:60]}
            if o.get("tag") not in tags + ["other_new"]:
                o["tag"] = "other_new"
            cache[r.ticket_id] = {"id": r.ticket_id, **o}
            f.write(json.dumps(cache[r.ticket_id]) + "\n"); f.flush()
        rows.append(cache[r.ticket_id])
    return t.merge(pd.DataFrame(rows).rename(columns={"id": "ticket_id", "tag": "root_cause"}), on="ticket_id")

if __name__ == "__main__":
    t = load_tickets()
    t["week"] = week_start(t.created_at)
    if "--discover" in sys.argv:
        discover(t)
    else:
        weeks = sorted(t.week.unique())[-3:-1]        # last 2 COMPLETE weeks
        sub = t[t.week.isin(weeks)]
        res = classify(sub)
        res.to_csv("vireo/out/tagged.csv", index=False)
        d = (res.groupby(["week", "root_cause"]).size().rename("tickets").reset_index()
               .sort_values(["week", "tickets"], ascending=[True, False]))
        d["top10_rank"] = d.groupby("week").cumcount() + 1
        d = d[d.top10_rank <= 10]
        open("vireo/out/weekly_digest.md", "w").write(d.to_markdown(index=False))
        print(d)