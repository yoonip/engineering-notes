# 달리기 경주

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/178871) · Level 1 · Python3

유형: 해시 · 배열 갱신

## 풀이 원리

선수 이름별 현재 배열 위치를 딕셔너리에 저장한다. 이름이 불리면 앞 선수와 배열 원소 두 개를 교환하고 두 사람의 위치 정보도 갱신한다. 매번 이름을 배열에서 다시 찾지 않아 호출 한 번을 평균 상수 시간에 처리한다.

선수 P명, 호출 C번: 평균 시간 O(P+C), 공간 O(P). 선수 리스트를 직접 바꾼다.

## 공식 예제

입력 인수: `[["mumu", "soe", "poe", "kai", "mine"], ["kai", "kai", "mine", "mine"]]`

반환값: `["mumu", "kai", "mine", "soe", "poe"]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(players, callings):
    position = {}
    for i, name in enumerate(players):
        position[name] = i
    for name in callings:
        i = position[name]
        front = players[i - 1]
        players[i - 1], players[i] = players[i], players[i - 1]
        position[name] = i - 1
        position[front] = i
    return players

# 전체 코드 줄별 설명
# def solution(players, callings):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 현재 선수 순서와 추월 호출을 입력받음.
#     position = {}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 선수 이름별 현재 위치를 저장할 딕셔너리.
#     for i, name in enumerate(players):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 선수의 위치와 이름을 함께 읽음.
#         position[name] = i  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 이름에 해당하는 현재 위치 저장.
#     for name in callings:  # for·in은 원소를 차례로 꺼내는 반복문. 추월하는 선수의 이름을 순서대로 확인.
#         i = position[name]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 추월할 선수의 현재 위치 조회.
#         front = players[i - 1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 바로 앞 선수의 이름을 보관.
#         players[i - 1], players[i] = players[i], players[i - 1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 두 선수의 배열 위치를 동시에 교환.
#         position[name] = i - 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 추월한 선수의 딕셔너리 위치 갱신.
#         position[front] = i  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 뒤로 밀린 선수의 위치도 갱신.
#     return players  # return은 결과를 돌려주고 함수 종료. 모든 추월 후 선수 순서 반환.

# 풀이 요약
# 선수 이름별 현재 배열 위치를 딕셔너리에 저장한다. 이름이 불리면 앞 선수와 배열 원소 두 개를 교환하고 두 사람의 위치 정보도 갱신한다. 매번 이름을 배열에서 다시 찾지 않아 호출 한 번을 평균 상수 시간에 처리한다.
# 선수 P명, 호출 C번: 평균 시간 O(P+C), 공간 O(P). 선수 리스트를 직접 바꾼다.
```

## 확인한 범위

2026-10-15 23:55:02의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
