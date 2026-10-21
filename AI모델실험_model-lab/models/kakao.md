# 위치 확장과 모델 계보: Kanana 1.5 2.1B | Position scaling and architecture

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `kakaocorp/kanana-1.5-2.1b-instruct-2505` |
| 제공·입출력 | 공개 가중치 · 한국어·영어 텍스트 |
| 구조·설정 | Dense 언어 모델 · 기본 32k / YaRN 확장 안내 |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

공식 config에는 `LlamaForCausalLM`, 32층, Q/KV 헤드 24/8, `head_dim=128`이 있습니다. 구현 클래스가 Llama라는 사실만으로 Meta 체크포인트를 추가 학습했다고 단정할 수는 없습니다. 구조의 호환성과 가중치의 학습 계보는 다른 근거가 필요한 주장입니다.

[공식 설정 파일](https://huggingface.co/kakaocorp/kanana-1.5-2.1b-instruct-2505/raw/main/config.json)과 [1.5 카드](https://huggingface.co/kakaocorp/kanana-1.5-2.1b-instruct-2505#kanana-15)를 함께 읽습니다. 카드의 후속 학습과 YaRN 확장을 구분하며, 이전 Kanana 논문 전체를 2505 배포물의 모든 학습 설정과 동일시하지 않습니다. 이 글에서는 실제 생성과 재학습을 하지 않았습니다.

모델 카드는 기본 32k와 YaRN을 통한 최대 128k 확장을 구분합니다. 위치 인코딩을 확장하는 설정은 긴 입력의 모든 정보를 정확히 활용한다는 증명과 다릅니다. 기능 호출도 형식이 맞는지와 실제 의도가 맞는지를 나누어 봐야 합니다.

## 실행에 필요한 조건과 비교 항목

공식 template과 확장 여부를 명시합니다. 기본 길이 이내의 문서와 길이 확장 문서를 따로 비교하고 근거 회수율을 기록합니다. 한국어 도구 설명을 영어로 바꿨을 때 선택과 인자가 유지되는지도 확인할 수 있습니다.

## 공개 범위와 한계

외부 도구의 설명·schema·결과 포맷이 바뀌면 모델이 같아도 결과가 달라질 수 있습니다. 이 문서에서는 도구 실행이나 장문 성능을 측정하지 않았습니다.

## 기본 문맥과 위치 확장을 나누는 이유

tokenizer는 대화의 역할과 본문을 정수 ID로 바꾸며, 모델은 그 순서의 위치 정보도 이용합니다. YaRN은 긴 위치 범위를 다루기 위한 확장 방식입니다. 입력 문자열을 그냥 길게 붙이는 조작과 같지 않습니다. 기본 설정과 확장 설정은 동일한 입력이라도 비교 조건이 달라지므로 구분해 남겨야 합니다. 이 배포물의 기본 32k와 확장 128k라는 안내가 그 구분의 출발점입니다. [Kanana 1.5의 문맥 설명](https://huggingface.co/kakaocorp/kanana-1.5-2.1b-instruct-2505#kanana-15)

모델 이름의 instruct는 사용자 지시에 맞게 조정된 배포물을 뜻하며, embedding 모델처럼 문장을 고정 길이 검색 벡터로 바꾸는 인터페이스와 구별합니다. 같은 Kanana 계열의 생성·임베딩 배포물을 바꾸어 넣는 것으로 같은 호출 결과를 기대하지 않습니다.

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#kakao)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/kakaocorp/kanana-1.5-2.1b-instruct-2505) · [공식 실행 코드 또는 참고 자료](https://arxiv.org/abs/2502.18934)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Native context and YaRN extension are different settings. Tool selection accuracy and schema validity should not be merged into one impressionistic score. This is a source-based release analysis; model inference was not run locally.
