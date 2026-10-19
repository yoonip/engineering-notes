# 덧칠하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/161989) · Level 1 · Python3

유형: 그리디 · 구간 덮기

## 풀이 원리

가장 왼쪽의 아직 안 칠한 구역을 포함하면서 오른쪽을 최대한 덮습니다. 끝을 넘는 롤러는 벽의 마지막 시작 위치로 옮깁니다. 이미 덮은 범위 안의 다음 구역은 건너뜁니다. 왼쪽 미처리 구역은 반드시 칠해야 하므로 이때 오른쪽을 넓게 덮는 선택이 불리하지 않습니다.

칠할 구역 수 K: 시간 O(K), 보조 공간 O(1).

## 공식 예제

입력 인수: `[8, 4, [2, 3, 6]]`

반환값: `2`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n, m, section):
    answer = 0
    painted_until = 0
    for position in section:
        if position > painted_until:
            answer += 1
            start = min(position, n - m + 1)
            painted_until = start + m - 1
    return answer

# 전체 코드 줄별 설명
# def solution(n, m, section):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. n: 벽 길이, m: 롤러 길이, section: 칠해야 하는 구역 번호 목록
#     answer = 0  # =는 값 저장. 롤러로 칠한 횟수. 아직 칠하지 않았으므로 0
#     painted_until = 0  # =는 값 저장. 마지막으로 칠한 구역 번호. 구역은 1번부터이므로 초기값은 0
#     for position in section:  # for·in은 원소를 차례로 꺼내는 반복문. 오름차순으로 주어진 구역 번호를 왼쪽부터 하나씩 확인
#         if position > painted_until:  # if는 조건이 참일 때 실행. >는 큼 비교. 이전에 칠한 범위보다 오른쪽이면 새로 칠해야 함
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 칠하는 횟수 증가. answer = answer + 1과 같은 의미
#             start = min(position, n - m + 1)  # min은 최솟값. =는 값 저장. 현재 구역에서 시작하되, 벽 끝을 넘으면 왼쪽으로 조정
#             painted_until = start + m - 1  # =는 값 저장. 시작 구역부터 m칸을 칠했을 때의 마지막 구역 번호
#     return answer  # return은 결과를 돌려주고 함수 종료. 필요한 구역을 모두 칠한 최소 횟수를 반환

# 풀이 요약
# 가장 왼쪽의 아직 안 칠한 구역을 포함하면서 오른쪽을 최대한 덮는다. 끝을 넘는 롤러는 벽의 마지막 시작 위치로 옮긴다. 이미 덮은 범위 안의 다음 구역은 건너뛴다. 왼쪽 미처리 구역은 반드시 칠해야 하므로 이때 오른쪽을 넓게 덮는 선택이 불리하지 않다.
# 칠할 구역 수 K: 시간 O(K), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 00:25:19의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
