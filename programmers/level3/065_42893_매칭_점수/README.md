# 매칭 점수

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [42893 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42893)

## 문제와 조건

각 페이지의 검색어 기본점수와 외부 링크로 나눠 받은 링크점수를 합쳐 가장 높은 매칭점수의 페이지 인덱스를 구합니다.

검색어는 영문 대소문자 무시·단어 단위로 비교합니다. 모든 URL은 https이고 동점은 작은 페이지 인덱스입니다.

`1≤pages≤20; 1≤HTML length≤1,500; 1≤word length≤12`

## 풀이를 따라가기

1. HTML에서 페이지 주소와 외부 링크를 추출하고, 영문자끼리 이어진 단어만 비교해 기본 점수를 셉니다. 각 링크에 기본 점수/외부 링크 수를 한 번 분배합니다.
2. 예제 1은 기본 점수 3·1·1에 링크 점수를 더해 4.5·4·1.5가 되어 0번이 이깁니다. 목록 밖으로 향하는 링크도 분모에는 포함합니다.
3. 전체 HTML 길이 S, 전체 링크 수 E일 때 파싱·집계는 O(S+E). 분수 계산 비용은 분모 크기에 따르며 페이지는 최대 20개입니다. 공간 O(S+E).

## 왜 이 방법으로 풀 수 있나

HTML에서 페이지 주소와 외부 링크를 추출하고, 영문자끼리 이어진 단어만 비교해 기본 점수를 셉니다. 각 링크에 기본 점수/외부 링크 수를 한 번 분배합니다.

시간·공간: 전체 HTML 길이 S·링크 수 E에서 파싱·집계 O(S+E), 분수의 큰 정수 연산 비용 별도, 공간 O(S+E)

## 다른 방법과 비교

HTMLParser로 주소와 링크를 추출합니다. 링크 점수는 Fraction으로 누적해 부동소수점 동점 오차를 피합니다. 정규식을 쓰는 기본 풀이와 파싱 경로가 다릅니다.

| 항목 | 기본 풀이 | HTMLParser와 정확한 분수 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 전체 HTML 길이 S·링크 수 E에서 파싱·집계 O(S+E), 분수의 큰 정수 연산 비용 별도, 공간 O(S+E) | O(S+E), 공간 O(S+E), 분수 연산 비용 별도 |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

예제 입력과 결과는 [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42893)에서 확인할 수 있습니다.

[examples.json](examples.json) contains the official example inputs and expected outputs, including narrative-format examples.

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Return the page index with highest matching score: word-count base score plus incoming link contributions.

Match complete alphabetic words case-insensitively. URLs use https, and score ties prefer the smaller page index.

`1≤pages≤20; 1≤HTML length≤1,500; 1≤word length≤12`

### Method and correctness

Parse each page’s canonical URL and outgoing links. Count case-insensitive complete alphabetic words for the base score, then distribute each page’s base score once over its outgoing links. Links to pages outside the input still contribute to the denominator. Exact rational arithmetic prevents score-tie rounding errors.

Main complexity: O(S+E) parsing and aggregation, excluding big-integer Fraction arithmetic.

### Alternative and trade-offs

Extract addresses and links with HTMLParser, then accumulate scores as exact Fractions. This independently checks the regular-expression parser in the main solution.

Code: [alternative.py](alternative.py).

Complexity: O(S+E), space O(S+E), excluding Fraction arithmetic.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 매칭 점수](https://school.programmers.co.kr/learn/courses/30/lessons/42893) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
