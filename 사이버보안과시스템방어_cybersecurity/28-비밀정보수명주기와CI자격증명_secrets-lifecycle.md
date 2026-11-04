# 비밀정보 수명주기와 CI 자격 증명 | Secrets lifecycle and CI credentials

[분야 목차](README.md) · [소프트웨어 공급망과 배포](09-소프트웨어공급망과배포_software-supply-chain.md) · [기업 계정과 관리자 권한](20-기업계정과관리자권한_enterprise-identity.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 비밀정보는 이름이 아니라 권한으로 판단합니다

비밀정보(secret)는 외부에 공개되면 계정·서비스·데이터에 접근하거나 서명·복호화를 할 수 있는 인증 자료입니다. 비밀번호뿐 아니라 API 키, 개인용 액세스 토큰(PAT), 데이터베이스 연결 자격 증명, 서명용 개인 키, 인증서와 세션 토큰도 포함합니다. 설정값처럼 보여도 해당 값으로 권한을 얻을 수 있다면 비밀정보로 관리합니다. 반대로 공개 식별자나 권한이 없는 일반 설정값까지 모두 비밀로 취급하면 보관·교체 과정이 불필요하게 복잡해집니다.

비밀정보는 만들고 저장하는 일에서 끝나지 않습니다. 누가 어떤 서비스에서 어떤 범위로 사용하는지 목록화하고, 필요한 순간에만 전달하고, 사용 기록을 남기며, 교체·폐기·만료까지 추적해야 합니다. CI/CD 파이프라인에 장기 자격 증명을 보관하면 저장소 관리자, workflow 변경자, 실행 action, runner와 로그가 모두 노출 경계에 들어갑니다. [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

```mermaid
flowchart LR
  INV["목록·소유자·권한 범위"] --> ISSUE["발급·수명 설정"]
  ISSUE --> USE["필요한 작업에 전달"]
  USE --> AUDIT["사용 기록·이상 사용 감시"]
  AUDIT --> ROTATE["교체·소비자 전환"]
  ROTATE --> REVOKE["이전 값 폐기·만료"]
  USE -. "노출 의심" .-> CONTAIN["권한 차단·영향 확인"]
  CONTAIN --> ROTATE
  CONTAIN --> AUDIT
```

## 비밀정보 목록에는 값 대신 관리 정보를 둡니다

목록이나 사고 문서에 실제 비밀값을 복사하면 노출 지점을 하나 더 만듭니다. 비밀 저장소의 항목 ID나 제공자 측 식별자만 기록하고, 실제 값은 저장하지 않습니다.

| 관리 항목 | 기록할 내용 |
| --- | --- |
| 소유자와 담당자 | 발급 팀, 운영 팀, 사고 때 승인·폐기를 맡을 연락 경로입니다. |
| 목적과 소비자 | 연결된 서비스·workflow·데이터베이스와 각 사용 목적입니다. |
| 권한 범위 | 읽기·쓰기 대상, 조직·프로젝트 범위, 네트워크·환경 제한입니다. |
| 저장 위치 | GitHub Actions secret, 클라우드 비밀 저장소, 인증서 관리자 등입니다. |
| 수명 | 발급 시각, 만료 시각, 마지막 사용, 교체 주기와 폐기 방법입니다. |
| 사용 기록 | 누가·어떤 job이나 workload로 읽거나 사용했는지 확인할 감사 경로입니다. |
| 교체 영향 | 기존 값과 새 값이 동시에 허용되는지, 소비자별 적용 순서와 복구 방법입니다. |

비밀 종류에 따라 교체 방법이 다릅니다. 애플리케이션 API 키는 새 키를 발급해 소비자를 옮긴 뒤 이전 키를 폐기할 수 있지만, 데이터 암호화 키는 기존 자료의 복호화와 재암호화 계획이 필요할 수 있습니다. 사용자 비밀번호·서명 키·서비스 계정·인증서에 같은 회전 절차를 적용하지 말고, 발급자의 공식 폐기·교체 기능을 확인합니다. OWASP는 생성·교체·폐기·만료를 수명주기 단계로 다루고, 동적 자격 증명은 소비가 끝났다고 자동 폐기된 것으로 간주하지 말고 실제 lease 만료나 명시적 revoke를 연결하라고 설명합니다. [OWASP 비밀정보 수명주기](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

## CI job은 장기 자격 증명 대신 짧은 권한을 받도록 설계합니다

| 방식 | 자격 증명이 생기는 곳 | 적합한 경우 | 주요 한계 |
| --- | --- | --- | --- |
| 장기 API 키·PAT를 저장소 secret으로 보관 | 저장소·조직·환경 설정에 저장한 값을 job이 읽습니다. | 공급자가 연합 인증을 지원하지 않거나 정적 키만 제공할 때 사용합니다. | 저장 위치가 늘고 만료·교체를 놓치기 쉽습니다. 노출되면 폐기 전까지 job 바깥에서도 재사용될 수 있습니다. |
| 중앙 비밀 저장소에서 job이 조회 | job 신원이 비밀 저장소에 인증한 뒤 필요한 항목을 읽습니다. | DB 암호 등 실제 애플리케이션 비밀을 관리해야 할 때 사용합니다. | 비밀 저장소 접근용 identity 자체도 최소 권한·로그·만료가 필요합니다. |
| OIDC 연합으로 단기 cloud token 발급 | job이 GitHub OIDC token을 요청하고 클라우드의 신뢰 정책을 통과하면 단기 접근 token을 받습니다. | GitHub Actions에서 AWS·Azure·GCP 등 연합 인증을 지원하는 클라우드 역할을 사용할 때 적합합니다. | workflow 자체가 침해되면 허용된 역할과 작업 범위 안에서 단기 token을 악용할 수 있습니다. 공급자 쪽 신뢰 조건을 좁혀야 합니다. |

GitHub Actions OIDC에서는 workflow가 토큰을 요청할 수 있도록 `id-token: write` 권한을 줍니다. 이 권한만으로 클라우드 자원에 쓸 수 있는 것은 아닙니다. 클라우드 제공자가 GitHub를 신뢰하는 연합 공급자로 등록하고 `iss`, `aud`, `sub` 등의 조건을 검사한 뒤 권한을 부여해야 합니다. 조건이 너무 넓으면 다른 저장소나 불신 workflow가 역할을 요청할 수 있습니다. [GitHub Actions OIDC 설정](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers), [OIDC claim과 trust 조건](https://docs.github.com/en/actions/reference/security/oidc)

다음은 workflow 권한 범위를 보여 주는 YAML 발췌입니다. 클라우드 제공자용 공식 action과 신뢰 정책을 생략했으므로 완성된 배포 workflow는 아닙니다.

```yaml
permissions: {}  # 최상위에서는 별도로 허용하지 않은 GITHUB_TOKEN 권한을 부여하지 않습니다.
jobs:  # jobs는 workflow에서 실행할 작업들을 묶습니다.
  deploy:  # deploy는 배포 작업의 식별자입니다.
    environment: production  # production 환경에 승인·브랜치 보호 규칙을 설정할 수 있습니다.
    permissions:  # 이 job만 요청할 GitHub 권한을 지정합니다.
      contents: read  # 저장소 checkout이 필요한 경우에만 소스 읽기를 허용합니다.
      id-token: write  # job이 OIDC JWT를 요청하게 하며 클라우드 자원 권한을 직접 주지는 않습니다.
```

`id-token: write`는 job 단위로 필요한 곳에만 둡니다. Cloud IAM의 신뢰 정책은 저장소·브랜치·environment를 제한하고, 필요한 경우 지원되는 claim으로 재사용 workflow까지 제한합니다. environment를 사용하면 `sub`의 형식이 branch 기반 예시와 달라집니다. 또한 GitHub는 2026년 7월 15일부터 새 저장소에 owner·repository ID를 포함하는 immutable subject 형식을 기본 적용하기 시작했습니다. 그 전에 만든 저장소는 별도 선택이 없으면 기존 형식을 유지할 수 있고, 이후 이름 변경·이전도 trust subject에 영향을 줄 수 있습니다. 운영 중인 trust policy에 예전 형식을 그대로 복사하지 말고 실제 저장소가 발급하는 claim과 클라우드 정책을 대조합니다. [GitHub OIDC subject 형식과 immutable claim](https://docs.github.com/en/actions/reference/security/oidc)

OIDC는 장기 cloud key를 줄이는 수단이지 workflow 보안을 대신하지 않습니다. 배포 branch와 environment 보호, action을 검토된 전체 commit SHA로 고정, 외부 PR과 배포 job 분리, 필요한 cloud 권한만 부여, 실행·승인 감사 기록을 함께 적용합니다. workflow가 허용된 신뢰 조건을 만족하면 공격자도 해당 job의 권한을 받을 수 있으므로, 신뢰할 수 있는 branch에 악성 workflow 변경이 들어가지 않게 막는 통제가 중요합니다.

## 저장소 탐지는 예방 통제와 사고 대응을 함께 사용합니다

GitHub secret scanning은 알려진 제공자 패턴과 구성에 따라 활성화된 범위에서 저장소 기록 등을 살펴보고 탐지 경보를 만들 수 있습니다. Push protection은 탐지 가능한 비밀정보를 원격 저장소에 올리기 전에 push를 막습니다. 하지만 모든 비밀 형식과 모든 경로를 알아내는 보장은 아닙니다. 일반 형식·사용자 정의 형식의 검사 여부는 보안 설정을 확인합니다. GitHub Actions 로그 마스킹도 비밀이 출력되지 않게 해 주는 보안 경계는 아닙니다. 값이 변환되거나 구조화된 데이터 안에 포함되면 자동 가림이 실패할 수 있고, workflow에서 새 민감 값을 만들었다면 별도로 등록해야 합니다. 비밀값을 workflow 출력에 쓰지 않습니다. [GitHub Secret Scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning), [GitHub Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection), [GitHub Actions 보안 사용 지침](https://docs.github.com/en/actions/reference/security/secure-use)

탐지 경보는 유출 사실의 확인과 대응을 시작하는 신호입니다. 스캐너가 해당 비밀을 지원하지 않거나 아직 알려지지 않은 형식이면 경보가 없을 수 있습니다. 값의 유효성은 발급자의 상태와 감사 기록으로 확인합니다. 정기 점검에서 저장소 파일 외에 workflow·issue·pull request·토론·artifact·runner 출력과 비밀 저장소의 읽기 이력도 검토합니다.

## 자격 증명이 노출되면 먼저 사용을 막고 소비자를 추적합니다

GitHub는 비밀값을 코드에서 지우는 것만으로는 사용을 막지 못한다고 설명합니다. 공개 저장소의 키는 자동 수집될 수 있으므로 노출된 비밀은 우선 침해된 것으로 간주합니다. [GitHub leaked secret 대응 절차](https://docs.github.com/en/code-security/tutorials/remediate-leaked-secrets/remediating-a-leaked-secret)

| 순서 | 조치 | 확인할 근거 |
| --- | --- | --- |
| 1. 유형·영향 확인 | 비밀 유형, 발급자, 권한 범위, 공개 여부, 활성 상태와 소비자를 파악합니다. | secret-scanning 경보, 저장소 위치, 환경 설정, 업무 서비스 목록입니다. |
| 2. 접근 차단 | 노출된 키를 발급자 측에서 폐기합니다. 업무 중단을 줄이기 위해 이중 키 전환이 가능하면 새 키를 소비자에 적용한 직후 이전 키를 폐기합니다. | 발급자에서 폐기 시각·상태와 새 키 발급 기록을 확인합니다. |
| 3. 사용 흔적 조사 | 마지막 정상 사용 이후의 호출·IP·대상·권한 변경을 검토합니다. | 클라우드 audit log, API 사용 기록, DB 로그인·권한 이력입니다. |
| 4. 소비자 교체 | workflow, 앱, 배치, 통합 서비스와 운영 환경에 새 자격 증명을 반영합니다. | 정상 health check, 새 식별자 사용 여부, 실패·재시도 로그입니다. |
| 5. 복제본 확인 | 같은 값이 다른 브랜치·저장소·issue·로그·artifact에 복사됐는지 찾고 저장 위치를 정리합니다. | 조직 전체 검색 결과, secret store 접근 이력, runner와 배포 로그입니다. |
| 6. 이력 정리 판단 | 키 폐기 후에도 Git 기록을 지울 필요가 있는지 판단하고, 필요하면 clone·fork·pull request 영향을 협의합니다. | 커밋 참조, 다른 clone, 캐시, 협업자의 재동기화 계획입니다. |
| 7. 재발 통제 | 원인 workflow·권한·저장 경로를 수정하고, 수명주기 목록·탐지·회귀 확인을 갱신합니다. | 새 권한 정책, scanner 설정, owner와 폐기 절차입니다. |

이전 키를 폐기할 때 영향이 큰 서비스라면 노출 위험과 중단 위험을 함께 평가합니다. 높은 권한의 활성 키가 공개된 경우에는 사용을 지속시키지 않도록 신속히 차단합니다. 공급자가 이중 키를 지원하면 새 키를 발급하고 소비자를 바꾼 뒤 이전 키를 바로 폐기하는 순서를 쓸 수 있습니다. 폐기 후에는 같은 계정의 다른 키, refresh token, 세션·인증서와 연동 애플리케이션을 따로 조사합니다. 하나의 키를 바꾸었다고 연결된 모든 접근 경로가 사라지는 것은 아닙니다.

## Git 기록을 다시 쓰는 일은 비밀 폐기와 별개의 결정입니다

파일에서 비밀 문자열을 삭제하고 새 commit을 올려도 과거 commit·fork·다른 사람의 clone·캐시에는 값이 남을 수 있습니다. 먼저 제공자에서 키를 폐기하고 소비자를 교체합니다. 그 뒤에도 기록 정리가 필요하면 영향받는 branch와 tag, pull request, fork, 협업자의 clone을 확인하고 history rewrite를 계획합니다. force push는 다른 작업자의 branch와 commit 링크를 깨뜨리거나 정리한 이력을 다시 합칠 때 값을 되살릴 수 있습니다. [GitHub 민감정보 제거와 clone 영향](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

새 파일 업로드 전에는 secret scanning과 push protection 설정을 확인하고, 변경된 기록과 CI 로그에 실비밀이 들어가지 않게 합니다. 예제에는 동작하는 키처럼 보이는 임의 문자열을 쓰지 말고 변수명이나 명시적인 비활성 placeholder를 사용합니다. Push protection을 우회한 경우에는 이유와 승인자를 기록하고, 경보를 닫기 전에 노출된 값이 실제로 비활성화됐는지 발급자 측에서 확인합니다.

## 적용 순서와 확인 기준

1. 저장소·CI·클라우드·서비스에 있는 장기 자격 증명을 목록화하고 소유자·범위·소비자를 연결합니다.
2. 각 secret 유형이 만료·회전·폐기되는 방식을 발급자 문서에서 확인합니다.
3. 클라우드 workload는 가능하면 OIDC 연합과 최소 권한 역할을 적용하고, 정적 자격 증명이 꼭 필요한 서비스는 중앙 저장소와 짧은 유효기간을 사용합니다.
4. Push protection·secret scanning을 설정하되 해당 기능의 대상 패턴과 제외 범위를 확인합니다.
5. 새 키 적용·이전 키 폐기·서비스 복구 절차를 테스트 환경에서 연습하고 로그로 확인합니다.
6. 노출 훈련에서 탐지 시각부터 사용 차단·소비자 교체·이상 사용 확인까지의 시간을 기록합니다.

확인 기준은 “secret을 삭제했다”가 아닙니다. 발급자가 이전 자격 증명을 거부하고, 정상 소비자가 새 자격 증명으로 작동하며, 감사 로그에서 예상하지 않은 사용이 없는지 확인합니다. Git history 정리는 별도 협의가 필요한 저장소 관리 작업이며, 폐기된 비밀이 다시 유효해지지 않게 하는 통제를 대신하지 않습니다.

## 출처와 적용 범위

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html): 비밀정보 수명주기, CI/CD 권한·감사·회전, 동적 자격 증명과 저장소 운영 원칙을 확인했습니다.
- [GitHub Actions OIDC cloud providers](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers): GitHub Actions OIDC 연동에 필요한 provider 신뢰 설정, workflow 권한, 환경 보호 규칙을 확인했습니다.
- [GitHub Actions OIDC reference](https://docs.github.com/en/actions/reference/security/oidc): `iss`·`aud`·`sub` claim, branch·environment subject 조건과 2026년 immutable subject 변경을 확인했습니다.
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning): 검사 범위, 경보, 제공자 확인과 설정 가능한 탐지 유형을 확인했습니다.
- [GitHub Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection): push 차단, 활성화 조건, 지원 패턴과 우회 감사 기록을 확인했습니다.
- [GitHub Actions Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): 최소 권한, 로그 마스킹의 한계, 구조화된 값과 workflow에서 만든 민감 값을 다루는 기준을 확인했습니다.
- [Remediating a leaked secret](https://docs.github.com/en/code-security/tutorials/remediate-leaked-secrets/remediating-a-leaked-secret): 폐기·재발급·소비자 갱신·이력 정리 순서를 확인했습니다.
- [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository): 폐기 우선 원칙, history rewrite의 clone·fork·cache 영향과 협업 범위를 확인했습니다.

YAML은 GitHub Actions 권한 설정을 보여 주는 직접 작성한 발췌이며, provider 로그인 action이나 실제 클라우드 역할 정책이 포함된 배포 예제가 아닙니다. 비밀정보 사고 절차와 role 조건은 실제 provider·서비스의 공식 문서와 조직의 승인 절차에 맞춰 정해야 합니다.

## English

Secrets require an explicit lifecycle: inventory, issuance, scoped use, audit, rotation, revocation, and expiry. GitHub Actions can use OIDC federation to avoid storing long-lived cloud credentials, but only when the cloud trust policy restricts repository, ref, environment, audience, and relevant workflow claims. Secret scanning and push protection reduce exposure but do not replace provider-side revocation. The workflow YAML is an authored permissions excerpt, not a tested deployment.
