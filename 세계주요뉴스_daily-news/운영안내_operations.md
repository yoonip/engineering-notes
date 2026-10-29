# 뉴스 수집 운영 | News collection operations

## 실행 방식

GitHub Actions가 GitHub의 Ubuntu 실행 환경에서 Python 수집기를 실행합니다. PC 전원, 이 채팅, GPT 사용량이나 별도 AI API 키에 의존하지 않습니다. 별도의 유료 뉴스 API도 사용하지 않습니다.

| 항목 | 설정 |
| --- | --- |
| 정기 실행 | 매일 09:17 KST = 00:17 UTC |
| 실행 파일 | [daily-news.yml](../.github/workflows/daily-news.yml) |
| 수집기 | [collect_news.py](자동수집_automation/collect_news.py) |
| 공식 피드 설정 | [sources.json](자동수집_automation/sources.json) |
| 자동으로 갱신하는 파일 | [최신뉴스_latest.md](최신뉴스_latest.md) |
| 실행 기록 | [GitHub Actions](https://github.com/yoonip/engineering-notes/actions/workflows/daily-news.yml) |

워크플로는 정기 실행과 수동 실행만 받습니다. 뉴스 갱신 커밋이 다시 수집을 일으키지 않습니다. 같은 저장소의 뉴스 수집은 순서대로 실행하며, 게시 단계에서는 뉴스 파일만 커밋합니다. 게시 직전 원격 main의 변경을 받아 다른 문서의 커밋을 보존합니다. 충돌이 있으면 강제로 덮어쓰지 않고 실패로 남깁니다.

GitHub는 예약 실행의 정확한 시작 시각을 보장하지 않습니다. 부하가 높으면 늦어지거나 누락될 수 있습니다. 공개 저장소에 60일 동안 활동이 없으면 정기 워크플로가 비활성화될 수 있습니다. 실제 동작 조건은 [GitHub의 schedule 문서](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)에서 확인하실 수 있습니다.

## 오류와 재실행

일부 피드가 실패해도 세계 뉴스 2곳·한국 뉴스 1곳 이상의 최신 기사를 확보하면 목록을 게시하고, 실패한 매체를 수집 상태 표와 Actions 경고에 기록합니다. 이 기준의 ‘곳’은 피드 단위이며, 같은 통신사 보도의 독립 확인 횟수를 뜻하지 않습니다. 기준에 미달하면 기존 정상 파일을 유지하고 실행을 실패로 표시합니다. HTTP 오류 응답에는 최대 한 번만 재시도합니다. 오래된 기사로 빈자리를 채우지 않습니다.

수동으로 다시 실행하려면 [Actions 실행 화면](https://github.com/yoonip/engineering-notes/actions/workflows/daily-news.yml)에서 `Run workflow` → `main` → `Run workflow`를 선택합니다. 각 실행의 Summary에 매체별 상태와 제외 항목 수가 남습니다. GitHub의 알림 설정에서 구독한 워크플로 실패 알림을 받을 수 있습니다.

정기 수집을 중지하려면 같은 화면의 메뉴에서 `Disable workflow`를 선택합니다. 다시 켤 때는 `Enable workflow`를 선택합니다. 방법은 [GitHub의 워크플로 중지·활성화 안내](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)에 나와 있습니다.

## 직접 확인

Python 3.12 이상에서 다음 명령을 실행합니다. 첫 명령은 고정된 가상 피드로 오류·경계 조건을 검사하며 인터넷에 연결하지 않습니다. 두 번째 명령은 공식 피드에 실제로 접속해 목록을 만듭니다.

```bash
python3 -m unittest discover -s '세계주요뉴스_daily-news/자동수집_automation' -p 'test_*.py' -v  # 수집기 동작을 검사합니다.
python3 '세계주요뉴스_daily-news/자동수집_automation/collect_news.py'  # 공식 피드를 읽어 최신 목록을 작성합니다.
```

피드 설정을 바꿀 때에는 공식 안내, 실제 응답, 기사의 발행 시각과 이용 조건을 함께 확인합니다. 재게시가 허용되지 않거나 갱신이 중단된 매체는 [공식 바로가기](README.md#주요-매체-바로가기)로 연결합니다. 이 자동 실행은 뉴스 목록만 갱신합니다.

[뉴스 안내](README.md) · [매체와 수집 기준](매체와수집기준_sources.md)
