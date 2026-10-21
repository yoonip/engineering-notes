# 베스트앨범

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [42579 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42579)

## 문제와 조건

총 재생 수가 큰 장르부터, 그 안에서는 재생 수가 큰 노래를 최대 두 곡씩 골라 고유번호를 반환합니다.

장르별 총 재생 수는 모두 다릅니다. 곡 재생 수가 같으면 작은 고유번호가 먼저입니다.

`1≤songs≤10,000; genres<100; at most 2 selected songs per genre`

## 풀이를 따라가기

1. 장르의 우선순위와 장르 안 노래의 우선순위를 따로 계산합니다. (-재생 수,고유 번호)로 정렬하면 두 노래 조건이 한 번에 적용됩니다.
2. 예: pop 총 3100회가 classic 1450회보다 앞서므로 pop의 4·1번, classic의 3·0번 순서가 됩니다.
3. 노래 N개일 때 시간 O(N log N), 공간 O(N). 장르에 한 곡만 있으면 슬라이스 결과도 한 곡입니다.

## 왜 이 방법으로 풀 수 있나

장르의 우선순위와 장르 안 노래의 우선순위를 따로 계산합니다. (-재생 수,고유 번호)로 정렬하면 두 노래 조건이 한 번에 적용됩니다.

시간·공간: 시간 O(N log N), 공간 O(N). 장르에 한 곡만 있으면 슬라이스 결과도 한 곡입니다.

## 다른 방법과 비교

장르별 전체 합과 곡 목록을 만든 후 nsmallest로 두 곡만 고릅니다. 장르 안 모든 곡을 정렬하는 대신 필요한 상위 항목만 추출합니다.

| 항목 | 기본 풀이 | 장르별 상위 2개 힙 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N log N), 공간 O(N). 장르에 한 곡만 있으면 슬라이스 결과도 한 곡입니다. | O(N+G log G), 공간 O(N) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[["classic", "pop", "classic", "classic", "pop"], [500, 600, 150, 800, 2500]]` | `[4, 1, 3, 0]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Select genres by total plays and at most two top songs per genre, returning their original IDs.

Genre totals are distinct; equal song play counts prefer the smaller original ID.

`1≤songs≤10,000; genres<100; at most 2 selected songs per genre`

### Method and correctness

Order genres by total plays. Inside each genre order songs by descending plays and ascending original index, selecting at most two. Genre totals are distinct in the supplied conditions, while song ties must use their smaller index.

Main complexity: O(N log N) time, O(N) space.

### Alternative and trade-offs

Aggregate genre totals, then use nsmallest to select only two songs per genre. This avoids fully sorting every genre’s songs.

Code: [alternative.py](alternative.py).

Complexity: O(N+G log G), space O(N).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 베스트앨범](https://school.programmers.co.kr/learn/courses/30/lessons/42579) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
