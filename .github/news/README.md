# 뉴스 게시 코드 | News publishing code

독자용 목록은 [뉴스](../../뉴스_news/README.md)의 세계·국내 두 분류입니다. 이 폴더에는 실행 코드와 설정을 보관합니다.

## 일정과 실행 자원

[daily-news.yml](../workflows/daily-news.yml)의 `17 * * * *`는 매시간 17분에 실행을 요청합니다. 한국도 매시간 17분입니다. 17분은 특정 방송사의 첫 기사 발표 시각이 아니라 GitHub의 정각 실행 혼잡을 피하기 위한 값입니다. [GitHub schedule 문서](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)는 정각 부하와 지연 가능성을 설명합니다. [ABC의 RSS 안내](https://abcnews.com/Site/page/rss-feeds-3520115)도 발행된 소식을 독자가 주기적으로 확인하는 방식을 설명하며 공통 첫 갱신 시각을 두지 않습니다.

GitHub의 예약 서비스가 실행 요청을 만들고, GitHub가 제공하는 Ubuntu 가상 머신에서 Python을 실행합니다. 프로그램은 공식 RSS를 확인하고 새 기사·실질적인 후속 내용만 골라 파일을 작성한 뒤 저장소 전용 GITHUB_TOKEN으로 커밋·push합니다. PC 전원이나 이 채팅을 켜 둘 필요가 없습니다. 이 토큰은 저장소 쓰기용 인증 수단이며 AI의 문장 처리 토큰과 다른 개념입니다.

사용하는 ubuntu-24.04 표준 공개 저장소 환경은 [GitHub 공식 사양](https://docs.github.com/en/actions/reference/runners/github-hosted-runners#standard-github-hosted-runners-for-public-repositories)상 CPU 4개·메모리 16GB·SSD 14GB이며 공개 저장소에서 무료로 제공됩니다. Python의 표준 라이브러리만 사용합니다. 실제로는 GitHub의 컴퓨터와 네트워크가 일을 합니다. 사람이 매번 명령하지 않아도 저장된 코드가 실행되는 것이며 자원 소비가 없다는 뜻은 아닙니다.

## 파일과 변경 판별

| 파일 | 역할 |
| --- | --- |
| [sources.json](sources.json) | 공식 피드, 이용 조건, 분류와 우선순위 |
| [collect_news.py](collect_news.py) | 허용한 HTTPS 피드의 제목·발행일·짧은 개요를 읽습니다. |
| [news_pipeline.py](news_pipeline.py) | 새 기사와 후속 내용만 골라 당일 목록에 반영합니다. |
| [archive_news.py](archive_news.py) | 최신 목록·날짜별 보관본·날짜 목차를 작성합니다. |
| [state.json](state.json) | 게시한 짧은 내용과 중복 판별용 해시·피드 응답 표식을 보관합니다. |

매체가 지원하면 ETag·Last-Modified로 변경 없는 피드 본문을 다시 받지 않습니다. 지원하지 않는 매체는 새 기사 유무를 확인하기 위해 목록을 읽습니다. 개별 기사 본문은 크롤링하지 않습니다.

이미 게시한 같은 URL·같은 내용, 제목 장식만 바뀐 재전송과 내용이 같은 매우 유사한 제목은 다시 게시하지 않습니다. 관측했지만 선정하지 않았던 기사도 해시를 기록해 다음 실행에서 바뀌지 않은 오래된 기사들이 뒤늦게 새 글처럼 나오지 않게 합니다. 미선정 기사의 본문이나 개요를 별도 데이터셋으로 저장하지 않습니다.

새 수치나 개요의 실질적인 변화는 후속 내용으로 반영합니다. 당일의 같은 URL은 한 항목으로 갱신하고 이전 날짜 보관본은 보존합니다. 새 내용이 없는 분류의 본문·갱신 시각·날짜 목차는 바꾸지 않습니다. 필요하면 중복 판별용 상태만 갱신합니다. 비교 범위는 공식 피드에 드러난 내용입니다.

중요도는 공식 주요 뉴스 피드, 정치·경제·사회·과학·보건·문화·스포츠 등의 입력, 사건·정책·재난 등 관련 표지와 기사 시각을 조합한 규칙으로 판단합니다. 매체별 수를 제한하며 일상 행사·판촉·개별 주가 속보의 우선순위는 낮춥니다. 이는 세계 모든 사건의 객관적 순위나 사실 확인을 완료했다는 뜻은 아닙니다.

## 한국어 기사 개요

한국어로 읽는 세계 뉴스는 연합뉴스 국제와 해외 매체의 공식 한국어 보도 등에서 받습니다. 국내·세계 모두 매체가 공식 피드로 제공한 짧은 소개를 인용하고 출처·발행 시각·원문 링크를 남깁니다. 전체 본문을 읽고 AI가 새로 작성한 요약이 아닙니다.

외부 AI API와 번역 모델은 사용하지 않습니다. 따라서 ChatGPT 사용량·API 토큰 요금이나 모델 추론이 필요하지 않습니다. 영어 원문 링크는 별도로 표시하며 한국어로 번역한 기사라고 표시하지 않습니다. [매체별 조건](sources.md)을 기사 본문 전체의 재출간 허가로 확대하지 않습니다.

## 확인과 중지

인터넷 없는 검사는 `python3 -m unittest discover -s .github/news -p 'test_*.py' -v`로 실행합니다. 실제 수집은 `python3 .github/news/news_pipeline.py`로 실행합니다.

[Actions 실행 화면](https://github.com/yoonip/engineering-notes/actions/workflows/daily-news.yml)에서 수동 실행·오류 기록을 확인하거나 Disable workflow로 중지할 수 있습니다. 뉴스 문서와 상태 파일만 커밋하고 강제 push하지 않습니다. 충돌은 실패로 남깁니다. 예약 실행은 부하에 따라 늦어지거나 누락될 수 있으며 공개 저장소가 장기간 비활성 상태이면 중지될 수 있습니다.
