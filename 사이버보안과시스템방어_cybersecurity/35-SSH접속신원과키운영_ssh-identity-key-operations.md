# SSH 접속 신원과 키 운영 | SSH identity and key operations

자료 확인일: 2026-11-04

## 이 장에서 다루는 범위

SSH는 원격 로그인과 파일 전송에 쓰이는 암호화 프로토콜입니다. 하지만 연결이 암호화되었다는 사실만으로 접속한 서버가 의도한 서버인지, 로그인한 사용자가 허가된 사람인지가 자동으로 보장되지는 않습니다. SSH 연결에는 서버 호스트 인증, 사용자 인증, 연결 채널의 권한 제한이라는 서로 다른 확인 단계가 있습니다.

이 장에서는 OpenSSH 클라이언트와 서버를 운영할 때 서버 신원 확인, 공개키·인증서 수명 주기, `ssh-agent` 사용, 점프 호스트, 서버 설정 검토를 어떻게 연결할지 설명합니다. 예시는 OpenBSD-current의 OpenSSH 설명서를 기준으로 작성했습니다. 배포판·제품·버전에 따라 기본값과 지원 설정이 다를 수 있으므로 적용 전 해당 시스템의 매뉴얼과 실제 유효 설정을 확인해야 합니다.

## 한 연결에서 서로 다른 신원 확인

SSH는 크게 전송 계층, 사용자 인증 계층, 연결 계층으로 동작합니다. 전송 계층은 서버 호스트를 인증하고 암호화·무결성을 제공합니다. 사용자 인증 계층은 클라이언트 사용자가 서버에 로그인할 수 있는지 확인합니다. 연결 계층은 인증이 끝난 뒤 셸, 명령 실행, 포트 전달 같은 채널을 엽니다.

| 확인 대상 | 확인하는 쪽 | 주로 쓰는 정보 | 확인하는 질문 |
| --- | --- | --- | --- |
| 서버 호스트 | SSH 클라이언트 | 서버 호스트 공개키 또는 신뢰된 호스트 인증서 | 지금 연결한 서버가 기대한 서버입니까? |
| 사용자 계정 | SSH 서버 | 공개키 서명, SSH 사용자 인증서, 조직이 허용한 추가 인증 | 이 사용자가 이 계정에 로그인할 수 있습니까? |
| 연결 기능 | SSH 서버와 계정 정책 | 포트 전달·PTY·명령·그룹 정책 | 인증된 사용자가 어떤 작업과 채널을 사용할 수 있습니까? |

서버의 호스트 키와 사용자의 로그인 키는 역할이 다릅니다. 사용자의 공개키를 `authorized_keys`에 등록했다고 서버 신원이 확인되는 것은 아니며, 서버의 호스트 키를 `known_hosts`에 등록했다고 사용자가 로그인할 권한이 생기는 것도 아닙니다. 이 구분은 RFC 4251이 SSH의 전송·사용자 인증·연결 프로토콜을 별도 구성요소로 설명하는 방식과 같습니다.

## `known_hosts`와 서버 신원 확인

클라이언트는 서버가 제시한 호스트 키를 이전에 신뢰한 키와 비교합니다. 사용자별 기본 저장소는 보통 `~/.ssh/known_hosts`입니다. 처음 연결할 때 제시되는 지문을 확인하지 않고 받아들이면 공격자가 중간에서 가짜 서버를 제시하는 상황을 구별하기 어렵습니다.

처음 등록할 때는 서버 관리자가 별도 신뢰 경로로 제공한 지문, 자산 관리 자료 또는 검증된 호스트 인증서 체계와 대조합니다. 연결 대상과 같은 SSH 세션이나 신뢰 여부를 확인하려는 같은 네트워크만을 확인 경로로 삼으면 독립 검증이 되지 않을 수 있습니다. `StrictHostKeyChecking yes`는 알 수 없는 키를 자동으로 추가하지 않고, 이미 저장된 키가 바뀐 경우 접속을 거부하도록 합니다.

