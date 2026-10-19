# 좌표 변환에서 pixel까지: 동차 좌표와 rasterization

## 같은 점도 좌표계가 바뀌면 숫자가 달라집니다

물체의 꼭짓점을 저장한 좌표계와 카메라의 좌표계, 화면의 pixel 좌표계는 서로 다릅니다. 그래픽 pipeline은 이 사이를 옮기면서 3차원 장면을 화면 표본으로 바꿉니다. 숫자가 맞아 보여도 좌표계 방향과 행렬 곱 순서가 다르면 다른 위치가 나옵니다. 이 글은 열벡터를 오른쪽에 두는 표기를 사용합니다.

강체 변환은 회전 $`R`$과 이동 $`t`$를 이용한 $`p'=Rp+t`$입니다. 이동은 원래 3×3 선형 변환만으로 표현되지 않지만 점 뒤에 1을 붙이면

$$\begin{bmatrix}p'\\1\end{bmatrix}
=T\begin{bmatrix}p\\1\end{bmatrix},\qquad
T=\begin{bmatrix}R&t\\0&1\end{bmatrix}.$$

이 4×4 동차 행렬로 회전과 이동을 합성할 수 있습니다. $`R^TR=I`$, $`\det R=1`$인 회전이면 역변환은 $`T^{-1}=[R^T,-R^Tt;0,1]`$입니다. 프레임 변환에서 $`T_{ab}T_{bc}=T_{ac}`$처럼 중간 좌표계를 지우며 생각할 수 있습니다. 곱셈은 일반적으로 교환되지 않습니다. [Northwestern Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/)

동차 좌표는 0이 아닌 공통 배율을 허용합니다. $`(x_h,y_h,z_h,w_h)`$에서 $`w_h\ne0`$이면 직교 좌표는 $`(x_h/w_h,y_h/w_h,z_h/w_h)`$입니다. 강체 변환을 거친 점은 $`w=1`$을 유지하지만 투영 뒤에는 그렇지 않습니다. 방향 벡터를 $`w=0`$으로 표현하면 이동 항이 적용되지 않습니다. 예제 함수는 유한한 “점”을 처리하므로 $`w=0`$ 결과는 거부합니다.

## 투영, clipping, viewport

Model은 물체에서 세계로, view는 세계에서 카메라로, projection은 카메라에서 clip 좌표로 바꾼다고 두면

$$p_{clip}=PVMp_{object}.$$

