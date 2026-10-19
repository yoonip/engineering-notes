# DeepSeek-R1-Distill

DeepSeek-R1은 추론 능력과 강화학습을 다루는 모델 계열이다. R1-Distill은 R1에서 생성한 데이터를 활용해 다른 기반 모델을 조정한 checkpoint들이다. 원본 R1과 같은 구조의 작은 복사본이라는 뜻은 아니다.

## 원본과 distill 모델

공식 release에는 Qwen·Llama 기반 distill 모델이 포함된다. 기반 구조와 parameter 수가 달라 tokenizer·context·추론 메모리·지원 runtime도 영향을 받는다. 모델 이름의 R1이라는 공통 표기만으로 자원 요구를 판단할 수 없다.

## 실행 메모리

가중치의 단순 저장 크기는 대략 `파라미터 수 × 파라미터당 byte`다. 실제 실행에는 KV cache·activation·workspace·runtime 상태가 추가된다. Context length와 batch가 늘어나면 가중치가 같아도 메모리 사용이 늘 수 있다. 양자화는 저장 표현을 줄이지만 지원 kernel과 수치 오차가 함께 달라진다.

## 생성과 평가

Chat template은 대화를 token sequence로 바꾸고, sampling 설정은 다음 token 선택을 바꾼다. 추론 출력이 길어지면 처리 시간과 메모리 조건도 영향을 받는다. 수학·코드·한국어 설명은 서로 다른 평가 입력과 기준이 필요하다.

[공식 release와 모델 목록](https://github.com/deepseek-ai/DeepSeek-R1) · [AI 기업과 모델](../PROVIDERS.md)
