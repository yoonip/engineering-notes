# 가사 검색

Level 4 · `60060` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/60060)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

?가 정확히 한 글자를 뜻하는 패턴과 일치하는 단어 수를 구한다. ?는 한쪽 끝에 연속해서만 나온다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`2≤word/query counts≤100000; individual lengths:1..10000; each total length≤1000000; distinct lowercase words; ? forms one nonempty prefix or suffix.`

## 풀이를 따라가기

단어를 길이별로 정렬한다. 고정 접두사를 공유하는 같은 길이 단어는 정렬 결과에서 연속이다. ?를 a·z로 바꾼 두 경계를 이진 탐색한다. 접미사는 단어와 질의를 뒤집어 접두사 문제로 만든다.

길이가 먼저 같고 문자가 소문자이므로 두 사전순 경계 사이가 정확히 일치 집합이다. 가운데 ?나 양쪽 ? 패턴에는 이 경계식을 그대로 쓸 수 없다.

## 다른 방법과 비교

대안은 길이별 정방향·역방향 trie에 접두사별 단어 수를 저장한다. 총 글자 수에 비례해 검색할 수 있지만 Python의 작은 딕셔너리 노드가 많아 메모리 상수가 커질 수 있다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O((W+Q) log N), 문자열 비교 포함 / including comparisons` | `O(W)` |
| 대안 풀이 | `O(W+Q) 평균 해시 / expected hashing` | 코드의 상태·탐색 구조 참조 |

W는 단어의 총 글자 수, Q는 질의의 총 글자 수, N은 단어 수다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Count words matching patterns where each ? represents one character and all wildcards form a single prefix or suffix.

Input limits and constants, using the parameter names in the code:

`2≤word/query counts≤100000; individual lengths:1..10000; each total length≤1000000; distinct lowercase words; ? forms one nonempty prefix or suffix.`

### Following the solution

Sort words by length. Words sharing a fixed prefix occupy one interval; replace wildcards with a/z to find its bounds by binary search. Reverse suffix searches into prefix searches.

Equal lengths and lowercase characters make the lexical interval exact. The same construction does not handle internal or two-ended wildcard patterns.

### Alternative and comparison

The alternative stores prefix counts in forward/reversed tries by word length. Expected work follows total characters, but many small Python dictionary nodes can increase memory overhead.

W and Q are total characters in words and queries, and N is the word count.

The primary solution takes `O((W+Q) log N), 문자열 비교 포함 / including comparisons` time and `O(W)` additional space. The alternative takes `O(W+Q) 평균 해시 / expected hashing` time. Its code shows the states and storage it uses.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 가사 검색](https://school.programmers.co.kr/learn/courses/30/lessons/60060): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
