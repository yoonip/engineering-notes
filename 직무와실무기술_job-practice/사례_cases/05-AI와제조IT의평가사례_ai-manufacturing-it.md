# AI 평가와 제조 IT의 기록 오류 | AI evaluation and manufacturing IT records

[직무 목차](../README.md) · [AI·데이터·제조 IT의 기초](../09-AI데이터와제조IT_ai-data-manufacturing-it.md) · [검사 판정·기록](../11-검사결과의판정과기록_test-decisions-evidence.md)

모델이 실행된다는 사실, 평가 점수가 높다는 사실, 공장 업무의 기록이 맞다는 사실은 서로 다릅니다. 이 글은 scikit-learn의 공식 Python 예제와 PostgreSQL의 공식 SQL 예제를 사용해 전처리 불일치·평가 누출·중복 기록을 분석합니다. 제조 업무에 연결한 상황은 자체 구성이고, 예제의 합성 자료를 실제 반도체 불량 자료로 바꾸어 설명하지 않습니다.

## 직무와 사례의 연결

| 직무·업무 | 맡는 문제 | 연결할 사례 |
| --- | --- | --- |
| AI 개발·AI 시스템·AI/DT | 데이터·모델·실행 환경을 잇고 평가의 의미를 확인합니다. | 학습·운영 전처리 불일치와 특성 선택의 평가 누출입니다. |
| 계측·검사 AI·제품/양산 데이터 분석 | 영상·센서·전기 시험에서 판단에 필요한 자료를 구성합니다. | 점수가 좋아 보이는 이유를 제품·lot·시점·라벨의 경계로 조사합니다. |
| IT·SW 개발·데이터 엔지니어링 | API·DB·이벤트·운영 상태를 일치시킵니다. | 같은 완료 메시지가 두 번 도착해 생산량이 늘어나는 경우입니다. |
| 생산관리·품질·영업/구매 지원 | 집계·추적·출하 판단의 자료가 맞는지 확인합니다. | 최초 실패와 재시험, 실제 제품과 사건의 식별 기준을 구분합니다. |

회사별 실제 요구는 [삼성 DX](../01-삼성DX의직무와요구역량_samsung-dx-role-map.md)·[삼성 DS](../02-삼성DS의직무와요구역량_samsung-ds-role-map.md)·[SK하이닉스](../03-SK하이닉스의직무와요구역량_sk-hynix-role-map.md)의 원문 대응표에 있습니다. 아래 도구의 기능을 설명하는 것과 특정 회사의 채택을 확인하는 것은 구분합니다.

## 1. 학습할 때와 운영할 때 값의 뜻이 달라진 모델

### 업무 상황과 관측 대상

장비 센서에서 후속 품질값을 예측하는 모델을 운영 서버에 옮겼다고 가정합니다. 학습 때에는 센서 값을 평균과 표준편차로 변환했는데 운영에서는 원래 숫자를 그대로 넣으면, 모델이 받는 입력의 뜻이 달라집니다.

표준화는 보통 `z=(x-학습 평균)/학습 표준편차`처럼 숫자의 기준과 크기를 바꾸는 전처리입니다. 예를 들어 원래 숫자 20이 변환 뒤에는 0.5였는데, 모델에 원래 값 20을 주면 전혀 다른 위치의 입력이 됩니다. 이 숫자는 개념 설명용이며 아래 공식 예제의 데이터가 아닙니다.

| 대상·도구 | 관측 항목 | 확인할 이유 |
| --- | --- | --- |
| 센서·영상·시험 결과의 원본 | 값·단위·열 순서·시각·제품·장비 ID입니다. | 입력의 의미가 학습 시점과 같은지 확인합니다. |
| 학습용 PC·운영 서버·edge 장치 | 코드·라이브러리·모델·전처리 판본입니다. | 같은 모델 이름이 같은 계산을 뜻하는지 확인합니다. |
| Python 전처리·평가 코드 | 변환 전후 배열·예측값·오차 분포입니다. | 변환 누락·열 교체·중복 변환을 분리합니다. |
| 운영 로그·기준 입력 묶음 | 동일 입력에 대한 단계별 출력입니다. | 모델 자체의 변경과 전달 경로의 변경을 구별합니다. |

