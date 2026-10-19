# 프로그래머스 — 문제 풀이와 학습 기록

문제를 읽고 풀이를 고르는 과정부터 코드가 답을 만드는 이유까지 정리합니다. 입력이 커질 때 어떤 연산이 병목이 되는지, 같은 문제를 다른 방법으로 풀면 무엇이 달라지는지도 함께 살펴봅니다.

## 문제 찾기

| 난이도 / Level | 문제 수 / Count | 제출 언어 / Submission languages |
|---|---:|---|
| [Level 2](level2/README.md) | 155 | Python3 117 · MySQL 36 · C++ 2 |
| [Level 3](level3/README.md) | 109 | Python3 82 · MySQL 21 · C++ 6 |
| [Level 4](level4/README.md) | 45 | Python3 25 · MySQL 18 · C++ 2 |

총 309문제이며 제출 언어별로 Python 224개, MySQL 75개, C++ 10개입니다. C++ 문제에는 별도의 Python 비교 구현도 있습니다.

[알고리즘 길잡이](ALGORITHMS.md) · [검증 내용과 실행 방법](VALIDATION.md) · [검색용 목록](catalog.json)

## 각 문제에 담은 내용

- 문제의 목표, 입력 범위, 예외와 정렬 조건
- 자료구조와 알고리즘을 선택한 이유, 코드가 답을 만드는 과정
- 한국어 주석을 단 기본 코드와 별도의 대안 코드
- 시간·공간 비용과 두 방법의 차이
- 공식 예제, 경계 입력, 생성 입력을 이용한 검증 코드
- 공식 문제 링크와 원본 제출 파일

설명은 한국어를 먼저 읽은 뒤 같은 내용을 영어로 확인할 수 있게 구성했습니다. 문제의 긴 배경과 그림은 공식 페이지에서 확인하고, 여기에서는 풀이에 필요한 조건을 요약합니다. 느린 전수 탐색은 작은 입력의 기준값을 확인하는 용도로 표시했습니다. 효율적인 기본 풀이와 적용 범위를 비교해 볼 수 있습니다.

SQL에서는 NULL, 중복, 공동 최댓값, 날짜 경계, 최종 정렬을 특히 구분합니다. 원본 채점 기록과 새로 실행한 로컬 검증은 [검증 기록](VALIDATION.md)에 따로 적었습니다.

## English

This collection follows the reasoning from problem conditions to an implementation: why an algorithm fits, how it produces the answer, and which operations become expensive as inputs grow. Alternative implementations make the trade-offs concrete.

The collection contains 309 problems: 155 at Level 2, 109 at Level 3, and 45 at Level 4. Submission languages are Python for 224 problems, MySQL for 75, and C++ for 10. C++ problems also have Python comparison implementations.

Each problem includes its objective and bounds, relevant edge and ordering rules, algorithm choice, correctness reasoning, commented primary code, a separate alternative, time and space costs, executable checks and an official source link. Explanations appear in Korean first and English second; code comments remain in Korean.

Long problem narratives and figures remain on the official pages. These notes summarize the conditions needed for solving them. Exhaustive references are labeled with their small-input scope and compared with the efficient primary solution. SQL notes distinguish NULLs, duplicates, tied maxima, date boundaries and final ordering.

[Algorithm guide](ALGORITHMS.md) · [Validation and reproducible commands](VALIDATION.md) · [Machine-readable index](catalog.json)
