# 택배상자

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131704) · Level 2 · Python3

주 컨베이어와 스택 보조 벨트로 원하는 순서대로 실을 수 있는 최대 상자 수를 구합니다.

## 조건과 입출력

입력 매개변수: `order`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ order의 길이 ≤ 1,000,000
- order는 1이상 order의 길이 이하의 모든 정수가 한번씩 등장합니다.

## 풀이를 따라가기

1번부터 들어오는 상자를 스택에 넣습니다. 맨 위가 지금 필요한 상자이면 꺼내 싣고 다음 주문을 봅니다. 마지막으로 실은 개수를 반환합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(order):
    stack = []
    answer = 0
    for box in range(1, len(order) + 1):
        stack.append(box)
        # 보조 벨트 맨 위가 필요한 상자이면 바로 싣는다.
        while stack and stack[-1] == order[answer]:
            stack.pop()
            answer += 1
    return answer
```

## 정답이 되는 이유

들어온 상자를 즉시 실을 수 없으면 보조 벨트에 두는 수밖에 없습니다. 꺼낼 수 있는 것은 꼭대기뿐이므로 필요한 상자를 가능한 순간에 꺼내는 과정이 유일한 진행을 따릅니다.

시간 O(N), 공간 O(N) / Time and space O(N)

주의할 점: 보조 벨트의 중간 상자를 꺼낼 수 없습니다. 각 상자는 한 번 들어가고 한 번만 나옵니다.

## 다른 방법: 요청 상자 기준의 역방향 시뮬레이션

```python
def solution(order):
    incoming=1
    waiting=[]
    loaded=0
    for target in order:
        while incoming<=target:
            waiting.append(incoming)
            incoming+=1
        if not waiting or waiting[-1]!=target: break
        waiting.pop()
        loaded+=1
    return loaded
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 1번부터 들어오는 상자를 스택에 넣습니다. 맨 위가 지금 필요한 상자이면 꺼내 싣고 다음 주문을 봅니다. 마지막으로 실은 개수를 반환합니다. | 요청 상자 기준의 역방향 시뮬레이션 |
| 비용 | 시간 O(N), 공간 O(N) / Time and space O(N) | 시간 O(N), 공간 O(N) / Time and space O(N) |

## 검증

공식 예제 2개와 생성 입력 70개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the longest loading prefix achievable with the main conveyor and a stack-like auxiliary belt.

### Conditions and input/output

Input arguments: `order`. The return value is an integer satisfying the task described below.

- 1 ≤ len(order) ≤ 1000000; order is a permutation of 1 … len(order)

### Approach

Push incoming boxes in numeric order. While the top matches the next requested box, pop and load it. Return the loaded count.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

An arriving box that cannot be loaded must wait on the auxiliary belt, whose top is the only removable box. Loading every available requested top follows the only feasible progress.

시간 O(N), 공간 O(N) / Time and space O(N)

Boundary cases: You cannot remove a middle box from the auxiliary belt. Each box is pushed and popped at most once.

### Alternative: Drive the simulation by requested box numbers

시간 O(N), 공간 O(N) / Time and space O(N)

### Verification

Local checks covered 2 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 택배상자](https://school.programmers.co.kr/learn/courses/30/lessons/131704) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
