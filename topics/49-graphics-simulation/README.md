# Graphics & Rendering

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

컴퓨터 그래픽스는 장면과 재질·빛·카메라를 계산해 영상을 만드는 분야다. Robotics·vision과 연결되면 시뮬레이션·센서 모델·합성 데이터 생성의 기반이 된다.

## 좌표에서 pixel까지

Model·world·view·projection 변환은 물체 좌표를 화면으로 연결한다. Rasterization은 도형이 차지하는 pixel을 찾고 shader는 위치·표면·조명 계산을 수행한다. Depth buffer는 가려짐을 처리한다. 좌표축 방향과 행렬 곱 순서가 다르면 같은 데이터도 다르게 보인다.

## 광선과 재질

Ray tracing은 광선과 장면의 교차를 계산한다. Physically based rendering은 재질과 빛의 상호작용을 물리적인 관계에 맞춰 모델링한다. Monte Carlo 적분은 많은 광 경로를 표본으로 추정하므로 표본 수와 noise가 연결된다.

OpenGL·Vulkan·DirectX·WebGPU는 GPU 기능에 접근하는 API, GLSL·HLSL은 shader 언어다. Blender는 모델링과 렌더링, Mitsuba·PBRT는 렌더링 연구, Unreal·Unity는 실시간 응용에 쓰인다. 합성 데이터의 시각적 완성도와 실제 센서 분포의 일치는 다른 문제다.

## 관련 기술

OpenGL, Vulkan, DirectX, WebGPU, GLSL, HLSL, Blender, Mitsuba, PBRT, Unreal, Unity

## 참고 자료

- [Physically Based Rendering](https://pbr-book.org/)
