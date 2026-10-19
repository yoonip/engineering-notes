# 신호처리와 제어

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

신호처리는 관측한 데이터를 변환·필터링·분석하는 분야이고, 제어는 원하는 동작에 가까워지도록 시스템 입력을 결정하는 분야다. 센서에서 얻은 신호가 상태 추정과 피드백 제어로 이어진다.

## 샘플링과 변환

연속 신호를 일정한 간격으로 관측하면 이산 신호가 된다. 제한된 대역의 신호를 복원하려면 표본화 조건과 anti-aliasing 필터가 중요하다. Fourier 변환은 주파수 성분, Laplace·Z 변환은 연속·이산 시스템의 동작을 해석한다. FFT는 DFT를 빠르게 계산하는 알고리즘이다.

## 필터와 피드백

FIR은 유한한 impulse response를, IIR은 피드백을 포함한 재귀 구조를 갖는다. PID는 오차의 현재값·누적·변화율을 이용한다. 적분기는 정상상태 오차를 줄일 수 있지만 포화 상황에서는 windup을 일으킬 수 있고, 미분 항은 고주파 잡음에 민감하다.

상태공간 모델은 내부 상태와 입력·출력의 관계를 표현한다. LQR은 이차 비용을 최소화하는 제어, MPC는 제약을 포함한 미래 구간의 최적화에 기반한다. Kalman filter는 모델과 관측의 불확실성을 결합하고 EKF·UKF는 비선형 시스템으로 확장하는 방법이다. System identification은 측정 데이터에서 모델을 추정한다.

## 관련 기술

FFT, FIR/IIR, PID, State Space, LQR/LQG, MPC, Kalman/EKF/UKF, System Identification, SciPy Signal, MATLAB Control

## 참고 자료

- [SciPy documentation](https://docs.scipy.org/doc/scipy/)
