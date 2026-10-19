# Python 연습문제 풀이

프로그래머스 공개 연습문제 39개의 풀이와 학습 기록을 정리했다. 각 풀이에는 알고리즘을 고른 이유와 시간·공간 비용을 한국어 주석으로 붙였다. 문자열과 기초 연산부터 정렬, 해시, 스택, 힙, BFS, Dijkstra, HLD와 implicit treap까지 다룬다.

## 구성

| 경로 | 내용 |
| --- | --- |
| `solutions/` | 문제마다 하나의 `solution` 함수와 알고리즘 설명 주석 |
| `catalog.json` | 문제 링크와 알고리즘 분류 |
| `tests/` | 예제·경계값·독립 구현 비교 검사 |
| `VALIDATION.json` | 로컬 실행 결과 |
| `PROVENANCE.md` | 구성과 변경 기록 |
| `SHA256SUMS` | 공개 파일의 SHA256 목록 |

## 실행

Python 3.12 이상과 표준 라이브러리로 실행한다. 현재 검사는 CPython 3.13.14에서 진행했다. 이 디렉터리에서 다음 명령을 실행한다.

```bash
python -B -m unittest discover -s tests -v
```

각 파일의 `solution` 함수를 직접 호출할 수도 있다.

```python
import runpy

solution = runpy.run_path("solutions/39_middle_character.py")["solution"]
print(solution("abcde"))  # c
```

## 문제 목록

