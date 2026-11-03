"""직접 작성한 교육 예제: 합성 로그인 기록에서 이동 시간창의 실패 누적을 찾습니다."""
from collections import defaultdict, deque  # defaultdict는 키별 초기값을, deque는 앞쪽 삭제가 빠른 큐를 제공합니다.

def failure_alerts(events, window=60, threshold=3):  # window초 안에 threshold회 실패한 계정을 찾습니다.
    if window <= 0 or threshold < 1:  # 양수가 아닌 설정을 거부합니다.
        raise ValueError("invalid detector settings")  # 잘못된 설정에 명시적으로 실패합니다.
    pending = defaultdict(deque)  # 계정마다 실패 시각 큐를 만듭니다.
    previous = None  # 이전 이벤트 시각이 아직 없음을 표시합니다.
    alerts = []  # []는 순서가 있는 결과 리스트입니다.
    for event in events:  # for는 입력 이벤트를 순서대로 처리합니다.
        now = event["time"]  # time은 합성 기록의 정수 초입니다.
        if previous is not None and now < previous:  # 시각 역전을 검사합니다.
            raise ValueError("events must be time ordered")  # 조용히 잘못 집계하지 않습니다.
        previous = now  # 다음 이벤트의 순서 검사 기준을 저장합니다.
        queue = pending[event["account"]]  # 요청한 계정의 큐를 가져옵니다.
        while queue and queue[0] <= now - window:  # (now-window, now] 밖의 오래된 실패를 지웁니다.
            queue.popleft()  # deque의 맨 앞 항목을 O(1)에 제거합니다.
        if event["result"] == "failure":  # 이 예제에서 실패한 로그인만 집계합니다.
            queue.append(now)  # 현재 실패 시각을 큐 뒤에 추가합니다.
            if len(queue) >= threshold:  # len은 시간창 안의 실패 횟수입니다.
                alerts.append((event["account"], now, len(queue)))  # 임계값 이상인 사건을 튜플로 기록합니다.
    return alerts  # 입력을 자동 차단하지 않고 경보 후보를 반환합니다.
