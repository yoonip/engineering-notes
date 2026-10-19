# 푸드 파이트 대회

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/134240) · Level 1 · Python3

유형: 문자열 · 대칭 구성

## 풀이 원리

각 음식 수의 절반만 한쪽 참가자에게 배정하고 번호순으로 나열한다. 반대편은 같은 순서를 거꾸로 배치해야 양쪽의 종류와 수가 같다. 가운데 물 0을 넣어 왼쪽+0+뒤집은 왼쪽을 만든다.

출력 길이 L: 문자열 연결 복사까지 고려한 시간 상한 O(L²), 공간 O(L).

## 공식 예제

입력 인수: `[[1, 3, 4, 6]]`

반환값: `"1223330333221"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(food):
    left = ""
    for i in range(1, len(food)):
        count = food[i] // 2
        left += str(i) * count
    answer = left + "0" + left[::-1]
    return answer

# 전체 코드 줄별 설명
# def solution(food):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 음식 종류별 개수가 담긴 리스트를 입력받음
#     left = ""  # =는 값 저장. 왼쪽 선수의 음식 배치를 저장할 빈 문자열
#     for i in range(1, len(food)):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 1번 음식부터 마지막 음식까지 반복 (0번은 물이므로 제외)
#         count = food[i] // 2  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. //는 내림한 정수 몫. =는 값 저장. 두 선수가 똑같이 먹어야 하므로 음식 개수를 2로 나눈 몫 계산
#         left += str(i) * count  # str은 문자열 변환. +=는 더하거나 연결한 값을 저장. 음식 번호를 문자열로 변환하고 개수만큼 반복해서 추가
#     answer = left + "0" + left[::-1]  # [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. 왼쪽 배치 + 가운데 물(0) + 왼쪽 배치를 뒤집은 오른쪽 배치
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 음식 배치 문자열 반환

# 풀이 요약
# 각 음식 수의 절반만 한쪽 참가자에게 배정하고 번호순으로 나열한다. 반대편은 같은 순서를 거꾸로 배치해야 양쪽의 종류와 수가 같다. 가운데 물 0을 넣어 왼쪽+0+뒤집은 왼쪽을 만든다.
# 출력 길이 L: 문자열 연결 복사까지 고려한 시간 상한 O(L²), 공간 O(L).
```

## 확인한 범위

2026-10-16 00:51:58의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
