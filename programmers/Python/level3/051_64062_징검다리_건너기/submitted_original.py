from collections import deque

def solution(stones, k):
    queue = deque()
    answer = float('inf')
    for i, value in enumerate(stones):
        while queue and queue[0] <= i - k:
            queue.popleft()
        while queue and stones[queue[-1]] <= value:
            queue.pop()
        queue.append(i)
        if i >= k - 1:
            answer = min(answer, stones[queue[0]])
    return answer

# 전체 코드 줄별 설명
# from collections import deque  # import는 도구 가져오기. deque는 앞·뒤 삽입과 삭제가 빠른 양방향 큐.
# 
# def solution(stones, k):  # def는 함수 정의. 디딤돌 내구도와 최대 점프 칸 수를 받음.
#     queue = deque()  # 내구도가 큰 순서로 후보 인덱스를 보관하는 단조 큐 생성.
#     answer = float('inf')  # float('inf')는 무한대. 각 k칸 구간 최댓값 중 최솟값을 찾을 초기값.
#     for i, value in enumerate(stones):  # enumerate는 인덱스와 원소를 함께 제공. 오른쪽 끝을 늘림.
#         while queue and queue[0] <= i - k:  # while은 조건 반복, and는 모두 참. [0]은 맨 앞. 현재 k칸 구간에서 벗어난 후보 제외.
#             queue.popleft()  # popleft는 앞 원소를 꺼내 삭제.
#         while queue and stones[queue[-1]] <= value:  # [-1]은 마지막 원소. 새 돌보다 작거나 같은 오래된 후보는 앞으로 최댓값이 될 수 없음.
#             queue.pop()  # pop은 뒤 원소를 꺼내 삭제.
#         queue.append(i)  # append는 끝에 추가. 새 디딤돌 인덱스 저장.
#         if i >= k - 1:  # k칸이 모두 모인 구간부터 답 계산.
#             answer = min(answer, stones[queue[0]])  # min은 최솟값. 큐 맨 앞은 현재 구간에서 가장 큰 내구도의 돌.
#     return answer  # 모든 k칸 구간 중 가장 먼저 완전히 사라지는 구간의 소진 인원 수.

# 풀이 요약
# 연속 k개 돌이 모두 0이 되면 다음 사람은 k+1칸을 뛰어야 하므로 실패한다. 한 구간이 모두 소진되는 인원은 그 구간의 최대 내구도다.
# 따라서 길이 k인 모든 구간의 최댓값 중 최솟값이 답이다. 단조 큐로 각 구간의 최댓값을 빠르게 유지한다.
# 예제는 [3,2,1] 구간의 최대가 3이어서 세 명까지 가능하다. 각 인덱스는 한 번 들어오고 나가므로 시간 O(N), 공간 O(K).
# 