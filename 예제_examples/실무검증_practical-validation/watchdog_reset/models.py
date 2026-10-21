"""작업 진행·feed 구간·리셋 기록의 교육용 호스트 모형입니다."""
MODULUS = 256  # 8비트 tick이 255 다음 0으로 돌아오는 공간입니다.
HALF = 128  # 이 모형은 비교하는 실제 시간 차이가 128 미만이라고 전제합니다.
CAUSES = {"watchdog": 1, "software": 2, "power": 4}  # 실제 RCC 비트 위치가 아닌 모형 값입니다.


def number(value: int, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:  # bool·범위 밖 값을 거부합니다.
        raise ValueError(f"integer in [{low}, {high}] required")
    return value


def elapsed(now: int, before: int) -> int:
    number(now, 0, 255)
    number(before, 0, 255)
    difference = (now - before) % MODULUS  # %는 나머지이며 순환한 tick의 차이를 구합니다.
    if difference >= HALF:
        raise ValueError("comparison outside the declared half-range")
    return difference


def window_action(now: int, last_feed: int, requested: bool,
                  earliest: int = 4, timeout: int = 12, raw_deadline: bool = False) -> str:
    number(earliest, 1, 126)
    number(timeout, earliest + 1, 127)
    age = elapsed(now, last_feed)
    expired = now >= (last_feed + timeout) % MODULUS if raw_deadline else age >= timeout
    if expired:
        return "reset_late"  # [earliest, timeout) 밖의 늦은 feed는 받아들이지 않습니다.
    if not requested:
        return "wait"
    return "reset_early" if age < earliest else "feed"


class HealthGate:
    def __init__(self, names: list[str], start: int, fresh_limit: int):
        if not names or len(set(names)) != len(names) or any(type(name) is not str or not name for name in names):
            raise ValueError("nonempty unique task names required")
        number(start, 0, 255)
        number(fresh_limit, 1, 127)
        self.fresh_limit = fresh_limit
        self.tasks = {name: {"sequence": 0, "accepted": 0, "tick": start} for name in names}

    def progress(self, name: str, tick: int) -> None:
        number(tick, 0, 255)
        if name not in self.tasks:  # not in은 등록하지 않은 task인지 확인합니다.
            raise ValueError("unknown task")
        task = self.tasks[name]
        task["sequence"] += 1  # +=는 누적 대입이며 완료 checkpoint를 한 번 더 셉니다.
        task["tick"] = tick

    def inspect(self, now: int) -> dict:
        observations = {
            name: {"sequence": task["sequence"], "accepted": task["accepted"],
                   "age": elapsed(now, task["tick"])} for name, task in self.tasks.items()
        }
        healthy = all(item["sequence"] > item["accepted"] and item["age"] <= self.fresh_limit
                      for item in observations.values())  # all은 모든 조건이 참인지 확인합니다.
        return {"healthy": healthy, "tasks": observations}

    def accept_epoch(self) -> None:
        for task in self.tasks.values():
            task["accepted"] = task["sequence"]  # 성공한 feed가 소비한 진행 상태를 저장합니다.


def monitor(fixture: dict, periodic_feed: bool = False, raw_deadline: bool = False) -> dict:
    start = fixture["start_absolute"]
    number(start, 0, 1000000)
    gate = HealthGate(fixture["tasks"], start % MODULUS, fixture["fresh_limit"])
    last_feed, previous = start % MODULUS, start
    trace, feeds = [], []  # []는 순서가 있는 list입니다.
    reset_at = None
    for event in fixture["events"]:
        absolute = number(event["at"], previous, start + 127)
        previous = absolute  # 시간 순서와 시작 뒤 127 이하라는 입력 계약을 검사합니다.
        now = absolute % MODULUS
        if "progress" in event:
            gate.progress(event["progress"], now)
            continue
        if event != {"at": absolute, "poll": True}:
            raise ValueError("event must be a progress checkpoint or poll")
        health = gate.inspect(now)
        age = elapsed(now, last_feed)
        requested = periodic_feed or (health["healthy"] and age >= fixture["earliest"])
        action = window_action(now, last_feed, requested, fixture["earliest"],
                               fixture["timeout"], raw_deadline)
        trace.append({"absolute": absolute, "tick": now, "feed_age": age,
                      "action": action, "health": health})
        if action.startswith("reset_"):
            reset_at = absolute
            break  # break는 리셋 뒤의 사건을 현재 부팅에서 더 실행하지 않습니다.
        if action == "feed":
            feeds.append(absolute)
            last_feed = now
            gate.accept_epoch()
    return {"feeds": feeds, "reset_at": reset_at, "trace": trace}


class ResetLatch:
    def __init__(self):
        self.flags = 0

    def latch(self, cause: str) -> None:
        if cause not in CAUSES:
            raise ValueError("unknown reset cause")
        self.flags |= CAUSES[cause]  # |=는 OR 누적이며 여러 원인 표시를 함께 남깁니다.

    def capture(self, clear_first: bool = False) -> dict:
        if clear_first:
            self.flags = 0  # 오류 대조: 원시 값을 보존하기 전에 상태를 지웁니다.
        saved = self.flags
        self.flags = 0
        return {"raw": saved, "causes": [name for name, bit in CAUSES.items() if saved & bit]}


class BootLedger:
    def __init__(self, limit: int = 3):
        self.limit = number(limit, 1, 100)
        self.failures = 0  # 부팅 간 보존된다고 가정한 모형 값이며 실제 retention 구현이 아닙니다.

    def boot(self, captured: dict, always_restart: bool = False) -> dict:
        if captured["raw"] & CAUSES["watchdog"]:
            self.failures += 1
        else:
            self.failures = 0  # 비-watchdog 부팅은 연속 watchdog 실패 구간을 끝냅니다.
        recovery = self.failures >= self.limit and not always_restart
        return {"failures": self.failures, "mode": "recovery" if recovery else "normal"}

    def stable_checkpoint(self) -> None:
        self.failures = 0  # 검증된 안정 운전 checkpoint 뒤에만 연속 실패를 초기화합니다.


def boot_sequence(events: list[str], clear_first: bool = False, always_restart: bool = False) -> list[dict]:
    latch, ledger = ResetLatch(), BootLedger()
    result = []
    for event in events:
        if event == "stable":
            ledger.stable_checkpoint()
            result.append({"failures": ledger.failures, "mode": "stable"})
            continue
        latch.latch(event)
        captured = latch.capture(clear_first)
        result.append({"captured": captured, **ledger.boot(captured, always_restart)})
    return result
