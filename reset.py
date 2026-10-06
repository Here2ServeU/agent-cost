#!/usr/bin/env python3
"""START CLEAN.

    python3 reset.py

Deletes the ledger folder: the run history, the daily spend file and
any saved checkpoints. Nothing else is touched. Run it before you
record or present, so every number on screen matches the README.
"""
import shutil
from pathlib import Path

if Path("ledger").exists():
    shutil.rmtree("ledger")
    print("ledger cleared. every number starts from zero.")
else:
    print("nothing to clear; the ledger is already empty.")
