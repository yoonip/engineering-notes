# Python 연습문제 풀이

프로그래머스 공개 연습문제를 바탕으로 AI로 작성한 학습 풀이 39개를 정리했다. 실행 코드와 줄별 한국어 주석을 함께 수록했다. 문자열과 기초 연산부터 정렬, 해시, 스택, 힙, BFS, Dijkstra, HLD와 implicit treap까지 다룬다.

## 구성

| 경로 | 내용 |
| --- | --- |
| `solutions/` | 실행 가능한 `solution` 함수와 같은 코드의 주석 설명 |
| `catalog.json` | 문제 링크와 알고리즘 분류 |
| `tests/` | 예제·경계값·독립 구현 비교 검사 |
| `VALIDATION.json` | 로컬 실행 결과 |
| `PROVENANCE.md` | 작성 경위와 공개본 변경 기록 |
| `SHA256SUMS` | 공개 파일의 SHA256 목록 |

## 실행

Python 3.12에서 표준 라이브러리로 실행한다. 이 디렉터리에서 검사 명령을 실행한다.

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
| 06 | [공원 / 돗자리](https://school.programmers.co.kr/learn/courses/30/lessons/340198) | 완전탐색 | [Python](solutions/06_park_mats.py) |
| 07 | [가장 많이 받은 선물](https://school.programmers.co.kr/learn/courses/30/lessons/258712) | 해시 / 쌍 비교 | [Python](solutions/07_most_gifts.py) |
| 08 | [데이터 분석](https://school.programmers.co.kr/learn/courses/30/lessons/250121) | 필터 / 정렬 | [Python](solutions/08_data_analysis.py) |
| 09 | [붕대 감기](https://school.programmers.co.kr/learn/courses/30/lessons/250137) | 시뮬레이션 | [Python](solutions/09_bandage.py) |
| 10 | [이웃한 칸](https://school.programmers.co.kr/learn/courses/30/lessons/250125) | 격자 탐색 | [Python](solutions/10_neighbor_cells.py) |
| 11 | [둘만의 암호](https://school.programmers.co.kr/learn/courses/30/lessons/155652) | 문자열 / 나머지 연산 | [Python](solutions/11_secret_code.py) |
| 12 | [중력 작용](https://school.programmers.co.kr/learn/courses/30/lessons/77887) | HLD / implicit treap / 구간 합 | [Python](solutions/12_gravity.py) |
| 13 | [명예의 전당 (1)](https://school.programmers.co.kr/learn/courses/30/lessons/138477) | 최소 힙 | [Python](solutions/13_hall_of_fame.py) |
| 14 | [햄버거 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/133502) | 스택 | [Python](solutions/14_hamburger.py) |
| 15 | [삼총사](https://school.programmers.co.kr/learn/courses/30/lessons/131705) | 완전탐색 / 조합 | [Python](solutions/15_three_friends.py) |
| 16 | [성격 유형 검사하기](https://school.programmers.co.kr/learn/courses/30/lessons/118666) | 해시 / 집계 | [Python](solutions/16_personality_test.py) |
| 17 | [신고 결과 받기](https://school.programmers.co.kr/learn/courses/30/lessons/92334) | 집합 / 해시 | [Python](solutions/17_report_results.py) |
| 18 | [나머지가 1이 되는 수 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/87389) | 선형 탐색 | [Python](solutions/18_remainder_one.py) |
| 19 | [숫자 문자열과 영단어](https://school.programmers.co.kr/learn/courses/30/lessons/81301) | 문자열 치환 | [Python](solutions/19_number_words.py) |
| 20 | [약수의 개수와 덧셈](https://school.programmers.co.kr/learn/courses/30/lessons/77884) | 약수 완전탐색 | [Python](solutions/20_divisor_count_sum.py) |
| 21 | [음양 더하기](https://school.programmers.co.kr/learn/courses/30/lessons/76501) | 반복 / 조건 | [Python](solutions/21_signed_sum.py) |
| 22 | [신규 아이디 추천](https://school.programmers.co.kr/learn/courses/30/lessons/72410) | 문자열 처리 | [Python](solutions/22_new_id.py) |
| 23 | [크레인 인형뽑기 게임](https://school.programmers.co.kr/learn/courses/30/lessons/64061) | 스택 / 시뮬레이션 | [Python](solutions/23_crane_game.py) |
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

## 검증 범위

39개 풀이의 구문과 실행 코드·주석 코드의 AST 일치를 확인하고, 50개 테스트를 실행했다. 예제·경계값 123건과 BFS·Dijkstra·그리디·스택·힙·중력 작용 등의 독립 구현 비교를 포함해 풀이 함수를 총 1,359회 호출했다. 비교 검사는 작은 합성 입력을 사용한다.

`VALIDATION.json`은 Python 3.12의 로컬 검사 기록이며 온라인 채점 결과는 포함하지 않는다.

## English overview

This collection contains 39 AI-generated Python learning solutions with Korean code annotations. The 50 standard-library tests cover examples, boundary cases, and comparisons against independent implementations, making 1,359 solution calls across all 39 files.
