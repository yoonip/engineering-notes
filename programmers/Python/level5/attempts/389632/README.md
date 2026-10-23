# 문자열과 알파벳과 쿼리: Python 시간 초과 기록

[Level 5 목록 / Level 5 index](../../README.md) · [풀이 전체 목차 / Solution index](../../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389632) · Level 5 · 미완료

## 결과부터 보기

Python으로 네 가지 구현을 시도했습니다. 저장된 사이트 결과는 v1과 v4 모두 15점이며, v4도 전체 통과하지 못했습니다. 정답 코드 목록에는 넣지 않았습니다.

| 저장된 제출 | 통과 | 시간 초과 | 점수 |
|---|---:|---:|---:|
| [v1](solution_v1.py) | 46/62 | 16/62 | 15/100 |
| [v4](solution_v4.py) | 58/62 | 4/62 | 15/100 |

v4의 시간 초과는 테스트 49·51·54·58입니다. 통과한 테스트 60도 9,452.85ms가 걸렸습니다. [저장된 채점 결과](saved_grading.json)에는 각 테스트의 결과를 남겼습니다. v2·v3의 별도 사이트 채점 결과는 보관돼 있지 않아 제출 점수를 추정하지 않습니다.

점수는 통과한 테스트 수에 비례하지 않습니다. 이 문제는 한 그룹의 테스트를 모두 통과해야 그 그룹의 점수를 받습니다. 배점은 작은 입력 세 그룹에 4·4·7점, 4번 쿼리가 없는 그룹에 35점, 추가 제한이 없는 그룹에 50점입니다. 따라서 58개가 통과해도 큰 두 그룹에 시간 초과가 남으면 점수는 15점에 머무를 수 있습니다.

## 문제 개요

문자에는 초기 위치를 기준으로 고유 번호가 있습니다. 현재 같은 문자열에 있는지 묻거나, 특정 알파벳을 새 문자열로 분리하거나, 번호 구간의 문자를 모으거나, 두 문자열을 합칩니다. 마지막에 각 문자열의 알파벳별 개수를 생성 순서대로 출력합니다. 문자열 길이는 최대 100,000, 쿼리는 최대 200,000입니다.

예를 들어 `s="aba"`에서 `2 1 a`를 처리하면 a 두 개가 새 문자열로 옮겨져 `{2}`와 `{1,3}`이 남습니다. `1 1 2`는 `NO`입니다. 이어 `4 1 2`로 합치면 먼저 생성된 문자열 하나로 돌아가고 마지막 출력은 `a 2 b 1`입니다.

## 구현을 바꾼 이유와 남은 병목

| 버전 | 저장 방식 | 바꾼 부분 | 남은 비용 |
|---|---|---|---|
| [v1](solution_v1.py) | 알파벳별 위치 목록·구간 트리·서로소 집합 | 같은 소속 구간에는 버킷 번호 하나를 저장 | 소속이 섞인 구간은 재귀로 내려가며 기존 소속의 개수를 차감 |
| [v2](solution_v2.py) | v1 + 작은 구간의 연속 구간 목록 | 64개 이하 구간에서 재귀 대신 경계 목록을 처리 | 목록 자르기·이어 붙이기, 사전 조회와 소속별 개수 갱신 |
| [v3](solution_v3.py) | 큰 정수 비트 집합 | 문자 소속 번호를 비트 평면으로 나눠 일괄 변경 | 한 비트 연산이 문자열 전체 길이에 비례하는 여러 정수 자릿수를 처리 |
| [v4](solution_v4.py) | 18개 비트 평면과 사전 계산 | 비트별 반복문 일부를 펼치고 알파벳 6개씩의 합집합을 미리 계산 | 큰 정수 연산량은 유지되고 사전 계산 비용도 추가 |

