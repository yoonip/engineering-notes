# 자동화와 기술 기록 | Automation and technical records

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

자동화는 반복 작업을 정해진 입력과 규칙으로 실행합니다. 데이터 수집·정리·실험 실행·그래프 생성·문서 빌드가 하나의 흐름으로 연결되면 결과가 만들어진 과정을 추적하기 쉽습니다.

## 스크립트와 CI

Python은 데이터 처리와 라이브러리 연결, Bash는 Linux 명령 조합, PowerShell은 Windows와 구조화된 시스템 작업에 쓰입니다. 스크립트는 입력·출력·종료 코드·로그를 통해 다른 작업과 연결됩니다. GitHub Actions·GitLab CI는 저장소 변경이나 예약된 이벤트에 따라 작업을 실행합니다.

## 문서 생성 도구

Quarto는 Markdown·Jupyter 기반의 글·수식·그래프를 웹 문서로 만들고, Jekyll·Hugo는 정적 사이트를 생성합니다. MkDocs·Sphinx는 기술 문서, Doxygen은 코드 API 문서, Jupyter Book은 계산 문서 묶음에 사용됩니다.

GitHub Pages는 생성된 정적 파일을 서비스합니다. Python 계산이나 모델 추론이 필요하면 로컬 또는 CI에서 실행해 결과를 만들거나 별도 서버와 연결합니다. 글의 원본은 내용을 편집하는 데, 생성된 HTML은 배포에 쓰입니다. 실험 데이터와 로그, 환경 정보는 결과를 재현하는 근거로 남깁니다.

## 관련 기술

Python, Bash, PowerShell, GitHub Actions, GitLab CI, Docker, Quarto, Jekyll, Hugo, MkDocs, Sphinx, Doxygen, Jupyter Book

## 참고 자료

- [Quarto and GitHub Pages](https://quarto.org/docs/publishing/github-pages.html)
- [Pro Git](https://git-scm.com/book/en/v2)

## 기초 해설

- [자동화의 기본: 검증, 재실행과 원자적 게시](해설_notes/자동화의기본_ci-idempotency-atomic-publication.md)

## English

Automation runs repeated work using defined inputs and rules. Connecting data collection, cleanup, experiments, plotting, and document builds makes it easier to trace how a result was produced.

### Scripts and CI

Python handles data and library integration, Bash combines Linux commands, and PowerShell supports Windows and structured system operations. Scripts connect through inputs, outputs, exit codes, and logs. GitHub Actions and GitLab CI run workflows in response to repository changes or scheduled events.

### Documentation tools

Quarto turns Markdown and Jupyter content into web documents with equations and plots. Jekyll and Hugo generate static sites. MkDocs and Sphinx support technical documentation, Doxygen generates code API documentation, and Jupyter Book collects computational documents.

GitHub Pages serves generated static files. Python computations and model inference can run locally or in CI to generate results, or connect to a separate server. Source documents, generated HTML, experiment data, logs, and environment records serve different roles in this workflow.

### Foundation article

- [자동화의 기본: 검증, 재실행과 원자적 게시](해설_notes/자동화의기본_ci-idempotency-atomic-publication.md#english)


## 심화 해설 | Advanced article

- [CI를 줄여도 검증은 빠뜨리지 않기: 변경 영향과 캐시](해설_notes/변경영향과CI캐시_incremental-ci-cache.md) · [English](해설_notes/변경영향과CI캐시_incremental-ci-cache.md#english)
