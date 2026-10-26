# Linux 설치와 EDA 라이선스 설정

반도체 설계 환경은 운영체제, 설계 도구, 라이선스, 공정 자료를 함께 맞춰야 동작합니다. 실행 파일이 설치되어 있어도 사용할 권한이나 맞는 PDK가 없으면 설계를 진행할 수 없습니다. 이 글은 상용 도구를 사용하는 연구실·회사 환경의 준비 순서와 Linux에서 문제를 구분하는 방법을 설명합니다. 공개 도구 설치 실습은 [LibreLane으로 RTL에서 GDS까지](12-공개도구로RTL에서GDS까지_open-rtl-to-gds.md)에서 이어집니다.

기준일은 2026년 10월 26일입니다. 아래 명령은 문서 설명용이며, 이 글을 작성하면서 Linux에 상용 EDA나 라이선스 서버를 설치하거나 명령을 실행하지 않았습니다.

## 1. 설치 전에 정할 항목

| 항목 | 확인할 내용 | 필요한 이유 |
|---|---|---|
| 제품과 판본 | 제품명, 주 판본, 서비스 팩·핫픽스 | 같은 공급사 제품도 설치 조건이 다를 수 있습니다. |
| 실행 호스트 | CPU 아키텍처, 배포판과 세부 버전, 메모리·저장 공간 | x86-64 실행 파일과 Arm 실행 파일을 구분해야 합니다. |
| 사용 방식 | 연구실 서버 접속, 로컬 워크스테이션, 승인된 클라우드 | GUI 표시, 파일 위치, 라이선스 접근 경로가 달라집니다. |
| 설치 권한 | 설치 담당자, 사용자 계정, 공유 그룹 | 도구 설치 영역과 개인 설계 영역의 권한을 나눕니다. |
| 라이선스 | 계약된 제품·기능, 서버 주소, 접속망, 사용 가능 수량 | 설치 프로그램과 사용권은 별개입니다. |
| PDK·라이브러리 | 공정과 옵션, PDK 판본, 도구별 지원 뷰 | 임의의 공정 자료를 연결해서는 해석 결과를 신뢰할 수 없습니다. |

