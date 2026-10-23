# 프로그래머스 풀이 | Programmers solutions

## 언어별 풀이

| 분류 | 목록 |
|---|---|
| C | [C 풀이](C/README.md) |
| C++ | [C++ 풀이](C%2B%2B/README.md) |
| Python 중심 기존 자료 | [기존 레벨별 목록](#기존-레벨별-목록) |

## 기존 레벨별 목록

제출 코드, 줄별 문법 설명, 풀이 원리와 채점 기록을 모았습니다. 사이트의 과거 제출 결과와 로컬 검증을 구분하며, 통과한 코드와 미완료 시도는 별도로 보관합니다. 사이트 목록과 대조한 시점과 범위는 [보관 범위](COVERAGE.md)에 있습니다.

| 난이도 / Level | 보관 언어 / Languages |
|---|---|
| [Level 0](level0/README.md) | Python3 |
| [Level 1](level1/README.md) | Python3 · MySQL |
| [Level 2](level2/README.md) | Python3 · MySQL · C++ |
| [Level 3](level3/README.md) | Python3 · MySQL · C++ |
| [Level 4](level4/README.md) | Python3 · MySQL · C++ |
| [Level 5](level5/README.md) | Python3 · MySQL |

[알고리즘별 설명](ALGORITHMS.md) · [보관 범위와 확인 결과](COVERAGE.md) · [검증 기록](VALIDATION.md) · [전체 검색 목록](all_problems.json)

## 자료를 읽는 방법

레벨 2~4의 상세 풀이에는 입력 조건, 알고리즘 선택, 정답이 되는 이유, 기본·대안 코드, 시간·공간 비용, 예제와 검증 코드가 있습니다. 설명은 한국어와 영어로, 코드 주석은 한국어로 적었습니다. [상세 풀이 목록](catalog.json)과 [검증 실행 방법](VALIDATION.md)에서 확인할 수 있습니다.

레벨 0·1과 레벨 5의 제출 자료에는 실행 코드 아래에 동일한 코드 전체를 주석 처리해 각 줄의 문법과 목적을 한국어로 적었습니다. 문제별 README에서도 코드와 풀이를 바로 읽을 수 있습니다. [기존 제출 자료](recent_submissions.json)와 [과거 제출 내역에서 가져온 원본](historical_submissions.json)은 출처를 구분해 보관했습니다.

과거 제출본 86개는 사이트 ‘제출 내역’에서 Python3 정답 100/100을 확인하고 가져왔습니다. `submitted_original.py`는 원본이고, `solution.py`는 기존 주석과 빈 줄을 정리한 실행 코드에 줄별 설명을 덧붙인 파일입니다. 두 파일의 실행 구문 AST가 같고 공개 예제 197개를 각각 실행한 결과도 같습니다. 같은 이름의 함수가 여러 번 정의된 원본은 정의 순서를 유지하고 마지막 함수가 쓰이는 이유를 설명했습니다. 이 주석본을 사이트에 새로 제출한 것은 아닙니다.

레벨 0·1은 [사이트 전체 목록](level0_1_catalog.json)과 문제 번호를 대조해 누락과 중복이 없는지 확인했습니다. 빈칸 채우기·한 줄 수정 형식의 16문제는 당시 제출 형식과 학습용 전체 주석본을 구분했습니다.

레벨 5는 일부 문제의 통과 코드만 보관하고 있습니다. [문자열과 알파벳과 쿼리](level5/attempts/389632/README.md)는 Python 구현별 부분 통과 기록과 시간 초과 원인을 따로 정리했습니다. 이 시도는 통과 코드로 표시하지 않습니다. 풀이를 보관하지 않은 문제까지 완료한 목록은 아닙니다.

## English

The archive separates accepted submissions from incomplete attempts. Saved website grades, source provenance and local checks are documented separately. The Level 0–1 archive was matched by ID against the site's unfiltered listing at the time of collection; this does not establish coverage of future additions.

The detailed Level 2–4 study notes include conditions, algorithm choice, correctness reasoning, primary and alternative implementations, complexity, examples and executable checks. Explanations are in Korean and English; code comments are in Korean. Their [catalog](catalog.json) and [validation record](VALIDATION.md) describe the checks.

The Level 0–1 and Level 5 submission notes contain executable code followed by an exact commented copy with Korean syntax and purpose notes. Their README files include the code and method explanations. The [earlier archived entries](recent_submissions.json) and [historical submissions](historical_submissions.json) retain separate provenance records.

The 86 historical Python submissions were copied from accepted 100/100 entries in the website submission history. Original source files are preserved. Annotated copies retain the same executable AST and passed 197 public examples against the originals, for 394 executions. Repeated function definitions retain their original order, with the final binding explained. The annotated copies were not resubmitted. Sixteen restricted-editing exercises distinguish their original submission format from the complete study copies.

Level 5 is a partial archive. Its [failed Python attempt](level5/attempts/389632/README.md) has a separate timeout analysis and is not marked as accepted. Problems without an archived solution are not presented as completed.

[Coverage](COVERAGE.md) · [All accepted problems](all_problems.json) · [Level 0–1 site catalog](level0_1_catalog.json)
