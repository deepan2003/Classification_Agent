# Memo: What customers complain about, and who closes tickets

**To:** Priya Raman, Head of Customer Experience, Vireo Audio
**From:** Deepan K S

## In short

I built a small tool that reads every ticket and tags it with the real reason, like "order not delivered" or "charging case dead". The chatbot's own category is too vague to use: about 1 in 7 tickets is just "Other". The tool gives you a weekly list of top complaints and a leaderboard of agents.

**Goal I suggest: cut avoidable "will it work with my phone?" and "send me my invoice" contacts by 30%. That is worth about Rs 22,000 a quarter.** It is a modest saving, and I explain why below.

## Top complaints, week of 22 June (199 tickets)

| # | Complaint | Tickets | Week before |
|---|---|---|---|
| 1 | Order not delivered or lost | 23 | 16 |
| 2 | Refund not received | 17 | 9 |
| 3 | Battery drains fast | 15 | not in top 10 |
| 4 | Question before buying: will it work with my phone or device? | 13 | 11 |
| 5 | Case or earbud not charging | 12 | 7 |

Orders not arriving is the top complaint in both weeks. Refund and battery complaints jumped in the latest week. Worth asking Logistics and Returns Desk about.

## Leaderboard: tickets closed, week of 22 June (Tier 1 agents)

| Rank | Agent | Team | Closed |
|---|---|---|---|
| 1 (tie) | Pooja Dhillon | Email | 11 |
| 1 (tie) | Vivaan Sethi | Returns Desk | 11 |
| 3 (tie) | Aishwarya Agarwal | Logistics | 10 |
| 3 (tie) | Diya Singh | Billing | 10 |
| 5 | Om Varghese | Chat | 9 |

Please read this carefully:
- Returns Desk, Logistics and Billing agents close about 5 tickets a week. Chat and Voice agents close about 3, because their tickets are different. **Compare agents within a team, not across teams.**
- A count does not show how hard a ticket was.
- The Escalations & Warranty team is left out on purpose, as Neha asked. Their cases take days by design.
- The full list is in `leaderboard.csv`.

## The money

Over the last 18 months, using the costs in the support policy:
- Transfers between teams cost about **Rs 59,700 a quarter**.
- Late first replies cost about **Rs 61,500 a quarter** in store credits.
- Every avoidable contact costs **Rs 290**.

**My suggestion:** about 20 tickets a week are questions a product page or an order email could answer (will it work with my phone, send me my invoice). If we cut those by 30%, that is 6 fewer a week, or about Rs 22,000 a quarter. The tool doesn't do this by itself. It shows you where the problem is, and you decide whether to fix it.

**A smaller saving:** faulty-product tickets that start with a front-line team are passed on more often (14 in 100, against 9 in 100 for other tickets). Sending them to the right team first could save about Rs 6,000 a quarter. I can't see where each transfer went, so this is rough.

**What I am not claiming:** savings on the late-reply credits. The credit is paid whatever the reason, and this tool does not change staffing. It is the largest cost, though, and Email has the most late replies (about 12 in 100). It is the best next thing to look at.

## How far to trust it

I tested the tool on 40 tickets it had never seen. It gave the same tag as my review in **38 of 40 (95%)**. The review labels were first drafted with an AI assistant, then checked by me. So this is a good sign, not a formal audit.

The Rs 22,000 is an estimate. It uses only two weeks of tagged tickets, and the 30% is my assumption. I tagged only the two latest weeks to keep the running cost small: [Rs X for 366 tickets, Rs Y per 1,000 tickets].

## What I need from you

1. A yes or no on adding answers to product pages and order emails for compatibility and invoice questions.
2. Should I tag the full history and add repeat-contact checking ("I already told your colleague")? I didn't get to that.
