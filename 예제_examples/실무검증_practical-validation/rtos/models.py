"""RTOS 계약을 설명하는 결정적 호스트 모델입니다. 커널이나 ISR을 실행하지 않습니다."""
from dataclasses import dataclass, field  # dataclass는 상태 보관용 클래스를 간단히 만듭니다.


def priority_schedule(low_work: int, medium_work: int, high_work: int,
                      inherit: bool, deadline: int = 5) -> dict:
    """L은 시각 0에 잠금을 보유하며 H와 M은 시각 1에 준비됩니다."""
    if low_work < 1 or medium_work < 0 or high_work < 1:
        raise ValueError("work must satisfy L>=1, M>=0, H>=1")
    remaining = {"L": low_work, "M": medium_work, "H": high_work}  # dict는 이름과 값을 연결합니다.
    base = {"L": 1, "M": 2, "H": 3}  # 이 모델은 큰 숫자가 높은 우선순위입니다.
    owner = "L"  # 잠금은 처음에 L이 소유합니다.
    trace, events = [], []  # list 두 개에 실행 순서와 상태 변화를 보관합니다.
    high_finished = None
    for tick in range(low_work + medium_work + high_work):
        released = {"L": True, "M": tick >= 1, "H": tick >= 1}
        high_waits = released["H"] and remaining["H"] > 0 and owner == "L"
        effective = base.copy()  # copy는 본래 우선순위 사전을 보존합니다.
        if inherit and high_waits:
            effective["L"] = base["H"]  # 대기 중인 H의 우선순위를 소유자에게 빌립니다.
        ready = [name for name in remaining if remaining[name] > 0 and released[name]
                 and not (name == "H" and high_waits)]  # 실행 가능한 작업만 추립니다.
        if not ready:
            raise RuntimeError("model unexpectedly has no runnable task")
        chosen = max(ready, key=lambda name: effective[name])  # lambda는 비교 값을 계산합니다.
        if chosen == "H" and owner is None:
            owner = "H"  # H는 사용 전에 비어 있는 잠금을 얻습니다.
        trace.append(chosen)
        events.append({"at": tick, "run": chosen, "owner": owner,
                       "high_waits": high_waits, "effective_low": effective["L"]})
        remaining[chosen] -= 1  # 한 모델 시간 단위의 CPU 일을 마칩니다.
        if chosen == "L" and remaining["L"] == 0:
            owner = None  # L의 남은 일이 끝나는 순간 잠금을 반환합니다.
        if chosen == "H" and remaining["H"] == 0:
            high_finished = tick + 1  # 구간 [tick, tick+1)의 끝을 완료 시각으로 씁니다.
            owner = None
    return {"trace": "".join(trace), "high_finished": high_finished,
            "high_response": high_finished - 1, "deadline": deadline,
            "deadline_met": high_finished <= deadline, "events": events}


@dataclass
class WakeState:
    queue: list[int] = field(default_factory=list)  # 인스턴스마다 독립적인 큐를 만듭니다.
    consumed: list[int] = field(default_factory=list)
    pending: int = 0
    checked_empty: bool = False
    waiting: bool = False


def wakeup_schedule(order: str, retained: bool, clear_before_wait: bool = False) -> dict:
    """C=큐 검사, W=대기, P=항목 공개+알림입니다. C는 W보다 먼저 실행됩니다."""
    if sorted(order) != ["C", "P", "W"] or order.index("C") > order.index("W"):
        raise ValueError("order must contain C before W and one P")
    state, events = WakeState(), []

    def drain() -> None:
        state.consumed.extend(state.queue)  # extend는 큐의 항목 전체를 처리 기록에 더합니다.
        state.queue.clear()  # 이 모형의 큐 읽기·비우기는 하나의 추상 사건입니다.

    for step in order:
        if step == "C":
            state.checked_empty = not state.queue  # not은 큐가 비었는지를 참/거짓으로 만듭니다.
            if not state.checked_empty:
                drain()
        elif step == "W" and state.checked_empty:
            if clear_before_wait:
                state.pending = 0  # 결함 주입: 이미 도착한 알림을 기다리기 전에 지웁니다.
            if retained and state.pending > 0:
                state.pending = 0  # 대기 API가 보관한 알림을 소비하는 추상 동작입니다.
                drain()
            else:
                state.waiting = True  # 알림이 없으면 대기 등록과 함께 잠듭니다.
        elif step == "P":
            state.queue.append(42)  # payload 공개가 알림보다 먼저입니다.
            if retained:
                state.pending += 1  # 아직 자고 있지 않아도 도착 사실을 보관합니다.
            if state.waiting:
                state.waiting = False
                state.pending = 0
                drain()  # 깨운 뒤 소비자가 다시 실행되는 부분까지 합친 추상 사건입니다.
        events.append({"step": step, "queue": state.queue.copy(),
                       "consumed": state.consumed.copy(), "pending": state.pending,
                       "waiting": state.waiting})
    lost = bool(state.queue) and state.waiting
    return {"order": order, "retained": retained, "clear_before_wait": clear_before_wait,
            "consumed": state.consumed, "remaining": state.queue,
            "pending": state.pending, "waiting": state.waiting,
            "lost_wakeup": lost, "events": events}


def coalesced_batch(drain_all: bool) -> dict:
    """두 알림을 clear-on-exit로 소비한 뒤 payload를 얼마나 처리하는지 비교합니다."""
    payload, notices = [42, 43], 2
    taken = notices  # ulTaskNotifyTake(pdTRUE)의 반환값과 소거를 단순화한 모형입니다.
    notices = 0
    count = len(payload) if drain_all else 1
    consumed = payload[:count]  # 슬라이스는 지정 범위의 항목을 복사합니다.
    remaining = payload[count:]
    return {"notification_return": taken, "pending": notices, "consumed": consumed,
            "remaining": remaining, "would_block_with_work": bool(remaining) and notices == 0}
