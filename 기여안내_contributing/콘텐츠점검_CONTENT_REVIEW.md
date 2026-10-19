# 콘텐츠와 분류 점검 | Content and navigation review

확인일은 2026-10-19입니다. 점검 전 Markdown 1,031개를 대상으로 문서 위치, 본문 유무, 반복 안내문, 코드와 본문의 구분을 살펴봤습니다. 출처·실행 조건·해설이 약한 부분을 아래와 같이 정리했습니다.

## 분류와 본문

| 대상 | 확인한 문제 | 현재 구성 |
| --- | --- | --- |
| 문서 목록 | 공학·언어·인문사회·이력·작성 기준이 한 경로에 섞여 있었습니다. | 학습 분야, 분석, 구현, 작성자 정보, 기여 안내를 나눴습니다. |
| 블로그 운영 | 파일명과 달리 언어·사회·경제 소개였습니다. | 언어 학습을 독립시키고 사회·경제는 인문사회 본문으로 연결했습니다. |
| 추론과 인문사회 | 시험 추론과 분야 지식의 입구가 하나였습니다. | 추론·시험과 철학·경제·사회·법을 별도 목록으로 나눴습니다. |
| 양식 | 실제 지원 기록·평가 지표·RC 예제·설계 설명이 양식으로 분류되어 있었습니다. | 각각 소개·리뷰·공학 기초·기여 안내로 옮겼습니다. |
| AI 모델 | 기관 목록에 비해 배포물 분석이 적고 실험 코드가 없었습니다. | 29개 기관의 대표 모델·서비스·도구 분석과 CPU 실험 4종을 연결했습니다. |
| 논문 읽기 | 방법 설명에 비해 개별 논문의 계산 사례가 적었습니다. | attention 수치 계산과 부분곱 실험 분석을 추가했습니다. |
| 기술 현황·제품 | 개념 해설과 날짜가 있는 현황·제품 동작이 구분되지 않았습니다. | MLPerf v6.1 분석과 SQLite 실행 리뷰를 독립된 목차에 넣었습니다. |
| 출처 | JSON 링크만 열려 읽기 어려웠습니다. | 글별 Markdown 출처 4개와 자동 생성·검사 도구를 연결했습니다. |
| 그림과 표 | 독자 목차에 편집 기준이 함께 있었습니다. | 기여 안내로 옮기고, 그림 24개의 읽기용 목록을 만들었습니다. |

철학·경제·사회·법과 추론의 첫 화면에는 실제 판단과 계산 예시를 추가했습니다. 본문이 이미 있는 분야는 기존 수식과 구현을 유지하며 연결과 문체를 정리했습니다. 제목이나 목록만 늘리는 방식으로 새 분야를 만들지는 않았습니다.

## 문체와 기록 보존

한국어 설명의 평서형·질문형·청유형을 존댓말이나 자연스러운 명사형으로 정리했습니다. 앞으로의 글에도 같은 기준을 적용하도록 [작성 기준](../AGENTS.md)에 남겼습니다. 코드와 원문 인용, 제출 당시의 주석, 실험 수치와 연구 이력은 문체 수정 때문에 바꾸지 않았습니다.

학습용 글의 존댓말과 별개로 제출 원본은 당시의 기록입니다. 프로그래머스 정답 672개의 소스와 채점 정보는 별도 무결성 검사로 확인했습니다. 새 채점을 실행했다는 뜻은 아닙니다.

## 실행과 검사

| 확인 | 방법 | 범위 |
| --- | --- | --- |
| 문서 경로 | `python 기여안내_contributing/tools/check_documents.py` | Markdown 상대 링크와 분야·출처 데이터의 문서 경로 |
| 출처 목록 | `python 기여안내_contributing/tools/build_reference_pages.py --check` | JSON과 Markdown 목록의 일치, 해설 132개 연결 기록 |
| 모델 계산 | `python -m unittest discover -s AI모델실험_model-lab/experiments -p "test_*.py" -v` | CPU 수치 검사 6개 통과 |
| attention | `python 논문해설_papers/attention_calculation.py` | 비율·닫힌 형태·causal mask 등 조건 5개 확인 |
| SQLite | `python 제품리뷰_reviews/sqlite_concurrency.py` | DELETE와 WAL 두 모드의 트랜잭션 관찰값 확인 |
| 부분곱 분석 | [사례의 재현 명령](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/부분곱실험의주장과근거_partial-product-reproduction-case.md) | INT6·k=2 입력 4,096쌍의 두 구현 일치 |
| 정답 기록 | `python programmers/tests/verify_archive.py` | 정답 672개와 주석 사본·원본 해시 확인 |

외부 문서는 AI 배포물과 새 분석의 핵심 근거를 공식 자료로 확인했습니다. 저장소의 모든 외부 URL을 실시간으로 검사하거나 기존 연구의 모든 실험을 재실행한 기록은 아닙니다. 모델 실험은 작은 수치 예제이며 공식 가중치 추론이나 GPU 벤치마크를 포함하지 않습니다.

## English

The review began with 1,031 Markdown files. Subject categories, model studies, paper calculations, dated technology analysis, executable product observations and readable references now have separate paths. Korean explanatory prose uses a polite register. Existing code, quotations, research facts and recorded measurements are preserved. Local document checks, six CPU numerical tests, attention properties, two SQLite journal observations and the 672-solution archive check were run. This is not a full rerun of every historical experiment or a continuous check of every external URL.
