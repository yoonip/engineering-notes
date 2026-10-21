# 보관 범위와 확인 결과 | Archive coverage

이 문서는 2026-10-19에 확인한 보관·검증 범위의 기록입니다. 아래 수량은 당시의 제출 자료와 실행 결과를 가리키며, 사이트에 새로 추가되는 문제까지 완료했다는 뜻은 아닙니다.

| 범위 | 코드·설명 | 확인한 내용 |
|---|---|---|
| 레벨 2~4, 309문제 | 조건, 풀이 원리, 정답 근거, 기본·대안 구현, 한국어·영어 해설 | 원본 제출 해시, 문제별 로컬 검증 스크립트 |
| 앞서 보관한 277문제 | 레벨 0·1의 273개와 레벨 5의 4개, 제출 코드와 전체 줄별 주석본 | 저장된 100점 기록, 코드 일치, 각 줄의 설명, Python 구문 |
| 과거 제출본 86문제 | 레벨 0의 4개와 레벨 1의 82개, 원본·주석본·풀이 원리·비용·유형 | 제출 내역 100점, AST 일치, 전체 주석본 일치, 공개 예제 197개 |
| 레벨 5, 389632 | Python 네 버전과 시간 초과 분석 | 저장된 부분 통과 기록, 작은 입력 비교, 로컬 실행시간 |

## 레벨 0·1 전체 대조

언어·상태 필터 없이 레벨 0·1의 전체 18페이지를 확인했습니다. [사이트 목록](level0_1_catalog.json)의 359개 문제 번호와 보관한 코드의 문제 번호 집합이 같습니다.

| 난이도 | 사이트 문제 수 | 코드·줄별 설명 | 빠진 문제 | 중복 번호 |
|---|---:|---:|---:|---:|
| 레벨 0 | 240 | 240 | 0 | 0 |
| 레벨 1 | 119 | 119 | 0 | 0 |
| 합계 | 359 | 359 | 0 | 0 |

기존에 미완료였던 273문제뿐 아니라 그 전에 완료한 86문제도 포함했습니다. 과거 제출은 사이트의 정답 100/100 항목을 열어 원본 코드와 제출 시각을 확인했습니다. 원본의 해시와 주석본의 해시는 문제별 `grading.json`과 [과거 제출 목록](historical_submissions.json)에 있습니다.

새 주석본은 원본에서 기존 설명 주석과 빈 줄을 정리하고 줄별 설명을 덧붙였습니다. 원본과 같은 순서의 실행 구문을 유지하며, Python AST 대조로 이를 확인했습니다. 함수가 반복 정의된 원본도 그대로 보존하고 마지막 정의가 호출되는 점을 설명했습니다. 996개 코드 줄에 설명을 붙였으며, 원본과 새 파일을 공개 예제 197개에 각각 실행한 394회 검사가 모두 통과했습니다. [실행 기록](HISTORICAL_VALIDATION.json)과 재실행 코드가 있습니다.

```bash
python programmers/tests/verify_history.py
python programmers/tests/verify_archive.py
```

## 전체 보관 수와 채점 범위

통과한 672문제는 [전체 목록](all_problems.json)에 중복 없이 들어 있습니다. 309개의 상세 풀이, 277개의 기존 제출본, 86개의 과거 제출본을 구분합니다. [파일 대조 결과](ARCHIVE_CHECK.json)에서 해시·주석본과 레벨 0·1의 누락 여부를 확인할 수 있습니다.

과거 86개 주석본은 사이트에 다시 제출하지 않았습니다. 100점은 보존한 원본의 사이트 채점 결과이며 공개 예제 비교는 로컬 검사입니다. 빈칸·한 줄 수정 형식 16문제의 전체 주석본도 학습용 파일로 구분했습니다.

레벨 5는 21문제 중 4문제 통과, 1문제 시간 초과, 16문제 미작성 상태입니다. 미완료 17문제는 통과 개수에 합산하지 않습니다. 시간 초과 코드는 [별도 폴더](level5/attempts/389632/README.md)에 있습니다.

## English

Checked on 2026-10-19. All 359 Level 0–1 IDs from the complete 18-page unfiltered listing match the archived code: 240 Level 0 problems and 119 Level 1 problems, with zero missing or duplicate IDs. The collection includes both 273 previously unfinished problems and 86 older accepted submissions.

The 86 historical Python submissions were copied from accepted 100/100 entries in the website history. Their original source, timestamps and hashes are preserved. Annotated copies keep the same executable AST, including repeated function definitions in their original order. The notes explain that the final definition binds the function name. All 996 code lines have annotations. Both source versions passed 197 public examples, for 394 executions. [Execution records](HISTORICAL_VALIDATION.json) and `tests/verify_history.py` reproduce those comparisons.

The [combined catalog](all_problems.json) contains 672 distinct accepted problems: 309 full study notes, 277 earlier archived submissions and 86 historical submissions. [Archive checks](ARCHIVE_CHECK.json) verify file integrity, exact commented copies and complete Level 0–1 ID coverage. The newly annotated copies were not resubmitted; website scores belong to the preserved accepted originals, while public-example comparisons are local checks. Sixteen restricted-editing exercises distinguish their original format from complete study files.

Level 5 remains four accepted problems, one timed-out attempt and 16 problems without archived solutions. The [failed attempt](level5/attempts/389632/README.md) is excluded from accepted totals.
