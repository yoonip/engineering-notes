# 논문·코드·특허 읽기: 주장과 재현 근거를 연결하기

[Papers, Code & Patents](../README.md) · [digest 예제](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 서로 다른 문서는 서로 다른 질문에 답합니다

논문은 연구 질문·방법·근거·해석을 설명합니다. 코드 저장소는 특정 구현과 실행 입력을 제공할 수 있습니다. 특허 문서는 발명의 공개와 권리의 범위를 살피는 자료입니다. 논문의 표, 최신 코드의 출력, 특허의 청구항이 같은 내용을 증명한다고 가정하면 검토가 꼬입니다.

재현성이라는 말도 정의를 먼저 고릅니다. National Academies의 2019년 보고서는 같은 입력 데이터·계산 절차·코드·분석 조건으로 일관된 결과를 얻는 것을 computational reproducibility로, 같은 질문에 대해 독립적으로 얻은 데이터의 연구들이 일관된 결과를 얻는 것을 replicability로 구분합니다. 분야별 용법은 다를 수 있습니다. 프로그램 한 번이 실행되었다는 사실만으로 독립 실험의 일치까지 입증되지는 않습니다. [National Academies, Chapter 3](https://www.nationalacademies.org/read/25303/chapter/6)

### 주장을 작은 단위로 나누기

“기존 방법보다 좋다”는 말은 비교 대상·입력 범위·지표·환경이 없으면 재현할 수 없습니다. 정확도 향상인지, 지연 감소인지, 에너지 감소인지 나눕니다. 같은 데이터 분할과 전처리, 공통 평가 코드인지도 확인합니다. 학습·평가 데이터가 섞였거나 설정을 평가 결과에 반복 맞췄다면 비교의 의미가 달라집니다.

| 기록할 연결 | 확인할 내용 |
| --- | --- |
| 주장 → 원문 | 절·식·표·페이지, 버전 |
| 원문 → 코드 | commit/tag, 구현 차이 |
| 코드 → 입력 | 데이터 버전·전처리·설정 |
| 입력 → 결과 | 실행 명령·환경·측정 지표·허용 오차 |

원문의 결론과 직접 확인한 결과, 아직 설명되지 않는 차이는 문장 안에서도 구분합니다. 오차 막대와 반복 횟수, 실패한 조건을 읽으면 평균 숫자 하나보다 적용 범위가 잘 보입니다. 실행을 다시 해도 같은 오류가 나올 수 있으므로 재현 가능성과 결론의 타당성도 별도 질문입니다.

### 공개되어 있다는 것과 재사용 허가는 다릅니다

GitHub에서 볼 수 있다는 사실만으로 코드를 원하는 조건으로 배포·수정할 권한이 생기지는 않습니다. 코드, 논문 PDF, 그림, 데이터와 모델 가중치의 조건을 각각 확인합니다. GitHub의 열람·fork 관련 약관상 범위와 일반적인 재배포 허가도 구분합니다. [GitHub 라이선스 안내](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

SPDX 식별자는 어떤 라이선스를 가리키는지 모호함을 줄이는 표준 표기입니다. `AND`와 `OR`도 의미가 다릅니다. 식별자를 붙이는 것만으로 원래 없던 권한이 생기거나, 출처·고지·소스 공개 등 실제 조건이 모두 충족되는 것은 아닙니다. 원문 조건과 파일별 적용 범위를 함께 읽습니다. [SPDX Handling License Info](https://spdx.dev/learn/handling-license-info/)

특허는 관할 지역과 권리 상태, 기간과 청구항을 함께 봅니다. 초록이 기술의 요약이라면 청구항은 보호받으려는 사항을 정의합니다. 공개된 출원과 등록 특허도 구분합니다. 특허가 존재한다는 사실이 그 제품의 성능 검증이나 모든 지역에서의 사용 허가를 뜻하지 않습니다. 공개 내용에서 기술을 이해하는 것과 실제 이용의 법적 조건을 판단하는 것은 별도 검토입니다. [WIPO 특허 FAQ](https://www.wipo.int/en/web/patents/faq_patents)

### 구현과 검증: 바뀐 입력부터 알아보기

예제 `snapshot_digest`는 파일명과 바이트를 묶어 비교합니다. 파일을 읽는 순서만 달라졌을 때는 같고, 내용이 바뀌면 다른 digest가 되는지 점검합니다. 실행 기록에는 소스뿐 아니라 데이터·설정·환경 명세를 넣어야 변경 위치를 찾을 수 있습니다. digest는 진위·권리·실험 품질을 판정하는 값이 아닙니다.

원문 그림을 옮기지 않아도 원래 수치와 조건을 인용하고 직접 계산한 표를 만들 수 있습니다. 이때 표의 출처와 재계산 방법을 남깁니다. 여기의 구현·테스트는 입력 동일성의 작은 모형이며 특정 논문 재현, 특허 유효성, 라이선스 적합성의 심사를 수행한 결과가 아닙니다.

## English

### Different artifacts answer different questions

A paper explains a question, method, evidence, and interpretation. A repository can provide an implementation and execution inputs. A patent discloses an invention and defines requested or granted rights. A paper table, current repository output, and patent claim do not establish the same proposition.

Terminology also matters. The National Academies' 2019 report defines computational reproducibility through consistent results from the same data, computational steps, code, and analysis conditions. Replicability concerns studies answering the same question with independently obtained data. Disciplines can use terms differently. One successful run does not establish agreement between independent experiments. [Chapter 3](https://www.nationalacademies.org/read/25303/chapter/6)

### Make a claim checkable

“Better than prior work” needs a baseline, input scope, metric, and environment. Distinguish accuracy, latency, and energy. Check dataset splits, preprocessing, common evaluation code, and possible leakage or repeated tuning against evaluation outcomes.

Connect claims to exact sections, equations, tables, pages, and versions; papers to code commits and deviations; code to data/preprocessing/configuration; and executions to commands, environment, metrics, and tolerances. Separate the original authors' conclusion, directly observed results, and unexplained differences. Repetition counts, uncertainty, and failure conditions help define scope. A reproducible error remains an error, so reproducibility differs from validity.

### Access is not unrestricted reuse

Public access does not automatically grant arbitrary modification or redistribution. Code, paper figures, datasets, and weights can carry different terms. GitHub viewing/forking permissions also differ from a general redistribution license. [GitHub licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

SPDX identifiers reduce ambiguity about a license; `AND` and `OR` express different combinations. Adding an identifier does not create missing permission or satisfy all notice, source, or attribution obligations. Read actual terms and file scope. [SPDX](https://spdx.dev/learn/handling-license-info/)

For patents, examine territory, legal status, term, and claims, distinguishing a published application from a granted patent. The abstract summarizes technical content; claims define the matter sought to be protected. Patent existence is not performance validation or permission to use the invention everywhere. Technical reading and a real legal-use assessment are separate tasks. [WIPO FAQ](https://www.wipo.int/en/web/patents/faq_patents)

### Implementation and verification

`snapshot_digest` compares names and bytes, remaining invariant to input enumeration order while detecting changes. Include data, configuration, and environment specifications as well as source in a real execution record. A digest establishes neither authenticity, rights, nor study quality.

An original recalculated table can link to source values and conditions without copying a figure; preserve the recalculation method and attribution. These tests model input identity only. They are not a completed replication of a paper or a patent/license determination.

## 출처 / Sources

National Academies의 재현성 정의, SPDX·GitHub의 권리 표기, WIPO의 특허 설명을 각각의 주장 범위 안에서 대조했습니다. / Research reproducibility and artifact rights were checked within their distinct scopes. 확인 / checked: 2026-10-19.
