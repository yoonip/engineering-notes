# 법령의 시간을 데이터로 읽기: 공포일, 시행일과 이력 조회

[분야 목차](../README.md) · [조회 구현](../../../예제_examples/심화_advanced/math_reasoning/models.py) · [경계 검증](../../../예제_examples/심화_advanced/math_reasoning/test_models.py)

## 한국어

### 1. 문서가 공개된 날과 규정이 작동하는 날

법령 자료를 읽을 때 제명만 저장하면 어느 시점의 조문인지 다시 확인하기 어렵습니다. 공포일, 시행일, 개정 이력, 조문별 시행 정보가 함께 있어야 합니다. 문서가 공포된 날과 모든 조항이 시행되는 날은 같다고 가정할 수 없습니다. 미래 시행 예정인 개정본이 공개되어 있어도 현재 조회 목적에 맞는 버전은 종전 본문일 수 있습니다.

[법제처 공동활용 API의 본문 조회 가이드](https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=lsNwInfoGuide)는 법령 ID, 법령 마스터 번호, 공포일자와 조문 시행일자를 구분합니다. [국가법령정보센터의 금융소비자 보호에 관한 법률 2024.8.14 시행본](https://www.law.go.kr/lsInfoP.do?efYd=20240814&lsiSeq=260405)에서도 부칙에 시행일과 적용례·경과조치가 각각 제시되는 구조를 확인할 수 있습니다. 이 글은 특정 분쟁의 법률 결론 대신, 이런 시간 정보를 안전하게 정리하는 계산 문제를 다룹니다.

### 2. 서로 다른 시간 질문을 분리합니다

| 질문 / Question | 필요한 정보 / Information |
| --- | --- |
| 언제 공포되었습니까 | 공포일·공포번호·원문 |
| 어느 날짜에 시행되는 본문입니까 | 법령·조문 시행일과 연혁 |
| 특정 사건에 어느 규정을 적용합니까 | 사실관계·적용례·경과조치·관련 법령·해석 |
| 당시 확인자가 어떤 자료를 보았습니까 | 수집 시점·조회 조건·보관한 응답 |

한 함수가 시행 이력을 골랐다고 해서 마지막 두 질문까지 해결한 것은 아닙니다. 조문마다 시행일이 다를 수 있어, 법령 전체를 단일 시행 구간으로 취급하면 정보가 사라집니다. 구현의 단위는 이미 범위와 식별 체계를 정리한 하나의 조항 또는 규칙입니다. 실제 원문을 수집하는 단계에서는 API의 각 필드와 개정·부칙의 관계를 보존해야 합니다.

### 3. 시간 구간을 수식으로 정의합니다

같은 조항의 시작일을 엄격히 증가하는 $`s_0,s_1,\ldots,s_{n-1}`$로 정렬합니다. 더 뒤의 개정이 앞선 버전을 대체한다는 단순한 이력 모형에서 각 버전 구간은

```math
I_i=[s_i,s_{i+1}),\quad i\lt n-1,
\qquad I_{n-1}=[s_{n-1},\infty).
```

시작일을 포함하고 다음 시작일은 제외하는 반열린 구간입니다. 조회일이 정확히 새 시작일이면 새 버전을 선택합니다. 날짜 $`t`$에 대해

```math
i=\max\{j:s_j\le t\}
```

를 구하면 됩니다. 첫 시작일보다 이르면 해당 이력 안에 버전이 없습니다. 자료가 수집된 시점의 “알려진 정보”까지 함께 재현하려면 시행 시간과 별도로 기록·수집 시간을 갖는 더 풍부한 이력이 필요합니다. 이 간단한 함수는 그 이중 시간 모델을 구현하지 않습니다.

### 4. 이진 탐색으로 구현합니다

`VersionTimeline`은 생성할 때 날짜를 파싱하고 정렬하며 중복 시작일을 거부합니다. 조회에는 `bisect_right`를 사용합니다. 이는 조회일과 같은 시작일들의 오른쪽 경계를 반환하므로, 1을 빼면 가장 최근의 시작일 인덱스가 됩니다. 생성은 $`O(n\log n)`$, 날짜 조회는 $`O(\log n)`$입니다. 반환값은 내부 레코드의 복사여서 호출자가 결과를 수정해도 이력 자체는 바뀌지 않습니다.

예제 레코드 `v1`, `v2`는 날짜 경계 검사를 위해 만든 메타데이터입니다. 실제 법령 번호나 특정 조문의 적용 결과를 뜻하지 않습니다. `v1`은 2024.2.1부터, `v2`는 2025.1.1부터 시작하며 `v2`의 공포일 필드는 2024.11.1입니다. 따라서 2024.12.1에 이 시행 이력을 조회하면 `v1`, 2025.1.1에는 `v2`가 나옵니다.

```bash
python 예제_examples/심화_advanced/math_reasoning/demo.py
```

출력의 `version_on_2024_12_01`에서 공포일만 보고 미래 시행 버전을 선택하지 않는 것을 확인할 수 있습니다. 이 값은 시행 구간을 고르는 조회 결과이고 사건에 적용할 법률관계를 판단한 결과는 아닙니다.

### 5. 검증과 재현성

테스트는 최초 시행 전날, 최초 시행일, 다음 개정 전날과 개정 당일을 검사합니다. 50개 이력을 넣고 361개 날짜에서 단순 선형 탐색의 결과와 이진 탐색을 비교합니다. 같은 시작일의 중복, 빈 입력을 거부하고, 반환 레코드를 바꿔도 원본 이력이 유지되는지 확인합니다.

법령 자료를 실제 연구나 시스템 요구사항에 연결할 때에는 조회 URL, 법령·조문 식별자, 개정 버전, 조회 기준일, 수집 시점을 함께 기록해야 같은 문장을 다시 찾을 수 있습니다. 원본 응답을 별도로 보관하면 API 표시나 현행 버전이 달라져도 비교 기준을 남길 수 있습니다. 날짜 형식은 API의 숫자형 표현을 그대로 연산하지 않고, 정규화 과정에서 달력 날짜로 검증합니다. 이 예제는 ISO 날짜 문자열을 그 내부 표현으로 사용합니다.

공포와 시행의 구분, 조문별 시간, 적용례·경과조치를 함께 읽는 습관은 법률 문서뿐 아니라 표준의 판 번호, 계약의 유효기간, 소프트웨어 요구사항의 변경 이력을 추적할 때에도 도움이 됩니다. 시간 선택과 규범적 판단을 분리하면 계산이 답하는 범위를 분명하게 유지할 수 있습니다.

## English

### 1. Publication and operation are different dates

A statute title alone does not identify which version was read. Promulgation, effective dates, amendment history and provision-level timing matter. A published future amendment need not be the version currently in force for the lookup's purpose. The [Ministry of Government Legislation API guide](https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=lsNwInfoGuide) distinguishes law identifiers, master/version numbers, promulgation and provision effective dates. The [historical Financial Consumer Protection Act version effective August 14, 2024](https://www.law.go.kr/lsInfoP.do?efYd=20240814&lsiSeq=260405) also exposes separate supplementary provisions for commencement, application and transition. This article addresses temporal metadata, rather than resolving a legal dispute.

### 2. Separate the questions

Promulgation asks when an official text was published. An effective-version lookup asks which text begins operating on a date. Applying law to a particular event additionally requires facts, transitional/application provisions, related rules and interpretation. Reconstructing what an observer knew also requires collection time and retained source responses.

One lookup does not answer all four questions. Different provisions may have different commencement dates, so the input unit here is a single already-identified provision or rule. Production ingestion must preserve provision and amendment relationships rather than assigning one simplistic date to an entire statute.

### 3. Interval model and algorithm

For strictly increasing starts $`s_i`$, the simplified successive-replacement model uses half-open intervals $`[s_i,s_{i+1})`$ and a final interval extending forward. A date equal to a new start selects the new version. Compute the largest index with $`s_i\le t`$; dates before the first start have no version in the supplied history. Reconstructing historical knowledge as well as effective time requires an additional recorded-time dimension, not implemented here.

`VersionTimeline` parses and sorts dates and rejects duplicate starts. `bisect_right` returns the position after an equal start; subtracting one locates the desired index. Construction costs $`O(n\log n)`$, lookup $`O(\log n)`$. Results are copied so callers cannot mutate internal records.

The `v1` and `v2` sample records are constructed boundary-test metadata, not real statute identifiers. Their effective starts are February 1, 2024 and January 1, 2025; the second promulgation field is November 1, 2024. Consequently December 1 returns `v1`, while January 1 returns `v2`. The command prints this effective-interval selection, not a conclusion about which law governs a case.

### 4. Verification and traceability

Tests cover the day before initial commencement, both commencement boundaries, the preceding day, duplicate starts and empty input. A 50-version history is checked against a linear oracle across 361 dates. Returned-record mutation must leave the source intact.

Traceable research and requirement work records source URL, provision identity, version, reference date and collection time. Retaining original responses preserves a comparison point when a service or its current version changes. Calendar dates should be validated during normalization instead of treating numeric API dates as ordinary arithmetic; ISO strings are this example's internal format.

The same temporal distinction helps track standards editions, contractual intervals and evolving system requirements. Keeping interval lookup separate from normative application makes clear exactly what the computation establishes.

## 출처 / Sources

법제처의 필드 정의와 국가법령정보센터의 역사적 본문·부칙 구조를 대조했습니다. 예제는 하나의 규칙에 대한 명시적 시간 모형만 구현합니다. / Official metadata definitions and historical-text structure were cross-checked; the example implements only its explicit single-rule timeline model. 확인 / checked: 2026-10-19.
