# 표 편집

Level 3 · [81303 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/81303)

## 문제와 조건

행 선택 이동, 현재 행 삭제, 최근 삭제 복구를 수행한 뒤 원래 각 행의 생존 여부를 문자열로 반환합니다.

모든 이동·복구는 유효하고 마지막 행까지 모두 지우는 명령은 없습니다. 결과는 원래 행 순서의 O·X입니다.

`5≤n≤1,000,000; 0≤k<n; 1≤Q≤200,000; 1≤X≤300,000; ΣX≤1,000,000`

## 풀이를 따라가기

1. 배열 두 개로 양방향 연결 리스트를 만든다. 삭제·복구는 양옆 연결만 바꾸고, 복구 정보는 후입선출 스택에 보관한다.
2. 예: 3↔4↔5에서 4를 삭제하면 3↔5. 복구할 때 저장한 (4,3,5)로 3↔4↔5를 되살린다.
3. 시간 O(N + 명령 수 + 총 이동 칸 수), 공간 O(N + 삭제 수). 총 이동은 최대 100만이라 한 칸씩 이동해도 된다.

## 왜 이 방법으로 풀 수 있나

배열 두 개로 양방향 연결 리스트를 만든다. 삭제·복구는 양옆 연결만 바꾸고, 복구 정보는 후입선출 스택에 보관한다.

시간·공간: 시간 O(N + 명령 수 + 총 이동 칸 수), 공간 O(N + 삭제 수). 총 이동은 최대 100만이라 한 칸씩 이동해도 된다.

## 다른 방법과 비교

살아 있는 행은 1, 삭제된 행은 0으로 두고 누적 개수를 관리합니다. 위·아래 이동을 현재 순위의 덧셈으로 바꾸고 해당 순위의 원래 행을 찾습니다.

| 항목 | 기본 풀이 | Fenwick tree 순위 선택 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N + 명령 수 + 총 이동 칸 수), 공간 O(N + 삭제 수). 총 이동은 최대 100만이라 한 칸씩 이동해도 된다. | O(n+Q log n), 공간 O(n) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[8, 2, ["D 2", "C", "U 3", "C", "D 4", "C", "U 2", "Z", "Z"]]` | `"OOOOXOOO"` |
| `[8, 2, ["D 2", "C", "U 3", "C", "D 4", "C", "U 2", "Z", "Z", "U 1", "C"]]` | `"OOXOXOOO"` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Simulate cursor moves, row deletion and undo; return original-row survival as an O/X string.

Moves and undo operations are valid, and at least one row always remains. Output O/X in original row order.

`5≤n≤1,000,000; 0≤k<n; 1≤Q≤200,000; 1≤X≤300,000; ΣX≤1,000,000`

### Method and correctness

Use previous and following arrays as a doubly linked list. Movement follows live neighbors. Deletion rewires the two neighbors and pushes the removed row plus its old neighbors onto a stack. Undo is last-in-first-out, making those neighbor links valid when the row is restored. Output original row order rather than current list order.

Main complexity: O(n+Q+sum of movement distances) time, O(n+Q) space.

### Alternative and trade-offs

Store live rows as ones in a Fenwick tree. Movement changes the current live rank, and order-statistic search converts that rank back to an original row index.

Code: [alternative.py](alternative.py).

Complexity: O(n+Q log n), space O(n).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 표 편집](https://school.programmers.co.kr/learn/courses/30/lessons/81303) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
