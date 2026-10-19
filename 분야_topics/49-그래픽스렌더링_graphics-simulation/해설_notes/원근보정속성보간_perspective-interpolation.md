# 원근 투영 뒤에도 표면의 속성을 맞추는 보간

[보간 구현](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [실행 CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 화면의 절반이 표면의 절반은 아닙니다

멀리 있는 물체는 작게 보입니다. 그래서 화면에서 삼각형의 꼭짓점 두 개 사이 중간을 택했다고 실제 표면에서도 두 점의 중간을 택한 것은 아닙니다. Texture 좌표를 화면의 비율로 곧바로 섞으면 바닥 무늬가 삼각형 경계를 따라 휘거나 움직이는 것처럼 보일 수 있습니다.

Perspective-correct interpolation은 투영으로 달라진 비율을 되돌려 표면 위의 속성을 계산합니다. 여기서는 clipping이 끝난 비퇴화 삼각형 내부의 한 점, 양의 clip w, 꼭짓점에 주어진 scalar 속성을 다룹니다. 벡터 속성은 성분마다 같은 식을 적용합니다. 속성이 원래 삼각형의 barycentric 좌표에 대해 선형이라는 전제도 필요합니다. [OpenGL 4.6 Core section 14.6](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

## 두 종류의 barycentric 좌표

삼각형 안의 점을 꼭짓점들의 가중합으로 적는 비율을 barycentric 좌표라 합니다. 세 가중치 합이 1이고 모두 0 이상이면 삼각형 내부 또는 경계의 점입니다. 원래 표면의 비율을 $`\alpha_i`$, 투영된 화면의 비율을 $`\lambda_i`$로 구분하겠습니다. 두 좌표는 같은 점을 표현하지만 서로 다른 공간의 비율입니다.

꼭짓점의 clip 좌표를 $`P_i=(X_i,Y_i,Z_i,w_i)`$라 하겠습니다. 원래 삼각형의 선형 결합은 $`P=\sum_i\alpha_iP_i`$이며, 화면 좌표는 homogeneous division으로 X/w, Y/w를 사용합니다.

```math
x=\frac{\sum_i\alpha_iX_i}{\sum_i\alpha_iw_i}
=\sum_i\frac{\alpha_iw_i}{\sum_j\alpha_jw_j}\frac{X_i}{w_i}.
```

y도 같은 꼴이므로 화면의 barycentric 좌표는

```math
\lambda_i=\frac{\alpha_iw_i}{\sum_j\alpha_jw_j}.
```

이 식을 α에 대해 풀면 각각 λ/w에 비례합니다. 합이 1이라는 조건으로 비례상수를 정하면

```math
\alpha_i=
\frac{\lambda_i/w_i}{\sum_j\lambda_j/w_j}.
```

처음에는 복잡해 보이지만 원리는 “화면 비율을 w로 나눈 뒤 다시 합이 1이 되게 만든다”입니다.

## 속성 보간식은 왜 분수입니까

속성 f가 원래 표면에서 선형이면 $`f=\sum_i\alpha_i f_i`$입니다. 방금 구한 α를 대입하면 원근 보정식이 나옵니다.

```math
f=
\frac{\sum_i\lambda_i f_i/w_i}{\sum_i\lambda_i/w_i}.
```

따라서 f/w와 1/w를 화면에서 각각 선형 보간하고 마지막에 나눕니다. $`\sum_i\lambda_i f_i`$는 화면 공간의 affine 보간이며 w가 다르면 일반적으로 다른 값입니다. `noperspective`는 이 화면 공간 보간을 선택하는 별도 규약입니다. `flat`은 보간 대신 정해진 꼭짓점의 값을 사용합니다. 어느 속성에 어떤 규약을 쓰는지도 렌더링 계약에 포함됩니다. [OpenGL interpolation 식과 qualifier](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

## 작은 숫자로 독립 검증하기

3차원 꼭짓점을 A=(0,0,1), B=(2,0,2), C=(0,4,4)로 놓고 pinhole 투영 $`(x,y)=(X/Z,Y/Z)`$를 사용하겠습니다. Clip w를 Z로 선택하면 화면 꼭짓점은 (0,0), (1,0), (0,1)입니다. 화면 점 (1/4,1/4)의 화면 비율은 $`\lambda=(1/2,1/4,1/4)`$입니다.

속성을 A=0, B=1, C=0으로 정하면 화면 보간은 1/4입니다. 원근 보정은

```math
f=\frac{(1/4)/2}{(1/2)/1+(1/4)/2+(1/4)/4}
=\frac{2}{11}\approx0.181818.
```

검증 기준을 같은 보간식에서 다시 만들면 구현 실수를 놓칠 수 있습니다. 대신 카메라 광선과 원래 3D 삼각형을 교차합니다. 이 화면 점으로 향하는 광선은 $`Q=t(1/4,1/4,1)`$입니다. $`Q=\alpha_AA+\alpha_BB+\alpha_CC`$의 X,Y 성분을 비교하면 $`\alpha_B=t/8`$, $`\alpha_C=t/16`$입니다. Z 성분과 합이 1인 조건은

```math
t=1+\alpha_B+3\alpha_C
=1+\frac{5t}{16},\qquad
t=\frac{16}{11},\qquad \alpha_B=\frac{2}{11}.
```

속성은 B에만 1을 주었으므로 바로 $`f=\alpha_B=2/11`$입니다. 투영 뒤의 분수식을 쓰지 않고 얻은 3D 기하 기준과 일치합니다.

## 구현과 경계 조건

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" raster
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

구현은 세 λ, 세 f, 세 양의 w를 받아 분자와 분모를 계산합니다. λ의 합과 비음수 조건을 검사하고, 내부 비율 계산에 O(1) 시간과 공간을 씁니다. CLI는 affine=0.25와 perspective≈0.181818을 출력합니다. 테스트는 위 광선 교차에서 구한 2/11과 비교하며 다음 성질도 확인합니다.

| 조건 | 기대 결과 |
|---|---|
| 세 w가 같습니다 | 보통의 affine 보간과 같습니다 |
| λ가 한 꼭짓점에 1입니다 | 그 꼭짓점의 f를 그대로 얻습니다 |
| 모든 w를 같은 양수 배율로 바꿉니다 | 분자·분모의 배율이 상쇄되어 결과가 같습니다 |

삼각형이 화면에서 퇴화하면 화면 λ 자체를 안정적으로 구할 수 없습니다. w가 0에 가까우면 투영의 수치 민감도가 커지며, 뒤쪽 점을 포함한 삼각형을 이 함수 하나로 처리할 수 없습니다. 실제 파이프라인에서는 near plane 등의 clipping을 먼저 적용하고 새 꼭짓점의 속성도 그 단계의 규약에 맞게 보간합니다.

이 함수는 coverage 판정, top-left 경계 소유 규칙, multisampling, clipping, texture filtering을 구현하지 않습니다. 픽셀 중심·경계 포함 규칙은 API와 버전의 계약입니다. 예를 들어 [Microsoft의 Direct3D 9 rasterization 규칙](https://learn.microsoft.com/en-us/windows/win32/direct3d9/rasterization-rules)은 해당 API의 화면 좌표와 coverage를 설명합니다. 그것을 모든 API의 픽셀 중심 규칙으로 옮겨 쓰면 안 됩니다.

일반적인 window depth 보간에는 이미 원근 나눗셈과 깊이 변환이 반영된 별도 규칙이 있습니다. 이 글의 일반 varying 보정식을 depth buffer 값에 다시 기계적으로 적용하지 않습니다. 보간한 normal 역시 길이가 1이라는 보장은 없어 shading에서 정규화가 필요할 수 있습니다. 정확한 작은 수치 모델은 이 구분을 이해하는 도구이며 전체 renderer의 정확성이나 GPU 성능을 검증한 결과는 아닙니다.

## English

### A screen midpoint is not a surface midpoint

Distant objects appear smaller. A midpoint between projected vertices therefore need not correspond to the midpoint on the original surface. Direct screen-space interpolation of texture coordinates can distort a pattern across triangles.

Perspective-correct interpolation recovers the surface proportions changed by projection. This model covers a nondegenerate, already-clipped triangle, a point inside it, positive clip w and one scalar vertex attribute. Vectors use the same expression per component. The attribute must be linear in the original triangle's barycentric coordinates. [OpenGL 4.6 Core section 14.6](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf) supplies the rasterization reference.

### Derive two coordinate systems

Barycentric coordinates express a point as a weighted sum of triangle vertices. Weights sum to one and are nonnegative inside or on its edges. Let α denote the original surface weights and λ denote the projected screen weights.

For clip vertices $`P_i=(X_i,Y_i,Z_i,w_i)`$, their linear combination is $`P=\sum_i\alpha_iP_i`$. Homogeneous division gives x as $`(\sum_i\alpha_iX_i)/(\sum_i\alpha_iw_i)`$. Rewriting this as a weighted sum of projected vertex coordinates shows $`\lambda_i=\alpha_iw_i/(\sum_j\alpha_jw_j)`$. The same relation holds for y.

Solving for α makes each weight proportional to λ/w. Normalizing their sum gives $`\alpha_i=(\lambda_i/w_i)/(\sum_j\lambda_j/w_j)`$. In plain terms, divide the screen proportions by w and normalize again.

For an attribute linear on the surface, substituting α into $`f=\sum_i\alpha_i f_i`$ yields the rational formula above. Interpolate f/w and 1/w linearly in screen space, then divide. Directly interpolating f with λ is instead affine screen-space interpolation; it differs when w values differ. `noperspective` selects that screen-space behavior, while `flat` uses a designated vertex rather than interpolating. These qualifiers are part of the rendering contract. [OpenGL interpolation rules](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

### Check with an independent ray intersection

Use 3D vertices A=(0,0,1), B=(2,0,2), C=(0,4,4) and pinhole projection (X/Z,Y/Z), with clip w=Z. Screen vertices become (0,0), (1,0), (0,1). At screen point (1/4,1/4), λ=(1/2,1/4,1/4). Give attribute values zero, one and zero. Affine interpolation returns 1/4; perspective correction returns 2/11, approximately 0.181818.

An independent reference intersects the original 3D triangle with ray $`Q=t(1/4,1/4,1)`$. Comparing X and Y gives αB=t/8 and αC=t/16. The Z component and unit weight sum give $`t=1+\alpha_B+3\alpha_C=1+5t/16`$, so t=16/11 and αB=2/11. Only B has attribute one, so f=2/11. This geometry obtains the answer without reusing the interpolation formula under test.

### Executed implementation and scope

The CLI prints affine 0.25 and perspective approximately 0.181818. The function checks three weights summing to one, nonnegativity and positive w, and evaluates a constant-size numerator and denominator in O(1) time and space. Tests compare against the independent ray result. Equal w must recover affine interpolation; a vertex weight of one must recover its exact attribute; scaling all w by the same positive factor must leave the result unchanged.

A degenerate projected triangle prevents stable construction of λ. Near-zero w makes projection sensitive, and triangles crossing behind the camera require clipping before this function. New clipping vertices also need attribute treatment consistent with that stage.

Coverage, edge ownership, multisampling, clipping and texture filtering are outside this implementation. Pixel-center and coverage rules depend on the API and version: [Microsoft's Direct3D 9 rasterization rules](https://learn.microsoft.com/en-us/windows/win32/direct3d9/rasterization-rules) describe that API, not a universal convention.

Window depth follows its own interpolation rule after perspective division and depth transformation; do not mechanically apply the generic varying correction a second time to depth-buffer values. Interpolated normals may require renormalization for shading. This small numerical model explains these distinctions; it does not validate an entire renderer or measure GPU performance.

## 출처 / Sources

- [Khronos, OpenGL 4.6 Core Specification section 14.6](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf): perspective interpolation, affine `noperspective`, flat attributes and depth rules.
- [Microsoft, Direct3D 9 Rasterization Rules](https://learn.microsoft.com/en-us/windows/win32/direct3d9/rasterization-rules): screen-space triangle coverage and API-specific sampling conventions. 확인 / checked: 2026-10-19.
