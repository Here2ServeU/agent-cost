#!/usr/bin/env python3
"""STEP 0: THE BEFORE PICTURE.

This is the agent you start with. It is honest about nothing.

It has no cost accounting, no cap, no loop detection, no checkpoints,
no definition of success and no alert. It will happily run until you
notice, which on a Tuesday night means until the morning.

Run it against the looping input and watch it never stop:

    python3 naive_agent.py --input samples/malformed.json --seconds 20

`--seconds 20` is you, pulling the plug after twenty seconds. It is not
part of the agent; the agent itself has no idea when to stop. (On Linux
you can use `timeout 20 python3 naive_agent.py ...` instead. Without
either, press Ctrl+C.)

You will see steps go by. You will not see a single number that tells
you what those steps cost. That is the whole problem.
"""
import argparse
import json
import time

from agent.llm import SimulatedModel


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--seconds", type=float,
                    help="pull the plug after this many seconds (you stopping it, not the agent)")
    args = ap.parse_args()

    task = json.loads(open(args.input).read())
    model = SimulatedModel(task)
    started = time.time()

    step = 0
    try:
        while True:                       # no ceiling. none. this is the bug.
            step += 1
            action, _usage = model.next_action()
            print(f"step {step:>4}  {action['type']}:{action['target']}")
            if action["type"] == "final":
                print("done")
                return
            if args.seconds and time.time() - started >= args.seconds:
                break
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    print()
    print(f"  stopped after {step} steps because YOU stopped it, not because it finished.")
    print("  what did those steps cost?  nobody knows. nothing in this agent was counting.")
    print()


if __name__ == "__main__":
    main()
