# heappush는 삽입, heappop은 최솟값 추출.
from heapq import heappush, heappop
# 없는 값은 0개로 조회됨.
from collections import Counter

# 삽입·최대/최소 삭제 명령 목록을 받음.
def solution(operations):
    # 최소 힙과 음수를 넣는 최대 힙을 각각 생성.
    minimum, maximum = [], []
    # 두 힙 사이의 삭제 상태를 동기화.
    counts = Counter()
    # 힙 맨 위에 쌓인 이미 삭제된 값을 정리하는 내부 함수.
    def clean(heap, sign):
        # sign으로 원래 값 복원.
        while heap and counts[sign * heap[0]] == 0:
            # 필요한 시점에만 지우는 지연 삭제 방식.
            heappop(heap)
    # for로 모든 명령 순서대로 처리.
    for operation in operations:
        # 명령 문자와 숫자 문자열 언패킹.
        command, text = operation.split()
        # int는 문자열을 정수로 변환.
        value = int(text)
        # 숫자 삽입 명령.
        if command == 'I':
            # 최소 힙에는 원래 숫자 삽입.
            heappush(minimum, value)
            # 원래 최댓값이 가장 작은 음수가 되어 먼저 나옴.
            heappush(maximum, -value)
            # 같은 숫자가 여러 번 들어와도 개수로 구분.
            counts[value] += 1
        else:
            # 1이면 최댓값, -1이면 최솟값 힙 선택.
            heap, sign = (maximum, -1) if value == 1 else (minimum, 1)
            # 삭제하기 전에 맨 위의 오래된 값 제거.
            clean(heap, sign)
            # 빈 큐 삭제 명령은 무시.
            if heap:
                # 실제 개수만 줄이고 반대 힙의 원소는 나중에 정리.
                counts[sign * heappop(heap)] -= 1
    # 최종 최솟값 앞에 남은 삭제 흔적 제거.
    clean(minimum, 1)
    # 최종 최댓값 앞의 삭제 흔적 제거.
    clean(maximum, -1)
    # 없으면 [0,0].
    return [-maximum[0], minimum[0]] if minimum else [0, 0]
