# 문서 점검 기록 | Document review history

이 문서는 2026-10-19 당시의 점검 기록입니다. 아래 글 수와 실행 수는 그때 확인한 범위이며 현재 목차의 총수를 뜻하지 않습니다. 점검 전 Markdown 1,031개를 대상으로 문서 위치, 본문 유무, 반복 안내문, 코드와 본문의 구분을 살펴봤습니다. 출처·실행 조건·해설이 약한 부분을 아래와 같이 정리했습니다.

## 분류와 본문

| 대상 | 당시 확인한 문제 | 당시 조치 |
| --- | --- | --- |
| 문서 목록 | 공학·언어·인문사회·이력·작성 기준이 한 경로에 섞여 있었습니다. | 학습 분야, 분석, 구현, 작성자 정보, 기여 안내를 나눴습니다. |
| 블로그 운영 | 파일명과 달리 언어·사회·경제 소개였습니다. | 외국어·기술 영어를 독립시키고 사회·경제는 인문사회 본문으로 연결했습니다. |
| 추론과 인문사회 | 시험 추론과 분야 지식의 입구가 하나였습니다. | 언어이해·추리논증의 학습 축과 철학·경제·사회·법의 분야 지식을 별도 목록으로 연결했습니다. |
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

## 기출 분석·영어 기초·대표 논문 추가 점검

앞선 분류 점검에 이어 2026-10-19에 다음 본문을 작성하고 확인했습니다. 제목이 있는지만 세지 않고, 문제 풀이·계산·정답 근거를 실제로 읽을 수 있는지 살폈습니다.

| 대상 | 작성한 내용 | 확인 범위 |
| --- | --- | --- |
| 실제 기출 | 수능 국어 6문항과 LEET 5문항의 지문 구조·선택지별 판단 근거 | 공식 문제·정답의 연도, 문항 번호, 쪽 위치를 대조했습니다. 원문 전체를 복제하지 않고 관계와 판단 근거를 해설했습니다. |
| 영어 기초 | 8단원, 연습 64개와 접어서 보는 정답·해설 | 문장 성분, be·일반동사, 관사, 시제·조동사, 연결 표현을 예제와 함께 확인했습니다. |
| 기사와 연구 읽기 | 직접 만든 두 가지 영어 읽기 자료와 연습 8개 | 주장·조건·비교 기준과 근거가 허용하는 범위를 구분했습니다. 실제 기사나 실험 결과로 소개하지 않았습니다. |
| 대표 논문 | 정보·전자공학 7편, 컴퓨팅·시스템 8편, 신경망 11편, Transformer·GPT-3·CLIP·LoRA 4편 | 원문 서지와 확인 위치, 한국어 개념 설명, 자체 계산, 자기점검과 답을 넣었습니다. 기존 Transformer 해설을 포함해 30편입니다. |
| 모델별 분석 | 짧게 남아 있던 배포물·도구 설명 27개 | 구조·입출력의 의미와 자체 평가 입력·판정표 또는 산술을 추가했습니다. 기존 두 개의 상세 분석과 함께 기관별 목록은 29개입니다. |
| 기초와 평가 | RC 충전, 모델 평가 지표, 기술 용어와 논문 용어 | 단위·가정·분모·행렬 모양과 계산 결과를 대조했습니다. |
| 목차 연결 | 61개 분야의 본문 연결과 주요 학습 경로 | 외국어 읽기 글의 이름과 위치를 정리하고, RC·개발 도구·세부 실습의 찾기 어려운 링크를 연결했습니다. |

[기출 목록](../언어이해와추리논증_reading-reasoning/시험자료_assessments/README.md), [영어 기초](../외국어와기술영어_foreign-languages/영어기초_english-basics/README.md), [논문 해설](../논문해설_papers/README.md), [모델별 분석](../AI모델실험_model-lab/models/README.md)에서 해당 본문으로 들어가실 수 있습니다. 논문은 교육과 후속 연구에 미친 영향을 기준으로 선정했으며 인용 횟수 순위를 산정한 목록은 아닙니다.

수치 예제는 별도 계산과 교차 검토로 확인했습니다. 예를 들어 Amdahl의 추가 비용은 기준 시간으로 나눈 값이어야 하고, LayerNorm과 BatchNorm은 통계를 구하는 축이 다릅니다. CLIP의 한계 절 번호, Moore의 1975년 후속 원문 링크, NVIDIA 카드 안에서 서로 다른 언어 목록도 원문에 맞춰 바로잡았습니다.

