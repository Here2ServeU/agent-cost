# For Finance: What This Project Means for the Budget

*A 10-minute read. No technical background needed, and you do not have to run anything.*

---

## The problem, in one paragraph

An **AI agent** is software that does a task, like reading an invoice, by asking an AI model
a series of small questions, one after another. Each question is a **step**, and each step
is billed, like a metered phone call. A normal invoice takes about six steps and costs about
six cents. But when the agent meets something it cannot handle, such as an amount written
out in words, it can keep retrying all night. It does not crash and it does not raise an
error, so nothing looks wrong until the bill arrives.

## Why this bill is different from other software costs

| Most software | AI agents |
|---|---|
| Fixed monthly licence | Pay per step, every step |
| Cost is known in advance | Cost depends on how hard each task turns out to be |
| A failure is cheap; it just stops | A failure can be the **most** expensive outcome, because it keeps going |
| The invoice matches the plan | The invoice reflects what the agent *chose* to do overnight |

## The two numbers

For one broken invoice:

| | Cost | How it was found |
|---|---|---|
| **With no protections** | **about $1,450 overnight** | by somebody, in the morning |
| **With the six protections** | **$0.07** | by the agent itself, after 6 steps, with the reason written down |

The $1,450 is a projection, and its assumptions are stated: 12 copies of the agent working
through a queue, one step every 3 seconds, from 9 pm until someone checks at 6:30 am. Your
engineering team can rerun it with your own numbers (`python3 two_numbers.py --workers 4
--hours 12`).

The difference, about $1,450, is **the bill that never arrived**. It will never appear on
an invoice, which is exactly why someone has to show it to you.

---

## The six protections, as finance controls

Each one maps onto a control you already know.

| # | Protection | The finance version | What it buys |
|---|---|---|---|
| 1 | **Instrument it** | Itemised receipts, coded to a cost centre | You can see what every step cost and which team pays |
| 2 | **Cap it** | A spending limit on a company card, per transaction and per day | No single task can spend more than you agreed in advance |
| 3 | **Detect the loop** | Duplicate-payment detection | Stops repeated work after a few steps, before it reaches the limit |
| 4 | **Checkpoint** | Saving a half-finished reconciliation | A stopped task resumes without paying for the finished part again |
| 5 | **Cost per success** | Unit economics: cost per *resolved* ticket, not per attempt | The real cost of one useful result |
| 6 | **Alert on the rate** | A burn-rate warning against the monthly budget | Somebody finds out while it is happening, not at month end |

---

## The number to budget with: cost per successful task

This is the most important idea for finance.

- **Cost per request** = total spend ÷ *all* runs. Most dashboards show this. It looks
  good because it spreads the failures across everything.
- **Cost per successful task** = total spend ÷ runs that *worked*. The failures stay in
  the total spend but are not counted as results. This is what one useful outcome actually
  costs.

From the demo:

```
  cost per request        $0.0624   (pays by the mile)
  cost per SUCCESSFUL     $0.1325   (pays for arrival)
  failed-run tax          $0.5714  (54% of spend)
```

Think of a taxi. *Cost per request* is the price per mile. *Cost per successful task* is
the price of actually getting where you were going, including the trips that ended up in
the wrong place.

**The failed-run tax** is the share of spend that went on work that failed. In the demo it
is high because the agent was broken on purpose many times. In a healthy system it should
be small, and it should go down after each fix.

Why it matters: a change can make **cost per request go down** while **cost per successful
task goes up**. For example, switching to a cheaper model that fails more often. Only the
second number catches that.

---

## What the alarms watch

There are two alarms, both based on the **monthly budget** ($300 in the demo, changeable in
one place):

| Alarm | Looks at | Goes off when | What happens |
|---|---|---|---|
| **Fast** | the last hour | spending is on pace for **2x** the monthly budget, for 5 minutes | somebody is paged straight away |
| **Slow** | the last 24 hours | spending is on pace for **1.2x** the monthly budget, for 2 hours | a ticket for the next working day |
| **Failed-run tax** | the last 6 hours | more than **35%** of spend is going to failed work | a ticket to investigate quality |

The alarms watch the **rate** of spending, meaning how fast money is going out. That is why
they can catch a problem within minutes instead of at month end.

The spending limits are still the real protection. **The limit is the seatbelt; the alarm
is the warning light.** The limit stops the spending whether or not anyone answers the page.

---

## How you know it is still working

Engineers run one check, `verify.py`, that tries each of the six failures on purpose and
confirms the protection stopped it. It runs automatically every time the code changes. If
any protection stops working, the check fails and the change cannot go in quietly.

Ask to see it. Six **PASS** lines means all six held today.

---

## Three sentences for three rooms

**To a manager:**
"The agent that could run away overnight now stops itself in six steps. Here is the run
with the protection off, and here it is with it on."

**To finance:**
"We know the cost per resolved invoice, and we know what share of spend goes to work that
fails. Both are reported with their definition attached."

**To the engineer who has to maintain it:**
"Under four hundred lines, one check that fails in CI if any of it breaks, and every
protection has an off switch so you can measure what it buys."

---

## Questions worth asking your engineering team

1. What is the **per-run** spending limit on each agent, and who chose it?
2. What is the **per-day** limit, and what happens when it is reached?
3. What is our **cost per successful task**, and how is *success* defined?
4. What share of last month's spend was the **failed-run tax**?
5. Who gets paged by the **fast** alarm, and has it ever fired?
6. Can you show me the run **with the protection off**?

The last one matters most. "Trust me" should not get budget. "Here is the same run with
the limit switched off" should.

---

## The data, for your own analysis

Every run is recorded as one line in a ledger that is only ever added to, never edited.
Running `python3 report.py --csv` writes it out as `ledger/runs.csv`, which opens in Excel
or Google Sheets:

| Column | Meaning |
|---|---|
| `run_id` | a unique code for this run |
| `task` | which invoice |
| `team` | who pays (cost centre) |
| `model` | which AI model, since they are priced differently |
| `result` | `success`, `looped`, `capped`, `ceiling` (step limit reached) or `failed` |
| `reason` | why it stopped, in plain words |
| `steps` | how many paid steps it took |
| `cost_usd` | what it cost, in US dollars |
| `saved_by_checkpoint_usd` | finished work that was carried over instead of paid for again |
| `duration_s` | how long it took, in seconds |

See [GLOSSARY.md](GLOSSARY.md) for any other term.
