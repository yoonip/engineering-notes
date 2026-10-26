# Python 풀이

문제별 코드, 줄별 주석, 풀이 설명과 검증 자료를 레벨별로 정리한 목록입니다.

[프로그래머스 전체 목차](../README.md) · [전체 코드 목록](catalog.json) · [기존 검증 기록](../VALIDATION.md)

[유형별 학습](../유형별학습_algorithm-patterns/README.md)과 [연습문제 찾기](../유형별학습_algorithm-patterns/연습문제_problem-index.md)에서 같은 문제의 C·C++·Python 풀이를 비교할 수 있습니다. 유형의 원리·정당성·반례와 언어별 구현 비용을 함께 설명합니다.

## 레벨별 목록

| 레벨 | Python3 제출 기록 | Python 비교 풀이 |
|---|---:|---:|
| [레벨 0](level0/README.md) | 240 | 0 |
| [레벨 1](level1/README.md) | 88 | 0 |
| [레벨 2](level2/README.md) | 117 | 2 |
| [레벨 3](level3/README.md) | 82 | 6 |
| [레벨 4](level4/README.md) | 25 | 2 |
| [레벨 5](level5/README.md) | 2 | 0 |

## 기록 구분

Python3 제출 기록 554개와 Python 비교 풀이 10개를 구분합니다. 비교 풀이 폴더에는 당시 C++ 제출본과 검증 자료도 함께 보관합니다. 레벨 5의 미완료 시도는 해당 레벨 목록에서 따로 확인할 수 있습니다. SQL 자료와 SQL 검증용 Python 스크립트는 기존 레벨별 자료에 남아 있습니다.

## 검증 실행

저장소 최상위에서 회귀 검사를 실행합니다.

```bash
python -B -m unittest discover -s programmers/Python/tests
```

문제별 검증과 원본 대조 방법은 [검증 기록](../VALIDATION.md)에서 확인할 수 있습니다.

## 레벨 5 재풀이 기록

기존 Python3 제출 기록 554개와 비교 풀이 10개는 이전 보관 목록의 수치로 유지합니다. 2026년 10월 24일 재풀이는 [별도 레벨 5 기록](<LEVEL5_REVISIT.md>)과 [문제별 목록](<level5/revisit_20261024/README.md>)에 연결합니다. 지원 문제 14개 중 정답 13개, 실패 5회 후 중단 1개입니다. 실제 제출은 총 18회이며 실패 결과는 5회입니다.
