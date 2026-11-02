# 주간 GitHub 프로젝트 게시 코드 | Weekly GitHub publishing

독자용 자료는 [인기 GitHub 프로젝트](../../인기GitHub프로젝트_github-weekly/README.md)에 있습니다. 이 폴더는 수집·한국어 소개·주차별 보관과 게시 코드를 담습니다.

| 파일 | 역할 |
| --- | --- |
| `collect.py` | 주간 Trending 앞 10개, 공식 저장소 메타데이터와 소개를 수집합니다. |
| `reviewed.json` | 공식 README를 확인한 날짜, 한국어 해설, 저장소 ID와 원문 설명 해시를 보관합니다. |
| `translations.json` | 원문 설명 SHA-256별 로컬 번역 결과를 보관합니다. |
| `publish.py` | 주간 기록 폴더와 번역 캐시만 커밋해 `main`에 정상 push합니다. |
| `test_collect.py` | 주차 경계·재실행·중복·수집 실패와 표시 문법을 검사합니다. |

매주 월요일 09:23 KST에 [워크플로](../workflows/github-weekly.yml)가 실행됩니다. 기존 뉴스·자료 게시와 같은 concurrency 그룹을 써서 저장소 쓰기를 직렬화합니다. 이후 push가 경쟁하면 원격을 fetch하고 정상 rebase·push하며, 충돌이 나면 실패합니다. 강제 push는 하지 않습니다.

수집은 HTML 구조·저장소 이름·주간 증가량·중복을 검사합니다. 한 저장소의 조회나 번역이 실패하면 그 실행에서는 불완전한 새 목록을 게시하지 않습니다. 이미 발행된 주의 기록은 그대로 두고, 중단 때문에 JSON만 남았다면 그 관측 데이터로 본문을 복구합니다. 원본 HTML·README를 실행하거나 프로젝트를 자동 설치하지 않습니다. 외부 HTML은 설명과 숫자를 읽는 입력으로만 사용합니다.

한국어 해설은 저장소 ID와 설명 해시가 맞을 때 사용합니다. 변경된 설명이나 처음 나타난 영어 소개는 Argos Translate 1.11.0과 영어→한국어 모델 1.1로 runner CPU에서 번역합니다. 결과에는 번역 방식을 기록하며 GPT·유료 번역 API를 호출하지 않습니다. 모델이 없으면 Argos 공식 목록에서 내려받고, 이미 번역한 같은 원문은 캐시를 사용합니다.

```sh
python3 -m pip install -r .github/github-weekly/requirements.txt
python3 -m unittest discover -s .github/github-weekly -p 'test_*.py' -v
python3 .github/github-weekly/collect.py
```

로컬 명령은 수집 파일만 만듭니다. 게시 명령은 GitHub Actions에서 `python3 .github/github-weekly/publish.py`로 실행합니다. 번역 모델도 직접 확인하려면 수동 실행의 `check_translation`을 켭니다. 번역 검사 문장은 운영 캐시에 넣지 않습니다.

2026년 11월 2일 [첫 서버 실행](https://github.com/yoonip/engineering-notes/actions/runs/41364746396)에서 21개 검사, 공개 영어→한국어 모델의 CPU 번역과 임시 폴더를 이용한 실제 원본 수집을 통과했습니다. 운영 기록은 같은 주가 이미 발행되어 재작성하지 않았으며, 게시 단계도 새 변경 없이 종료했습니다.
