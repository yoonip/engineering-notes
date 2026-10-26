# 기술 용어의 뜻과 뉘앙스

[기초 문서](README.md) · [English](#english)

영어 단어를 한국어 한 단어로 바꾼 것만으로는 계산이나 장치의 동작이 잘 떠오르지 않을 때가 있습니다. 이름에서 얻는 첫 느낌과 실제 정의를 나란히 정리했습니다. 비유는 이해를 돕는 출발점이고, 식과 명세를 대신하지 않습니다. 각 항목의 자세한 유도와 공식 출처는 연결된 기초 글에 있습니다.

## AI에서 자주 만나는 표현

| 용어 | 이렇게 받아들이면 이해하기 쉽습니다 | 구분할 점 |
| --- | --- | --- |
| [Attention](../전자컴퓨터공학_ece/44-언어음성멀티모달AI_language-speech-multimodal/해설_notes/attention-from-equations.md) | “지금 항목을 기준으로 다른 정보들을 얼마씩 참고해 섞을까?” | 사람의 의식적 집중이나 정답의 중요도를 직접 측정하는 기능은 아닙니다 |
| Query·Key·Value | 찾는 기준·비교할 표식·가져올 내용 | 실제로는 벡터입니다. key는 암호 키, value는 좋고 나쁨을 나타내는 가치가 아닙니다 |
| Self-attention | 같은 입력 시퀀스 안에서 서로의 정보를 참고합니다 | 자기 자신 하나만 참고한다는 뜻은 아닙니다 |
| Weight | 결과에 어떤 입력이 얼마나 영향을 주도록 곱하는 계수 | parameter weight는 학습으로 바뀌는 모델 값, attention weight는 입력마다 계산되는 혼합 비율입니다 |
| [Bias](../전자컴퓨터공학_ece/23-AI머신러닝_ai-machine-learning/해설_notes/미분에서학습까지_gradients-and-learning.md) | $wx+b$에서 그래프의 기준 위치를 옮기는 $b$ | 이 문맥의 bias는 ‘편견’이 아닙니다. 통계의 추정 편향, 회로의 바이어스는 문맥에 맞게 따로 정의합니다 |
| Logit | sigmoid나 softmax에 넣기 전의 점수 | 0–1 확률 범위에 갇히지 않습니다. 확률과 같은 값으로 취급하지 않습니다 |
| [Gradient](../전자컴퓨터공학_ece/23-AI머신러닝_ai-machine-learning/해설_notes/미분에서학습까지_gradients-and-learning.md) | 여러 조절 손잡이를 조금씩 바꿀 때 손실이 어느 방향으로 얼마나 변하는지 모은 값 | 국소 변화율입니다. 멀리 움직여도 같은 효과를 보장하지 않습니다 |
| Backpropagation | 최종 손실에서 앞선 계산으로 거슬러 가며 연쇄 법칙을 적용합니다 | gradient를 구하는 과정입니다. 실제 매개변수 갱신은 optimizer가 합니다 |

Attention의 경우 “주의를 기울인다”에서 출발하되, 마지막에는 행별 점수 → softmax → 가중합이라는 계산으로 이해해야 합니다. 언어의 인상만으로 모델이 무엇을 이해하고 있는지 단정하지 않습니다. [원 논문 §3.2](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf)과 [Stanford CS224n 강의](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1234/slides/cs224n-2021-lecture09-transformers.pdf)의 Q/K/V 정의가 기준입니다.

## 하드웨어와 시스템의 표현

| 용어 | 이렇게 받아들이면 이해하기 쉽습니다 | 구분할 점 |
| --- | --- | --- |
| [State](../전자컴퓨터공학_ece/56-물리기초_physics-foundations/해설_notes/역학에너지진동_mechanics-energy-oscillation.md) | 입력이 주어졌을 때 다음 동작을 계산하는 데 필요한 현재 정보 | 물리 진동자에서는 위치만이 아니라 속도도 필요합니다. 상태가 항상 ‘정상·오류’ 같은 모드 이름은 아닙니다 |
| [Cache locality](../전자컴퓨터공학_ece/33-메모리저장장치_memory-storage/해설_notes/메모리지역성과캐시_locality-cache-amat.md) | 최근 값이나 가까운 주소를 다시 쓰는 경향 | 여기서 locality는 지리적 위치가 아니라 접근의 시간·주소 패턴입니다 |
| [Virtual memory](../전자컴퓨터공학_ece/07-컴퓨터공학기초_cs-foundations/해설_notes/같은주소다른메모리_processes-memory-concurrency.md) | 프로그램이 보는 주소를 실제 메모리와 연결하고 접근 권한을 관리하는 구조 | ‘가상’이라고 데이터가 허구라는 뜻은 아닙니다. 가상 주소와 물리 주소의 해석이 다릅니다 |
| [Volatile](../전자컴퓨터공학_ece/17-펌웨어-RTOS_firmware-rtos/해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md) | C에서 특정 접근을 컴파일러가 다루는 방식에 제약을 주는 한정자 | ‘쉽게 바뀌는 값’이라는 느낌만으로 원자성·스레드 동기화·DMA 일관성까지 보장한다고 생각하면 안 됩니다 |
| [Frame](../전자컴퓨터공학_ece/20-인터페이스통신_interfaces-communications/해설_notes/바이트가메시지가되려면_framing-uart-crc.md) | 흐르는 데이터에 경계를 붙여 한 묶음으로 해석한 것 | UART의 start/data/stop bit 묶음과 응용 프로토콜의 메시지 묶음은 서로 다른 계층일 수 있습니다 |
| [Bandwidth·latency·throughput](../전자컴퓨터공학_ece/25-CUDA성능최적화_cuda-performance/해설_notes/계산이느린가데이터를기다리는가_roofline-and-parallel-limits.md) | 통로가 나를 수 있는 양·한 작업을 기다리는 시간·실제로 처리한 양의 속도 | 통로가 넓어도 한 요청의 응답이 빨라지는 것은 아닙니다. 측정 계층과 단위를 함께 씁니다 |

같은 단어도 분야가 바뀌면 정의가 달라질 수 있습니다. 통신의 bandwidth는 Hz로 주파수 폭을 뜻하기도 하고, 메모리 bandwidth는 보통 byte/s로 전송 능력을 뜻합니다. [NVIDIA 성능 설명](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html)의 memory/math bandwidth도 이 문맥을 구분해서 읽습니다. 공유 메모리의 접근과 동기화는 [Linux의 volatile 설명](https://docs.kernel.org/process/volatile-considered-harmful.html)과 [DMA API](https://docs.kernel.org/core-api/dma-api-howto.html)에서 별도로 다룹니다.

## 측정과 모델에서의 표현

| 용어 | 이렇게 받아들이면 이해하기 쉽습니다 | 구분할 점 |
| --- | --- | --- |
| [Model](../전자컴퓨터공학_ece/56-물리기초_physics-foundations/해설_notes/열전도와확산_heat-diffusion.md) | 목적에 필요한 관계를 남겨 현상이나 시스템을 표현한 것 | AI의 학습된 모델만을 뜻하지 않습니다. 회로 식·상태 전이·열방정식도 모델입니다 |
| [Uncertainty](../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/단위차원측정불확도_units-dimensional-analysis-uncertainty.md) | 측정 결과에 부여할 수 있는 값들의 퍼짐을 평가한 것 | 알려진 실수를 얼버무리는 말도, 자동으로 참값을 포함하는 최대 오차도 아닙니다 |
| [Verification·validation](검증기록_VERIFICATION.md) | 식·명세대로 계산하는가 / 의도한 현실을 충분히 잘 설명하는가 | 수치해가 식과 맞는 것과 실제 장치 측정이 맞는 것은 다른 확인입니다 |

측정 불확도의 표현과 전파는 [NIST TN 1297](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty), 물리 모델의 타당성 범위는 [NASA-STD-7009](https://standards.nasa.gov/standard/NASA/NASA-STD-7009)와 연결해 읽을 수 있습니다.

## English

Replacing an English term with a single Korean word can lose the intuition needed to understand a calculation or device. The tables distinguish everyday associations from technical definitions. Analogies support understanding; they do not replace equations and specifications. Linked foundation articles provide derivations and official sources.

### AI terminology

| Term | Useful intuition | Important distinction |
| --- | --- | --- |
| [Attention](../전자컴퓨터공학_ece/44-언어음성멀티모달AI_language-speech-multimodal/해설_notes/attention-from-equations.md#english) | How much information should the current item draw from each other item? | It does not directly measure conscious focus or the true importance of an answer |
| Query, key, value | Search criterion, comparison marker, retrieved content | They are vectors; a key is not a cryptographic key and value is not a judgment of worth |
| Self-attention | Items in one input sequence can refer to one another | It does not restrict each item to looking only at itself |
| Weight | A coefficient controlling an input's contribution | Parameter weights are learned model values; attention weights are input-dependent mixing coefficients |
| [Bias](../전자컴퓨터공학_ece/23-AI머신러닝_ai-machine-learning/해설_notes/미분에서학습까지_gradients-and-learning.md#english) | The offset $b$ that shifts the baseline in $wx+b$ | This is not social prejudice; estimation bias and circuit bias need their own definitions |
| Logit | A score before sigmoid or softmax | It is not restricted to the probability interval 0–1 |
| [Gradient](../전자컴퓨터공학_ece/23-AI머신러닝_ai-machine-learning/해설_notes/미분에서학습까지_gradients-and-learning.md#english) | Local loss changes for small movements of several adjustment knobs | The same effect is not guaranteed for a large movement |
| Backpropagation | Apply the chain rule backward from loss through earlier operations | It computes gradients; the optimizer performs the parameter update |

Attention may start with the everyday idea of paying attention, but its operational meaning is row-wise scores, softmax and a weighted sum. Names alone do not establish what a model understands. The [original paper §3.2](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) and [Stanford's archived lecture](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1234/slides/cs224n-2021-lecture09-transformers.pdf) define Q/K/V.

### Hardware and systems terminology

| Term | Useful intuition | Important distinction |
| --- | --- | --- |
| [State](../전자컴퓨터공학_ece/56-물리기초_physics-foundations/해설_notes/역학에너지진동_mechanics-energy-oscillation.md#english) | Current information needed to predict the next behavior under an input | An oscillator needs velocity as well as position; state is not always a named mode such as normal/error |
| [Cache locality](../전자컴퓨터공학_ece/33-메모리저장장치_memory-storage/해설_notes/메모리지역성과캐시_locality-cache-amat.md#english) | Reusing recent values or nearby addresses | Locality concerns time and address patterns, not geographic proximity |
| [Virtual memory](../전자컴퓨터공학_ece/07-컴퓨터공학기초_cs-foundations/해설_notes/같은주소다른메모리_processes-memory-concurrency.md#english) | Mapping program-visible addresses and managing permissions | Virtual does not mean fictional data; virtual and physical addresses have different interpretations |
| [Volatile](../전자컴퓨터공학_ece/17-펌웨어-RTOS_firmware-rtos/해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md#english) | A C qualifier constraining how certain accesses are handled by the compiler | It does not by itself provide atomicity, thread synchronization or DMA coherence |
| [Frame](../전자컴퓨터공학_ece/20-인터페이스통신_interfaces-communications/해설_notes/바이트가메시지가되려면_framing-uart-crc.md#english) | A bounded unit interpreted within a data stream | A UART start/data/stop unit and an application message may be at different layers |
| [Bandwidth, latency, throughput](../전자컴퓨터공학_ece/25-CUDA성능최적화_cuda-performance/해설_notes/계산이느린가데이터를기다리는가_roofline-and-parallel-limits.md#english) | Transfer capacity, time for one operation, actual completed-work rate | A wider channel does not necessarily reduce individual-response time; state units and measurement level |

Meaning changes with context. Communication bandwidth may mean a frequency interval in Hz; memory bandwidth normally means a transfer capability in byte/s. [NVIDIA's guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html) uses memory and math bandwidth in specific performance contexts. [Linux volatile guidance](https://docs.kernel.org/process/volatile-considered-harmful.html) and the [DMA API](https://docs.kernel.org/core-api/dma-api-howto.html) separately explain access, synchronization and coherence.

### Measurement and modeling terminology

| Term | Useful intuition | Important distinction |
| --- | --- | --- |
| [Model](../전자컴퓨터공학_ece/56-물리기초_physics-foundations/해설_notes/열전도와확산_heat-diffusion.md#english) | A representation retaining relationships needed for a purpose | It includes circuit equations, state transitions and heat equations, not only learned AI models |
| [Uncertainty](../전자컴퓨터공학_ece/06-수식과코드_math-to-code/해설_notes/단위차원측정불확도_units-dimensional-analysis-uncertainty.md#english) | An evaluated dispersion expressing how well a measured quantity is known | It is neither an excuse for a known mistake nor automatically a guaranteed maximum error |
| [Verification and validation](검증기록_VERIFICATION.md#english) | Does the implementation follow the equations/specification? Is the model adequate for its intended reality? | Matching numerical equations and matching physical measurements are different checks |

[NIST TN 1297](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty) supports uncertainty propagation; [NASA-STD-7009](https://standards.nasa.gov/standard/NASA/NASA-STD-7009) provides the context for credibility and intended-use validation of models.
