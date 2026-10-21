# 로또의 최고 순위와 최저 순위

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/77484) · Level 1 · Python3

유형: 집계 · 경우 나누기

## 풀이 원리

확실히 맞힌 수와 알아볼 수 없는 0의 수를 셉니다. 최고 순위는 0이 전부 당첨인 경우, 최저 순위는 0이 전부 빗나간 경우입니다. 0개·1개를 맞혀도 6등이므로 7-일치수의 상한을 6으로 제한합니다.

로또와 당첨 번호가 각각 6개이므로 시간·보조 공간 O(1).

## 공식 예제

입력 인수: `[[44, 1, 0, 0, 31, 25], [31, 10, 45, 1, 6, 19]]`

반환값: `[3, 5]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(lottos, win_nums):
    matched = 0
    unknown = lottos.count(0)
    for number in lottos:
        if number in win_nums:
            matched += 1
    best_rank = min(6, 7 - (matched + unknown))
    worst_rank = min(6, 7 - matched)
    return [best_rank, worst_rank]

# 전체 코드 줄별 설명
# def solution(lottos, win_nums):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. lottos: 구매한 로또 번호, win_nums: 당첨 번호 목록
#     matched = 0  # =는 값 저장. 알아볼 수 있는 번호 중 당첨 번호와 일치하는 개수를 저장
#     unknown = lottos.count(0)  # count는 등장 횟수. =는 값 저장. 0의 개수를 셈. 0은 지워져서 알 수 없는 번호를 의미
#     for number in lottos:  # for·in은 원소를 차례로 꺼내는 반복문. 구매한 번호를 하나씩 꺼내서 확인
#         if number in win_nums:  # if는 조건이 참일 때 실행. in은 포함 여부. 현재 번호가 당첨 번호 목록 안에 있는지 검사
#             matched += 1  # +=는 더하거나 연결한 값을 저장. 당첨 번호에 있다면 맞은 개수를 1 증가시킴
#     best_rank = min(6, 7 - (matched + unknown))  # min은 최솟값. =는 값 저장. 모르는 번호까지 전부 맞았을 때의 최고 순위
#     worst_rank = min(6, 7 - matched)  # min은 최솟값. =는 값 저장. 모르는 번호가 전부 틀렸을 때의 최저 순위
#     return [best_rank, worst_rank]  # return은 결과를 돌려주고 함수 종료. []는 리스트. [최고 순위, 최저 순위]를 리스트로 반환

# 풀이 요약
# 확실히 맞힌 수와 알아볼 수 없는 0의 수를 센다. 최고 순위는 0이 전부 당첨인 경우, 최저 순위는 0이 전부 빗나간 경우다. 0개·1개를 맞혀도 6등이므로 7-일치수의 상한을 6으로 제한한다.
# 로또와 당첨 번호가 각각 6개이므로 시간·보조 공간 O(1).
```

## 확인한 범위

2026-10-16 01:53:28의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
