# 방의 개수

[Level 5 목록 / Level 5 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/49190) · Level 5 · Python3

## 풀이

새로운 선분으로 기존 꼭짓점에 도착하면 방이 하나 늘어납니다. 이미 그은 선분을 되짚을 때는 늘어나지 않습니다.
한 이동을 두 단계로 쪼개 대각선끼리 중간에서 교차하는 점도 반드시 기록합니다. 예제 답은 3이며 시간·공간은 O(N)입니다.

## 정답이 되는 이유

한 번도 그리지 않은 선분으로 이미 방문한 점에 닿으면 새로운 닫힌 영역이 하나 생깁니다. 지나갔던 선분을 되짚는 경우는 영역이 늘지 않습니다. 무방향 선분은 두 끝점의 순서를 통일해 집합에 넣으므로 왕복을 같은 선분으로 알아봅니다.

각 이동을 두 번의 작은 이동으로 나누는 이유는 대각선 교차 때문입니다. 원래 격자의 한 칸 안에서 만나는 두 대각선의 교점도, 좌표를 두 배로 늘리면 정수 좌표로 기록됩니다. 이 점을 빼먹으면 교차로 생기는 방을 놓칩니다.

작은 예 `[0, 2, 4, 6]`은 위·오른쪽·아래·왼쪽으로 돌아와 방 하나를 만듭니다. 이어 같은 사각형을 한 번 더 돌아도 이미 그린 선분뿐이므로 답은 여전히 1입니다. 이동 수가 N이면 집합 조회의 평균 비용을 기준으로 시간 `O(N)`, 공간 `O(N)`입니다.

## Reasoning

A new edge reaching an existing vertex creates one additional enclosed face. Retracing an edge adds none, so endpoints are normalized before inserting an undirected edge into the set. Doubling every move makes diagonal intersections integer vertices. `[0,2,4,6]` draws one square; tracing it again keeps the answer at one. Expected time is `O(N)` with hash-set operations and space is `O(N)`.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arrows):
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    current = (0, 0)
    vertices = {current}
    edges = set()
    rooms = 0
    for arrow in arrows:
        dx, dy = directions[arrow]
        for _ in range(2):
            following = (current[0] + dx, current[1] + dy)
            edge = (current, following) if current < following else (following, current)
            if edge not in edges:
                if following in vertices:
                    rooms += 1
                edges.add(edge)
                vertices.add(following)
            current = following
    return rooms

# 전체 코드 줄별 설명
# def solution(arrows):  # def는 함수 정의. arrows는 0~7 방향 번호를 담은 입력 리스트.
#     directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))  # ()는 변경 불가 튜플. 위부터 시계 방향으로 좌표 변화량 저장.
#     current = (0, 0)  # 현재 좌표를 두 정수의 튜플로 저장. 튜플은 집합의 원소로 사용 가능.
#     vertices = {current}  # {}에 원소를 쓰면 집합 set. 방문 좌표를 중복 없이 저장하고 빠르게 조회.
#     edges = set()  # set()은 빈 집합. 이미 그은 무방향 선분을 저장.
#     rooms = 0  # 새로 완성된 방의 개수 초기화.
#     for arrow in arrows:  # for는 반복문. 입력 방향을 차례대로 처리.
#         dx, dy = directions[arrow]  # []로 인덱스 접근. 튜플의 두 값을 dx, dy로 나누어 받음.
#         for _ in range(2):  # range(2)는 0,1. 한 이동을 두 단계로 나누어 대각선 교차점도 좌표로 처리. _는 사용하지 않는 변수.
#             following = (current[0] + dx, current[1] + dy)  # 현재 x·y에 방향 변화량을 더해 다음 좌표 계산.
#             edge = (current, following) if current < following else (following, current)  # 조건 표현식. 튜플은 앞 값부터 비교하여 두 끝점의 순서를 통일.
#             if edge not in edges:  # if는 조건문, not in은 집합에 없음. 처음 그리는 선분만 검사.
#                 if following in vertices:  # in은 포함 여부. 새 선분으로 이미 방문한 점에 닿으면 닫힌 방 하나 생성.
#                     rooms += 1  # +=는 기존 값에 더해 저장. 방 개수 1 증가.
#                 edges.add(edge)  # add는 집합에 원소 추가. 이 선분을 그렸다고 기록.
#                 vertices.add(following)  # 도착 좌표를 방문 집합에 기록. 이미 있으면 변화 없음.
#             current = following  # 다음 반복을 위해 현재 위치를 도착 좌표로 갱신.
#     return rooms  # return은 함수 결과 반환. 총 방 개수 출력.

# 풀이 요약
# 새로운 선분으로 기존 꼭짓점에 도착하면 방이 하나 늘어납니다. 이미 그은 선분을 되짚을 때는 늘어나지 않습니다.
# 한 이동을 두 단계로 쪼개 대각선끼리 중간에서 교차하는 점도 반드시 기록합니다. 예제 답은 3이며 시간·공간은 O(N)입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
