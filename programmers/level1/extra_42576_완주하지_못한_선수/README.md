# 완주하지 못한 선수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/42576) · Level 1 · Python3

유형: 정렬 · 동명이인 처리

## 풀이 원리

실제로 호출되는 마지막 solution은 참가자와 완주자를 각각 정렬한다. 처음으로 같은 위치의 이름이 다르면 참가자 쪽 이름이 미완주자다. 앞부분이 모두 같으면 마지막 참가자가 답이다. 동명이인도 같은 이름이 여러 번 정렬되므로 횟수가 보존된다.

참가자 N명: 최종 함수 시간 O(N log N), Python 정렬 보조 공간 상한 O(N). 두 입력 리스트를 바꾼다.

## 공식 예제

입력 인수: `[["leo", "kiki", "eden"], ["eden", "kiki"]]`

반환값: `"leo"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

원본에는 `solution`이 4번 정의돼 있다. Python은 나중에 나온 같은 이름의 정의를 사용하므로 마지막 함수가 실제로 호출된다. 위 실행 부분도 원본의 정의 순서를 유지했다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
from collections import Counter

def solution(participant, completion):
    p_counter = Counter(participant)
    c_counter = Counter(completion)
    result = p_counter - c_counter
    answer = list(result.keys())[0]
    return answer
from collections import Counter

def solution(participant, completion):
    p_counter = Counter(participant)
    c_counter = Counter(completion)
    result = p_counter - c_counter
    for name in result:
        return name

def solution(participant, completion):
    counts = {}
    for name in participant:
        if name in counts:
            counts[name] = counts[name] + 1
        else:
            counts[name] = 1
    for name in completion:
        counts[name] = counts[name] - 1
    for name in counts:
        if counts[name] > 0:
            return name

def solution(participant, completion):
    participant.sort()
    completion.sort()
    for i in range(len(completion)):
        if participant[i] != completion[i]:
            return participant[i]
    return participant[-1]

# 전체 코드 줄별 설명
# from collections import Counter  # from collections import는 collections 모듈에서 이름을 가져옴. Counter는 원소별 등장 횟수를 세는 딕셔너리형 자료구조. collections 모듈에서 원소별 개수를 세는 Counter 클래스를 가져옴
# 
# def solution(participant, completion):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 참가자 목록과 완주자 목록을 입력받는 함수
#     p_counter = Counter(participant)  # Counter는 원소별 횟수 집계. =는 값 저장. 참가자들의 이름별 등장 횟수를 계산
#     c_counter = Counter(completion)  # Counter는 원소별 횟수 집계. =는 값 저장. 완주자들의 이름별 등장 횟수를 계산
#     result = p_counter - c_counter  # =는 값 저장. 참가자 수에서 완주자 수를 빼서 완주하지 못한 선수만 남김
#     answer = list(result.keys())[0]  # list는 순서 있는 리스트로 변환. keys는 딕셔너리의 키들. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 남은 선수의 이름을 리스트로 변환하고 첫 번째 값을 가져옴
#     return answer  # return은 결과를 돌려주고 함수 종료. 완주하지 못한 선수의 이름을 문자열로 반환
# from collections import Counter  # from collections import는 collections 모듈에서 이름을 가져옴. Counter는 원소별 등장 횟수를 세는 딕셔너리형 자료구조. collections 모듈에서 원소별 개수를 세는 Counter 클래스를 가져옴
# 
# def solution(participant, completion):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 참가자 목록과 완주자 목록을 입력받는 함수
#     p_counter = Counter(participant)  # Counter는 원소별 횟수 집계. =는 값 저장. 참가자들의 이름별 등장 횟수를 계산
#     c_counter = Counter(completion)  # Counter는 원소별 횟수 집계. =는 값 저장. 완주자들의 이름별 등장 횟수를 계산
#     result = p_counter - c_counter  # =는 값 저장. 참가자 수에서 완주자 수를 빼서 완주하지 못한 선수만 남김
#     for name in result:  # for·in은 원소를 차례로 꺼내는 반복문. 차이 Counter에 남은 이름을 순회.
#         return name  # return은 결과를 돌려주고 함수 종료. 완주하지 못한 이름을 반환.
# 
# def solution(participant, completion):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 참가자 목록과 완주자 목록을 입력받는 함수
#     counts = {}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 이름별 참가 횟수 딕셔너리.
#     for name in participant:  # for·in은 원소를 차례로 꺼내는 반복문. 참가자 이름들을 셈.
#         if name in counts:  # if는 조건이 참일 때 실행. in은 포함 여부. 이 이름을 전에 센 적 있는지 확인.
#             counts[name] = counts[name] + 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 동명이인 참가 횟수 증가.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 처음 나온 이름인 경우.
#             counts[name] = 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 첫 참가 횟수 1을 저장.
#     for name in completion:  # for·in은 원소를 차례로 꺼내는 반복문. 완주한 이름들을 확인.
#         counts[name] = counts[name] - 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 해당 이름의 남은 참가 횟수를 하나 줄임.
#     for name in counts:  # for·in은 원소를 차례로 꺼내는 반복문. 모든 이름의 남은 횟수를 검사.
#         if counts[name] > 0:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >는 큼 비교. 완주 기록에서 지워지지 않은 참가자가 있는지 확인.
#             return name  # return은 결과를 돌려주고 함수 종료. 미완주자 이름 반환.
# 
# def solution(participant, completion):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 참가자 목록과 완주자 목록을 입력받는 함수
#     participant.sort()  # sort는 원래 리스트 정렬. 참가자를 이름순으로 제자리 정렬.
#     completion.sort()  # sort는 원래 리스트 정렬. 완주자도 같은 기준으로 정렬.
#     for i in range(len(completion)):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 완주자 수만큼 두 목록을 같은 위치에서 비교.
#         if participant[i] != completion[i]:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. !=는 다름 비교. 같은 순서에서 이름이 달라지는지 확인.
#             return participant[i]  # return은 결과를 돌려주고 함수 종료. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 참가자 쪽의 현재 이름이 미완주자.
#     return participant[-1]  # return은 결과를 돌려주고 함수 종료. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 앞부분이 모두 같으면 마지막 참가자가 미완주자.

# 풀이 요약
# 실제로 호출되는 마지막 solution은 참가자와 완주자를 각각 정렬한다. 처음으로 같은 위치의 이름이 다르면 참가자 쪽 이름이 미완주자다. 앞부분이 모두 같으면 마지막 참가자가 답이다. 동명이인도 같은 이름이 여러 번 정렬되므로 횟수가 보존된다.
# 참가자 N명: 최종 함수 시간 O(N log N), Python 정렬 보조 공간 상한 O(N). 두 입력 리스트를 바꾼다.
```

## 확인한 범위

2026-10-16 18:01:57의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
