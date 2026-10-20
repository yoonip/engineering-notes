# AI 배포의 전처리와 특성 순서 | Preprocessing and feature order in model serving

온도·진동·부하 세 숫자를 받는 모델에서 열 순서를 바꾸어도 배열의 크기는 같습니다. 실행은 끝나고 0~1의 점수도 나오지만 판단은 바뀔 수 있습니다. 이 사례는 학습한 모델과 배포 코드 사이의 입력 계약을 검사합니다. 합성 자료로 실제 학습한 작은 분류기를 사용하며, 설비나 기업의 운영 장애를 재현한 기록은 아닙니다.

전체 코드는 [`feature_contract.py`](../예제_examples/실무검증_practical-validation/ai/feature_contract.py)입니다. 잘못된 열 순서·누락된 전처리·요청별 재학습을 같은 입력에 적용하고, 열 이름과 저장한 변환 상태로 해결합니다. 2026-10-21의 관측과 해시는 [AI 실행 기록](검증기록_evidence/AI배포와그룹평가검증_20261021.md)에 있습니다.

## 먼저 고정할 것은 배열 크기보다 넓습니다

자체 예제의 입력은 `temperature_c`, `vibration_mm_s`, `load_pct`입니다. 각각 degC, mm/s, %를 단위로 선언합니다. 학습 자료 160행은 온도 20~90, 진동 0.1~8, 부하 10~100 사이에서 고정 seed로 생성합니다. 정답은 직접 정한 `진동 + 0.02×온도 − 0.015×부하 > 4`입니다. 이 식은 물리적인 불량 기준이 아닙니다.

StandardScaler는 열마다 학습 평균을 빼고 학습 표준편차로 나누는 표준화를 수행합니다. 단위가 다른 입력을 비교 가능한 크기로 바꾸는 과정입니다. 평균 50·표준편차 10인 열에서 70은 `(70−50)/10=2`입니다. 이후 LogisticRegression이 표준화한 세 값의 가중합을 학습합니다. sigmoid는 그 가중합을 0~1로 바꾸며, 이 예제의 class 1 판정 문턱은 0.5입니다.

저장한 계약에는 열 이름·순서·단위, 평균·표준편차, 가중치·절편, class 순서 `[0,1]`, 판정 문턱, 형식 버전이 들어갑니다. 정확히 이 이진 선형 모델을 위한 JSON 형식입니다. 임의 신경망이나 모든 scikit-learn 모델을 같은 구조로 저장할 수 있다는 뜻은 아닙니다.

## 오류 1: 세 숫자의 자리를 바꿉니다

학습 순서는 `[온도, 진동, 부하]`인데 서버가 `[부하, 온도, 진동]`으로 배열을 만들었다고 가정합니다. 세 값 모두 유한한 실수이며 열 수도 3이므로 차원 검사만으로는 거절되지 않습니다. 가중치는 자리에 연결되어 있어 온도를 진동으로 해석하는 순간 다른 식을 계산합니다.

같은 네 요청의 실제 관측은 다음과 같습니다. 아래 값은 합성 분류기의 class 1 점수이며 임상·설비의 보정된 불량 확률은 아닙니다.

| 요청 `(온도, 진동, 부하)` | 정상 Pipeline 점수 | 열 순서 오류 | 전처리 누락 |
| --- | ---: | ---: | ---: |
| `(30, 0.5, 80)` | 0.00008751 | 1.00000000 | 약 0 |
| `(80, 7, 20)` | 0.99993215 | 1.00000000 | 1.00000000 |
| `(45, 3, 60)` | 0.09067039 | 1.00000000 | 0.99893509 |
| `(70, 4.5, 75)` | 0.84554846 | 1.00000000 | 1.00000000 |

열 순서 오류에서는 네 요청 중 두 판정이 바뀌었습니다. 표의 1은 반올림 또는 수치적으로 포화된 점수이지 완벽한 확신의 증거가 아닙니다. 배포 프로그램이 오류를 내지 않고 오히려 극단적인 점수를 내는 실패입니다.

## 해결: 이름으로 읽고 저장한 순서로 배열을 만듭니다

```python
names = bundle["features"]                  # 저장한 열 이름 목록을 가져옵니다.
if set(row) != set(names):                   # set은 중복 없는 집합이며 두 열 집합을 비교합니다.
    raise ValueError("feature set mismatch") # 누락·예상 밖 열이면 계산 전에 중단합니다.
values = [number(row[name]) for name in names] # for로 계약 순서대로 읽고 숫자를 검사합니다.
```

`row`는 열 이름을 key로 갖는 dict입니다. `row.values()`를 그대로 쓰면 삽입 순서에 의존합니다. 수정한 코드는 dict의 키를 반대 순서로 넣어도 같은 점수를 냅니다. `number()`는 bool, 문자열, NaN, 무한대를 거절합니다. Python에서 bool은 int와 관계가 있으므로 `isinstance(value, int)`만으로는 `True`가 들어오는 문제를 놓칠 수 있습니다.

단위도 요청 메타데이터와 저장 계약을 비교합니다. mm/s를 기대하는 모델에 µm/s라고 선언한 요청은 거절합니다. 다만 실제 µm/s 값을 넣고 mm/s라고 잘못 표시하면 이름 검사만으로 알아낼 수 없습니다. 장비의 단위 변환, 원천 자료의 정의와 분포 변화는 이 인터페이스 검사 밖에서도 확인해야 합니다.

## 오류 2: 학습 때 쓴 scaler를 빼먹습니다

학습은 표준화한 입력으로 진행됐는데 배포에서는 원래 온도·진동·부하를 분류기에 직접 전달합니다. 가중치가 적용되는 좌표계가 바뀝니다. 위 표에서 세 번째 요청은 정상 점수 약 0.09067에서 약 0.99894로 바뀌어 class가 반전됐습니다.

