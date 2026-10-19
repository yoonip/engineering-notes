# DeepSeek R1-Distill의 구조와 메모리 | R1-Distill architecture and memory

여기서는 `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`를 구체적인 분석 대상으로 삼았습니다. 공식 자료 확인일은 2026-10-19입니다. R1이 만든 풀이 데이터를 다른 기반 모델에 학습시킨 배포물이며, 원본 R1의 층을 단순히 줄인 모델이 아닙니다. [공식 R1 자료](https://github.com/deepseek-ai/DeepSeek-R1)

## 원본 모델과 학생 모델

| 배포물 | 기반 구조·역할 | 직접 연결하면 안 되는 가정 |
|---|---|---|
| DeepSeek-R1 원본 | DeepSeek-V3-Base 계보의 MoE 추론 모델입니다. | Distill 학생도 같은 MoE라고 가정하면 안 됩니다. |
| R1-Distill-Qwen-1.5B | Qwen2.5-Math-1.5B 계보의 dense 모델입니다. | 원본 R1의 메모리·속도·정답률을 그대로 옮길 수 없습니다. |
| R1-Distill-Llama | 크기에 따라 Llama 계보를 사용합니다. | Qwen 학생과 tokenizer·기반 라이선스가 같다고 볼 수 없습니다. |

공식 release의 코드·가중치 조건은 MIT로 안내되며, Qwen·Llama 기반 모델의 출처와 원래 조건도 따로 명시합니다. [개별 모델 카드](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)에서 기반 모델과 사용 안내를 함께 확인하실 수 있습니다.

## 공개 설정을 읽어 메모리를 계산하기

[공식 config.json](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B/raw/main/config.json)의 `Qwen2ForCausalLM`, 28층, hidden size 1536, Q 헤드 12개, KV 헤드 2개를 확인했습니다. 이 모델의 헤드 차원은 `1536/12=128`입니다. `use_sliding_window=false`이므로 아래 계산은 전체 길이를 보관하는 K·V 배열을 대상으로 합니다.

Batch 1, BF16에서는 `2×28×2×128×토큰 수×2 bytes`로 계산합니다. [직접 실행한 계산 코드](../experiments/cpu_lab.py)의 결과는 다음과 같습니다.

| 보관 토큰 수 | 계산한 K·V 배열 저장량 |
|---:|---:|
| 4,096 | 0.109375 GiB |
| 16,384 | 0.437500 GiB |
| 32,768 | 0.875000 GiB |

가중치를 이름의 근삿값 1.5B로 잡으면 BF16 payload는 약 2.794 GiB입니다. 실제 파라미터 수를 센 값이나 체크포인트 파일 크기는 아닙니다. 4bit의 이상적인 payload는 약 0.698 GiB이지만 scale·일부 비양자화 값·activation·작업 공간은 별도입니다. 따라서 이 표를 그대로 최소 RAM 또는 VRAM 보장값으로 사용하면 안 됩니다.

## 학생이 무엇을 배우는지 확인하는 작은 실험

[CPU 실험 3](../experiments/README.md#3-확률을-배우는-학생과-정답-번호만-배우는-학생)에서는 세 클래스 교사의 전체 확률을 알려 주는 경우와 최상위 정답 번호만 알려 주는 경우를 비교했습니다. 학생은 기울기·절편 총 6개를 갖습니다. 학습 입력 7개, 별도 입력 40개, 경사하강법 1,200회로 조건을 맞췄습니다.

| 학습 정보 | 교사와 최상위 클래스 일치율 | 교사→학생 평균 KL 발산 |
|---|---:|---:|
| 정답 번호 | 90% | 0.379719331 |
| 확률 분포 | 100% | 약 0.000000001 |

이는 실제 R1-Distill 학습을 재현하지 않습니다. 이 예제는 전통적인 확률 분포 증류를 설명합니다. R1-Distill은 생성된 풀이 텍스트를 학생에게 학습시키는 접근이므로 학습 신호가 다릅니다. 또한 학생이 교사의 식을 표현할 수 있게 구성했으므로 작은 모델의 실제 한계나 압축률을 평가한 결과도 아닙니다.

## 가중치 추론을 재현할 때

선택한 DeepSeek 배포물의 tokenizer와 chat template을 함께 사용합니다. 기반 Qwen의 설정으로 임의 교체하지 않습니다. 공식 권장 temperature 범위는 0.5~0.7이며 0.6을 권합니다. System prompt 대신 user 입력에 지시를 두라는 안내와 반복 평가 조건도 확인합니다.

수학은 최종 답 일치, 코드는 독립 테스트 실행, 한국어 설명은 사실 보존·문체를 따로 평가합니다. 출력 토큰 한도가 짧아 풀이가 잘린 실패와 답 자체가 틀린 실패도 구분해야 합니다. 여기서는 공식 가중치 추론과 공식 벤치마크를 실행하지 않았습니다.

[모델·도구 분석](../models/README.md) · [메모리·증류·양자화 실험](../experiments/README.md)

## English

The selected distilled checkpoint is a Qwen-based dense student, not a smaller copy of the original R1 MoE. The official configuration gives a 0.109375 GiB BF16 KV payload at 4,096 cached tokens and batch one. This is calculated array storage, not measured GPU usage. A separate six-parameter student experiment illustrates probability-target learning; it does not reproduce DeepSeek training, model inference, or official benchmarks.
