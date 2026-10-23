# 뒤에 있는 큰 수 찾기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/154539) · Level 2 · Python3

각 원소 오른쪽에서 처음 만나는 더 큰 수를 찾습니다.

## 조건과 입출력

입력 매개변수: `numbers`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 4 ≤ numbers의 길이 ≤ 1,000,000
- 1 ≤ numbers[i] ≤ 1,000,000

## 풀이를 따라가기

아직 답을 못 찾은 인덱스를 감소 스택에 둡니다. 새 값이 스택 끝의 값보다 크면 그 인덱스의 답을 새 값으로 정합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(numbers):
    answer = [-1] * len(numbers)
    stack = []
    for index, value in enumerate(numbers):
        # 지금 값이 처음 만난 더 큰 수인 미해결 인덱스를 꺼낸다.
        while stack and numbers[stack[-1]] < value:
            previous = stack.pop()
            answer[previous] = value
        # 현재 인덱스도 이후의 더 큰 수를 기다린다.
        stack.append(index)
    return answer
```

## 정답이 되는 이유

스택에 남은 원소는 지금까지 더 큰 오른쪽 값을 만나지 못했습니다. 처음 더 큰 값에서 바로 꺼내므로 가장 가까운 큰 값이 답입니다.

시간 O(N), 공간 O(N) / Time and space O(N)

주의할 점: 같은 값은 더 큰 수가 아닙니다. 끝까지 남은 인덱스의 답은 −1입니다.

## 다른 방법: 오른쪽부터 답 인덱스 건너뛰기

```python
def solution(numbers):
    n=len(numbers)
    following=[n]*n
    for i in range(n-1,-1,-1):
        j=i+1
        while j<n and numbers[j]<=numbers[i]:
            j=following[j]
        following[i]=j
    return [numbers[j] if j<n else -1 for j in following]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 아직 답을 못 찾은 인덱스를 감소 스택에 둡니다. 새 값이 스택 끝의 값보다 크면 그 인덱스의 답을 새 값으로 정합니다. | 오른쪽부터 답 인덱스 건너뛰기 |
| 비용 | 시간 O(N), 공간 O(N) / Time and space O(N) | 최악 시간 O(N²), 공간 O(N) / Worst-case time O(N²), space O(N); 스택 풀이가 선형 보장 / the stack guarantees linear time |

## 검증

공식 예제 2개와 생성 입력 100개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the first strictly greater value to the right of every element.

### Conditions and input/output

Input arguments: `numbers`. The return value is a numeric list satisfying the task described below.

- 4 ≤ len(numbers) ≤ 1000000; 1 ≤ numbers[i] ≤ 1000000

### Approach

Keep unresolved indices in a decreasing stack. When the new value exceeds the stack-top value, resolve that index with the new value.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Unresolved entries have encountered no greater value so far. Popping at the first greater value therefore returns the nearest greater element.

시간 O(N), 공간 O(N) / Time and space O(N)

Boundary cases: Equal values do not qualify. Any index left unresolved keeps −1.

### Alternative: Right-to-left jumping through next-greater links

최악 시간 O(N²), 공간 O(N) / Worst-case time O(N²), space O(N); 스택 풀이가 선형 보장 / the stack guarantees linear time

### Verification

Local checks covered 2 official examples and 100 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 뒤에 있는 큰 수 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/154539) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