해결은 학습 평균·표준편차를 모델 상태와 함께 보존하고, 배포에서도 같은 식을 적용하는 것입니다. 저장한 값을 JSON에서 다시 읽은 뒤 표준 라이브러리만으로 표준화·가중합·sigmoid를 계산했습니다. 네 요청에서 scikit-learn Pipeline과의 최대 절대 차이는 약 `1.39×10⁻¹⁷`이었으며 사전에 둔 허용값 `10⁻¹²`보다 작았습니다. 이는 이 모델의 수치 배선 확인이며 산업 데이터에서의 정확도 검증이 아닙니다.

입력 검사는 모델 상태에도 적용합니다. 0인 scale이나 계수 개수 불일치는 계산 전에 거절합니다. 0으로 나눠 나온 무한대를 점수 0·1로 바꾸어 조용히 반환하지 않습니다. sigmoid는 양수와 음수 분기를 나누어 `exp()`의 큰 지수 계산을 피하지만, 그 전에 가중합이 유한한지도 확인합니다.

## 오류 3: 요청마다 평균과 표준편차를 다시 맞춥니다

`fit_transform()`은 현재 자료로 통계를 새로 계산하고 변환합니다. `transform()`은 이미 학습한 통계를 사용합니다. 두 함수는 단순히 빠르기만 다른 함수가 아닙니다.

네 요청을 한꺼번에 새 scaler로 맞추면 첫 점수는 약 0.00016251입니다. 첫 요청 하나만 새 scaler로 맞추면 각 열의 중심값이 그 요청 자신이 되고, 표준화 결과가 모두 0이 됩니다. 점수는 절편에 의해서만 정해져 약 0.59853463이 됩니다. 같은 요청인데 같이 보낸 다른 요청의 유무로 class가 달라지는 재현입니다.

이 네 요청을 한 묶음으로 재표준화했을 때는 판정 반전이 0개였습니다. 그렇다고 올바른 것은 아닙니다. 점수는 달라졌고 단일 요청 대조에서는 판정도 바뀝니다. 판정 일치만 검사하면 문턱에서 멀리 떨어진 입력의 전처리 오류를 놓칠 수 있으므로 점수의 허용 차이와 요청 묶음 독립성도 확인합니다.

## 재현과 검증 결과

[AI 예제 안내](../예제_examples/실무검증_practical-validation/ai/README.md)의 독립 가상환경에서 실행합니다. 저장소 루트 기준이며 출력 폴더는 매번 새 이름을 사용합니다.

```text
python -B 예제_examples/실무검증_practical-validation/ai/feature_contract.py --out /new/path/feature-contract
```

이번 실행은 Windows, CPython 3.12.14, NumPy 2.5.4, scikit-learn 1.9.1입니다. 일곱 대조 조건이 통과했고 그중 입력 거부 확인은 누락 열·추가 열·NaN·무한대·bool·문자열·실수 범위를 넘는 큰 정수·다른 단위·0 scale·계수 길이의 10가지를 포함합니다. 큰 정수의 실수 변환 오류도 ValueError로 명시적으로 거절합니다. 조건 수와 입력 경우 수를 합쳐 독립 모델 실험 수로 세지 않습니다. 결과 폴더에는 입력·모델 JSON과 원본/오류 점수, 거부 결과, 환경·소스 해시가 남습니다.

실제 서비스에서는 요청 ID·모델 버전·전처리 버전·출력 점수·오류 원인을 연결할 수 있어야 합니다. 모든 원문 입력을 로그에 무조건 남기는 정책은 별도 데이터 권한과 보존 조건이 필요합니다. 이 예제는 직접 만든 숫자만 저장합니다. 모델의 편향·성능·새 설비 분포·처리 지연·동시 요청·보안 경계 전체를 시험하지는 않습니다.

## 확인 문제

1. 배열의 shape이 `(1,3)`으로 같으면 특성 순서도 맞습니까?
2. 네 요청에서 class가 같아도 전처리 구현이 맞다고 결론 내릴 수 있습니까?
3. 한 요청에 `fit_transform()`을 적용하면 학습 평균을 사용하는 것입니까?

답: 1번은 아닙니다. 열의 의미와 단위를 함께 확인해야 합니다. 2번은 아닙니다. 점수·허용 차이·단일/묶음 요청 대조가 필요합니다. 3번은 아닙니다. 현재 요청으로 새 통계를 맞추므로 학습 때의 좌표계가 사라집니다.

## 근거와 연결

- scikit-learn 1.9.1, [Common pitfalls §12.1](https://scikit-learn.org/1.9/common_pitfalls.html#inconsistent-preprocessing), 학습·추론의 변환 일치.
- [StandardScaler](https://scikit-learn.org/1.9/modules/generated/sklearn.preprocessing.StandardScaler.html), 저장한 mean·scale과 transform, 분산의 `ddof=0` 정의. 2026-10-21 열람했습니다.
- [LogisticRegression](https://scikit-learn.org/1.9/modules/generated/sklearn.linear_model.LogisticRegression.html), 계수·절편·class와 예측 API.
- [기존 제조 시계열의 저장 추론](제조시계열의인과경계_causal-trace-validation.md): 모델 입력 경계·저장 상태를 다른 구조에서 확인한 사례입니다.

## English

A trained synthetic binary classifier serves four named requests. Reordered features change two decisions; omitting the scaler changes one. Re-fitting on each request makes the first score depend on whether other requests accompany it. The fixed adapter validates names, declared units and finite JSON numbers, then reuses saved training statistics. A model-specific JSON export matches the scikit-learn pipeline within 1e-12. These are CPU contract checks, not industrial accuracy or load tests.