호스트 키 변경 경고가 나타나면 `known_hosts` 항목을 곧바로 지우거나 검사를 끄지 않습니다. 가상 머신 재생성, 서버 교체, 의도된 키 교체일 수도 있지만 DNS 조작, 잘못된 접속 대상, 중간자 공격 가능성도 있습니다. 담당자가 변경 티켓과 자산 식별자를 확인하고 새 지문을 별도 경로에서 검증한 뒤, 승인된 키만 교체해야 합니다.

### 호스트 키 교체 확인 순서

1. 경고가 난 호스트 이름·주소·접속 시각과 터미널 오류를 기록합니다.
2. 기존 세션과 자동 배포를 보류하고, 접속한 이름이 인벤토리의 대상과 일치하는지 확인합니다.
3. 서버 재설치·교체·키 회전 작업이 승인되어 있었는지 변경 기록과 담당자에게 확인합니다.
4. 새 호스트 키 지문을 관리 콘솔·서버 측 신뢰 경로 등 기존 SSH 연결과 분리된 경로로 확인합니다.
5. 지문·호스트 이름·키 종류가 일치하고 변경이 승인된 경우에만 알려진 호스트 정보를 갱신합니다.
6. 설명되지 않는 변경이면 접속을 중단하고 네트워크·DNS·서버 접근 기록을 보존해 조사합니다.

`ssh-keygen -F host.example.net`은 저장된 호스트 항목을 찾는 데 사용하고, `ssh-keygen -lf key.pub`는 공개키 파일의 지문을 표시하는 데 사용합니다. 이 명령들은 비교 자료를 보여 줄 뿐, 지문이 올바른 대상에서 왔다는 사실을 스스로 증명하지는 않습니다.

## 사용자 키와 계정 권한

공개키 인증에서는 서버가 승인된 공개키로 서명을 검증하고, 클라이언트가 대응하는 개인키를 보유했음을 확인합니다. 개인키 파일을 서버에 복사할 필요는 없습니다. 개인키를 복사·메신저·저장소에 올리지 말고, 목적이나 관리 주체가 다른 환경에는 별도 키를 발급해 노출 범위를 줄입니다.

키의 주석(comment)은 운영자가 식별을 돕도록 붙이는 문구입니다. 주석의 이메일이나 이름은 인증 근거가 아니며, 권한은 서버 계정과 해당 공개키가 등록된 위치, 키 옵션과 서버 정책에서 결정합니다. 직원 퇴사나 단말 분실 때는 누가 어떤 키를 어느 서버·계정에 등록했는지 찾아 제거할 수 있어야 합니다.

실무에서 관리할 항목은 다음과 같습니다.

- 키 소유자·목적·등록 계정·대상 시스템·발급 시각을 자산 목록에 기록합니다.
- 가능하면 키에 암호문구(passphrase)를 설정하고, 단말 보안과 백업 정책을 함께 적용합니다.
- 개인용·배포용·자동화용 키를 구분하고 자동화 키에는 필요한 호스트와 명령만 허용합니다.
- 권한 변경이나 단말 폐기 시 계정 접근 목록, 중앙 키 저장소, 인증서 발급 시스템을 함께 회수합니다.
- 키 폐기 뒤에는 대체 키를 발급하고 접속 시험과 감사 기록을 확인합니다.

`ssh-agent`는 개인키를 에이전트 프로세스에 등록해 매 접속마다 개인키 암호문구를 입력하지 않도록 돕습니다. 키 파일 자체를 다른 서버로 전송하는 기능은 아닙니다. 에이전트는 등록 키의 사용 권한을 유지하는 민감한 구성요소이므로, 필요한 키만 제한된 시간 동안 적재하고 공유 단말에서는 세션 종료 후 제거합니다. OpenSSH의 `ssh-add -t`로 키의 유효 시간을 제한할 수 있으며, `ssh-add -l`로 에이전트에 등록된 지문을 확인할 수 있습니다.

## 에이전트 전달과 점프 호스트