여기서 검사 장비는 모델을 실행하는 PC·서버와 원본 측정 경로입니다. 물리량을 재는 오실로스코프 대신 고정 입력과 단계별 결과를 대조하는 소프트웨어 검사를 수행합니다. 센서 자체의 정확도는 별도 계측 문제입니다.

### 공식 Python 예제의 잘못된 전처리

출처는 scikit-learn 1.7.2의 [Common pitfalls: Inconsistent preprocessing](https://scikit-learn.org/1.7/common_pitfalls.html#inconsistent-preprocessing)입니다. [고정 원문 27–47행](https://github.com/scikit-learn/scikit-learn/blob/25dee604bae18205b01548348388baf7a1cdfe0e/doc/common_pitfalls.rst#L27-L47)의 실행문을 연결했습니다. 프롬프트·문서 출력은 제거하고 한국어 주석을 추가했습니다. 입력은 `make_regression`이 만든 합성 회귀 자료이며 실제 설비 자료가 아닙니다.

```python
from sklearn.datasets import make_regression  # from·import는 모듈에서 합성 회귀 자료 생성 함수를 가져옵니다.
from sklearn.model_selection import train_test_split  # 함수를 가져와 입력과 목표값을 함께 학습·평가용으로 나눕니다.
random_state = 42  # =는 대입이며 난수 선택을 반복할 정수 기준을 저장합니다.
X, y = make_regression(random_state=random_state, n_features=1, noise=1)  # 두 반환값을 X·y에 풀어 담고 특성 하나와 잡음으로 자료를 만듭니다.
X_train, X_test, y_train, y_test = train_test_split(  # 괄호 안 호출을 다음 줄로 이어 쓰며 네 배열을 받습니다.
    X, y, test_size=0.4, random_state=random_state)  # 키워드 인수로 평가 비율과 분할 난수 기준을 정합니다.
from sklearn.metrics import mean_squared_error  # 실제값과 예측값의 제곱 오차 평균을 구하는 함수를 가져옵니다.
from sklearn.linear_model import LinearRegression  # 선형 회귀 모델의 클래스를 가져옵니다.
from sklearn.preprocessing import StandardScaler  # 학습 평균·표준편차로 변환하는 클래스입니다.
scaler = StandardScaler()  # ()로 객체를 만들며 아직 평균·표준편차를 학습하지 않았습니다.
X_train_transformed = scaler.fit_transform(X_train)  # fit_transform은 학습 배열에서 변환 규칙을 구하고 바로 적용합니다.
model = LinearRegression().fit(X_train_transformed, y_train)  # 변환된 입력으로 회귀 객체를 학습하고 model에 저장합니다.
mean_squared_error(y_test, model.predict(X_test))  # 평가 입력을 변환하지 않은 공식 오류 예이며, 계산은 되지만 기준이 다릅니다.
```

`fit`은 자료에서 규칙·계수를 정하는 단계이고 `transform`은 이미 정한 규칙을 적용하는 단계입니다. 이 예에서는 평가 자료의 평균으로 다시 학습하는 것도 정답이 아닙니다. 학습에서 정한 동일한 변환을 평가·운영 자료에 적용해야 합니다.

### 같은 변환과 Pipeline을 적용한 공식 예제

다음은 같은 원문의 [55–56행](https://github.com/scikit-learn/scikit-learn/blob/25dee604bae18205b01548348388baf7a1cdfe0e/doc/common_pitfalls.rst#L55-L56)입니다. 앞에서 학습한 `scaler`와 `model`을 이어 사용합니다.

```python
X_test_transformed = scaler.transform(X_test)  # 학습에서 정한 규칙을 바꾸지 않고 평가 배열에 적용합니다.
mean_squared_error(y_test, model.predict(X_test_transformed))  # 모델이 학습한 좌표계의 입력으로 예측하고 오차를 구합니다.
```

이어지는 [63–69행](https://github.com/scikit-learn/scikit-learn/blob/25dee604bae18205b01548348388baf7a1cdfe0e/doc/common_pitfalls.rst#L63-L69)은 변환과 모델을 Pipeline으로 묶습니다. 아래 실행문은 문서의 별도 대안을 발췌한 것이며, 저자가 새로 추측한 추론 코드는 아닙니다.

```python
from sklearn.pipeline import make_pipeline  # 처리 단계를 순서대로 연결하는 함수를 가져옵니다.
model = make_pipeline(StandardScaler(), LinearRegression())  # 표준화 객체와 회귀 객체를 하나의 파이프라인으로 묶습니다.
model.fit(X_train, y_train)  # 앞 단계의 변환을 학습한 뒤 그 출력으로 모델을 학습합니다.
mean_squared_error(y_test, model.predict(X_test))  # predict가 같은 전처리를 먼저 적용하므로 변환 누락을 줄입니다.
```

### 실행 결과와 업무에서의 해석

공식 문서의 실행문을 추출해 NumPy 2.2.6·scikit-learn 1.7.2로 로컬 실행했습니다. Python 실행과 결과 수집을 위한 비공개 호출은 이 글 작성 중 구성했습니다.

| 실행 흐름 | 로컬 MSE | 해석 |
| --- | --- | --- |
| 변환한 학습 입력·변환하지 않은 평가 입력 | 62.808671 | 같은 회귀 모델이라도 입력 표현이 맞지 않아 오차가 커집니다. |
| 학습 변환을 평가에도 적용 | 0.902798 | 기준을 맞춘 비교입니다. |
| StandardScaler와 회귀 모델을 Pipeline으로 연결 | 0.902798 | 같은 처리 순서를 묶은 대안입니다. |

MSE는 mean squared error, 오차를 제곱한 값의 평균입니다. 이 합성 예제의 목표값 단위에 따른 수치이며 반도체 불량률·수율·센서 오차의 측정값이 아닙니다.

실제 문제를 조사할 때는 다음을 구분합니다.

- 같은 원시 입력에서 학습 환경과 운영 환경의 변환 배열이 다르면 열 순서·단위·결측 처리·전처리 판본을 먼저 비교합니다.
- 변환 배열은 같고 예측값만 다르면 모델 파일·연산 정밀도·실행 backend를 비교합니다.
- 같은 입력의 결과가 일치하지만 새 기간에서 오차가 커지면 입력 분포·제품 구성·측정 경로·라벨 정의의 변화를 조사합니다.

수정 후에는 대표 정상값뿐 아니라 누락·범위 경계·열 순서 오류도 확인해야 합니다. 남길 근거는 원본 입력, 변환된 배열, 모델·전처리의 식별값, 예측·정답, 판정 조건입니다.

## 2. 아무 신호도 없는 자료인데 점수가 높아진 평가

### 평가 누출의 기초

평가 자료는 처음 보는 문제를 얼마나 잘 푸는지 확인하기 위해 남겨 둔 자료입니다. 그 자료의 정답을 보면서 쓸 특성을 고르면, 모델 학습 전에 이미 시험 문제의 답을 참고한 셈이 됩니다. 이를 데이터 누출, leakage라고 합니다.

제조 자료에서는 최종 불량 분석 후에 생긴 항목을 사전 예측 입력으로 넣거나, 같은 웨이퍼의 매우 비슷한 표본을 학습과 평가에 섞는 경우가 관련 문제입니다. 아래 공식 예제는 그중 ‘평가 정답을 사용한 특성 선택’만 보여 줍니다. 제품·시간·lot 분할을 모두 해결하는 프로그램은 아닙니다.

### 누출을 드러내는 공식 코드

출처는 같은 판본의 [특성 선택과 누출 설명](https://scikit-learn.org/1.7/common_pitfalls.html#data-leakage-during-pre-processing)과 [고정 원문 144–176행](https://github.com/scikit-learn/scikit-learn/blob/25dee604bae18205b01548348388baf7a1cdfe0e/doc/common_pitfalls.rst#L144-L176)입니다. 문서 사이의 설명·출력·빈 줄을 제거해 실행문을 연결하고 주석을 붙였습니다. 이 블록은 잘못된 평가를 보여 주는 공식 반례입니다.

```python
import numpy as np  # NumPy를 np라는 짧은 이름으로 불러옵니다.
n_samples, n_features, n_classes = 200, 10000, 2  # 쉼표 대입으로 표본·특성·클래스 수를 정합니다.
rng = np.random.RandomState(42)  # 고정 초기값으로 난수 생성 객체를 만듭니다.
X = rng.standard_normal((n_samples, n_features))  # () 안 튜플은 배열 크기이며 독립 정규 난수 특성을 만듭니다.
y = rng.choice(n_classes, n_samples)  # 특성과 무관하게 두 클래스의 정답을 무작위로 만듭니다.
from sklearn.model_selection import train_test_split  # 입력과 정답을 함께 분할하는 함수를 가져옵니다.
from sklearn.feature_selection import SelectKBest  # 정답과의 통계적 관계로 k개 특성을 고르는 클래스입니다.
from sklearn.ensemble import HistGradientBoostingClassifier  # 여러 단계의 트리를 쌓는 분류 모델 클래스입니다.
from sklearn.metrics import accuracy_score  # 실제 클래스와 예측 클래스가 같은 비율을 구합니다.
X_selected = SelectKBest(k=25).fit_transform(X, y)  # 오류 지점이며, 평가에 쓸 정답까지 본 뒤 25개 특성을 고릅니다.
X_train, X_test, y_train, y_test = train_test_split(  # 선택을 끝낸 자료를 뒤늦게 학습·평가로 나눕니다.
    X_selected, y, random_state=42)  # 평가 행도 특성 선택에 참여했으므로 분할만으로 누출이 없어지지 않습니다.
gbc = HistGradientBoostingClassifier(random_state=1)  # 고정 난수 기준으로 분류 객체를 만듭니다.
gbc.fit(X_train, y_train)  # 분류 모델은 학습 자료만 보지만 앞선 특성 선택의 누출이 남아 있습니다.
y_pred = gbc.predict(X_test)  # 선택된 평가 입력에서 클래스를 예측합니다.
accuracy_score(y_test, y_pred)  # 공식 반례의 정확도를 계산하며 높은 점수가 실제 신호를 뜻하지 않습니다.
```

특성이 10,000개나 있으면 무작위 정답과 우연히 잘 맞는 열도 생깁니다. 전체 정답을 본 뒤 그런 열을 고르면 평가 자료에서의 우연도 선택에 반영됩니다.

### 먼저 분할한 뒤 학습하는 공식 대안

[원문 206–217행](https://github.com/scikit-learn/scikit-learn/blob/25dee604bae18205b01548348388baf7a1cdfe0e/doc/common_pitfalls.rst#L206-L217)의 Pipeline 대안입니다. 위에서 만든 `X`, `y`와 가져온 클래스·함수를 이어 사용합니다. 프롬프트·표시 출력만 제거하고 줄별 주석을 더했습니다.

```python
from sklearn.pipeline import make_pipeline  # 특성 선택과 모델 학습의 순서를 연결합니다.
X_train, X_test, y_train, y_test = train_test_split(  # 원래 입력에서 먼저 학습·평가 경계를 정합니다.
    X, y, random_state=42)  # 평가 정답이 특성 선택에 들어가기 전에 자료를 나눕니다.
pipeline = make_pipeline(SelectKBest(k=25),  # 학습할 때만 특성을 고르는 단계를 앞에 둡니다.
                         HistGradientBoostingClassifier(random_state=1))  # 선택된 입력을 받는 분류 단계를 뒤에 둡니다.
pipeline.fit(X_train, y_train)  # 선택기와 분류기를 학습 자료 안에서 학습합니다.
y_pred = pipeline.predict(X_test)  # 평가 자료는 이미 선택한 열로 변환하고 예측만 수행합니다.
accuracy_score(y_test, y_pred)  # 학습 경계를 지킨 평가 점수를 계산합니다.
```

| 비교 | 공식 문서·로컬 실행 결과 | 읽어야 할 결론 |
| --- | --- | --- |
| 전체 자료로 특성을 고른 뒤 분할 | 정확도 0.76입니다. | 무작위 자료에서도 누출로 점수가 부풀 수 있습니다. |
| 먼저 분할하고 학습 자료로만 선택 | 정확도 0.50입니다. | 이 실행에서는 무작위 정답에 가까운 결과입니다. |
| 먼저 분할한 Pipeline | 정확도 0.50입니다. | 해당 특성 선택의 경계를 묶어 관리합니다. |

0.50이 모든 무작위 실험의 정확한 고정 결과라는 뜻은 아닙니다. 위 자료·난수·모델·분할의 공식 예제를 같은 판본으로 실행한 값입니다. 이 검토에서 실제 결함 영상이나 공장 센서로 AI 모델을 학습하지는 않았습니다.

### 실제 제조 자료에서의 원인 분석

| 높은 점수의 원인 후보 | 확인할 근거 | 수정 후 평가 |
| --- | --- | --- |
| 평가 자료를 본 전처리·특성 선택 | 각 `fit`에 실제로 들어간 행과 정답입니다. | 분할 안에서만 학습하고 전체 선택 과정을 다시 수행합니다. |
| 동일 제품·웨이퍼의 유사 자료 중복 | 제품·lot·wafer·die·이미지 원본 ID입니다. | 목적에 맞는 집단 경계로 분리한 결과를 봅니다. |
| 미래 정보·사후 판정의 입력 혼입 | 각 입력이 실제로 알 수 있었던 시각입니다. | 예측 시점 이전에 확보한 정보로 다시 구성합니다. |
| 정상 비율이 매우 큰 표본 | 정상품·불량품 수와 오탐·미탐입니다. | 정확도 외에 recall·precision·분모·표본 수를 함께 봅니다. |
| 특정 장비·기간만의 특성 | 장비·공정 판본·기간별 오류 분포입니다. | 다른 장비·새 기간에서의 결과를 따로 보고합니다. |

Pipeline은 첫 행의 일부 실수를 줄이는 도구이며, 올바른 제품 ID·시간 경계·정답 정의를 자동으로 찾아주지는 않습니다. 업무의 조치는 모델 교체가 아니라 데이터 구성·분할·라벨·평가 절차의 수정일 수도 있습니다. [생산 묶음 단위 평가](../../설계와검증사례_engineering-cases/생산묶음단위분할과평가누출_ai-group-evaluation.md)와 [기저율·경보 정밀도](../../설계와검증사례_engineering-cases/불량비율과경보의정밀도_ai-prevalence-precision.md)를 이어 읽으실 수 있습니다.

### Python 코드의 출처와 사용 조건

위 Python 코드는 scikit-learn 공식 문서의 예제 실행문입니다. 주석·발췌·여러 대화형 구간의 연결 외에 모델·입력·인수를 변경하지 않았습니다. Copyright (c) 2007–2024 The scikit-learn developers. [BSD 3-Clause 전문](licenses/scikit-learn-1.7.2-COPYING.txt), [고정 판본 원본 라이선스](https://github.com/scikit-learn/scikit-learn/blob/25dee604bae18205b01548348388baf7a1cdfe0e/COPYING)를 제공합니다. 라이브러리의 공식 교육 예제를 특정 회사의 양산 검사 코드로 표시하지 않았습니다.

## 3. 같은 시험 완료 메시지가 두 번 기록되는 제조 IT

### 검사 대상은 물리 제품과 기록의 대응 관계입니다

설비가 시험 완료 메시지를 보낸 뒤 응답을 받지 못해 다시 보냈다고 가정합니다. 수신 서버가 메시지마다 생산량을 더하면 한 번의 시험이 두 번 집계될 수 있습니다. 반대로 제품 ID만으로 중복을 막으면 정상적인 재시험까지 사라질 수 있습니다.

| 관측 대상·도구 | 확인할 항목 | 분석에 필요한 이유 |
| --- | --- | --- |
| 설비·서버 로그와 네트워크 추적 | 송신 시각·재송신·응답·연결 중단입니다. | 실제 시험 반복과 메시지 재전달을 분리합니다. |
| API·메시지 수신 기록 | 사건 ID·실행 ID·제품 ID·본문·처리 결과입니다. | 같은 사건인지, 같은 제품의 새 시험인지 구별합니다. |
| PostgreSQL 등 DB | unique 제약·트랜잭션·삽입/충돌·커밋입니다. | 동시 수신에서 두 번 기록되지 않도록 규칙을 표현합니다. |
| 업무 집계·화면 | 최초 시험·재시험·현재 상태의 분모입니다. | 원시 사건 수와 양품·생산량의 의미를 혼동하지 않게 합니다. |

멱등성은 같은 작업 요청이 반복되어도 의도한 효과가 중복되지 않는 성질입니다. 네트워크 재시도를 없애는 개념이 아니라, 재전달을 예상하고 식별·판정하는 계약입니다. 어떤 키를 사건의 동일성으로 사용할지는 업무에서 정해야 합니다.

### 공식 SQL 코드로 읽는 중복 처리

출처는 PostgreSQL 17.6의 [INSERT Examples 원문 723–724행](https://github.com/postgres/postgres/blob/7885b94dd81b98bbab9ed878680d156df7bf857f/doc/src/sgml/ref/insert.sgml#L723-L724)입니다. 원문은 유통업체 예제이므로 표·열·회사 이름을 그대로 두었습니다. 반도체 설비 테이블처럼 이름을 바꾼 자체 코드를 공식 원문으로 제시하지 않았습니다.

```sql
INSERT INTO distributors (did, dname) VALUES (7, 'Redline GmbH') -- 지정한 두 열에 새 행을 넣으며 괄호 안 값은 열 순서와 대응합니다.
    ON CONFLICT (did) DO NOTHING; -- did의 대응 unique 규칙과 충돌하면 새 행을 넣지 않고 문장을 마칩니다.
```

이 예제에는 `did`의 unique index가 이미 존재한다는 전제가 있습니다. unique는 지정한 키가 중복되는 행을 제한하는 규칙입니다. `ON CONFLICT`만 적고 실제 식별 제약이 없으면 같은 의미가 되지 않습니다. [공식 ON CONFLICT 설명](https://www.postgresql.org/docs/17/sql-insert.html#SQL-ON-CONFLICT)에서 충돌 대상과 원자적 갱신의 범위를 확인할 수 있습니다.

공식 문서에는 [711–713행](https://github.com/postgres/postgres/blob/7885b94dd81b98bbab9ed878680d156df7bf857f/doc/src/sgml/ref/insert.sgml#L711-L713)의 갱신 대안도 있습니다.

```sql
INSERT INTO distributors (did, dname) -- 새 행을 시도할 대상과 열을 정합니다.
    VALUES (5, 'Gizmo Transglobal'), (6, 'Associated Computing, Inc') -- 쉼표로 두 행의 값을 지정합니다.
    ON CONFLICT (did) DO UPDATE SET dname = EXCLUDED.dname; -- 충돌 시 새로 제안한 행의 이름으로 기존 값을 갱신합니다.
```

두 대안은 같은 업무 효과가 아닙니다. 시험 이력에 두 번째 대안을 무조건 적용하면 최초 실패가 나중 PASS로 덮일 수 있습니다. 현재 상태를 갱신하는 표와 각 시도를 보존하는 이력은 목적을 구분해야 합니다.

SQL 실행문은 고정 원문과 같고 줄별 설명 주석만 붙였습니다. Portions Copyright (c) 1996–2025 PostgreSQL Global Development Group; Portions Copyright (c) 1994 The Regents of the University of California. [PostgreSQL 라이선스 전문](licenses/postgresql-17.6-COPYRIGHT.txt), [원본 COPYRIGHT](https://github.com/postgres/postgres/blob/7885b94dd81b98bbab9ed878680d156df7bf857f/COPYRIGHT)를 제공합니다. 이 문서 작업에서는 PostgreSQL 서버에 실행하지 않았습니다.

### 업무의 원인과 복구를 끝까지 확인합니다

다음은 위 원리를 시험 이력에 적용한 자체 진단 계획입니다. 원문의 유통업체 예제가 이런 제조 시스템 전체를 구현한다는 뜻은 아닙니다.

| 확인할 상황 | 올바르게 구별할 결과 | 잘못됐을 때의 원인 후보 |
| --- | --- | --- |
| 같은 사건 ID·같은 본문이 재전달됩니다. | 원시 재전달 이력과 실제 한 번의 업무 반영을 구분합니다. | 사건 식별·중복 처리·동시성 규칙이 빠졌을 수 있습니다. |
| 같은 사건 ID인데 본문이 다릅니다. | 조용히 무시하지 않고 충돌·변경을 조사합니다. | ID 재사용·잘못된 재시도·송신 측 버그가 후보입니다. |
| 같은 제품에 새 시험 실행 ID가 있습니다. | 별도의 시험 시도로 보존합니다. | 제품 ID만을 사건 키로 사용하면 정당한 재시험을 잃을 수 있습니다. |
| 서버 응답 전에 DB 커밋이 끝났습니다. | 재수신 후 기존 기록과 실제 반영 상태를 확인합니다. | 응답 실패를 미처리로 단정하면 두 번 반영할 수 있습니다. |
| DB 기록은 완료인데 설비의 실제 상태가 불명확합니다. | 물리 상태·설비 응답을 별도로 확인합니다. | DB의 원자성을 장치 동작까지 확대해 해석했을 수 있습니다. |

코드 수정 후에는 같은 요청의 동시 도착, 연결 중단 뒤 재전달, 정상 재시험, ID·본문 충돌, 재시작 후 복구를 각각 대조해야 합니다. 집계는 원시 로그의 수·사건 수·제품 수·최초/재시험 결과를 나누어 계산합니다. [시험 데이터의 식별자](../../설계와검증사례_engineering-cases/시험데이터의식별자와오판율_test-data-identity-metrics.md)에서 이어집니다.

이 사례에서 SQL은 기록 규칙을 표현합니다. Python이나 Java 등의 업무 서버는 요청 검증·로그·DB 호출을 연결할 수 있지만, 공개된 제조 API·스키마가 없으므로 회사의 실제 인터페이스를 추측한 C·Python 서버 코드는 만들지 않았습니다.

## 출처와 확인 범위

| 자료 | 이 글에서 확인한 범위 |
| --- | --- |
| scikit-learn 1.7.2 `doc/common_pitfalls.rst` | 전처리 불일치, 데이터 누출, Pipeline의 공식 실행문과 결과입니다. 고정 commit은 `25dee604bae18205b01548348388baf7a1cdfe0e`입니다. |
| 로컬 실행 | 위 공식 실행문을 추출해 Python에서 실행했습니다. NumPy 2.2.6·SciPy 1.15.3·scikit-learn 1.7.2를 사용했고 실제 공장 자료·설비는 사용하지 않았습니다. |
| PostgreSQL 17.6 `doc/src/sgml/ref/insert.sgml` | `ON CONFLICT` 설명·unique 전제·Examples의 SQL과 사용 조건을 읽었습니다. 고정 commit은 `7885b94dd81b98bbab9ed878680d156df7bf857f`입니다. |
| 자체 구성 | 제조 센서·품질 예측의 업무 맥락, 누출 원인 비교표, 시험 이벤트 진단·재평가 계획입니다. 해당 기업에서 실제 발생한 장애라고 제시하지 않았습니다. |

출처 확인과 로컬 실행 기준일은 2026-10-26입니다.

## English

The cases use official scikit-learn examples to explain preprocessing mismatch and feature-selection leakage, followed by PostgreSQL's official conflict-handling examples for event records. Synthetic ML scores, local reruns, source SQL and hypothetical manufacturing diagnosis are kept separate. The SQL was inspected, not executed against a PostgreSQL server, and no company-internal manufacturing API was invented.