투영 후 $`w_{clip}`$로 나누어 normalized device coordinates를 얻습니다. 이어 viewport가 이를 화면 좌표로 옮깁니다. Clipping은 나눗셈 전에 보이는 영역과 primitive를 처리하는 단계입니다. OpenGL 사양은 clip 좌표의 perspective division, viewport, rasterization의 순서를 구분합니다. API에 따라 깊이 범위와 원점 방향이 달라질 수 있으므로 이 글의 pinhole 계산을 특정 API의 projection matrix와 그대로 동일시하지 않습니다. [OpenGL 4.6 §§13.7–13.8](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

원근감의 핵심은 깊이로 나눈다는 점입니다. 같은 길이의 물체도 멀어지면 화면에서 작아집니다. 기하학 검증에서는 역변환으로 원래 점을 복원하는지, 같은 광선 위 점들이 같은 영상 위치로 가는지, near plane 주변에서 무엇을 clip하는지 각각 따로 확인합니다.

## 삼각형 안을 표본으로 채우기

Rasterization은 삼각형 같은 primitive를 화면 표본과 연결합니다. 화면의 점 $`p`$를 삼각형 꼭짓점 $`a,b,c`$의 가중 합으로 쓰면

$$p=\lambda_a a+\lambda_b b+\lambda_c c,
\qquad\lambda_a+\lambda_b+\lambda_c=1.$$

퇴화하지 않은 삼각형에서는 signed area 비율로 계수를 구할 수 있습니다. 예를 들어 $`\lambda_a=\mathrm{cross}(b-p,c-p)/\mathrm{cross}(b-a,c-a)`$입니다. 나머지도 순환시켜 얻습니다. 모든 계수가 음이 아니면 삼각형 내부 또는 경계입니다. $`a=(0,0),b=(2,0),c=(0,2),p=(0.5,0.5)`$의 계수는 ((0.5,0.25,0.25))입니다.

실제 rasterizer는 pixel center나 multisample 위치를 검사합니다. 공유 edge를 양쪽 삼각형이 중복해서 채우지 않도록 경계 소유 규칙이 필요합니다. 예제는 계수만 계산하며 top-left rule이나 완전한 rasterizer를 구현하지 않습니다. [OpenGL §14.6](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

원근 투영 뒤의 일반적인 속성 $`f`$를 화면 계수로 보간할 때는 clip $`w_i`$를 포함합니다.

$$f=\frac{\sum_i\lambda_i f_i/w_i}{\sum_i\lambda_i/w_i}.$$

화면의 선형 거리와 물체 표면의 선형 거리가 같지 않기 때문입니다. 모든 $`w_i`$가 같으면 보통의 선형 보간으로 줄어듭니다. 반면 window depth나 `noperspective`, `flat` 속성은 각각의 API 규칙을 따릅니다. 모든 속성에 위 식을 무조건 적용하지 않습니다.

## 구현과 검증

[`transform_point`, `barycentric`](../../../예제_examples/확장기초_extended/ai_data/models.py)은 행렬 변환과 삼각형 계수를 계산합니다. [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 90도 회전·이동과 해석적 역행렬의 왕복, 알려진 삼각형의 계수, 그 계수로 점을 재구성하는 성질, 외부 점의 음수 계수를 확인합니다. 이 검증은 좌표·보간의 계산 검증이며 GPU rasterizer와 pixel 단위로 같은 렌더링 결과를 보장하지 않습니다. 퇴화 삼각형, clip 경계, edge 소유, 깊이 비교와 수치 허용 오차는 실제 renderer의 추가 검증 대상입니다.

## English

### Coordinates depend on their frame

Object vertices, camera coordinates and screen pixels use different frames. Rendering moves between them before sampling a scene. This article uses column vectors multiplied on the right; coordinate conventions and multiplication order are part of correctness.

A rigid transform $`p'=Rp+t`$ becomes a 4×4 matrix by appending a one to each point. For a proper orthogonal rotation, its inverse uses $`R^T`$ and $`-R^Tt`$. Composition follows $`T_{ab}T_{bc}=T_{ac}`$ and is generally not commutative. [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/)

Nonzero common scaling preserves a homogeneous point. Homogeneous coordinates represent a finite point by dividing the first components by nonzero $`w`$. Rigid point transforms preserve $`w=1`$, whereas projection need not. Directions use $`w=0`$ so translation has no effect. The example handles finite points and rejects a zero output $`w`$.

### Projection and clipping

With model, view and projection matrices, $`p_{clip}=PVMp_{object}`$. Clipping acts before division by clip $`w`$; perspective division produces normalized device coordinates, then the viewport maps them to the window. OpenGL specifies these stages separately. Depth ranges and origin conventions vary by API, so a pinhole formula is not automatically a particular API's projection matrix. [OpenGL §§13.7–13.8](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

Division by depth creates perspective: the same physical size appears smaller farther away. Independent geometric checks include inverse-transform recovery, equal projections along one ray and explicit behavior at clipping boundaries.

### Triangle sampling and interpolation

Barycentric coordinates express $`p=\sum\lambda_i v_i`$ with coefficients summing to one. Signed area ratios compute them for a nondegenerate triangle. The example triangle and point above give ((0.5,0.25,0.25)); nonnegative coefficients identify its closed interior. Rasterizers evaluate pixel centers or multisample locations and need an ownership rule so adjacent triangles do not both fill a shared edge. The example computes coefficients only and implements neither a top-left rule nor a complete rasterizer. [OpenGL §14.6](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

General perspective-correct interpolation uses the ratio involving $`f_i/w_i`$ and $`1/w_i`$. Screen-linear distance is not surface-linear distance. Equal $`w_i`$ reduces the expression to ordinary affine interpolation. Window depth and `noperspective` or `flat` attributes follow their own API rules rather than blindly using this formula.

### Implementation and checks

The linked functions transform finite points and calculate triangle coordinates. Tests apply a 90-degree rotation and translation followed by their independently written analytic inverse, verify known barycentric values, reconstruct the point and identify an outside point through a negative coefficient. These establish geometric arithmetic, not pixel-identical behavior with a hardware rasterizer. Degenerate triangles, clipping, shared-edge ownership, depth comparisons and numerical tolerances remain additional renderer-level checks.

## Sources

- [Northwestern University, Modern Robotics §3.3.1](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/): rigid homogeneous transforms and composition.
- [Khronos, OpenGL 4.6 Core Specification §§13.7–13.8, 14.6](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf): clipping/division/viewport ordering, triangle coverage and interpolation. Reference date: 2026-10-19.
