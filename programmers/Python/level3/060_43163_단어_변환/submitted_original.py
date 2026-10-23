from collections import deque

def solution(begin, target, words):
    if target not in words:
        return 0
    queue = deque([(begin, 0)])
    visited = {begin}
    while queue:
        word, steps = queue.popleft()
        if word == target:
            return steps
        for candidate in words:
            if candidate not in visited and sum(a != b for a, b in zip(word, candidate)) == 1:
                visited.add(candidate)
                queue.append((candidate, steps + 1))
    return 0

# 전체 코드 줄별 설명
# from collections import deque  # import는 도구 가져오기. deque는 먼저 넣은 원소를 앞에서 빠르게 꺼내는 BFS용 큐.
# 
# def solution(begin, target, words):  # def는 함수 정의. 시작 단어·목표 단어·사용 가능한 단어 목록을 받음.
#     if target not in words:  # not in은 포함되어 있지 않음. 목표가 목록에 없으면 변환 불가능.
#         return 0  # 불가능을 뜻하는 0 반환.
#     queue = deque([(begin, 0)])  # []는 리스트, ()는 튜플. (단어,변환 횟수)를 담은 선입선출 큐 생성.
#     visited = {begin}  # {} 안 원소만 쓰면 집합. 이미 발견한 단어를 저장.
#     while queue:  # 큐가 비어 있지 않은 동안 너비 우선 탐색(BFS).
#         word, steps = queue.popleft()  # popleft는 앞 원소를 꺼내 삭제. 두 값을 언패킹.
#         if word == target:  # ==는 같음. 목표 단어에 도달했는지 검사.
#             return steps  # BFS는 적은 변환 횟수부터 방문하므로 처음 도착한 횟수가 최소.
#         for candidate in words:  # for로 다음 변환 후보 단어 순회.
#             if candidate not in visited and sum(a != b for a, b in zip(word, candidate)) == 1:  # and는 모두 참, zip은 같은 위치 글자끼리 묶음, !=는 다름. sum은 다른 글자의 수를 합산해 정확히 하나인지 검사.
#                 visited.add(candidate)  # add는 집합에 원소 추가. 큐에 넣을 때 방문 표시해 중복 탐색 방지.
#                 queue.append((candidate, steps + 1))  # append는 끝에 추가. 한 번 변환한 다음 단어를 큐에 넣음.
#     return 0  # 큐가 빌 때까지 목표에 도달하지 못하면 불가능.

# 풀이 요약
# 단어를 노드, 한 글자만 다른 단어 사이를 간선으로 보고 BFS한다. 한 번 변환할 때마다 비용이 1이므로 최단 단계가 나온다.
# 예: hit→hot→dot→dog→cog는 네 번 변환. 목표가 목록에 없거나 이어지는 길이 없으면 0이다.
# 단어 수 W≤50, 글자 수 L≤10. 시간 O(W²·L), 공간 O(W).
# 