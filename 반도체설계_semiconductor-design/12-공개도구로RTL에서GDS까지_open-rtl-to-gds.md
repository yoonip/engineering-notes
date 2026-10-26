# LibreLane으로 RTL에서 GDS까지

이 실습은 공식 LibreLane 입문 예제인 PM32를 사용해 RTL, 설정 파일, 합성·배치배선, 보고서와 GDS를 연결합니다. PM32는 직렬·병렬 곱셈 블록을 이용하는 32비트 곱셈기 예제입니다. 예제 RTL은 공식 저장소에서 그대로 가져오며, 독자적으로 새 회로를 검증한 사례로 제시하지 않습니다.

기준일은 2026년 10월 26일입니다. 실행 경로는 Linux의 Nix와 LibreLane 3.0.16 태그로 고정합니다. 아래 설치·실행 명령과 결과 구조는 공식 문서를 대조해 작성했으며, 이 문서를 작성한 Windows 작업 환경에서 Nix 설치, smoke test, PM32 실행 또는 GDS 생성을 수행하지 않았습니다. 소요 시간·면적·전력·타이밍 통과 수치를 자체 측정 결과로 제시하지 않습니다.

## 1. 어떤 도구를 실행하는 실습인지

LibreLane은 여러 도구를 연결하는 흐름 기반입니다. 이 실습에서는 기본 Classic 흐름을 사용합니다. Yosys가 합성을, OpenROAD가 물리 구현의 여러 단계를 맡으며, 흐름에 구성된 검사 도구가 레이아웃과 연결을 확인합니다. OpenLane 2나 OpenROAD-flow-scripts의 명령을 이 실습의 명령과 섞지 않습니다. 구성은 [3.0.16 태그의 입문 문서](https://github.com/librelane/librelane/blob/3.0.16/docs/source/getting_started/newcomers/index.md)와 [Classic 단계 설명](https://librelane.readthedocs.io/en/stable/reference/flows.html)을 참고했습니다.

```text
pm32.v + spm.v + config.json
               ↓
RTL 검사 → 합성 → 플로어플랜·전원망 → 배치 → 클록 트리 → 배선
                                                               ↓
                     보고서·GDS 확인 ← 타이밍·DRC·LVS·기생 추출
```

이 흐름이 생성하는 블록 레이아웃과 I/O 패드·패키지·테스트 계획을 갖춘 완성 칩은 구분합니다. GDS 파일이 생겼다는 사실만으로 기능 검증, 모든 제작 규칙, 파운드리 승인과 제조 수율까지 확인된 것은 아닙니다.

## 2. 설치 전 준비

LibreLane의 [Linux용 Nix 설치 안내](https://librelane.readthedocs.io/en/stable/installation/nix_installation/installation_linux.html)는 Ubuntu 22.04 이상을 주 지원 대상으로 설명하며, 최소 8 GiB·권장 16 GiB RAM을 제시합니다. 이 수치는 공식 입문 환경의 안내이며 모든 설계의 자원 요구량을 보장하지 않습니다. 설치·PDK 내려받기·실행 결과를 저장할 공간과 인터넷 연결도 필요합니다.

이하 명령은 Bash용입니다. Ubuntu 이외의 배포판에서는 `apt-get` 줄을 복사하지 않고 해당 배포판의 패키지 설치 방법을 사용합니다. 기관에서 Nix를 관리한다면 개인적으로 다시 설치하지 않고 관리자 안내에 따라 캐시 설정을 확인합니다.

다음은 공식 설치 절차에 필요한 `curl`과 소스 다운로드에 필요한 `git`을 준비하는 예시입니다. 공식 문서의 `curl` 설치 줄에 `git`을 함께 지정한 부분과 작업 디렉터리를 만드는 부분은 이 글의 추가입니다.

```bash
sudo apt-get install -y curl git # Ubuntu에서 내려받기와 소스 복제에 필요한 도구를 설치합니다.
mkdir -p ~/eda-setup # 설치 파일을 검토할 개인 디렉터리를 만듭니다.
cd ~/eda-setup # 설치 파일을 저장할 위치로 이동합니다.
curl --proto '=https' --tlsv1.2 -fsSL https://artifacts.nixos.org/nix-installer -o nix-installer # 공식 안내의 Nix 설치기를 파일로 받습니다.
less ./nix-installer # 설치기 내용을 읽고 q로 빠져나옵니다.
```

공식 문서는 설치기 출력을 `sh`로 바로 전달합니다. 여기서는 같은 설치기를 먼저 파일로 저장해 읽고 실행하도록 순서를 바꿨습니다. 다음 한 줄의 `\n`은 Bash의 `$'…'` 안에서 줄바꿈이 되며, 세 가지 Nix 설정을 전달합니다. 설치기 URL은 움직이는 배포 경로이므로 LibreLane 태그를 고정하더라도 설치기 자체의 판본까지 고정되는 것은 아닙니다. 설치 시 표시되는 Nix 판본과 사용한 안내를 기록합니다.

```bash
sh ./nix-installer install --no-confirm --extra-conf $'extra-substituters = https://nix-cache.fossi-foundation.org\nextra-trusted-public-keys = nix-cache.fossi-foundation.org:3+K59iFwXqKsL7BNu6Guy0v+uTlwsxYQxjspXzqLYQs=\nextra-experimental-features = nix-command flakes' # 공식 설치 인자와 캐시·실험 기능 설정을 전달합니다.
```

캐시는 미리 빌드한 도구를 내려받는 저장소이고 공개키는 그 캐시의 서명 검증에 쓰입니다. `nix-command`와 `flakes`는 이 환경이 요구하는 Nix 기능입니다. 이미 Nix가 있다면 설정 파일을 통째로 덮어쓰지 말고 [공식 설치 안내의 기존 설치 부분](https://librelane.readthedocs.io/en/stable/installation/nix_installation/installation_linux.html)을 확인합니다. 설치 절차가 끝나면 공식 안내대로 터미널을 모두 닫고 새 터미널에서 진행합니다.

설치 명령과 캐시 설정의 고정된 원문 위치는 [3.0.16의 Linux 설치 문서](https://github.com/librelane/librelane/blob/3.0.16/docs/source/installation/nix_installation/installation_linux.md)입니다. 설치는 시스템 구성 변경과 관리자 권한 요청을 포함할 수 있으므로 공유 서버에서는 기관의 설치 담당자가 수행합니다.

## 3. 판본을 고정하고 설치 확인

새 Bash 터미널에서 진행합니다. `~/librelane`이 이미 다른 작업에 사용 중이면 그 디렉터리에 덮어쓰지 않고 별도 경로를 정한 뒤 아래 경로들을 함께 바꿉니다.

```bash
git clone --branch 3.0.16 --depth 1 https://github.com/librelane/librelane/ ~/librelane # 확인한 공식 태그만 내려받습니다.
git -C ~/librelane rev-parse HEAD # 실제로 받은 소스의 커밋 식별자를 표시합니다.
nix-shell ~/librelane/shell.nix # 해당 소스의 도구 환경으로 들어갑니다.
```

공식 입문 문서의 기본 브랜치 복제 명령에 태그와 얕은 복제 옵션을 추가했습니다. [공식 3.0.16 릴리스](https://github.com/librelane/librelane/releases)와 [그 태그의 shell.nix](https://github.com/librelane/librelane/blob/3.0.16/shell.nix) 존재를 확인한 경로입니다. 이후 명령은 이 Nix 셸 안에서 실행합니다. 처음에는 도구와 의존성을 내려받습니다.

```bash
librelane --smoke-test # 공식 설치 확인용 작은 흐름을 실행합니다.
```

smoke test는 설치된 흐름을 작은 예제로 시험하는 단계입니다. 이 테스트가 통과해도 PM32나 수정한 RTL의 기능까지 검증한 것은 아닙니다. 기본 공개 PDK의 내려받기가 발생할 수 있습니다. [3.0.16의 PDK 안내](https://github.com/librelane/librelane/blob/3.0.16/docs/source/usage/about_pdks.md)는 흐름이 시험한 Open PDKs 판본을 Ciel로 준비하는 방식을 설명합니다. 임의의 PDK 최신판으로 바꿔 설치 문제를 덮지 않습니다.

## 4. 공식 PM32 파일 준비

공식 입문 문서는 두 RTL 파일을 생성하여 예제 내용을 넣도록 안내합니다. 여기서는 이미 받은 같은 태그의 파일을 복사합니다. RTL과 원래 저작권 표시를 바꾸지 않는 편의상 변경입니다. 원문은 [pm32.v](https://github.com/librelane/librelane/blob/3.0.16/docs/source/getting_started/newcomers/pm32.v)와 [spm.v](https://github.com/librelane/librelane/blob/3.0.16/docs/source/getting_started/newcomers/spm.v)입니다.

```bash
mkdir -p ~/my_designs/pm32 # 입문 문서와 같은 설계 디렉터리를 만듭니다.
cp ~/librelane/docs/source/getting_started/newcomers/pm32.v ~/my_designs/pm32/ # 공식 최상위 RTL을 복사합니다.
cp ~/librelane/docs/source/getting_started/newcomers/spm.v ~/my_designs/pm32/ # 공식 하위 곱셈 블록 RTL을 복사합니다.
```

텍스트 편집기로 `~/my_designs/pm32/config.json`을 만들고 다음 공식 설정을 저장합니다. JSON은 주석을 허용하지 않으므로 각 항목의 뜻은 표로 설명합니다.

```json
{
  "DESIGN_NAME": "pm32",
  "VERILOG_FILES": ["dir::pm32.v", "dir::spm.v"],
  "CLOCK_PERIOD": 25,
  "CLOCK_PORT": "clk"
}
```

| 항목 | 뜻 |
|---|---|
| `DESIGN_NAME` | 최상위 모듈 이름 `pm32`입니다. |
| `VERILOG_FILES` | 읽을 RTL 두 개이며 `dir::`는 설정 파일 디렉터리를 기준으로 해석하는 LibreLane 경로 표기입니다. |
| `CLOCK_PERIOD` | 예제에서 지정한 클록 주기 25 ns입니다. 합성·구현 목표이며 실제 측정한 최대 동작 주파수가 아닙니다. |
| `CLOCK_PORT` | 최상위 RTL의 클록 입력 `clk`입니다. |

단위와 공통 설정의 뜻은 [공식 공통 변수 표](https://librelane.readthedocs.io/en/stable/reference/common_flow_vars.html)에서도 확인할 수 있습니다.

이 설정은 입문 예제를 위한 최소 구성입니다. 실제 외부 회로와 연결되는 블록에서는 입력·출력 지연, 부하·구동 조건, 여러 클록과 예외 경로 등의 제약도 설계 조건에 맞게 정해야 합니다. 이 예제의 최소 파일을 모든 프로젝트의 완성된 타이밍 제약으로 간주하지 않습니다.

## 5. 실행과 GDS 보기

Nix 셸 안에서 실행합니다. 실패하면 마지막 오류 한 줄뿐 아니라 처음 실패한 단계의 로그를 함께 읽습니다.

```bash
librelane ~/my_designs/pm32/config.json # 공식 PM32 설정으로 기본 흐름을 실행합니다.
```

흐름이 정상적으로 끝난 뒤 그래픽 화면을 사용할 수 있는 세션에서 다음 공식 명령으로 마지막 실행 결과를 엽니다.

```bash
librelane --last-run --flow openinklayout ~/my_designs/pm32/config.json # 마지막 실행의 레이아웃을 KLayout에서 엽니다.
```

`--last-run`은 기존 실행 결과를 고르는 옵션입니다. 실패한 실행을 성공으로 바꾸는 옵션이 아닙니다. 창이 열리지 않으면 GUI 접속 문제와 GDS 생성 실패를 구분합니다. 서버의 배치 실행 결과는 남아 있어도 현재 터미널에 그래픽 표시 경로가 없을 수 있습니다.

GDS 파일 자체를 확인할 때는 해당 실행의 `final/gds` 등 실제 생성된 GDS 뷰 경로를 찾고 KLayout의 파일 열기에서 그 파일을 선택합니다. 현재 보고 있는 데이터가 GDS인지 LEF/DEF 등 다른 레이아웃 뷰인지도 구분합니다.

## 6. 결과를 읽는 순서

실행별 디렉터리는 설계 아래 `runs`에 생깁니다. 공식 문서에 등장하는 `RUN_2023-12-27_16-59-15` 같은 이름은 예시이며 이 글의 실행 시각이 아닙니다. 단계 번호나 파일 이름의 일부는 구성·판본에 따라 달라질 수 있으므로 현재 실행 디렉터리와 로그에서 찾습니다.

| 확인 대상 | 읽는 목적 |
|---|---|
| 각 단계의 로그와 `COMMANDS` | 어떤 도구가 어떤 입력으로 실행되었고 어디서 실패했는지 확인합니다. |
| 단계의 `config.json` | 그 실행에 실제로 적용된 설정을 확인합니다. |
| `state_in.json`, `state_out.json` | 단계 전후의 산출물 경로와 상태를 연결합니다. |
| `final/gds` 등 레이아웃 뷰 | 최종 도형과 참조 셀을 확인합니다. GDS 화면만으로 모든 검사를 판단하지 않습니다. |
| 최종 netlist·SDC·SPEF 등 | 셀 연결, 시간 제약, 배선 기생 정보를 서로 구분합니다. |
| 타이밍·DRC·LVS 보고서와 최종 지표 | 실제 실행한 검사의 범위, 위반 내용과 분석 조건을 확인합니다. |

산출물 구조는 [공식 입문 문서의 Run directory와 Final views](https://librelane.readthedocs.io/en/stable/getting_started/newcomers/index.html)를 참고했습니다. 정적 타이밍의 입력 관계는 [OpenSTA 설명](https://openroad.readthedocs.io/en/latest/main/src/sta/README.html), 배선 기생 추출은 [OpenRCX 설명](https://openroad.readthedocs.io/en/latest/main/src/rcx/README.html)과 연결해 읽을 수 있습니다.

타이밍에서는 setup과 hold를 나눠 보고, slack은 요구 시간과 도착 시간의 관계로 해석합니다. WNS가 음수이면 해당 분석에서 가장 나쁜 경로의 시간 여유가 부족한 것입니다. 이 실습에서 사용하는 [OpenSTA의 `report_wns`](https://opensta.readthedocs.io/en/latest/Commands/#report_wns)는 최악 slack이 양수이면 0을 보고합니다. WNS가 0이거나 개별 경로의 slack이 양수여도 코너·제약·미제약 경로와 검사한 경로 범위를 함께 읽습니다. DRC는 위반 규칙과 위치를, LVS는 소자·핀·연결의 차이를 확인합니다.

## 7. 실패 원인별 진단

| 증상 | 먼저 확인할 내용 |
|---|---|
| `nix`·`nix-shell`을 찾지 못합니다. | 설치 완료 여부와 새 터미널의 환경 적용 |
| Nix가 도구를 계속 소스에서 빌드합니다. | 공식 캐시 주소·신뢰 공개키, 캐시 접근 오류와 설치 안내 |
| `librelane`을 찾지 못합니다. | 해당 태그의 Nix 셸 안에 있는지와 shell.nix 로딩 오류 |
| PDK를 준비하지 못합니다. | 내려받기 오류, 저장 공간·권한, 흐름이 요구하는 PDK 판본 |
| 최상위 모듈·파일을 찾지 못합니다. | `DESIGN_NAME`, 실제 모듈 이름, `VERILOG_FILES` 경로 |
| JSON을 읽지 못합니다. | 쉼표·따옴표·주석, 파일 인코딩과 저장 위치 |
| 배치·배선·타이밍 단계가 실패합니다. | 실패한 단계 로그, 플로어플랜·혼잡·클록·제약과 라이브러리 조건 |
| 레이아웃 화면만 열리지 않습니다. | 실행 성공 여부와 별도로 그래픽 세션·원격 표시 설정 |
| DRC·LVS가 실패합니다. | 해당 보고서의 첫 원인, 전원·셀·매크로 뷰와 실제 도형·연결 |

설치·다운로드 문제를 회로 오류로 판단하거나 검사 실패를 건너뛰어 성공으로 기록하지 않습니다. 먼저 원래 예제와 고정한 판본에서 설치 확인이 되는지 구분한 뒤, RTL·클록·핀 배치 등을 바꿀 때는 무엇을 바꿨는지와 새 실행 결과를 따로 남깁니다.

## 8. 남길 실행 기록

독자가 실제 실행할 때는 날짜, OS·아키텍처, Nix 판본, LibreLane 태그와 커밋, PDK·표준 셀 판본, 설정 파일, 실행별 디렉터리와 종료 상태를 남깁니다. 설치 확인 통과, PM32 흐름 완료, 기능 시뮬레이션 통과와 제작 승인 여부를 각각 구분합니다. 면적·지연·전력 수치를 비교하려면 같은 입력과 제약·코너·도구·PDK 조건인지 먼저 확인합니다.

PDK의 파일 역할은 [공정·PDK·라이브러리](02-공정노드와PDK및라이브러리_process-pdk-libraries.md), 개별 도구의 위치는 [설계 도구 지도](03-설계도구와공급사_eda-tool-map.md), 상용 환경에서의 셸·라이선스 문제는 [Linux와 라이선스](01-Linux설치와라이선스_linux-eda-setup.md)에서 이어서 설명합니다.
