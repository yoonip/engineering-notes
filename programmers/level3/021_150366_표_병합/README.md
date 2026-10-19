# 표 병합

Level 3 · [150366 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/150366)

## 문제와 조건

50×50 표의 값 갱신·병합·병합 해제·출력을 명령 순서대로 처리합니다. 병합된 셀은 한 값을 공유합니다.

값은 소문자·숫자 문자열입니다. UPDATE 두 종류, MERGE, UNMERGE, PRINT를 처리하며 PRINT가 한 번 이상 있습니다.

`1≤Q≤1,000; 1≤r,c≤50; 1≤len(value)≤10`

## 풀이를 따라가기

1. 2500칸뿐이므로 각 셀에 그룹 번호를 직접 저장하고 병합·해제 때 전체를 순회합니다. 값은 그룹 대표 한 곳에만 둡니다.
2. MERGE는 첫 셀 값이 있으면 우선합니다. UNMERGE는 모든 소속 셀을 초기화한 후 지정 셀 하나만 값을 남깁니다. 명령 Q개에 대해 시간 O(2500Q), 공간 O(2500+출력 수).
3. 예: a와 b가 있는 두 셀을 첫 셀 우선으로 병합하면 모두 a. 둘째 셀에서 해제하면 첫 셀은 EMPTY, 둘째 셀만 a입니다.

## 왜 이 방법으로 풀 수 있나

2500칸뿐이므로 각 셀에 그룹 번호를 직접 저장하고 병합·해제 때 전체를 순회합니다. 값은 그룹 대표 한 곳에만 둡니다.

시간·공간: 시간 O(2500Q), 공간 O(2500+출력 수).

## 다른 방법과 비교

대표 번호 전체 배열을 훑는 대신 그룹마다 셀 집합을 유지합니다. 병합과 해제는 실제 구성원만 방문하지만 집합 자료구조가 추가로 필요합니다.

| 항목 | 기본 풀이 | 그룹별 구성원 집합 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(2500Q), 공간 O(2500+출력 수). | 최악 O(2500Q), 공간 O(2500+출력) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[["UPDATE 1 1 menu", "UPDATE 1 2 category", "UPDATE 2 1 bibimbap", "UPDATE 2 2 korean", "UPDATE 2 3 rice", "UPDATE 3 1 ramyeon", "UPDATE 3 2 korean", "UPDATE 3 3 noodle", "UPDATE 3 4 instant", "UPDATE 4 1 pasta", "UPDATE 4 2 italian", "UPDATE 4 3 noodle", "MERGE 1 2 1 3", "MERGE 1 3 1 4", "UPDATE korean hansik", "UPDATE 1 3 group", "UNMERGE 1 4", "PRINT 1 3", "PRINT 1 4"]]` | `["EMPTY", "group"]` |
| `[["UPDATE 1 1 a", "UPDATE 1 2 b", "UPDATE 2 1 c", "UPDATE 2 2 d", "MERGE 1 1 1 2", "MERGE 2 2 2 1", "MERGE 2 1 1 1", "PRINT 1 1", "UNMERGE 2 2", "PRINT 1 1"]]` | `["d", "EMPTY"]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Process update, merge, unmerge and print commands on a 50×50 table; merged cells share one value.

Values contain lowercase letters and digits. Process both UPDATE forms, MERGE, UNMERGE, and at least one PRINT.

`1≤Q≤1,000; 1≤r,c≤50; 1≤len(value)≤10`

### Method and correctness

Represent every cell by a group identifier and keep one value per group. Merge redirects all members of the second group and preserves the first cell’s value when present. Unmerge first collects all members, resets them to singleton groups, then restores the old group value only at the requested cell. Collecting members before resetting prevents partial unmerge mistakes.

Main complexity: O(2500Q) time, O(2500+output) space.

### Alternative and trade-offs

Store a member set for each group. Merge and unmerge visit actual members rather than scanning the full board, at the cost of set bookkeeping.

Code: [alternative.py](alternative.py).

Complexity: worst case O(2500Q), space O(2500+output).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 표 병합](https://school.programmers.co.kr/learn/courses/30/lessons/150366) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 13개 입력에서 26회 검사를 통과했습니다.

Passed 26 implementation checks across 13 official, boundary and fixed-seed differential inputs.
