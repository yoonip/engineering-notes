# 두 개 뽑아서 더하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/68644) · Level 1 · Python3

유형: 완전탐색 · 집합 · 정렬

## 풀이 원리

서로 다른 두 인덱스를 i<j로 골라 모든 합을 구합니다. 집합은 같은 합을 한 번만 남기고, 마지막 sorted가 오름차순 리스트를 만듭니다. 같은 값의 숫자라도 인덱스가 다르면 고를 수 있습니다.

원소 N개, 서로 다른 합 K개: 시간 O(N²+K log K), 공간 O(K).

## 공식 예제

입력 인수: `[[2, 1, 3, 4, 1]]`

반환값: `[2, 3, 4, 5, 6, 7]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(numbers):
    result = set()
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            result.add(numbers[i] + numbers[j])
    answer = sorted(result)
    return answer

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 정수 배열 numbers를 입력받는 함수
#     result = set()  # set은 중복 없는 집합. =는 값 저장. 중복된 합계를 자동으로 제거하는 빈 집합 생성
#     for i in range(len(numbers)):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 첫 번째 숫자의 인덱스 i를 0부터 끝까지 순회
#         for j in range(i + 1, len(numbers)):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 두 번째 숫자는 i 다음 위치부터 순회하여 같은 인덱스와 중복 조합 방지
#             result.add(numbers[i] + numbers[j])  # add는 집합에 원소 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 서로 다른 두 위치의 숫자를 더해 집합에 추가
#     answer = sorted(result)  # sorted는 정렬한 새 리스트. =는 값 저장. 집합의 숫자들을 오름차순으로 정렬하여 리스트 생성
#     return answer  # return은 결과를 돌려주고 함수 종료. 중복 없이 정렬된 합계 리스트 반환

# 풀이 요약
# 서로 다른 두 인덱스를 i<j로 골라 모든 합을 구한다. 집합은 같은 합을 한 번만 남기고, 마지막 sorted가 오름차순 리스트를 만든다. 같은 값의 숫자라도 인덱스가 다르면 고를 수 있다.
# 원소 N개, 서로 다른 합 K개: 시간 O(N²+K log K), 공간 O(K).
```

## 확인한 범위

2026-10-16 02:30:28의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
