# 방의 개수 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/49190>) · [재풀이 목록](<../README.md>)

정답률 8%와 풀이 인원 3318명은 이번 목록 확인 시점의 값입니다. 전체 1순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

새 간선으로 이미 방문한 점에 도착할 때만 방이 하나 늘어남. 같은 선분을 다시 지나갈 때는 방향 비트가 이미 있어 건너뛰기.
모든 이동을 두 번으로 나눠 대각선끼리 만나는 중간점도 꼭짓점으로 처리.
최대 20만 칸 이동하므로 y 좌표 차이는 40만 이하. x*400001+y로 좌표를 충돌 없이 묶어 튜플·간선 집합 대신 점별 방향 딕셔너리 하나 사용.
시간과 공간 모두 O(N).

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
def solution(arrows):
    base = 400001
    moves = (1, base + 1, base, base - 1, -1, -base - 1, -base, -base + 1)
    visited = {0: 0}
    position = 0
    rooms = 0
    for direction in arrows:
        step = moves[direction]
        forward = 1 << direction
        backward = 1 << ((direction + 4) & 7)
        for _ in range(2):
            following = position + step
            if not visited[position] & forward:
                old = visited.get(following)
                if old is None:
                    old = 0
                else:
                    rooms += 1
                visited[position] |= forward
                visited[following] = old | backward
            position = following
    return rooms

# 전체 코드 줄별 설명
# def solution(arrows):  # 방향 배열을 받아 닫힌 방 개수를 계산하는 함수
#     base = 400001  # 좌표를 정수 하나로 묶을 간격; 두 배 격자의 y 차이보다 크게 잡기
#     moves = (1, base + 1, base, base - 1, -1, -base - 1, -base, -base + 1)  # 위부터 시계 방향으로 x*base+y의 변화량을 튜플에 저장
#     visited = {0: 0}  # 딕셔너리 키는 좌표, 값은 이미 그은 여덟 방향의 비트
#     position = 0  # 원점의 좌표 키로 시작
#     rooms = 0  # 새로 닫힌 방 수
#     for direction in arrows:  # 이동 방향을 입력 순서대로 처리
#         step = moves[direction]  # 해당 방향으로 한 칸 움직일 때의 키 변화
#         forward = 1 << direction  # 현재 점에서 나가는 간선을 표시할 비트
#         backward = 1 << ((direction + 4) & 7)  # 도착점에서 반대로 돌아오는 방향 비트
#         for _ in range(2):  # 한 이동을 두 번으로 나눠 대각선의 중간 교차점도 방문
#             following = position + step  # 다음 점의 정수 좌표 키
#             if not visited[position] & forward:  # 처음 그리는 간선일 때만 방 증가 여부 확인
#                 old = visited.get(following)  # 처음 보는 점이면 None, 방문한 점이면 방향 비트 반환
#                 if old is None:  # 새 점으로 뻗는 간선은 방을 만들지 않음
#                     old = 0  # 새 점의 방향 표시를 빈 상태로 시작
#                 else:  # 새 간선으로 기존 점에 닿는 경우
#                     rooms += 1  # 닫힌 영역 하나가 추가됨
#                 visited[position] |= forward  # 현재 점의 나가는 간선을 기록
#                 visited[following] = old | backward  # 도착점에도 같은 무방향 간선의 반대 방향을 기록
#             position = following  # 다음 이동의 출발점 갱신
#     return rooms  # 완성된 방 수 반환

# 풀이 요약
# 새 간선으로 이미 방문한 점에 도착할 때만 방이 하나 늘어남. 같은 선분을 다시 지나갈 때는 방향 비트가 이미 있어 건너뛰기.
# 모든 이동을 두 번으로 나눠 대각선끼리 만나는 중간점도 꼭짓점으로 처리.
# 최대 20만 칸 이동하므로 y 좌표 차이는 40만 이하. x*400001+y로 좌표를 충돌 없이 묶어 튜플·간선 집합 대신 점별 방향 딕셔너리 하나 사용.
# 시간과 공간 모두 O(N).
```
