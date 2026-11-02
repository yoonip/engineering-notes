# 음성·에이전트·디자인·역공학 프로젝트 | Projects to explore

음성 도구, 코딩 에이전트 스킬, 디자인, 영상 제작과 바이너리 분석 프로젝트의 기능·대상 사용자·설치·사용 예시를 소개합니다. 아래 목록은 분야별로 살펴볼 프로젝트이며 월간 순위가 아닙니다.

설치 명령은 공식 문서에서 가져왔으며 이 글을 작성하며 각 프로젝트를 설치·실행한 결과는 아닙니다. 설명용 시나리오는 단계별 사용 흐름을 보여줍니다.

메타데이터 수집 시각: 2026-11-02T08:56:08+09:00

## debpalash/VoiceStudio

음성 복제·음성 생성·영상 더빙·받아쓰기·오디오북 제작을 한 작업 공간에서 다루는 로컬 음성 도구입니다.

필요한 음성 엔진과 모델을 골라 내려받고 로컬 API·MCP로 작업을 연결할 수 있습니다. 앱의 AGPL 라이선스와 모델 가중치·음성 자산의 이용 조건은 별도로 확인합니다.

### 어떤 일을 하나요

- 깨끗한 참조 녹음을 바탕으로 음성을 복제하고, 입력한 문장을 선택한 목소리로 생성합니다.
- 영상 더빙, 받아쓰기·전사와 오디오북 제작을 같은 작업 공간에서 다룹니다.
- Model Manager에서 필요한 엔진과 모델을 선택해 내려받으며, 로컬 API·MCP 연결도 제공합니다.

### 누구에게 유용한가요

- 내레이션·오디오북·영상 더빙용 음성을 로컬에서 만들려는 제작자에게 유용합니다.
- 참조 녹음과 음성 엔진을 바꾸며 결과를 비교하거나 로컬 API로 음성 작업을 연결하려는 개발자에게 적합합니다.

### 설치 방법

준비 사항: 운영체제에 맞는 설치본과 사용할 모델을 저장할 공간이 필요합니다. CPU에서도 작동하지만 엔진과 하드웨어에 따라 생성 속도가 달라집니다. 앱 라이선스와 내려받는 모델·음성 자산의 이용 조건을 각각 확인합니다.

- 공식 Releases에서 운영체제에 맞는 데스크톱 설치본을 받거나, README가 제시하는 설치 스크립트를 사용합니다.
- 아래 코드는 README의 Windows PowerShell 설치 예시입니다. 다른 운영체제에서는 해당 운영체제 절차를 따릅니다.
- 앱을 연 뒤 사용할 엔진·모델을 선택합니다. 모델을 내려받기 전 앱이 확인을 요청합니다.

공식 문서의 명령·예시:

```powershell
irm https://voicestudio.sh/install.ps1 | iex
```

