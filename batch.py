#!/usr/bin/env python3
"""STEP 5, PART ONE: A MIXED BATCH, SO THE REPORT HAS SOMETHING TO SAY.

    python3 batch.py

Runs ten invoices through the safe agent: six normal ones that succeed
and four broken ones that loop and get stopped. They are added to the
ledger on top of everything you already ran today, because a real day
is like that: most work goes fine, some of it does not, and all of it
is on the bill.

Then run `python3 report.py` to see what that day really cost.
"""
from __future__ import annotations

from agent.runner import Config, SafeAgent

GOOD, LOOPING = "samples/good.json", "samples/malformed.json"
BATCH = [GOOD] * 6 + [LOOPING] * 4


def main() -> None:
    print(f"\n  running a batch of {len(BATCH)} invoices: 6 normal, 4 broken\n")
    for i, task in enumerate(BATCH, 1):
        r = SafeAgent(Config.load(), verbose=False).run(task)
        print(f"  {i:>2}. {task:<24} {r.result:<8} {r.steps:>3} steps   ${r.cost_usd:.4f}")
    print("\n  done. now run:  python3 report.py\n")


if __name__ == "__main__":
    main()
