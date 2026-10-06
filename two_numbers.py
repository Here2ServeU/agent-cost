#!/usr/bin/env python3
"""THE BILL THAT NEVER ARRIVED.

    python3 two_numbers.py

Two numbers, worked out in front of you:

  1. What the looping invoice would have cost overnight with nothing
     in the way. Measured from the real per-step cost, then projected
     with the assumptions printed next to it. Change any of them with
     a flag; the arithmetic is the point, not the default values.

  2. What the same invoice costs now, with all six steps switched on.
     A real run, not a projection.

    python3 two_numbers.py --hours 9.5 --seconds-per-step 3 --workers 12
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.llm import SimulatedModel
from agent.pricing import cost_usd
from agent.runner import Config, SafeAgent

LOOPING = "samples/malformed.json"
RED, GREEN, GOLD, DIM, OFF = "\033[91m", "\033[92m", "\033[93m", "\033[2m", "\033[0m"


def runaway_cost_per_step(model: str, steps: int = 300) -> float:
    """The naive agent's loop, priced. No ledger, no caps, nothing in the way."""
    sim = SimulatedModel(json.loads(Path(LOOPING).read_text()), model)
    total = 0.0
    for _ in range(steps):
        _action, usage = sim.next_action()
        total += cost_usd(model, usage["input_tokens"], usage["output_tokens"])
    return total / steps


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=9.5,
                    help="hours until somebody notices (default 9.5: 9 pm to 6:30 am)")
    ap.add_argument("--seconds-per-step", type=float, default=3.0,
                    help="how long one real model call takes (default 3)")
    ap.add_argument("--workers", type=int, default=12,
                    help="copies of the agent working through the invoice queue (default 12)")
    a = ap.parse_args()

    cfg = Config.load()
    per_step = runaway_cost_per_step(cfg.model)
    steps_per_hour = 3600 / a.seconds_per_step
    would_have = per_step * steps_per_hour * a.workers * a.hours

    now = SafeAgent(cfg, verbose=False).run(LOOPING)

    print()
    print(f"  {RED}BEFORE: what it would have cost{OFF}   {DIM}(same invoice, nothing in the way){OFF}")
    print(f"  cost of one step                 ${per_step:.4f}   {DIM}measured over 300 steps{OFF}")
    print(f"  one step every                   {a.seconds_per_step:g} seconds   {DIM}a typical real model call{OFF}")
    print(f"  steps per hour, per worker       {steps_per_hour:,.0f}")
    print(f"  workers on the invoice queue     {a.workers}")
    print(f"  hours until somebody notices     {a.hours:g}")
    print(f"  {RED}= the overnight bill             ${would_have:,.2f}{OFF}")
    print()
    print(f"  {GREEN}NOW: what it actually costs{OFF}       {DIM}(a real run, all six steps on){OFF}")
    print(f"  stopped because                  {now.reason}")
    print(f"  steps                            {now.steps}")
    print(f"  {GREEN}= the cost                       ${now.cost_usd:.4f}{OFF}   {DIM}per worker that hits it{OFF}")
    print()
    print(f"  {GOLD}the bill that never arrived      ${would_have - now.cost_usd * a.workers:,.2f}{OFF}")
    print(f"  {DIM}nobody will thank you for that number; it never appears on an invoice.{OFF}")
    print(f"  {DIM}which is exactly why you have to show it to them yourself.{OFF}")
    print()


if __name__ == "__main__":
    main()
