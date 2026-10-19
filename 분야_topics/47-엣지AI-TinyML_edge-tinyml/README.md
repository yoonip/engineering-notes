# 엣지 AI·TinyML·NPU | Edge AI, TinyML & NPUs

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

Edge AI는 데이터가 생성되는 장치나 그 가까이에서 추론하는 방식이다. 네트워크 연결과 전송 지연을 줄일 수 있지만 계산량·메모리·전력·열·지원 연산의 제약을 장치 안에서 해결해야 한다. TinyML은 특히 자원이 작은 MCU에서 머신러닝을 실행하는 데 초점을 둔다.

## 모델에서 장치 실행으로

모델 변환은 학습 framework의 graph를 배포 runtime이 이해하는 표현으로 옮긴다. ONNX는 모델 교환 표현이다. NPU는 특정 신경망 연산을 효율적으로 실행하는 가속기이며 모든 연산이나 동적 shape가 동일하게 지원되는 것은 아니다. 지원하지 않는 연산의 CPU fallback은 전체 latency를 늘릴 수 있다.

## 경량화와 측정

Quantization은 값의 표현을 줄인다. Post-training quantization은 학습 후 보정·변환을, quantization-aware training은 학습 과정에서 양자화 효과를 반영한다. 가중치 크기와 실행 중 activation·workspace 메모리는 별개다. 입력 전처리와 후처리까지 포함해야 장치의 실제 응답 시간을 알 수 있다.

TensorRT·OpenVINO·LiteRT·TensorFlow Lite Micro·CMSIS-NN·ExecuTorch·TVM은 대상과 실행 범위가 서로 다른 배포 도구다. Jetson·Coral·모바일 NPU·MCU는 자원과 개발 흐름이 다르다. 음성·비전·이상 탐지·로봇 제어에서 정확도와 에너지·지연의 균형이 중요하다.

## 관련 기술

ONNX Runtime, TensorRT, OpenVINO, LiteRT/TFLite, TFLite Micro, CMSIS-NN, ExecuTorch, TVM, Jetson, Coral

## 참고 자료

- [ONNX documentation](https://onnx.ai/onnx/)

## 기초 해설

- [정수 양자화: scale, zero-point, 배포 오차](해설_notes/정수양자화_integer-quantization-and-deployment-error.md)

## English

### Edge AI, TinyML, and NPUs

Edge AI performs inference on or near the device that produces the data. It can reduce network dependence and transfer latency, while placing compute, memory, power, thermal, and operator-support constraints on the device. TinyML focuses on machine learning with especially limited microcontroller resources.

### From a model to device execution

Model conversion translates a training framework's graph into a representation understood by a deployment runtime. ONNX provides a model-exchange representation. An NPU accelerates selected neural-network operations, but support varies across operators and dynamic shapes. CPU fallback for an unsupported operation can increase end-to-end latency.

### Model compression and measurement

Quantization reduces numerical representation. Post-training quantization calibrates and converts a trained model; quantization-aware training includes quantization effects during training. Weight storage, activations, and execution workspace are separate memory requirements. Preprocessing and postprocessing must be included to measure the device's actual response time.

TensorRT, OpenVINO, LiteRT, TensorFlow Lite Micro, CMSIS-NN, ExecuTorch, and TVM support different targets and execution scopes. Jetson, Coral, mobile NPUs, and MCUs have different resources and development flows. Speech, vision, anomaly detection, and robotics applications balance accuracy against energy and latency.

### Foundation article

- [정수 양자화: scale, zero-point, 배포 오차](해설_notes/정수양자화_integer-quantization-and-deployment-error.md#english)


## 심화 해설 | Advanced article

- [채널별 정수 양자화와 오차의 크기](해설_notes/채널별정수양자화_per-channel-quantization.md) · [English](해설_notes/채널별정수양자화_per-channel-quantization.md#english)
