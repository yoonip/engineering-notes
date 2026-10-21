# Embedded Linux: 부팅, Device Tree와 드라이버의 경계

[Embedded Linux](../README.md) · [실행 모형](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 부팅 로그를 단계별로 나누는 이유

전원을 넣고 셸이 뜨기까지 하나의 프로그램만 실행되는 것은 아닙니다. 플랫폼에 따라 ROM·보안 펌웨어·bootloader가 메모리와 실행 환경을 준비하고 kernel을 넘겨받게 합니다. kernel은 장치와 메모리를 관리하고, root filesystem에서 초기 사용자 공간 프로그램을 실행합니다. initramfs나 여러 단계의 bootloader를 쓰는 경우도 있으며 모든 보드가 같은 경로를 따르지는 않습니다.

AArch64 Linux의 직접 진입 규약에는 이미지·Device Tree의 배치, 레지스터와 예외 수준, cache 등의 조건이 있습니다. 예를 들어 해당 DT 부팅 규약에서 x0는 DTB의 물리 주소를 전달합니다. 이를 다른 CPU나 EFI 경로의 모든 단계에 무조건 적용하지 않습니다. “파일을 메모리에 복사했다”와 “kernel 진입 전제를 만족했다”는 다른 상태입니다. [Linux Booting AArch64](https://docs.kernel.org/arch/arm64/booting.html)

### Device Tree는 장치 설명이고 드라이버는 동작 코드입니다

Device Tree는 자동 발견이 어려운 하드웨어 구조와 속성을 전달하는 자료입니다. 텍스트 소스 DTS를 DTB로 컴파일해 전달할 수 있습니다. 노드에는 `compatible`, 주소 범위, interrupt, clock·reset·전원 등의 연결 정보가 담길 수 있습니다. 어떤 속성이 필요한지는 해당 binding이 정합니다. 주소 셀의 수와 버스 변환 규칙을 무시한 채 `reg` 숫자를 곧바로 CPU 주소로 읽지 않습니다. [Linux and the Devicetree](https://docs.kernel.org/devicetree/usage-model.html)

DTB를 수정했다고 실제 배선이 바뀌거나 드라이버 기능이 생기지는 않습니다. 부팅 중 적용한 DTB가 빌드 디렉터리의 파일과 같은지도 별도 문제입니다. bootloader의 수정과 overlay가 적용될 수 있기 때문입니다.

| 확인할 경계 | 서로 다른 사실 |
| --- | --- |
| 하드웨어 설명 | 노드가 존재합니다 |
| 장치 생성·매칭 | 버스가 장치와 지원 드라이버를 연결합니다 |
| probe | 자원과 장치 상태를 확인하고 초기화합니다 |
| 사용자 공간 | 인터페이스를 열고 실제 기능을 이용합니다 |

지원 ID가 맞아도 probe가 성공한다는 보장은 없습니다. 의존 clock·regulator 같은 자원이 준비되지 않아 재시도가 필요할 수 있고 실제 오류가 있을 수도 있습니다. 매칭, probe, 사용 가능한 인터페이스를 구분해 로그를 읽습니다. [Linux Driver Binding](https://docs.kernel.org/driver-api/driver-model/binding.html)

### 관찰할 때 남길 근거

UART console의 마지막 줄만으로 원인을 정하기보다 어느 단계의 로그인지 먼저 구분합니다. kernel 진입 전이면 부트 이미지·부팅 규약을, kernel에서 root mount가 실패하면 저장장치·filesystem·명령행을, 장치 하나가 빠졌다면 DT·driver 설정·probe 오류를 따라갑니다. Linux에서 다음 조회는 시작점이 됩니다.

```bash
# 실행 중인 kernel과 부팅 인자·드라이버 로그를 구분해 읽는다.
uname -r
cat /proc/cmdline
dmesg
ls /sys/bus/platform/devices
```

접근 권한이나 배포판에 따라 로그를 읽는 방법이 달라집니다. `dmesg`에 로그가 없다는 사실만으로 드라이버가 없다고 결론 내리지 않습니다. kernel 설정, module 존재·로드 상태, 실제 bus 종류를 함께 봅니다. sysfs 경로도 장치·버스별로 다릅니다.

### 모형과 실제 보드 검증

`probe_model`은 compatible 미일치, 자원 미준비, 준비 완료를 각각 `no-match`, `deferred`, `bound`로 구분하는 교육용 모형입니다. 실제 Linux의 버스 매칭·binding과 모든 probe 반환값을 구현한 함수가 아닙니다. 테스트는 매칭 성공과 자원 준비가 같은 조건이 아님을 확인합니다.

실제 검증에는 보드·SoC revision, kernel commit/config, bootloader, DTB와 rootfs를 함께 기록합니다. 장치가 등록된 뒤 정상 데이터·오류 입력·재부팅 조건에서 기능을 확인해야 합니다. 이 예제 묶음의 Python 테스트는 실보드 부팅 성공이나 드라이버 적합성을 인증하지 않습니다.

### 업데이트한 파일과 다음 부팅의 선택을 구분합니다

새 kernel·firmware 파일을 받았다는 사실만으로 다음 부팅의 확정 대상으로 바꾸지는 않습니다. 별도 [A/B 업데이트 파일 모형](../../../예제_examples/실무검증_practical-validation/firmware_update/README.md)은 기존 A를 보존한 채 B를 기록·길이/해시 확인·pending 게시·trial 선택·checkpoint 뒤 confirm으로 나눕니다. 첫 trial 표시를 남긴 뒤 확인 없이 재시작하면 A로 rollback합니다. 실제 kernel 진입이나 firmware 분기를 실행하는 모형은 아닙니다.

초기 상태는 active=A·generation0, 후보 게시 뒤 generation1, trial 표시 뒤 generation2입니다. 확인되면 active=B·generation3, 확인 없이 다시 시작하면 active=A·generation3입니다. 같은 generation3이라도 어느 전이를 했는지에 따라 선택 슬롯은 다릅니다. 숫자가 크다는 사실만으로 새 이미지가 업무를 정상 수행했거나 보안상 허가됐다고 판단하지 않습니다.

```python
from pathlib import Path  # from/import는 경로 객체를 가져옵니다.
from models import load_state  # 새 예제 폴더의 CRC·상태 해석 함수를 가져옵니다.
def recorded_slot(result_store):  # def는 파일이 있는 위치를 인수로 받는 함수를 정의합니다.
    state = load_state(Path(result_store))  # 실제 파일 두 부 중 유효한 최신 상태를 읽습니다.
    return state["active"], state["generation"]  # []로 키를 읽어 슬롯과 기록 세대를 반환합니다.
```

예제 코드 폴더에서 실행하며 `result_store`에는 새 검증 결과의 `happy/store` 경로를 줍니다. 로컬 정상 실행의 해당 경로를 읽은 결과는 `('B', 3)`입니다. 이는 저장된 metadata 해석이며 선택 이미지의 실제 실행·하드웨어 초기화 결과는 아닙니다.

메타데이터 두 부는 generation과 CRC로 갱신 전후를 구분합니다. 새 기록을 전부 쓰기 전에 중단돼도 이전 부가 남도록 구성했습니다. [사례 본문](../../../설계와검증사례_engineering-cases/중단된업데이트의슬롯선택과롤백_firmware-ab-update.md)은 34개 선택한 파일 기록 지점에서 자식을 종료하고 새 프로세스로 다시 읽은 결과를 비교합니다. `flush`·`fsync` 뒤 명시적으로 끝낸 호스트 시험이며 실제 flash 전원 오류·erase 단위·마모·디렉터리 내구성을 시험하지 않았습니다.

실제 Embedded Linux에서는 kernel 하나뿐 아니라 DTB·rootfs·boot 인자·저장장치 배치의 호환성도 업데이트 계약에 넣어야 합니다. 이 모형은 작은 단일 바이트 이미지를 사용합니다. 해시가 맞아도 권한 인증·anti-rollback은 별도이며, 본문에는 이미지와 해시를 함께 바꾼 입력과 이전 이미지의 재설치를 허용하는 한계 대조를 남겼습니다. MCUboot의 [v2.2.0 설계](https://github.com/mcu-tools/mcuboot/blob/v2.2.0/docs/design.md)와 [Zephyr 이미지 사용 안내](https://github.com/mcu-tools/mcuboot/blob/v2.2.0/docs/readme-zephyr.md)는 확인·복구·서명을 구분하는 원자료입니다. 자체 JSON 형식이 MCUboot image trailer와 같다는 뜻은 아닙니다.

### 부팅에 성공해도 저장 데이터는 별도로 복구합니다

kernel이 실행되고 root filesystem을 mount했다는 사실만으로 응용 데이터의 마지막 변경이 확정됐다고 판단하지 않습니다. bootloader의 이미지 선택과 응용 데이터의 트랜잭션 복구는 서로 다른 계약입니다. 별도 [데이터 저널 파일 예제](../../../예제_examples/실무검증_practical-validation/storage_recovery/README.md)는 실제 파일을 새 Python 프로세스에서 읽어 DATA/COMMIT이 맞는 변경만 재생합니다. SQLite나 실제 보드 전원 오류를 실행한 예제는 아닙니다.

초기 credit=50·stock=10의 seq1 파일은 64바이트입니다. 새 credit=80·stock=7을 담은 DATA는 39바이트, 그 DATA CRC와 seq2를 가리키는 COMMIT은 20바이트입니다. 새 기록 중 39바이트만 남으면 값은 아직 이전의 50/10이고, 59바이트 전체가 있으면 새 값인 80/7입니다. 파일의 존재·값의 존재·확정 표시가 각각 다른 사실입니다.

```python
from pathlib import Path  # from/import는 파일 경로 객체를 가져옵니다.
from models import read_journal  # storage_recovery 코드 폴더의 실제 파일 해석 함수를 가져옵니다.
def recovered_values(store):  # def는 저널 폴더를 받는 함수를 정의합니다.
    _, result = read_journal(Path(store))  # tuple의 raw bytes는 _로 받고 복구 결과를 선택합니다.
    return result["sequence"], result["state"], result["tail_kind"]  # []로 확정 번호·값·꼬리 상태를 읽습니다.
```

storage_recovery 폴더를 작업 경로로 사용하고 `store`에 새 실행의 `happy/store`를 넘깁니다. 최종 정상 파일을 읽은 관측은 `(2, {'credit': 80, 'stock': 7}, 'CLEAN')`입니다. 복구는 원본을 읽기만 하고 tail을 잘라내지 않습니다. 미확정 꼬리 뒤 append는 TAIL_NEEDS_REPAIR로 거부합니다.

[사례 본문](../../../설계와검증사례_engineering-cases/중단된저널의트랜잭션복구_storage-journal-recovery.md)은 59바이트 기록의 prefix 0~59를 각각 동기화·명시 종료·새 프로세스 복구로 비교합니다. 완전한 frame의 CRC 오류는 거부하지만, header length 손상은 부족한 마지막 frame처럼 보일 수 있습니다. 길이를 128로 바꾼 182바이트 파일에서 계산된 끝인 208에 못 미쳐 이전 상태·INCOMPLETE_FRAME으로 남는 한계도 기록했습니다. 이 결과를 모든 저장장치 손상 검출이나 파일시스템 내구성으로 확대하지 않습니다.

SQLite의 [WAL 형식](https://www.sqlite.org/fileformat2.html#walformat)은 commit marker와 유효 frame을, [Atomic Commit](https://www.sqlite.org/atomiccommit.html)은 동기화 순서·복구·더 넓은 crash test를 설명합니다. Linux의 [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html)는 파일과 디렉터리 동기화를 구분합니다. 여기서 실행한 것은 Windows 호스트 파일과 Python 자식이며 Linux kernel·SQLite·directory fsync·실제 전원 제거를 실행한 것이 아닙니다.

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

### Updated files and boot selection

The separate A/B file model preserves A while writing and validating B. Generation 1 publishes a pending image; generation 2 records a trial before selection. Confirmation makes B active at generation 3; an unconfirmed restart rolls back to A at generation 3. The same generation number can therefore describe different decisions. Reading the successful run's stored state returns `('B', 3)` but does not execute firmware or a kernel.

Thirty-four declared interruption checkpoints use flushed file prefixes and fresh Python processes. They do not model flash power loss or persistent filesystem guarantees. A real Linux update also needs a compatibility contract for the kernel, DTB, rootfs and boot arguments. Hash matching, authorization and anti-rollback remain distinct; the unsigned educational model intentionally demonstrates the latter two limits.

### Boot success and application-data recovery

A running kernel and mounted root filesystem do not establish that the last application transaction committed. The separate host-file journal replays matching DATA/COMMIT pairs. Its initial 64-byte file holds credit 50/stock 10; a 39-byte DATA alone preserves those values, while the full 59-byte update recovers credit 80/stock 7 at sequence 2. Reading the normal run returns `(2, {'credit': 80, 'stock': 7}, 'CLEAN')`.

Recovery is read-only and unresolved tails prevent append. Complete-frame CRC errors are rejected, but a damaged declared length can resemble an incomplete tail; the 182-byte versus 208-byte example demonstrates this limitation. Sixty synced prefixes and fresh Python processes do not execute SQLite, Linux filesystem recovery, directory synchronization or actual storage power cuts.

## 출처 / Sources

아키텍처별 부팅 규약, 하드웨어 설명, 드라이버 연결의 역할을 Linux 공식 문서 세 편으로 대조했습니다. / Three kernel documents distinguish architecture entry, hardware description, and binding. 확인 / checked: 2026-10-19.
