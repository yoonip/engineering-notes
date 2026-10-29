# AI 모델 동향과 분석 | AI model releases and analysis

새로운 주요 모델의 발표와 실제 제공 범위를 한국어로 읽습니다. 출시 날짜, API·공개 가중치의 차이, 이전 판본에서 달라진 기능과 비용, 평가 조건을 함께 정리합니다. 프론티어는 이 글들에서 복잡한 추론·코딩·도구 사용·다중모달 과제를 다루는 주요 모델을 가리키며, 하나의 시험으로 확정한 종합 순위는 아닙니다.

자료 확인 기준일은 2026년 10월 29일입니다. 각 글은 확인한 발표·판본을 다루며, 뒤의 새 모델이 나오더라도 이전 판본의 설명과 날짜를 구분해 읽을 수 있도록 구성했습니다.

[모델 발표](새소식_updates/README.md)에는 공식 자료의 새 소식과 한국어 개요를 날짜별로 모읍니다. 매시간 확인하며 같은 원문은 반복 게시하지 않습니다. 아래 모델별 분석은 각 판본을 별도로 검토한 해설입니다.

## 모델별 분석

| 개발사·모델 | 발표·확인 시점 | 분석에서 다루는 변화 |
| --- | --- | --- |
| [OpenAI GPT-6 Astra](모델별/GPT6아스트라의장기작업과도구사용_gpt-6-astra.md) | API 출시 2026-09-03 | 긴 작업과 도구 사용, 모델 판단과 실제 실행의 경계 |
| [OpenAI GPT-6.1 Sol](모델별/GPT61솔의단가와작업완료비용_gpt-6-1-sol.md) | API 출시 2026-09-29 | 단가와 완료한 업무의 비용, API와 제품 기본 문맥의 차이 |
| [Anthropic Claude Fable 5.1](모델별/클로드페이블51의추론과제공범위_claude-fable-5-1.md) | API 문서의 출시일 2026-09-01 | 어려운 추론 과제, Opus와의 용도·비용 차이, 제한 제공 모델과의 구분 |
| [Anthropic Claude Opus 5.5](모델별/클로드오퍼스55의장기작업과캐시비용_claude-opus-5-5.md) | 2026-09-22 | 장기 작업의 상태 보존과 캐시 비용, 발표 절감률의 뜻 |
| [Google Gemini 4 Argon](모델별/제미나이4아르곤의긴문맥과출력_gemini-4-argon.md) | 제한 제공 2026-09-30, 일반 제공 2026-10-13 | 긴 문맥·출력 예산과 실제 자료 처리 조건 |
| [DeepSeek-V4.1-Flash-1017](모델별/DeepSeek의입력처리와캐시절감_deepseek-v41-flash-1017.md) | V4.1 발표 2026-09-10, 갱신 2026-10-17 | 입력 처리와 생성 단계, KV 캐시와 배포 판본 |
| [Qwen3.8-Max](모델별/Qwen의공개가중치와서비스사양_qwen38-max.md) | 서비스 발표 2026-08-03 | 공개 가중치·서비스 사양과 이용 조건의 차이 |
| [GLM-5.3](모델별/GLM의후속학습과평가조건_glm53.md) | 2026-10-29 배포물 확인 | 후속 학습과 평가 예산, 공개 배포물의 개별 라이선스 |
| [Kimi K3.1 Pro](모델별/Kimi의서비스출시와가중치공개예정_kimi-k31-pro.md) | 2026-10-24 | 서비스 출시와 가중치 공개 예정, 반복 평가의 해석 |

발표일을 확인하지 못한 배포물에는 확인일을 사용했습니다. 공개 예정과 이미 내려받을 수 있는 가중치를 같은 상태로 표시하지 않습니다. 출시 이후 API alias나 모델 카드가 바뀔 수 있으므로 각 글의 확인 범위와 공식 링크를 함께 읽습니다.

## 성능과 비용을 읽는 방법

[모델 발표를 읽는 방법](모델발표를읽는방법_reading-model-releases.md)에서 문맥 창, 추론 설정, MoE, 도구 연결과 벤치마크 조건을 짧은 예제로 설명합니다. 숫자가 높은 이유가 모델의 변화인지, 재시도·추론량·도구 조건의 차이인지 구분하는 데 초점을 둡니다.

모델별 글은 공식 발표·카드·설정·라이선스를 읽은 분석입니다. 개발사가 보고한 평가와 설명용 계산을 구분했습니다. 별도의 API 실행이나 벤치마크 재현은 수행하지 않았습니다.

## 공식 발표를 찾는 곳

| 개발사 | 공식 자료 |
| --- | --- |
| OpenAI | [API 변경 기록](https://developers.openai.com/api/docs/changelog) · [모델 문서](https://developers.openai.com/api/docs/models) |
| Anthropic | [출시 소식](https://www.anthropic.com/news) · [현재 모델과 제공 범위](https://platform.claude.com/docs/en/models/overview) |
| Google DeepMind | [Gemini](https://deepmind.google/models/gemini/) · [모델 카드](https://deepmind.google/models/model-cards/) |
| DeepSeek | [공식 변경 기록](https://api-docs.deepseek.com/updates/) · [공식 가중치](https://huggingface.co/deepseek-ai) |
| Qwen | [공식 발표](https://qwen.ai/blog) · [공식 가중치](https://huggingface.co/Qwen) |
| Z.ai | [GLM-5.3 발표](https://z.ai/blog/glm-5.3) · [공식 저장소](https://github.com/zai-org/GLM-5) · [공식 가중치](https://huggingface.co/zai-org) |
| Moonshot AI | [Kimi 연구·발표](https://www.kimi.com/en/blog/) · [공식 가중치](https://huggingface.co/moonshotai) |

각 경로에서 새 발표와 배포물을 찾을 수 있으며, 이 저장소에서 다룬 판본과 확인일은 위의 분석 목록에 표시합니다.

## 기존 자료와 함께 읽기

- [AI 모델과 수치 실험](../AI모델과수치실험_ai-models/README.md): 특정 공개 모델의 구조·실행 형식, 별도의 교육용 계산입니다.
- [기술 동향](../기술동향_technology/README.md): 하드웨어·표준·시스템 벤치마크의 변화입니다.
- [미래·경제 보고서](../미래경제보고서_future-economic-reports/README.md): AI 투자와 생산성, 전력·인력·산업 정책의 중장기 조건입니다.

## English

These Korean release studies track dated model announcements, access conditions, public weights, evaluation settings and practical costs. Provider results, illustrative calculations and direct measurements are kept separate. Official source links accompany each study.

[처음으로](../README.md)