| 번호 | 공개 문제 | 알고리즘 | 소스 |
|---|---|---|---|
| 01 | [공원 산책](https://school.programmers.co.kr/learn/courses/30/lessons/172928) | 격자 시뮬레이션 | [Python](solutions/01_park.py) |
| 02 | [게임 맵 최단거리](https://school.programmers.co.kr/learn/courses/30/lessons/1844) | BFS / deque | [Python](solutions/02_game_map.py) |
| 03 | [배달](https://school.programmers.co.kr/learn/courses/30/lessons/12978) | Dijkstra / 최소 힙 | [Python](solutions/03_delivery.py) |
| 04 | [유연근무제](https://school.programmers.co.kr/learn/courses/30/lessons/388351) | 시간 변환 / 시뮬레이션 | [Python](solutions/04_flexible_work.py) |
| 05 | [노란불 신호등](https://school.programmers.co.kr/learn/courses/30/lessons/468371) | 최소공배수 / 주기 탐색 | [Python](solutions/05_yellow_lights.py) |
| 06 | [공원 / 돗자리](https://school.programmers.co.kr/learn/courses/30/lessons/340198) | 최대 정사각형 DP | [Python](solutions/06_park_mats.py) |
| 07 | [가장 많이 받은 선물](https://school.programmers.co.kr/learn/courses/30/lessons/258712) | 해시 / 쌍 비교 | [Python](solutions/07_most_gifts.py) |
| 08 | [데이터 분석](https://school.programmers.co.kr/learn/courses/30/lessons/250121) | 필터 / 정렬 | [Python](solutions/08_data_analysis.py) |
| 09 | [붕대 감기](https://school.programmers.co.kr/learn/courses/30/lessons/250137) | 공격 간격 일괄 회복 | [Python](solutions/09_bandage.py) |
| 10 | [이웃한 칸](https://school.programmers.co.kr/learn/courses/30/lessons/250125) | 격자 탐색 | [Python](solutions/10_neighbor_cells.py) |
| 11 | [둘만의 암호](https://school.programmers.co.kr/learn/courses/30/lessons/155652) | 알파벳 위치 표 / 나머지 연산 | [Python](solutions/11_secret_code.py) |
| 12 | [중력 작용](https://school.programmers.co.kr/learn/courses/30/lessons/77887) | HLD / implicit treap / 구간 합 | [Python](solutions/12_gravity.py) |
| 13 | [명예의 전당 (1)](https://school.programmers.co.kr/learn/courses/30/lessons/138477) | 최소 힙 | [Python](solutions/13_hall_of_fame.py) |
| 14 | [햄버거 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/133502) | 스택 | [Python](solutions/14_hamburger.py) |
| 15 | [삼총사](https://school.programmers.co.kr/learn/courses/30/lessons/131705) | 완전탐색 / 조합 | [Python](solutions/15_three_friends.py) |
| 16 | [성격 유형 검사하기](https://school.programmers.co.kr/learn/courses/30/lessons/118666) | 해시 / 집계 | [Python](solutions/16_personality_test.py) |
| 17 | [신고 결과 받기](https://school.programmers.co.kr/learn/courses/30/lessons/92334) | 집합 / 해시 | [Python](solutions/17_report_results.py) |
| 18 | [나머지가 1이 되는 수 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/87389) | n-1의 최소 약수 | [Python](solutions/18_remainder_one.py) |
| 19 | [숫자 문자열과 영단어](https://school.programmers.co.kr/learn/courses/30/lessons/81301) | 문자열 치환 | [Python](solutions/19_number_words.py) |
| 20 | [약수의 개수와 덧셈](https://school.programmers.co.kr/learn/courses/30/lessons/77884) | 등차합 / 제곱합 수식 | [Python](solutions/20_divisor_count_sum.py) |
| 21 | [음양 더하기](https://school.programmers.co.kr/learn/courses/30/lessons/76501) | 반복 / 조건 | [Python](solutions/21_signed_sum.py) |
| 22 | [신규 아이디 추천](https://school.programmers.co.kr/learn/courses/30/lessons/72410) | 한 번의 순회 / 문자열 정규화 | [Python](solutions/22_new_id.py) |
| 23 | [크레인 인형뽑기 게임](https://school.programmers.co.kr/learn/courses/30/lessons/64061) | 열별 스택 / 시뮬레이션 | [Python](solutions/23_crane_game.py) |
| 24 | [다트 게임](https://school.programmers.co.kr/learn/courses/30/lessons/17682) | 문자열 파싱 | [Python](solutions/24_dart_game.py) |
| 25 | [실패율](https://school.programmers.co.kr/learn/courses/30/lessons/42889) | 빈도 집계 / 정렬 | [Python](solutions/25_failure_rate.py) |
| 26 | [2016년](https://school.programmers.co.kr/learn/courses/30/lessons/12901) | 누적 일수 / 나머지 연산 | [Python](solutions/26_year_2016.py) |
| 27 | [문자열 내 마음대로 정렬하기](https://school.programmers.co.kr/learn/courses/30/lessons/12915) | 튜플 정렬 키 | [Python](solutions/27_custom_string_sort.py) |
| 28 | [예산](https://school.programmers.co.kr/learn/courses/30/lessons/12982) | 그리디 / 정렬 | [Python](solutions/28_budget.py) |
| 29 | [행렬의 덧셈](https://school.programmers.co.kr/learn/courses/30/lessons/12950) | 중첩 반복 | [Python](solutions/29_matrix_addition.py) |
| 30 | [핸드폰 번호 가리기](https://school.programmers.co.kr/learn/courses/30/lessons/12948) | 문자열 슬라이싱 | [Python](solutions/30_phone_mask.py) |
| 31 | [평균 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/12944) | 합계 / 평균 | [Python](solutions/31_average.py) |
| 32 | [짝수와 홀수](https://school.programmers.co.kr/learn/courses/30/lessons/12937) | 나머지 연산 | [Python](solutions/32_even_odd.py) |
| 33 | [정수 제곱근 판별](https://school.programmers.co.kr/learn/courses/30/lessons/12934) | 정수 제곱근 | [Python](solutions/33_square_root_check.py) |
| 34 | [자릿수 더하기](https://school.programmers.co.kr/learn/courses/30/lessons/12931) | 형 변환 / 반복 | [Python](solutions/34_digit_sum.py) |
| 35 | [시저 암호](https://school.programmers.co.kr/learn/courses/30/lessons/12926) | 문자 코드 / 나머지 연산 | [Python](solutions/35_caesar_cipher.py) |
| 36 | [문자열을 정수로 바꾸기](https://school.programmers.co.kr/learn/courses/30/lessons/12925) | 정수 형 변환 | [Python](solutions/36_string_to_integer.py) |
| 37 | [문자열 내 p와 y의 개수](https://school.programmers.co.kr/learn/courses/30/lessons/12916) | 대소문자 정규화 / 개수 집계 | [Python](solutions/37_count_p_y.py) |
| 38 | [나누어 떨어지는 숫자 배열](https://school.programmers.co.kr/learn/courses/30/lessons/12910) | 조건 필터 / 정렬 | [Python](solutions/38_divisible_array.py) |
| 39 | [가운데 글자 가져오기](https://school.programmers.co.kr/learn/courses/30/lessons/12903) | 인덱스 / 슬라이싱 | [Python](solutions/39_middle_character.py) |

## 탐색과 자료구조

돗자리는 최대 정사각형 DP, 붕대는 공격 간격 계산, 크레인은 열별 스택으로 같은 영역이나 시간을 다시 훑는 일을 줄였다. 나머지가 1인 수는 n-1의 최소 약수로 찾는다. 약수 개수와 덧셈은 완전제곱수에서만 부호가 바뀐다는 성질을 등차합·제곱합 수식에 적용한다. 구간 길이와 무관하게 정해진 횟수의 정수 연산으로 계산하며, 큰 정수의 연산 비용은 비트 길이에 따라 달라진다. 암호와 아이디 문제는 결과를 리스트에 모아 한 번에 연결한다.

05번 노란불 신호등은 신호 주기의 최소공배수 T를 한 구간 순회한다. 신호가 N개일 때 시간 비용은 O(NT)이며, T가 커지면 실행 시간도 늘어난다.

## 검증 범위

65개 테스트에서 풀이 함수를 총 4,190회 호출했다. 기존 예제·경계값 123건과 독립 구현 대조를 포함한 1,359회 실행 검사는 유지하고, 바꾼 일곱 풀이에 무작위·작은 입력 비교와 큰 간격·정수 제곱 경계·큰 구간 분할 검사 2,831회를 더했다. 추가 검사에서는 입력이 바뀌지 않는지도 확인한다.

39개 파일의 구문, 단일 `solution` 정의, 설명 주석, 불러올 때 출력이 없는지를 검사한다. 일곱 풀이 외 나머지 32개는 이전 공개본과 실행 코드의 AST가 같다.

`VALIDATION.json`에는 현재 CPython 3.13.14의 로컬 검사 결과와 이전 CPython 3.12.14의 검사 기록이 담겨 있다.

## English

Thirty-nine public Programmers exercises are organized as Python solutions and study notes, with Korean comments explaining algorithm choices and time/space costs. Topics range from strings/basic arithmetic to sorting, hashing, stacks, heaps, BFS, Dijkstra, heavy-light decomposition and implicit treaps.

### Files and running

`solutions/` contains one executable `solution` function per exercise, with concise algorithm comments. `catalog.json` records original links and algorithm categories. `tests/` covers examples, boundaries and independent-reference comparisons. `VALIDATION.json`, `PROVENANCE.md` and `SHA256SUMS` hold recorded checks, change notes and hashes.

Use Python 3.12 or later and the standard library. The current checks ran on CPython 3.13.14. Run the listed unittest command from this directory, or load an individual `solution` function with `runpy` as shown above.

### Exercise index

The Korean index above preserves the official titles, original URLs and source links. The same numbered exercises cover:

| Numbers | Topics |
| --- | --- |
| 01–05 | Park walking/grid simulation; shortest game-map path/BFS; delivery/Dijkstra; flexible schedules/time conversion; yellow traffic lights/LCM and periodic search |
| 06–10 | Park mats/rolling maximum-square DP; gifts/hash and pair comparisons; data filtering/sorting; bandage recovery between attacks; neighboring grid cells |
| 11–15 | Letter-skipping cipher/alphabet position table and modular arithmetic; gravity/HLD, implicit treap and range sums; hall of fame/min-heap; hamburger assembly/stack; zero-sum triples/combinations |
| 16–20 | Personality scoring/hash aggregation; report results/set and hash; smallest-divisor search on n-1; number words/string replacement; divisor-count parity through arithmetic-series and square-sum formulas |
| 21–25 | Signed sums; single-pass new-ID normalization; crane game/per-column stacks; dart-score parsing; failure-rate counting/sorting |
| 26–30 | 2016 calendar/cumulative days; custom string sorting/tuple keys; budget/greedy sorting; matrix addition; phone-number masking/slicing |
| 31–35 | Mean; parity; integer square-root check; digit sum; Caesar cipher/character codes |
| 36–39 | String-to-integer conversion; case-insensitive p/y counting; divisible-array filtering/sorting; middle-character indexing/slicing |

### Search and data structures

Maximum-square DP for park mats, interval-based recovery for bandages, and per-column stacks for the crane avoid repeatedly scanning the same regions or times. Remainder-one search uses the smallest divisor of n-1. The divisor-count sum uses arithmetic-series and square-sum formulas, since only perfect squares need a sign change. It performs a fixed number of integer operations regardless of interval width; large-integer operation costs still depend on bit length. The cipher and ID solutions collect characters in lists and join them once.

Exercise 05 searches one least-common-multiple period T of the traffic signals. With N signals, its time cost is O(NT), so larger combined periods increase the runtime.

### Verification

Sixty-five tests made 4,190 solution calls. The original 1,359 calls, including 123 example/boundary cases and independent-reference comparisons, were retained. The seven revised solutions received 2,831 additional calls covering random and small inputs, large time gaps, exact integer-square boundaries, and large-interval partition checks. The additional checks also verify that inputs remain unchanged.

All thirty-nine files are checked for syntax, a single `solution` definition, explanatory comments, and no output during loading. The executable ASTs of the other thirty-two solutions match the previous published version. `VALIDATION.json` contains the current local CPython 3.13.14 results and the earlier CPython 3.12.14 record.
