# Glossary: Every Word in This Project, in Plain English

## The money words

**Token**: the unit AI models charge by, roughly three quarters of a word. "Invoice
number 4471" is about five tokens.

**Input tokens / output tokens**: words sent *to* the model and words it sends *back*.
They are priced differently. Here, input is $3 and output is $15 per million tokens. Never
average them into one price.

**Step**: one question to the AI model and its answer. One paid call. A normal invoice
takes 6 steps.

**Run**: one attempt at one task, from the first step to the last.

**Cost per request**: total spend divided by every run. It looks cheap because the failures
are spread across everything.

**Cost per successful task**: total spend, failures included, divided by only the runs that
worked. The real cost of one useful result, and the number to budget with.

**Failed-run tax**: the share of spend that went to runs that did not succeed. Money that
bought nothing.

**Burn rate**: how fast money is going out, such as dollars per hour, projected to a month.

**The bill that never arrived**: the difference between what a runaway would have cost and
what it costs with the protections on. It never shows up on an invoice, so you have to
show it to people yourself.

## The protection words

**Instrumenting**: making the agent record what every step cost, and who it was for.

**Label**: a tag on every cost, like a cost-centre code. This project uses four: *agent*
(which one), *team* (who pays), *run* (which attempt) and *result* (did it work).

**Cap / budget cap**: a spending limit. *Per run* limits one task; *per day* limits the
total for the day.

**Pre-flight check**: before each step, the agent estimates whether it can afford one more.
If not, it does not start. That is why it stops *under* the limit, not over it.

**Drain / stop / kill**: three ways to behave when a limit is reached. *Drain* (the
default) finishes the current step, saves everything and stops cleanly. *Stop* finishes the
step without saving. *Kill* stops immediately.

**Step ceiling**: the maximum number of steps any run may take, whatever else happens. The
last line of defence.

**Loop**: the agent going round in circles without making progress. Three kinds:

- **Stuck**: the same step, again and again.
- **Bouncing**: two steps taking turns, each undoing the other (read the amount, check it,
  fail, read it again).
- **Drifting**: always trying something new, never finishing. The quiet, expensive one,
  because every step looks like progress.

**Checkpoint**: a save point written after every finished step, so a stopped run can pick
up where it left off without paying for the finished part again.

**Atomic write**: saving a file by writing a temporary copy and then swapping it in, all at
once. A half-written save is worse than none.

**Definition of success**: the written rule for what counts as "worked". Here: *produced
the required output field and passed validation*. It is printed next to every number.

**Ledger**: a file with one line per run, only ever added to, never edited. The dashboard
says what is happening now; the ledger says what happened, for the meeting three weeks
later.

**Alert / alarm**: an automatic warning. **Fast** looks at the last hour and pages someone.
**Slow** looks at the last 24 hours and raises a ticket.

**Pending / firing**: an alarm is *pending* when the condition has just become true, and
*firing* once it has stayed true long enough (5 minutes for the fast alarm). Firing is when
someone gets notified.

**Proof by turning it off**: running with one protection switched off to measure what it
was buying you. Every check in `verify.py` works this way.

## The computer words

**Terminal / PowerShell**: a window where you type commands instead of clicking.

**Command**: one line you type into the terminal and run with Enter.

**Python**: the programming language every script here is written in. `python3 file.py`
(or `py file.py` on Windows) runs a file.

**Script**: a file of instructions the computer runs from top to bottom. Every `.py` file
here is one.

**Flag**: an option added to a command, starting with `--`. For example, `--no-caps`
switches the spending limits off.

**Folder / directory**: the same thing. `cd agent-cost` means "go into the agent-cost
folder".

**Git / GitHub / clone**: Git keeps track of versions of a project. GitHub is a website
that hosts projects. *Cloning* copies one onto your computer.

**Virtual environment (`.venv`)**: a private space for this project's Python add-ons, so
they do not interfere with anything else on your computer. "Activating" it means stepping
inside; your prompt then starts with `(.venv)`.

**Package**: an add-on for Python. This project needs one, `prometheus-client`.

**JSON**: a plain-text format for data. The sample invoices and `config.json` use it.

**CSV**: a plain-text table that opens in Excel or Google Sheets.

**Simulated model**: a stand-in for a real AI model that gives realistic answers and token
counts without calling anything or costing anything.

**Docker**: a tool that runs other programs in sealed boxes called *containers*, so you do
not have to install them yourself.

**Prometheus**: free software that collects numbers over time and sounds alarms.

**Pushgateway**: a mailbox. The agent drops its numbers there and Prometheus collects them.
Needed because each run only lasts a few seconds.

**Grafana**: free software that turns those numbers into charts. The dashboard here has four
panels, each titled with a question someone actually asks: *What are we spending? What is it
buying us? Who is spending it? How much is wasted?*

**Cardinality bomb**: a tag that gets a new value on every run, like a run ID used as a
Prometheus label. It quietly overloads the monitoring system. That is why the run ID lives
in the ledger instead.

**localhost**: your own computer. `http://localhost:3000` is a web page served by a program
on your machine, not the internet.

**CI (continuous integration)**: GitHub running `verify.py` automatically every time the
code changes, so a broken protection gets noticed the same day.
