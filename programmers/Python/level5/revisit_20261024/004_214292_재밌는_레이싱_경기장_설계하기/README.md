# 재밌는 레이싱 경기장 설계하기 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/214292>) · [재풀이 목록](<../README.md>)

정답률 3%와 풀이 인원 171명은 이번 목록 확인 시점의 값입니다. 전체 4순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

정렬한 높이에서 절반 간격으로 떨어진 값들의 차이를 비교.
기둥이 2m개면 이 차이들의 최솟값이 가능한 최적값. 2m+1개면 절반을 가르는 경계가 한 번 더 겹쳐 두 번째로 작은 차이가 한계.
홀수일 때 차이가 같은 두 쌍도 따로 세야 함. 서로 다른 값만 남겨 두 번째를 찾으면 오답.
정렬 시간 O(N log N), 정렬 결과를 저장할 공간 O(N).

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
def solution(heights):
    ordered = sorted(heights)
    n = len(ordered)
    half = n // 2
    smallest = second = float("inf")
    for left in range(n - half):
        gap = ordered[left + half] - ordered[left]
        if gap < smallest:
            second = smallest
            smallest = gap
        elif gap < second:
            second = gap
    return smallest if n % 2 == 0 else second

# 전체 코드 줄별 설명
# def solution(heights):  # 지점 순서를 바꿔 이웃 높이 차이의 최솟값을 최대화
#     ordered = sorted(heights)  # 높이를 오름차순으로 정렬한 새 리스트
#     n = len(ordered)  # 기둥 수
#     half = n // 2  # 정렬한 목록에서 절반 간격
#     smallest = second = float("inf")  # 가장 작은 간격과 두 번째 간격을 무한대로 초기화
#     for left in range(n - half):  # 절반 간격으로 마주 보는 모든 높이 쌍 확인
#         gap = ordered[left + half] - ordered[left]  # 두 높이의 차이
#         if gap < smallest:  # 지금까지의 최솟값보다 더 작은 차이
#             second = smallest  # 기존 최솟값이 두 번째 값으로 이동
#             smallest = gap  # 새 최솟값 저장
#         elif gap < second:  # 최솟값이 아니어도 두 번째 값이 될 수 있음
#             second = gap  # 같은 값도 별개 쌍이면 두 번째 후보로 포함
#     return smallest if n % 2 == 0 else second  # 짝수는 최소 간격, 홀수는 두 번째 간격이 한계

# 풀이 요약
# 정렬한 높이에서 절반 간격으로 떨어진 값들의 차이를 비교.
# 기둥이 2m개면 이 차이들의 최솟값이 가능한 최적값. 2m+1개면 절반을 가르는 경계가 한 번 더 겹쳐 두 번째로 작은 차이가 한계.
# 홀수일 때 차이가 같은 두 쌍도 따로 세야 함. 서로 다른 값만 남겨 두 번째를 찾으면 오답.
# 정렬 시간 O(N log N), 정렬 결과를 저장할 공간 O(N).
```
