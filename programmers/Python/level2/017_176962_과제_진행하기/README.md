# 과제 진행하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/176962) · Level 2 · Python3

새 과제가 시작되면 현재 과제를 멈추고, 빈 시간에는 가장 최근에 멈춘 과제를 이어 합니다.

## 조건과 입출력

입력 매개변수: `plans`. 반환값은 문자열 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 3 ≤ plans의 길이 ≤ 1,000
- 2 ≤ name의 길이 ≤ 10
- 1 ≤ playtime ≤ 100

## 풀이를 따라가기

시각을 분으로 바꾸고 시작순으로 정렬합니다. 두 시작 사이의 시간을 스택 꼭대기 과제에 씁니다. 남은 시간이 부족하면 잔여 시간을 갱신해 다시 넣습니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(plans):
    tasks = []
    for name, start, duration in plans:
        hour, minute = map(int, start.split(':'))
        tasks.append((hour * 60 + minute, name, int(duration)))
    tasks.sort()
    stack = []
    answer = []
    previous = 0
    for start, name, duration in tasks:
        free = start - previous
        # 다음 시작 전까지 가장 최근에 멈춘 과제부터 이어 한다.
        while free > 0 and stack:
            old_name, remaining = stack.pop()
            if remaining <= free:
                free -= remaining
                answer.append(old_name)
            else:
                # 끝내지 못한 작업의 남은 시간을 보존한다.
                stack.append((old_name, remaining - free))
                free = 0
        stack.append((name, duration))
        previous = start
    # 새 과제가 더 없으면 최근 중단 순서로 모두 끝낸다.
    while stack:
        answer.append(stack.pop()[0])
    return answer
```

## 정답이 되는 이유

스택의 역순이 바로 최근 중단 우선 규칙입니다. 각 시작 시각 전까지 가능한 일을 모두 처리한 다음 새 과제를 넣으므로 실제 완료 순서를 유지합니다.

시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N)

주의할 점: 다음 과제 시작과 동시에 끝나면 완료로 기록합니다. 마지막에는 스택을 거꾸로 비웁니다.

## 다른 방법: 분 단위 시간 시뮬레이션

```python
def solution(plans):
    tasks = []
    for name,start,duration in plans:
        h,m=map(int,start.split(':'))
        tasks.append((h*60+m,name,int(duration)))
    tasks.sort()
    now=tasks[0][0]
    index=0
    stack=[]
    answer=[]
    while index<len(tasks) or stack:
        while index<len(tasks) and tasks[index][0]==now:
            _,name,work=tasks[index]
            stack.append([name,work])
            index+=1
        if stack:
            stack[-1][1]-=1
            if stack[-1][1]==0:
                answer.append(stack.pop()[0])
        now+=1
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 시각을 분으로 바꾸고 시작순으로 정렬합니다. 두 시작 사이의 시간을 스택 꼭대기 과제에 씁니다. 남은 시간이 부족하면 잔여 시간을 갱신해 다시 넣습니다. | 분 단위 시간 시뮬레이션 |
| 비용 | 시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N) | 시간 O(정렬+총 수행 시간), 공간 O(N) / Time O(N log N + total work duration), space O(N) |

## 검증

공식 예제 3개와 생성 입력 40개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Pause the current task when a new one starts, then resume the most recently paused task during free time.

### Conditions and input/output

Input arguments: `plans`. The return value is a list of strings satisfying the task described below.

- 3 ≤ len(plans) ≤ 1000; unique task names, length 2 … 10
- 00:00 ≤ start ≤ 23:59; all starts distinct; duration 1 … 100 minutes
- input need not be sorted; completion exactly at another start counts as completed

### Approach

Convert times to minutes and sort starts. Spend the gap until each next start on the stack top; if the gap is insufficient, push back the remaining duration.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The stack implements last-paused-first-resumed ordering. Exhausting each time gap before pushing the new task preserves the actual completion order.

시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N)

Boundary cases: A task finishing exactly at the next start counts as completed. After the final start, drain the stack in reverse order.

### Alternative: Minute-by-minute simulation

시간 O(정렬+총 수행 시간), 공간 O(N) / Time O(N log N + total work duration), space O(N)

### Verification

Local checks covered 3 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 과제 진행하기](https://school.programmers.co.kr/learn/courses/30/lessons/176962) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
