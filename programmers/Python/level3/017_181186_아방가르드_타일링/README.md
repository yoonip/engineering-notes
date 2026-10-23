# 아방가르드 타일링

Level 3 · [181186 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/181186)

## 문제와 조건

회전 가능한 I·L 트리오미노로 3×n 판을 빈틈·겹침 없이 채우는 방법 수를 구합니다.

`1≤n≤100,000; modulus=1,000,000,007`

## 풀이를 따라가기

1. 높이 3의 I·L 트리오미노 타일링을 폭별 DP로 셉니다. 세로로 더 나눌 수 없는 끝 묶음은 폭 1·2·3에서 1·2·5가지, 이후 2·2·4가 3칸 주기로 반복됩니다.
2. 이 주기 누적식에서 3칸 전 식을 빼면 D[w]=D[w-1]+2D[w-2]+6D[w-3]+D[w-4]-D[w-6]으로 정리됩니다. 폭 0·1·2·3은 1·1·3·10으로 따로 시작합니다. 시간·공간 O(N).
3. 예: 폭 4는 10+2×3+6×1+1=23. 폭 6부터 여섯 칸 전 항을 빼 중복 누적을 보정합니다.

## 왜 이 방법으로 풀 수 있나

높이 3의 I·L 트리오미노 타일링을 폭별 DP로 셉니다. 세로로 더 나눌 수 없는 끝 묶음은 폭 1·2·3에서 1·2·5가지, 이후 2·2·4가 3칸 주기로 반복됩니다.

시간·공간: 시간·공간 O(N).

## 다른 방법과 비교

처음 세로로 끊을 수 있는 블록의 폭을 모두 합산합니다. 폭 1·2·3의 개수는 1·2·5, 그 뒤는 폭이 3의 배수이면 4, 아니면 2입니다. 압축 점화식을 쓰지 않아 작은 폭 검증에 적합합니다.

| 항목 | 기본 풀이 | 첫 분리 블록 누적 DP |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(N). | O(n²), 공간 O(n), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[2]` | `3` |
| `[3]` | `10` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count tilings of a 3×n board using rotatable straight and L-shaped triominoes, without gaps or overlaps.

`1≤n≤100,000; modulus=1,000,000,007`

### Method and correctness

Use width DP with D[0..3]=[1,1,3,10]. Indecomposable end blocks have counts 1,2,5 for widths 1,2,3, then repeat 2,2,4. Subtracting the recurrence three widths earlier yields D[w]=D[w−1]+2D[w−2]+6D[w−3]+D[w−4]−D[w−6], with the last term absent below width six. Reduce each result modulo 1,000,000,007.

Main complexity: O(n) time and space.

### Alternative and trade-offs

Sum over the width of the first indecomposable block: counts are 1, 2, 5 for widths 1–3, then 4 for multiples of 3 and 2 otherwise. This uncompressed recurrence checks the faster recurrence on small widths.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(n²), space O(n), small-input checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 아방가르드 타일링](https://school.programmers.co.kr/learn/courses/30/lessons/181186) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
