# 외부 PR과 권한 있는 GitHub Actions workflow | Untrusted pull requests and privileged workflows

[분야 목차](README.md) · [소프트웨어 공급망과 배포](09-소프트웨어공급망과배포_software-supply-chain.md) · [비밀정보 수명주기와 CI 자격 증명](28-비밀정보수명주기와CI자격증명_secrets-lifecycle.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## PR 코드가 실행되면 검토 대상이 작업 환경이 됩니다

외부 pull request(PR)는 변경된 소스 파일만 제공하지 않습니다. 빌드 스크립트, 테스트, 패키지 설치 hook, 설정 파일, 하위 의존성도 바꿀 수 있습니다. CI가 이를 빌드하거나 실행하면 작성자가 제공한 코드가 runner 안에서 실행됩니다. 그 job에 비밀정보나 쓰기 권한 token이 있으면 실행 코드는 해당 권한을 악용할 수 있습니다. 실행하지 않더라도 PR 제목·본문·브랜치 이름과 artifact는 신뢰하지 않는 입력으로 다뤄야 합니다.

핵심은 이벤트 이름 자체를 안전·위험으로 나누는 데 있지 않습니다. workflow가 어떤 commit의 YAML을 읽고, 어떤 코드를 실행하며, 어떤 권한과 비밀정보를 받는지 한 작업 단위로 확인해야 합니다. [GitHub의 workflow 보안 지침](https://docs.github.com/en/actions/reference/security/secure-use)

## 이벤트마다 실행 기준과 권한 경계가 다릅니다

| 이벤트 | workflow가 실행되는 기준 | fork PR에서 유의할 점 | 권장 용도 |
| --- | --- | --- | --- |
| `pull_request` | PR의 merge commit 문맥에서 검증합니다. | fork의 workflow에는 기본적으로 읽기 전용 `GITHUB_TOKEN`이 제공되고 저장소 비밀정보는 전달되지 않습니다. 비공개 저장소에는 조직·저장소 정책으로 이 기본 동작을 바꾸는 설정이 있으므로 확인해야 합니다. | 비밀정보가 필요 없는 빌드·시험을 격리된 runner에서 수행합니다. |
| `pull_request_target` | 대상 저장소 기본 브랜치의 workflow 문맥에서 실행합니다. PR에서 온 제목·본문·변경 정보를 처리할 수 있도록 만들어진 이벤트입니다. | 권한 있는 token이나 secret을 쓸 수 있는 문맥입니다. PR 코드를 checkout·빌드·실행하면 그 코드가 권한을 이용할 수 있습니다. | PR에 label을 붙이거나 제한된 메타데이터 작업을 수행할 때 사용합니다. |
| `workflow_run` | 다른 workflow가 시작되거나 끝난 뒤 기본 브랜치의 별도 workflow를 시작합니다. | 앞 단계가 읽기 전용이어도 후속 workflow는 secret과 쓰기 권한을 가질 수 있습니다. 앞 단계 artifact의 내용은 신뢰 근거가 아닙니다. | 별도 승인·검증이 필요한 후속 조치를 처리하되, 앞 단계의 코드나 artifact를 실행하지 않습니다. |

fork PR의 기본 권한만으로 모든 저장소가 안전하다고 볼 수는 없습니다. 비공개 저장소는 fork workflow에 쓰기 token이나 secret을 허용하는 설정이 있고, 같은 저장소에 쓰기 권한이 있는 기여자는 workflow 변경을 제안할 수 있습니다. 조직·저장소의 Actions 정책, event별 `permissions`, 환경 승인 규칙과 branch 보호를 함께 확인합니다. [fork workflow 설정](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository), [workflow event 설명](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

## 권한이 섞이는 대표 경로

1. PR이 `Makefile`, package manifest, 테스트 설정이나 build script를 바꿉니다.
2. 권한 있는 이벤트가 PR head를 checkout하고 install·build·test 명령을 실행합니다.
3. 변경 코드나 설치 hook이 runner 안에서 명령을 실행합니다.
4. 실행 중인 workflow가 접근 가능한 secret·token·캐시·네트워크 자원이 악용될 수 있습니다.
5. 쓰기 token이 있으면 저장소 변경, PR 수정, release 또는 다른 workflow 실행까지 피해가 이어질 수 있습니다.

`actions/checkout` 단계만으로 코드가 실행되지는 않지만, checkout한 경로에서 `npm install`, 빌드, 테스트를 실행하면 PR이 바꾼 설정과 의존성이 실행될 수 있습니다. 실행 지점은 눈에 보이는 `run:` 한 줄에 한정되지 않습니다. GitHub는 이 조합을 `pull_request_target` 및 `workflow_run` 보안 위험으로 설명합니다. [GitHub: Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target), [GitHub Security Lab: Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)

## 안전한 workflow는 신뢰 수준별로 나눕니다

### 1. 외부 코드 시험

가능하면 `pull_request`로 실행하고 필요한 권한만 부여합니다. fork PR 코드가 secret에 접근하지 않도록 하고, 쓰기가 필요하지 않은 시험에는 `GITHUB_TOKEN` 읽기 권한만 둡니다. 제삼자 action은 검토한 commit SHA로 고정합니다. PR에서 수정한 workflow 파일과 build 설정도 코드처럼 검토하며, 처음 참여하는 기여자의 workflow 실행은 저장소의 승인 정책에 따릅니다.

다음 YAML은 권한을 좁히는 부분만 보여 주는 발췌입니다. 이벤트 필터, checkout, 시험 명령, action의 검토된 commit SHA는 생략했으므로 완성된 workflow가 아닙니다.

```yaml
permissions:  # workflow 또는 job에 부여할 GITHUB_TOKEN 권한을 지정합니다.
  contents: read  # 저장소 파일을 읽는 권한만 허용합니다.
```

이 권한은 다른 자격 증명이나 runner의 네트워크 접근까지 제한하지는 않습니다. 시험 코드가 비밀정보를 받지 않는지, runner가 내부 서비스에 연결되는지, job 사이에 파일·캐시가 남는지도 별도로 봅니다.

### 2. PR 메타데이터 처리

label 설정이나 간단한 안내처럼 저장소 쓰기 권한이 필요한 작업은 `pull_request_target`을 검토할 수 있습니다. 이 이벤트에서는 PR의 제목·본문·브랜치 이름을 shell 명령에 직접 삽입하지 않습니다. 해당 이벤트의 workflow는 신뢰된 기본 브랜치에서 실행하되, fork의 코드나 artifact를 checkout·다운로드해 build·test·실행하지 않습니다. 작업이 PR 코드를 검사해야 한다면 권한 없는 별도 `pull_request` job으로 분리합니다.

### 3. 시험 결과를 쓰기 작업으로 전달

읽기 전용 시험 뒤에 PR comment 같은 쓰기 작업이 꼭 필요하면 workflow를 나눌 수 있습니다. 다만 `workflow_run`의 후속 job은 앞 단계보다 높은 권한을 가질 수 있으므로 결과 artifact를 코드나 shell 입력으로 실행해서는 안 됩니다.

| 후속 job이 확인할 항목 | 이유 |
| --- | --- |
| 완료된 workflow의 ID·이름·event 종류 | 다른 workflow의 실행 결과를 잘못 받지 않도록 합니다. |
| 저장소 전체 이름, 대상 branch, head commit SHA | 다른 저장소나 예상하지 않은 revision의 결과를 거부합니다. |
| 실행 결론과 PR의 연결 관계 | 실패·취소된 실행이나 무관한 PR 결과를 성공으로 표시하지 않습니다. |
| artifact ID와 크기·형식 | 요청한 실행에 속한 결과만 받고, 크기와 자료 형식을 제한합니다. |
| 출력에 허용할 필드 | 고정된 상태 코드와 숫자만 사용하고 임의 문자열은 명령·Markdown·HTML로 해석하지 않습니다. |

메타데이터 확인은 artifact의 신뢰성을 만들어 주지 않습니다. artifact는 계속 입력 자료입니다. 가능하면 GitHub API의 check 결과처럼 플랫폼이 관리하는 실행 정보를 사용합니다. 파일을 받아야 한다면 지정한 파일 형식만 파싱하고, 추출 파일의 경로·크기·중복 키·자료형을 확인하며, 스크립트나 실행 파일로 호출하지 않습니다. 파서가 취약할 수 있으므로 최소 권한·격리된 runner도 유지합니다.

다음 Python 코드는 CI 결과 JSON의 형식과 크기만 제한하는 직접 작성한 교육용 예시입니다. artifact가 어느 저장소·workflow·commit에서 왔는지 인증하지 않으며, 서명 검증·악성 파일 검사·실제 운영 배포를 대신하지 않습니다. 이 예제는 실행하지 않았습니다.

```python
import json  # JSON 문서를 파싱하는 표준 라이브러리를 가져옵니다.
from pathlib import Path  # 파일 경로와 바이트 읽기를 다루는 표준 라이브러리를 가져옵니다.

MAX_BYTES = 16_384  # 결과 파일의 최대 크기를 16 KiB로 제한합니다.
ALLOWED_KEYS = {"schema_version", "status", "passed", "failed"}  # 허용할 필드 이름만 모읍니다.

def reject_duplicate_keys(pairs):  # JSON 객체의 키·값 쌍을 받아 중복 키를 거부합니다.
    result = {}  # 검증한 키·값을 담을 새 딕셔너리입니다.
    for key, value in pairs:  # JSON 객체의 각 항목을 순서대로 확인합니다.
        if key in result:  # 같은 키가 이미 있으면 문서 해석이 모호합니다.
            raise ValueError("duplicate JSON key")  # 중복 키가 있는 입력을 실패 처리합니다.
        result[key] = value  # 중복이 아닌 항목을 결과에 보관합니다.
    return result  # 중복 검사를 마친 객체를 JSON 파서에 돌려줍니다.

def read_ci_summary(path: Path, report_dir: Path):  # 신뢰된 결과 폴더 안의 고정 보고서에서 제한된 값만 읽습니다.
    root = report_dir.resolve(strict=True)  # workflow가 정한 보고서 폴더의 실제 위치를 확인합니다.
    resolved = path.resolve(strict=True)  # 심볼릭 링크를 따라 실제 파일 위치를 확인합니다.
    if not root.is_dir() or root not in resolved.parents:  # 폴더가 유효하고 파일이 그 하위에 있는지 확인합니다.
        raise ValueError("report path is outside the report directory")  # 폴더 밖의 경로와 링크를 거부합니다.
    with resolved.open("rb") as stream:  # 확인한 파일을 바이너리 모드로 열어 읽기량을 제한합니다.
        raw = stream.read(MAX_BYTES + 1)  # 제한보다 한 바이트 더 읽어 초과 여부만 판별합니다.
    if len(raw) > MAX_BYTES:  # 파싱 전에 파일 크기를 제한합니다.
        raise ValueError("report is too large")  # 지나치게 큰 결과 파일을 거부합니다.
    document = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)  # UTF-8 JSON을 파싱하면서 중복 키도 검사합니다.
    if type(document) is not dict or set(document) != ALLOWED_KEYS:  # 최상위 구조와 필드 집합을 고정합니다.
        raise ValueError("unexpected report shape")  # 예상하지 않은 구조는 사용하지 않습니다.
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:  # 버전은 정확히 정수 1이어야 합니다.
        raise ValueError("unsupported report version")  # 모르는 형식의 결과를 거부합니다.
    if type(document["status"]) is not str or document["status"] not in {"passed", "failed"}:  # 문자열 상태만 허용된 값과 비교합니다.
        raise ValueError("invalid status")  # 자유 형식 문자열이 상태를 대신하지 못하게 합니다.
    for name in ("passed", "failed"):  # 시험 개수 필드를 각각 검사합니다.
        if type(document[name]) is not int or not 0 <= document[name] <= 1_000_000:  # bool과 음수·과도한 값을 거부합니다.
            raise ValueError("invalid test count")  # 안전한 정수 범위를 벗어나면 사용하지 않습니다.
    expected = "passed" if document["failed"] == 0 else "failed"  # 실패 개수에서 상태를 독립적으로 계산합니다.
    if document["status"] != expected:  # 제출된 상태와 개수의 관계를 대조합니다.
        raise ValueError("status does not match counts")  # 모순된 결과는 후속 job에 전달하지 않습니다.
    return {name: document[name] for name in ALLOWED_KEYS}  # 허용 목록에 있는 필드만 새 객체로 반환합니다.
```

이 코드는 신뢰된 workflow가 지정한 보고서 폴더 안의 파일만 읽고 JSON 모양을 제한할 뿐입니다. artifact 압축을 안전하게 푸는 절차, run metadata 인증, 서명 검증은 구현하지 않았습니다. 반환값을 PR comment에 넣을 때는 Markdown 해석이나 API 요청에 임의 데이터를 다시 삽입하지 말고, 인증된 run metadata 검사를 별도로 적용해야 합니다. [Python `json` 문서](https://docs.python.org/3/library/json.html), [Python `pathlib` 문서](https://docs.python.org/3/library/pathlib.html)

## 캐시와 runner도 권한 경계에 포함합니다

캐시는 서명된 빌드 증거가 아닙니다. 캐시를 쓸 수 있는 낮은 신뢰도의 job이 실행 파일이나 build input을 캐시에 넣고, 나중에 높은 권한 job이 이를 복원해 실행하면 PR 코드가 경계를 넘어갈 수 있습니다. GitHub는 `pull_request_target`에서 기본 cache 접근을 읽기 전용으로 제한하지만, write-capable `cache-mode`를 명시하면 cache poisoning 위험이 다시 생깁니다. 낮은 신뢰도의 workflow가 만든 캐시는 비밀정보가 있는 job에서 신뢰하지 않습니다. [GitHub dependency caching 보안 지침](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)

외부 코드를 처리하는 self-hosted runner는 내부 네트워크·cloud metadata endpoint·다른 job의 파일에 접근하지 못하도록 분리하고, 실행 뒤 재사용하지 않는 구성을 고려합니다. 격리 없는 컨테이너 하나만으로 호스트와 네트워크 경계가 보장되지는 않습니다. 물리·가상 환경을 재사용한다면 작업 뒤 임시 파일·자격 증명·프로세스·캐시를 정리해도 남는 상태가 없는지 확인해야 합니다. GitHub도 권한 있는 `pull_request_target` workflow의 compute를 격리·일회용으로 운영하라고 안내합니다.

## 운영 전 점검표

- 외부 코드 시험과 secret·쓰기 token을 사용하는 작업을 서로 다른 workflow와 runner로 나눴습니다.
- `pull_request_target`은 실제로 필요한 메타데이터 처리에만 사용하고, fork 코드를 checkout·build·실행하지 않습니다.
- `workflow_run`에서 앞 단계 artifact를 실행하지 않으며, run·저장소·branch·commit을 확인합니다.
- 각 job의 `permissions`를 필요한 범위로 줄이고, 환경 보호 규칙과 승인자를 확인합니다.
- action을 검토한 전체 commit SHA로 고정하고, 입력·설정 파일도 외부 코드처럼 검토합니다.
- 낮은 신뢰도의 job에서 만든 캐시나 artifact를 높은 권한 job의 실행 입력으로 취급하지 않습니다.
- 외부 PR 실행에 사용하는 runner의 네트워크 경로·수명·재사용 여부를 확인합니다.
- CodeQL for Actions 등 workflow 분석 결과를 검토하고 실제 trigger·권한·checkout ref를 함께 살펴봅니다.

## 출처와 적용 범위

- [GitHub Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target): 기본 브랜치 문맥, 안전한 메타데이터 처리, 신뢰하지 않는 코드 checkout, cache와 runner 경계를 확인했습니다.
- [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): `pull_request`, `pull_request_target`, `workflow_run`의 이벤트 문맥과 fork 동작을 확인했습니다.
- [Managing GitHub Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository): fork PR의 token·secret·승인 정책 설정 범위를 확인했습니다.
- [GitHub dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching): 낮은 신뢰도의 trigger에서 cache 쓰기 권한이 생길 때의 위험과 제한을 확인했습니다.
- [GitHub Security Lab: Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/): PR build·test·dependency install이 공격자 코드 실행으로 이어지는 경로를 확인했습니다.
- [Python JSON decoder](https://docs.python.org/3/library/json.html), [Python pathlib](https://docs.python.org/3/library/pathlib.html): 예제에 사용한 표준 라이브러리 API를 확인했습니다.

이 글의 Python 코드는 직접 작성한 입력 검증 예시이며, 실행 결과나 workflow 전체의 안전성을 주장하지 않습니다. 실제 권한은 저장소·조직 설정, event, runner 유형, job permission, artifact 경로가 함께 결정하므로 해당 설정을 기준으로 검토해야 합니다.

## English

Treat pull request code, workflow output, caches, and artifacts as untrusted input. Use `pull_request` for isolated checks with minimal permissions. Reserve `pull_request_target` for metadata operations and never build or run fork code in that privileged context. A `workflow_run` job can have more privileges than the workflow that triggered it, so validate run metadata and parse artifacts as data without executing them. The included Python example only constrains a JSON report's size and shape; it does not authenticate the artifact or prove workflow safety.
