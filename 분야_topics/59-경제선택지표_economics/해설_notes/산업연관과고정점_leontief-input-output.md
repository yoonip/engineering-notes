# 산업 간 연결을 행렬로 읽기: 투입산출 모형과 고정점

[분야 목차](../README.md) · [계산 구현](../../../예제_examples/심화_advanced/math_reasoning/models.py) · [검증](../../../예제_examples/심화_advanced/math_reasoning/test_models.py)

## 한국어

### 1. 한 산업의 생산에는 다른 산업의 생산이 들어간다

컴퓨터 생산에는 반도체·전력·운송 같은 중간 투입이 필요하고, 이 산업들도 다시 다른 생산물을 사용한다. 최종 수요 하나의 변화가 여러 공급 단계를 거치는 모습을 투입산출 모형으로 나타낼 수 있다. 중요한 점은 모든 거래 금액을 합한 총산출과 중간 거래를 제외한 부가가치를 구분하는 것이다. 총산출의 파급 배율을 GDP나 순편익의 배율로 곧바로 읽으면 중복 계산을 만들 수 있다.

[미국 BEA의 RIMS II 안내서, §2·p. 2–10](https://www.bea.gov/sites/default/files/methodologies/RIMSII_User_Guide.pdf)와 [BEA Input–Output Accounts 방법론](https://www.bea.gov/resources/methodologies/concepts-methods-io-accounts)을 기준으로 직접 필요량·총 필요량의 구분을 확인했다. 예제의 두 산업은 계산을 위해 만든 집계이며 실제 국가 산업표를 추정한 자료가 아니다.

### 2. 계수의 행과 열을 먼저 정한다

$`a_{ij}`$는 산업 $`j`$의 산출 한 단위를 만들 때 산업 $`i`$에서 필요한 투입량이다. 즉 열 $`j`$가 그 산업의 투입 구성을 나타낸다. 산출 벡터를 $`x`$, 최종 수요를 $`d`$라고 하면 산업 $`i`$의 생산은 중간 수요와 최종 수요의 합이다.

```math
x_i=\sum_j a_{ij}x_j+d_i,
\qquad x=Ax+d.
```

금액 기반 계수라면 같은 평가 기준과 가격 시점의 산출·투입을 사용해야 한다. 국내 투입과 수입을 어디에 포함하는지도 모형의 경계를 바꾼다. 서로 다른 정의의 산업표에서 숫자만 가져와 같은 행렬에 섞으면 안 된다.

### 3. 역행렬과 반복 계산은 같은 균형을 찾는다

식을 정리하면 $`(I-A)x=d`$다. 역행렬이 존재할 때 $`x=(I-A)^{-1}d`$로 쓸 수 있지만, 구현에서 역행렬을 직접 만들 필요는 없다. 여기서는 $`x^{(0)}=0`$에서 반복한다.

```math
x^{(1)}=d,\quad x^{(2)}=d+Ad,\quad
x^{(3)}=d+Ad+A^2d,
\qquad x^{(r+1)}=Ax^{(r)}+d.
```

일반적인 Neumann 급수의 수렴 조건은 $`\rho(A)\lt1`$다. 이 구현은 더 쉽게 확인할 수 있는 충분조건 $`q=\Vert A\Vert_\infty=\max_i\sum_j a_{ij}\lt1`$을 요구한다. 행합이 1 이상이라고 모든 투입산출 모형이 틀렸다는 뜻은 아니다. 이 코드가 보증할 수 있는 입력 범위를 제한한 것이다. 비음수 계수와 수요에서 각 반복은 음이 아닌 산출을 만든다.

### 4. 언제 멈춰도 되는지 오차 상계를 구한다

현재 계산값 $`\hat x`$의 잔차를 $`r=\hat x-A\hat x-d`$라 하자. 정확한 평형값 $`x^*`$와의 차이는 $`(I-A)(\hat x-x^*)=r`$다. $`\Vert A\Vert_\infty=q\lt1`$이면

```math
\Vert(I-A)^{-1}\Vert_\infty
\le\sum_{j=0}^{\infty}\Vert A\Vert_\infty^j
=\frac1{1-q},\qquad
\Vert\hat x-x^*\Vert_\infty\le\frac{\Vert r\Vert_\infty}{1-q}.
```

따라서 두 반복값이 비슷하다는 느낌 대신, 잔차로 계산한 상계가 허용값 아래인지 확인하고 멈춘다. 이는 명시한 선형계 안의 수치오차 상계다. 계수의 추정 오차나 산업 모형이 현실과 다른 정도까지 포함하는 구간은 아니다. 부동소수점 계산에서는 상계 자체의 반올림 오차도 고려해야 한다.

### 5. 실행 예와 독립 확인

```math
A=\begin{bmatrix}0.2&0.1\\0.3&0.2\end{bmatrix},
\qquad d=\begin{bmatrix}70\\50\end{bmatrix}.
```

이 예의 정확한 균형은 $`x=(100,100)^T`$다. 첫 산업은 중간 수요 30과 최종 수요 70, 둘째 산업은 중간 수요 50과 최종 수요 50을 채운다. `leontief_fixed_point`는 반복 횟수와 잔차 기반 상계도 반환한다. 기본 허용값에서 29회 계산하며 결과는 약 $`(99.99999999997,99.99999999995)`$다.

```bash
python 예제_examples/심화_advanced/math_reasoning/demo.py
```

테스트는 정확한 유리수 2×2 풀이와 독립 비교하고, 실제 오차가 계산된 상계 안에 있는지 확인한다. 투입이 0이면 산출이 최종 수요와 같은 경우, 행합 조건 위반, 반복 한도 내 미수렴도 검사한다. 희소한 산업 연결을 쓰면 한 반복은 연결 수에 비례해 구현할 수 있지만, 이 작은 구현은 밀집 행렬이라 반복당 $`O(n^2)`$다.

### 6. 경제적 해석의 범위

고정 계수는 수요가 바뀌어도 같은 생산 방식과 가격 비율이 유지된다고 가정한다. 재고·여유 생산능력·가격 반응·대체재·수입 누출·지역 경계가 달라지면 결과 해석도 달라진다. 계산된 산출 증가를 그대로 순고용 증가나 사회적 편익으로 바꾸지 않는다. 여기서 중요한 것은 연결 구조를 명시하고, 결과가 어떤 균형식과 가정에서 나왔는지 되짚을 수 있게 하는 것이다.

## English

### 1. Production depends on production

A computer industry purchases intermediate inputs, whose suppliers purchase further inputs. Input–output models express these linked rounds. Gross output includes intermediate transactions and must be distinguished from value added; an output multiplier is not automatically a GDP or net-benefit multiplier. The definitions of direct and total requirements were checked against [BEA RIMS II, §2 and p. 2–10](https://www.bea.gov/sites/default/files/methodologies/RIMSII_User_Guide.pdf) and the [BEA I–O methodology](https://www.bea.gov/resources/methodologies/concepts-methods-io-accounts). The two-sector numbers are constructed for calculation, not estimated national accounts.

### 2. Orientation and equilibrium

$`a_{ij}`$ is input from sector $`i`$ per unit output of sector $`j`$, so column $`j`$ describes its input composition. Intermediate plus final demand gives $`x_i=\sum_j a_{ij}x_j+d_i`$, hence $`x=Ax+d`$. Monetary tables require consistent valuation and price dates; treatment of domestic inputs, imports and regional boundaries must also match.

Rearranging yields $`(I-A)x=d`$. Starting at zero, the fixed-point iteration generates $`d`$, $`d+Ad`$, $`d+Ad+A^2d`$ and subsequent rounds. The general Neumann-series condition is $`\rho(A)\lt1`$. This implementation enforces the simpler sufficient condition $`q=\Vert A\Vert_\infty\lt1`$ for a nonnegative matrix. A row sum above one does not invalidate every I–O model; it lies outside this implementation's guaranteed input class. Nonnegative data keep iterates nonnegative.

### 3. A residual certificate

For residual $`r=\hat x-A\hat x-d`$, the equilibrium error satisfies $`(I-A)(\hat x-x^*)=r`$. Submultiplicativity and the geometric series give $`\Vert(I-A)^{-1}\Vert_\infty\le1/(1-q)`$, so error is bounded by $`\Vert r\Vert_\infty/(1-q)`$. The runner stops when this bound reaches tolerance. It addresses numerical error in the stated model, not coefficient uncertainty or model discrepancy; floating-point evaluation also rounds the certificate.

### 4. Execution and interpretation

For the matrix and demand shown above, exact gross output is $`(100,100)^T`$: intermediate demands are 30 and 50, and final demands are 70 and 50. `leontief_fixed_point` returns output, iteration count and the residual certificate. The default run takes 29 iterations and approaches the exact values as shown in Korean. Tests compare with a rational 2×2 inverse calculation, verify the certificate, and exercise zero coefficients, invalid contraction bounds and iteration exhaustion. Dense work is $`O(n^2)`$ per iteration; a sparse implementation could instead scale with the number of connections.

Fixed coefficients assume unchanged production technology and relevant price ratios. Inventories, capacity limits, substitution, imports and regional boundaries affect interpretation. Gross-output changes are not automatically net employment or social welfare changes. The useful result is a traceable calculation linking explicit accounting assumptions to a computed equilibrium.

## 출처 / Sources

직접·총 필요량과 산출·부가가치의 구분은 BEA 자료로 확인했다. 반복식·오차 상계는 이 글의 행렬 조건에서 유도하고 유리수 해로 검증했다. / BEA sources support the accounting interpretation; iteration and error bounds are derived for the explicit contraction condition and checked with rational arithmetic. 확인 / checked: 2026-10-19.