`ForwardAgent yes`를 설정하면 원격 호스트에서 로컬 인증 에이전트 소켓을 사용할 수 있게 연결을 전달합니다. 원격 호스트의 사용자가 그 소켓에 접근하면 등록된 키로 인증 서명 작업을 요청할 수 있습니다. 개인키 원문을 에이전트에서 추출할 수 있다는 뜻은 아니지만, 원격 호스트가 침해된 동안에는 해당 키의 신원으로 인증 작업이 이뤄질 수 있어 위험합니다. OpenSSH는 에이전트 전달을 기본적으로 끄고 신중히 사용하도록 안내합니다.

서버에 접속하기 위해 중간 호스트를 거쳐야 한다면 `ProxyJump`를 사용할 수 있습니다. 클라이언트가 점프 호스트에 SSH 연결을 만들고, 그 호스트를 통해 최종 대상까지 TCP 전달을 구성합니다. 이는 에이전트 소켓 전달과 다른 기능입니다. 점프 호스트를 쓴다고 최종 서버의 호스트 키 검증이 생략되는 것은 아니며 클라이언트는 최종 대상의 신원도 확인해야 합니다.

```sshconfig
Host bastion                         # 점프 호스트용 별칭입니다.
    HostName bastion.example.net     # 별칭이 연결될 실제 DNS 이름입니다.
    User ops                         # 점프 호스트에서 사용할 계정입니다.
    IdentityFile ~/.ssh/id_ed25519_bastion  # 점프 호스트 전용 키를 지정합니다.
    IdentitiesOnly yes               # 지정한 인증 키를 우선 사용합니다.
    StrictHostKeyChecking yes        # 검증되지 않은 키와 바뀐 키를 자동 수용하지 않습니다.
    ForwardAgent no                  # 로컬 agent socket을 점프 호스트에 전달하지 않습니다.

Host prod-app-01                     # 운영 애플리케이션 서버 별칭입니다.
    HostName app-01.internal.example.net  # 내부망의 최종 서버 이름입니다.
    User deploy                      # 최종 서버의 로그인 계정입니다.
    IdentityFile ~/.ssh/id_ed25519_prod  # 운영 서버용 키를 지정합니다.
    IdentitiesOnly yes               # 다른 에이전트 키를 무심코 제시하지 않습니다.
    ProxyJump bastion                # bastion을 통해 최종 서버에 연결합니다.
    StrictHostKeyChecking yes        # 최종 서버 호스트 키도 검증합니다.
    ForwardAgent no                  # 최종 서버에 agent socket을 전달하지 않습니다.
```

위 설정은 OpenSSH 클라이언트용 예시입니다. `HostName`, 계정, 키 경로, 점프 호스트는 조직의 실제 인벤토리에 맞춰야 합니다. `IdentitiesOnly yes`는 지정한 `IdentityFile` 등 명시된 인증 파일만 사용하도록 제한하는 데 도움을 줍니다. 환경에 따라 인증서와 다른 인증 방식이 함께 구성될 수 있으므로 `ssh -G prod-app-01`로 최종 적용 설정을 확인합니다. 실제 서버에 접속하거나 이 설정을 적용한 결과는 이 자료에서 시험하지 않았습니다.

## 여러 서버의 키를 관리하는 OpenSSH 인증서

서버가 많아질수록 사용자 공개키를 각 서버의 `authorized_keys`에 직접 복사하고 회수하는 방식은 누락이 생기기 쉽습니다. OpenSSH 인증서는 사용자 또는 호스트 공개키에 CA 서명을 붙여 신원 정보, principal, 유효 기간, 옵션을 검증할 수 있게 합니다. 서버는 여러 사용자 키를 직접 배포하는 대신 사용자 CA 공개키를 신뢰할 수 있고, 클라이언트도 호스트 CA를 신뢰해 관리 대상 호스트 인증서를 확인할 수 있습니다.

OpenSSH 인증서는 X.509 인증서와 다른 간결한 형식입니다. 사용자 인증서의 principal은 허용 사용자 이름 등이며, 호스트 인증서의 principal은 호스트 이름입니다. 서버는 `TrustedUserCAKeys`와 `AuthorizedPrincipalsFile` 등을 통해 신뢰할 CA와 허용 principal을 설정할 수 있습니다. CA 개인키는 일반 접속용 개인키와 분리하고 발급·승인 권한을 제한합니다.

