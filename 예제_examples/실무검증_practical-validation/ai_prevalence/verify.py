"""Compare fixed synthetic scores with independent counts and exact ratios."""
import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys

from model import (ContractError, MUTATIONS, evaluate_bundle, evaluate_cohort,
                   load_fixture, validate_document)


class Checks:
    def __init__(self):
        self.count = 0
        self.rejections = 0
        self.issues = []
        self.observations = {}

    def equal(self, label, actual, expected):
        self.count += 1
        if actual != expected:
            self.issues.append({"case": label, "actual": actual, "expected": expected})

    def reject(self, label, action, code):
        self.count += 1
        try:
            actual = action()
        except ContractError as error:
            self.rejections += 1
            if error.code != code:
                self.issues.append({"case": label, "actual": error.code, "expected": code})
        except Exception as error:
            self.issues.append({"case": label, "unexpected_exception": repr(error), "expected": code})
        else:
            self.issues.append({"case": label, "accepted": actual, "expected": code})


POLICY = {"threshold": 0.5, "selection": "fixed-before-evaluation"}
COST = {"false_positive": 1, "false_negative": 20}


def row(identifier, score, label):
    return {"id": identifier, "score": score, "label": label}


def small(rows, name="edge"):
    return {"id": name, "rows": rows}


def fraction_value(value):
    if value["denominator"] == 0:
        return None
    return str(Fraction(value["numerator"], value["denominator"]))


