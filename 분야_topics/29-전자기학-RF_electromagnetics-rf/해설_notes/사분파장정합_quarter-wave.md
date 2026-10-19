# 사분파장 정합: 선로 길이로 임피던스 바꾸기

[전자기학·RF 목차](../README.md) · [전송선 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 저항을 넣지 않고도 다른 저항처럼 보이게 한다

50 Ω 선로 끝에 100 Ω 부하를 바로 연결하면 반사가 생긴다. 중간에 알맞은 특성임피던스와 길이의 선로를 넣으면 입력에서는 50 Ω처럼 보이게 만들 수 있다. 부하가 실제로 바뀐 것은 아니다. 진행파와 반사파가 선로를 따라 더해지는 위상이 달라져 입력의 전압·전류 비율이 바뀐 것이다. 물리적 길이가 신호 파장의 1/4일 때 식이 특히 간단해진다.

[University of Kansas의 quarter-wave 강의](https://www.ittc.ku.edu/~jstiles/723/handouts/section_5_4_The_Quarter_Wave_Transformer_present.pdf)는 무손실 선로의 임피던스 변환을 유도한다. [Ansys의 quarter-wave transformer 예](https://optics.ansys.com/hc/en-us/articles/360042041094-Quarter-wave-impedance-transformer)는 실제 형상과 수치 전자기 해석 사이의 관계를 보여 준다. 여기의 실행 코드는 그 형상 해석이 아니라 이상적인 선로 식이다.

### 경계조건에서 입력 임피던스까지

특성임피던스 $`Z_t`$가 양의 실수이고, 전기적 길이가 $`\theta=\beta l`$인 균일·무손실 선로를 가정한다. 부하를 향해 흐르는 전류를 양으로 잡으면 전송선 ABCD 관계는 다음과 같다.

```math
\begin{bmatrix}V_{in}\\I_{in}\end{bmatrix}
=\begin{bmatrix}\cos\theta&jZ_t\sin\theta\\
j\sin\theta/Z_t&\cos\theta\end{bmatrix}
\begin{bmatrix}V_L\\I_L\end{bmatrix}.
```

$`V_L=Z_LI_L`$를 넣고 입력 전압을 입력 전류로 나누면 얻는다.

```math
Z_{in}=Z_t\frac{Z_L\cos\theta+jZ_t\sin\theta}
{Z_t\cos\theta+jZ_L\sin\theta}.
```

이 형태는 tanθ를 직접 계산하는 식보다 θ=π/2 부근에서 다루기 편하다. 사분파장에서는 cosθ=0, sinθ=1이므로 $`Z_{in}=Z_t^2/Z_L`$다. 부하가 양의 실수 RL이고 입력을 기준 저항 R0와 맞추려면 다음을 고른다.

```math
Z_t=\sqrt{R_0R_L},\qquad l=\lambda/4.
```

R0=50 Ω, RL=100 Ω이면 Zt≈70.71 Ω다. 반파장 θ=π에서는 다시 Zin=ZL가 된다. 사분파장 변환을 두 번 적용해도 원래 부하로 돌아온다. 이런 특수 경우는 구현을 검산하는 좋은 독립 기준이다.

### 정합과 손실을 혼동하지 않기

입력 반사계수는 기준 R0에서 $`\Gamma_{in}=(Z_{in}-R_0)/(Z_{in}+R_0)`$다. 중심 주파수에서 Γ가 0이어도 중간의 각 경계에 반사가 전혀 없다는 뜻은 아니다. 왕복 위상을 거친 여러 반사파의 합이 입력에서 상쇄된다. 손실 없는 정합에서는 반사되지 않은 전력이 부하로 가지만, 손실이 있는 구조에서는 작은 S11만으로 효율이 높다고 말할 수 없다.

| 조건 | 결과 |
|---|---|
| θ=π/2, 양의 실수 부하 | 제곱/부하 임피던스 변환 |
| θ=π | 원래 부하가 입력에 반복됨 |
| 주파수 변경 | 전기적 길이와 반사계수 변경 |
| 복소 부하 | 단순 기하평균 Zt만으로 실수 정합 불충분 |

비분산 근사에서 길이를 고정하면 θ는 주파수에 비례한다. 따라서 한 설계 주파수 부근의 정합을 broadband 정합으로 확대하면 안 된다. 홀수 사분파장에서도 이상적인 같은 변환이 반복될 수 있으며, 중심 주파수 외에 정합점이 절대 없다는 식의 표현도 피한다.

### 실행과 실제 RF 검증

```bash
python demo.py --case rf
python -m unittest -v test_models.HardwareModels.test_quarter_and_half_wave test_models.HardwareModels.test_line_passivity_and_quarter_involution
```

코드는 quarter·half-wave 해석값, 사분파장 두 번의 원상복구, 양의 실수부를 가진 수동 부하의 $`|\Gamma|\le1`$을 확인한다. 실물 microstrip에서는 유효 유전율, 유전체·도체 손실, dispersion, 두께와 폭 공차, 불연속 연결을 포함해 길이와 Zt를 정한다. VNA는 calibration과 de-embedding 후 같은 기준면에서 비교해야 한다. 이 예제는 Python 이상 선로 계산이며 Ansys 실행이나 S-parameter 측정 결과는 아니다.

## English

### Changing the apparent impedance with a line

A 100 Ω load attached directly to a 50 Ω line reflects energy. A suitably chosen line section can make that load appear as 50 Ω at its input. The load itself is unchanged; propagation changes the phase relationship between voltage and current waves. A quarter wavelength produces a particularly simple transformation.

[The University of Kansas lecture](https://www.ittc.ku.edu/~jstiles/723/handouts/section_5_4_The_Quarter_Wave_Transformer_present.pdf) derives the lossless result. [Ansys's transformer example](https://optics.ansys.com/hc/en-us/articles/360042041094-Quarter-wave-impedance-transformer) connects the idea with a physical electromagnetic model. The executable example here evaluates ideal line equations rather than that geometry simulation.

### Derivation and special cases

Assume a uniform lossless line with positive real characteristic impedance Zt and electrical length θ=βl. With current directed toward the load, use the displayed ABCD relation. Substituting VL=ZL IL gives the sine/cosine input-impedance formula above. It avoids directly evaluating tanθ near π/2.

At θ=π/2 the cosine terms vanish, giving $`Z_{in}=Z_t^2/Z_L`$. A positive real load RL is matched to real reference R0 by choosing $`Z_t=\sqrt{R_0R_L}`$. For 50 Ω and 100 Ω this is approximately 70.71 Ω. At θ=π the input repeats the original load. Applying the quarter-wave transformation twice also returns the original load. These independent limits are useful implementation checks.

### Matching, bandwidth and loss

The input reflection coefficient is $`(Z_{in}-R_0)/(Z_{in}+R_0)`$. Zero input reflection does not imply absence of reflections at the internal boundaries: multiple reflected waves cancel at the input after propagation. A lossless matched network delivers incident power to the load, but low S11 in a lossy physical structure does not by itself establish high efficiency.

Changing frequency changes electrical length and the input match. A complex load is generally not matched by the simple real geometric-mean choice alone. With a fixed length and nondispersive propagation, electrical length scales with frequency; this is not inherently broadband matching. Odd quarter wavelengths can repeat the same ideal transformation, so the design frequency need not be the only possible match at all frequencies.

### Executable and physical checks

Run the commands above. Tests compare quarter- and half-wave values with analytic results, apply the quarter-wave transform twice and check $`|\Gamma|\le1`$ for passive loads with positive real part. A physical microstrip additionally needs effective permittivity, dielectric and conductor losses, dispersion, geometry tolerances and junction discontinuities. Compare VNA data only after suitable calibration and reference-plane de-embedding. The example is Python ideal-line calculation, not an Ansys run or an S-parameter measurement.

## 출처 / Sources

- University of Kansas, Jim Stiles, *The Quarter-Wave Transformer*: transformation, multiple reflections and matching limitations.
- Ansys, *Quarter-wave impedance transformer*: geometry-based simulation context. Links appear above.
