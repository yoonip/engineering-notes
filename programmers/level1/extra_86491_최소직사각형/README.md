# 최소직사각형

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/86491) · Level 1 · Python3

유형: 그리디 · 회전 · 최댓값

## 풀이 원리

명함의 긴 변을 가로, 짧은 변을 세로로 통일합니다. 가장 긴 긴 변과 가장 긴 짧은 변을 각각 수용하는 지갑이면 전부 들어갑니다. 두 최대 길이보다 작게 줄일 수는 없으므로 그 곱이 최소 넓이입니다.

명함 N개: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[[60, 50], [30, 70], [60, 30], [80, 40]]]`

반환값: `4000`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

원본에는 `solution`이 2번 정의돼 있습니다. Python은 나중에 나온 같은 이름의 정의를 사용하므로 마지막 함수가 실제로 호출됩니다. 위 실행 부분도 원본의 정의 순서를 유지했습니다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(sizes):
    max_width = 0
    max_height = 0
    for width, height in sizes:
        long_side = max(width, height)
        short_side = min(width, height)
        max_width = max(max_width, long_side)
        max_height = max(max_height, short_side)
    return max_width * max_height

def solution(sizes):
    max_width = 0
    max_height = 0
    for width, height in sizes:
        long_side = max(width, height)
        short_side = min(width, height)
        if long_side > max_width:
            max_width = long_side
        if short_side > max_height:
            max_height = short_side
    return max_width * max_height

# 전체 코드 줄별 설명
# def solution(sizes):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. sizes: 각 명함의 [가로, 세로]가 들어 있는 리스트
#     max_width = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 가로 길이. 처음에는 0으로 시작
#     max_height = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 세로 길이. 처음에는 0으로 시작
#     for width, height in sizes:  # for·in은 원소를 차례로 꺼내는 반복문. 명함을 하나씩 꺼내 가로와 세로를 각각 변수에 저장
#         long_side = max(width, height)  # max는 최댓값. =는 값 저장. 두 길이 중 큰 값 → 이 명함의 가로로 사용할 길이
#         short_side = min(width, height)  # min은 최솟값. =는 값 저장. 두 길이 중 작은 값 → 이 명함의 세로로 사용할 길이
#         max_width = max(max_width, long_side)  # max는 최댓값. =는 값 저장. 지금까지 확인한 긴 변 중 가장 큰 값을 유지
#         max_height = max(max_height, short_side)  # max는 최댓값. =는 값 저장. 지금까지 확인한 짧은 변 중 가장 큰 값을 유지
#     return max_width * max_height  # return은 결과를 돌려주고 함수 종료. 필요한 가로 길이 × 세로 길이로 최소 넓이를 반환
# 
# def solution(sizes):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. sizes: 각 명함의 [가로, 세로]가 들어 있는 리스트
#     max_width = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 가로 길이. 처음에는 0으로 시작
#     max_height = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 세로 길이. 처음에는 0으로 시작
#     for width, height in sizes:  # for·in은 원소를 차례로 꺼내는 반복문. 명함을 하나씩 꺼내 가로와 세로를 각각 변수에 저장
#         long_side = max(width, height)  # max는 최댓값. =는 값 저장. 두 길이 중 큰 값 → 이 명함의 가로로 사용할 길이
#         short_side = min(width, height)  # min은 최솟값. =는 값 저장. 두 길이 중 작은 값 → 이 명함의 세로로 사용할 길이
#         if long_side > max_width:  # if는 조건이 참일 때 실행. >는 큼 비교. 긴 변의 최대 길이를 새로 갱신해야 하는지 비교.
#             max_width = long_side  # =는 값 저장. 새로운 최대 긴 변 길이 저장.
#         if short_side > max_height:  # if는 조건이 참일 때 실행. >는 큼 비교. 짧은 변의 최대 길이를 갱신해야 하는지 비교.
#             max_height = short_side  # =는 값 저장. 새로운 최대 짧은 변 길이 저장.
#     return max_width * max_height  # return은 결과를 돌려주고 함수 종료. 필요한 가로 길이 × 세로 길이로 최소 넓이를 반환

# 풀이 요약
# 명함의 긴 변을 가로, 짧은 변을 세로로 통일한다. 가장 긴 긴 변과 가장 긴 짧은 변을 각각 수용하는 지갑이면 전부 들어간다. 두 최대 길이보다 작게 줄일 수는 없으므로 그 곱이 최소 넓이다.
# 명함 N개: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 17:33:36의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
