# 프롬프트와 검색 자료 | LLM and RAG security

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 자료가 명령처럼 해석되는 경계

프롬프트 주입은 공격자가 제어하는 입력이 시스템의 의도와 충돌하는 지시로 작용하는 문제입니다. 사용자가 직접 보내는 경우와 웹·PDF·메일·코드 주석·검색 결과에 숨긴 내용이 읽히는 간접 주입을 구분합니다. 모델이 원문 내용을 정확하게 요약하더라도 원문 안의 실행 지시를 자신의 권한으로 받아들이면 문제가 됩니다. [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

문서 상담 서비스가 ‘문서에 적힌 외부 주소로 결과를 전송하라’는 내용을 읽는 상황을 생각해 봅니다. 문서 작성자는 참고 자료를 바꿀 수 있는 권한만 있어도 서비스의 외부 전송 권한을 간접 사용하려 합니다. ‘이 문서는 신뢰하지 않습니다’라는 프롬프트는 도움이 될 수 있지만, 실제 네트워크·자료 접근을 제어하는 서버 정책을 대신하지 않습니다.

## RAG에는 검색 전과 생성 후의 검사가 필요합니다

RAG는 외부 자료를 검색해 모델 입력에 붙이는 구조입니다. 벡터 유사도는 내용이 관련되는 정도이지 읽기 권한이 아닙니다. 고객·문서 ACL을 검색 시 적용하고, 캐시와 인덱스의 권한 변경·삭제 반영도 관리합니다. 결과에서 숨겨도 이미 모델 입력에 들어갔다면 노출 경계는 지난 것입니다.

| 단계 | 확인할 조건 | 예시 실패 |
| --- | --- | --- |
| 수집 | 원문 출처·수집 권한·문서 판본을 남깁니다. | 신뢰한 사이트의 사용자 댓글까지 같은 신뢰로 묶습니다. |
| 인덱싱 | 조직·문서 ID·ACL·삭제 상태를 보존합니다. | chunk를 나누면서 조직 식별자를 버립니다. |
| 검색 | 인증 주체의 읽기 권한으로 필터링합니다. | 답변에서만 필터링합니다. |
| 생성 | 외부 자료와 실행 지시의 역할을 분리합니다. | 검색 문서가 관리자 메시지 역할을 대신합니다. |
| 출력 | 출처·민감정보·출력 문맥·도구 인수를 검사합니다. | 모델 문자열을 HTML·shell 코드로 실행합니다. |

## 방어는 여러 층의 조건입니다

입력 검사·프롬프트 구조·위험 신호 탐지는 보조층입니다. 실행기는 허용한 도구·인수·대상·행위만 받고, 비밀은 모델 문맥에서 줄이며, 외부 전송 경로를 제한합니다. 정규식 금칙어만으로 자연어의 우회 표현을 모두 막는다고 주장하지 않습니다.

출처 링크가 붙었다고 답변의 모든 문장이 근거를 갖는 것은 아닙니다. 실제 인용 구간이 주장을 뒷받침하는지, 다른 문서의 명령을 인용해 실행하려는지 구분합니다. 출력은 HTML 텍스트인지 코드인지 파일 경로인지에 따라 다르게 처리합니다. [XSS의 출력 문맥](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

## 검사할 입력과 지표

정상 문서, 지시문을 인용한 교육 문서, 악의적 지시가 있는 문서, 다른 조직 문서, 삭제·권한 변경 문서, 상충하는 판본을 각각 시험합니다. 거부율만 높이면 정상 검색도 망가질 수 있으므로 정상 작업 성공률과 권한 위반률을 함께 봅니다. 이 카테고리의 실습은 LLM을 실행하지 않으며 모델의 주입 저항률을 측정한 결과도 아닙니다. 대신 모델이 잘못 제안했을 때 실행기가 거부하는 경계를 검사합니다.

## OWASP LLM Top 10:2026을 시스템 경계에 연결합니다

OWASP의 2026판은 2025판과 항목 구성·순서가 달라졌습니다. 이를 실제 발생 빈도의 순위나 한 제품의 결함 목록으로 읽지 않습니다. 각 항목을 시스템 설계의 점검 질문으로 옮깁니다. 공식 목록은 [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)과 [정식 GitHub 원고](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/README.md)에서 확인할 수 있습니다.

| OWASP 항목 | 설계에서 확인할 질문 |
| --- | --- |
| LLM01 Prompt Injection | 사용자·검색·도구 결과의 지시가 실행 경계를 바꾸나요? |
| LLM02 Sensitive Information Disclosure | 문맥·출력·로그·캐시에서 다른 주체 자료가 노출되나요? |
| LLM03 Excessive Agency | 모델이 필요한 범위를 넘어 도구·자원에 접근하나요? |
| LLM04 Supply Chain | 모델·데이터·도구·빌더의 출처와 판본을 확인할 수 있나요? |
| LLM05 Data and Model Poisoning | 학습·검색·평가 데이터의 변경과 출처를 추적하나요? |
| LLM06 Unbounded Consumption | 입력·반복 호출·출력 크기·비용에 상한이 있나요? |
| LLM07 Misinformation | 검증되지 않은 답변이 결정·업무 실행으로 이어지나요? |
| LLM08 Hidden Context Exposure | 시스템 지시·숨은 문맥·다른 대화가 응답에 드러나나요? |
| LLM09 Vector and Embedding Weaknesses | 유사도 검색과 문서 ACL·삭제·테넌트 경계가 분리되어 있나요? |
| LLM10 Improper Output Handling | 출력 문자열이 HTML·명령·쿼리·파일 경로로 실행되나요? |

RAG에서는 검색 전에 인증 주체로 접근 가능한 문서만 필터링하고, 검색 후에는 원문 판본·문서 ID·인용 구간을 답변과 연결합니다. 유사도 점수는 읽기 권한이 아니며, 임베딩 인덱스에서 결과를 숨기는 것만으로 모델 입력에 이미 들어간 자료를 되돌릴 수 없습니다. 시스템 지시를 비밀로 숨기는 것보다 접근 통제·최소 수집·출력 검사·감사 기록을 신뢰 경계에서 집행합니다.

## 원문에서 이어 읽기

- [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html): 직접·간접 주입·도구 권한·다층 방어 절입니다.
- [OWASP Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html): 출력 문맥·인코딩·safe sinks 절입니다.
- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): 최소권한·기본 거부·매 요청 검사 절입니다.

## English

RAG relevance is not authorization. Prompt defenses need retrieval access controls, constrained tools and output handling at enforced boundaries.
