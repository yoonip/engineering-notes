"""Account for example coverage cells; never connects to a DUT."""
import csv
from collections import Counter
from pathlib import Path

rows = list(csv.DictReader(Path(__file__).with_name(
    "coverage_example.csv").open(encoding="utf-8", newline="")))
keys = [(r["requirement"], r["corner"]) for r in rows]
if len(keys) != len(set(keys)):
    raise ValueError("This summary requires one final row per coverage cell")
counts = Counter(r["status"] for r in rows)
allowed = {"PASS", "DUT_FAIL", "INFRA_ERROR", "NOT_RUN", "UNSUPPORTED"}
if set(counts) - allowed:
    raise ValueError("Unknown status; do not silently classify missing evidence")
# Legal unsupported combinations are documented exclusions, not tested cells.
planned = len(rows) - counts["UNSUPPORTED"]
executed = planned - counts["NOT_RUN"]
valid = counts["PASS"] + counts["DUT_FAIL"]
print(f"MODEL ONLY: planned={planned}, executed={executed}, valid={valid}")
print(dict(counts))
print(f"attempt coverage={executed}/{planned} = {executed/planned:.1%}")
print(f"valid coverage={valid}/{planned} = {valid/planned:.1%}")
print(f"conditional pass={counts['PASS']}/{valid} = "
      f"{counts['PASS']/valid:.1%}")
print("Repetitions and distinct coverage cells need separate denominators.")