인증서 만료 시간만 짧게 두어도 모든 회수가 자동으로 끝나는 것은 아닙니다. 발급된 인증서나 키가 만료 전에 폐기되어야 한다면 KRL(Key Revocation List)을 만들고 모든 관련 서버에 일관되게 배포해야 합니다. `RevokedKeys` 파일이 읽히지 않는 경우 OpenBSD `sshd_config` 설명서는 공개키 인증을 모든 사용자에 대해 거부한다고 명시합니다. 따라서 KRL 배포 실패 감시와 원자적 파일 교체, 복구 절차를 준비합니다. 인증서 발급 CA, KRL 게시 경로, 서버의 적용 시각을 함께 관리합니다.

## 서버 설정을 적용하기 전 확인할 점

서버 설정 예시는 접근 경로를 줄이는 출발점이지 모든 환경의 정답은 아닙니다. 특히 비밀번호 인증을 끄기 전에 대체 인증, 비상 관리자 접근, 콘솔 복구 경로가 동작하는지 확인해야 합니다. 포트 전달이나 SFTP를 실제로 사용하는 업무가 있다면 전역으로 막기보다 사용자·그룹별로 필요한 기능만 남기는 정책을 설계합니다.

```text
PubkeyAuthentication yes             # 사용자 공개키 인증을 허용합니다.
PasswordAuthentication no            # SSH password 방식은 허용하지 않습니다.
KbdInteractiveAuthentication no       # keyboard-interactive 방식은 별도 승인 전까지 허용하지 않습니다.
PermitRootLogin no                    # root 계정의 직접 SSH 로그인을 막습니다.
AllowGroups ssh-operators              # 지정한 운영 그룹의 계정만 로그인시킵니다.
AllowTcpForwarding no                 # TCP 터널 전달을 막되 업무 영향과 셸 권한을 함께 검토합니다.
X11Forwarding no                      # 필요하지 않은 X11 전달을 막습니다.
PermitTunnel no                       # SSH tun 장치 생성을 허용하지 않습니다.
RevokedKeys /etc/ssh/revoked_keys     # 폐기된 공개키와 인증서를 거부하도록 목록을 읽습니다.
```

위 예시는 권한 있는 운영 계정에 대한 축약 설정입니다. 비밀번호와 keyboard-interactive를 함께 끄는 경우 PAM·MFA·비상 접근 구성에 어떤 영향을 주는지 배포판의 OpenSSH 문서로 확인해야 합니다. `AllowTcpForwarding no`는 SSH 터널을 사용하는 애플리케이션이나 관리 흐름도 차단할 수 있으므로 실제 필요성을 확인한 뒤 적용합니다. 서버 설정 문법과 `Match` 조건은 OpenSSH 버전 및 배포판 정책에 따라 달라질 수 있습니다.

또한 셸 접근을 허용한 사용자는 자체 포워더를 실행할 수 있으므로 `AllowTcpForwarding no`만으로 네트워크 터널링을 완전히 막는 통제가 되지는 않습니다. 포트 전달 제한은 셸·명령·단말 접근의 제한과 함께 설계해야 하며, 제한 계정에는 허용할 명령과 채널을 별도로 구성합니다.

안전한 변경 순서는 현재 접근 경로를 유지한 상태에서 새 설정을 검토하고, 설정 검증 도구를 통과시킨 뒤 별도 세션에서 새 인증 경로를 시험하는 것입니다. 다음 명령은 예시이며 여기서 실제 서버에는 실행하지 않았습니다.

```sh
sudo sshd -t  # 서버 설정 파일과 키 파일의 기본 유효성을 확인합니다.
sudo sshd -T -C user=deploy,host=app-01.internal.example.net,addr=192.0.2.20  # 조건별 유효 설정을 출력합니다.
```

