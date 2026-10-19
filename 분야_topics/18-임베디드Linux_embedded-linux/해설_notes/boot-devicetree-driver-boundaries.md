# Embedded Linux: 부팅, Device Tree와 드라이버의 경계

[Embedded Linux](../README.md) · [실행 모형](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 부팅 로그를 단계별로 나누는 이유

전원을 넣고 셸이 뜨기까지 하나의 프로그램만 실행되는 것은 아니다. 플랫폼에 따라 ROM·보안 펌웨어·bootloader가 메모리와 실행 환경을 준비하고 kernel을 넘겨받게 한다. kernel은 장치와 메모리를 관리하고, root filesystem에서 초기 사용자 공간 프로그램을 실행한다. initramfs나 여러 단계의 bootloader를 쓰는 경우도 있으며 모든 보드가 같은 경로를 따르지는 않는다.

AArch64 Linux의 직접 진입 규약에는 이미지·Device Tree의 배치, 레지스터와 예외 수준, cache 등의 조건이 있다. 예를 들어 해당 DT 부팅 규약에서 x0는 DTB의 물리 주소를 전달한다. 이를 다른 CPU나 EFI 경로의 모든 단계에 무조건 적용하지 않는다. “파일을 메모리에 복사했다”와 “kernel 진입 전제를 만족했다”는 다른 상태다. [Linux Booting AArch64](https://docs.kernel.org/arch/arm64/booting.html)

### Device Tree는 장치 설명이고 드라이버는 동작 코드다

Device Tree는 자동 발견이 어려운 하드웨어 구조와 속성을 전달하는 자료다. 텍스트 소스 DTS를 DTB로 컴파일해 전달할 수 있다. 노드에는 `compatible`, 주소 범위, interrupt, clock·reset·전원 등의 연결 정보가 담길 수 있다. 어떤 속성이 필요한지는 해당 binding이 정한다. 주소 셀의 수와 버스 변환 규칙을 무시한 채 `reg` 숫자를 곧바로 CPU 주소로 읽지 않는다. [Linux and the Devicetree](https://docs.kernel.org/devicetree/usage-model.html)

DTB를 수정했다고 실제 배선이 바뀌거나 드라이버 기능이 생기지는 않는다. 부팅 중 적용한 DTB가 빌드 디렉터리의 파일과 같은지도 별도 문제다. bootloader의 수정과 overlay가 적용될 수 있기 때문이다.

| 확인할 경계 | 서로 다른 사실 |
| --- | --- |
| 하드웨어 설명 | 노드가 존재한다 |
| 장치 생성·매칭 | 버스가 장치와 지원 드라이버를 연결한다 |
| probe | 자원과 장치 상태를 확인하고 초기화한다 |
| 사용자 공간 | 인터페이스를 열고 실제 기능을 이용한다 |

지원 ID가 맞아도 probe가 성공한다는 보장은 없다. 의존 clock·regulator 같은 자원이 준비되지 않아 재시도가 필요할 수 있고 실제 오류가 있을 수도 있다. 매칭, probe, 사용 가능한 인터페이스를 구분해 로그를 읽는다. [Linux Driver Binding](https://docs.kernel.org/driver-api/driver-model/binding.html)

### 관찰할 때 남길 근거

UART console의 마지막 줄만으로 원인을 정하기보다 어느 단계의 로그인지 먼저 구분한다. kernel 진입 전이면 부트 이미지·부팅 규약을, kernel에서 root mount가 실패하면 저장장치·filesystem·명령행을, 장치 하나가 빠졌다면 DT·driver 설정·probe 오류를 따라간다. Linux에서 다음 조회는 시작점이 된다.

```bash
# 실행 중인 kernel과 부팅 인자·드라이버 로그를 구분해 읽는다.
uname -r
cat /proc/cmdline
dmesg
ls /sys/bus/platform/devices
```

접근 권한이나 배포판에 따라 로그를 읽는 방법이 달라진다. `dmesg`에 로그가 없다는 사실만으로 드라이버가 없다고 결론 내리지 않는다. kernel 설정, module 존재·로드 상태, 실제 bus 종류를 함께 본다. sysfs 경로도 장치·버스별로 다르다.

### 모형과 실제 보드 검증

`probe_model`은 compatible 미일치, 자원 미준비, 준비 완료를 각각 `no-match`, `deferred`, `bound`로 구분하는 교육용 모형이다. 실제 Linux의 버스 매칭·binding과 모든 probe 반환값을 구현한 함수가 아니다. 테스트는 매칭 성공과 자원 준비가 같은 조건이 아님을 확인한다.

실제 검증에는 보드·SoC revision, kernel commit/config, bootloader, DTB와 rootfs를 함께 기록한다. 장치가 등록된 뒤 정상 데이터·오류 입력·재부팅 조건에서 기능을 확인해야 한다. 이 예제 묶음의 Python 테스트는 실보드 부팅 성공이나 드라이버 적합성을 인증하지 않는다.

## English

### Separate the stages behind a boot log

Power-on to shell usually crosses several programs. Depending on the platform, ROM, security firmware, and a bootloader prepare execution before the kernel manages memory/devices and starts initial userspace from a root filesystem. Initramfs and multistage loaders are possible; no single chain covers every board.

Direct AArch64 kernel entry has image, DT, register, exception-level, and cache requirements. For its DT entry convention, x0 carries the DTB physical address. Do not apply that statement indiscriminately to every architecture or EFI stage. Copying an image into memory does not establish that its entry contract is satisfied. [AArch64 booting](https://docs.kernel.org/arch/arm64/booting.html)

### Description and operation are separate

Device Tree describes hardware and connections that may not be discoverable automatically. DTS source can compile to DTB. Bindings define properties such as `compatible`, resources, interrupts, clocks, resets, and power relationships. Address-cell and bus-translation rules matter; a `reg` number is not automatically a CPU address. [Devicetree usage](https://docs.kernel.org/devicetree/usage-model.html)

Editing DTB does not alter wiring or implement a driver. Bootloader changes and overlays can also make the running tree differ from a build-directory file.

Distinguish a described node, a created/matched device, successful probe and initialization, and actual userspace use. Supported identifiers do not guarantee successful probe. Dependencies may require retrying later, or a real failure may exist. [Driver binding](https://docs.kernel.org/driver-api/driver-model/binding.html)

### Observe the correct boundary

Locate the stage before assigning a cause: pre-kernel failures concern images and entry conditions; root-mount failures concern storage, filesystems, and command lines; a missing device leads through DT, configuration, and probe evidence. The read-only commands inspect kernel version, boot arguments, logs, and platform-device enumeration. Permissions and distributions affect log access. Absent log text alone does not prove absent support; check configuration, modules, and the actual bus. Sysfs paths vary by device and bus.

### Model and board validation

`probe_model` distinguishes identifier mismatch, missing resources, and readiness. It models neither the complete Linux matching machinery nor every probe return. Tests show that matching and resource readiness are distinct conditions.

A board check records SoC/revision, kernel commit/config, bootloader, DTB, and rootfs, then verifies actual operation under normal, erroneous, and reboot conditions. The Python tests do not establish real-board boot success or driver compatibility.

## 출처 / Sources

아키텍처별 부팅 규약, 하드웨어 설명, 드라이버 연결의 역할을 Linux 공식 문서 세 편으로 대조했다. / Three kernel documents distinguish architecture entry, hardware description, and binding. 확인 / checked: 2026-10-19.
