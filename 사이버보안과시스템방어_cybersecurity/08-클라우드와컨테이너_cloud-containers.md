# 클라우드와 컨테이너 | Cloud and container security

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 서버보다 먼저 자격증명과 정책을 봅니다

클라우드 사고는 운영체제 취약점뿐 아니라 공개 저장소 설정, 과도한 IAM 권한, 유출된 서비스 키, 잘못된 네트워크 연결에서도 시작합니다. IAM은 누가 어떤 자원에 어떤 작업을 수행할 수 있는지 정하는 체계입니다. 사용자, 서비스, 배포 작업의 자격증명을 분리하고 역할 인수·권한 상속·조직 간 접근을 실제 정책 평가 결과로 확인합니다.

장기 비밀키보다 수명과 대상이 제한된 workload identity를 사용할 수 있는지 검토합니다. 다만 토큰을 짧게 만들었다는 이유로 발급 신뢰나 권한 범위가 자동으로 맞아지지는 않습니다. OIDC 연동에서는 발급자·대상·작업·브랜치 같은 신뢰 조건을 좁혀야 합니다.

## 컨테이너·Kubernetes의 분리 단위

컨테이너는 보통 호스트 커널을 공유합니다. 이미지에 들어간 패키지, 실행 사용자, capability, 마운트, 호스트 socket, 네트워크를 함께 봅니다. 이미지 스캔에서 알려진 CVE가 0개여도 배포 권한이 과도하면 위험할 수 있습니다.

| 구성 | 설계 원칙 | 확인할 반례 |
| --- | --- | --- |
| 실행 사용자 | 가능한 작업은 비특권 사용자로 실행합니다. | root가 필요한 이유와 쓰기 경로를 확인합니다. |
| 파일시스템 | 읽기 전용 본문과 필요한 임시 쓰기를 분리합니다. | 비밀을 이미지 레이어에 굽지 않습니다. |
| 서비스 계정 | Pod별 필요한 API 권한만 줍니다. | 모든 Pod에 관리자 계정이나 자동 토큰이 붙지 않게 합니다. |
| 네트워크 | 필요한 통신 방향과 목적지만 열어 둡니다. | NetworkPolicy를 실제 CNI가 적용하는지 검사합니다. |
| Secret | 읽는 주체·저장 보호·교체를 관리합니다. | Base64는 암호화가 아니며 열람 권한도 별도입니다. |
| 이미지 | 출처·digest·서명·빌드 이력을 연결합니다. | 태그가 같은 새 이미지와 기존 이미지를 구분합니다. |

Kubernetes의 [Security Checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)는 이러한 설정을 연결하는 진입점입니다. 이 글은 특정 클러스터를 직접 배포·점검한 기록은 아닙니다. 운영 환경에서는 배포 manifest뿐 아니라 admission 정책·실제 적용 상태·우회 권한도 확인합니다.

## 자체 설계 사례: 문서 처리 worker

업로드를 처리하는 worker가 원문 저장소 전체와 운영 DB 관리키를 가지면 한 파일 처리기의 결함이 모든 고객으로 확대됩니다. worker에는 그 작업의 읽기 대상과 결과 저장 권한만 주고, 관리망 접근·임의 외부 전송·호스트 장치 접근을 분리합니다. 제한된 임시공간과 시간·메모리 한도를 두고 실패한 작업의 자료 수명도 정합니다.

시험에서는 다른 조직의 객체 키, 과도한 파일 크기, 만료된 토큰, 거부된 출구 연결을 넣어 봅니다. 정책이 파일에 적혀 있다는 사실보다 실제 요청이 거부되는지와 누가 예외를 줄 수 있는지를 확인합니다. [NIST Zero Trust의 자원 중심 관점](https://csrc.nist.gov/pubs/sp/800/207/final)

## 클라우드 권한은 신원·정책·자원 경로를 묶어 봅니다

클라우드 역할의 정책 문구뿐 아니라 누가 그 역할을 맡을 수 있는지, 어떤 리소스에 어떤 API를 호출할 수 있는지, 그 권한이 어느 서비스까지 이어지는지 확인합니다. 장기 access key를 코드나 CI 변수에 보관하기보다 짧은 수명의 workload identity를 검토하되, 발급자·대상·저장소·브랜치·실행 이벤트 조건을 좁힙니다. 단기 토큰도 지나치게 넓은 역할을 받으면 침해 범위가 큽니다.

컨테이너는 일반적으로 호스트 커널을 공유하므로 VM과 같은 격리 경계로 간주하면 안 됩니다. 실행 사용자, Linux capabilities, seccomp·AppArmor 정책, hostPath·socket 마운트, 네트워크 출구, 비밀 접근, 이미지 공급망을 한 묶음으로 검토합니다. Kubernetes의 네트워크 정책은 실제 CNI 구현이 이를 집행해야 효과가 있으므로 설정 파일만 확인하지 않습니다. [Kubernetes Security Checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)

## 격리 계층과 시험 결과를 연결합니다

| 통제 | 확인할 실효성 | 경계 사례 |
| --- | --- | --- |
| 비특권 실행·capabilities | 프로세스가 실제로 가진 Linux 권한입니다. | 특정 기능을 위해 추가한 capability가 다른 경로에서 쓰입니다. |
| 읽기 전용 파일시스템 | 이미지와 root filesystem의 변경 여부입니다. | 임시 경로·마운트된 hostPath는 쓰기 가능합니다. |
| 서비스 계정 | Pod가 받을 토큰과 API 권한입니다. | 필요 없는 자동 토큰이나 네임스페이스 밖 권한이 있습니다. |
| 네트워크 정책 | Pod에서 나가는 연결도 실제 차단되는지입니다. | DNS·프록시·노드 경로가 정책을 우회합니다. |
| 비밀 저장 | 접근 주체·암호화·회전·감사 경로입니다. | manifest 인코딩이나 로그에 평문이 남습니다. |
| 이미지 검증 | digest·서명·빌더·기반 이미지의 출처입니다. | 신뢰한 태그가 다른 digest를 가리킵니다. |

이 항목의 통과 조건은 정책이 선언됐다는 사실이 아니라 권한 없는 동작이 실행 환경에서 거부되고 감사 기록에 남는 것입니다. 제품별 정책 평가기와 예외 권한을 확인하고, 클러스터 변경 시험은 승인된 비운영 환경에서 먼저 수행합니다.

## 원문에서 이어 읽기

- [Kubernetes Security Checklist](https://kubernetes.io/docs/concepts/security/security-checklist/): 인증·권한·네트워크·Pod 보안·이미지 절입니다.
- [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final): 공식 초록·자원 중심 접근과 내부망 신뢰의 구분입니다.
- [GitHub Actions Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): 최소 토큰 권한·외부 입력·SHA 고정·신뢰하지 않는 코드 checkout입니다.

## English

Cloud IAM, container privileges, service accounts, network policy and artifact identity need to be evaluated together. Configuration documents alone do not prove enforcement.