`sshd -t`는 구성 파일과 키 파일의 유효성을 검사하고, `sshd -T`는 적용될 설정을 출력합니다. `-C`는 연결 조건을 지정해 `Match` 규칙을 포함한 유효 설정을 확인하는 데 씁니다. 실제 배포에서는 사용 중인 포트·설정 파일 경로·서비스 관리 방식도 환경에 맞춰야 합니다. 새 세션에서 로그인, 필요한 명령, 전달 기능, 로그 기록을 확인하기 전 기존 관리자 세션을 닫지 않습니다.

## 운영 사고를 줄이는 점검 흐름

### 신규 서버를 등록할 때

1. 자산 인벤토리에서 호스트 이름, 환경, 소유 팀, 접속 경로와 관리자를 확인합니다.
2. 호스트 키 또는 호스트 인증서를 독립된 신뢰 경로에서 검증합니다.
3. 사용자·자동화 계정의 공개키, 인증서 principal, 만료·회수 정책을 등록합니다.
4. 점프 호스트 경유가 필요한 경우 최종 대상까지의 접속과 두 호스트의 신원을 각각 확인합니다.
5. 권한·세션·포워딩 설정을 검토하고 접속 로그에서 예상 계정과 원격 주소가 보이는지 확인합니다.

### 키 유출이나 사용자 변경이 생겼을 때

1. 영향을 받은 개인키·계정·호스트·인증서 발급 시점을 확인하고 추가 발급을 일시 제한합니다.
2. 관련 공개키를 각 서버와 중앙 관리 시스템에서 제거하거나 KRL로 폐기하고, 폐기 자료가 적용됐는지 확인합니다.
3. 키 사용 기록과 인증 로그를 보존하고, 해당 자격 증명으로 접근 가능한 시스템을 조사합니다.
4. 깨끗한 단말과 승인된 절차로 대체 키를 발급하고 최소 권한으로 재등록합니다.
5. 실제 접속 시험과 감사 로그를 확인한 뒤 임시 통제를 해제하고 사고 기록을 갱신합니다.

키를 폐기했다는 관리 기록만으로 실제 모든 서버에서 사용이 차단되었다고 단정하지 않습니다. 정적 `authorized_keys`, 설정 관리 시스템, 인증 CA, 인증서 폐기 목록, 오프라인 장비처럼 회수 지점이 서로 다를 수 있으므로 적용 범위를 대조해야 합니다.

## 진단 명령과 해석 범위

| 명령 | 확인하는 정보 | 이 명령만으로 알 수 없는 것 |
| --- | --- | --- |
| `ssh -G alias` | 별칭에 적용된 클라이언트 설정 | 서버에 설정이 반영되었는지 또는 인증이 성공하는지 |
| `ssh-keygen -F host` | `known_hosts`에서 호스트 항목 검색 | 저장된 키가 현재 접속 대상의 정당한 키인지 |
| `ssh-keygen -lf key.pub` | 공개키의 지문과 키 형식 | 파일의 소유자 신원이나 지문 배포 경로의 신뢰성 |
| `ssh-add -l` | 에이전트에 적재된 키 지문 목록 | 각 키가 실제로 필요한 권한만 갖는지 |
| `sshd -t` | 서버 설정의 기본 구문·키 파일 검사 | 업무 접근 경로가 안전하고 정상 동작하는지 |
| `sshd -T -C ...` | 조건에 따라 계산된 유효 서버 설정 | 네트워크 정책·계정 디렉터리·운영 절차 전체의 안전성 |

`ssh-keygen -R host`는 특정 호스트의 저장 항목을 제거하는 도구입니다. 호스트 키 변경 경고를 숨기는 목적으로 먼저 실행하면 안 됩니다. 새로운 지문을 독립 확인하고 승인된 회전을 확인한 이후에만 관리 절차에 따라 기존 항목을 갱신합니다.

## 검토할 운영 질문

