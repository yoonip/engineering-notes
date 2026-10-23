def solution(n, data):
    groups = []
    for x, y in sorted(data):
        if not groups or groups[-1][0] != x:
            groups.append((x, []))
        groups[-1][1].append(y)
    answer = 0
    for i, (x, heights) in enumerate(groups):
        for y in heights:
            low, high = -1, 2 ** 31
            for j in range(i + 1, len(groups)):
                others = groups[j][1]
                for other in others:
                    if other != y and low <= other <= high:
                        answer += 1
                for other in others:
                    if other > y:
                        high = min(high, other)
                    elif other < y:
                        low = max(low, other)
    return answer

# 전체 코드 줄별 설명
# def solution(n, data):  # def는 함수 정의. 쐐기 개수와 좌표 목록 입력.
#     groups = []  # []는 리스트. 같은 x의 y좌표를 묶어서 저장.
#     for x, y in sorted(data):  # sorted는 x·y순 정렬, for에서 좌표 언패킹.
#         if not groups or groups[-1][0] != x:  # not은 비어 있음 검사, or는 하나라도 참. 새 x좌표면 그룹 추가.
#             groups.append((x, []))  # append는 추가, ()는 튜플. x와 수정 가능한 y목록을 묶음.
#         groups[-1][1].append(y)  # [-1]은 마지막 그룹. 해당 y를 목록에 추가.
#     answer = 0  # 유효한 꼭짓점 쌍 수.
#     for i, (x, heights) in enumerate(groups):  # enumerate는 인덱스·값 제공. 왼쪽 x그룹 순회.
#         for y in heights:  # 왼쪽 꼭짓점의 y를 하나씩 고정.
#             low, high = -1, 2 ** 31  # **는 거듭제곱. 안쪽에 나타난 가장 가까운 아래·위 y경계 초기화.
#             for j in range(i + 1, len(groups)):  # 더 큰 x의 그룹만 순회해 너비 0과 중복 쌍 방지.
#                 others = groups[j][1]  # 현재 오른쪽 x의 y목록.
#                 for other in others:  # 같은 x그룹을 우선 모두 후보로 검사.
#                     if other != y and low <= other <= high:  # !=는 다름. 높이가 양수이고 경계를 넘지 않으면 안쪽 점이 없음. 같은 y경계는 직사각형 변이라 허용.
#                         answer += 1  # +=는 더해 저장. 유효한 텐트 쌍 증가.
#                 for other in others:  # 다음 x그룹을 보기 전에 현재 점들을 내부 후보로 반영.
#                     if other > y:  # 기준 y보다 위에 있는 점.
#                         high = min(high, other)  # min은 최솟값. 가장 가까운 위쪽 장애 y 유지.
#                     elif other < y:  # elif는 추가 조건. 기준보다 아래에 있는 점.
#                         low = max(low, other)  # max는 최댓값. 가장 가까운 아래쪽 장애 y 유지.
#     return answer  # 내부에 다른 쐐기가 없는 쌍 수 반환.

# 풀이 요약
# 점을 x순으로 정렬한다. 왼쪽 꼭짓점 하나를 고정하고 오른쪽으로 훑으며, 지금까지 안쪽 x구간에서 본 y 중 기준보다 바로 위·아래 값을 경계로 유지한다.
# 오른쪽 꼭짓점의 y가 그 경계를 넘으면 내부에 쐐기가 생긴다. 같은 x의 점들은 모두 후보로 검사한 후 경계를 갱신해 직사각형 경계의 점을 허용한다.
# 예제는 세 쌍만 가능하고 (0,2)-(2,0)은 (1,1)이 안에 있어 제외된다. 시간 O(N²+N log N), 공간 O(N).
# 