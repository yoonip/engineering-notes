# 시험 데이터의 식별자와 오판율 / Test identity and classification denominators

두 시험의 합격률이 같다고 같은 제품을 합격시킨 것은 아닙니다. CSV의 같은 행끼리 비교하면 서로 다른 제품을 짝지으면서도 완벽한 일치율을 만들 수 있습니다. 이 사례는 고유 식별자로 시험 결과를 연결한 뒤 수율과 오판율을 구분합니다. 모든 제품·정답 분류는 직접 구성한 합성 자료이며 실제 ATE·SLT·공장 생산품의 기록이 아닙니다. 실행 기준일은 2026-10-21입니다.

## 무엇을 같은 시험으로 볼지 정합니다

ATE는 자동 시험 장비를 사용하는 검사, SLT는 시스템에 가까운 조건에서 수행하는 시험을 가리킵니다. 이름만으로 항목·온도·전압·입력·판정 한계가 같아지지는 않습니다. [NI의 wafer 시험 자료](https://www.ni.com/en/solutions/semiconductor/enterprise-data-management-analytics/reducing-quality-escapes-manufacturing.html)는 die 식별·lot·parametric 값·판정을 연결하는 genealogy를 설명합니다. Genealogy는 한 제품이 거친 단계와 기록의 연결 관계입니다. 이 자료의 상용 솔루션 효과를 아래 합성 예제의 성능으로 옮기지 않습니다.

재현 코드는 [기존 correlation 모듈](../프로젝트_projects/practical-silicon-lab/validation/correlation.py)의 생성·검사 함수를 수정 없이 가져옵니다. 이 모형에서는 CSV마다 serial이 한 번만 등장하고, 두 파일의 serial 집합·lot·온도·전압이 정확히 같아야 비교할 수 있습니다. 실제 재검사 이력은 같은 serial을 지워서 맞추는 대신 test-run ID, 시간, program·firmware 버전 등을 포함한 연결 규칙이 필요합니다.

새 [실행기](../예제_examples/실무검증_practical-validation/chip/run_chip_cases.py)는 같은 CSV 쌍에 잘못된 행 비교와 식별자 비교를 각각 적용합니다. 알고리즘의 차이만 보려는 실험이므로 원본을 정렬해서 한쪽 방법에 유리하게 바꾸지 않습니다. 입력 CSV의 hash도 결과에 남깁니다.

## 네 제품만으로 거짓 일치율을 만듭니다

첫 파일의 제품은 T-0, T-1, T-2, T-3 순서이며 결과는 P, P, F, F입니다. 둘째 파일은 T-2, T-3, T-0, T-1 순서이며 결과가 똑같이 P, P, F, F입니다. P와 F는 이 예제의 완료된 PASS·FAIL 판정입니다.

| 행 | ATE 제품·결과 | SLT 제품·결과 | 행끼리 비교 |
|---|---|---|---|
| 1 | T-0 / P | T-2 / P | 같음 |
| 2 | T-1 / P | T-3 / P | 같음 |
| 3 | T-2 / F | T-0 / F | 같음 |
| 4 | T-3 / F | T-1 / F | 같음 |

```python
for a, s in zip(ate_rows, slt_rows):  # 잘못된 대조: 같은 행이 같은 제품이라고 가정합니다.
    agreement += a['result'] == s['result']  # 문자열 값만 같아도 일치로 셉니다.
```

`zip`은 같은 위치의 원소를 묶습니다. 제품의 정체를 확인하는 함수가 아니며 길이가 다르면 짧은 쪽에서 끝납니다. 위 대조는 4/4=100% 일치라고 보고하지만 네 쌍 모두 serial이 다릅니다. 같은 serial로 연결하면 T-0과 T-1은 P/F, T-2와 T-3은 F/P여서 일치율이 0/4=0%입니다. 두 시험의 합격률은 각각 50%로 같습니다. 합격률·제품별 일치율·정답 대비 정확도가 서로 다른 질문임을 보여 줍니다.

해결은 결과 비교 전에 식별자와 비교 조건을 확인하는 것입니다. `load_unique()`는 빈 ID와 중복 ID를 거부하고, `analyse()`는 키 집합을 대조한 뒤 같은 ID의 행을 비교합니다. 중복이 있는 상태에서 사전을 바로 만들면 나중 행이 앞 행을 덮을 수 있으므로 먼저 중복을 검사합니다. 실제 retest라면 이 모형의 단순 중복 제거 규칙을 그대로 적용해서는 안 됩니다.

## 1,000개 합성 자료에서도 두 계산을 대조합니다

기존 생성기는 ATE와 SLT를 서로 반대 행 순서로 저장합니다. 실행기가 같은 파일을 읽었을 때 제품 ID로 연결한 행렬은 다음과 같습니다.

| ATE / SLT | SLT PASS | SLT FAIL | 합계 |
|---|---:|---:|---:|
| ATE PASS | 900 | 60 | 960 |
| ATE FAIL | 20 | 20 | 40 |
| 합계 | 920 | 80 | 1,000 |

제품별 일치율은 `(900+20)/1000=92%`입니다. 잘못된 행 비교는 `880/1000=88%`를 만듭니다. 1,000쌍 모두 ID가 다른데 숫자 자체는 그럴듯합니다. 따라서 ‘예상했던 90% 근처’라는 감각으로 데이터 연결을 검증할 수 없습니다. 네 제품 예에서는 과대평가, 1,000개 예에서는 과소평가가 나왔으므로 행 비교가 항상 한 방향으로만 틀린다고도 볼 수 없습니다.

이 92%만으로 어느 시험이 더 정확한지는 알 수 없습니다. 불일치 80개에는 ATE가 틀린 경우, SLT가 틀린 경우, 다른 고장을 잡은 경우, 조건이 다른 경우 등이 있을 수 있습니다. 표만으로 ATE PASS·SLT FAIL 60개를 모두 실제 불량으로 분류하지 않습니다.

## 독립 정답이 있을 때만 오판율을 계산합니다

별도의 `truth.csv`에는 합성품 940개를 GOOD, 60개를 BAD로 정한 독립 기준이 있습니다. 이 ‘정답’은 예제 생성 규칙이며 실제 현장의 불량 분석·수명 시험을 대신하지 않습니다. SLT 결과와 이 분류를 연결하면 BAD를 통과시킨 수는 10개, GOOD을 실패시킨 수는 30개입니다.

| 질문 | 분자 / 분모 | 실제 계산 |
|---|---|---|
| SLT 합격률 | 합격품 / 전체 고유품 | 920/1000 = 92% |
| 불량 중 놓친 비율 | BAD이면서 PASS / BAD | 10/60 ≈ 16.67% |
| 양품 중 잘못 거부한 비율 | GOOD이면서 FAIL / GOOD | 30/940 ≈ 3.19% |
| 합격품 속 불량 비율 | BAD이면서 PASS / PASS | 10/920 ≈ 1.087% |

False accept는 불량을 합격으로 받아들인 경우입니다. 위 두 관련 비율은 같은 10개를 세지만 분모가 다릅니다. ‘불량을 얼마나 놓쳤나’에는 BAD 60개를, ‘통과한 묶음 안에 불량이 얼마나 있나’에는 PASS 920개를 사용합니다. 예제의 shipped defective fraction은 SLT 합격품을 출하 집합으로 간주한 모형의 이름이며 실제 출하·고객 고장 관측이 아닙니다.

예제에서 DPPM은 `10/920×1,000,000≈10,869.57`입니다. 이를 오류율 10/60과 섞거나 실제 기업의 품질 수준으로 해석하지 않습니다. 표본 선택과 정답의 신뢰성이 달라지면 해석도 달라집니다. 실제 검사가 반복 측정과 재검사를 포함한다면 제품 수와 시험 횟수의 분모도 따로 둡니다.

## 이상 입력은 비율을 내기 전에 멈춥니다

실행기는 복사한 CSV에 여섯 가지 변경을 하나씩 적용합니다. 중복 ID, 한 제품 누락, 빈 ID, 같은 제품의 전압 조건 변경, TIMEOUT 결과, UNKNOWN 정답 분류입니다. 각각 `ValueError`가 발생해야 확인을 통과합니다. 예상된 거부와 프로그램 자체의 예상 밖 오류를 JSON에서 구별합니다.

여기서 조건은 문자열을 정확히 비교합니다. `0.80`과 `0.8`도 다르게 취급하므로 원자료에 표현 차이가 있으면 이 예제는 비교를 거부할 수 있습니다. 실무에서는 단위와 정밀도를 정한 변환 계층을 두고 원문·정규화 값·변환 버전을 함께 남깁니다. 문자열 비교를 무작정 느슨하게 하여 다른 단위나 다른 전압을 합쳐서는 안 됩니다.

GOOD 한 개가 FAIL인 입력도 실행합니다. BAD는 0개, PASS도 0개라서 두 분모 기반 비율은 계산할 수 없습니다. 보고서는 `null`과 undefined 목록을 남깁니다. 계산 불가를 0%로 바꾸면 검출에 성공했다는 잘못된 의미가 생깁니다. 독립 정답 파일 없이 실행한 보고서에는 false accept 항목 자체를 만들지 않습니다.

[Python 3.12의 csv 문서](https://docs.python.org/3.12/library/csv.html)는 `DictReader`가 열 이름을 키로 읽고 파일을 `newline=''`로 여는 사용법을 설명합니다. CSV 읽기가 성공한 것은 ID의 유일성·단위·시험 완료 여부를 검증했다는 뜻이 아니므로 이 검사는 응용 코드가 수행합니다.

## 실행과 검증 결과

저장소 루트에서 다음 명령을 실행합니다. 기존 결과 경로를 주면 종료 코드 2로 거부합니다.

```shell
python -B 예제_examples/실무검증_practical-validation/chip/run_chip_cases.py --out /new/path/chip-run
```

`correlation/four_parts/`와 `correlation/thousand_parts/`에 실제 사용한 CSV, `serial_join.json`, `wrong_row_zip.json`이 생깁니다. `reject_*` 폴더는 거부 조건을 재현한 입력입니다. 전체 `summary.json`에는 이 파일들의 SHA-256과 비교 결과를 남깁니다. `PASS`는 자료 연결·거부 규칙 등 실행기의 44개 확인이 예상과 일치했다는 뜻입니다. 1,000개 칩의 실물 시험이 통과했다는 뜻이 아닙니다.

2026-10-21 실행에서 44개 확인은 모두 통과했고 기존 offline 19개도 별도로 통과했습니다. 기존 프로젝트 파일 39개의 실행 전후 hash는 같았습니다. [실행 기록](검증기록_evidence/칩모델과시험자료검증_20261021.md)은 환경·보존 범위·미실행 항목을 연결합니다. 실제 데이터에 적용하려면 ID의 생애주기와 재검사 규칙부터 정의해야 합니다.

## 확인 문제

1. 두 시험이 각각 50%를 합격시키면 같은 제품을 합격시켰습니까?
2. 불량 통과 10개에서 10/60과 10/920 중 어느 것이 맞습니까?
3. BAD가 0개일 때 불량 미검출 비율을 0%라고 적어도 됩니까?

<details>
<summary>답과 이유</summary>

1. 알 수 없습니다. 네 제품 예에서 두 합격 집합은 반대이며 제품별 일치율은 0%입니다.
2. 둘 다 다른 질문의 답입니다. 불량 중 미검출은 10/60, 통과 집합 속 불량은 10/920입니다.
3. 안 됩니다. 해당 분모로는 계산할 수 없으므로 이 실행기는 `null`로 기록합니다.

</details>

## English summary

The same four-part CSV fixture produces 100% agreement by row pairing and 0% agreement by serial matching. A separate 1,000-part synthetic dataset distinguishes yield, false acceptance per bad part and defective fraction among passed parts. Missing or duplicate identities and incompatible conditions are rejected before analysis. No physical production data or measured yield is reported.

## 원자료와 읽은 범위

2026-10-21에 NI의 [품질 누락과 die genealogy 설명](https://www.ni.com/en/solutions/semiconductor/enterprise-data-management-analytics/reducing-quality-escapes-manufacturing.html) 본문, Python 3.12 `csv`의 reader·DictReader·newline 설명, 저장소의 correlation 생성·분석·offline 테스트를 읽었습니다. 수치와 CSV 반례는 자체 교육용 실행 결과입니다. 공급사의 수율 향상 주장이나 실제 ATE 처리량을 재현하지 않았습니다.

[함께 읽기: PVT·shmoo와 수율의 분모](../현장계측과검증_measurement-validation/칩과시스템시험_chip-system-testing/조건별오동작과수율의경계_pvt-shmoo-characterization.md)
