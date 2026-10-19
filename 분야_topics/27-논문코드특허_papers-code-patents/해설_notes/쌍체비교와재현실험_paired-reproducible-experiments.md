# 재현 실험 설계: 같은 조건에서 차이를 비교하기

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 실행에 성공한 것과 주장을 확인한 것은 다릅니다

논문의 공개 코드가 오류 없이 끝나더라도 핵심 결과를 확인했다고 할 수는 없습니다. 정확도, 지연 시간, 에너지 중 무엇을 비교하는지, 어떤 입력·장치·설정에서 어떤 기준보다 나아졌다는 주장인지를 먼저 고정해야 합니다. 자료를 공개했는지와 다른 사람이 결과를 재현했는지도 다른 질문입니다. ACM SIGIR의 artifact 절차는 available artifact와 reproduced result의 조건을 구분합니다. [ACM SIGIR artifact badging](https://sigir.org/general-information/acm-sigir-artifact-badging/)

여기서는 알고리즘 A와 B의 실행 시간을 같은 입력 묶음에서 비교하는 작은 설계를 다룹니다. 수치는 실제 벤치마크가 아니라 계산 규칙을 보이는 구성 예시입니다. 낮은 값이 좋은 지표라면 B-A의 음수는 B가 더 빠르다는 방향입니다. 정확도처럼 큰 값이 좋은 지표에서는 같은 부호의 의미가 달라집니다.

### 비슷한 조건을 한 쌍으로 묶습니다

A를 아침의 차가운 장비에서, B를 오후의 뜨거운 장비에서만 실행하면 알고리즘 차이와 환경 차이가 섞입니다. 같은 입력·비슷한 시간·같은 device 조건을 한 block으로 묶고 block 안에서 A와 B를 비교합니다. 실행 순서도 AB·BA를 섞어 한쪽만 항상 warm cache의 이익을 얻지 않게 합니다. blocking과 randomization은 다른 역할을 하며 알려진 교란과 남은 교란을 나누어 다룹니다. [NIST randomized block designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm)

쌍체 비교는 단순히 표의 같은 행끼리 빼는 기법이 아닙니다. 어떤 조건 때문에 그 둘이 자연스러운 쌍인지 실험 설계에서 정해져야 합니다. 서로 관계없는 두 표를 편의상 정렬해서 짝지으면 오차 모형이 달라집니다. [NIST paired observations](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm)

### 차이의 평균과 불확실성을 유도합니다

쌍 i의 결과를 $`a_i,b_i`$라 하고 $`d_i=b_i-a_i`$로 둡니다. 쌍 사이 차이가 독립이며 같은 분포에서 왔고 유한 분산을 갖는다는 모형 아래

```math
\bar d=\frac1n\sum_{i=1}^n d_i,\qquad
s_d^2=\frac1{n-1}\sum_{i=1}^n(d_i-\bar d)^2,\qquad
\mathrm{SE}(\bar d)=\frac{s_d}{\sqrt n}.
```

평균의 분산은 독립성 때문에 개별 분산의 합을 $`n^2`$로 나눈 값이 되어 표준오차 식이 나옵니다. 같은 run에서 timer를 1,000번 읽은 값을 독립 1,000회 실험처럼 세면 표준오차를 부당하게 줄일 수 있습니다. autocorrelation이나 장치별 묶임이 있으면 독립 단위부터 다시 정해야 합니다. 표준오차는 표준편차와도 다릅니다.

신뢰구간을 만들려면 표본 크기와 분포 가정에 맞는 절차를 추가해야 합니다. 이 예제는 표준오차만 반환하며 “평균 ±2SE면 항상 95%”라고 주장하지 않습니다. 작은 n, 비대칭 분포, 극단값에서는 특히 조심해야 합니다. 결과를 보고 유리한 조건만 고르는 행위도 단순한 계산 오차와 다른 문제입니다.

### 실행과 독립 검산

`paired_summary()`에 A=[100,200,300,400], B=[102,201,304,403]을 넣으면 차이는 [2,1,4,3], 평균은 2.5입니다. 테스트는 `Fraction`의 유리수 계산으로 평균과 분산을 독립 검산하고 양쪽에 같은 상수를 더해도 차이 통계가 유지되는지 확인합니다. 쌍이 하나뿐이거나 길이가 다르거나 값이 비유한이면 거부합니다. 시간과 공간은 표본 수에 비례합니다.

실험 기록의 재현 단위에는 원본 결과와 제외 기준, 실행 순서, 입력 digest, 코드 revision, 설정·환경·장비, 단위와 통계 절차가 들어갑니다. 실패한 run도 처리 규칙에 따라 남겨야 합니다. 이 예제는 표본 계산의 검증이며 실측 성능 우위, 논문 결과의 재현 성공, artifact badge 취득을 뜻하지 않습니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" experiment
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Successful execution differs from checking a claim

Public code finishing without errors does not by itself reproduce a paper's central result. Define the metric, inputs, equipment, configuration, baseline, and direction of improvement. Artifact availability and independently reproduced results are separate questions in ACM SIGIR's artifact procedure. [ACM SIGIR artifact badging](https://sigir.org/general-information/acm-sigir-artifact-badging/)

This example compares execution times for algorithms A and B on paired inputs. Its numbers are constructed to illustrate calculations, not measured benchmark results. For a lower-is-better metric, negative B-A favors B; the interpretation reverses for higher-is-better metrics such as accuracy.

### Pair comparable conditions

Running A only on a cool machine in the morning and B only on a hot machine later confounds implementation and environment. Blocks can group the same input, nearby time, and device conditions. Mixing AB and BA order prevents one implementation always receiving a warm-cache advantage. Blocking and randomization address different sources of variation. [NIST randomized block designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm)

Pairing requires a meaningful relationship defined by the design, not merely subtracting rows after arbitrarily sorting unrelated tables. [NIST paired observations](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm)

### Derive the mean difference and its uncertainty

For pair i, define $`d_i=b_i-a_i`$. Under independent, identically distributed pair differences with finite variance,

```math
\bar d=\frac1n\sum_{i=1}^n d_i,\qquad
s_d^2=\frac1{n-1}\sum_{i=1}^n(d_i-\bar d)^2,\qquad
\mathrm{SE}(\bar d)=\frac{s_d}{\sqrt n}.
```

Independence makes the variance of the mean the sum of individual variances divided by $`n^2`$, yielding the standard-error expression. Reading a timer 1,000 times within one run does not automatically create 1,000 independent experiments. Autocorrelation and device grouping require reconsidering the independent unit. Standard error differs from sample standard deviation.

A confidence interval needs an additional procedure with appropriate distribution and sample-size assumptions. This example returns standard error and does not claim that mean ±2SE always gives 95% coverage. Small samples, asymmetry, and outliers particularly matter. Selecting favorable conditions after inspecting results introduces a separate selection problem.

### Execution and independent calculation

For A=[100,200,300,400] and B=[102,201,304,403], differences are [2,1,4,3] and mean difference is 2.5. Tests independently compute mean and variance with exact Fraction arithmetic and check invariance under adding the same constant to both measurements. One pair, unequal lengths, and nonfinite data are rejected. Time and storage scale with sample count.

A reproducible record connects raw results and exclusion rules to execution order, input digest, source revision, configurations, environment, equipment, units, and statistical procedure. Failed runs need a predefined handling rule too. These checks establish sample calculations, not measured superiority, successful paper reproduction, or an artifact badge.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" experiment
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [ACM SIGIR: Artifact Badging](https://sigir.org/general-information/acm-sigir-artifact-badging/): 공개 artifact와 결과 재현의 구분 / artifacts versus reproduced results
- [NIST: Randomized block designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm): blocking·randomization
- [NIST: Analysis of paired observations](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm): 쌍체 차이의 통계 / paired-difference statistics
