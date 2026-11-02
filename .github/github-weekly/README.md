# 주간 GitHub 프로젝트 게시 코드 | Weekly GitHub publishing

독자용 자료는 [인기 GitHub 프로젝트](../../인기GitHub프로젝트_github-weekly/README.md)에 있습니다. 이 폴더는 수집·한국어 소개·주차별 보관과 게시 코드를 담습니다.

| 파일 | 역할 |
| --- | --- |
| `collect.py` | 주간 Trending 앞 10개, 공식 저장소 메타데이터와 소개를 수집합니다. |
| `reviewed.json` | 공식 README를 확인한 날짜, 한국어 해설, 저장소 ID와 원문 설명 해시를 보관합니다. |
| `details.json` | 공식 문서에 근거한 기능·사용자·환경·설치·사용 예시를 저장소 ID·README SHA와 연결합니다. |
| `guides.py` | README와 연결된 Markdown 문서에서 구간·조건·명령을 읽고 같은 형식의 안내를 만듭니다. |
| `translations.json` | 원문 설명 SHA-256별 로컬 번역 결과를 보관합니다. |
| `publish.py` | 주간 기록 폴더와 번역 캐시만 커밋해 `main`에 정상 push합니다. |
| `test_collect.py`·`test_guides.py` | 주차·중복·실패 처리, README 판본·구간·설치 조건·명령 보존을 검사합니다. |

매주 월요일 09:23 KST에 [워크플로](../workflows/github-weekly.yml)가 실행됩니다. 기존 뉴스·자료 게시와 같은 concurrency 그룹을 써서 저장소 쓰기를 직렬화합니다. 이후 push가 경쟁하면 원격을 fetch하고 정상 rebase·push하며, 충돌이 나면 실패합니다. 강제 push는 하지 않습니다.

수집은 HTML 구조·저장소 이름·주간 증가량·중복을 검사합니다. 한 저장소의 조회나 번역이 실패하면 그 실행에서는 불완전한 새 목록을 게시하지 않습니다. 이미 발행된 주의 기록은 그대로 두고, 중단 때문에 JSON만 남았다면 그 관측 데이터로 본문을 복구합니다. 원본 HTML·README를 실행하거나 프로젝트를 자동 설치하지 않습니다. 외부 HTML은 설명과 숫자를 읽는 입력으로만 사용합니다.

한국어 해설은 저장소 ID와 설명 해시가 맞을 때 사용합니다. 변경된 설명이나 처음 나타난 영어 소개는 Argos Translate 1.11.0과 영어→한국어 모델 1.1로 runner CPU에서 번역합니다. 결과에는 번역 방식을 기록하며 GPT·유료 번역 API를 호출하지 않습니다. 모델이 없으면 Argos 공식 목록에서 내려받고, 이미 번역한 같은 원문은 캐시를 사용합니다.

상세 안내는 ‘기능·유용한 사용자·설치·사용 예시’ 순서를 사용합니다. 기존 한국어 상세 해설은 저장소 ID와 README의 blob SHA가 맞을 때만 재사용합니다. 다른 경우에는 기본 브랜치의 커밋을 먼저 고정하고 그 판본의 README와 연결된 설치·사용 Markdown 문서를 최대 두 개 읽습니다. 제목 경계와 코드 펜스를 구분하고, 문서에 있는 짧은 절차와 명령만 그대로 옮깁니다. Windows·macOS·Linux 등 하위 절 제목과 명령 앞의 조건을 함께 표시합니다. 원문에 없는 설치 명령이나 사용 사례를 생성하지 않습니다.

자연어 구간은 CPU 번역을 사용하고 코드 블록은 원문을 유지합니다. 문서가 특정 사용자나 설치법을 설명하지 않거나 예시가 너무 길면 확인 가능한 원문 링크를 표시합니다. JSON에는 문서의 고정 커밋·파일 경로·blob SHA·확인 시각·사용한 짧은 구간을 남기며 전체 README를 재게시하지 않습니다. 자동 실행은 원격 저장소의 코드를 설치·실행하지 않습니다.

```sh
python3 -m pip install -r .github/github-weekly/requirements.txt
python3 -m unittest discover -s .github/github-weekly -p 'test_*.py' -v
python3 .github/github-weekly/collect.py
```

로컬 명령은 수집 파일만 만듭니다. 게시 명령은 GitHub Actions에서 `python3 .github/github-weekly/publish.py`로 실행합니다. 번역 모델도 직접 확인하려면 수동 실행의 `check_translation`을 켭니다. 번역 검사 문장은 운영 캐시에 넣지 않습니다.

2026년 11월 2일 [첫 서버 실행](https://github.com/yoonip/engineering-notes/actions/runs/41364746396)에서 21개 검사, 공개 영어→한국어 모델의 CPU 번역과 임시 폴더를 이용한 실제 원본 수집을 통과했습니다. 운영 기록은 같은 주가 이미 발행되어 재작성하지 않았으며, 게시 단계도 새 변경 없이 종료했습니다.

같은 날 [상세 안내 서버 검사](https://github.com/yoonip/engineering-notes/actions/runs/41366634386)에서는 41개 검사와 실제 원본 수집을 통과했습니다. 기존 상세 해설을 사용하는 경로와, 해당 해설을 비우고 README 구간을 추출해 CPU로 번역하는 신규 프로젝트 경로를 모두 실행했습니다. 기존 소개의 설치·사용 코드 31개도 해당 공식 문서의 고정 판본과 줄 단위로 대조했습니다. 이 검사는 수집·표시 코드의 실행 확인이며 소개한 프로젝트 자체의 설치·실행 시험과는 구분합니다.
