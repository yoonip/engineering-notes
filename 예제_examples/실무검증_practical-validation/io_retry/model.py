"""Decoded one-LBA event model; no block API, DMA, timer, or disk access."""
from dataclasses import dataclass, field
import re


MUTATIONS = ("callback-filter-only", "release-buffer-on-timeout",
             "unbounded-retry", "accept-stale-callback")


class ContractError(ValueError):
    """An event or input violates this educational model's contract."""


def name(value):
    if not isinstance(value, str) or re.fullmatch(r"[A-Za-z0-9_-]{1,24}", value) is None:
        raise ContractError("invalid identifier")
    return value


def block(value):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{8}", value) is None:
        raise ContractError("one block must be four lowercase-hex bytes")
    return value


@dataclass
class Request:
    kind: str
    payload: str | None
    current: str
    attempts: list = field(default_factory=list)
    outcome: str = "PENDING"


@dataclass
class Attempt:
    request: str
    generation: int
    slot: str
    state: str = "SUBMITTED"
    applied: bool = False
    read_value: str | None = None


class IoModel:
    """Each method is one ordered event, not a concurrent driver implementation."""

    def __init__(self, *, max_attempts=2, guard_writes=True, mutation=None):
        if type(max_attempts) is not int or not 1 <= max_attempts <= 4:
            raise ContractError("attempt limit must be 1..4")
        if type(guard_writes) is not bool:
            raise ContractError("guard_writes must be bool")
        if mutation is not None and mutation not in MUTATIONS:
            raise ContractError("unknown mutation")
        self.max_attempts = max_attempts
        self.guard_writes = guard_writes and mutation != "callback-filter-only"
        self.mutation = mutation
        self.media = "00000000"
        self.requests = {}
        self.attempts = {}
        self.owners = {}
        self.notifications = []
        self.trace = []

    def _attempt(self, aid):
        name(aid)
        if aid not in self.attempts:
            raise ContractError("unknown attempt")
        return self.attempts[aid]

    def _record(self, event, aid, result):
        self.trace.append({"event": event, "attempt": aid, "result": result,
                           "media": self.media})
        return result

    def _allocate(self, rid, aid, slot):
        name(aid)
        name(slot)
        if aid in self.attempts:
            raise ContractError("attempt identifiers are never reused in this run")
        if slot in self.owners:
            raise ContractError("buffer slot is still owned")
        req = self.requests[rid]
        generation = len(req.attempts) + 1
        self.attempts[aid] = Attempt(rid, generation, slot)
        self.owners[slot] = aid
        req.current = aid
        req.attempts.append(aid)
        req.outcome = "PENDING"
        return self._record("SUBMIT", aid, "SUBMITTED")

    def start(self, rid, aid, kind, payload, slot):
        name(rid)
        name(aid)
        name(slot)
        if kind not in ("WRITE", "READ"):
            raise ContractError("unsupported operation")
        if kind == "WRITE":
            block(payload)
        elif payload is not None:
            raise ContractError("READ has no payload")
        if rid in self.requests or len(self.requests) >= 16:
            raise ContractError("request identifier reused or request limit reached")
        if aid in self.attempts or slot in self.owners:
            raise ContractError("attempt or slot already exists")
        if self.guard_writes and kind == "WRITE" and any(
                r.kind == "WRITE" and r.outcome not in ("SUCCESS", "FAILED")
                for r in self.requests.values()):
            raise ContractError("unresolved overlapping write")
        self.requests[rid] = Request(kind, payload, aid)
        return self._allocate(rid, aid, slot)

    def timeout(self, aid):
        attempt = self._attempt(aid)
        if attempt.state in ("COMPLETED", "QUIESCED"):
            return self._record("TIMEOUT", aid, "ALREADY_RESOLVED")
        attempt.state = "TIMED_OUT"
        req = self.requests[attempt.request]
        if req.current == aid:
            req.outcome = "UNKNOWN"
        if self.mutation == "release-buffer-on-timeout":
            self.owners.pop(attempt.slot, None)
        return self._record("TIMEOUT", aid, "UNKNOWN")

    def quiesce(self, aid, stopped):
        """stopped=True is external evidence of no future device effect, not a timer."""
        attempt = self._attempt(aid)
        if type(stopped) is not bool or attempt.state != "TIMED_OUT":
            raise ContractError("quiesce needs a timed-out attempt and a bool")
        if not stopped:
            return self._record("QUIESCE", aid, "NOT_QUIESCED")
        attempt.state = "QUIESCED"
        self.owners.pop(attempt.slot, None)
        return self._record("QUIESCE", aid, "QUIESCED")

    def retry(self, rid, aid, slot):
        name(rid)
        name(aid)
        name(slot)
        if rid not in self.requests:
            raise ContractError("unknown request")
        req = self.requests[rid]
        if req.outcome != "UNKNOWN":
            raise ContractError("retry requires an unknown outcome")
        if self.mutation != "unbounded-retry" and len(req.attempts) >= self.max_attempts:
            raise ContractError("attempt limit reached")
        if self.guard_writes and req.kind == "WRITE" and any(
                self.attempts[old].state not in ("QUIESCED", "COMPLETED")
                for old in req.attempts):
            raise ContractError("old write can still take effect")
        return self._allocate(rid, aid, slot)

    def apply(self, aid):
        """The device effect and the host callback are deliberately separate events."""
        attempt = self._attempt(aid)
        if attempt.state not in ("SUBMITTED", "TIMED_OUT") or attempt.applied:
            raise ContractError("attempt cannot apply")
        req = self.requests[attempt.request]
        if req.kind == "WRITE":
            self.media = req.payload
        else:
            attempt.read_value = self.media
        attempt.applied = True
        return self._record("APPLY", aid, "APPLIED")

    def complete(self, aid, rid, generation, status):
        attempt = self._attempt(aid)
        name(rid)
        if rid != attempt.request or type(generation) is not int or generation != attempt.generation:
            raise ContractError("callback identity mismatch")
        if status not in ("SUCCESS", "ERROR"):
            raise ContractError("unsupported completion status")
        if attempt.state == "QUIESCED":
            return self._record("CALLBACK", aid, "IGNORED_QUIESCED")
        if attempt.state == "COMPLETED":
            return self._record("CALLBACK", aid, "IGNORED_DUPLICATE")
        if status == "SUCCESS" and not attempt.applied:
            raise ContractError("success before the device effect")
        attempt.state = "COMPLETED"
        self.owners.pop(attempt.slot, None)
        req = self.requests[rid]
        if req.current != aid:
            if self.mutation == "accept-stale-callback":
                self.notifications.append({"request": rid, "status": status,
                                           "value": attempt.read_value})
            return self._record("CALLBACK", aid, "IGNORED_STALE")
        if status == "ERROR":
            req.outcome = "UNKNOWN"
            return self._record("CALLBACK", aid, "FAILED_UNCERTAIN")
        req.outcome = "SUCCESS"
        self.notifications.append({"request": rid, "status": "SUCCESS",
                                   "value": attempt.read_value})
        return self._record("CALLBACK", aid, "SUCCESS")

    def give_up(self, rid):
        name(rid)
        if rid not in self.requests:
            raise ContractError("unknown request")
        req = self.requests[rid]
        if req.outcome != "UNKNOWN" or any(
                self.attempts[aid].state not in ("QUIESCED", "COMPLETED")
                for aid in req.attempts):
            raise ContractError("cannot abandon unresolved device activity")
        req.outcome = "FAILED"
        self.notifications.append({"request": rid, "status": "FAILED", "value": None})
        return self._record("GIVE_UP", req.current, "FAILED")

    def snapshot(self):
        return {"media": self.media, "owners": dict(self.owners),
                "outcomes": {rid: req.outcome for rid, req in self.requests.items()},
                "notifications": list(self.notifications), "trace": list(self.trace)}
