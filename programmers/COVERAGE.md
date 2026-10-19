# 보관 범위와 확인 결과 | Archive coverage

확인일: 2026-10-19.

| 범위 | 코드·설명 | 확인한 내용 |
|---|---|---|
| 레벨 2~4, 309문제 | 조건, 풀이 원리, 정답 근거, 기본·대안 구현, 한영 설명 | 원본 제출 해시, 문제별 로컬 검증 스크립트 |
| 레벨 0·1, 273문제 | 제출 코드, 같은 코드의 전체 주석본, 짧은 풀이 | 저장된 100점 기록, 코드 일치, 각 줄의 설명, Python 구문 |
| 레벨 5, 4문제 | 제출 코드, 같은 코드의 전체 주석본, 풀이 원리 | 저장된 100점 기록, 코드 일치, 각 줄의 설명, Python 구문 |
| 레벨 5, 389632 | Python 네 버전과 시간 초과 분석 | 저장된 부분 통과 기록, 작은 입력 비교, 로컬 실행시간 |

통과한 586문제는 [전체 목록](all_problems.json)에 중복 없이 들어 있다. 기존 309문제의 상세 풀이 목록은 [catalog.json](catalog.json), 나중에 보관한 277개 제출본은 [recent_submissions.json](recent_submissions.json)에서 구분한다. 파일별 해시와 확인 결과는 [제출본 대조 결과](ARCHIVE_CHECK.json)에 있다.

레벨 0·1에서 새로 푼 273문제는 모두 보관했다. 이 작업 전에 계정에서 이미 완료돼 있던 문제의 코드는 이번 보관 목록에 없다. 따라서 계정의 모든 과거 제출까지 빠짐없이 정리한 자료라고 부르지는 않는다.

레벨 5는 21문제 중 4문제 통과, 1문제 시간 초과, 16문제 미작성 상태다. 미완료 17문제를 통과 개수에 합산하지 않는다. 시간 초과 코드는 [별도 폴더](level5/attempts/389632/README.md)에 두었다.

새로 보관한 277개 코드의 채점은 저장된 사이트 결과다. 이 문서를 정리하며 새로 제출한 결과는 아니다. 빈칸·한 줄 수정 형식의 12문제는 사이트 제출 범위와 전체 학습용 주석본을 구분했다. 코드 대조 검사는 알고리즘 정답성이나 SQL 실행계획을 새로 검증하는 검사가 아니다.

## English

Checked on 2026-10-19. The [combined catalog](all_problems.json) contains 586 distinct accepted problems. The original 309 Level 2–4 entries include full study notes, alternatives and local test scripts. The later 277 entries preserve accepted submissions, exact commented copies and short Korean method notes. [Archive checks](ARCHIVE_CHECK.json) verify file hashes, annotations and Python syntax; they do not add algorithm-correctness or SQL execution-plan coverage.

All 273 previously unfinished Level 0–1 problems solved during the recorded session are archived. Older submissions that were already completed on the account are outside this collection. This is not a claim to preserve every historical submission.

Level 5 consists of four accepted problems, one timed-out attempt and 16 problems without archived solutions. The [failed attempt](level5/attempts/389632/README.md) is excluded from accepted totals. Its analysis separates saved judge outcomes from local comparisons.

The later submissions retain saved 100/100 results; this documentation update did not resubmit them. Twelve restricted-editing exercises distinguish the submitted changes from the complete annotated reference files.
