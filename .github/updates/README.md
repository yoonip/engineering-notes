# 모델 발표·기관 보고서 게시 코드 | Publication updates

독자용 자료는 [모델 발표](../../AI모델동향_ai-model-updates/새소식_updates/README.md)와 [보고서 소식](../../미래경제보고서_future-economic-reports/새소식_updates/README.md)에 있습니다. 기존 모델 분석·보고서 해설은 수정하지 않습니다.

## 실행과 자원

[GitHub Actions](../workflows/model-report-updates.yml)가 매시간 37분에 실행을 요청합니다. 기존 뉴스의 매시간 17분과 시간을 나누고 동일 concurrency 그룹으로 자동 게시 작업의 push를 직렬화합니다. GitHub가 제공하는 Ubuntu 가상 머신의 CPU·네트워크에서 Python과 HTML 파서를 실행하며, ChatGPT·Codex·GPT API·외부 번역 API는 호출하지 않습니다.

공개 저장소의 표준 runner는 [GitHub 공식 안내](https://docs.github.com/en/actions/reference/runners/github-hosted-runners#standard-github-hosted-runners-for-public-repositories)상 무료입니다. PC와 채팅을 켜 둘 필요가 없습니다. 커밋에 쓰는 GITHUB_TOKEN은 저장소 쓰기 인증이며 GPT 사용량과 관계없습니다. [예약 실행](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)은 부하에 따라 지연되거나 누락될 수 있습니다.

## 수집 범위와 소개 방식

- [모델 출처](model_sources.json): OpenAI·Google 공식 한국어 RSS, DeepMind RSS, Anthropic·DeepSeek·Kimi의 공개 발표 목록, Qwen·Z.ai 공식 Hub 조직입니다. 고객 활용 사례·행사·양자화 변형 등은 모델 발표와 구분합니다.
- [보고서 출처](report_sources.json): LG경영연구원, KDI, ETRI, KISTI, 서울대 국가미래전략원, KAIST 미래전략연구센터의 공개 목록입니다. 월간·연간 등 실제 발행 주기와 프로그램의 확인 주기는 별개입니다.
- 한국어 공식 소개는 짧게 발췌하고 출처·원문·확인되는 PDF 링크를 붙입니다. 소개가 없는 경우 또는 다른 언어인 경우에는 확인된 제목·기관·주제의 한국어 자료 안내로 표시합니다. 전체 PDF 번역·새 논문 해설·성능 실험을 자동 생성하지 않습니다.
- HF createdAt은 배포 저장소 등록일입니다. 웹 게시일·원문 판본월과 PDF 발행일을 같다고 가정하지 않습니다. 원문의 날짜가 없으면 수집일로 대신하지 않습니다.

삼성글로벌리서치는 확인한 robots 규칙이 전체 크롤링을 금지하므로 이 실행에 넣지 않았습니다. IMF·IEA는 직접 요청이 차단되어 기존 원문 안내만 유지합니다. [기관별 원문 경로](../../미래경제보고서_future-economic-reports/기관과원문찾기_institutions-and-sources.md)에서 직접 읽을 수 있습니다. 로그인이나 접속 제한을 우회하지 않습니다.

## 중복과 보관

정규화한 공식 URL·문서 ID·내용 지문을 state.json에 기간 만료 없이 보관합니다. pub_no·idx·연월·DeepSeek의 절 식별자는 보존하고 추적 query는 비교에서 제외합니다. 기존 해설에서 연결한 정확한 원문도 다시 게시하지 않습니다. 제목·소개가 같은 항목은 상세 페이지를 다시 요청하지 않으며, 날짜·조회수·가중치 revision만 바뀌어도 새 글을 만들지 않습니다.

처음 연결할 때에는 최근 45일 범위에서 출처당 최대 3개를 표시합니다. 나머지 관측 항목은 기록해 다음 실행에서 구판이 조금씩 신규로 올라오는 일을 막습니다. 이후 새 ID는 24시간 만료를 적용하지 않습니다. 수정은 원문 목록에서 드러나는 제목·소개·PDF 링크의 변화를 기준으로 합니다. 목록이 갱신 표시를 제공하지 않는 본문의 모든 정정을 탐지하는 기능은 아닙니다.

날짜별 문서는 KST 반영일로 보관하고 각 항목에 원문 날짜를 따로 표시합니다. 당일의 같은 원문은 한 항목으로 갱신하며 이전 날짜 문서는 보존합니다. 새 내용이 없으면 독자용 문서와 갱신 시각을 쓰지 않습니다. 조건부 요청용 표식과 운영 상태만 바뀔 수 있습니다.

## 확인·복구·중지

`python3 -m unittest discover -s .github/updates -p 'test_*.py' -v`로 인터넷 없는 검사를 실행합니다. 실제 확인은 `python3 .github/updates/update_pipeline.py --report status.json`입니다. 모든 출처 실패는 게시하지 않고 실패로 남기며, 일부 실패는 기존 자료를 유지하면서 해당 출처·상세 오류를 Actions 요약에 기록합니다. 실패한 상세 요청은 재시도 대상으로 남깁니다.

[Actions 실행 화면](https://github.com/yoonip/engineering-notes/actions/workflows/model-report-updates.yml)에서 실행·오류를 확인하고 Disable workflow로 중지할 수 있습니다. 코드와 원문 사이트의 형식·접근 규칙이 달라지면 수정이 필요합니다. 원문·PDF 전체를 보관하거나 재배포하지 않습니다.
