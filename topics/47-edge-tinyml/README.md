# Edge AI · TinyML · NPU

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

Edge AI는 데이터가 생성되는 장치나 그 가까이에서 추론하는 방식이다. 네트워크 연결과 전송 지연을 줄일 수 있지만 계산량·메모리·전력·열·지원 연산의 제약을 직접 다룬다. TinyML은 특히 작은 MCU 자원에서의 머신러닝과 연결된다.

## 모델에서 장치 실행으로

모델 변환은 학습 framework의 graph를 배포 runtime이 이해하는 표현으로 옮긴다. ONNX는 모델 교환 표현이다. NPU는 특정 신경망 연산을 효율적으로 실행하는 가속기이며 모든 연산이나 동적 shape가 동일하게 지원되는 것은 아니다. 지원하지 않는 연산의 CPU fallback은 전체 latency를 늘릴 수 있다.

## 경량화와 측정

Quantization은 값의 표현을 줄인다. Post-training quantization은 학습 후 보정·변환을, quantization-aware training은 학습 과정에서 양자화 효과를 반영한다. 가중치 크기와 실행 중 activation·workspace 메모리는 별개다. 입력 전처리와 후처리까지 포함해야 장치의 실제 응답 시간을 알 수 있다.

TensorRT·OpenVINO·LiteRT·TensorFlow Lite Micro·CMSIS-NN·ExecuTorch·TVM은 대상과 실행 범위가 다른 배포 생태계다. Jetson·Coral·모바일 NPU·MCU는 자원과 개발 흐름이 다르다. 음성·비전·이상 탐지·로봇 제어에서 정확도와 에너지·지연의 균형이 중요하다.

## 관련 기술

ONNX Runtime, TensorRT, OpenVINO, LiteRT/TFLite, TFLite Micro, CMSIS-NN, ExecuTorch, TVM, Jetson, Coral

## 참고 자료

- [ONNX documentation](https://onnx.ai/onnx/)
