# 역매핑과 쌍선형 보간 / Inverse mapping and bilinear interpolation

[계산 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 좌표 변환과 영상의 값은 다른 계산입니다

카메라·좌표 변환으로 목적지 pixel이 원본의 어디를 볼지 정했어도 원본 좌표가 2.4, 1.7처럼 정수가 아닐 수 있습니다. 원본 배열에는 이 좌표의 값이 직접 저장되어 있지 않습니다. Resampling은 이웃 표본으로 그 값을 추정합니다. Bilinear interpolation은 x·y 방향의 선형 보간을 결합하는 방법입니다.

예제의 영상은 단일 channel 실수 배열이며 pixel 중심은 정수 좌표 $`(x,y)`$입니다. Array index는 `image[y][x]`로 둡니다. 정수 중심 규약과 배열 순서를 먼저 고정해야 전치·반 pixel 오차를 구분할 수 있습니다. OpenCV도 기하 변환에서 좌표 매핑과 interpolation을 나누어 설명합니다. [OpenCV geometric transforms](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html)

## 한 축을 보간하고 다른 축을 보간합니다

$`i=\lfloor x\rfloor`$, $`j=\lfloor y\rfloor`$, $`a=x-i`$, $`b=y-j`$라 하면 a,b는 0~1 범위의 비율입니다. 위 행과 아래 행의 수평 보간은 각각

```math
r_0=(1-a)I_{j,i}+aI_{j,i+1},\qquad
r_1=(1-a)I_{j+1,i}+aI_{j+1,i+1}.
```

두 행의 값을 다시 수직 보간하면

```math
I(x,y)=(1-b)r_0+br_1
=\sum_{u=0}^1\sum_{v=0}^1
w_x(u)w_y(v)I_{j+v,i+u}.
```

네 가중치는 음이 아니며 합이 1입니다. 네 이웃 값이 모두 같은 c면 결과도 c이고, 범위 안의 네 값 사이를 벗어나지 않습니다. 다만 경계 밖을 0으로 채우면 원래 영상의 최솟값보다 작아질 수 있습니다. 그 경우 네 이웃에 이미 경계값 0이 포함되어 있다는 뜻입니다.

이 보간은 각 축에 대해 1차이며 2차원 전체에서 반드시 affine 함수인 것은 아닙니다. 반면 원본 값이 $`I(x,y)=ux+vy+c`$인 평면이면 내부에서 그 값을 정확히 재현합니다. 이것이 테스트의 독립 oracle입니다. 예를 들어 $`2x+3y+5`$를 저장한 영상의 소수 좌표 결과를 식에 직접 대입해 비교합니다.

## 역매핑으로 출력 픽셀의 원본 위치 찾기

원본 pixel을 목적지로 하나씩 보내는 forward mapping은 반올림 뒤 일부 목적지가 비거나 여러 원본이 겹칠 수 있습니다. Inverse mapping은 출력 pixel마다 원본의 연속 좌표를 구해 값을 하나씩 채웁니다.

```math
\begin{bmatrix}x_s\\y_s\end{bmatrix}
=
\begin{bmatrix}a_{00}&a_{01}&a_{02}\\a_{10}&a_{11}&a_{12}\end{bmatrix}
\begin{bmatrix}x_d\\y_d\\1\end{bmatrix}.
```

코드의 `inverse_map`은 이미 목적지→원본 방향의 행렬입니다. 원본을 오른쪽으로 반 pixel 이동해 보이게 하려면 목적지 x에서 원본의 x-0.5를 읽습니다. 변환 방향과 물체가 화면에서 움직이는 방향의 부호가 반대라는 점을 유도하면 외워서 바꾸는 일을 줄일 수 있습니다. OpenCV의 `remap`도 목적지 위치에서 원본 좌표를 지정합니다.

## 라이브러리 좌표를 맞추는 법

PyTorch `grid_sample`은 기본적으로 -1~1 정규화 좌표를 받으며 `align_corners`가 의미를 바꿉니다. 이 예제의 정수 pixel 중심 x와 연결하면 `align_corners=False`에서 정규화 값은 $`u=2(x+1/2)/W-1`$입니다. True이며 W>1일 때는 $`u=2x/(W-1)-1`$입니다. 같은 u라도 설정이 다르면 같은 원본 위치가 아닙니다. [PyTorch grid_sample](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.grid_sample.html)

코드는 정규화 grid를 받지 않고 직접 pixel 좌표를 사용합니다. 경계는 constant 0이며 clamp·reflection을 쓰지 않습니다. 영상 [10] 하나를 x=-0.25,y=0에서 읽으면 내부 값 10의 가중치가 0.75라 결과는 7.5입니다. 좌표가 밖에 있다는 이유로 결과 전체를 즉시 0으로 만드는 정책과 다릅니다.

## 실행과 검증

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" warp
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

CLI는 $`I[y,x]=10y+x`$인 5×4 입력을 실제 resampling합니다. 역매핑에 x-0.5,y-0.25를 사용하므로 내부의 출력 (1,1)은 원본 (0.5,0.75)의 값 8입니다. JSON에는 입력, 변환, 출력 배열 전체가 있어 경계와 내부를 비교할 수 있습니다.

테스트는 평면 재현, 항등 변환, 정수 이동에서 알려진 배열, 영상 한 점의 경계 가중치를 검사합니다. 원본 파일이나 학습 모델 없이 좌표·표본화 계산을 검증합니다. 전체 변환은 원본의 직사각형 여부를 한 번 검사하고, 각 출력 위치에서 네 표본을 사용합니다. 원본 높이를 $`H_s`$라 하면 행 길이 검사와 보간의 시간은 $`O(H_s+H_dW_d)`$, 출력 저장 공간은 $`O(H_dW_d)`$입니다.

크게 축소하는 영상은 고주파가 낮은 표본 격자에서 겹칠 수 있습니다. Bilinear라고 충분한 anti-aliasing filter를 항상 제공하는 것은 아닙니다. 실제 영상 비교는 축소율·전처리·좌표 convention·색 공간을 맞추고, 선명도와 aliasing을 과제에 맞게 검토합니다. Interpolation 정확성과 인식 성능은 별개의 평가입니다.

## English

### Coordinates do not supply missing samples

A geometric transformation can point to source coordinate (2.4,1.7), where no stored pixel exists. Resampling estimates its value. This implementation uses a single-channel real array, integer pixel centers and `image[y][x]` indexing. These conventions prevent transposition and half-pixel disagreements from being mistaken for arithmetic errors. [OpenCV transforms](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html)

For floor coordinates i,j and fractions a,b, first interpolate each neighboring row horizontally, then interpolate those two results vertically. The equations above produce four nonnegative weights summing to one. Constant neighbors remain constant; the result stays within the four sampled values. Zero padding can lower a positive image near its edge because zero has become one of those sampled neighbors.

Bilinear means linear in each axis, not necessarily globally affine in two dimensions. However, an affine plane $`ux+vy+c`$ is reproduced exactly in the interior. Tests use that independent closed-form oracle rather than another copy of the interpolation loop.

### Map each destination back to its source

Forward mapping can leave holes or overlapping assignments after rounding. Inverse mapping visits every output pixel and requests a continuous source position. The 2×3 matrix above is already destination-to-source. To display a half-pixel movement to the right, read x-0.5 from the source. This explains the sign reversal between displayed motion and sampling coordinates. OpenCV `remap` uses the same destination-to-source viewpoint.

### Library conventions and borders

PyTorch `grid_sample` normally uses normalized -1 to 1 coordinates. With `align_corners=False`, integer-center source x maps to $`u=2(x+1/2)/W-1`$; with True and W>1, it maps to $`u=2x/(W-1)-1`$. Identical normalized values do not identify identical pixels across settings. [grid_sample](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.grid_sample.html)

The example directly uses pixel coordinates and constant-zero padding, without clamping or reflection. Sampling the one-pixel image [10] at (-0.25,0) gives 7.5 because the valid neighbor has weight 0.75. This differs from immediately returning zero whenever a coordinate is outside.

### Executed example and limits

The commands resample a 5×4 plane $`10y+x`$ using x-0.5,y-0.25. Destination (1,1) reads source (0.5,0.75), giving eight. Full input and output arrays are emitted in JSON.

Tests check affine-plane reproduction, identity, known integer translation and border weighting. They verify arithmetic without a camera or trained model. The whole-image transform validates rectangular row lengths once and uses four samples per output. With source height $`H_s`$, validation and interpolation take $`O(H_s+H_dW_d)`$ time and $`O(H_dW_d)`$ output storage.

Large downsampling can alias high-frequency content. Bilinear interpolation is not automatically an adequate antialiasing filter for every scale. Real comparisons also align scale, preprocessing, coordinate convention and color space. Resampling correctness and recognition quality remain different evaluation targets.

## 출처 / Sources

- [OpenCV, Geometric Image Transformations](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html): inverse mapping, bilinear methods and border semantics.
- [PyTorch 2.9 grid_sample](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.grid_sample.html): normalized coordinates, align_corners and padding. 확인 / checked: 2026-10-19.