구간 트리는 구간 질의에 흔히 쓰지만, v1의 `assign`은 섞인 노드를 통째로 갱신하지 못합니다. 이전 그룹들의 문자 수를 각각 빼야 하므로 자식으로 내려갑니다. 따라서 이 함수의 모든 호출을 단순히 `O(log N)`이라고 계산하면 실제 작업량을 놓칩니다. 이것만으로 전체 쿼리의 누적 비용이 항상 `O(NQ)`라고 단정할 수도 없습니다. 구간이 만들어지고 합쳐지는 횟수에 대한 별도 분석이 필요합니다.

v3·v4는 문자 하나씩 이동하는 반복을 큰 정수의 `&`, `|`, `^`로 바꿨습니다. 하지만 Python 정수는 크기가 늘어나는 자료형입니다. 이 실행 환경에서는 정수 한 자릿수가 30비트이므로 100,000비트짜리 마스크는 약 3,334자릿수를 가집니다. 이 크기의 교집합·합집합·반전은 상수 시간 한 번으로 끝나지 않습니다. `plane >> index`도 이동한 정수를 만들기 때문에 단일 배열 원소를 읽는 것과 비용이 다릅니다.

`B=ceil(N/30)`, 소속 번호의 비트 수를 `K`라 두면, 비트 평면 K개를 순회하는 주요 쿼리의 큰 정수 연산은 최악에 `O(KB)` 규모입니다. 알파벳 선택 마스크 구성 비용도 별도로 듭니다. 최대 입력에서는 K가 18까지 필요하고 쿼리가 200,000개입니다. Python 반복문 일부를 없애도 이 큰 정수 처리량은 줄지 않습니다. 마지막 집계 또한 N개 위치마다 K개 평면을 읽으므로 Python 수준에서 `O(NK)` 작업을 합니다.

v4는 실제 쿼리 수와 관계없이 `2^18=262,144`개의 비트 변경 목록도 만듭니다. 이 튜플들에는 합계 2,359,296개의 원소 자리가 생깁니다. 6개 알파벳 묶음 표와 LRU 캐시도 넓은 마스크를 보관합니다. 이 비용 때문에 v4가 v3보다 항상 빠른 것은 아닙니다.

이 비용 분석은 코드와 로컬 측정에서 확인한 병목 설명입니다. 비공개 테스트 입력과 채점 서버 프로파일은 없으므로, 실패한 네 테스트가 각각 어떤 쿼리 분포였는지는 알 수 없습니다.

## Python 코드끼리 비교한 결과

이전에 저장한 [비교 1](python_comparison.json)·[비교 2](python_comparison_v4.json)의 결과는 다음과 같습니다. 초 단위의 로컬 측정이며 사이트 제한 시간과 직접 비교하지 않습니다. 당시 입력 생성 코드가 함께 남아 있지 않아 이 표는 보관된 측정 기록으로만 취급합니다.

| 입력 | v1 | v2 | v3 | v4 |
|---|---:|---:|---:|---:|
| 문자 100,000개·임의 알파벳 구간 20,001쿼리 | 8.004 | 5.245 | 0.501 | — |
| 문자 100,000개·분리/병합 30,001쿼리 | 4.370 | 3.178 | 1.313 | — |
| 임의 구간 100,000쿼리 | — | — | 2.360 | 2.439 |
| 혼합 90,000쿼리 | — | — | 4.105 | 4.276 |

이번에는 [재실행 가능한 비교 코드](verify_attempts.py)도 남겼습니다. 작은 생성 입력 24개에서 네 버전을 문자별 단순 구현과 비교했고 결과가 같았습니다. 문자 29,978개·구간 이동 6,001쿼리에서는 v1 0.9339초, v2 0.7140초, v3 0.0977초, v4 0.1395초였습니다. 시간 측정과 별도로 프로파일링한 v1은 `assign`을 3,546,124회, `find`를 1,441,603회 호출했습니다. 작은 쿼리 수에도 Python 함수 호출이 빠르게 늘어난다는 근거입니다.

```bash
python programmers/Python/level5/attempts/389632/verify_attempts.py
```

[실행 환경·고정 시드·측정 결과](local_comparison.json)를 함께 보관했습니다. 이 비교는 검사한 입력에서 출력이 같았다는 뜻이며 전체 정답성이나 사이트 통과를 뜻하지 않습니다. 재실행 시간은 컴퓨터와 실행 상태에 따라 달라집니다.

