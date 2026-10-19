# 그래픽스와 렌더링 | Computer Graphics, Rendering & Simulation

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

컴퓨터 그래픽스는 장면과 재질·빛·카메라를 계산해 영상을 만드는 분야입니다. 로봇과 컴퓨터 비전에서는 시뮬레이션, 센서 모델, 합성 데이터 생성에도 쓰입니다.

## 좌표에서 pixel까지

Model·world·view·projection 변환은 물체 좌표를 화면으로 연결합니다. Rasterization은 도형이 차지하는 pixel을 찾고 shader는 위치·표면·조명 계산을 수행합니다. Depth buffer는 가려짐을 처리합니다. 좌표축 방향과 행렬 곱 순서가 다르면 같은 데이터도 다르게 보입니다.

## 광선과 재질

Ray tracing은 광선과 장면의 교차를 계산합니다. Physically based rendering은 재질과 빛의 상호작용을 물리적인 관계에 맞춰 모델링합니다. Monte Carlo 적분은 광 경로를 표본으로 뽑아 빛의 전달을 추정합니다. 표본 수에 따라 영상의 noise가 달라집니다.

OpenGL·Vulkan·DirectX·WebGPU는 GPU 기능에 접근하는 API, GLSL·HLSL은 shader 언어입니다. Blender는 모델링과 렌더링, Mitsuba·PBRT는 렌더링 연구, Unreal·Unity는 실시간 응용에 쓰입니다. 합성 데이터가 시각적으로 정교하더라도 실제 센서 데이터와 분포가 일치하는지는 따로 살펴야 합니다.

## 관련 기술

OpenGL, Vulkan, DirectX, WebGPU, GLSL, HLSL, Blender, Mitsuba, PBRT, Unreal, Unity

## 참고 자료

- [Physically Based Rendering](https://pbr-book.org/)

## 기초 해설

- [좌표 변환에서 pixel까지: 동차 좌표와 rasterization](해설_notes/좌표변환에서pixel까지_transforms-projection-and-rasterization.md)

## English

### Graphics and rendering

Computer graphics computes images from scenes, materials, lighting, and cameras. In robotics and vision, it also supports simulation, sensor models, and synthetic data generation.

### From coordinates to pixels

Model, world, view, and projection transforms map object coordinates to the screen. Rasterization finds the pixels covered by geometry, while shaders compute positions, surfaces, and lighting. A depth buffer handles occlusion. Coordinate-axis conventions and matrix multiplication order can change how the same data appears.

### Rays and materials

Ray tracing computes intersections between rays and a scene. Physically based rendering models the interaction of materials and light through physical relationships. Monte Carlo integration estimates light transport by sampling paths, linking the number of samples to image noise.

OpenGL, Vulkan, DirectX, and WebGPU expose GPU functionality, while GLSL and HLSL are shader languages. Blender supports modeling and rendering; Mitsuba and PBRT support rendering research. Unreal and Unity support real-time applications. Visually convincing synthetic data can still differ from the distribution of a real sensor.

### Foundation article

- [좌표 변환에서 pixel까지: 동차 좌표와 rasterization](해설_notes/좌표변환에서pixel까지_transforms-projection-and-rasterization.md#english)


## 심화 해설 | Advanced article

- [원근 투영 뒤에도 표면의 속성을 맞추는 보간](해설_notes/원근보정속성보간_perspective-interpolation.md) · [English](해설_notes/원근보정속성보간_perspective-interpolation.md#english)
