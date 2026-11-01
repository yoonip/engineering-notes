# 음성·에이전트·디자인·역공학 프로젝트 | Projects to explore

음성 도구, 코딩 에이전트 스킬, 디자인, 영상 제작과 바이너리 분석 프로젝트를 소개합니다. 아래 목록은 분야별로 살펴볼 프로젝트이며 월간 순위가 아닙니다.

원본·메타데이터 확인 시각: 2026-11-02T08:56:08+09:00

## debpalash/VoiceStudio

음성 복제·음성 생성·영상 더빙·받아쓰기·오디오북 제작을 한 작업 공간에서 다루는 로컬 음성 도구입니다.

필요한 음성 엔진과 모델을 골라 내려받고 로컬 API·MCP로 작업을 연결할 수 있습니다. 앱의 AGPL 라이선스와 모델 가중치·음성 자산의 이용 조건은 별도로 확인합니다.

- [저장소](https://github.com/debpalash/VoiceStudio) · [README](https://github.com/debpalash/VoiceStudio#readme) · [소개 근거](https://github.com/debpalash/VoiceStudio#readme)
- 주요 언어: Python · 라이선스: AGPL-3.0
- 누적 별: 97,890개 · 포크: 10,871개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: VoiceStudio is the open-source, fully-local ElevenLabs alternative — voice cloning, voice design, video dubbing, dictation, transcription &amp; audiobook creation in 646 languages.

## DietrichGebert/ponytail

코딩 에이전트가 필요한 변경을 작게 작성하고 기존 해법을 활용하도록 안내하는 스킬·플러그인입니다.

검증·오류 처리·보안·접근성을 유지하면서 불필요한 코드와 작업을 줄이는 개발 원칙을 제공합니다. 기존 시스템에 기능을 추가할 때 변경 범위를 좁히는 흐름을 살펴볼 수 있습니다.

- [저장소](https://github.com/DietrichGebert/ponytail) · [README](https://github.com/DietrichGebert/ponytail#readme) · [소개 근거](https://github.com/DietrichGebert/ponytail#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 182,100개 · 포크: 10,036개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Makes your AI agent think like the laziest senior dev in the room. The best code is the code you never wrote.

## cloudflare/security-audit-skill

코드 구조와 신뢰 경계를 파악하고 취약점 후보 탐색·검증·보고를 단계별로 수행하도록 구성한 보안 감사 스킬입니다.

서로 독립적인 검증 역할, 구조화된 findings.json과 감사 범위 기록을 사용합니다. 어떤 코드를 조사했는지와 취약점 근거가 무엇인지 남기는 흐름을 살펴볼 수 있습니다.

- [저장소](https://github.com/cloudflare/security-audit-skill) · [README](https://github.com/cloudflare/security-audit-skill#readme) · [소개 근거](https://github.com/cloudflare/security-audit-skill#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 56,343개 · 포크: 3,672개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: A coding-agent skill for multi-phase security audits with independently verified, machine-readable findings

## affaan-m/ECC

코딩 에이전트의 계획·테스트·구현·리뷰·검증·기억을 연결하는 스킬과 작업 흐름 모음입니다.

Claude Code·Codex·OpenCode·Cursor 등 여러 환경에서 반복되는 개발 절차를 재사용하도록 구성합니다. 스킬 수를 외우기보다 프로젝트에 필요한 절차와 설정 파일을 골라 읽는 데 적합합니다.

- [저장소](https://github.com/affaan-m/ECC) · [README](https://github.com/affaan-m/ECC#readme) · [소개 근거](https://github.com/affaan-m/ECC#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 294,782개 · 포크: 43,635개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

## pbakaus/impeccable

코딩 에이전트가 화면 디자인을 구체적으로 지시하고 검토할 때 쓰는 디자인 어휘와 명령을 제공합니다.

polish·bolder·critique·audit 같은 작업으로 시각적 방향과 UI 품질을 조정합니다. 디자인 지침과 실제 검토 명령이 어떻게 연결되는지 살펴볼 수 있습니다.

- [저장소](https://github.com/pbakaus/impeccable) · [README](https://github.com/pbakaus/impeccable#readme) · [소개 근거](https://github.com/pbakaus/impeccable#readme)
- 주요 언어: Rust · 라이선스: Apache-2.0
- 누적 별: 99,290개 · 포크: 5,870개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: The design vocabulary for your coding agent. Steer with polish and bolder, review with critique and audit, catch AI slop before it ships.

## heygen-com/hyperframes

HTML·CSS와 시간 탐색이 가능한 애니메이션으로 영상을 작성하고 미리보기·렌더링하는 도구입니다.

에이전트용 스킬이 영상 계획·미디어 배치·검사·렌더링을 안내하며 GSAP·CSS·Lottie·Three.js 등의 애니메이션을 연결할 수 있습니다. 웹 기반 장면을 영상으로 출력하는 구조를 익히는 데 도움이 됩니다.

- [저장소](https://github.com/heygen-com/hyperframes) · [README](https://github.com/heygen-com/hyperframes#readme) · [소개 근거](https://github.com/heygen-com/hyperframes#readme)
- 주요 언어: TypeScript · 라이선스: Apache-2.0
- 누적 별: 77,097개 · 포크: 7,067개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Write HTML. Render video. Built for agents.

## Panniantong/Agent-Reach

웹·소셜·영상 플랫폼의 자료를 읽고 검색해 에이전트에서 다루기 쉽게 연결하는 CLI 도구입니다.

YouTube·Bilibili의 자막과 전사, GitHub 저장소·이슈 등 플랫폼별 입력을 제공합니다. 일부 기능은 인증이나 별도 도구가 필요하며 플랫폼마다 지원 범위가 다릅니다.

- [저장소](https://github.com/Panniantong/Agent-Reach) · [README](https://github.com/Panniantong/Agent-Reach#readme) · [소개 근거](https://github.com/Panniantong/Agent-Reach#readme)
- 주요 언어: Python · 라이선스: MIT
- 누적 별: 107,596개 · 포크: 9,593개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Give your AI agent eyes to see the entire internet. Read &amp; search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu — one CLI, zero API fees.

## NationalSecurityAgency/ghidra

NSA 연구부서가 만들고 유지하는 소프트웨어 역공학 프레임워크입니다.

컴파일된 실행 파일을 디스어셈블·디컴파일하고 제어 흐름 그래프와 스크립팅으로 분석합니다. Windows·macOS·Linux에서 바이너리 분석 구조와 디컴파일 결과를 공부할 때 활용할 수 있습니다.

- [저장소](https://github.com/NationalSecurityAgency/ghidra) · [README](https://github.com/NationalSecurityAgency/ghidra#readme) · [소개 근거](https://github.com/NationalSecurityAgency/ghidra#readme)
- 주요 언어: Java · 라이선스: Apache-2.0
- 누적 별: 96,768개 · 포크: 10,927개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Ghidra is a software reverse engineering (SRE) framework

## Leonxlnx/taste-skill

웹사이트와 앱 화면을 만들 때 코딩 에이전트에 미술적 방향·참고 이미지·브라우저 확인 절차를 제공하는 디자인 스킬입니다.

실제 이미지를 참고해 방향을 정하고 구현한 화면을 브라우저에서 확인하는 흐름을 제공합니다. 설치 환경은 저장소의 현재 요구사항에서 확인할 수 있습니다.

- [저장소](https://github.com/Leonxlnx/taste-skill) · [README](https://github.com/Leonxlnx/taste-skill#readme) · [소개 근거](https://github.com/Leonxlnx/taste-skill#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 107,759개 · 포크: 7,279개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Agent skills that give coding agents taste: art direction, reference images and a browser check instead of generic AI pages

## tashfeenahmed/freellmapi

여러 LLM 제공자의 무료 사용 구간과 사용자 지정 엔드포인트를 하나의 OpenAI 호환 API에 연결하는 라우터입니다.

제공자가 제한에 걸리면 다음 제공자로 전환하고 키별 사용량을 추적합니다. 무료 범위와 이용 조건은 각 제공자에 따르며, 제작자는 개인 실험·학습 용도로 설명합니다.

- [저장소](https://github.com/tashfeenahmed/freellmapi) · [README](https://github.com/tashfeenahmed/freellmapi#readme) · [소개 근거](https://github.com/tashfeenahmed/freellmapi#readme)
- 주요 언어: TypeScript · 라이선스: MIT
- 누적 별: 45,707개 · 포크: 6,241개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: 7.4 billion tokens per month. 34 free LLM providers. 635 free model endpoints. All behind one /v1 endpoint, plus any custom OpenAI-compatible endpoint. Smart routing, automatic failover, encrypted keys. Personal experimentation only.

## deepseek-ai/DeepInfer

DeepSeek 모델용 대규모 추론 프레임워크로 최적화 커널·병렬 실행·비동기 스케줄링·구조화 출력을 제공합니다.

공개판은 오프라인 추론을 중심으로 하며 완전한 서비스에는 KV 캐시·분리형 서빙·부하 분산 등의 추가 구성이 필요합니다. 지원 모델과 GPU·가속기 조건은 공식 README에서 확인합니다.

- [저장소](https://github.com/deepseek-ai/DeepInfer) · [README](https://github.com/deepseek-ai/DeepInfer#readme) · [소개 근거](https://github.com/deepseek-ai/DeepInfer#readme)
- 주요 언어: Python · 라이선스: Apache-2.0
- 누적 별: 24,808개 · 포크: 3,010개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: DeepInfer: High-performance, large-scale inference framework for DeepSeek models

[주간 Trending 기록](주간기록/README.md) · [전체 안내](README.md)