## 다음에 다시 풀 때 확인할 것

1. 각 쿼리의 처리 횟수를 세고, 소속이 잘게 나뉘었다 합쳐지는 입력에서도 누적 작업량을 제한할 수 있는지 확인합니다.
2. 전체 N비트 마스크를 매번 처리하는 대신 실제로 바뀌는 구간이나 블록만 갱신할 수 있는지 검토합니다. 병합 뒤에도 소속·생성 순서·알파벳 개수가 맞아야 합니다.
3. 마지막 출력은 한 번만 있으므로 중간 쿼리에 필요하지 않은 집계는 끝으로 미룰 수 있는지 살핍니다.
4. 더 빠른 Python 구현을 만들면 위 단순 구현과 대조한 뒤 최대 크기 입력과 사이트 채점을 다시 확인합니다.

아직 새 구현을 만들거나 통과를 확인한 상태는 아닙니다. 현재 파일은 다음 시도를 위한 미완료 기록입니다.

## English

Four Python implementations are archived. The saved judge results are 15/100 for both v1 and v4: v1 passed 46 of 62 tests and timed out on 16; v4 passed 58 and timed out on tests 49, 51, 54 and 58. Test 60 passed in 9,452.85ms. Separate judge records for v2 and v3 are unavailable. The problem awards points only for complete groups: 4, 4 and 7 points for smaller bounds, 35 points without merge queries, and 50 points without extra restrictions. More individual passes can therefore leave the score at 15.

Characters retain their original position IDs. Queries compare membership, extract letters from one group, gather letters within an ID interval, merge into the older group, and finally report letter counts in creation order. Bounds are 100,000 characters and 200,000 queries. With `aba`, extracting `a` from the initial group separates IDs `{1,3}` from `{2}`; IDs 1 and 2 then differ. Merging them restores the final report `a 2 b 1`.

v1 stores per-letter position lists, segment trees and disjoint-set buckets. A mixed node cannot be assigned in one step because counts must be deducted from its previous owners. Assuming every `assign` call costs `O(log N)` misses this traversal. A tight bound across all updates requires a separate amortized argument. v2 uses run boundaries inside blocks of at most 64 positions, reducing some recursion while retaining list-copying and bookkeeping costs.

v3 stores group IDs across integer bit planes. It replaces per-character moves with bitwise operations, but a Python integer operation is not constant-time at arbitrary width. In this environment each digit holds 30 bits, so a 100,000-bit mask spans about 3,334 digits. With `B=ceil(N/30)` and K ID bits, a query that scans the planes can require `O(KB)` digit work, plus letter-mask construction. Right shifts also create integer results. Final reporting reads K planes per character, taking `O(NK)` Python-level work.

v4 unrolls some loops, precomputes six-letter unions and fixes K at 18. The full-width integer work remains. Its 262,144 precomputed flip tuples contain 2,359,296 element slots, and union tables and caches retain additional masks. It is consequently not always faster than v3. Saved local timings show v3/v4 at 2.360/2.439 seconds for 100,000 random-range queries and 4.105/4.276 seconds for 90,000 mixed queries. Older benchmark generators are not preserved, so those figures are historical records rather than reproducible fixtures.

The included comparison script adds 24 fixed-seed small cases against a direct per-character reference. All four versions matched. On 29,978 characters and 6,001 range queries, this run measured v1/v2/v3/v4 at 0.9339/0.7140/0.0977/0.1395 seconds. A separate v1 profile counted 3,546,124 `assign` calls and 1,441,603 `find` calls. Environment and seeds are recorded in [local_comparison.json](local_comparison.json). These are local observations, not a replay of hidden judge cases or proof of correctness.

A future Python attempt should establish bounds on repeated fragmentation and merging, investigate updates limited to changed blocks or intervals, and defer counts needed only by the final report. It must retain creation order and ownership semantics, pass reference comparisons and maximum-size checks, and then pass the website judge. No such accepted replacement is claimed here.
