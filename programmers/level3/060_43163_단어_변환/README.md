# 단어 변환

Level 3 · [43163 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/43163)

## 문제와 조건

begin을 target으로 한 글자씩 바꾸되 중간 단어는 words 안에 있어야 합니다. 최소 변환 횟수 또는 불가능한 경우 0을 반환합니다.

같은 길이 소문자 단어이고 목록에 중복이 없습니다. 목록의 단어로만 한 글자씩 바꾸며 불가능하면 0입니다.

`3≤word length≤10; 3≤W≤50; begin≠target`

## 풀이를 따라가기

1. 단어를 노드, 한 글자만 다른 단어 사이를 간선으로 보고 BFS합니다. 한 번 변환할 때마다 비용이 1이므로 최단 단계가 나옵니다.
2. 예: hit→hot→dot→dog→cog는 네 번 변환. 목표가 목록에 없거나 이어지는 길이 없으면 0입니다.
3. 단어 수 W≤50, 글자 수 L≤10. 시간 O(W²·L), 공간 O(W).

## 왜 이 방법으로 풀 수 있나

단어를 노드, 한 글자만 다른 단어 사이를 간선으로 보고 BFS합니다. 한 번 변환할 때마다 비용이 1이므로 최단 단계가 나옵니다.

시간·공간: 시간 O(W²·L), 공간 O(W).

## 다른 방법과 비교

한 글자를 별표로 바꾼 형태끼리 버킷을 만듭니다. 같은 버킷의 단어는 한 글자 변환으로 이어집니다. 단어 쌍을 매번 비교하는 대신 버킷을 재사용합니다.

| 항목 | 기본 풀이 | 와일드카드 버킷 BFS |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(W²·L), 공간 O(W). | O(WL²+W²L), 공간 O(WL²) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `["hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]]` | `4` |
| `["hit", "cog", ["hot", "dot", "dog", "lot", "log"]]` | `0` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Transform begin into target one character at a time using words, returning minimum steps or zero if impossible.

Words are equally sized lowercase strings without duplicates. Change one character at a time using listed words; return zero if impossible.

`3≤word length≤10; 3≤W≤50; begin≠target`

### Method and correctness

Model each word as a vertex and connect words differing at exactly one position. BFS finds the minimum number of transformations. A target absent from the allowed list is impossible. Mark words visited when enqueued to avoid duplicate expansion.

Main complexity: O(W²L) time, O(W) auxiliary space.

### Alternative and trade-offs

Group words by patterns with one character replaced by a wildcard. Words in a bucket differ in one position, avoiding repeated full pairwise comparisons.

Code: [alternative.py](alternative.py).

Complexity: O(WL²+W²L), space O(WL²).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 단어 변환](https://school.programmers.co.kr/learn/courses/30/lessons/43163) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
