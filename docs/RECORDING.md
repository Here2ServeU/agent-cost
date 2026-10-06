# Run Sheet: Recording This in 30 to 45 Minutes

For the presenter. The README is what viewers follow; this page is what you keep open
beside it.

---

## The day before

- [ ] Python, Git, VS Code and Docker Desktop installed ([README Part A](../README.md#part-a-install-the-tools-do-this-before-you-record))
- [ ] Project cloned and `bash setup.sh` (Windows: `.\setup.ps1`) run once: six PASS lines
- [ ] `docker compose up -d` run once, so the ~1 GB download is already done, then
      `docker compose down`

## Ten minutes before you hit record

- [ ] Docker Desktop open, whale icon steady
- [ ] Terminal open **in the project folder**, `(.venv)` showing at the prompt
- [ ] `python3 reset.py`, so every number matches the README
- [ ] `docker compose up -d`, so the dashboard is warm when you get to Step 6
- [ ] Browser tabs ready but hidden: `http://localhost:9090/alerts` and
      `http://localhost:3000/d/agent-cost-four`
- [ ] Terminal font size 18 or larger; window wide enough that lines do not wrap
- [ ] Notifications off (macOS: Focus > Do Not Disturb; Windows: Focus assist)
- [ ] `clear` the terminal

Or drive the whole session with `python3 walkthrough.py`: it shows each command, waits for
Enter, runs it, then prints one line on what it meant. Good if you would rather talk than
type.

---

## The session

| Clock | Section | Type | Say |
|---|---|---|---|
| 0:00 | Intro | | "One agent, one looping input, six steps. Every one of them proven by running it." |
| 0:02 | Setup | `bash setup.sh` · `source .venv/bin/activate` · `python3 reset.py` | "Offline, free, the same numbers every time. The model is simulated, so nothing here costs money." |
| 0:04 | **0. Before** | `python3 naive_agent.py --input samples/malformed.json --seconds 20` | "It ends because I killed it, not because it finished. Not one number on that screen says what it cost." |
| 0:07 | **1. Instrument** | `python3 run_agent.py --input samples/good.json` | "Every step now has a price. Four labels: agent, team, run, result. Run is *not* a metric label; it lives in the ledger." |
| 0:11 | **2. Cap** | `python3 run_agent.py --input samples/malformed.json --no-loop-detect --per-run-usd 0.05` | "$0.0446 against a $0.05 cap. It did not get lucky; it declined to start a step it could not afford to finish." |
| 0:15 | **3. Loop** | `python3 run_agent.py --input samples/malformed.json`, then `stuck.json`, `drifting.json` | "6 steps and seven cents, against 14 steps on the cap alone. The cheap stop fires before the expensive one. That is the whole ordering rule." |
| 0:20 | **4. Checkpoint** | `... samples/good.json --step-ceiling 3`, then `... --resume` | "$0.0291 not re-paid. Without this, every stop you build costs you a restart." |
| 0:24 | **5. Cost per success** | `python3 batch.py` · `python3 report.py --csv` | "Failures go on the top. Cost per request pays by the mile; cost per success pays for arrival." |
| 0:30 | **6. Alert** | runaway command (below), then switch to the browser | "The only dangerous command in the course. Caps off, once, with the ceiling on." |
| 0:32 | | refresh `localhost:9090/alerts` | "Pending. Five minutes of this and somebody's phone rings. The cap is the seatbelt; the alert is the warning light." |
| 0:33 | **The two numbers** | `python3 two_numbers.py` | "Fourteen hundred dollars, minus seven cents. Nobody will ever send you that invoice." |
| 0:37 | | back to `localhost:9090/alerts` | "Firing. That is the page somebody would have got, and the cap would still have stopped it." |
| 0:41 | **The check** | `python3 verify.py` | "Six PASS lines. Safe to leave overnight, not because I said so, but because the thing that would have hurt you was tried and stopped." |
| 0:43 | Close | `docker compose down` | "Decide early. Write it down. Let a machine enforce it." |

The Step 6 runaway command:

```bash
python3 run_agent.py --input samples/malformed.json --no-caps --no-loop-detect --step-ceiling 120 --pace 1 --push --quiet
```

It takes two minutes. Start it, then switch to the browser and talk over the climbing
chart. The fast alert goes **pending** about 30 seconds in and turns **firing** five
minutes after that. To show it red on screen, do *the two numbers* while you wait, then go
back to the alerts tab. (Do not start the runaway earlier, before Step 5: it would land in
the ledger and change the report's numbers.)

---

## Numbers you will see (after `reset.py`, steps in order)

| Where | Number |
|---|---|
| Step 1, good invoice | 6 steps, $0.0615 |
| Step 2, capped at $0.05 | 4 steps, $0.0446 |
| Step 3, bouncing caught | 6 steps, $0.0671 |
| Step 3, stuck / drifting | 3 steps $0.0332 / 12 steps $0.1289 |
| Step 4, not re-paid | $0.0291 |
| Step 5, report | 17 runs, 8 succeeded; $0.0624 per request, $0.1325 per success, 54% failed-run tax |
| Step 6, fast alert | pending at roughly $900+/month projected vs $300 budget |
| Two numbers | $1,447.89 overnight vs $0.0671 |
| verify.py | $0.0671 / 6 · $0.0446 · 6 vs 14 · $0.0291 · 129% · $9,145/mo vs $300 |

The run ID (`run 8a35a899`) is random every time; everything else is fixed.

## If it goes wrong on camera

- **Numbers do not match:** you skipped `reset.py`. Say so, run it, carry on.
- **`not pushed (URLError)`:** Docker is not up. `docker compose up -d`, wait 10 seconds,
  run the runaway again.
- **Grafana asks for a password:** `admin` / `admin`, then *Skip*.
- **Lost your place:** `python3 walkthrough.py --from 4` picks up at Step 4.
