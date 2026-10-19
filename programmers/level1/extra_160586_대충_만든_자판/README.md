# 대충 만든 자판

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/160586) · Level 1 · Python3

유형: 해시 · 최솟값 집계

## 풀이 원리

모든 자판을 훑어 각 문자를 누르는 최소 횟수를 저장한다. 목표 문자열에서는 문자별 최소 횟수를 더한다. 한 문자라도 자판에 없으면 그 목표는 만들 수 없어 -1을 넣는다. 각 문자를 입력하는 선택이 독립적이라 최소 횟수의 합이 전체 최솟값이다.

자판 문자 수 K, 목표 문자 수 T: 평균 시간 O(K+T), 공간 O(서로 다른 문자 수+목표 수).

## 공식 예제

입력 인수: `[["ABACD", "BCEFD"], ["ABCD", "AABB"]]`

반환값: `[9, 4]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(keymap, targets):
    min_press = {}
    for keys in keymap:
        for i, ch in enumerate(keys):
            count = i + 1
            if ch not in min_press or count < min_press[ch]:
                min_press[ch] = count
    answer = []
    for target in targets:
        total = 0
        for ch in target:
            if ch not in min_press:
                total = -1
                break
            total += min_press[ch]
        answer.append(total)
    return answer

# 전체 코드 줄별 설명
# def solution(keymap, targets):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 함수 정의, 자판 배열과 목표 문자열 배열을 입력받음
#     min_press = {}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 각 문자의 최소 입력 횟수를 저장할 딕셔너리 생성
#     for keys in keymap:  # for·in은 원소를 차례로 꺼내는 반복문. 여러 자판 중 하나를 꺼내 반복
#         for i, ch in enumerate(keys):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 자판의 문자와 인덱스를 함께 가져옴
#             count = i + 1  # =는 값 저장. 인덱스는 0부터 시작하므로 1을 더해 입력 횟수 계산
#             if ch not in min_press or count < min_press[ch]:  # if는 조건이 참일 때 실행. not in은 포함되지 않음. or는 한 조건 이상 참. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. <는 작음 비교. 처음 등장하거나 기존보다 적은 횟수라면
#                 min_press[ch] = count  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 해당 문자의 최소 입력 횟수를 갱신
#     answer = []  # []는 리스트. =는 값 저장. 각 목표 문자열의 결과를 저장할 리스트
#     for target in targets:  # for·in은 원소를 차례로 꺼내는 반복문. 목표 문자열을 하나씩 확인
#         total = 0  # =는 값 저장. 현재 목표 문자열의 총 입력 횟수를 0으로 초기화
#         for ch in target:  # for·in은 원소를 차례로 꺼내는 반복문. 목표 문자열의 문자를 하나씩 확인
#             if ch not in min_press:  # if는 조건이 참일 때 실행. not in은 포함되지 않음. 자판에 존재하지 않는 문자라면
#                 total = -1  # =는 값 저장. 입력할 수 없으므로 -1 저장
#                 break  # break는 가장 가까운 반복문 종료. 현재 목표 문자열에 대한 반복문 종료
#             total += min_press[ch]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 해당 문자의 최소 입력 횟수를 총합에 더함
#         answer.append(total)  # append는 리스트 끝에 추가. 현재 목표 문자열의 결과를 리스트에 추가
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 목표 문자열의 결과 반환

# 풀이 요약
# 모든 자판을 훑어 각 문자를 누르는 최소 횟수를 저장한다. 목표 문자열에서는 문자별 최소 횟수를 더한다. 한 문자라도 자판에 없으면 그 목표는 만들 수 없어 -1을 넣는다. 각 문자를 입력하는 선택이 독립적이라 최소 횟수의 합이 전체 최솟값이다.
# 자판 문자 수 K, 목표 문자 수 T: 평균 시간 O(K+T), 공간 O(서로 다른 문자 수+목표 수).
```

## 확인한 범위

2026-10-16 00:18:08의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
