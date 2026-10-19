# 예산

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12982) · Level 1 · Python3

유형: 그리디 · 정렬

## 풀이 원리

요청 금액이 작은 부서부터 지원합니다. 같은 개수의 부서를 지원할 때 가장 작은 금액들을 고르면 지출이 최소입니다. 정렬한 다음 요청이 예산을 넘으면 그 뒤의 더 비싼 요청도 지원할 수 없으므로 멈춥니다.

부서 N개: 시간 O(N log N), Python 정렬 보조 공간 상한 O(N). 입력을 정렬합니다.

## 공식 예제

입력 인수: `[[1, 3, 2, 5, 4], 9]`

반환값: `3`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(d, budget):
    d.sort()
    total = 0
    answer = 0
    for cost in d:
        if total + cost>budget:
            break
        total +=cost
        answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(d, budget):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 요청 금액들과 전체 예산을 입력받음.
#     d.sort()  # sort는 원래 리스트 정렬. 적은 금액부터 지원하도록 정렬.
#     total = 0  # =는 값 저장. 지원한 금액 합계 초기화.
#     answer = 0  # =는 값 저장. 지원한 부서 수 초기화.
#     for cost in d:  # for·in은 원소를 차례로 꺼내는 반복문. 정렬한 요청 금액을 순서대로 확인.
#         if total + cost>budget:  # if는 조건이 참일 때 실행. >는 큼 비교. 이번 요청까지 지원하면 예산을 초과하는지 확인.
#             break  # break는 가장 가까운 반복문 종료. 이후 요청도 더 비싸므로 지원 중단.
#         total +=cost  # +=는 더하거나 연결한 값을 저장. 지원 금액 누적.
#         answer += 1  # +=는 더하거나 연결한 값을 저장. 지원 부서 수 증가.
#     return answer  # return은 결과를 돌려주고 함수 종료. 지원 가능한 최대 부서 수 반환.

# 풀이 요약
# 요청 금액이 작은 부서부터 지원한다. 같은 개수의 부서를 지원할 때 가장 작은 금액들을 고르면 지출이 최소다. 정렬한 다음 요청이 예산을 넘으면 그 뒤의 더 비싼 요청도 지원할 수 없으므로 멈춘다.
# 부서 N개: 시간 O(N log N), Python 정렬 보조 공간 상한 O(N). 입력을 정렬한다.
```

## 확인한 범위

2026-10-17 15:11:34의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
