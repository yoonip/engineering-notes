from heapq import heappush, heappop
from collections import Counter

def solution(operations):
    minimum, maximum = [], []
    counts = Counter()
    def clean(heap, sign):
        while heap and counts[sign * heap[0]] == 0:
            heappop(heap)
    for operation in operations:
        command, text = operation.split()
        value = int(text)
        if command == 'I':
            heappush(minimum, value)
            heappush(maximum, -value)
            counts[value] += 1
        else:
            heap, sign = (maximum, -1) if value == 1 else (minimum, 1)
            clean(heap, sign)
            if heap:
                counts[sign * heappop(heap)] -= 1
    clean(minimum, 1)
    clean(maximum, -1)
    return [-maximum[0], minimum[0]] if minimum else [0, 0]

# 전체 코드 줄별 설명
# from heapq import heappush, heappop  # import는 도구 가져오기. 최소 힙은 작은 값부터 꺼내는 자료구조. heappush는 삽입, heappop은 최솟값 추출.
# from collections import Counter  # Counter는 값별 개수를 저장하는 딕셔너리형 자료구조. 없는 값은 0개로 조회됨.
# 
# def solution(operations):  # def는 함수 정의. 삽입·최대/최소 삭제 명령 목록을 받음.
#     minimum, maximum = [], []  # []는 빈 리스트. 최소 힙과 음수를 넣는 최대 힙을 각각 생성.
#     counts = Counter()  # 실제 남아 있는 값의 개수. 두 힙 사이의 삭제 상태를 동기화.
#     def clean(heap, sign):  # 힙 맨 위에 쌓인 이미 삭제된 값을 정리하는 내부 함수.
#         while heap and counts[sign * heap[0]] == 0:  # while은 조건 반복, and는 모두 참, [0]은 힙 최솟값. sign으로 원래 값 복원.
#             heappop(heap)  # 유효하지 않은 힙 원소 삭제. 필요한 시점에만 지우는 지연 삭제 방식.
#     for operation in operations:  # for로 모든 명령 순서대로 처리.
#         command, text = operation.split()  # split은 공백으로 분리. 명령 문자와 숫자 문자열 언패킹.
#         value = int(text)  # int는 문자열을 정수로 변환.
#         if command == 'I':  # ==는 같음. 숫자 삽입 명령.
#             heappush(minimum, value)  # 최소 힙에는 원래 숫자 삽입.
#             heappush(maximum, -value)  # 최대 힙에는 음수 삽입. 원래 최댓값이 가장 작은 음수가 되어 먼저 나옴.
#             counts[value] += 1  # +=는 더해 저장. 같은 숫자가 여러 번 들어와도 개수로 구분.
#         else:  # D 삭제 명령.
#             heap, sign = (maximum, -1) if value == 1 else (minimum, 1)  # 조건부 표현식. 1이면 최댓값, -1이면 최솟값 힙 선택.
#             clean(heap, sign)  # 삭제하기 전에 맨 위의 오래된 값 제거.
#             if heap:  # 힙이 비어 있지 않을 때만 삭제. 빈 큐 삭제 명령은 무시.
#                 counts[sign * heappop(heap)] -= 1  # -=는 빼서 저장. 실제 개수만 줄이고 반대 힙의 원소는 나중에 정리.
#     clean(minimum, 1)  # 최종 최솟값 앞에 남은 삭제 흔적 제거.
#     clean(maximum, -1)  # 최종 최댓값 앞의 삭제 흔적 제거.
#     return [-maximum[0], minimum[0]] if minimum else [0, 0]  # 남아 있으면 최대·최소를 리스트로 반환. 없으면 [0,0].

# 풀이 요약
# 두 힙을 사용하되 실제 남은 개수는 Counter 하나로 관리한다. 한 힙에서 삭제한 값이 다른 힙 맨 위에 나오면 그때 버린다.
# 예: 3을 두 번 넣고 최댓값을 한 번 삭제해도 counts[3]=1이라 다른 3은 남는다. 각 힙에는 같은 값의 오래된 복사본이 있어도 실제 개수로 판정한다.
# 명령 Q개일 때 각 삽입 원소는 힙마다 최대 한 번 삭제되므로 시간 O(Q log Q), 공간 O(Q).
# 