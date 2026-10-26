# 전문가 선택과 대화 형식: OpenAI gpt-oss-20b | MoE and Harmony

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `openai/gpt-oss-20b` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | MoE · 전체 약 21B / 활성 약 3.6B |
| 사용 조건의 표기 | Apache 2.0 |

## 구조와 용도

MoE(mixture of experts)는 모든 내부 계산망을 매 토큰에 전부 쓰는 대신 일부 전문가 망을 선택하는 구조입니다. 전문가 망은 외부 검색 도구가 아니라 학습된 가중치의 일부입니다. 따라서 모델 내부 라우팅과 응답에 나타나는 함수 호출은 다른 동작입니다. 공개된 gpt-oss의 형식·가중치 설명을 비공개 GPT 서비스의 구조로 옮기지 않습니다.

이 글에서 확인한 [공식 구현 안내](https://developers.openai.com/cookbook/articles/gpt-oss/verifying-implementations)는 Harmony 입력, 도구 사이의 메시지 보존, MXFP4에 맞는 실행 코드를 다룹니다. 학습 데이터 전체를 다시 모아 원 모델을 훈련한 기록은 이 저장소에 없습니다. 공식 구현 문서와 로컬 교육용 계산의 범위는 다릅니다.

토큰마다 활성화되는 파라미터가 적어도 모든 전문가의 가중치를 저장해야 합니다. 활성 3.6B를 모델 전체 저장량으로 계산하면 메모리를 크게 잘못 추정하게 됩니다. 공식 실행 안내는 MXFP4를 이용한 20b 모델에 약 16GB VRAM을 제시하며, BF16 경로는 더 많은 메모리를 사용합니다.

## 실행에 필요한 조건과 비교 항목

공식 Transformers 실행 안내에서 하드웨어의 MXFP4 지원과 설치 조건을 확인합니다. 대화는 Harmony 형식으로 구성하며, reasoning effort와 출력 토큰 수를 고정해 비교합니다. 모델이 도구 호출 형식을 생성하는 일과 실제 프로그램을 실행하는 일은 구분합니다.

## 공개 범위와 한계

이 수치는 공식 안내의 조건이며 이 저장소에서 측정한 값이 아닙니다. 같은 이름의 hosted API 설정을 로컬 실행 설정에 그대로 적용할 수는 없습니다.

## Harmony는 답변의 경계를 정하는 형식입니다

Harmony에는 누가 말했는지 나타내는 역할과, 어떤 종류의 메시지인지 나타내는 채널이 있습니다. `analysis`와 사용자에게 전달할 `final`, 도구로 넘기는 호출을 한 문자열로 합치면 최종 답과 실행 요청을 구분하기 어렵습니다. 메시지 끝, 사용자 응답 완료, 도구로 제어를 넘기는 경계도 서로 다른 뜻입니다. [OpenAI 공식 Harmony 설명](https://developers.openai.com/cookbook/articles/openai-harmony)

로컬 가중치는 이런 형식의 토큰을 생성하고, 도구 실행기는 요청을 해석해 실제 프로그램을 호출한 뒤 결과를 다시 대화에 연결합니다. 모델의 출력만으로 인터넷 검색이나 Python 실행이 자동으로 이루어졌다고 판단하지 않습니다. 최종 채널의 답을 평가하고 내부 처리·도구 요청은 해당 역할로 분리하는 것이 입력·출력 계약을 읽는 방법입니다.

## 가중치 저장량의 근사

저장량도 별도로 계산할 수 있습니다. 전체 21B를 모두 2바이트로 둔 자체 근사는 42,000,000,000바이트이고 활성 3.6B만 곱한 7,200,000,000바이트와 다릅니다. 이는 BF16 가중치 본문을 이해하는 산술이며 실제 배포 형식이나 최고 VRAM의 측정값이 아닙니다. MXFP4는 일부 연산·가중치 표현과 실행 지원을 함께 고려해야 하므로 모든 매개변수를 단순히 4비트로 곱해 장치에 들어간다고 판정하지 않습니다. [공식 Transformers 실행 조건](https://developers.openai.com/cookbook/articles/gpt-oss/run-transformers)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#openai)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://developers.openai.com/api/docs/models/gpt-oss-20b) · [공식 실행 코드 또는 참고 자료](https://developers.openai.com/cookbook/articles/gpt-oss/run-transformers)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

The total and active parameter counts describe different resource costs. Harmony formatting and MXFP4 hardware support matter when reproducing local inference. This is a source-based release analysis; model inference was not run locally.
