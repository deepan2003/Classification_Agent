# Vireo Audio: Weekly Complaint Digest and Agent Leaderboard

Built for Priya Raman, Head of Customer Experience at Vireo Audio. It does two things:

1. **Weekly digest:** an AI reads each ticket (the customer's message and the agent's note), gives it one specific reason, and lists the top 10 complaints per week.
2. **Leaderboard:** Tier 1 agents ranked by tickets closed per week. Tier 2 (Escalations & Warranty) is left out on purpose, because the support policy says they must not be ranked by volume.

It is a few small Python scripts. No platform.

---

## 1. Setup

You need Anaconda or Miniconda, and an [OpenRouter](https://openrouter.ai/settings/keys) API key.

```bash
git clone https://github.com/deepan2003/Classification_Agent.git
cd Classification_Agent

conda create -n vireo python=3.11 -y
conda activate vireo
pip install -r requirements.txt
```

Create a file named `.env` in the project folder:

```
OPENROUTER_API_KEY=your_key_here
MODEL=openai/gpt-4o-mini
```

Create the folders, then put `tickets.csv` and `agents.csv` from the Vireo data pack into `data/` (the data is private, so it is not in this repo):

```bash
mkdir data
mkdir vireo
mkdir vireo\out        # Mac/Linux: mkdir -p vireo/out
```

---

## 2. How to run

Run from the project folder, in this order:

| Step | Command | What it does | Output |
|---|---|---|---|
| 1 | `python digest.py --discover` | AI reads 200 random tickets and suggests complaint tags. **Then edit the list by hand.** | `vireo/out/taxonomy.json` |
| 2 | `python digest.py` | AI tags every ticket from the last 2 full weeks and builds the weekly top 10. | `vireo/out/tagged.csv`, `vireo/out/weekly_digest.md` |
| 3 | `python leaderboard.py` | Ranks Tier 1 agents by tickets closed each week. | `vireo/out/leaderboard.csv` |
| 4 | `python savings.py` | Shows what transfers and late replies cost today. | printed on screen |

Checking accuracy:

| Command | What it does |
|---|---|
| `python evaluate.py` | Picks 50 tagged tickets to label by hand. |
| `python make_holdout.py` | Picks 40 new tickets the prompt was never tuned on. |
| `python compare.py` | Compares the hand labels with the AI tags and prints accuracy and mistakes. |

**Important:** AI answers are saved in `.llm_cache.jsonl` so re-runs don't cost money again. **Delete this file whenever you change the prompt or the tag list**, or the old answers will be reused.

---

## 3. Choices I made

**Cleaning the data (`common.py`).** The original file is never changed.
- **Duplicates:** 653 ticket IDs appear twice because old tickets were re-imported. I keep the copy from the new helpdesk.
- **Time zone:** old tickets store the closing time in UTC, not IST. I add 5h30m. Before this fix, tickets looked like they closed before they were opened. After it, there are 0 such tickets.
- **Weeks** run Monday to Sunday.

**How the AI tags tickets.**
- The chatbot's category is too vague (about 1 in 7 tickets is just "Other"), so I ignore it and read the real text.
- The AI first suggests tags from 200 tickets. I clean that list by hand. Then it picks one tag per ticket from the cleaned list. A fixed list means the same problem always has the same name, so weekly counts can be compared.
- **Not fine-tuning:** there was no labelled training data, and it would not fit in five hours.
- **Not Jev (OpenRouter's decision model):** it can only pick from options you give it. It cannot create tags, so it can't build the list.

**Leaderboard rules.** Only `resolved` and `closed` tickets count. Tier 2 agents are removed. Ranking is per week, by closing date.

---

## 4. Does it work?

Evaluation labels were drafted by Claude and reviewed by me. So this is a check against a second opinion, not a fully independent human test.

| Test | What changed | Accuracy |
|---|---|---|
| 50 tickets, first tag list | Tags suggested by the AI, not yet cleaned | 78% (39/50) |
| 50 tickets, cleaned list | Merged overlapping tags, added `bluetooth_connection_drops` and `payment_failed_no_order`, removed one vague tag | 92% (46/50) |
| 50 tickets, 5 extra prompt rules | Rules for charging, pre-sales questions, dead products, trusting the agent note | 100% (50/50) |
| **40 new tickets, cleaned list** | Never used for tuning | **95% (38/40)** |
| 40 new tickets, extra prompt rules | Same 40 tickets | 95% (38/40), no gain |

What this tells us:
- Cleaning the tag list gave the real improvement (78% to 92%).
- The extra rules fixed the tickets they were written for, but made no difference on new tickets.
- The first three rows were tested on tickets I used to make changes, so they look better than real life. **Trust the 95% on new tickets.**
- With only 40 new tickets, the real accuracy could be a few points higher or lower.
- Mistakes are rare and look alike: a complaint with no matching tag (a "hiss" in the audio), and tickets that fit two tags (refund vs repair status).
- Not tested: other weeks, or the full 18 months.

---

## 5. Business goal and money

**Goal: cut avoidable pre-sales ("will it work with my phone?") and invoice contacts by 30%. Worth about Rs 22,000 a quarter.**

How the number is built:
- The digest shows about 20 such tickets a week (19 and 21 in the two weeks tagged).
- Each contact costs Rs 290 (the policy figure, as Priya confirmed in the email thread).
- 6 fewer a week × 13 weeks × Rs 290 ≈ Rs 22,600 a quarter.

The 30% is my assumption, and it rests on two weeks of data. The tool finds the pattern. Vireo has to fix product pages and order emails to get the saving.

Other costs found by `savings.py` (Jan 2025 to Jun 2026):

| Cost | Count | Total | Per quarter |
|---|---|---|---|
| Transfers between teams (Rs 305 each) | 1,169 | Rs 356,545 | about Rs 59,700 |
| Late first replies (Rs 350 credit each) | 1,051 | Rs 367,850 | about Rs 61,600 |

- Better tagging could cut only a small part of the transfers (about Rs 6,000 a quarter).
- Late-reply credits are paid whatever the cause, so this tool does not reduce them. They are the biggest cost and the best next thing to study.

**Running cost:** about Rs 5 for 366 tickets, or about Rs 13 per 1,000 tickets (total project spend was $0.16, about Rs 14, including testing; per-ticket figures are estimated from that total). At Vireo's volume (about 650 tickets a week, roughly 2,800 a month) that is about Rs 35 a month, using `openai/gpt-4o-mini`.

---

## 6. What I left out, and why

- **Orders, customers and products files:** the digest and leaderboard don't need them. Joining products would show which product causes which complaint. A good next step.
- **Tagging all 18 months:** only the last 2 full weeks (366 tickets), to keep cost and time low.
- **Repeat contacts** ("I already told your colleague", raised by Neha): not built.
- **CSAT scores and refund amounts:** not used. Old rows use 0 for "no response" and a different money unit, so both need cleaning first.

---

## 7. Known problems

- The 95% is measured on 40 tickets, and the labels were AI-drafted.
- No tag exists for audio quality problems like hiss or distortion.
- Some tickets fit two tags (`order_not_delivered` vs `order_status_stuck`, `refund_pending` vs `rma_status_query`).
- The leaderboard counts tickets only. It ignores how hard a ticket was, and Chat, Voice, Returns, Logistics and Billing do different work. **Compare agents within a team only.**
- The business-goal number is an estimate from two weeks of data.
- Paths like `vireo/out/` are hard-coded in the scripts.

---

## 8. AI tools used

- **Claude (chat):** helped write and debug the scripts, drafted the evaluation labels, helped draft the memo and this README.
- **OpenRouter, `openai/gpt-4o-mini`:** the model that tags tickets in the tool.
- **Thrown away:** Jev (doesn't fit), fine-tuning, free-form tags (names were inconsistent).

---

## 9. Files

```
common.py          loads and cleans tickets
digest.py          builds the tag list, tags tickets, writes the weekly digest (current prompt)
digest_v2.py       earlier prompt, kept to show what changed
leaderboard.py     Tier 1 weekly leaderboard
savings.py         cost of transfers and late replies
evaluate.py        picks 50 tickets to label
make_holdout.py    picks 40 new tickets for the honest test
compare.py         accuracy and mistakes
requirements.txt   packages
vireo/out/         generated results
```
