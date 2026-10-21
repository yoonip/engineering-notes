"""Fixed-threshold evaluation of bounded synthetic cohorts, not a learned model."""
import json
import math
from pathlib import Path
import re


MUTATIONS = ("precision-uses-all-samples", "copy-validation-precision",
             "missing-label-as-normal", "retune-on-test-labels")
SCHEMA = "AI-PREVALENCE-1"
MAX_BYTES = 300000


class ContractError(ValueError):
    """A rejected input has a stable reason code and no evaluation result."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def fields(value, names):
    if type(value) is not dict or set(value) != set(names):
        raise ContractError("FIELDS")


def identifier(value):
    if type(value) is not str or re.fullmatch(r"[A-Za-z0-9_-]{1,32}", value) is None:
        raise ContractError("IDENTIFIER")


def unit_number(value):
    if type(value) not in (int, float):
        raise ContractError("UNIT_NUMBER")
    # Range checks reject huge integers before conversion by math.isfinite().
    if not 0 <= value <= 1 or not math.isfinite(value):
        raise ContractError("UNIT_NUMBER")


def mutation_name(value):
    if value is not None and value not in MUTATIONS:
        raise ContractError("MUTATION")


def validate_policy(policy, mutation=None):
    fields(policy, ("threshold", "selection"))
    unit_number(policy["threshold"])
    if policy["selection"] != "fixed-before-evaluation":
        if not (mutation == "retune-on-test-labels" and policy["selection"] == "test-labels"):
            raise ContractError("EVALUATION_LABEL_TUNING_FORBIDDEN")


def validate_cost(cost):
    fields(cost, ("false_positive", "false_negative"))
    for value in cost.values():
        if type(value) is not int or not 0 <= value <= 1000000:
            raise ContractError("COST")


def validate_cohort(cohort):
    fields(cohort, ("id", "rows"))
    identifier(cohort["id"])
    rows = cohort["rows"]
    if type(rows) is not list or len(rows) > 2000:
        raise ContractError("ROWS")
    seen = set()
    for row in rows:
        fields(row, ("id", "score", "label"))
        identifier(row["id"])
        if row["id"] in seen:
            raise ContractError("DUPLICATE_ID")
        seen.add(row["id"])
        unit_number(row["score"])
        label = row["label"]
        if label is not None and (type(label) is not int or label not in (0, 1)):
            raise ContractError("CLASS")


def validate_document(document, mutation=None):
    mutation_name(mutation)
    fields(document, ("schema", "policy", "cost", "cohorts"))
    if document["schema"] != SCHEMA:
        raise ContractError("SCHEMA")
    validate_policy(document["policy"], mutation)
    validate_cost(document["cost"])
    cohorts = document["cohorts"]
    if type(cohorts) is not list or not 1 <= len(cohorts) <= 4:
        raise ContractError("COHORTS")
    cohort_ids, sample_ids = set(), set()
    total = 0
    for cohort in cohorts:
        validate_cohort(cohort)
        if cohort["id"] in cohort_ids:
            raise ContractError("DUPLICATE_COHORT")
        cohort_ids.add(cohort["id"])
        for row in cohort["rows"]:
            if row["id"] in sample_ids:
                raise ContractError("OVERLAPPING_COHORTS")
            sample_ids.add(row["id"])
        total += len(cohort["rows"])
    if total > 4000:
        raise ContractError("TOTAL_ROWS")


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ContractError("DUPLICATE_JSON_KEY")
        value[key] = item
    return value


def _nonfinite(token):
    raise ContractError("NONFINITE_JSON")


def load_fixture(path):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise ContractError("FILE_TOO_LARGE")
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ContractError("FILE_TOO_LARGE")
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                              parse_constant=_nonfinite)
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        if isinstance(error, ContractError):
            raise
        raise ContractError("JSON") from error
    validate_document(document)
    return document


def ratio(numerator, denominator):
    # Keep the unreduced denominator to show which population was counted.
    return {"numerator": numerator, "denominator": denominator,
            "value": None if denominator == 0 else numerator / denominator}


def _leaky_threshold(rows, cost):
    """An intentionally wrong alternative: optimize on evaluation answers."""
    candidates = sorted({0, 1, *(row["score"] for row in rows)})

    def objective(threshold):
        fp = sum(row["label"] == 0 and row["score"] >= threshold for row in rows)
        fn = sum(row["label"] == 1 and row["score"] < threshold for row in rows)
        return (fp * cost["false_positive"] + fn * cost["false_negative"], threshold)

    return min(candidates, key=objective)


def evaluate_cohort(cohort, policy, cost, *, mutation=None):
    """Evaluate every row at one predeclared threshold; never select it here."""
    mutation_name(mutation)
    validate_policy(policy, mutation)
    validate_cost(cost)
    validate_cohort(cohort)
    rows = cohort["rows"]
    threshold = policy["threshold"]
    known = sum(row["label"] is not None for row in rows)
    missing = len(rows) - known
    if mutation == "retune-on-test-labels" and policy["selection"] == "test-labels":
        if missing:
            raise ContractError("TUNING_REQUIRES_LABELS")
        threshold = _leaky_threshold(rows, cost)
    alarms = sum(row["score"] >= threshold for row in rows)
    result = {"cohort_id": cohort["id"], "status": "METRICS_NOT_ESTABLISHED",
              "threshold_used": threshold, "threshold_origin": policy["selection"],
              "sample_count": len(rows), "known_labels": known, "missing_labels": missing,
              "alarms": alarms, "alarm_rate": ratio(alarms, len(rows)),
              "confusion": None, "metrics": None, "cost_total": None,
              "cost_per_sample": None}
    if not rows or (missing and mutation != "missing-label-as-normal"):
        return result
    counts = {"tp": 0, "fn": 0, "fp": 0, "tn": 0}
    for row in rows:
        positive = row["score"] >= threshold
        label = 0 if row["label"] is None else row["label"]
        key = ("tp" if positive else "fn") if label == 1 else ("fp" if positive else "tn")
        counts[key] += 1
    tp, fn, fp, tn = (counts[key] for key in ("tp", "fn", "fp", "tn"))
    precision_denominator = len(rows) if mutation == "precision-uses-all-samples" else tp + fp
    total_cost = fp * cost["false_positive"] + fn * cost["false_negative"]
    result.update(status="METRICS_ESTABLISHED", confusion=counts,
                  metrics={"precision": ratio(tp, precision_denominator),
                           "recall": ratio(tp, tp + fn), "fpr": ratio(fp, fp + tn),
                           "accuracy": ratio(tp + tn, len(rows)),
                           "prevalence": ratio(tp + fn, len(rows))},
                  cost_total=total_cost, cost_per_sample=ratio(total_cost, len(rows)))
    return result


def evaluate_bundle(document, *, mutation=None):
    validate_document(document, mutation)
    results = [evaluate_cohort(cohort, document["policy"], document["cost"], mutation=mutation)
               for cohort in document["cohorts"]]
    if mutation == "copy-validation-precision" and results and results[0]["metrics"]:
        # Wrong cache reuse: the first cohort's precision is not a deployment property.
        cached = dict(results[0]["metrics"]["precision"])
        for result in results[1:]:
            if result["metrics"]:
                result["metrics"]["precision"] = dict(cached)
    return results
