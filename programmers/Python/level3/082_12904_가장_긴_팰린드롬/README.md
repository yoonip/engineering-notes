# 가장 긴 팰린드롬

Level 3 · [12904 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12904)

## 문제와 조건

문자열의 연속 구간 중 앞뒤로 읽어 같은 가장 긴 구간의 길이를 구합니다.

`1≤len(s)≤2,500; s∈[a-z]+`

## 풀이를 따라가기

1. 글자 사이에 #를 넣어 홀수·짝수 길이를 같은 형태로 다룹니다. 양끝 경계 문자 ^·$는 소문자 입력에 없으므로 비교를 멈추는 표지로 쓸 수 있습니다.
2. radius[i]는 변환 문자열의 i를 중심으로 양쪽에 같은 글자가 이어지는 반지름입니다. 이 반지름은 원래 문자열의 팰린드롬 길이와 같습니다.
3. 현재 위치가 이미 확인한 팰린드롬 안에 있으면 중심의 대칭 위치에서 알려진 반지름을 가져옵니다. 오른쪽 경계를 넘는 부분만 새로 비교합니다.
4. 더 멀리 뻗었으면 중심과 오른쪽 경계를 갱신합니다. 모든 중심의 반지름 중 최댓값이 답입니다.

## 왜 이 방법으로 풀 수 있나

대칭으로 복사한 구간은 이미 확인된 팰린드롬 안에 있으므로 다시 비교할 필요가 없습니다. 복사로 확정할 수 없는 비교는 오른쪽 경계를 늘리는 비교뿐이며 경계는 왼쪽으로 돌아가지 않습니다. 따라서 전체 확장 횟수는 문자열 길이에 비례합니다.

시간·공간: Manacher O(N) 시간·O(N) 공간

## 다른 방법과 비교

중심 확장은 각 글자와 글자 사이를 중심으로 직접 양쪽을 비교합니다. 구조가 단순하지만 반복 문자가 많으면 같은 쌍을 여러 번 비교합니다. 기본 코드는 Manacher로 선형 시간에 처리하고, 중심 확장 코드는 이해와 독립 비교에 사용합니다.

| 항목 | 기본 풀이 | 다른 방법 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | Manacher O(N) 시간·O(N) 공간 | 중심 확장 O(N²) 시간; 역순 확인을 포함한 최대 보조 공간 O(N) |

## 예제와 검증

[공식 예제 입력·결과](examples.json) · [고정 검증 입력](test_cases.json) · [실제 제출 원본](submitted_original.py)

저장된 제출본은 100점 채점을 받은 코드입니다. 현재 기본 구현은 효율을 높인 별도 구현이며, 공식 예제·경계 입력·독립 대안 비교를 합쳐 45개 입력에서 90회 로컬 검사를 통과했습니다.

```bash
python test_solution.py
```

## English

### Task and constraints

Find the longest contiguous substring that reads the same forwards and backwards.

`1≤len(s)≤2,500; s∈[a-z]+`

### Method

Insert # separators to unify odd and even lengths and use ^/$ boundary markers absent from lowercase input. For each center, its transformed radius equals the palindrome length in the original string. When the center lies inside the rightmost known palindrome, reuse the mirrored radius up to that boundary; compare only beyond the known region. Extend the center/right boundary when necessary and return the largest radius.

### Correctness and complexity

Mirrored comparisons lie inside an already verified palindrome. Any successful comparison beyond the mirrored bound advances the global right boundary, which never moves backwards. Thus the total number of new extensions is linear.

Main complexity: O(N) time and space.

### Alternative and trade-offs

Center expansion compares both sides of every character and every gap directly. It is simpler, but repeated characters cause repeated comparisons. The main Manacher implementation is linear-time; the alternative remains useful for understanding and independent cross-checking.

Alternative complexity: O(N²) time, O(N) peak auxiliary space including the reverse-string shortcut.

### Verification

The saved original submission received 100 points. The current main solution is a separate, more efficient implementation, locally verified by 90 checks on 45 official, boundary and independent differential inputs. Run `python test_solution.py`; inputs and results are in [examples.json](examples.json) and [test_cases.json](test_cases.json).

## 출처 / Sources

- [프로그래머스 공식 문제: 가장 긴 팰린드롬](https://school.programmers.co.kr/learn/courses/30/lessons/12904) — 조건·예제 / task rules and examples. 확인 / checked: 2026-10-19.
