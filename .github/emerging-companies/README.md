# 신생기업 원문 수집과 자동 분석

이 도구는 GitHub Actions에서 공개 원문을 수집하고 로컬 공개 모델로 한국어 기업 분석을 생성합니다. 별도 모델 검토와 결정적 형식·근거 검사를 통과한 결과만 `신생기업과기술사업_emerging-companies/자동분석_auto-research/날짜/`에 게시할 수 있도록 준비합니다. 사람의 원문 대조나 독립 기관 검증과는 구분합니다.

## 실행 경로

1. `sources.json`에 지정한 대학·투자사·액셀러레이터의 현재 원문 목록에서 새 자료 후보를 찾습니다.
2. 미등재 기업의 회사명·식별자·회사 도메인을 기존 목록과 대조합니다. 초기 후보는 `research_candidates.json`에도 둘 수 있습니다.
3. 초기 후보가 없거나 검토에서 탈락하면 새로 발견한 기관 원문에 실제로 연결된 회사 홈페이지를 후보로 제안합니다. 모델이 임의로 만든 URL은 사용하지 않습니다.
4. 공개 HTTPS 원문을 둘 이상 가져옵니다. 호스트 허용 목록·공개 DNS·리디렉션·robots.txt·시간·응답 크기를 검사합니다. 자료가 부족하거나 접근을 허용하지 않으면 건너뜁니다.
5. 실제로 읽은 원문만 로컬 모델에 전달합니다. 각 사실은 원문 식별자와 원문 그대로의 짧은 근거 문자열에 대응해야 합니다.
6. 인용 문자열의 실재·숫자의 인용 내 존재·자료 수·한국어 형식·본문 길이·허용된 파일 경로를 검사합니다.
7. 같은 로컬 모델의 별도 호출로 초안과 원문을 다시 비교합니다. 이는 별도 자동 검토 단계이며 독립 기관이나 사람의 검증은 아닙니다.
8. 통과한 본문과 목차·출처·목록·조사 기록을 출력합니다. 게이트를 통과하지 못한 초안은 게시하지 않으며 원인을 아티팩트에 남깁니다.

실행마다 새 기업 둘 또는 셋을 목표로 할 수 있지만 수량을 맞추려고 부실한 본문을 채우지 않습니다. 모델의 문장과 검토 판단이 틀릴 수 있으며 자동 검사가 오류를 모두 찾는다고 보장하지 않습니다. 자동 분석은 사람이 대조한 기존 본문과 폴더·표기로 구분합니다.

## 파일과 명령

`pipeline.py`는 후보 수집·중복·상태·결과물을 관리합니다. `llm_research.py`는 원문 제한, 로컬 모델 호출, 사실별 근거와 별도 모델 검토를 담당합니다. `publish.py`는 결과 manifest에 있는 허용 경로만 복사·커밋합니다.

수집과 검토 완료 큐 확인만 수행하는 명령입니다.

```bash
python .github/emerging-companies/pipeline.py --root . --output research-output
```

로컬 모델 서버가 준비된 뒤 자동 분석을 시험하되 본문 게시 파일은 만들지 않는 명령입니다. 초안과 검토 결과는 `research-output/audits`에 남습니다.

```bash
python .github/emerging-companies/pipeline.py --root . --output research-output --auto-research --limit 1
```

검사를 통과한 결과의 게시 파일을 준비하려면 `--publish-ready`를 추가합니다. 실제 커밋·푸시는 별도 단계입니다.

```bash
python .github/emerging-companies/pipeline.py --root . --output research-output --auto-research --limit 3 --publish-ready
python .github/emerging-companies/publish.py --root . --output research-output --push
```

모델 호출은 고정된 루프백 주소 `http://127.0.0.1:8080/v1/chat/completions`만 허용합니다. 기본 Python 표준 라이브러리를 사용하며 API 키를 보내지 않습니다. 실행에 쓰는 모델 파일·리비전·해시는 런타임 설치 도구와 workflow에서 고정해야 합니다. `LOCAL_MODEL_ID`와 `LOCAL_MODEL_REVISION`은 검토 아티팩트의 추적 정보로 남습니다.

## 검토 완료 큐

사람이 미리 검토한 본문은 선택적으로 `reviewed` 폴더에 Markdown과 JSON으로 둘 수 있습니다. JSON에는 `status: reviewed`, 검토자·검토일, 본문 SHA-256, 기업 정보, 실제로 읽은 원문 URL 둘 이상과 원문 SHA-256이 있어야 합니다. 본문이나 원문이 검토 뒤 달라졌다면 자동 게시를 중단합니다. 이 경로의 검토자 표기를 자동 모델 결과에 재사용하지 않습니다.

자동 분석은 사전 원문 전체를 커밋하지 않습니다. 아티팩트에는 원문 URL·해시·모델 입력 길이·초안·근거 인용·검토 결과·실패 단계만 남깁니다. 웹문서의 실행 지시, 외부 링크나 모델이 만든 명령을 실행하지 않습니다. 생성 결과는 코드·workflow·인증 파일을 수정할 수 없습니다.

## 실패와 재시도

접근 제한, 원문 부족, 모델 시간 초과, JSON 오류, 근거 불일치, 자동 검토 탈락은 결과에 구분해 남습니다. 탈락한 기업은 상태가 저장된 경우 일정 기간 뒤 다시 시도하며 그동안 다른 후보를 탐색합니다. 모든 자동 분석이 탈락하면 종료 코드 2와 `needs_review` 결과를 남깁니다. 아티팩트만 생성한 실행을 새 분석 게시 성공으로 보고하지 않습니다.

## 검증

```bash
python -m unittest discover -s .github/emerging-companies -p test_pipeline.py -v
```

테스트는 비공개 주소·다른 호스트 리디렉션·경로 이탈, 출처 중복, 원문 인용·숫자 매핑, 두 번째 모델의 거부, 실패 기록과 자동 분석 표기를 검사합니다. 모의 원문·모의 모델 테스트와 실제 GitHub 실행은 별도 검증입니다.

## GitHub 실행의 조건

GitHub의 공식 안내에 따르면 GitHub Models의 추론 API는 2026-07-30 종료되었습니다. 따라서 이 도구는 종료된 무료 추론 서비스를 호출하지 않습니다. CPU 러너 안에서 별도로 고정한 공개 모델을 실행하는 경로를 사용합니다. [GitHub Models 종료 안내](https://docs.github.com/en/github-models)

GitHub Actions의 예약은 서버에서 실행되며 예약 시각에 지연될 수 있습니다. 매일 한국시간 오전 9시는 UTC 자정에 해당합니다. 개인 컴퓨터나 ChatGPT 예약은 이 workflow의 실행 조건이 아닙니다. [GitHub의 schedule 설명](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

실행 상태와 실제 게시 수는 Actions 요약·아티팩트·해당 실행의 커밋에서 확인합니다. 모델·원문·검토 게이트를 실제로 실행한 기록이 없는 상태에서는 전체 자동 분석이 검증됐다고 적지 않습니다.
