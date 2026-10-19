# 과일 장수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/135808) · Level 1 · Python3

유형: 그리디 · 정렬

## 풀이 원리

점수를 내림차순으로 정렬해 좋은 사과끼리 m개씩 묶습니다. 한 상자의 가격은 그 안의 최솟값×m이므로 각 묶음의 마지막 값만 읽으면 됩니다. m개를 채우지 못하는 나머지는 팔지 않습니다.

사과 N개: 시간 O(N log N), Python 정렬의 보조 공간 상한 O(N).

## 공식 예제

입력 인수: `[3, 4, [1, 2, 3, 1, 2, 3, 1]]`

반환값: `8`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(k, m, score):
    answer = 0
    score.sort(reverse=True)
    for i in range(m - 1, len(score), m):
        answer += score[i] * m
    return answer

# 전체 코드 줄별 설명
# def solution(k, m, score):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. k: 최고 점수, m: 상자당 사과 수, score: 사과별 점수 목록
#     answer = 0  # =는 값 저장. 모든 상자를 판매해서 얻는 총금액을 저장
#     score.sort(reverse=True)  # sort는 원래 리스트 정렬. =는 이름 붙인 인수에 값 지정. True·False는 참·거짓. 점수 목록을 큰 값부터 작은 값 순서로 정렬
#     for i in range(m - 1, len(score), m):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 완성된 각 상자의 마지막 사과 위치만 확인
#         answer += score[i] * m  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 상자의 최저 점수 × 사과 수를 총금액에 더함
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 상자의 판매 금액을 합한 최대 이익을 반환

# 풀이 요약
# 점수를 내림차순으로 정렬해 좋은 사과끼리 m개씩 묶는다. 한 상자의 가격은 그 안의 최솟값×m이므로 각 묶음의 마지막 값만 읽으면 된다. m개를 채우지 못하는 나머지는 팔지 않는다.
# 사과 N개: 시간 O(N log N), Python 정렬의 보조 공간 상한 O(N).
```

## 확인한 범위

2026-10-16 01:00:04의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
