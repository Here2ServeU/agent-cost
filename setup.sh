#!/usr/bin/env bash
# One-time setup for macOS and Linux.
#
#   bash setup.sh
#
# Makes a private Python box for this project (.venv), installs the one
# package it needs, and runs the six-proof check so you know it works.

set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. See 'Install the tools' in README.md."
  exit 1
fi

echo "1/3  making a private Python box for this project (.venv)"
python3 -m venv .venv

echo "2/3  installing the one package it needs (prometheus-client)"
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements.txt

echo "3/3  running the check"
.venv/bin/python verify.py
.venv/bin/python reset.py >/dev/null

echo
echo "Ready. In every new terminal window, first run:"
echo "    source .venv/bin/activate"
