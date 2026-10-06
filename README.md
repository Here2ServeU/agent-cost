# Agent Cost Control: Safe to Leave Running Overnight

An AI agent is a program that works through a task one small step at a time. Every step is
a paid call to an AI model. Most of the time it finishes in a handful of steps and costs a
few cents. But give it one bad input, like an invoice with an amount it cannot read, and it
can go round in circles all night. Nobody gets an error, every dashboard stays green, and
the bill arrives in the morning.

This project takes that agent and adds **six protections, one at a time**. Then it proves
each one works by switching it **off**, measuring what happens, and switching it back on.

| | Same broken invoice | Found by | Cost |
|---|---|---|---|
| **Before** | nothing in the way, overnight | somebody else, in the morning | **$1,400+** |
| **After** | all six protections on | the agent itself, in 6 steps | **$0.07** |

> **No money, no account, no API key.** The AI model is *simulated*. Everything runs on
> your own computer, offline, for free, and prints the same numbers every time. The prices
> it uses are realistic, so the arithmetic is the same as with a real model.

---

## Who this is for

- **Complete beginners.** Never used a terminal? Fine. Every command is written out in
  full, with what you should see and what it means.
- **Finance and budget owners.** You do not need to run anything. Read
  [docs/FINANCE.md](docs/FINANCE.md) (10 minutes) for what this means for the budget, and
  [docs/GLOSSARY.md](docs/GLOSSARY.md) for every technical word in plain English.
- **Engineers.** Under 400 lines of safety code, one check that fails in CI if any of it
  breaks, and a flag on every protection so you can measure what it buys.
- **Presenters.** [docs/RECORDING.md](docs/RECORDING.md) is a run sheet for doing this live
  or on video in 30 to 45 minutes.

---

## The 45-minute plan

Install the tools (Part A) **before** you start the clock or the recording. Then:

