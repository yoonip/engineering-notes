# 매체와 수집 기준 | Sources and selection

## 기사 선택

매체가 제공하는 국제 뉴스·주요 뉴스·전체 뉴스 피드에서 최근 24시간에 발행된 항목을 읽습니다. 각 피드의 순서를 유지하며 매체별로 소수 기사를 연결합니다. 언론사 홈페이지의 모든 기사나 실시간 인기 순위를 수집하는 방식은 아닙니다.

기사의 발행 시각이 없거나 해석되지 않는 항목, 미래 시각과 오래된 항목은 제외합니다. 채널 전체의 갱신 시각을 개별 기사 발행 시각으로 대신 쓰지 않습니다. 같은 원문 주소는 목록에서 한 번만 연결하며, 제목이 다른 별도 매체의 기사는 함께 실릴 수 있습니다.

제목을 번역·요약하거나 기사에 없는 해설을 생성하지 않습니다. 목록에는 제목·매체명·발행 시각·원문 링크를 표시하고, 피드에 작성자·제공자가 기재되어 있으면 함께 적습니다. 원시 피드, 기사 본문과 사진은 공개 저장소에 저장하지 않습니다. 날짜별 기사 데이터셋을 별도로 만들지 않고 최신 읽기 화면을 갱신합니다. 이전 화면은 Git 변경 이력에 남습니다.

수집에 사용한 매체와 결과는 매 실행마다 [뉴스 목록](최신뉴스_latest.md) 아래에 표시합니다. 시스템이 매체의 주장이나 사실관계를 별도로 검증했다는 의미는 아닙니다.

## 자동 수집 매체

공식 피드 응답과 안내를 2026년 10월 29일 확인했습니다. 이 저장소는 광고·유료 판매가 없는 개인 비상업 뉴스 링크 모음으로 운영합니다. 각 매체의 RSS 이용 조건을 아래에 연결합니다.

| 매체·피드 범위 | 공식 피드 | 공식 안내와 적용 범위 |
| --- | --- | --- |
| ABC News 미국 · 국제 | [RSS](https://feeds.abcnews.com/abcnews/internationalheadlines) | [공식 RSS 안내](https://abcnews.com/Site/page/rss-feeds-3520115)는 헤드라인의 뉴스 집계와 외부 사이트에서 원문으로 연결하는 사용을 설명합니다. 호주 ABC와는 다른 방송사입니다. |
| NPR · 세계 | [RSS](https://feeds.npr.org/1004/rss.xml) | [이용약관의 Content Feeds](https://www.npr.org/about-npr/179876898/terms-of-use)는 개인 비상업 사이트의 피드 표시·발췌·직접 링크를 허용합니다. NPR와 피드에 기재된 작성자·제공자를 가까이 표시하고 원제와 링크를 유지합니다. |
| The Christian Science Monitor · 세계 | [RSS](https://rss.csmonitor.com/feeds/world) | [공식 RSS 안내의 Copyright Notice](https://www.csmonitor.com/About/RSS)는 비상업 사이트의 CSMonitor.com 기사 링크 제공을 허용합니다. RSS files © The Christian Science Monitor. |
| AllAfrica · 최근 기사 | [RSS/RDF](https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf) | [공식 RSS 안내의 Headlines on a Web Site·Terms and Conditions](https://allafrica.com/misc/tools/rss.html)는 헤드라인 웹 표시를 허용하며 allAfrica.com 표기와 홈페이지 링크를 요구합니다. 여러 아프리카 매체의 기사를 모으는 서비스입니다. |
| 연합뉴스 · 국제 | [RSS](https://www.yna.co.kr/rss/international.xml) | [공식 RSS 안내](https://www.yna.co.kr/rss/index)의 비상업 블로그·개인 이용 범위입니다. 국제 기사를 한국어로 읽는 경로입니다. |
| 연합뉴스 · 전체 | [RSS](https://www.yna.co.kr/rss/news.xml) | [공식 RSS 안내](https://www.yna.co.kr/rss/index)의 같은 조건을 적용합니다. 국제 피드와 원문 주소가 같으면 한 번만 표시합니다. |
| SBS 뉴스 · 이 시각 이슈 | [RSS](https://news.sbs.co.kr/news/headlineRssFeed.do?plink=RSSREADER) | [공식 RSS 안내](https://news.sbs.co.kr/news/rss.do)의 개인 비상업 이용 조건에 맞춰 제목과 직접 링크를 표시합니다. |
| 동아일보 · 전체 | [RSS](https://rss.donga.com/total.xml) | [공식 RSS 안내](https://rss.donga.com/)의 개인 비상업 이용 조건을 적용합니다. 개별 발행 시각이 있는 전체 뉴스 피드를 사용합니다. |

## 자동 수집과 공식 바로가기의 구분

[뉴스 안내](README.md)의 주요 매체 바로가기는 해당 언론사의 홈페이지를 여는 링크입니다. 자동 수집에 사용하는 피드는 위 표에 한정합니다.

| 매체 | 이번 구성에서 공식 바로가기를 제공하는 이유 |
| --- | --- |
| CNN | 확인한 기존 edition RSS의 기사 갱신이 오래전에 멈췄습니다. HTTP 응답 성공을 현재 뉴스 제공으로 간주하지 않습니다. |
| BBC News | [이용약관 §15](https://downloads.bbc.co.uk/usingthebbc/bbc_terms_of_use.pdf)의 웹 피드 표시 조건과 메타데이터 추출 제한을 함께 고려해, 이 목록의 선별 추출 대상에 넣지 않았습니다. |
| KBS·YTN·중앙일보 | 이번 확인에서 사용할 수 있는 공식 뉴스 피드와 수집 조건을 함께 확보하지 못했습니다. |
| 조선일보·경향신문 | [조선일보 RSS 가이드](https://news.chosun.com/section/guide/index.html)와 [경향신문 RSS 안내](https://www.khan.co.kr/help/help_rss.html)의 공개 재배포 조건을 고려해 홈페이지로 연결합니다. |
| The Guardian·The New York Times | [Guardian 이용약관](https://www.theguardian.com/help/terms-of-service)의 자동 추출 제한과 [NYT 이용약관](https://help.nytimes.com/hc/en-us/articles/115014893428-Terms-of-Service)의 데이터셋 배포 조건을 고려해 홈페이지로 연결합니다. |

매체명·기사 제목·원문은 해당 권리자의 자료입니다. 공식 자료에 없는 사용 허가나 제휴 관계를 주장하지 않습니다.

[뉴스 안내](README.md) · [오늘의 뉴스](최신뉴스_latest.md) · [운영 안내](운영안내_operations.md)
