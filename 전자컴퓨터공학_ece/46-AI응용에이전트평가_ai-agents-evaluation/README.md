# AI 응용·에이전트·평가 | AI Applications, Agents & Evaluation

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

AI 응용은 모델 호출에 데이터 검색, 도구 실행, 사용자 인터페이스, 오류 처리, 평가를 연결한 구조입니다. 모델 지식과 외부 자료·도구에서 얻은 정보를 구분해 두면 오류가 어디서 생겼는지 찾기 쉽습니다.

## API와 도구 실행

Structured output은 출력 형식을 schema와 연결하고, function calling은 모델이 요청한 도구 이름·인자를 애플리케이션이 처리하는 구조입니다. 실제 파일 변경이나 외부 동작은 모델의 문장 생성과 별도의 실행 단계입니다. Agent는 관찰·계획·도구 호출·상태 갱신을 반복하는 형태로 구성될 수 있습니다. MCP는 도구·자료와 애플리케이션을 연결하는 프로토콜입니다.

## RAG와 workflow

RAG는 검색한 자료를 생성 과정의 문맥으로 제공합니다. 문서 분할·embedding·retrieval·reranking·인용 연결이 답변 품질에 영향을 줍니다. 검색이 틀린 경우와 검색 자료를 잘못 해석한 경우는 다른 오류입니다. LangChain·LlamaIndex·DSPy는 이런 응용을 구성하는 데 쓰입니다.

## 평가 항목

정확성, 근거 일치, 한국어·영어 응답 품질, tool 성공률, latency, token·API 비용을 나누어 봅니다. lm-evaluation-harness·Ragas·promptfoo는 서로 다른 평가 작업에 쓰입니다. Prompt나 모델 버전 변경 후 같은 질문 집합을 다시 실행하면 개선과 회귀를 비교할 수 있습니다.

## 관련 기술

OpenAI APIs, Claude API, Gemini API, LangChain, LlamaIndex, DSPy, MCP, lm-evaluation-harness, Ragas, promptfoo

## 참고 자료

- [OpenAI model documentation](https://developers.openai.com/api/docs/models)
- [Hugging Face documentation](https://huggingface.co/docs)

## 기초 해설

- [모델 평가 지표: 정확도·정밀도·재현율·속도·메모리](해설_notes/모델평가지표_MODEL_EVALUATION.md)
- [RAG와 도구 실행: 검색, 근거, 평가의 경계](해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md)

## 불량 비율과 경보의 정밀도

경보를 검토할 때에는 전체 정확도뿐 아니라 “경보 중 실제 대상이 몇 개인가”를 봅니다. Precision은 `TP/(TP+FP)`로 경보 전체를 분모로 합니다. Recall은 `TP/(TP+FN)`로 실제 불량 전체를, FPR은 `FP/(FP+TN)`로 실제 정상 전체를 분모로 합니다. FPR 10%가 경보의 10%만 오경보라는 뜻은 아닙니다.

[고정 점수의 실행 사례](../../설계와검증사례_engineering-cases/불량비율과경보의정밀도_ai-prevalence-precision.md)에서는 TPR 0.9·FPR 0.1을 같게 정하고 실제 불량 비율을 50%에서 1%로 바꿨습니다. A는 200행에서 TP 90·FP 10, B는 1,000행에서 TP 9·FP 99입니다. Precision은 90%에서 약 8.33%로 달라지며 경보는 각각 100개·108개입니다. 표본 수가 다르므로 경보 비율 50%·10.8%도 함께 기록했습니다. Accuracy가 둘 다 90%인 것은 TPR와 TNR을 모두 0.9로 정했기 때문이며 일반 법칙이 아닙니다.

기저율은 집합 전체에서 대상이 원래 나타나는 비율입니다. 실제 새 공장에서는 class별 점수 분포까지 달라질 수 있으므로, 이 합성 대조를 배포처의 성능 보장으로 쓰지 않습니다. 점수 0.8도 보정된 불량 확률 80%라는 뜻이 아닙니다. label이 하나라도 미상이면 전체 성능과 비용을 미확정으로 두되, 점수에서 셀 수 있는 경보 수는 남깁니다. 경보가 없어 precision의 분모가 0이면 값은 None입니다.

예제의 FP당 1·FN당 20이라는 자체 비용은 A 210·B 119, 표본당 1.05·0.119입니다. 실제 금액·인건비·안전 위험이 아닙니다. 비용의 절대 합계나 accuracy 하나로 서로 다른 모집단을 순위 매기지 않습니다. 평가 정답으로 threshold를 다시 골라 같은 집합을 최종 성능으로 보고하는 호출은 거부합니다. [코드와 입력 계약](../../예제_examples/실무검증_practical-validation/ai_prevalence/README.md), [실제 실행·오류 변이 기록](../../설계와검증사례_engineering-cases/검증기록_evidence/기저율과경보업무량검사_20261021.md)을 함께 볼 수 있습니다.

## English

### AI applications, agents, and evaluation

An AI application connects model calls to retrieval, tool execution, a user interface, error handling, and evaluation. Separating model knowledge from information obtained through external sources and tools makes it easier to identify where a failure occurred.

### APIs and tool execution

Structured output constrains a response through a schema. With function calling, an application handles the tool name and arguments requested by a model. Changing a file or performing an external action is an execution step separate from generating text. An agent can repeatedly observe, plan, call tools, and update state. MCP is a protocol for connecting tools and resources to applications.

### RAG and workflows

Retrieval-augmented generation supplies retrieved material as context for generation. Document chunking, embeddings, retrieval, reranking, and citation links all affect answer quality. Retrieving the wrong material and misinterpreting correctly retrieved material are distinct errors. LangChain, LlamaIndex, and DSPy support the construction of these applications.

### What to evaluate

Evaluation can separate correctness, agreement with evidence, Korean and English response quality, tool success rates, latency, and token or API cost. lm-evaluation-harness, Ragas, and promptfoo serve different evaluation tasks. Running the same question set after a prompt or model-version change helps identify improvements and regressions.

The related APIs and tools include OpenAI APIs, Claude API, Gemini API, LangChain, LlamaIndex, DSPy, MCP, lm-evaluation-harness, Ragas, and promptfoo.

### Foundation article

- [Model evaluation metrics: quality, speed and memory](해설_notes/모델평가지표_MODEL_EVALUATION.md#english)
- [RAG와 도구 실행: 검색, 근거, 평가의 경계](해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md#english)


### Alert precision and defect prevalence

Precision divides true positives by all alerts, whereas recall divides by actual positives and FPR divides by actual negatives. In the [synthetic fixed-score case](../../설계와검증사례_engineering-cases/불량비율과경보의정밀도_ai-prevalence-precision.md#english), TPR 0.9 and FPR 0.1 remain fixed while prevalence changes from 50% to 1%. Precision changes from 90/100 to 9/108; there are 100 alerts among 200 rows and 108 among 1,000. Accuracy stays at 0.9 here only because TPR and TNR are both 0.9.

Unknown labels leave all label-dependent cohort metrics and losses unestablished, while observable alert counts remain available. A zero denominator gives a None value. Scores are not calibrated probabilities. The assigned loss `FP + 20*FN` and the count of review items are educational quantities, not monetary, labor, or safety measurements. The example rejects threshold selection using evaluation answers and does not change existing training data or checkpoints.

## 심화 해설 | Advanced article

- [Macro·micro 지표와 평가의 불확실성](해설_notes/평가지표와불확실성_metrics-uncertainty.md) · [English](해설_notes/평가지표와불확실성_metrics-uncertainty.md#english)
