# 코드 출처와 구현 범위

Python·SystemVerilog 연산 모델과 교육용 Level1 회로 모델을 포함합니다. `metrics/`에는 이 구현에서 얻은 실험 집계치를 정리했습니다.

| 구성 | 출처와 역할 | 배포 범위 |
|---|---|---|
| ResNet18/50 구조 | [torchvision ResNet](https://docs.pytorch.org/vision/0.23/models/resnet.html), [ResNet 논문](https://arxiv.org/abs/1512.03385) | 라이브러리 API 호출; 라이브러리·사전학습 가중치 미포함 |
| 학습·텐서 연산 | [PyTorch](https://pytorch.org/), [NumPy](https://numpy.org/) | 외부 의존성 |
| 데이터 | [CIFAR10/100](https://www.cs.toronto.edu/~kriz/cifar.html) | 데이터 미포함 |
| SAM | [논문](https://arxiv.org/abs/2010.01412), [공식 참고 구현](https://github.com/google-research/sam) | 두 단계 gradient 알고리즘을 별도로 구현; 외부 저장소 사본 미포함 |
| Signed 부분곱 | [Baugh–Wooley 방법](https://ieeexplore.ieee.org/document/1672241/) | 비트 행렬과 열 제거 사양을 별도로 구현 |
| 회로 시뮬레이터 | [ngspice](https://ngspice.sourceforge.io/) | 실행 파일·라이브러리 미포함 |
| 선택적 공정 모델 | [공식 SKY130 primitive 저장소](https://github.com/google/skywater-pdk-libs-sky130_fd_pr), commit `f62031a1be9aefe902d6d54cddd6f59b57627436` | 외부 로컬 모델만 읽음; 공급사 코드·모델·계수 사본 미포함 |

`circuit/models/educational_level1.pm`은 직접 작성한 예시 모델이며 공정 보정이 없습니다. SKY130 및 다른 공급사의 모델과 출처가 다릅니다. 외부 라이브러리·데이터·PDK의 이용 조건은 각 배포물에 따릅니다. 자체 소스의 오픈소스 라이선스는 지정하지 않았습니다.

`MANIFEST_SHA256.json`은 현재 공개 파일의 크기와 해시입니다. 문서의 바이트가 달라져도 `VALIDATION_RESULTS.json`의 과거 실행 기록과 `metrics/`의 측정값은 새 실행 결과로 바뀌지 않습니다.

## English

The project includes Python and SystemVerilog arithmetic models and an educational Level1 circuit model. `metrics/` stores aggregate measurements from this implementation.

| Component | Attribution and role | Distribution |
| --- | --- | --- |
| ResNet18/50 | [torchvision](https://docs.pytorch.org/vision/0.23/models/resnet.html) and the [ResNet paper](https://arxiv.org/abs/1512.03385) | Library API calls; no library copy or pretrained weights |
| Training/tensor operations | [PyTorch](https://pytorch.org/) and [NumPy](https://numpy.org/) | External dependencies |
| Data | [CIFAR10/100](https://www.cs.toronto.edu/~kriz/cifar.html) | Not bundled |
| SAM | [Paper](https://arxiv.org/abs/2010.01412) and [official reference](https://github.com/google-research/sam) | Separate implementation of the two-step gradient method; no repository copy |
| Signed partial products | [Baugh–Wooley method](https://ieeexplore.ieee.org/document/1672241/) | Separate bit-matrix and column-removal implementation |
| Circuit simulation | [ngspice](https://ngspice.sourceforge.io/) | No binaries or libraries |
| Optional process model | [Official SKY130 primitives](https://github.com/google/skywater-pdk-libs-sky130_fd_pr), commit `f62031a1be9aefe902d6d54cddd6f59b57627436` | Reads a local model; no vendor source, model or coefficient copy |

`circuit/models/educational_level1.pm` is an example model without process calibration. It is separate from SKY130 and other vendor models. External libraries, datasets and PDKs retain their own terms. An open-source license has not been assigned to the project source.

`MANIFEST_SHA256.json` identifies the current published sizes and hashes. Document changes do not turn the historical runs in `VALIDATION_RESULTS.json` or the measurements under `metrics/` into new execution results.
