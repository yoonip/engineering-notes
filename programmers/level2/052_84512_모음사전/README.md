# 모음사전

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/84512) · Level 2 · Python3

A·E·I·O·U로 만든 길이 1~5 단어의 사전 순서를 구한다.

## 조건과 입출력

입력 매개변수: `word`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- word의 길이는 1 이상 5 이하입니다.

## 풀이를 따라가기

자리별 건너뛰는 단어 수 781·156·31·6·1을 사용한다. 해당 글자보다 앞선 모음 수만큼 그 가중치를 더하고 현재 접두 단어 하나를 더한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(word):
    # 남은 자리의 모든 접미어 수 1+5+…를 자리별 가중치로 쓴다.
    weights = [781, 156, 31, 6, 1]
    answer = 0
    for index, character in enumerate(word):
        # 앞선 모음의 전체 묶음과 현재 접두 단어 하나를 건너뛴다.
        answer += 'AEIOU'.index(character) * weights[index] + 1
    return answer
```

## 왜 맞는가

각 자리에서 모음 하나를 건너뛰면 그 글자로 시작하는 길이 0~남은 길이 접미어의 수 1+5+…만큼 건너뛴다. 이를 자리별로 더하면 정확한 사전 순위다.

시간 O(len(word)), 공간 O(1) / Time O(len(word)), space O(1)

주의할 점: 단어 자체가 접두어보다 뒤에 오므로 매 자리 +1이 필요하다. 빈 문자열은 사전에 없다.

## 다른 방법: 사전순 DFS로 단어 생성

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
def solution(word):
    rank=0
    answer=0
    def visit(prefix):
        nonlocal rank,answer
        if prefix:
            rank+=1
            if prefix==word: answer=rank
        if len(prefix)==5: return
        for vowel in 'AEIOU': visit(prefix+vowel)
    visit('')
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 자리별 건너뛰는 단어 수 781·156·31·6·1을 사용한다. 해당 글자보다 앞선 모음 수만큼 그 가중치를 더하고 현재 접두 단어 하나를 더한다. | 사전순 DFS로 단어 생성 |
| 비용 | 시간 O(len(word)), 공간 O(1) / Time O(len(word)), space O(1) | 최대 3905단어, 시간 O(5^5), 공간 O(5) / At most 3905 words, time O(5^5), space O(5) |

## 검증

공식 예제 4개와 생성 입력 60개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find the dictionary rank among words of lengths one through five over A, E, I, O and U.

### Conditions and input/output

Input arguments: `word`. The return value is an integer satisfying the task described below.

- 1 ≤ len(word) ≤ 5; alphabet A,E,I,O,U

### Approach

Use positional block sizes 781, 156, 31, 6 and 1. Add the number of preceding vowels times that block size, plus one for the current prefix word.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Skipping one vowel skips all its suffixes, whose count is 1+5+… up to the remaining length. Adding these disjoint blocks yields the exact rank.

시간 O(len(word)), 공간 O(1) / Time O(len(word)), space O(1)

Boundary cases: Add one at each position because the prefix precedes its extensions. The empty word is excluded.

### Alternative: Generate dictionary order with DFS

It computes the same result using different intermediate states or evaluation steps. 최대 3905단어, 시간 O(5^5), 공간 O(5) / At most 3905 words, time O(5^5), space O(5)

The main approach follows the steps described above. The alternative uses generate dictionary order with dfs; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 4 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 모음사전](https://school.programmers.co.kr/learn/courses/30/lessons/84512) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
