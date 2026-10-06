#!/usr/bin/env python3
"""THE WHOLE THING, IN ORDER, ONE KEYPRESS AT A TIME.

    python3 walkthrough.py               # pauses before every step; press Enter to go on
    python3 walkthrough.py --no-pause    # runs straight through
    python3 walkthrough.py --from 4      # start at step 4

Runs exactly the commands in the README, in the README's order, with a
plain-English line before each one saying what to look for and a line
after saying what it meant. If you would rather not type, this is the
whole session.

It starts by clearing the ledger, so your numbers match the README.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import urllib.request

PY = sys.executable          # the same Python that is running this, venv included
BOLD, DIM, GOLD, OFF = "\033[1m", "\033[2m", "\033[93m", "\033[0m"


def pushgateway_up() -> bool:
    try:
        urllib.request.urlopen("http://localhost:9091/-/ready", timeout=1)
        return True
    except Exception:  # noqa: BLE001
        return False


def runaway_command() -> list[str]:
    base = ["run_agent.py", "--input", "samples/malformed.json", "--no-caps", "--no-loop-detect"]
    if pushgateway_up():
        return base + ["--step-ceiling", "120", "--pace", "1", "--push", "--quiet"]
    print(f"  {DIM}(Docker is not running, so this runs without the dashboard. "
          f"Start it with: docker compose up -d){OFF}")
    return base + ["--quiet"]


# (step, title, what to look for, commands, what it meant)
STEPS = [
    (0, "The before picture",
     "An agent with nothing in it that can stop it. Watch the steps go by. Look for a price.",
     [["naive_agent.py", "--input", "samples/malformed.json", "--seconds", "10"]],
     "It only stopped because the timer pulled the plug. Not one number said what it cost."),

    (1, "Instrument it: you can see it",
     "The same kind of agent, now writing down what every step cost.",
     [["run_agent.py", "--input", "samples/good.json"]],
     "Every line has a price, and there is a running total. A normal invoice: about six cents."),

    (2, "Cap it: it is bounded",
     "The broken invoice, with loop detection switched OFF, so only the $0.05 spending cap can stop it.",
     [["run_agent.py", "--input", "samples/malformed.json", "--no-loop-detect", "--per-run-usd", "0.05"]],
     "It stopped just under five cents. It refused to start a step it could not afford to finish."),

    (3, "Detect the loop: 6 steps, not 14",
     "The same broken invoice, everything back on. Then the other two ways an agent goes round in circles.",
     [["run_agent.py", "--input", "samples/malformed.json"],
      ["run_agent.py", "--input", "samples/stuck.json"],
      ["run_agent.py", "--input", "samples/drifting.json"]],
     "Caught in 6 steps for $0.0671, and it says why in plain words. "
     "The cap alone took 14 steps and $0.1455. Cheap stop first."),

    (4, "Checkpoint: stopping is cheap",
     "Stop a good invoice after three steps, as if something killed it. Then pick it back up.",
     [["run_agent.py", "--input", "samples/good.json", "--step-ceiling", "3"],
      ["run_agent.py", "--input", "samples/good.json", "--resume"]],
     "'not re-paid $0.0291': the work that was already done, and was not bought twice."),

    (5, "Cost per successful task: the true number",
     "Ten more invoices, six fine and four broken, on top of everything run so far. Then the arithmetic.",
     [["batch.py"], ["report.py", "--csv"]],
     "Cost per SUCCESSFUL task is the number to budget with. The failed-run tax is the share of "
     "spend that bought nothing."),

    (6, "Alert on the rate: you find out",
     "The one dangerous command: caps OFF, loop detection OFF, on purpose, once. "
     "If Docker is up, open http://localhost:9090/alerts and http://localhost:3000 while it runs.",
     [None],                                # filled in at run time
     "Nothing stopped it but the step ceiling, and the spending rate went straight past the alert "
     "line. In real life the caps stay on: the alert tells you, the cap is what stops it."),

    (7, "The bill that never arrived",
     "Two numbers: what that broken invoice would have cost overnight, and what it costs now.",
     [["two_numbers.py"]],
     "Fourteen hundred dollars, minus seven cents. Nobody will ever send you that invoice."),

    (8, "The check",
     "Six claims, six proofs. Each one turns a protection off, measures, and turns it back on.",
     [["verify.py"]],
     "Six PASS lines. Safe to leave running overnight, because the thing that would have hurt "
     "you was tried and stopped."),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pause", action="store_true")
    ap.add_argument("--from", dest="start", type=int, default=0)
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)     # keep our lines in order with the scripts'

    if a.start == 0:
        subprocess.run([PY, "reset.py"])

    for n, title, before, commands, after in STEPS:
        if n < a.start:
            continue
        label = f"STEP {n}" if 1 <= n <= 6 else ("BEFORE" if n == 0 else "FINALE")
        print(f"\n{GOLD}{'=' * 72}{OFF}\n  {BOLD}{label}: {title}{OFF}\n  {before}\n")
        for cmd in commands:
            cmd = cmd or runaway_command()
            print(f"  {DIM}${OFF} {BOLD}python3 {' '.join(cmd)}{OFF}")
            if not a.no_pause:
                input(f"  {DIM}press Enter to run it{OFF} ")
            subprocess.run([PY, *cmd])
        print(f"  {GOLD}what that meant:{OFF} {after}")
        if not a.no_pause:
            input(f"\n  {DIM}press Enter for the next step{OFF} ")

    print(f"\n  {BOLD}Decide early. Write it down. Let a machine enforce it.{OFF}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
