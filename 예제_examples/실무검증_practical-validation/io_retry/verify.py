"""Literal checks for one decoded I/O state machine, with new-output protection."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

from model import ContractError, IoModel, MUTATIONS


class Checks:
    def __init__(self):
        self.count = 0
        self.rejections = 0
        self.observations = {}
        self.issues = []

    def equal(self, label, actual, expected):
        self.count += 1
        if actual != expected:
            raise AssertionError(f"{label}: {actual!r} != {expected!r}")

    def reject(self, label, action):
        self.count += 1
        try:
            action()
        except ContractError:
            self.rejections += 1
            return
        raise AssertionError(label + ": invalid event was accepted")

    def run(self, label, action):
        try:
            self.observations[label] = action()
        except Exception as error:
            self.issues.append({"case": label, "type": type(error).__name__, "message": str(error)})


def suite(f, mutation):
    c = Checks()

    def make(**kwargs):
        return IoModel(mutation=mutation, **kwargs)

    def unsafe_order():
        d = make(guard_writes=False)
        d.start("R1", "A", "WRITE", f["r1"], "a")
        c.equal("timeout is unknown", d.timeout("A"), "UNKNOWN")
        d.retry("R1", "B", "b")
        d.apply("B")
        d.complete("B", "R1", 2, "SUCCESS")
        d.start("R2", "C", "WRITE", f["r2"], "c")
        d.apply("C")
        d.complete("C", "R2", 1, "SUCCESS")
        c.equal("before the late apply", d.media, f["safe_final"])
        d.apply("A")
        c.equal("stale callback is ignored", d.complete("A", "R1", 1, "SUCCESS"), "IGNORED_STALE")
        c.equal("filter does not fix media", d.media, f["unsafe_final"])
        c.equal("application completion IDs", [v["request"] for v in d.notifications], f["completion_ids"])
        return d.snapshot()

    def fixed_order():
        d = make()
        d.start("R1", "A", "WRITE", f["r1"], "a")
        d.timeout("A")
        c.equal("timeout retains slot", d.owners, {"a": "A"})
        c.reject("retry blocked", lambda: d.retry("R1", "B", "b"))
        c.reject("new overlapping write blocked", lambda: d.start("R2", "C", "WRITE", f["r2"], "c"))
        c.equal("failed recovery is not quiescence", d.quiesce("A", False), "NOT_QUIESCED")
        c.reject("give up cannot cancel", lambda: d.give_up("R1"))
        c.equal("explicit stop evidence", d.quiesce("A", True), "QUIESCED")
        c.reject("new request cannot overtake logical R1", lambda: d.start("R2", "C", "WRITE", f["r2"], "c"))
        c.reject("old stopped attempt cannot apply", lambda: d.apply("A"))
        d.retry("R1", "B", "a")
        d.apply("B")
        d.complete("B", "R1", 2, "SUCCESS")
        c.equal("old callback cannot release reused slot", d.complete("A", "R1", 1, "SUCCESS"), "IGNORED_QUIESCED")
        d.start("R2", "C", "WRITE", f["r2"], "a")
        c.equal("slot belongs to C", d.owners, {"a": "C"})
        d.apply("C")
        d.complete("C", "R2", 1, "SUCCESS")
        c.equal("safe final bytes", d.media, f["safe_final"])
        c.equal("logical outcomes", d.snapshot()["outcomes"], f["safe_outcomes"])
        c.equal("one completion per request", [v["request"] for v in d.notifications], f["completion_ids"])
        c.equal("all buffers returned", d.owners, {})
        return d.snapshot()

    def read_retry():
        d = make()
        d.start("Q", "QA", "READ", None, "a")
        d.timeout("QA")
        c.reject("read retry cannot reuse old buffer", lambda: d.retry("Q", "QB", "a"))
        d.retry("Q", "QB", "b")
        c.equal("both read buffers held", d.owners, {"a": "QA", "b": "QB"})
        d.apply("QB")
        d.complete("QB", "Q", 2, "SUCCESS")
        d.apply("QA")
        d.complete("QA", "Q", 1, "SUCCESS")
        c.equal("old read cannot notify twice", d.notifications, f["read_notifications"])
        c.equal("read did not change media", d.media, f["initial"])
        c.equal("read buffers returned", d.owners, {})
        return d.snapshot()

    def completion_edges():
        observations = {}
        for ordering in ("before-timeout", "after-timeout"):
            d = make()
            d.start("R1", "A", "WRITE", f["r1"], "a")
            if ordering == "after-timeout":
                d.timeout("A")
            d.apply("A")
            c.equal(ordering + " success", d.complete("A", "R1", 1, "SUCCESS"), "SUCCESS")
            c.equal(ordering + " timeout after completion", d.timeout("A"), "ALREADY_RESOLVED")
            c.equal(ordering + " duplicate", d.complete("A", "R1", 1, "SUCCESS"), "IGNORED_DUPLICATE")
            c.equal(ordering + " once", len(d.notifications), 1)
            c.equal(ordering + " bytes", d.media, f["r1"])
            observations[ordering] = d.snapshot()
        return observations

    def failed_retry_limit():
        d = make()
        d.start("R1", "A", "WRITE", f["r1"], "a")
        c.equal("error may have unknown effects", d.complete("A", "R1", 1, "ERROR"), "FAILED_UNCERTAIN")
        d.retry("R1", "B", "a")
        d.timeout("B")
        c.reject("cannot abandon in-flight B", lambda: d.give_up("R1"))
        d.quiesce("B", True)
        c.reject("bounded attempt budget", lambda: d.retry("R1", "C", "a"))
        d.give_up("R1")
        c.reject("duplicate give up", lambda: d.give_up("R1"))
        d.start("R2", "D", "WRITE", f["r2"], "a")
        d.apply("D")
        d.complete("D", "R2", 1, "SUCCESS")
        c.equal("failed request once then next request", d.notifications, f["failed_then_next"])
        c.equal("recovery final", d.media, f["safe_final"])
        return d.snapshot()

    def apply_before_unknown():
        d = make()
        d.start("R1", "A", "WRITE", f["r1"], "a")
        d.apply("A")
        d.timeout("A")
        c.equal("timeout did not roll back", d.media, f["r1"])
        d.quiesce("A", True)
        c.equal("quiesce did not roll back", d.media, f["r1"])
        d.retry("R1", "B", "a")
        d.apply("B")
        d.complete("B", "R1", 2, "SUCCESS")
        c.equal("same payload final", d.media, f["r1"])
        return d.snapshot()

    def input_boundaries():
        for value in (0, 5, True, "2", None):
            c.reject("attempt limit type/range", lambda value=value: make(max_attempts=value))
        c.reject("guard type", lambda: make(guard_writes=1))
        c.reject("mutation name", lambda: IoModel(mutation="unknown"))
        d = make()
        for payload in ("", "414141", "4141414141", "GGGGGGGG", "ABCDEF01", [], 123, None):
            c.reject("payload type/length", lambda payload=payload: d.start("R", "A", "WRITE", payload, "a"))
        for identifier in ("", "space here", "x" * 25, True, []):
            c.reject("identifier type/range", lambda identifier=identifier: d.start(identifier, "A", "WRITE", f["r1"], "a"))
        c.reject("read payload", lambda: d.start("R", "A", "READ", f["r1"], "a"))
        c.reject("unknown op", lambda: d.start("R", "A", "FLUSH", None, "a"))
        d.start("R", "A", "WRITE", f["r1"], "a")
        before = d.snapshot()
        c.reject("wrong request", lambda: d.complete("A", "WRONG", 1, "SUCCESS"))
        c.reject("wrong generation", lambda: d.complete("A", "R", 2, "SUCCESS"))
        c.reject("bool generation", lambda: d.complete("A", "R", True, "SUCCESS"))
        c.reject("bad status", lambda: d.complete("A", "R", 1, "OK"))
        c.reject("premature success", lambda: d.complete("A", "R", 1, "SUCCESS"))
        c.reject("quiesce before timeout", lambda: d.quiesce("A", True))
        c.equal("invalid callbacks preserve state", d.snapshot(), before)
        d.apply("A")
        c.reject("duplicate apply", lambda: d.apply("A"))
        d.complete("A", "R", 1, "SUCCESS")
        c.reject("attempt ID reused after complete", lambda: d.start("R2", "A", "READ", None, "a"))
        c.reject("request ID reused", lambda: d.start("R", "B", "READ", None, "a"))
        c.reject("retry after success", lambda: d.retry("R", "B", "a"))
        c.reject("unknown apply", lambda: d.apply("MISSING"))
        c.reject("unknown retry", lambda: d.retry("MISSING", "B", "a"))
        c.reject("unknown give up", lambda: d.give_up("MISSING"))
        d.start("Q", "B", "READ", None, "a")
        d.timeout("B")
        c.reject("quiesce evidence type", lambda: d.quiesce("B", 1))
        c.equal("one-attempt boundary", make(max_attempts=1).max_attempts, 1)
        c.equal("four-attempt boundary", make(max_attempts=4).max_attempts, 4)
        return {"rejection_checks_so_far": c.rejections, "media": d.media}

    for label, action in (("callback_only_counterexample", unsafe_order),
                          ("barrier_and_quiesce", fixed_order), ("read_retry", read_retry),
                          ("completion_edges", completion_edges),
                          ("failed_retry_limit", failed_retry_limit),
                          ("apply_before_unknown", apply_before_unknown),
                          ("input_boundaries", input_boundaries)):
        c.run(label, action)
    return c


def load_fixture(path):
    if path.stat().st_size > 16384:
        raise ValueError("fixture too large")
    f = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(f, dict) or f.get("schema") != "IO-RETRY-1":
        raise ValueError("wrong fixture schema")
    if type(f.get("lba_count")) is not int or f["lba_count"] != 1 or type(f.get("block_bytes")) is not int or f["block_bytes"] != 4:
        raise ValueError("only one four-byte LBA is supported")
    for key in ("initial", "r1", "r2", "unsafe_final", "safe_final", "completion_ids",
                "safe_outcomes", "read_notifications", "failed_then_next"):
        if key not in f:
            raise ValueError("missing fixture key: " + key)
    return f


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("fixtures.json"))
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    try:
        if args.out.exists():
            raise ValueError("output already exists")
        f = load_fixture(args.fixture)
        args.out.mkdir(parents=True, exist_ok=False)
    except (OSError, ValueError) as error:
        print("INPUT_ERROR: " + str(error), file=sys.stderr)
        return 2
    c = suite(f, args.mutation)
    here = Path(__file__).parent
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in (here / "model.py", here / "verify.py", args.fixture)}
    result = {"status": "PASS" if not c.issues else "ERROR", "mutation": args.mutation,
              "checks": c.count, "rejections": c.rejections, "issues": c.issues,
              "source_sha256": sources, "observations": c.observations,
              "environment": {"python": sys.version, "executable": sys.executable,
                              "platform": platform.platform(), "optimize": sys.flags.optimize},
              "argv": sys.argv, "time_utc": datetime.now(timezone.utc).isoformat()}
    (args.out / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("status", "checks", "rejections", "issues")}, ensure_ascii=False))
    return 0 if not c.issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