def suite(document, mutation, out):
    c = Checks()

    def evaluate(cohort, policy=None, cost=None):
        return evaluate_cohort(cohort, POLICY if policy is None else policy,
                               COST if cost is None else cost, mutation=mutation)

    before = copy.deepcopy(document)
    results = evaluate_bundle(document, mutation=mutation)
    c.equal("input object remains unchanged", document, before)
    c.equal("fixture cohort IDs", [item["cohort_id"] for item in results], ["A", "B"])
    # These literals are not produced by the model, the fixture, or an estimator.
    expected = (
        ("A", 200, {"tp": 90, "fn": 10, "fp": 10, "tn": 90}, 100,
         {"precision": "9/10", "recall": "9/10", "fpr": "1/10", "accuracy": "9/10", "prevalence": "1/2"}, 210, "21/20"),
        ("B", 1000, {"tp": 9, "fn": 1, "fp": 99, "tn": 891}, 108,
         {"precision": "1/12", "recall": "9/10", "fpr": "1/10", "accuracy": "9/10", "prevalence": "1/100"}, 119, "119/1000"),
    )
    for actual, (name, count, matrix, alarms, rates, cost, average) in zip(results, expected):
        c.equal(name + " established", actual["status"], "METRICS_ESTABLISHED")
        c.equal(name + " sample count", actual["sample_count"], count)
        c.equal(name + " known labels", actual["known_labels"], count)
        c.equal(name + " missing labels", actual["missing_labels"], 0)
        c.equal(name + " matrix", actual["confusion"], matrix)
        c.equal(name + " alarms", actual["alarms"], alarms)
        c.equal(name + " fixed threshold", actual["threshold_used"], 0.5)
        c.equal(name + " threshold origin", actual["threshold_origin"], "fixed-before-evaluation")
        for metric, exact in rates.items():
            observed = actual["metrics"][metric]
            c.equal(name + " " + metric + " exact", fraction_value(observed), exact)
            c.equal(name + " " + metric + " float", observed["value"], float(Fraction(exact)))
        c.equal(name + " precision population", actual["metrics"]["precision"]["denominator"], alarms)
        c.equal(name + " own total cost", actual["cost_total"], cost)
        c.equal(name + " cost per sample", fraction_value(actual["cost_per_sample"]), average)
    c.observations["cohorts"] = results
    reversed_document = copy.deepcopy(document)
    for cohort in reversed_document["cohorts"]:
        cohort["rows"].reverse()
    c.equal("row order does not change counts", evaluate_bundle(reversed_document, mutation=mutation), results)

    # The algebra is an independent arithmetic check, not a prevalence estimator.
    for name, prevalence, precision in (("A", Fraction(1, 2), Fraction(9, 10)),
                                        ("B", Fraction(1, 100), Fraction(1, 12))):
        numerator = Fraction(9, 10) * prevalence
        denominator = numerator + Fraction(1, 10) * (1 - prevalence)
        c.equal(name + " base-rate identity", str(numerator / denominator), str(precision))

    unknown = small([row("u1", 0.8, None), row("u2", 0.2, None)], "unlabeled")
    partial = small([row("p1", 0.8, 1), row("p2", 0.2, None)], "partial")
    for name, cohort, known, missing in (("unlabeled", unknown, 0, 2), ("partial", partial, 1, 1)):
        result = evaluate(cohort)
        c.equal(name + " status", result["status"], "METRICS_NOT_ESTABLISHED")
        c.equal(name + " labels", (result["known_labels"], result["missing_labels"]), (known, missing))
        c.equal(name + " observable alarms", result["alarms"], 1)
        for key in ("confusion", "metrics", "cost_total", "cost_per_sample"):
            c.equal(name + " no guessed " + key, result[key], None)
        c.observations[name] = result

    boundary = small([row("x0", 0, 0), row("x1", 0.5, 1), row("x2", 1, 1)])
    actual = evaluate(boundary)
    c.equal("threshold equality is positive", actual["confusion"], {"tp": 2, "fn": 0, "fp": 0, "tn": 1})
    for threshold, alarms in ((0, 3), (1, 1)):
        policy = dict(POLICY, threshold=threshold)
        c.equal("inclusive unit threshold " + str(threshold), evaluate(boundary, policy)["alarms"], alarms)
    empty = evaluate(small([]))
    c.equal("empty cohort status", empty["status"], "METRICS_NOT_ESTABLISHED")
    c.equal("empty alarm denominator", empty["alarm_rate"], {"numerator": 0, "denominator": 0, "value": None})
    c.equal("empty metrics", empty["metrics"], None)
    no_alarms = evaluate(small([row("n1", 0.2, 0), row("n2", 0.2, 1)]))
    c.equal("undefined precision", no_alarms["metrics"]["precision"]["value"], None)
    c.equal("zero recall is defined", no_alarms["metrics"]["recall"]["value"], 0.0)
    all_negative = evaluate(small([row("n", 0.8, 0)]))
    c.equal("undefined recall", all_negative["metrics"]["recall"]["value"], None)
    all_positive = evaluate(small([row("p", 0.8, 1)]))
    c.equal("undefined FPR", all_positive["metrics"]["fpr"]["value"], None)
    c.equal("zero own costs", evaluate(boundary, cost={"false_positive": 0, "false_negative": 0})["cost_total"], 0)
    c.observations["zero_denominators"] = {"empty": empty, "no_alarms": no_alarms,
                                          "all_negative": all_negative, "all_positive": all_positive}

    leak = small([row("l1", 0.9, 1), row("l2", 0.49, 1),
                  row("l3", 0.6, 0), row("l4", 0.1, 0)], "tuning_boundary")
    fixed = evaluate(leak)
    c.equal("fixed boundary matrix", fixed["confusion"], {"tp": 1, "fn": 1, "fp": 1, "tn": 1})
    c.equal("fixed boundary cost", fixed["cost_total"], 21)
    c.equal("fixed boundary threshold", fixed["threshold_used"], 0.5)
    leaky_policy = dict(POLICY, selection="test-labels")
    c.reject("evaluation labels cannot select threshold", lambda: evaluate(leak, leaky_policy),
             "EVALUATION_LABEL_TUNING_FORBIDDEN")
    # Always retain the wrong-path observation, even during the normal run.
    wrong = evaluate_cohort(leak, leaky_policy, COST, mutation="retune-on-test-labels")
    c.equal("leaky contrast actually changes threshold", wrong["threshold_used"], 0.49)
    c.equal("leaky contrast actually changes cost", wrong["cost_total"], 1)
    c.observations["threshold_boundary"] = {"fixed": fixed, "leaky_error_contrast": wrong}

    for bad in (True, False, "0.5", None, float("nan"), float("inf"), float("-inf"), -0.01, 1.01, 10 ** 1000):
        c.reject("score type/range " + repr(bad), lambda bad=bad: evaluate(small([row("x", bad, 0)])), "UNIT_NUMBER")
        c.reject("threshold type/range " + repr(bad), lambda bad=bad: evaluate(boundary, dict(POLICY, threshold=bad)), "UNIT_NUMBER")
    for bad in (True, False, -1, 2, 0.0, "1", [], {}):
        c.reject("class type/range " + repr(bad), lambda bad=bad: evaluate(small([row("x", 0.5, bad)])), "CLASS")
    for bad in ("", "a b", "../x", "x" * 33, True, 1, None):
        c.reject("identifier " + repr(bad), lambda bad=bad: evaluate(small([row(bad, 0.5, 0)])), "IDENTIFIER")
    c.reject("missing ID", lambda: evaluate(small([{"score": 0.5, "label": 0}])), "FIELDS")
    c.reject("missing score", lambda: evaluate(small([{"id": "x", "label": 0}])), "FIELDS")
    c.reject("missing label key", lambda: evaluate(small([{"id": "x", "score": 0.5}])), "FIELDS")
    c.reject("extra row field", lambda: evaluate(small([dict(row("x", 0.5, 0), other=1)])), "FIELDS")
    c.reject("duplicate ID", lambda: evaluate(small([row("x", 0.1, 0), row("x", 0.9, 1)])), "DUPLICATE_ID")
    c.reject("rows type", lambda: evaluate(small({})), "ROWS")
    c.reject("row type", lambda: evaluate(small([[]])), "FIELDS")
    c.reject("cohort type", lambda: evaluate([]), "FIELDS")
    c.reject("cohort ID", lambda: evaluate(small([], "bad id")), "IDENTIFIER")
    c.reject("too many rows", lambda: evaluate(small([row(f"z{i}", 0.5, 0) for i in range(2001)])), "ROWS")
    max_rows = small([row(f"z{i}", 0.5, 0) for i in range(2000)])
    c.equal("2000-row limit inclusive", evaluate(max_rows)["alarms"], 2000)
    for bad in (True, -1, 1.0, 1000001, None, "1"):
        c.reject("cost type/range " + repr(bad), lambda bad=bad: evaluate(boundary, cost=dict(COST, false_positive=bad)), "COST")
        c.reject("FN cost type/range " + repr(bad), lambda bad=bad: evaluate(boundary, cost=dict(COST, false_negative=bad)), "COST")
    c.equal("maximum cost inclusive", evaluate(small([row("m", 0.8, 0)]), cost=dict(COST, false_positive=1000000))["cost_total"], 1000000)
    for policy in ({"threshold": 0.5}, dict(POLICY, extra=True), []):
        c.reject("policy exact keys", lambda policy=policy: evaluate(boundary, policy), "FIELDS")
    for cost in ({"false_positive": 1}, dict(COST, extra=True), []):
        c.reject("cost exact keys", lambda cost=cost: evaluate(boundary, cost=cost), "FIELDS")
    c.reject("unknown selection", lambda: evaluate(boundary, dict(POLICY, selection="unknown")), "EVALUATION_LABEL_TUNING_FORBIDDEN")
    c.reject("unknown mutation", lambda: evaluate_cohort(boundary, POLICY, COST, mutation="unknown"), "MUTATION")

    minimal = {"schema": "AI-PREVALENCE-1", "policy": dict(POLICY), "cost": dict(COST),
               "cohorts": [small([row("x", 0.8, 1)], "one")]}
    for key in ("schema", "policy", "cost", "cohorts"):
        bad = copy.deepcopy(minimal)
        del bad[key]
        c.reject("missing document " + key, lambda bad=bad: validate_document(bad), "FIELDS")
    c.reject("extra document field", lambda: validate_document(dict(minimal, extra=1)), "FIELDS")
    c.reject("wrong schema", lambda: validate_document(dict(minimal, schema="OTHER")), "SCHEMA")
    c.reject("empty cohorts", lambda: validate_document(dict(minimal, cohorts=[])), "COHORTS")
    c.reject("cohort list type", lambda: validate_document(dict(minimal, cohorts={})), "COHORTS")
    c.reject("cohort count bound", lambda: validate_document(dict(minimal, cohorts=[small([], str(i)) for i in range(5)])), "COHORTS")
    c.reject("duplicate cohort", lambda: validate_document(dict(minimal, cohorts=[small([], "one"), small([], "one")])), "DUPLICATE_COHORT")
    c.reject("overlapping sample IDs", lambda: validate_document(dict(minimal, cohorts=[minimal["cohorts"][0], small([row("x", 0.2, 0)], "two")])), "OVERLAPPING_COHORTS")
    large = [small([row(f"{j}_{i}", 0.5, 0) for i in range(2000)], str(j)) for j in range(2)]
    c.equal("4000-row document bound inclusive", validate_document(dict(minimal, cohorts=large)), None)
    c.reject("4001-row document bound", lambda: validate_document(dict(minimal, cohorts=large + [small([row("extra", 0.5, 0)], "third")])), "TOTAL_ROWS")

    invalid_json = {
        "duplicate_root": ('{"schema":"AI-PREVALENCE-1","schema":"OTHER"}', "DUPLICATE_JSON_KEY"),
        "duplicate_nested": ('{"a":{"id":"one","id":"two"}}', "DUPLICATE_JSON_KEY"),
        "NaN": ('{"x":NaN}', "NONFINITE_JSON"),
        "Infinity": ('{"x":Infinity}', "NONFINITE_JSON"),
        "negative_Infinity": ('{"x":-Infinity}', "NONFINITE_JSON"),
        "invalid_utf8": (b"\xff", "JSON"),
        "truncated": ('{"schema":', "JSON"),
        "too_large": (b" " * 300001, "FILE_TOO_LARGE"),
        "exponent_overflow": (json.dumps(minimal).replace('0.8', '1e999'), "UNIT_NUMBER"),
    }
    for name, (raw, reason) in invalid_json.items():
        path = out / ("invalid_" + name + ".json")
        path.write_bytes(raw if isinstance(raw, bytes) else raw.encode())
        c.reject("JSON parser " + name, lambda path=path: load_fixture(path), reason)
    c.observations["contract_rejections"] = c.rejections
    return c


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("fixtures.json"))
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    try:
        if args.out.exists() or args.out.is_symlink():
            raise ContractError("OUTPUT_EXISTS")
        fixture = load_fixture(args.fixture)
        args.out.mkdir(parents=True, exist_ok=False)
    except (ContractError, OSError, ValueError) as error:
        print("INPUT_ERROR: " + str(error), file=sys.stderr)
        return 2
    paths = [Path(__file__).with_name("model.py"), Path(__file__), args.fixture]
    sources_before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    try:
        checks = suite(fixture, args.mutation, args.out)
    except Exception as error:
        checks = Checks()
        checks.issues.append({"case": "suite runtime", "exception": repr(error)})
    sources_after = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    checks.equal("source and fixture bytes unchanged", sources_after, sources_before)
    result = {"status": "PASS" if not checks.issues else "ERROR", "mutation": args.mutation,
              "checks": checks.count, "rejections": checks.rejections, "issues": checks.issues,
              "source_sha256": sources_before, "source_sha256_after": sources_after,
              "observations": checks.observations,
              "environment": {"python": sys.version, "executable": sys.executable,
                              "platform": platform.platform(), "optimize": sys.flags.optimize},
              "argv": sys.argv, "time_utc": datetime.now(timezone.utc).isoformat()}
    (args.out / "result.json").write_bytes((json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())
    print(json.dumps({key: result[key] for key in ("status", "checks", "rejections", "issues")}, ensure_ascii=False))
    return 0 if not checks.issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