- 서버 호스트 키와 사용자 인증 키의 소유자·보관 위치·교체 담당자가 각각 정해져 있습니까?
- 최초 접속 지문과 키 변경을 SSH 세션 외의 신뢰 경로로 확인할 수 있습니까?
- 사람·자동화·비상 접근 계정이 같은 개인키나 동일한 관리자 계정을 공유하지 않습니까?
- 에이전트에 적재된 키 수와 수명을 제한하고 원격 호스트로의 전달을 기본 차단합니까?
- 점프 호스트를 통해서도 최종 서버의 호스트 키를 확인하고 접근 경로를 기록합니까?
- 인증서 principal, 만료, KRL 배포 실패, CA 개인키 보호를 포함한 회수 절차가 있습니까?
- 설정 변경 뒤 새 로그인과 기존 업무 터널을 확인할 수 있는 별도 세션과 복구 경로가 있습니까?

## English summary

SSH uses separate mechanisms for server host authentication, user authentication, and post-authentication channels. A secure encrypted transport does not remove the need to verify the server host key. Treat host-key changes as an investigation event, keep private keys on the client, limit agent lifetime and forwarding, and use `ProxyJump` without confusing it with agent forwarding. OpenSSH certificates can centralize trust through principals, validity intervals, and revocation lists, but their CA and KRL distribution must be operated reliably. Validate effective client and server configuration before deployment and keep a tested recovery path.

## 출처

- [RFC 4251, The Secure Shell (SSH) Protocol Architecture](https://www.rfc-editor.org/rfc/rfc4251.html), §4: SSH 전송·사용자 인증·연결 프로토콜의 역할 구분입니다.
- [RFC 4252, The Secure Shell (SSH) Authentication Protocol](https://www.rfc-editor.org/rfc/rfc4252.html), §5·§7: 공개키 사용자 인증 교환과 서명 검증 흐름입니다.
- [RFC 4253, The Secure Shell (SSH) Transport Layer Protocol](https://www.rfc-editor.org/rfc/rfc4253.html), §4·§8: 서버 호스트 인증, 키 교환, 암호화와 무결성입니다.
- [OpenBSD `ssh(1)`](https://man.openbsd.org/ssh), VERIFYING HOST KEYS·SSH-BASED VIRTUAL PRIVATE NETWORKS: 호스트 키 검증과 SSH 연결 사용 설명입니다.
- [OpenBSD `ssh_config(5)`](https://man.openbsd.org/ssh_config), `StrictHostKeyChecking`·`ForwardAgent`·`ProxyJump`·`IdentityFile`·`IdentitiesOnly`·`UpdateHostKeys`: 클라이언트 접속 설정입니다.
- [OpenBSD `sshd_config(5)`](https://man.openbsd.org/sshd_config), `PermitRootLogin`·`PasswordAuthentication`·`KbdInteractiveAuthentication`·`AllowGroups`·`TrustedUserCAKeys`·`AuthorizedPrincipalsFile`·`RevokedKeys`: 서버 인증·계정·폐기 설정입니다.
- [OpenBSD `sshd(8)`](https://man.openbsd.org/sshd), `-t`·`-T`·`-C`: 설정 구문 검사와 조건별 유효 설정 출력입니다.
- [OpenBSD `ssh-keygen(1)`](https://man.openbsd.org/ssh-keygen), CERTIFICATES·KEY REVOCATION LISTS·`-F`·`-R`·`-l`: 키 지문·호스트 항목·OpenSSH 인증서·KRL 관리입니다.
- [OpenBSD `ssh-agent(1)`](https://man.openbsd.org/ssh-agent), DESCRIPTION·`-t`: 에이전트의 역할과 등록 키 수명 설정입니다.
- [OpenBSD `ssh-add(1)`](https://man.openbsd.org/ssh-add), DESCRIPTION·`-t`·`-l`: 에이전트 키 추가·시간 제한·지문 확인입니다.

OpenBSD-current 매뉴얼을 2026-11-04 확인했습니다. 다른 운영체제의 OpenSSH 패키지는 판본·기본값·추가 설정이 다를 수 있습니다. 설정 블록과 명령은 설명용 예시로, 실제 운영 서버에 적용하거나 접속 시험한 결과가 아닙니다.
