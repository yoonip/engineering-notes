import sys  # 그래프 정수 입력 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
left_count, right_count, edge_count = next(tokens), next(tokens), next(tokens)  # 두 집합과 간선 수
adjacent = [[] for _ in range(left_count)]  # 사람별 허용 작업
for _ in range(edge_count):  # 중복 없는 관계 입력
    left, right = next(tokens), next(tokens)  # 간선 양끝
    adjacent[left].append(right)  # 작업 후보 추가
owner = [-1] * right_count  # 작업을 맡은 왼쪽 정점
def augment(left, visited):  # 기존 배정을 바꾸는 증가 경로
    for right in adjacent[left]:  # 허용 작업 순회
        if visited[right]:  # 이번 탐색에서 이미 본 작업
            continue  # 순환 탐색 제외
        visited[right] = True  # 작업 방문 표시
        if owner[right] == -1 or augment(owner[right], visited):  # 빈 작업이나 재배정 성공
            owner[right] = left  # 현재 사람에게 연결
            return 1  # 매칭 크기 증가
    return 0  # 증가 경로 부재
answer = 0  # 현재 매칭 수
for left in range(left_count):  # 각 사람의 추가 배정 시도
    answer += augment(left, [False] * right_count)  # 탐색마다 독립 방문 표
print(answer)  # 최대 매칭 크기
