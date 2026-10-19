# 구성과 변경 기록

프로그래머스 공개 연습문제 39개의 Python 풀이를 모았습니다. 01~39번으로 구분하며 문제명과 원문 링크는 `catalog.json`에서 확인할 수 있습니다.

각 파일에는 하나의 실행 코드와 알고리즘을 고른 이유, 시간·공간 비용 주석을 남겼습니다. 같은 코드를 전체 주석으로 다시 적었던 부분은 없앴습니다. 처음 정리할 때 `36_string_to_integer.py`에서 제거한 확인용 `print`도 그대로 제외했습니다.

## 자료구조와 탐색 변경

| 번호 | 문제 | 변경 내용 |
| --- | --- | --- |
| 06 | 공원 / 돗자리 | 후보 위치마다 영역을 확인하던 방식에서 한 행만 저장하는 최대 정사각형 DP로 변경 |
| 09 | 붕대 감기 | 매초 시뮬레이션하던 회복을 공격 사이 간격과 연속 회복 횟수로 계산 |
| 11 | 둘만의 암호 | 알파벳 위치 표로 글자를 찾고 리스트에 결과를 모아 join |
| 18 | 나머지가 1이 되는 수 찾기 | n 전체 범위 대신 n-1의 약수를 정수 제곱근까지 탐색 |
| 20 | 약수의 개수와 덧셈 | 완전제곱수의 부호만 바뀌는 성질을 등차합·제곱합 수식에 적용해 구간 순회 제거 |
| 22 | 신규 아이디 추천 | 필터링과 연속 마침표 제거를 한 번에 처리하고 join |
| 23 | 크레인 인형뽑기 게임 | 열별 스택을 만들어 인형을 꺼낼 때 위에서 다시 탐색하지 않도록 변경 |

이 일곱 풀이 외 나머지 32개는 이전 공개본과 실행 코드의 AST가 같습니다. 단일 실행 코드 구조에 맞춰 구문·함수 정의·설명 주석·불러올 때의 무출력을 검사하며, 기존 예제와 독립 비교 검사는 유지했습니다.

65개 테스트에서 풀이 함수를 4,190회 호출했습니다. 기존 1,359회에 일곱 풀이의 추가 회귀 검사 2,831회를 더한 수치입니다. 공개 예제와 합성 입력을 사용하며, 테스트의 식별자와 데이터도 합성 값입니다. 현재 CPython 3.13.14의 결과와 이전 CPython 3.12.14의 결과는 `VALIDATION.json`에 구분해 남겼습니다.

## English

This collection contains thirty-nine Python solutions to public Programmers exercises. Files are numbered 01–39; `catalog.json` records the problem names and original links.

Each file contains one executable implementation, with comments explaining its algorithm choice and time/space costs. The fully commented copies of the same code were removed. The diagnostic `print` removed from `36_string_to_integer.py` during the initial cleanup remains excluded.

### Data structures and search changes

| Number | Exercise | Change |
| --- | --- | --- |
| 06 | Park mats | Replaced repeated candidate-region checks with maximum-square DP storing one row |
| 09 | Bandage | Replaced second-by-second recovery with calculations over attack intervals and completed healing streaks |
| 11 | Letter-skipping cipher | Added an alphabet-position table and list accumulation followed by join |
| 18 | Remainder-one search | Searches divisors of n-1 up to its integer square root instead of scanning the full range |
| 20 | Divisor counts and addition | Uses arithmetic-series and square-sum formulas to account for perfect-square sign changes without iterating over the interval |
| 22 | New ID | Combines filtering and repeated-period removal in one pass, followed by join |
| 23 | Crane game | Uses per-column stacks to avoid scanning each column from the top for every move |

The executable ASTs of the other thirty-two solutions match the previous published version. Checks now cover syntax, function definitions, explanatory comments, and no output during loading, matching the single-implementation structure. The original examples and independent-reference comparisons were retained.

Sixty-five tests made 4,190 solution calls: the original 1,359 plus 2,831 regression calls for the seven changed solutions. Tests use public examples and synthetic inputs, including synthetic identifiers and data. `VALIDATION.json` separates the current CPython 3.13.14 results from the earlier CPython 3.12.14 results.
