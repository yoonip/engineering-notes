# 코드 출처와 구현 범위

Python, SystemVerilog, 교육용 Level1 모델의 작성·수정 과정에서 AI 코딩 도구를 사용했다. 연산 사양을 별도로 구현했으며 `metrics/`는 이 구현으로 수행한 실험의 집계치다.

| 구성 | 출처와 역할 | 배포 범위 |
|---|---|---|
| ResNet18/50 구조 | [torchvision ResNet](https://docs.pytorch.org/vision/0.23/models/resnet.html), [ResNet 논문](https://arxiv.org/abs/1512.03385) | 라이브러리 API 호출; 라이브러리·사전학습 가중치 미포함 |
| 학습·텐서 연산 | [PyTorch](https://pytorch.org/), [NumPy](https://numpy.org/) | 외부 의존성 |
| 데이터 | [CIFAR10/100](https://www.cs.toronto.edu/~kriz/cifar.html) | 데이터 미포함 |
| SAM | [논문](https://arxiv.org/abs/2010.01412), [공식 참고 구현](https://github.com/google-research/sam) | 두 단계 gradient 알고리즘을 별도로 구현; 외부 저장소 사본 미포함 |
| Signed 부분곱 | [Baugh–Wooley 방법](https://ieeexplore.ieee.org/document/1672241/) | 비트 행렬과 열 제거 사양을 별도로 구현 |
| 회로 시뮬레이터 | [ngspice](https://ngspice.sourceforge.io/) | 실행 파일·라이브러리 미포함 |
| 선택적 공정 모델 | [공식 SKY130 primitive 저장소](https://github.com/google/skywater-pdk-libs-sky130_fd_pr), commit `f62031a1be9aefe902d6d54cddd6f59b57627436` | 외부 로컬 모델만 읽음; 공급사 코드·모델·계수 사본 미포함 |

`circuit/models/educational_level1.pm`은 직접 작성한 예시 모델이며 공정 보정이 없다. SKY130 및 다른 공급사의 모델과 출처가 다르다. 외부 라이브러리·데이터·PDK의 이용 조건은 각 배포물에 따른다. 자체 소스의 오픈소스 라이선스는 지정하지 않았다.

## English attribution

AI coding tools were used while developing this independent implementation. External libraries are imported, and ngspice is a separate dependency. Datasets and process models are managed separately. Component attribution is listed above.
