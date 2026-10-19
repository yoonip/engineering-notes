# 실패율

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/42889) · Level 1 · Python3

유형: 집계 · 정렬

## 풀이 원리

스테이지별 멈춘 사용자 수를 세고, 아직 도달해 있는 사용자 수로 나눠 실패율을 구한다. 현재 스테이지의 실패율을 계산한 다음 그 인원을 분모에서 뺀다. 도달한 사용자가 없으면 0으로 둔다. 실패율 내림차순·번호 오름차순으로 정렬한다.

사용자 P명, 스테이지 N개: 시간 O(P+N log N), 공간 O(N).

## 공식 예제

입력 인수: `[5, [2, 1, 2, 6, 2, 4, 3, 3]]`

반환값: `[3, 4, 2, 1, 5]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(N, stages):
    counts = [0] * (N + 2)
    for stage in stages:
        counts[stage] += 1
    reached = len(stages)
    rates = []
    for stage in range(1, N + 1):
        if reached == 0:
            rate = 0
        else:
            rate = counts[stage] / reached
        rates.append((stage, rate))
        reached -= counts[stage]
    rates.sort(key=lambda item: (-item[1], item[0]))
    return [item[0] for item in rates]

# 전체 코드 줄별 설명
# def solution(N, stages):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 단계 수와 사용자별 현재 단계를 받습니다.
#     counts = [0] * (N + 2)  # []는 리스트. =는 값 저장. 0이 N+2개인 리스트입니다. 모든 단계를 통과한 N+1도 인덱스로 사용합니다.
#     for stage in stages:  # for·in은 원소를 차례로 꺼내는 반복문. 사용자들의 단계 번호를 하나씩 꺼냅니다.
#         counts[stage] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 해당 단계에 멈춘 사람 수를 1 늘립니다.
#     reached = len(stages)  # len은 길이. =는 값 저장. len()은 원소 수입니다. 처음에는 모든 사용자가 1단계에 도달했습니다.
#     rates = []  # []는 리스트. =는 값 저장. 단계 번호와 실패율을 담을 빈 리스트입니다.
#     for stage in range(1, N + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 1부터 N까지 처리합니다. range는 끝값을 제외하므로 +1합니다.
#         if reached == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. ==로 도달 인원이 0인지 비교합니다.
#             rate = 0  # =는 값 저장. 도달한 사람이 없으면 실패율은 0입니다. 0으로 나누는 오류도 방지합니다.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 도달 인원이 있으면 실행합니다.
#             rate = counts[stage] / reached  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. /는 소수 부분을 유지하는 나눗셈입니다.
#         rates.append((stage, rate))  # append는 리스트 끝에 추가. ()로 묶은 여러 값은 변경 불가 튜플. 두 값을 튜플로 묶어 리스트에 추가합니다. 예: (1, 0.125).
#         reached -= counts[stage]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. -=는 빼서 저장. 현재 단계에 멈춘 사람은 다음 단계에 도달하지 않았으므로 제외합니다.
#     rates.sort(key=lambda item: (-item[1], item[0]))  # sort는 원래 리스트 정렬. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ()로 묶은 여러 값은 변경 불가 튜플. =는 이름 붙인 인수에 값 지정. lambda는 이름 없는 짧은 함수, key는 정렬 기준. lambda는 짧은 함수입니다. 실패율 내림차순, 동점이면 번호 오름차순으로 정렬합니다.
#     return [item[0] for item in rates]  # return은 결과를 돌려주고 함수 종료. in은 포함 여부. []는 리스트. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 내포문은 반복하면서 원소를 구성. 리스트 컴프리헨션으로 정렬된 튜플에서 단계 번호만 꺼내 반환합니다.

# 풀이 요약
# 스테이지별 멈춘 사용자 수를 세고, 아직 도달해 있는 사용자 수로 나눠 실패율을 구한다. 현재 스테이지의 실패율을 계산한 다음 그 인원을 분모에서 뺀다. 도달한 사용자가 없으면 0으로 둔다. 실패율 내림차순·번호 오름차순으로 정렬한다.
# 사용자 P명, 스테이지 N개: 시간 O(P+N log N), 공간 O(N).
```

## 확인한 범위

2026-10-16 02:11:22의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