이 점검에서는 Markdown 1,139개의 상대 링크·목차 경로 검사와 출처 목록 일치 검사가 통과했습니다. 기존 attention 계산의 다섯 조건도 다시 확인했습니다. 이번 변경의 기준 커밋 `f8a086f`와 비교해 코드·데이터·그림 등 Markdown 이외의 기존 파일 3,699개는 바이트 단위로 같았습니다. 기존 제출 원본과 실행 기록은 보존되어 있습니다.

새 모델 설명의 입력과 기대값은 학습용으로 구성한 자료입니다. 이번 작성 과정에서 공식 가중치 추론·유료 API 호출·이미지나 영상 생성·하드웨어 실측을 추가로 수행하지 않았습니다. 원 논문의 실험 결과, 기존에 실행한 수치 실험, 새로 만든 설명용 계산을 구분했습니다.

## 2026-10-21 분류·표기·출처 점검

모델의 공식 구조·학습 설명은 `models`에 모으고, 직접 구성한 평가 질문과 기존 CPU 계산은 `experiments`로 구분했습니다. DeepSeek R1-Distill과 Samsung TRM도 모델별 문서 아래에서 찾으실 수 있습니다. 회사, 원개발자, 기반 모델, 배포 플랫폼과 실행 도구의 역할을 따로 설명합니다.

제품 목차에서는 양자컴퓨터를 컴퓨팅 장치로, BCI·수술 로봇·광자 계수 CT를 의료기기로 분류했습니다. 글을 옮긴 경로와 관련 목차·출처 링크도 함께 확인했습니다. 질문을 기계적으로 존댓말로 바꾼 제목과 표 항목은 실제 다루는 내용을 나타내는 표현으로 정리했습니다.

계속 늘어나는 목차의 소개에서는 고정된 글 수를 뺐습니다. 논문 표본 수, 실험 입력 수, 날짜가 있는 검증 기록의 수치는 보존했습니다. 출처 JSON의 제목과 독자용 Markdown 출처 목록도 본문의 제목에 맞췄습니다.

공식 모델 카드·설정·API 문서, 논문 서지와 원문 판본, 제품 비교에 쓰인 평가표를 대조했습니다. 원문을 읽은 범위와 등록 서지만 확인한 범위는 구별하며, 접근하지 못한 자료를 확인한 것으로 세지 않았습니다. 제품 평가에는 판본·시점·분모와 평가 주체를 명시하고, 연구 결과와 자체 계산을 나눕니다.

문서 검사는 내부 경로뿐 아니라 제목으로 연결되는 앵커도 확인합니다. 출처 목록의 재생성 검사, Python 구문·JSON 형식 검사와 기존 제출 자료의 무결성 검사를 실행했습니다. 기존 실험·프로젝트의 코드·데이터·그림은 보존했으며, MNIST의 과거 정확도에는 원본 지표 파일과 소스 해시를 연결했습니다. 모든 프로젝트를 재실행하거나 모든 원논문 전문을 다시 읽었다는 뜻은 아닙니다.

## English

The counts in the following paragraphs describe the reviews on October 19, 2026, rather than the current collection size.

The review began with 1,031 Markdown files. Subject categories, model studies, paper calculations, dated technology analysis, executable product observations and readable references now have separate paths. Korean explanatory prose uses a polite register. Existing code, quotations, research facts and recorded measurements are preserved. Local document checks, six CPU numerical tests, attention properties, two SQLite journal observations and the 672-solution archive check were run. This is not a full rerun of every historical experiment or a continuous check of every external URL.

The follow-up adds analyses of 11 actual exam questions, eight English units with 64 exercises, eight additional reading exercises, 30 selected paper studies including the expanded Transformer article, and fuller explanations for 27 model/runtime entries. Local checks pass across 1,139 Markdown files. All 3,699 existing non-Markdown files remain byte-identical to the follow-up baseline. Constructed examples are distinguished from published results and executed experiments.

The October 21 review separates official model descriptions from constructed evaluation designs and existing numerical examples, relocates computing and medical-device reviews, and aligns article titles, indexes and source registries. Growing indexes no longer state a fixed collection size. Source editions, benchmark versions and reading limits remain explicit. Local links and heading anchors, reference generation, Python syntax, JSON format and saved submission integrity were checked. This review does not rerun every project or revalidate every paper in full.