| Clock | Part | What happens |
|---|---|---|
| 0:00 | [B. Get the project](#part-b-get-the-project-about-4-minutes) | Download it, set it up, see six PASS lines |
| 0:04 | [Step 0. The before picture](#step-0-the-before-picture-3-minutes) | Watch an agent that cannot stop |
| 0:07 | [Step 1. Instrument it](#step-1-instrument-it-4-minutes) | Every step now has a price |
| 0:11 | [Step 2. Cap it](#step-2-cap-it-4-minutes) | A spending limit per run and per day |
| 0:15 | [Step 3. Detect the loop](#step-3-detect-the-loop-5-minutes) | Stop the circling early and cheaply |
| 0:20 | [Step 4. Checkpoint](#step-4-checkpoint-4-minutes) | Stopping does not throw away finished work |
| 0:24 | [Step 5. Cost per success](#step-5-cost-per-successful-task-6-minutes) | The number to budget with |
| 0:30 | [Step 6. Alert on the rate](#step-6-alert-on-the-spending-rate-8-minutes) | A live dashboard, and an alarm going off |
| 0:38 | [The two numbers](#the-two-numbers-3-minutes) | What it would have cost, and what it costs now |
| 0:41 | [The check](#the-check-3-minutes) | Six proofs, one command |
| 0:44 | [Clean up](#clean-up-1-minute) | Switch everything off |

Rather not type? `python3 walkthrough.py` runs every command below in order, stopping
before each one until you press Enter. It is the whole session in one command.

---

## Part A: Install the tools (do this before you record)

You need four free programs. This takes 10 to 15 minutes once. If you already have them,
skip to [Check it worked](#check-it-worked).

| Program | What it is for | Needed for |
|---|---|---|
| **Python** (3.10 or newer) | runs every script in this project | everything |
| **Git** | downloads this project | everything |
| **VS Code** | lets you read the files, and has a terminal built in | everything |
| **Docker Desktop** | runs the live dashboard and the alarm | Step 6 only |

**A terminal** is a window where you type commands instead of clicking. On a Mac, open
**Terminal** (press `Cmd + Space`, type *Terminal*, press Enter). On Windows, open
**PowerShell** (press the Windows key, type *PowerShell*, press Enter). Or, in VS Code, use
**Terminal > New Terminal**. You type a command, press Enter, and it runs.

If you would rather watch than read, these two short videos go from a blank computer to Git,
Python and VS Code installed:

| macOS | Windows |
|---|---|
| [![Install on a Mac](https://img.youtube.com/vi/8ZIiXg4XOY0/hqdefault.jpg)](https://youtu.be/8ZIiXg4XOY0) | [![Install on Windows](https://img.youtube.com/vi/f091sbQSv7I/hqdefault.jpg)](https://youtu.be/f091sbQSv7I) |

### macOS

Install [Homebrew](https://brew.sh) first (copy the one line from its home page into
Terminal), then:

```bash
brew install python git
brew install --cask visual-studio-code
brew install --cask docker
```

Open **Docker** once from your Applications folder and accept its prompts. It needs to be
running (whale icon in the menu bar) for Step 6.

### Windows 10 or 11 (PowerShell)

```powershell
winget install Python.Python.3.12
winget install Git.Git
winget install Microsoft.VisualStudioCode
winget install Docker.DockerDesktop
```

Restart the computer when Docker asks. Then close and reopen PowerShell so it can find the
new programs.

> **Windows readers: one difference for the rest of this page.** Wherever you see
> `python3`, type `py` instead. Everything else is the same.

### Check it worked

```bash
python3 --version          # Windows: py --version     should say 3.10 or higher
git --version
docker --version           # only needed for Step 6
```

Each one prints a version number. If one says *command not found*, that program did not
install. Run its install line again, then close and reopen the terminal.

---

## Part B: Get the project (about 4 minutes)

**1. Download it**

```bash
git clone https://github.com/Here2ServeU/agent-cost
cd agent-cost
```

`git clone` copies the project onto your computer. `cd` ("change directory") steps into
its folder. **Run every command on this page from inside this folder.**

**2. Set it up**

macOS or Linux:

```bash
bash setup.sh
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned    # once per computer; answer Y
.\setup.ps1
.venv\Scripts\Activate.ps1
```

The setup script makes a private Python space for this project (called `.venv`), installs
the one extra package it needs, and runs the check once. The second line steps into that
private space; your prompt now starts with `(.venv)`.

> **Opened a new terminal?** Run the second line again (`source .venv/bin/activate`, or
> `.venv\Scripts\Activate.ps1` on Windows). If you see `No module named 'prometheus_client'`,
> this is what you forgot.

You should see six green **PASS** lines. It works. The rest of the session takes it apart
to show *why* it works.

**3. Start clean**

```bash
python3 reset.py
```

This wipes the run history so your numbers match this page exactly. Do it before you
record.

---

## The story you are about to watch

The agent reads invoices for a finance team. You will feed it three kinds:

| File | What it is | What it does |
|---|---|---|
| `samples/good.json` | a normal invoice | finishes in 6 steps. This is the control. |
| `samples/malformed.json` | the amount says *"one thousand four hundred and twenty dollars only (see attached)"* | **bounces**: read the amount, check it, fail, read it again. Forever. |
| `samples/drifting.json` | an invoice the agent cannot make sense of | **drifts**: tries something new every step and never finishes. The quiet, expensive one. |

There is also `samples/stuck.json`, the simplest loop: the exact same step, over and over.

---

## Step 0: The before picture (3 minutes)

```bash
python3 naive_agent.py --input samples/malformed.json --seconds 20
```

**What you will see:** steps scrolling past for twenty seconds, then something like this
(the step count depends on how fast your computer is):

```
step  373  validate:amount
step  374  parse:amount

  stopped after 374 steps because YOU stopped it, not because it finished.
  what did those steps cost?  nobody knows. nothing in this agent was counting.
```

**What it means:** this agent has no price tag, no spending limit and no way to notice it
is going in circles. `--seconds 20` is *you* pulling the plug. Overnight, nobody does.

---

## Step 1: Instrument it (4 minutes)

*Buys you: you can see it.* File: [`agent/metrics.py`](agent/metrics.py) and
[`agent/pricing.py`](agent/pricing.py).

```bash
python3 run_agent.py --input samples/good.json
```

**What you will see:**

```
  step   1  read:input             $0.0094   run total $0.0094
  step   2  parse:amount           $0.0115   run total $0.0209
  step   3  validate:amount        $0.0082   run total $0.0291
  step   4  lookup:vendor          $0.0098   run total $0.0389
  step   5  write:record           $0.0112   run total $0.0500
  step   6  final:record           $0.0115   run total $0.0615

  run 8a35a899   SUCCESS
  why          produced the required output field and passed validation
  steps        6
  cost         $0.0615
```

(The `run` code is random and will differ each time. Every other number should match.)

**What it means:** every step now has a price and a running total. AI models charge by the
*token*, roughly three quarters of a word. Words sent *in* and words sent *back* are priced
differently ($3 and $15 per million tokens here), so the agent records both. Each run is
also tagged with **which agent**, **which team pays**, and **whether it succeeded**, so the
bill has somewhere to go.

---

## Step 2: Cap it (4 minutes)

*Buys you: it is bounded.* File: [`agent/budget.py`](agent/budget.py).

To prove the spending limit works on its own, switch the loop detector **off**
(`--no-loop-detect`) and set a five-cent limit per run:

```bash
python3 run_agent.py --input samples/malformed.json --no-loop-detect --per-run-usd 0.05
```

**What you will see:**

```
  step   1  validate:amount        $0.0097   run total $0.0097
  step   2  parse:amount           $0.0130   run total $0.0227
  step   3  validate:amount        $0.0109   run total $0.0335
  step   4  parse:amount           $0.0111   run total $0.0446

  run 2c066e03   STOPPED: budget cap
  why          pre-flight: next step would cross the per-run cap
  steps        4
  cost         $0.0446
```

**What it means:** it stopped at $0.0446 against a $0.05 limit. It did not get lucky.
Before each step it asks *"can I afford one more?"*, and when the answer was no, it did not
start. There are two limits: **per run** (default $0.15) and **per day** (default $10.00),
both in [`config.json`](config.json). Think of it as a spending limit on a company card.

---

## Step 3: Detect the loop (5 minutes)

*Buys you: 6 steps, not 14.* File: [`agent/loops.py`](agent/loops.py).

Same broken invoice, everything switched back on:

```bash
python3 run_agent.py --input samples/malformed.json
```

**What you will see:**

```
  run c17b2c2e   STOPPED: loop detected
  why          bouncing: 'validate:amount' <-> 'parse:amount' for 3 cycles
  steps        6
  cost         $0.0671
```

Now try the other two kinds of loop:

```bash
python3 run_agent.py --input samples/stuck.json       # stuck: same step 3 times, $0.0332
python3 run_agent.py --input samples/drifting.json    # drifting: 12 steps of no progress, $0.1289
```

**What it means:** the spending limit works, but only once the money is spent. The loop
detector notices the agent is going in circles after a few steps and stops it, **with a
reason written in plain English**. With the spending limit as the only protection, this
invoice takes 14 steps and $0.1455. With the detector, 6 steps and $0.0671. The cheap stop
fires first; the limit is the backstop.

---

## Step 4: Checkpoint (4 minutes)

*Buys you: stopping is cheap.* File: [`agent/checkpoint.py`](agent/checkpoint.py).

Stop a *good* invoice after 3 steps, as if a protection had cut it off. Then resume it:

```bash
python3 run_agent.py --input samples/good.json --step-ceiling 3
python3 run_agent.py --input samples/good.json --resume
```

**What you will see** on the second command:

```
resuming: 3 step(s) already done, $0.0291 already spent and not paid twice
  step   4  lookup:vendor          $0.0094   run total $0.0384
  step   5  write:record           $0.0115   run total $0.0499
  step   6  final:record           $0.0082   run total $0.0582

  run 4b08ac0e   SUCCESS
  not re-paid  $0.0291  (work the checkpoint kept)
```

**What it means:** the agent saves its progress after every step. When something stops
it, the finished work is kept, and picking it back up does not pay for it again. That is
what makes it safe to set the limits tight: stopping costs you nothing you had already
bought.

---

## Step 5: Cost per successful task (6 minutes)

*Buys you: the true number.* Files: [`batch.py`](batch.py) and [`report.py`](report.py).

Run a batch of ten more invoices (six normal, four broken) on top of everything so far.
Then ask for the arithmetic:

```bash
python3 batch.py
python3 report.py --csv
```

**What you will see:**

```
  COST PER SUCCESSFUL TASK
  success means: produced the required output field and passed validation
  --------------------------------------------------------------
  runs started            17
  succeeded               8      <- the denominator
  did not                 9      <- still counts on top
  total spend             $1.0601
  --------------------------------------------------------------
  cost per request        $0.0624   (pays by the mile)
  cost per SUCCESSFUL     $0.1325   (pays for arrival)
  the gap                 112% higher, and it is the true number
  failed-run tax          $0.5714  (54% of spend)
  saved by checkpoints    $0.0291  (work not paid for twice)
```

**What it means, line by line:**

- **Cost per request** divides the whole bill by *every* run. It looks cheap, and it is
  the number most dashboards show.
- **Cost per successful task** divides the *whole* bill, failures included, by only the
  runs that **worked**. Here it is more than double. **This is the number to budget
  with**, because it is what one useful result actually costs you.
- **Failed-run tax** is the share of spend that bought nothing. Here it is high because
  this session deliberately broke the agent a lot. On a healthy system you watch it come
  down.
- The definition of "success" is printed **above** the number, every time. A number
  without its definition is a rumour.

`--csv` also writes `ledger/runs.csv`, one row per run, which opens in Excel or Google
Sheets.

---

## Step 6: Alert on the spending rate (8 minutes)

*Buys you: you find out.* Files: [`prometheus/rules/agent_alerts.yml`](prometheus/rules/agent_alerts.yml)
and [`docker-compose.yml`](docker-compose.yml). **Needs Docker Desktop running.**

**1. Start the dashboard and the alarm system** (the first time downloads about 1 GB;
do it before you record):

```bash
docker compose up -d
```

This starts three free tools in the background:
**Prometheus** (collects the numbers and sounds the alarm),
**Pushgateway** (a mailbox the agent drops its numbers into), and
**Grafana** (the charts).

**2. Open two browser tabs:**

- The alarms: **http://localhost:9090/alerts**
- The dashboard: **http://localhost:3000/d/agent-cost-four** (log in as `admin` / `admin`
  if asked; click *Skip* on the password change)

**3. Run the runaway on purpose.** This is the one dangerous command in the project:
spending limits **off**, loop detection **off**. It still has a hard ceiling of 120 steps,
and `--pace 1` makes each step take one second like a real model would, so you can watch
it happen. It takes 2 minutes.

```bash
python3 run_agent.py --input samples/malformed.json --no-caps --no-loop-detect --step-ceiling 120 --pace 1 --push --quiet
```

**What you will see:** after about 30 seconds, refresh the alerts tab. **AgentBurnRateFast**
turns yellow (*pending*), with a message like *"At the last hour's pace this is $943/month
against a $300 budget."* If spending stays that high for 5 minutes, it turns red (*firing*), which is the
moment somebody's phone would ring. The Grafana panel *"What are we spending?"* climbs while
it runs. (Tip: carry on with [the two numbers](#the-two-numbers-3-minutes) while you wait,
then come back to the alerts tab to see it go red.)

**What it means:** there are two alarms, because one cannot do both jobs.
A **fast** one watches the last hour and would wake somebody up (spending at twice the
monthly budget). A **slow** one watches the last 24 hours and raises a ticket for the
morning (spending drifting 20% over budget). They watch the *rate* of spending, not the
total, so they catch a problem while it is happening, not at month end.

> **Now switch the protections back on.** They are on by default; just do not use
> `--no-caps` again. The alarm tells you something is wrong. The spending limit is what
> actually stops it. The limit is the seatbelt; the alarm is the warning light.

---

## The two numbers (3 minutes)

```bash
python3 two_numbers.py
```

**What you will see:**

```
  BEFORE: what it would have cost   (same invoice, nothing in the way)
  cost of one step                 $0.0106   measured over 300 steps
  one step every                   3 seconds   a typical real model call
  steps per hour, per worker       1,200
  workers on the invoice queue     12
  hours until somebody notices     9.5
  = the overnight bill             $1,447.89

  NOW: what it actually costs       (a real run, all six steps on)
  stopped because                  bouncing: 'validate:amount' <-> 'parse:amount' for 3 cycles
  steps                            6
  = the cost                       $0.0671   per worker that hits it

  the bill that never arrived      $1,447.08
```

**What it means:** the first number is a projection, and every assumption is printed next
to it: 12 copies of the agent working through a queue of invoices, one step every 3
seconds, from 9 pm until somebody looks at 6:30 am. Change any of them to match your own
situation:

```bash
python3 two_numbers.py --workers 4 --hours 12 --seconds-per-step 5
```

Nobody will ever thank you for this number, because it never appears on an invoice. That
is exactly why you have to show it to them yourself.

---

## The check (3 minutes)

```bash
python3 verify.py
```

**What you will see:**

```
  1. Instrumented: cost, tokens, labels         PASS  $0.0671 over 6 steps, on agent/team/model labels
  2. Capped: per run and per day, deliberately  PASS  stopped at $0.0446 against a $0.05 cap, behaviour=drain
  3. Loop caught before the cap is reached      PASS  6 steps / $0.0671 vs 14 steps / $0.1455 on the cap alone
  4. Checkpointed: a kill wastes nothing        PASS  $0.0291 of finished work carried over, not re-paid
  5. Cost per successful task, failures on top  PASS  $0.1499 per success vs $0.0656 per request (129% higher)
  6. Alerted on burn rate, proven by triggering it PASS  $9,145/month projected at 1 step / 3s, budget $300

  All six hold.
```

**What it means:** each line switches one protection off, runs the agent for real,
measures what happened, and checks the protection made the difference. If any of the six
ever stops being true, this command fails. It also runs automatically on GitHub every time
the code changes ([`.github/workflows/verify.yml`](.github/workflows/verify.yml)), because
safety features break quietly and a failing check is the only thing that keeps this true
in six months.

(`verify.py` clears the run history and starts its own, so `python3 report.py` afterwards
shows its 17 runs: $0.2485 per request, $0.6035 per success, 90% failed-run tax.)

---

## Clean up (1 minute)

```bash
docker compose down        # stop the dashboard and alarm
python3 reset.py           # clear the run history
deactivate                 # step out of the private Python space
```

---

## If something goes wrong

| You see | What it means | Fix |
|---|---|---|
| `command not found: python3` | Python is not installed, or the terminal was opened before it was | Install it (Part A), then close and reopen the terminal. On Windows, type `py`. |
| `No module named 'prometheus_client'` | You are not inside the private Python space | `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`) |
| `running scripts is disabled on this system` (Windows) | PowerShell blocks scripts by default | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `No such file or directory: 'samples/...'` | You are in the wrong folder | `cd agent-cost` first. Every command runs from that folder. |
| Your numbers do not match this page | Earlier runs are still in the history | `python3 reset.py`, then run the steps in order |
| `STOPPED: budget cap` with `per-day cap reached` | You have run a lot today and hit the $10 daily limit. It is working. | `python3 reset.py` |
| `Cannot connect to the Docker daemon` | Docker Desktop is not open | Open Docker Desktop and wait for the whale icon to stop moving |
| `port is already allocated` | Something else is using 3000, 9090 or 9091 | `docker compose down`, close the other program, try again |
| `metrics  not pushed (URLError)` | The dashboard is not running. The agent still ran fine. | `docker compose up -d` |
| The alarm stays at *pending* | It needs 5 minutes over the line before it fires | Wait, or run the runaway command again |

---

## What is in the folder

| File | Step | In plain English |
|---|---|---|
| `naive_agent.py` | 0 | the agent before any protection |
| `run_agent.py` | 1 to 6 | the protected agent; flags switch each protection off |
| `agent/pricing.py` | 1 | the price list, in one place, so a price change is a one-line edit |
| `agent/metrics.py` | 1 | records cost, tokens, which agent, which team, did it succeed |
| `agent/budget.py` | 2 | the per-run and per-day spending limits |
| `agent/loops.py` | 3 | spots *stuck*, *bouncing* and *drifting* |
| `agent/checkpoint.py` | 4 | saves progress after every step |
| `agent/ledger.py` | 5 | one line per run, added and never edited, like a ledger |
| `agent/runner.py` | all | the loop that puts the six together, in the order they must fire |
| `agent/llm.py` | | the simulated AI model; swap this for a real one and nothing else changes |
| `batch.py`, `report.py` | 5 | a mixed batch of work, then the arithmetic |
| `prometheus/`, `grafana/` | 6 | the alarm rules and the dashboard |
| `two_numbers.py` | | the bill that never arrived |
| `verify.py` | | the six proofs |
| `walkthrough.py` | | the whole session, one keypress at a time |
| `config.json` | | the settings: limits, step ceiling, which protections are on |
| `setup.sh`, `setup.ps1`, `reset.py` | | set up, and start clean |

Engineers: read [`agent/runner.py`](agent/runner.py) top to bottom. Every protection appears
exactly once, in the order it has to fire: **record the step, save the checkpoint, check
for a loop, check the cap.** Record first, because you want the cost of the step that
stopped you. Loop before cap, because the cheap stop should fire before the expensive one.

---

## Try it yourself

1. **Break the order.** In `agent/runner.py`, move the "record it" lines below the cap
   check. Can you still say what the last step cost?
2. **Switch one protection off.** Any one. Write down what the number became.
3. **Tighten the limit.** Halve `per_run_usd` in `config.json`. What stops succeeding? Do
   you care?
4. **Add a fourth loop shape** that your own agent does, in `agent/loops.py` and `verify.py`.
5. **Make the check fail on purpose** once, so you know the failure is visible.
6. **Swap in a real model** by replacing `SimulatedModel` in `agent/llm.py`. Nothing else
   should need to change.
7. **Write down your two numbers**, uncapped and today's, somewhere you can find them.

---

## The idea worth keeping

Every one of these six is a decision made **earlier**:

- **A spending limit** decides what a task is worth *before* it runs, not after.
- **A step limit** decides how long is too long while you are calm, not during an incident.
- **A definition of success** decides what you mean *before* you report a number, not in a
  meeting.
- **A checkpoint** decides that stopping should be cheap, before you need to stop.

None of these are hard in advance. All of them are hard at three in the morning.

**Decide early. Write it down. Let a machine enforce it.**

---

Made by [Here2ServeU](https://github.com/Here2ServeU) · Emmanuel Naweji ·
MIT [licence](LICENSE)