지원 OS는 설치할 제품의 해당 판본 릴리스 노트와 플랫폼 표에서 확인합니다. 예를 들어 Synopsys의 [SCL Supported OS](https://www.synopsys.com/support/licensing-installation-computeplatforms/licensing/scl-supported-os.html)는 라이선스 서버인 SCL의 지원표입니다. 이 표를 모든 Synopsys 설계 도구의 지원표로 사용하면 안 됩니다. 오래된 공개 플랫폼 PDF의 `Current Releases`라는 제목만 보고 현재 도구의 지원 여부를 확정해서도 안 됩니다.

공개 실습에 쓰는 LibreLane의 Linux 안내는 Ubuntu 22.04 이상을 주 지원 대상으로 설명합니다. 이는 [그 공개 도구의 안내](https://librelane.readthedocs.io/en/stable/installation/nix_installation/installation_linux.html)이며, Virtuoso·Spectre·Calibre 등의 지원 OS를 보증하는 근거가 아닙니다. WSL이나 컨테이너에서 실행된다는 사실과 공급사의 공식 지원도 구분합니다.

## 2. Linux를 준비하는 순서

이미 기관 서버가 있다면 계정과 접속 방법, 작업 디렉터리, 환경 설정 파일을 먼저 받습니다. 개인 PC에 설치한다면 선정한 도구가 요구하는 배포판의 공식 설치 절차를 따르고, 가상머신을 쓸 때는 호스트와 게스트의 CPU 아키텍처 및 자원 배분을 확인합니다. 상용 도구의 GUI, 라이선스용 host ID, 장치 접근은 가상화 방식에 따라 추가 조건이 있을 수 있으므로 해당 제품 문서를 확인합니다.

### 2.1 처음 설치하는 예: Ubuntu 24.04 LTS 가상머신

다음은 x86-64 Windows PC에서 공개 도구를 학습하기 위한 예시입니다. Windows 안에 새 가상머신과 가상 디스크 파일을 만들고 그 안에 Ubuntu를 설치합니다. 호스트 PC를 USB로 부팅하거나 Windows 디스크의 파티션을 바꾸는 절차가 아닙니다. 이 문서 작성 과정에서는 실제 가상머신 생성이나 디스크 작업을 수행하지 않았습니다.

1. Ubuntu의 [24.04 설치 안내](https://ubuntu.com/desktop/docs/en/24.04/tutorial/install-ubuntu-desktop/)에서 해당 LTS의 Desktop ISO를 확인하고 내려받습니다. `amd64`는 이 예시의 x86-64 아키텍처를 뜻합니다.
2. [Ubuntu의 VirtualBox 안내](https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox)에 연결된 공식 배포 경로로 호스트 OS용 VirtualBox를 설치합니다. 이 안내의 화면은 Ubuntu 22.10 예시입니다. 여기서는 가상머신을 만드는 원리를 Ubuntu 24.04 LTS에 적용하고, 자동 설치 대신 수동 설치를 선택합니다.
3. VirtualBox에서 `New`를 선택하고 이름·보관 폴더·ISO를 지정합니다. 무인 설치를 건너뛰는 옵션을 선택하여 Ubuntu 설치 화면에서 직접 계정을 정하도록 합니다. 메뉴 이름은 VirtualBox 판본에 따라 달라질 수 있습니다.
4. CPU·메모리와 가상 디스크 크기를 정합니다. 호스트가 계속 사용할 자원을 남기고, Ubuntu 자체뿐 아니라 [LibreLane의 자원 안내](https://librelane.readthedocs.io/en/stable/installation/nix_installation/installation_linux.html)와 도구·PDK·실행 결과 저장 공간을 함께 고려합니다.
5. 새 가상 하드디스크 파일을 생성합니다. 기존 물리 디스크를 직접 연결하는 설정은 사용하지 않습니다. 생성 요약에서 ISO와 새 가상 디스크가 이 가상머신에 연결되어 있는지 확인합니다.
6. 가상머신을 시작하고 설치 화면에서 언어·키보드·네트워크를 정합니다. 설치 대상을 선택할 때는 새 가상 디스크인지 확인합니다. 이 구성에서 설치기의 디스크 지우기 선택은 연결한 가상 디스크에 적용되므로, 호스트 물리 디스크 설치 절차와 혼동하지 않습니다.
7. 시간대·계정·암호를 정하고 설치를 마칩니다. 재시작 때 설치 매체 제거 안내가 나오면 가상 광학 드라이브의 ISO를 분리하고, 설치된 가상 디스크로 부팅합니다.
8. Ubuntu에 로그인하여 네트워크와 터미널을 확인하고 시스템 업데이트를 적용합니다. 필요한 화면 크기 조절 등은 해당 VirtualBox 판본의 Guest Additions 안내를 따릅니다. 기본 환경이 준비되면 가상머신을 종료한 상태의 스냅샷·백업을 남기고 공개 도구 설치로 진행합니다.

실제 PC에 Ubuntu를 직접 설치하는 선택지는 디스크 변경을 포함하므로 위 가상머신 예시와 다릅니다. 직접 설치를 선택했다면 Ubuntu 공식 안내의 백업·설치 대상·디스크 설정 절차를 별도로 따라야 합니다. 또한 이 Ubuntu 예시는 상용 도구의 지원 OS를 정한 것이 아닙니다.

### 2.2 상용 사용권에서 첫 제품 실행까지

| 순서 | 수행할 일 | 확인 기준 |
|---|---|---|
| 1. 사용 경로 선택 | 기관의 기존 계약·교육용 제공 여부를 CAD 담당자에게 확인하거나 공급사 공식 문의 창구에서 사용 목적을 전달합니다. | 회사·학교 계정이 있다는 사실과 도구 사용권 보유는 구분합니다. |
| 2. 계정과 권한 연결 | 계약 또는 기관의 승인 범위에 맞춰 고객 지원 계정과 다운로드 권한을 연결합니다. | 필요한 제품·판본이 계정에서 보이는지 확인합니다. |
| 3. 라이선스 준비 | 기존 서버의 주소를 받거나, 지정된 관리자가 실제 서버의 host ID 등을 제출하여 사용권을 발급받습니다. | 받은 파일·서버 주소가 계약과 실제 서버에 맞아야 합니다. |
| 4. 설치 매체 확보 | 해당 판본의 설치기·제품 패키지·릴리스 노트와 플랫폼 조건을 받습니다. | 인터넷의 임의 재배포본을 제품 설치 경로로 사용하지 않습니다. |
| 5. 도구 설치 | 담당자가 쓰기 가능한 설치 영역에 공식 설치 절차를 적용하고 필요한 패치·설치 검사를 수행합니다. | 설치 경로와 정확한 판본을 기록합니다. |
| 6. PDK·셸 환경 연결 | 승인된 PDK와 라이브러리, 도구별 설정 파일을 받고 해당 셸에서 적용합니다. | 실행 파일·모델·공정 뷰·라이선스 경로를 각각 확인합니다. |
| 7. 첫 실행 | 제품 설치 안내의 실행 방법으로 도구를 열고 기관이 제공한 작은 확인용 설계나 시험을 실행합니다. | 시작 성공, 라이선스 체크아웃, 모델 읽기와 해석 성공을 나누어 확인합니다. |

Cadence의 [Software Downloads](https://www.cadence.com/en_US/home/support/software-downloads.html)는 계약·고객 계정에 따른 다운로드 접근과 InstallScape를 통한 다운로드·설치를 설명합니다. Virtuoso·Spectre에서는 계정에서 허용된 해당 제품 패키지와 설치 문서를 선택합니다. 같은 다운로드 페이지에 있는 BETA CAE용 `BETA_LM` 절차를 Spectre 설치 절차로 사용하지 않습니다.

Synopsys의 [Licensing, Installation & Supported Platforms](https://www.synopsys.com/support/licensing-installation-computeplatforms.html)는 SolvNetPlus 계정, 다운로드, 제품 설치와 플랫폼 문서를 연결합니다. [SCL QuickStart](https://www.synopsys.com/support/licensing-installation-computeplatforms/licensing.html)는 라이선스 서버 패키지 SCL, Linux용 Synopsys Installer와 SmartKeys의 key file 준비를 구분합니다. 기존 기관 서버를 사용하는 일반 사용자는 별도 서버를 새로 만드는 대신 배정받은 주소를 설정합니다. Siemens EDA도 사용 제품의 공식 고객 지원·설치·라이선스 안내를 따라 계약된 배포물을 받습니다.

첫 실행이 회로 설계 환경인 Virtuoso라면 프로젝트 라이브러리와 해당 PDK의 기술 연결을 확인하고, 시뮬레이션 단계에서 Spectre가 필요한 모델과 조건을 읽는지도 확인합니다. 임의의 전역 환경 변수나 feature 이름을 새로 만들지 않고, 기관 설정과 해당 판본의 설치 안내를 기준으로 진행합니다.

### 2.3 설치한 환경을 읽어 보는 명령

처음에는 실행 환경과 파일 권한을 읽어 보는 것만으로도 문제를 상당 부분 구분할 수 있습니다. 다음은 Bash에서 쓰는 일반적인 진단 예시입니다.

```bash
cat /etc/os-release # 배포판 이름과 판본을 확인합니다.
uname -m # 실행 호스트의 CPU 아키텍처를 확인합니다.
id # 현재 계정과 소속 그룹을 확인합니다.
printf '%s\n' "$SHELL" # 계정에 등록된 기본 셸 경로를 표시합니다.
df -h . # 현재 작업 위치가 속한 파일시스템의 남은 공간을 확인합니다.
ls -ld . # 현재 작업 디렉터리의 소유자와 접근 권한을 확인합니다.
command -v virtuoso # PATH에서 Virtuoso 실행 파일을 찾는지 확인합니다.
command -v spectre # PATH에서 Spectre 실행 파일을 찾는지 확인합니다.
```

`command -v`는 실행 파일 검색 결과를 보여 줄 뿐, 라이선스 체크아웃이나 시뮬레이션 성공을 확인하지 않습니다. `$SHELL`도 현재 대화형 셸과 반드시 같지는 않습니다. 원격 로그인·작업 스케줄러·컨테이너가 실제로 어떤 셸과 시작 파일을 사용하는지도 확인해야 합니다.

설치된 공용 도구와 PDK는 일반 사용자가 내용을 바꾸지 않도록 관리하고, 로그·파형·배치 결과는 쓰기 권한이 있는 프로젝트 디렉터리에 저장하는 구성이 편리합니다. 디렉터리의 `x` 권한은 경로를 통과하는 권한입니다. 최종 파일이 읽기 가능해도 상위 디렉터리를 통과할 수 없으면 열 수 없습니다. `Permission denied`를 만났을 때 전체 설치 트리에 재귀적으로 `chmod 777`을 적용하지 말고, 실패한 경로와 필요한 읽기·쓰기·실행 권한을 구분합니다.

## 3. Bash와 C shell 환경 설정

셸은 터미널에서 입력한 명령을 해석하는 프로그램입니다. Bash의 `export 변수=값`과 csh/tcsh의 `setenv 변수 값`은 문법이 다릅니다. 기관에서 제공한 `.sh` 또는 `.csh` 설정 파일을 해당 셸에서 읽어야 합니다. 파일 이름만 같게 바꾸어도 문법은 변하지 않습니다.

다음 `27020@aspen`은 Synopsys 공식 문서에 나온 예시 주소입니다. 실제 사용 시에는 관리자가 배정한 포트와 서버명으로 바꿉니다. 서버를 선택하는 설정이지, 새로운 사용권을 만드는 설정이 아닙니다.

```bash
export SNPSLMD_LICENSE_FILE='27020@aspen' # Bash에서 공식 예시의 SCL 서버 주소를 설정합니다.
```

```csh
setenv SNPSLMD_LICENSE_FILE 27020@aspen # csh/tcsh에서 같은 공식 예시 주소를 설정합니다.
```

환경 설정 파일은 현재 셸에서 `source`해야 그 셸의 환경에 반영됩니다. 별도 셸에서 스크립트를 실행하면 자식 프로세스에서 바뀐 환경이 부모 셸로 돌아오지 않습니다. Bash 계열의 대화형·로그인 셸과 배치 작업은 시작 파일을 읽는 조건도 다르므로, 배치 작업에서만 실패한다면 환경을 불러오는 위치부터 확인합니다. 제품별 설정 파일에는 실행 파일 경로뿐 아니라 도구가 요구하는 추가 설정이 있을 수 있습니다.

## 4. FlexNet과 제품별 라이선스 변수

FlexNet 계열 라이선스 서버는 여러 공급사에서 사용하지만 서버 프로그램, vendor daemon, 환경 변수와 계약된 기능은 제품마다 다릅니다. `PATH`는 실행 파일을 찾는 경로이고, 라이선스 변수는 사용권을 찾는 경로입니다. PDK 경로는 또 다른 설정입니다.

| 대상 | 공식 문서에서 확인한 설정 | 적용 범위 |
|---|---|---|
| Cadence | `CDS_LIC_FILE`, 경우에 따라 `LM_LICENSE_FILE` | [Cadence 계정 등록 도움말의 Finding your Host ID](https://registration.cadence.com/resource/COSHelpPages/Help/help_register_en_US.html)는 파일 경로와 `port@host` 형식을 설명합니다. 실제 우선순위와 제품별 조건은 설치 문서를 확인합니다. |
| Synopsys SCL | `SNPSLMD_LICENSE_FILE` 권장, `snpslmd` daemon | [Licensing QuickStart의 Linux 사용자 환경](https://www.synopsys.com/support/licensing-installation-computeplatforms/licensing.html)은 `LM_LICENSE_FILE`보다 전용 변수를 권장합니다. |
| Siemens EDA의 SALT 기반 제품 | `SALT_LICENSE_SERVER`, `saltd` daemon | [Questa–Altera FPGA Edition 안내](https://docs.altera.com/r/docs/691278/21.3/questa-altera-fpga-edition-quick-start-quartus-prime-pro-edition/prerequisites?contentId=V3LT4GtnQKslf4eFeQZrWw)에서 확인한 사례입니다. 다른 Siemens 제품·구판에 일괄 적용하지 않습니다. |

이름이 비슷한 환경 변수를 모두 같은 값으로 채우기보다, 현재 제품의 라이선스 설명과 기관 설정을 확인합니다. 구판 자료에서 보이는 `MGLS_LICENSE_FILE` 등의 설정을 최신 SALT 안내와 섞지 않습니다. 여러 독립 서버를 나열하는 구분자도 운영체제와 제품에 따라 확인해야 합니다. Synopsys Linux 예시에서는 독립 서버 사이에 콜론을, 삼중 중복 서버 구성에는 쉼표를 사용합니다.

제품 패키지 이름과 실제 체크아웃 feature 이름은 같지 않을 수 있습니다. Virtuoso 편집 환경이 열려도 Spectre 시뮬레이터나 별도 분석 옵션의 사용권이 충분하다는 뜻은 아닙니다. 필요한 feature·토큰·동시 실행 수는 계약과 판본의 공식 라이선스 안내 및 실제 로그로 확인합니다.

## 5. 호스트·포트·권한을 분리한 진단

네트워크 라이선스에서 `port@host`의 포트는 보통 라이선스 매니저가 듣는 TCP 포트입니다. Synopsys SCL 문서는 `SERVER`의 매니저 포트와 `VENDOR snpslmd`의 daemon 포트를 별도로 설명합니다. 매니저에 접속된다고 vendor daemon까지 통신된다고 단정할 수 없습니다. 방화벽 설정은 승인된 관리자가 실제 서버 구성에 맞춰 수행합니다.

| 증상 | 먼저 구분할 원인 | 확인할 자료 |
|---|---|---|
| 명령을 찾지 못합니다. | 설치 경로·PATH·셸 설정 | `command -v` 결과와 배치 작업의 환경 |
| 실행 파일을 찾지만 시작하지 못합니다. | 아키텍처·동적 라이브러리·파일 또는 마운트 실행 권한 | OS 정보, 공급사 설치 검사, 시작 오류 |
| 서버를 찾지 못하거나 연결 시간이 초과됩니다. | 서버명 해석·VPN·라우팅·포트 | 정확한 `port@host`, 접속망, 관리자 통신 검사 |
| 서버에는 연결되지만 체크아웃이 거절됩니다. | 기능 미보유·모든 수량 사용 중·만료·daemon 호환성·접근 제한 | 클라이언트 오류와 서버 로그 |
| GUI만 표시되지 않습니다. | 원격 화면 전달·DISPLAY·그래픽 환경 | 기관의 원격 GUI 접속 안내 |
| 도구는 시작하지만 모델·셀을 찾지 못합니다. | PDK 뷰·라이브러리 매핑·경로·권한 | 도구 로그의 최초 누락 파일과 프로젝트 설정 |

관리자가 제공한 FlexNet 도구가 PATH에 있을 때 다음처럼 상태를 조회할 수 있습니다. 여기서도 주소는 공식 예시입니다. 출력에는 사용자·호스트 정보가 들어갈 수 있으므로 공유할 때는 필요한 오류 부분을 골라 전달합니다.

```bash
lmutil lmstat -a -c '27020@aspen' # 지정한 공식 예시 서버의 상태를 조회합니다.
```

명령 형식과 `-a`, `-c`의 의미는 Synopsys가 제공하는 [FlexNet Publisher 2024 R2 관리 안내의 Command-Line Utilities와 lmstat 절](https://www.synopsys.com/content/dam/synopsys/support/documents/licensing/enduser.pdf)에서 확인할 수 있습니다. 해당 PDF의 인쇄 쪽수는 각각 125쪽과 152쪽입니다.

라이선스 파일의 서명·feature 줄을 고쳐 해결하려 하지 않습니다. 사용자는 실패한 제품 판본, 시각, 호스트, 오류 문구와 재현 순서를 전달하고, 관리자는 서버·계약·네트워크를 확인하는 방식으로 역할을 나눕니다. 전체 서버 재시작이나 다른 사용자의 작업 종료는 단순한 사용자 진단과 별개입니다.

## 6. 다음 학습

설치가 끝나면 [공정·PDK·라이브러리의 관계](02-공정노드와PDK및라이브러리_process-pdk-libraries.md)를 확인하고, [도구 역할 지도](03-설계도구와공급사_eda-tool-map.md)에서 현재 수행할 단계의 입력과 출력을 찾습니다. 공개 환경에서는 [LibreLane PM32 실습](12-공개도구로RTL에서GDS까지_open-rtl-to-gds.md)으로 설치 확인, 배치 실행, 보고서와 GDS 확인을 연결합니다.

## 출처와 확인 범위

- Synopsys [Licensing QuickStart](https://www.synopsys.com/support/licensing-installation-computeplatforms/licensing.html): SCL·FlexNet 버전 구별, 다운로드 권한, Linux 변수, 서버·daemon 포트와 상태 진단 부분을 확인했습니다. 특정 feature나 계약 수량을 추정하지 않았습니다.
- Synopsys [SCL Supported OS](https://www.synopsys.com/support/licensing-installation-computeplatforms/licensing/scl-supported-os.html): 적용 대상이 라이선스 서버임을 확인했습니다.
- Cadence [Registration Help](https://registration.cadence.com/resource/COSHelpPages/Help/help_register_en_US.html): Host ID와 라이선스 경로 부분을 확인했습니다.
- Altera [Questa 라이선스 선행 조건](https://docs.altera.com/r/docs/691278/21.3/questa-altera-fpga-edition-quick-start-quartus-prime-pro-edition/prerequisites?contentId=V3LT4GtnQKslf4eFeQZrWw): SALT 설정 사례를 확인했습니다. 상용 Siemens EDA 전체의 설치 지침으로 일반화하지 않았습니다.
- LibreLane [Linux용 Nix 설치](https://librelane.readthedocs.io/en/stable/installation/nix_installation/installation_linux.html): 공개 실습 환경의 지원 대상과 설치 방식만 참고했습니다.