[명령·예시 원문](https://github.com/debpalash/VoiceStudio/blob/1a29929cb87f8ff1470271e6498f0694d395f54d/README.md#get-started)

### 사용 예시

- 본인의 녹음이나 사용 허락을 받은 참조 음성으로 짧은 안내문 내레이션을 만드는 상황을 가정합니다.
- Voice cloning 화면에서 기존 목소리를 고르거나 잡음이 적은 참조 녹음을 추가합니다.
- 읽을 문장을 입력하고 음성을 생성한 뒤, 발음·속도·목소리가 원하는 결과와 맞는지 들어봅니다.
- 영상 더빙이 목적이면 공식 더빙 안내에서 화자별 처리와 더빙 내보내기 흐름을 이어서 확인합니다.

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (1a29929cb87f)](https://github.com/debpalash/VoiceStudio/blob/1a29929cb87f8ff1470271e6498f0694d395f54d/README.md)
- [VoiceStudio 공식 Releases](https://github.com/debpalash/VoiceStudio/releases/latest)
- [앱·모델·음성 자산의 라이선스 구분](https://github.com/debpalash/VoiceStudio/blob/1a29929cb87f8ff1470271e6498f0694d395f54d/LICENSE-NOTICE.md)

### 저장소 정보

- [저장소](https://github.com/debpalash/VoiceStudio) · [README](https://github.com/debpalash/VoiceStudio#readme) · [소개 근거](https://github.com/debpalash/VoiceStudio#readme)
- 주요 언어: Python · 라이선스: AGPL-3.0
- 누적 별: 97,890개 · 포크: 10,871개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: VoiceStudio is the open-source, fully-local ElevenLabs alternative — voice cloning, voice design, video dubbing, dictation, transcription &amp; audiobook creation in 646 languages.

## DietrichGebert/ponytail

코딩 에이전트가 필요한 변경을 작게 작성하고 기존 해법을 활용하도록 안내하는 스킬·플러그인입니다.

검증·오류 처리·보안·접근성을 유지하면서 불필요한 코드와 작업을 줄이는 개발 원칙을 제공합니다. 기존 시스템에 기능을 추가할 때 변경 범위를 좁히는 흐름을 살펴볼 수 있습니다.

### 어떤 일을 하나요

- 관련 코드를 먼저 읽고 기존 해법을 찾아 필요한 만큼 구현하도록 에이전트의 작업 방식을 안내합니다.
- 현재 변경을 검사하는 review, 전체 저장소를 살피는 audit 등 별도 진입점을 제공합니다.
- 강도 설정과 사용 중지 명령이 있으며, 지원되는 Claude Code 환경에서는 작업 비용·시간 등의 표시도 제공합니다.

### 누구에게 유용한가요

- 에이전트가 작은 기능에도 코드를 많이 만들거나 이미 있는 컴포넌트를 다시 작성해 곤란했던 개발자에게 유용합니다.
- 기존 코드의 변경 범위를 좁히면서 오류 처리·테스트·접근성을 유지하려는 팀에 적합합니다.

### 설치 방법

준비 사항: 스킬 또는 플러그인을 지원하는 코딩 에이전트가 필요합니다. 실제 코드 생성은 연결된 에이전트와 모델이 수행합니다. 명령 제공 방식은 호스트마다 다르며, Codex에서는 플러그인 이름공간의 스킬을 사용합니다.

- 아래는 README가 제시하는 Codex용 설치 명령입니다. 두 명령을 차례로 실행합니다.
- 설치 후 Codex의 /hooks에서 생명주기 훅을 확인·신뢰한 뒤 새 대화를 시작합니다.
- 다른 에이전트에서는 공식 INSTALL.md의 해당 호스트 절차를 선택합니다.

공식 문서의 명령·예시:

```sh
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

[명령·예시 원문](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/README.md#install)

### 사용 예시

- 날짜 입력을 추가해야 하는 기존 웹 프로젝트에서 에이전트에게 먼저 관련 입력 컴포넌트와 브라우저 기본 기능을 살펴보도록 요청합니다.
- 구현 후 현재 diff를 대상으로 review를 실행해 버그·보안·부하·누락된 테스트와 불필요한 코드를 확인합니다.
- 아래 명령은 공식 README가 제시하는 Codex의 review 스킬 호출입니다. 호스트에 따라 slash 명령과 호출법이 다릅니다.
- 검토 결과에서 실제 문제와 근거를 읽고 수정하며, 줄 수가 적다는 이유만으로 검증 단계를 생략하지 않습니다.

공식 문서의 명령·예시:

```text
$ponytail:ponytail-review
```

[명령·예시 원문](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/README.md#commands)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (96608e078b2d)](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/README.md)
- [호스트별 설치 안내](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/INSTALL.md)

### 저장소 정보

- [저장소](https://github.com/DietrichGebert/ponytail) · [README](https://github.com/DietrichGebert/ponytail#readme) · [소개 근거](https://github.com/DietrichGebert/ponytail#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 182,100개 · 포크: 10,036개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Makes your AI agent think like the laziest senior dev in the room. The best code is the code you never wrote.

## cloudflare/security-audit-skill

코드 구조와 신뢰 경계를 파악하고 취약점 후보 탐색·검증·보고를 단계별로 수행하도록 구성한 보안 감사 스킬입니다.

서로 독립적인 검증 역할, 구조화된 findings.json과 감사 범위 기록을 사용합니다. 어떤 코드를 조사했는지와 취약점 근거가 무엇인지 남기는 흐름을 살펴볼 수 있습니다.

### 어떤 일을 하나요

- 구조·신뢰 경계·입력면을 파악한 뒤 조사 범위를 나누고, 후보를 독립 검증하는 단계별 감사 흐름을 제공합니다.
- findings.json에 확인·추가 검증 필요·기각 상태를 구분하고, 범위 장부와 결과 보고서를 생성합니다.
- Node.js 검증기로 결과 형식과 범위 기록의 일관성을 확인합니다.

### 누구에게 유용한가요

- 자신이 관리하는 코드의 입력 경계·인증·데이터 격리·의존성 등을 체계적으로 검토하려는 개발자와 보안 담당자에게 유용합니다.
- 발견한 취약점 후보를 근거와 함께 기록하고 다른 검증자가 재확인할 수 있게 만들려는 팀에 적합합니다.

### 설치 방법

준비 사항: 도구 사용과 병렬 하위 에이전트를 지원하는 모델·코딩 에이전트가 필요합니다. 결과·범위 검증기를 실행할 Node.js와 검사할 코드베이스가 필요합니다.

- Skills CLI를 통해 아래 명령으로 security-audit 스킬을 설치합니다.
- 사용할 에이전트 선택과 비대화형 설치 옵션은 npx skills --help에서 확인합니다.
- 검사할 프로젝트 디렉터리에서 에이전트를 시작하거나 해당 코드베이스를 대상으로 지정합니다.

공식 문서의 명령·예시:

```sh
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit
```

[명령·예시 원문](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#installation)

### 사용 예시

- 프로젝트의 src 경로를 먼저 검사하려는 상황에서는 아래의 공식 요청 예시를 에이전트에 입력합니다.
- 에이전트가 파악한 구조·입력면·조사 범위를 확인하고, 후보별 코드 위치와 검증 결과를 읽습니다.
- findings.json과 보고서에서 confirmed·needs\_validation·rejected를 구분합니다. 미해결 후보를 확정된 취약점으로 취급하지 않습니다.

공식 문서의 명령·예시:

```text
find security vulnerabilities in ./src
```

[명령·예시 원문](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md#usage)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (c1c8a8c14710)](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md)
- [공식 스킬·검증기 파일](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit)

### 저장소 정보

- [저장소](https://github.com/cloudflare/security-audit-skill) · [README](https://github.com/cloudflare/security-audit-skill#readme) · [소개 근거](https://github.com/cloudflare/security-audit-skill#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 56,343개 · 포크: 3,672개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: A coding-agent skill for multi-phase security audits with independently verified, machine-readable findings

## affaan-m/ECC

코딩 에이전트의 계획·테스트·구현·리뷰·검증·기억을 연결하는 스킬과 작업 흐름 모음입니다.

Claude Code·Codex·OpenCode·Cursor 등 여러 환경에서 반복되는 개발 절차를 재사용하도록 구성합니다. 스킬 수를 외우기보다 프로젝트에 필요한 절차와 설정 파일을 골라 읽는 데 적합합니다.

### 어떤 일을 하나요

- 계획 수립, 테스트 주도 구현, 코드 리뷰, 빌드 오류 수정 등의 개발 흐름을 스킬과 명령으로 제공합니다.
- 호스트별 플러그인·규칙·훅을 구성하며, 필요한 작업부터 선택해 사용할 수 있습니다.
- 저장소 이름은 affaan-m/ECC, npm 패키지는 ecc-universal, Claude 플러그인 식별자는 ecc@ecc로 구분됩니다.

### 누구에게 유용한가요

- 기능 개발·버그 수정·코드 리뷰를 매번 비슷한 순서로 진행하는 개발자에게 유용합니다.
- 여러 코딩 에이전트에서 계획·테스트·검증·세션 기록을 일정한 방식으로 연결하려는 팀에 적합합니다.

### 설치 방법

준비 사항: 아래 범용 패키지 설치는 Node.js 18 이상이 필요합니다. Claude 플러그인 설정은 Git과 Claude Code 2.1 이상도 PATH에서 사용할 수 있어야 합니다. 아래 setup 예시는 Claude Code용 안내 설치입니다. Codex 등 다른 호스트는 README의 해당 설치 경로를 선택합니다.

- 공식 README가 고정한 패키지 버전의 안내 설치를 실행합니다.
- 설치 마법사에서 적용 범위와 훅 프로필을 선택하고 표시된 변경을 확인합니다.
- 새 Claude Code 세션의 플러그인 목록에서 ecc@ecc가 활성화됐는지 확인합니다. 동일 호스트에 플러그인 설치와 전체 수동 설치를 겹치지 않습니다.

공식 문서의 명령·예시:

```sh
npx ecc-universal@2.2.3 setup
```

[명령·예시 원문](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/README.md#recommended-universal-guided-setup)

### 사용 예시

- OAuth 사용자 인증을 추가하는 프로젝트에서 아래 공식 계획 명령으로 구현 단계를 먼저 정리합니다.
- 생성된 계획을 검토한 뒤 tdd-workflow를 이용해 실패하는 테스트부터 작성하고 기능을 구현합니다.
- 구현 후 code-review 흐름으로 변경을 다시 살피고 회귀 테스트를 확인합니다. 명령의 이름공간은 플러그인 설치와 수동 설치에 따라 다릅니다.

공식 문서의 명령·예시:

```text
/ecc:plan "Add user authentication with OAuth"
```

[명령·예시 원문](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/README.md#start-using-ecc)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (b38be6a7f635)](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/README.md)

### 저장소 정보

- [저장소](https://github.com/affaan-m/ECC) · [README](https://github.com/affaan-m/ECC#readme) · [소개 근거](https://github.com/affaan-m/ECC#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 294,782개 · 포크: 43,635개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

## pbakaus/impeccable

코딩 에이전트가 화면 디자인을 구체적으로 지시하고 검토할 때 쓰는 디자인 어휘와 명령을 제공합니다.

polish·bolder·critique·audit 같은 작업으로 시각적 방향과 UI 품질을 조정합니다. 디자인 지침과 실제 검토 명령이 어떻게 연결되는지 살펴볼 수 있습니다.

### 어떤 일을 하나요

- critique는 사용성과 시각적 완성도를 검토하고, audit는 접근성·성능·테마·반응형 문제를 정리합니다.
- bolder·quieter·polish 등 디자인 방향과 마무리 작업을 구체적인 명령으로 제공합니다.
- 프로젝트 목적을 PRODUCT.md에, 기존 시각 규칙을 DESIGN.md에 기록해 후속 작업이 같은 맥락을 사용하도록 합니다.

### 누구에게 유용한가요

- 화면 구현은 가능하지만 디자인 방향을 말로 구체화하거나 검토하기 어려운 프런트엔드 개발자에게 유용합니다.
- 기존 제품의 가격표·가입 흐름·설정 화면처럼 범위가 분명한 UI를 점검하려는 팀에 적합합니다.

### 설치 방법

준비 사항: npx 설치 경로에는 Node.js가 필요하며, 사용할 코딩 도구가 스킬 또는 플러그인 설치를 지원해야 합니다. 아래 slash 예시는 Claude Code 계열 호출이며 Codex에서는 README가 안내하는 $impeccable 호출을 사용합니다.

- 적용할 프로젝트의 루트 디렉터리에서 아래 설치 명령을 실행합니다.
- 설치 프로그램이 감지한 코딩 도구와 프로젝트·전역 범위를 선택합니다. 훅을 지원하는 호스트에서는 해당 설정도 확인합니다.
- 코딩 도구를 다시 열고 impeccable init을 실행해 프로젝트 목적을 정리합니다. Codex의 훅은 /hooks에서 신뢰해야 적용됩니다.

공식 문서의 명령·예시:

```sh
npx impeccable install
```

[명령·예시 원문](https://github.com/pbakaus/impeccable/blob/e89e3ada3e875a89ac2c5d33d11e65ebef6fe285/README.md#installation)

### 사용 예시

- 가격 요금제 카드의 위계·대비·문구가 불명확한 화면에서 아래 공식 critique 예시를 실행합니다.
- 검토 결과의 우선순위를 읽고 카드 한 영역씩 수정합니다. 전체 사이트를 한 번에 바꾸기보다 대상을 명확히 지정합니다.
- 수정한 화면에서 모바일 배치·키보드 초점·대비를 확인하고, 필요한 경우 audit 또는 polish로 후속 검토합니다.

공식 문서의 명령·예시:

```text
/impeccable critique the pricing cards
```

[명령·예시 원문](https://github.com/pbakaus/impeccable/blob/e89e3ada3e875a89ac2c5d33d11e65ebef6fe285/README.md#why)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (e89e3ada3e87)](https://github.com/pbakaus/impeccable/blob/e89e3ada3e875a89ac2c5d33d11e65ebef6fe285/README.md)

### 저장소 정보

- [저장소](https://github.com/pbakaus/impeccable) · [README](https://github.com/pbakaus/impeccable#readme) · [소개 근거](https://github.com/pbakaus/impeccable#readme)
- 주요 언어: Rust · 라이선스: Apache-2.0
- 누적 별: 99,290개 · 포크: 5,870개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: The design vocabulary for your coding agent. Steer with polish and bolder, review with critique and audit, catch AI slop before it ships.

## heygen-com/hyperframes

HTML·CSS와 시간 탐색이 가능한 애니메이션으로 영상을 작성하고 미리보기·렌더링하는 도구입니다.

에이전트용 스킬이 영상 계획·미디어 배치·검사·렌더링을 안내하며 GSAP·CSS·Lottie·Three.js 등의 애니메이션을 연결할 수 있습니다. 웹 기반 장면을 영상으로 출력하는 구조를 익히는 데 도움이 됩니다.

### 어떤 일을 하나요

- HTML·CSS·미디어와 시간 탐색이 가능한 애니메이션을 MP4로 렌더링합니다.
- CLI로 프로젝트 생성·브라우저 미리보기·영상 출력을 연결하고, 별도 스킬은 계획·작성·검사·렌더링을 안내합니다.
- 기존 웹 애니메이션 라이브러리와 미디어를 시간축에 배치하는 방식으로 영상 장면을 구성합니다.

### 누구에게 유용한가요

- HTML·CSS와 웹 애니메이션 경험을 영상 제작에 활용하려는 개발자에게 유용합니다.
- 제품 소개·자막·차트·모션그래픽을 코드로 구성하고 에이전트와 함께 반복 수정하려는 제작자에게 적합합니다.

### 설치 방법

준비 사항: 아래 수동 CLI 예시는 Node.js 22 이상과 FFmpeg가 필요합니다. 에이전트 스킬을 사용할 경우에는 해당 코딩 에이전트도 별도로 준비합니다. CLI만으로 수동 작업을 시작할 수도 있습니다.

- 공식 Quick Start의 아래 명령으로 my-video 프로젝트를 만들고 해당 디렉터리로 이동합니다.
- 생성된 프로젝트의 HTML·CSS·미디어와 애니메이션을 편집합니다.
- 에이전트와 작업하려면 영상 프로젝트 디렉터리에서 공식 스킬 설치 경로를 추가로 선택합니다.

공식 문서의 명령·예시:

```sh
npx hyperframes init my-video
cd my-video
```

[명령·예시 원문](https://github.com/heygen-com/hyperframes/blob/7c5c1ce849a6b479f957b69de8dcac8db7eab127/README.md#manually-with-the-cli)

### 사용 예시

- 짧은 제품 소개 영상에 제목이 나타나는 장면·배경 영상·배경 음악을 배치하는 상황을 가정합니다.
- 아래 preview 명령으로 브라우저에서 장면과 시간축을 확인하고, 제목 표시 시점과 미디어 배치를 조정합니다.
- render 명령으로 MP4를 출력한 뒤 길이·프레임·자막·소리가 의도한 결과와 맞는지 확인합니다.

공식 문서의 명령·예시:

```sh
npx hyperframes preview
npx hyperframes render
```

[명령·예시 원문](https://github.com/heygen-com/hyperframes/blob/7c5c1ce849a6b479f957b69de8dcac8db7eab127/README.md#manually-with-the-cli)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (7c5c1ce849a6)](https://github.com/heygen-com/hyperframes/blob/7c5c1ce849a6b479f957b69de8dcac8db7eab127/README.md)

### 저장소 정보

- [저장소](https://github.com/heygen-com/hyperframes) · [README](https://github.com/heygen-com/hyperframes#readme) · [소개 근거](https://github.com/heygen-com/hyperframes#readme)
- 주요 언어: TypeScript · 라이선스: Apache-2.0
- 누적 별: 77,097개 · 포크: 7,067개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Write HTML. Render video. Built for agents.

## Panniantong/Agent-Reach

웹·소셜·영상 플랫폼의 자료를 읽고 검색해 에이전트에서 다루기 쉽게 연결하는 CLI 도구입니다.

YouTube·Bilibili의 자막과 전사, GitHub 저장소·이슈 등 플랫폼별 입력을 제공합니다. 일부 기능은 인증이나 별도 도구가 필요하며 플랫폼마다 지원 범위가 다릅니다.

### 어떤 일을 하나요

- GitHub 저장소·README·이슈·PR, YouTube의 영상 정보·자막, 일반 웹페이지 등 채널별 읽기와 검색을 제공합니다.
- 한 채널의 작업이 실패하면 정해진 대체 도구를 순서대로 사용하는 구조이며 채널별 상태를 확인할 수 있습니다.
- 동영상 음성 전사에는 별도 제공자 키가 필요할 수 있고, 일부 플랫폼은 로그인을 요구합니다.

### 누구에게 유용한가요

- 코딩 에이전트로 웹페이지·동영상 자막·GitHub 문서를 함께 조사하는 개발자와 연구자에게 유용합니다.
- 플랫폼마다 다른 읽기·검색 도구를 하나의 CLI 인터페이스로 연결하려는 사용자에게 적합합니다.

### 설치 방법

준비 사항: 터미널 명령을 실행할 수 있는 환경과 uv가 필요합니다. README는 Python 3.10 이상을 표시합니다. 현재 공식 설치는 GitHub Releases의 ZIP을 uv로 설치하는 방식입니다. PyPI의 동명 패키지는 이 프로젝트가 아니라고 공식 설치 문서가 명시합니다.

- 공식 install.md의 새 설치 절차를 읽고 uv를 준비합니다.
- 아래 두 명령으로 공식 Release ZIP을 설치하고 기본 채널·에이전트 스킬을 설정합니다.
- 명령을 찾지 못하면 공식 문서의 uv tool update-shell 안내를 따라 새 터미널을 엽니다. setup의 설치 보고서에서 사용할 채널과 추가 설정을 확인합니다.

공식 문서의 명령·예시:

```bash
uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip
agent-reach setup
```

[명령·예시 원문](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/docs/install.md#1-install-and-set-up)

### 사용 예시

- 공식 사용 절차를 적용한 예시로, 조사할 GitHub 저장소나 YouTube 영상 주소를 에이전트에 전달하고 README 또는 자막을 읽어 달라고 요청할 수 있습니다.
- 사용 가능한 작업과 매개변수는 agent-reach channels에서 확인합니다. 필요한 채널이 준비됐는지는 doctor 출력으로 살펴봅니다.
- 결과에 인증·의존성 오류가 나오면 해당 채널의 안내를 따릅니다. 자료를 실제로 읽었는지와 반환된 원문 링크를 확인한 뒤 자신의 조사에 사용합니다.

공식 문서의 명령·예시:

```bash
agent-reach channels
agent-reach doctor --text
```

[명령·예시 원문](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/agent_reach/skill/SKILL.md)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (7a38047acf26)](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/README.md)
- [공식 설치·업데이트 절차](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/docs/install.md)
- [공식 채널 명령과 상태 확인](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/agent_reach/skill/SKILL.md)

### 저장소 정보

- [저장소](https://github.com/Panniantong/Agent-Reach) · [README](https://github.com/Panniantong/Agent-Reach#readme) · [소개 근거](https://github.com/Panniantong/Agent-Reach#readme)
- 주요 언어: Python · 라이선스: MIT
- 누적 별: 107,596개 · 포크: 9,593개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Give your AI agent eyes to see the entire internet. Read &amp; search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu — one CLI, zero API fees.

## NationalSecurityAgency/ghidra

NSA 연구부서가 만들고 유지하는 소프트웨어 역공학 프레임워크입니다.

컴파일된 실행 파일을 디스어셈블·디컴파일하고 제어 흐름 그래프와 스크립팅으로 분석합니다. Windows·macOS·Linux에서 바이너리 분석 구조와 디컴파일 결과를 공부할 때 활용할 수 있습니다.

### 어떤 일을 하나요

- 기계어를 어셈블리와 디컴파일 결과로 보여주고 함수 그래프·호출 관계·심볼·바이트를 함께 탐색합니다.
- 프로젝트 데이터베이스에 이름·주석·자료형과 분석 결과를 저장하며 스크립트와 확장 기능을 지원합니다.
- 디컴파일 결과는 분석용 표현이므로 원래 소스코드와 동일하다고 간주하지 않고 실제 명령·호출·데이터를 함께 확인합니다.

### 누구에게 유용한가요

- 컴파일된 실행 파일의 구조를 이해하려는 보안 분석가·펌웨어 개발자·컴퓨터구조 학습자에게 유용합니다.
- 소스코드가 없는 프로그램을 디스어셈블·디컴파일하고 함수 관계를 조사해야 하는 사용자에게 적합합니다.

### 설치 방법

준비 사항: 현재 공식 README의 사전 빌드 배포판 설치 기준은 64비트 JDK 25입니다. 운영체제에 맞는 공식 multi-platform Release ZIP을 사용합니다. Release의 Source Code ZIP은 사전 빌드 프로그램과 다릅니다. Python은 PyGhidra를 사용할 때 별도로 필요하며, 일반 GUI를 시작하는 절차와 소스 빌드 요구사항은 구분합니다.

- 공식 Releases에서 ghidra\_&lt;version&gt;\_&lt;release&gt;\_&lt;date&gt;.zip 형태의 배포 파일을 받습니다.
- JDK를 준비하고 새 폴더에 ZIP을 압축 해제합니다. 기존 설치 폴더 위에 덮어 풀지 않는 방식이 공식 안내입니다.
- Linux·macOS에서는 압축 해제한 폴더에서 아래 명령으로 시작합니다. Windows에서는 ghidraRun.bat을 실행합니다.

공식 문서의 명령·예시:

```bash
./ghidraRun
```

[명령·예시 원문](https://github.com/NationalSecurityAgency/ghidra/blob/4718f50d9941b9d7b7ebd1febc2982f055560a73/README.md#install)

### 사용 예시

- 공식 초급 교재의 흐름에 따라 Project Manager에서 File→New Project를 선택하고 혼자 공부할 경우 Non-Shared 프로젝트를 만듭니다.
- 직접 빌드했거나 분석 권한이 있는 작은 실행 파일을 프로젝트에 가져와 CodeBrowser로 엽니다. 해당 형식에 맞는 분석 설정을 선택합니다.
- 함수 목록에서 관심 함수를 열고 어셈블리·Decompiler·Function Graph를 나란히 읽습니다. 문자열 참조나 호출 대상을 찾아 의미 있는 이름과 주석을 기록합니다.

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (4718f50d9941)](https://github.com/NationalSecurityAgency/ghidra/blob/4718f50d9941b9d7b7ebd1febc2982f055560a73/README.md)
- [현재 README의 설치·JDK 요구사항](https://github.com/NationalSecurityAgency/ghidra/blob/4718f50d9941b9d7b7ebd1febc2982f055560a73/README.md#install)
- [공식 사전 빌드 배포판](https://github.com/NationalSecurityAgency/ghidra/releases)
- [공식 시작·실행 안내](https://github.com/NationalSecurityAgency/ghidra/blob/4718f50d9941b9d7b7ebd1febc2982f055560a73/GhidraDocs/GettingStarted.md)
- [프로젝트 생성·프로그램 가져오기·분석을 다루는 공식 초급 교재](https://github.com/NationalSecurityAgency/ghidra/blob/4718f50d9941b9d7b7ebd1febc2982f055560a73/GhidraDocs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html)

### 저장소 정보

- [저장소](https://github.com/NationalSecurityAgency/ghidra) · [README](https://github.com/NationalSecurityAgency/ghidra#readme) · [소개 근거](https://github.com/NationalSecurityAgency/ghidra#readme)
- 주요 언어: Java · 라이선스: Apache-2.0
- 누적 별: 96,768개 · 포크: 10,927개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Ghidra is a software reverse engineering (SRE) framework

## Leonxlnx/taste-skill

웹사이트와 앱 화면을 만들 때 코딩 에이전트에 미술적 방향·참고 이미지·브라우저 확인 절차를 제공하는 디자인 스킬입니다.

실제 이미지를 참고해 방향을 정하고 구현한 화면을 브라우저에서 확인하는 흐름을 제공합니다. 설치 환경은 저장소의 현재 요구사항에서 확인할 수 있습니다.

### 어떤 일을 하나요

- 주제와 자료를 읽어 시각적 방향을 선택하고, 실제 이미지와 출처를 연결해 페이지를 만드는 절차를 제공합니다.
- 정적 웹페이지와 작업용 앱 화면을 다른 경로로 다루며, 여러 화면 폭의 스크린샷과 검사 결과를 보고 수정하는 흐름을 포함합니다.
- 현재 저장소의 설치 이름은 design-taste-frontend입니다. 과거의 일부 스킬은 별도 저장소로 이동했습니다.

### 누구에게 유용한가요

- 코딩 에이전트로 랜딩 페이지·포트폴리오·제품 페이지나 앱 화면을 구현하는 프런트엔드 개발자에게 유용합니다.
- 글꼴·색상·이미지·레이아웃의 방향을 정하고 실제 브라우저 결과까지 확인하려는 디자이너·개인 제작자에게 적합합니다.

### 설치 방법

준비 사항: 스킬을 읽고 코드를 실행할 수 있는 코딩 에이전트 환경이 필요합니다. 스킬의 도구 스크립트에는 Node.js 22 이상과 Chrome·Edge·Chromium 중 하나가 필요합니다. 참고 이미지 검색에는 네트워크 연결이 필요합니다. 스킬 스크립트에 별도 API 키가 필요 없다는 안내와, 사용하는 코딩 에이전트의 모델 사용 비용은 구분합니다.

- 공식 README의 npx skills 명령으로 design-taste-frontend를 설치합니다.
- 설치 대상 에이전트에서 스킬을 불러올 수 있는지 확인한 뒤 제작할 페이지의 목적·독자·콘텐츠와 기존 프로젝트 위치를 제공합니다.
- Codex·Claude Code용 플러그인 설치를 원하는 경우에는 README의 해당 환경 전용 명령을 사용합니다.

공식 문서의 명령·예시:

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

[명령·예시 원문](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/README.md#install)

### 사용 예시

- 공식 제작 절차를 적용한 예시로, 카페 소개 페이지를 만든다면 실제 매장 사진·메뉴·영업시간·예약 방법을 에이전트에 제공하고 design-taste-frontend 사용을 요청합니다.
- 에이전트가 선택한 시각적 방향을 확인한 뒤 실제 자료로 화면을 구성합니다. 앱 대시보드가 대상이면 공식 app-screens 경로를 사용합니다.
- 세 가지 화면 폭의 브라우저 스크린샷과 검사 결과를 보고 수정하며, 문구·메뉴 가격·링크가 제공한 자료와 일치하는지 확인합니다.

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (12af471f627f)](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/README.md)
- [공식 설치 명령과 실행 환경](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/README.md#install)
- [방향 선택·이미지·브라우저 검사 흐름](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/README.md#how-v2-works)
- [페이지와 앱 화면의 공식 실행 절차](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/skills/taste-skill/SKILL.md)

### 저장소 정보

- [저장소](https://github.com/Leonxlnx/taste-skill) · [README](https://github.com/Leonxlnx/taste-skill#readme) · [소개 근거](https://github.com/Leonxlnx/taste-skill#readme)
- 주요 언어: JavaScript · 라이선스: MIT
- 누적 별: 107,759개 · 포크: 7,279개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: Agent skills that give coding agents taste: art direction, reference images and a browser check instead of generic AI pages

## tashfeenahmed/freellmapi

여러 LLM 제공자의 무료 사용 구간과 사용자 지정 엔드포인트를 하나의 OpenAI 호환 API에 연결하는 라우터입니다.

제공자가 제한에 걸리면 다음 제공자로 전환하고 키별 사용량을 추적합니다. 무료 범위와 이용 조건은 각 제공자에 따르며, 제작자는 개인 실험·학습 용도로 설명합니다.

### 어떤 일을 하나요

- 요청을 설정된 제공자로 전달하고 제한이나 실패가 발생하면 대체 체인을 적용합니다.
- 대시보드에서 제공자 키·사용량·모델을 관리하며 통합 API 키로 클라이언트를 연결합니다.
- 무료 구간과 실제 이용 가능 모델은 제공자 조건에 따릅니다. 라우터가 계산 자원이나 제공자의 사용 한도를 새로 만들어 주는 것은 아닙니다.

### 누구에게 유용한가요

- 여러 LLM 제공자의 API를 개인 실험에서 하나의 OpenAI 호환 주소로 연결하려는 개발자에게 유용합니다.
- 제공자별 키와 사용량·실패 시 대체 순서를 자신의 컴퓨터에서 관리하려는 사용자에게 적합합니다.

### 설치 방법

준비 사항: 아래 Bash 설치 예시는 Git·Docker·Docker Compose·OpenSSL이 준비된 macOS·Linux 환경을 전제로 합니다. 사용할 제공자의 API 키를 준비합니다. Windows 사용자는 공식 Releases의 데스크톱 설치 파일 또는 설치 문서의 PowerShell 절차를 선택할 수 있습니다. 새 복제 폴더에서 암호화 키를 생성하는 예시입니다. 기존 설치를 갱신할 때에는 기존 .env와 암호화 키를 유지해야 합니다.

- 공식 설치 문서의 Docker Compose 절차에 따라 저장소를 새 폴더에 복제하고 암호화 키와 포트를 기록합니다.
- 아래 명령으로 컨테이너를 시작한 뒤 http://localhost:3001에서 대시보드를 엽니다.
- Keys 화면에 사용할 제공자의 키를 추가하고 Fallback Chain의 순서를 정합니다. 클라이언트에는 대시보드의 통합 API 키를 사용합니다.

공식 문서의 명령·예시:

```bash
git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi
ENCRYPTION_KEY="$(openssl rand -hex 32)"
printf "ENCRYPTION_KEY=%s\nPORT=3001\n" "$ENCRYPTION_KEY" > .env

docker compose up -d
```

[명령·예시 원문](https://github.com/tashfeenahmed/freellmapi/blob/21d287aed0aad56cf74bd001d24194916b5a4515/docs/en/install/01-install.md#docker-compose)

### 사용 예시

- 공식 README의 Python 클라이언트 예시는 base\_url을 로컬 라우터의 /v1 주소로 정하고 통합 키로 요청을 보냅니다.
- 아래 api\_key의 예시 문자열을 자신의 통합 키로 바꾸고, OpenAI 호환 Python SDK가 준비된 별도 클라이언트에서 실행합니다. model=auto는 라우터의 선택을 사용합니다.
- 대시보드의 요청 기록에서 실제 사용된 제공자·모델과 실패·대체 여부를 확인합니다. 아래 코드는 공식 예시에서 응답 본문을 출력하는 부분까지 발췌했으며 이 문서 작성 중 실행한 결과는 아닙니다.

공식 문서의 명령·예시:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:3001/v1",
    api_key="freellmapi-your-unified-key",
)

resp = client.chat.completions.create(
    model="auto",  # let the router pick; or "auto:fast", "auto:smart", a profile, or a model id
    messages=[{"role": "user", "content": "Summarise the fall of Rome in one sentence."}],
)
print(resp.choices[0].message.content)
```

[명령·예시 원문](https://github.com/tashfeenahmed/freellmapi/blob/21d287aed0aad56cf74bd001d24194916b5a4515/README.md#using-the-api)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (21d287aed0aa)](https://github.com/tashfeenahmed/freellmapi/blob/21d287aed0aad56cf74bd001d24194916b5a4515/README.md)
- [공식 Docker Compose 설치와 암호화 키 관리](https://github.com/tashfeenahmed/freellmapi/blob/21d287aed0aad56cf74bd001d24194916b5a4515/docs/en/install/01-install.md#docker-compose)
- [공식 데스크톱 배포판](https://github.com/tashfeenahmed/freellmapi/releases/latest)

### 저장소 정보

- [저장소](https://github.com/tashfeenahmed/freellmapi) · [README](https://github.com/tashfeenahmed/freellmapi#readme) · [소개 근거](https://github.com/tashfeenahmed/freellmapi#readme)
- 주요 언어: TypeScript · 라이선스: MIT
- 누적 별: 45,707개 · 포크: 6,241개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: 7.4 billion tokens per month. 34 free LLM providers. 635 free model endpoints. All behind one /v1 endpoint, plus any custom OpenAI-compatible endpoint. Smart routing, automatic failover, encrypted keys. Personal experimentation only.

## deepseek-ai/DeepInfer

DeepSeek 모델용 대규모 추론 프레임워크로 최적화 커널·병렬 실행·비동기 스케줄링·구조화 출력을 제공합니다.

공개판은 오프라인 추론을 중심으로 하며 완전한 서비스에는 KV 캐시·분리형 서빙·부하 분산 등의 추가 구성이 필요합니다. 지원 모델과 GPU·가속기 조건은 공식 README에서 확인합니다.

### 어떤 일을 하나요

- 최적화 커널과 모델 실행기, MoE 병렬 실행과 부하 조정, 비동기 스케줄링, 구조화 출력을 제공합니다.
- 현재 공개판은 오프라인 추론을 중심으로 합니다. 완전한 온라인 서비스에는 KV 캐시 시스템·프리필과 디코드 분리·복제본 간 부하 분산 등의 추가 구성이 필요합니다.
- 확인한 README의 지원 모델은 DeepSeek-V4.1-Flash이며 지원 하드웨어는 NVIDIA SM100과 Huawei Ascend 950입니다.

### 누구에게 유용한가요

- 대규모 DeepSeek 모델의 추론 엔진·GPU 커널·병렬화·스케줄링을 연구하는 시스템 엔지니어에게 유용합니다.
- 지원 가속기와 모델을 갖춘 연구실·추론 인프라 팀이 공식 오프라인 예제와 성능 측정 구조를 살펴볼 때 적합합니다.

### 설치 방법

준비 사항: Linux·GCC 13 이상·Python 3.12가 필요합니다. NVIDIA 환경에는 CUDA 13, Ascend 환경에는 CANN 9.2가 필요합니다. 지원 가속기와 모델 가중치를 보관할 저장 공간·모델 실행에 필요한 메모리와 병렬 환경을 준비해야 합니다. 공식 문서에 따라 비어 있는 Python 3.12 환경을 만들고 활성화한 뒤 저장소 루트에서 빌드합니다. 일반 CPU 노트북용 설치 예시는 아닙니다.

- 공식 저장소를 내려받고 Getting started의 하드웨어·컴파일러·런타임 요구사항을 맞춥니다.
- 새 Python 환경에서 사용할 가속기를 환경변수로 정하고 build.sh를 실행합니다. 아래는 NVIDIA용 공식 명령이며 Ascend 환경은 문서가 안내하는 ascend 값을 사용합니다.
- 추론을 실행할 터미널에서도 DEEPINFER\_ACCELERATOR 값을 유지합니다.

공식 문서의 명령·예시:

```bash
export DEEPINFER_ACCELERATOR=nvidia
./build.sh
```

[명령·예시 원문](https://github.com/deepseek-ai/DeepInfer/blob/553741557a57df44a46fb3ab72b6aafeaf945337/README.md#build-from-source)

### 사용 예시

- 공식 오프라인 예제를 실행하면 기본 DeepSeek-V4.1-Flash-1017 체크포인트를 Hugging Face 캐시에 내려받아 사용합니다. 로컬 복사본을 쓰려면 문서의 DEEPINFER\_HF\_MODEL\_DIR 설정을 따릅니다.
- 아래 명령의 출력과 공식 examples 문서의 예제 입력·출력 흐름을 비교합니다. 더 큰 병렬 실행은 실제 장치 수에 맞춰 ep·dp·cp 옵션을 선택합니다.
- 성능을 비교할 때에는 입력 길이·배치 크기·하드웨어 수와 측정 구간을 함께 기록합니다. 저장소의 벤치마크 수치를 자신의 장비에서 얻은 결과처럼 사용하지 않습니다.

공식 문서의 명령·예시:

```bash
python examples/offline_inference.py
```

[명령·예시 원문](https://github.com/deepseek-ai/DeepInfer/blob/553741557a57df44a46fb3ab72b6aafeaf945337/README.md#offline-inference)

### 출처와 확인 범위

소개 방식: 공식 문서 한국어 해설 · 문서 확인: 2026-11-02

- [공식 README 고정 판본 (553741557a57)](https://github.com/deepseek-ai/DeepInfer/blob/553741557a57df44a46fb3ab72b6aafeaf945337/README.md)
- [공식 오프라인 추론·병렬 실행·벤치마크 예제](https://github.com/deepseek-ai/DeepInfer/blob/553741557a57df44a46fb3ab72b6aafeaf945337/examples/README.md)

### 저장소 정보

- [저장소](https://github.com/deepseek-ai/DeepInfer) · [README](https://github.com/deepseek-ai/DeepInfer#readme) · [소개 근거](https://github.com/deepseek-ai/DeepInfer#readme)
- 주요 언어: Python · 라이선스: Apache-2.0
- 누적 별: 24,808개 · 포크: 3,010개
- 소개 방식: README 해설 (2026-11-02 확인)

원문 소개: DeepInfer: High-performance, large-scale inference framework for DeepSeek models

[주간 기록](주간기록/README.md) · [전체 안내](README.md)
