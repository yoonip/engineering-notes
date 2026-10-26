# DeepSeek R1-Distill의 구조와 메모리 | R1-Distill architecture and memory

여기서는 `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`를 구체적인 분석 대상으로 삼았습니다. 공식 자료 재확인일은 2026-10-21입니다. R1이 만든 풀이 데이터를 다른 기반 모델에 학습시킨 배포물이며, 원본 R1의 층을 단순히 줄인 모델이 아닙니다. [공식 R1 자료](https://github.com/deepseek-ai/DeepSeek-R1)

## 원본 모델과 학생 모델

| 배포물 | 기반 구조·역할 | 직접 연결하면 안 되는 가정 |
|---|---|---|
| DeepSeek-R1 원본 | DeepSeek-V3-Base 계보의 MoE 추론 모델입니다. | Distill 학생도 같은 MoE라고 가정하면 안 됩니다. |
| R1-Distill-Qwen-1.5B | Qwen2.5-Math-1.5B 계보의 dense 모델입니다. | 원본 R1의 메모리·속도·정답률을 그대로 옮길 수 없습니다. |
| R1-Distill-Llama | 크기에 따라 Llama 계보를 사용합니다. | Qwen 학생과 tokenizer·기반 라이선스가 같다고 볼 수 없습니다. |

공식 release의 코드·가중치 조건은 MIT로 안내되며, Qwen·Llama 기반 모델의 출처와 원래 조건도 따로 명시합니다. [개별 모델 카드](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)에서 기반 모델과 사용 안내를 함께 확인하실 수 있습니다.

## 공개 설정을 읽어 메모리를 계산하기

[공식 config.json](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B/raw/main/config.json)의 `Qwen2ForCausalLM`, 28층, hidden size 1536, Q 헤드 12개, KV 헤드 2개를 확인했습니다. 이 모델의 헤드 차원은 `1536/12=128`입니다. `use_sliding_window=false`이므로 아래 계산은 전체 길이를 보관하는 K·V 배열을 대상으로 합니다.

Batch 1, BF16에서는 `2×28×2×128×토큰 수×2 bytes`로 계산합니다. [직접 실행한 계산 코드](../../experiments/cpu_lab.py)의 결과는 다음과 같습니다.

| 보관 토큰 수 | 계산한 K·V 배열 저장량 |
|---:|---:|
| 4,096 | 0.109375 GiB |
| 16,384 | 0.437500 GiB |
| 32,768 | 0.875000 GiB |

가중치를 이름의 근삿값 1.5B로 잡으면 BF16 payload는 약 2.794 GiB입니다. 실제 파라미터 수를 센 값이나 체크포인트 파일 크기는 아닙니다. 4bit의 이상적인 payload는 약 0.698 GiB이지만 scale·일부 비양자화 값·activation·작업 공간은 별도입니다. 따라서 이 표를 그대로 최소 RAM 또는 VRAM 보장값으로 사용하면 안 됩니다.

## 실제 증류의 학습 신호

공식 R1 README는 R1이 생성한 풀이 표본으로 Qwen·Llama 기반의 dense 모델을 미세조정했다고 설명합니다. 원본 R1의 강화학습과 학생 모델의 표본 기반 미세조정은 같은 절차가 아닙니다. 또한 학생 모델에서 세부 config와 tokenizer를 바꾸었다고 하므로 기반 모델의 설정으로 임의 교체하지 않습니다. [공식 Distillation·배포물 설명](https://github.com/deepseek-ai/DeepSeek-R1#2-model-summary)

전통적인 확률 분포 증류는 교사의 출력 확률을 학습 목표로 쓰는 방식입니다. R1-Distill의 생성 풀이 텍스트 학습과 학습 신호가 다릅니다. [별도 CPU 실험 3](../../experiments/README.md#3-확률을-배우는-학생과-정답-번호만-배우는-학생)은 확률 회귀를 설명하며 실제 R1·Qwen 가중치를 쓰지 않습니다. 그 실험의 일치율을 R1-Distill 품질이나 압축률로 소개하지 않습니다.

## 가중치 추론을 재현할 때

선택한 DeepSeek 배포물의 tokenizer와 chat template을 함께 사용합니다. 기반 Qwen의 설정으로 임의 교체하지 않습니다. 공식 권장 temperature 범위는 0.5~0.7이며 0.6을 권합니다. System prompt 대신 user 입력에 지시를 두라는 안내와 반복 평가 조건도 확인합니다.

수학은 최종 답 일치, 코드는 독립 테스트 실행, 한국어 설명은 사실 보존·문체를 따로 평가합니다. 출력 토큰 한도가 짧아 풀이가 잘린 실패와 답 자체가 틀린 실패도 구분해야 합니다. 여기서는 공식 가중치 추론과 공식 벤치마크를 실행하지 않았습니다.

[모델·도구 분석](../README.md) · [메모리·증류·양자화 실험](../../experiments/README.md)

## English

The selected distilled checkpoint is a Qwen-based dense student, not a smaller copy of the original R1 MoE. The official configuration gives a 0.109375 GiB BF16 KV payload at 4,096 cached tokens and batch one. This is calculated array storage, not measured GPU usage. A separate six-parameter student experiment illustrates probability-target learning; it does not reproduce DeepSeek training, model inference, or official benchmarks.
