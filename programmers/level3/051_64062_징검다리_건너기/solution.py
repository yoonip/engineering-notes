# deque는 앞·뒤 삽입과 삭제가 빠른 양방향 큐.
from collections import deque

# 디딤돌 내구도와 최대 점프 칸 수를 받음.
def solution(stones, k):
    # 내구도가 큰 순서로 후보 인덱스를 보관하는 단조 큐 생성.
    queue = deque()
    # 각 k칸 구간 최댓값 중 최솟값을 찾을 초기값.
    answer = float('inf')
    # 오른쪽 끝을 늘림.
    for i, value in enumerate(stones):
        # 현재 k칸 구간에서 벗어난 후보 제외.
        while queue and queue[0] <= i - k:
            # popleft는 앞 원소를 꺼내 삭제.
            queue.popleft()
        # 새 돌보다 작거나 같은 오래된 후보는 앞으로 최댓값이 될 수 없음.
        while queue and stones[queue[-1]] <= value:
            # pop은 뒤 원소를 꺼내 삭제.
            queue.pop()
        # 새 디딤돌 인덱스 저장.
        queue.append(i)
        # k칸이 모두 모인 구간부터 답 계산.
        if i >= k - 1:
            # 큐 맨 앞은 현재 구간에서 가장 큰 내구도의 돌.
            answer = min(answer, stones[queue[0]])
    # 모든 k칸 구간 중 가장 먼저 완전히 사라지는 구간의 소진 인원 수.
    return answer
