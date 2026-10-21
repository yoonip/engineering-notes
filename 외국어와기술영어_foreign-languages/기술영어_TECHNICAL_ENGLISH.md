# 기술 영어의 조건과 주장 | Conditions and claims in technical English

문장을 번역하기 전에 ‘무엇을 어떤 조건에서 주장하는가’를 찾습니다. 아래 문장은 설명을 위해 직접 만든 예시이며 특정 제품의 실제 명세가 아닙니다.

## 조건을 먼저 표시하기

`The device enters sleep mode only if the buffer is empty.`는 장치가 절전 모드에 들어갔다면 버퍼가 비어 있다는 뜻입니다. 절전 진입을 S, 버퍼가 비어 있음을 E로 놓으면 `S → E`입니다. 버퍼가 비어 있다는 사실만으로 절전 진입을 보장하지는 않습니다.

`If the buffer is empty, the device enters sleep mode.`는 `E → S`입니다. 단어가 비슷해도 조건의 방향이 반대입니다. 문장을 읽은 뒤 가능한 반례를 하나 써 보면 방향을 확인하기 쉽습니다. 첫 문장에서는 ‘버퍼가 비어 있지만 장치가 깨어 있음’이 허용됩니다.

| 표현 | 읽는 방법 | 판단 기준 |
| --- | --- | --- |
| if / only if | 충분조건 / 필요조건의 방향을 구분합니다. | 조건에서 결론으로 이어지는 방향 |
| unless | 예외 조건을 먼저 떼어 냅니다. | 예외가 없을 때 적용되는 규칙 |
| at least / at most | 하한 / 상한입니다. | 경계값의 포함 여부 |
| respectively | 앞뒤 항목을 같은 순서로 짝짓습니다. | 나열 순서와 값의 대응 |
| by / to | 변화량과 도달값을 구분합니다. | 증가한 양과 최종값의 차이 |

## 의무와 가능성을 구분하기

규격에서 대문자 `MUST`, `SHOULD`, `MAY`를 쓰는 경우에는 그 문서가 채택한 정의를 따릅니다. [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)는 필수 요구, 정당한 사유가 있으면 벗어날 수 있는 권고, 선택 사항을 구분합니다. [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)는 이 특별한 의미가 대문자 표기에 적용됨을 명확히 합니다. 일반 논문의 소문자 `may`까지 동일한 규범 용어로 읽지는 않습니다.

직접 만든 예시 `Clients MUST reject malformed frames`는 손상된 프레임을 거절해야 한다는 요구입니다. `The method may reduce traffic`은 트래픽 감소의 가능성을 말하며, 모든 입력에서의 보장이나 측정된 감소율을 주지는 않습니다.

## 논문의 한 문장을 표로 풀기

예시 문장 `Under a fixed memory budget, method A reduces average latency by 12% on dataset D compared with B`를 읽을 때는 다음 정보를 남깁니다.

| 항목 | 문장에서 알 수 있는 내용 | 추가로 필요한 정보 |
| --- | --- | --- |
| 조건 | 고정된 메모리 예산 | B도 같은 예산인지, GPU·정밀도·배치·입력 길이가 같은지 여부 |
| 지표 | 평균 지연시간 | p95·p99와 반복 횟수 |
| 비교 | D에서 B 대비 12% 감소 | B의 구현·튜닝 수준과 절대 시간 |
| 범위 | 데이터셋 D | 다른 데이터로 일반화되는지 여부 |

12%라는 숫자만 외우면 조건을 잃습니다. ‘고정 예산·D·평균·B 대비’까지 한 문장으로 다시 말할 수 있어야 결과를 제대로 읽은 것입니다. 이 예시의 12%는 실제 실험값이 아닙니다.

## 10분 연습

1. 공식 문서에서 문장 하나를 고르고 주어·동사·조건을 표시합니다.
2. `only`, `not`, `except`, `at most`처럼 범위를 바꾸는 말을 따로 적습니다.
3. 원문을 덮고 한국어로 뜻을 설명한 뒤, 의미가 달라지는 반례를 만듭니다.
4. 원문과 비교해 빠뜨린 조건만 고칩니다. 번역을 예쁘게 만드는 일보다 뜻을 보존하는 일을 먼저 합니다.

## 수치와 인과 표현을 직접 판별하기

아래도 모두 학습을 위해 만든 문장입니다.

| 문장 | 보존해야 할 의미 | 흔한 오독 |
|---|---|---|
| Latency fell by 20%, to 8 ms. | 20% 감소한 결과가 8 ms입니다. | 20 ms 감소했다고 읽습니다. |
| A is twice as fast as B. | 같은 일을 처리하는 속도가 두 배라는 주장입니다. | 지연시간이 200% 감소했다고 씁니다. |
| The error is no greater than 2%. | 오차가 2% 이하이며 경계 2%를 포함합니다. | 오차가 정확히 2%라고 읽습니다. |
| The effect was not significant. | 문맥의 검정 기준에서 유의하다고 판단하지 않았습니다. | 효과가 없다는 사실을 증명했다고 읽습니다. |
| A is associated with B. | 두 항목의 관련성을 주장합니다. | A가 B의 원인이라고 단정합니다. |

첫 문장에서는 원래 지연시간을 x라 놓으면 `0.8x=8`이므로 x=10 ms입니다. 속도가 두 배라는 둘째 문장은 같은 작업량에서 시간이 절반이 된다고 연결할 수 있습니다. 처리량과 지연시간은 실제 서비스에서 단순한 역수 관계가 아닐 수 있으므로 지표 정의를 확인합니다.

`not all`과 `all ... not`도 구분합니다. `Not all requests succeed`는 적어도 하나의 요청이 실패한다는 뜻이며 모든 요청의 실패를 말하지 않습니다. `Only cached requests are fast`는 빠른 요청이면 캐시된 요청이라는 방향으로 읽습니다. 캐시된 요청이 모두 빠르다는 역방향은 문장만으로 보장되지 않습니다.

## 확인 문제

1. `Power decreased by 25% to 6 W`라면 이전 전력은 얼마인가요?
2. `Not all models passed`에서 모든 모델이 실패했다고 결론 내릴 수 있나요?
3. `The method may improve accuracy`만으로 실제 개선이 측정됐다고 쓸 수 있나요?

<details>
<summary>답과 풀이</summary>

1. 8 W입니다. 6을 0.75로 나눕니다.
2. 그렇게 결론 내릴 수 없습니다. 적어도 하나가 통과하지 못했다는 의미입니다.
3. 측정됐다고 쓸 수 없습니다. 가능성 표현이며 실험 설계·결과를 별도로 확인해야 합니다.

</details>

## English

Read technical sentences as conditions, actions and claims. “S only if E” means S implies E; it does not establish the converse. Standards may define uppercase requirements such as MUST, SHOULD and MAY, while ordinary prose need not use them in that special sense. When reading an experimental claim, retain its budget, dataset, metric and baseline rather than memorizing a percentage alone. All worked sentences and numerical values on this page are constructed examples.
