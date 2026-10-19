# AI 응용·에이전트·평가 | AI Applications, Agents & Evaluation

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

AI 응용은 모델 호출에 데이터 검색, 도구 실행, 사용자 인터페이스, 오류 처리, 평가를 연결한 구조다. 모델 지식과 외부 자료·도구에서 얻은 정보를 구분해 두면 오류가 어디서 생겼는지 찾기 쉽다.

## API와 도구 실행

Structured output은 출력 형식을 schema와 연결하고, function calling은 모델이 요청한 도구 이름·인자를 애플리케이션이 처리하는 구조다. 실제 파일 변경이나 외부 동작은 모델의 문장 생성과 별도의 실행 단계다. Agent는 관찰·계획·도구 호출·상태 갱신을 반복하는 형태로 구성될 수 있다. MCP는 도구·자료와 애플리케이션을 연결하는 프로토콜이다.

## RAG와 workflow

RAG는 검색한 자료를 생성 과정의 문맥으로 제공한다. 문서 분할·embedding·retrieval·reranking·인용 연결이 답변 품질에 영향을 준다. 검색이 틀린 경우와 검색 자료를 잘못 해석한 경우는 다른 오류다. LangChain·LlamaIndex·DSPy는 이런 응용을 구성하는 데 쓰인다.

## 평가 항목

정확성, 근거 일치, 한국어·영어 응답 품질, tool 성공률, latency, token·API 비용을 나누어 본다. lm-evaluation-harness·Ragas·promptfoo는 서로 다른 평가 작업에 쓰인다. Prompt나 모델 버전 변경 후 같은 질문 집합을 다시 실행하면 개선과 회귀를 비교할 수 있다.

## 관련 기술

OpenAI APIs, Claude API, Gemini API, LangChain, LlamaIndex, DSPy, MCP, lm-evaluation-harness, Ragas, promptfoo

## 참고 자료

- [OpenAI model documentation](https://developers.openai.com/api/docs/models)
- [Hugging Face documentation](https://huggingface.co/docs)

## 기초 해설

- [RAG와 도구 실행: 검색, 근거, 평가의 경계](해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md)

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

- [RAG와 도구 실행: 검색, 근거, 평가의 경계](해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md#english)
