# 카메라 모델, 영상 필터, CV 검증

## 영상의 좌표는 어떻게 만들어지는가

카메라는 3차원 장면을 2차원 밝기 배열로 바꾼다. 같은 물체도 거리와 방향, 조명, 렌즈에 따라 다르게 보인다. 따라서 영상 인식의 앞에는 좌표계와 측정 모델이 있다. 이 글은 왜곡 없는 pinhole 카메라, 정지한 장면, 양의 깊이 $Z_c>0$를 가정한다. 실제 렌즈의 왜곡, motion blur, rolling shutter와 노출 변화는 별도 모델이다.

카메라 좌표의 점 $P_c=(X_c,Y_c,Z_c)$에서 작은 구멍을 통과하는 광선을 생각하자. 닮은 삼각형 때문에 정규화 영상 좌표는 $x=X_c/Z_c$, $y=Y_c/Z_c$다. 물리 초점거리와 pixel 크기를 결합한 $f_x,f_y$의 단위는 pixel이고, 주점 $c_x,c_y$도 pixel 좌표다.

$$u=f_xX_c/Z_c+c_x,\qquad v=f_yY_c/Z_c+c_y.$$

세계 좌표에서는 $P_c=RP_w+t$를 먼저 계산한다. 이 식의 $R,t$는 세계에서 카메라로 바꾸는 변환이며 카메라 위치 자체와 $t$를 혼동하지 않는다. OpenCV의 pinhole 정의도 이 방향과 내부 파라미터를 사용한다. [OpenCV calibration](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

예를 들어 $f_x=f_y=800$, $c=(320,240)$, $P_c=(1,2,4)$이면 영상 위치는 ((520,640))다. 점과 깊이를 함께 두 배로 늘린 ((2,4,8))도 같은 곳에 보인다. 한 장의 영상만으로 절대 거리를 알아내기 어려운 이유가 이 광선 방향의 모호함에 있다. $Z_c=0$에서는 나눗셈이 정의되지 않는다. 모델은 카메라 뒤의 점도 거부한다.

## 이웃 pixel을 결합하는 필터

영상 (I[y,x])에 작은 가중치 배열 (K[j,i])를 적용하면 주변 정보를 결합할 수 있다. 커널을 뒤집지 않는 cross-correlation의 valid 영역 연산은

$$Y[y,x]=\sum_{j=0}^{k_h-1}\sum_{i=0}^{k_w-1}K[j,i]I[y+j,x+i].$$

Stride는 1, padding은 없다고 정했다. $H\times W$ 영상의 출력 크기는 $(H-k_h+1)\times(W-k_w+1)$이고 직접 계산 비용은 $O(HWk_hk_w)$ 정도다. 수학적 convolution은 커널 방향을 뒤집는다는 차이가 있다. OpenCV `filter2D`도 이름과 달리 기본적으로 correlation을 계산한다고 문서에 명시한다. [OpenCV filtering](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html)

2×2 평균 커널의 원소가 모두 $1/4$이면 가중치 합이 1이므로 상수 영상 $I=c$에서 $Y=c\sum K=c$다. 반면 `[1,-1]` 커널은 가중치 합이 0이므로 상수 구간에서 0이고, `[1,2,3]`에 적용하면 `[-1,-1]`이다. 이 비대칭 커널은 뒤집기 실수를 드러내는 데 유용하다. 대칭 평균 커널만 검사하면 convolution과 correlation을 잘못 구현해도 차이가 보이지 않을 수 있다.

| 확인할 항목 | 계산·측정의 의미 |
|---|---|
| 좌표계·pixel 원점 | 같은 수치가 같은 위치를 뜻하는지 |
| 입력 크기·dtype·정규화 | 모델이 기대하는 입력과 일치하는지 |
| padding·stride·커널 방향 | 필터 경계와 출력 위치가 맞는지 |
| 데이터 분리 | 같은 사람·영상 연속 frame이 양쪽에 섞이지 않는지 |
| task별 지표 | 검출·분류·좌표 추정의 오류를 맞게 셌는지 |

## 계산 정확성과 시각 시스템 성능은 다르다

카메라 calibration에서는 알려진 3D 점을 영상으로 다시 투영해 관측점과의 pixel 오차를 계산할 수 있다. 예를 들어 $e_{RMS}=\sqrt{\frac1N\sum_i[(u_i-\hat u_i)^2+(v_i-\hat v_i)^2]}$다. 이 정의는 좌표 두 개의 제곱을 합한 “점당” RMS이며, 좌표당 RMS와 분모가 다르다. 학습에 사용한 calibration 영상의 오차만 작아도 다른 거리·화면 가장자리·렌즈 설정에서 정확하다는 결론은 나오지 않는다. [OpenCV calibration model과 reprojection](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

인식 모델은 별도의 정답 label과 고정된 train/validation/test 분리가 필요하다. 연속 frame은 거의 같은 장면을 공유할 수 있으므로 무작위 frame 분할만으로 독립 평가가 되지 않을 수 있다. 성공 평균뿐 아니라 어두운 장면, 작은 물체, 가림처럼 조건별 실패도 기록해야 결과를 해석할 수 있다. 이 평가 설계는 아래의 계산 테스트가 다루는 범위보다 넓다.

## 구현과 검증

[`pinhole`, `correlate_valid`](../../../예제_examples/확장기초_extended/ai_data/models.py)는 위의 정확한 전제를 사용한다. [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 닮은 삼각형에서 계산한 좌표, 동일 광선의 배율 불변, 깊이 0 거부, 상수 영상 보존, 비대칭 커널과 1×1 항등 필터를 확인한다. 실제 카메라나 학습 모델을 실행한 검증은 아니다. 물리 장치와 연결하려면 렌즈·해상도·좌표 convention을 고정하고 독립된 관측 데이터와 비교하는 단계가 이어진다.

## English

### From 3D points to pixels

A camera maps a scene to a brightness array. Geometry, illumination and optics change its appearance, so coordinate and measurement models precede recognition. Here the assumptions are a distortion-free pinhole camera, a static scene and positive camera depth $Z_c>0$. Lens distortion, motion blur, rolling shutter and exposure changes are separate effects.

Similar triangles give normalized coordinates $X_c/Z_c,Y_c/Z_c$. Multiplication by focal lengths $f_x,f_y$ in pixels and addition of principal-point coordinates produce the projection equations above. First transform a world point using $P_c=RP_w+t$; this $R,t$ maps world coordinates to camera coordinates. Translation $t$ is not itself the camera position in the world. [OpenCV camera model](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

With focal lengths 800, principal point ((320,240)) and camera point ((1,2,4)), the pixel is ((520,640)). Scaling the point to ((2,4,8)) preserves its image. This ray ambiguity explains why a single image does not directly establish absolute distance. Projection at zero depth is undefined, and the model rejects points behind the camera.

### Local filtering

The correlation equation combines an image neighborhood with kernel coefficients without flipping the kernel. With unit stride and no padding, an $H\times W$ image gives $(H-k_h+1)\times(W-k_w+1)$ output. Direct work is approximately $O(HWk_hk_w)$. Mathematical convolution flips kernel directions. OpenCV explicitly documents that `filter2D` computes correlation. [Image filtering](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html)

A 2×2 averaging kernel has coefficients $1/4$, so a constant input $c$ stays constant because $c\sum K=c$. The asymmetric kernel `[1,-1]` has zero sum and yields zero on constants; on `[1,2,3]` it produces `[-1,-1]`. This catches kernel reversal errors that a symmetric averaging filter would hide.

The table lists coordinate origins, dtype and normalization, padding/stride/orientation, data separation and task-specific metrics. Each describes a separate agreement needed between data, code and evaluation.

### Correct calculations versus useful vision

Reprojection compares observed pixels with projections of known 3D points. The RMS formula above sums both coordinate errors and averages per point; a per-coordinate RMS has a different denominator. Small error on the same calibration images does not establish accuracy at other distances, image edges or lens settings. [OpenCV calibration](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

Recognition additionally needs labels and fixed training, validation and test splits. Adjacent frames may share almost identical scenes, so random frame splitting may fail to provide independent evaluation. Conditions such as darkness, small objects and occlusion can reveal failures hidden by an overall average. These system-level questions extend beyond the arithmetic checks below.

### Models and checks

The linked `pinhole` and `correlate_valid` implement the stated conventions. Tests check hand-derived projection coordinates, ray-scaling invariance, zero-depth rejection, preservation of constant images, an asymmetric kernel and a 1×1 identity. They do not test a physical camera or a trained model. Connecting the model to hardware requires fixed lens, resolution and coordinate conventions plus comparison against independent observations.

## Sources

- [OpenCV, Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html): pinhole coordinates, intrinsic/extrinsic parameters and reprojection.
- [OpenCV, Image Filtering](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html): correlation versus convolution and border behavior. Reference date: 2026-10-19.
