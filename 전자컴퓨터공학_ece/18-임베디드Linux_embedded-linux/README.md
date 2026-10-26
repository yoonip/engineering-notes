# 임베디드 Linux | Embedded Linux

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

Embedded Linux는 특정 장치의 기능과 자원에 맞춰 Linux 시스템을 구성하는 분야입니다. 부트로더·커널·장치 정보·루트 파일시스템·사용자 프로그램을 연결해 하나의 시스템을 만듭니다.

## 부팅의 구성요소

U-Boot 같은 부트로더는 커널과 필요한 데이터를 메모리에 올리고 제어를 넘깁니다. Device Tree는 하드웨어 구성을 커널에 전달하는 방식 중 하나입니다. 커널 드라이버는 장치를 운영체제 인터페이스에 연결하고, root filesystem에는 초기화 프로그램과 라이브러리·명령·애플리케이션이 들어갑니다.

## 빌드와 이식

크로스 컴파일은 개발 PC와 다른 대상 플랫폼용 코드를 만드는 일입니다. 툴체인에는 컴파일러·링커·라이브러리 등이 포함됩니다. BSP는 보드에 필요한 지원 코드를 묶습니다. Buildroot는 임베디드 시스템 이미지 구성에, Yocto Project는 재사용 가능한 메타데이터와 레시피 기반의 배포판 구성에 쓰입니다. BusyBox는 여러 기본 명령을 작은 실행 파일로 묶습니다.

QEMU는 지원하는 보드·장치 모델에서 시스템을 시험하는 데 쓰입니다. 실제 보드에서는 전원·부트 설정·장치 트리·드라이버·사용자 공간의 로그를 나눠 읽으며 부팅 실패 지점을 좁힙니다.

## 관련 기술

Linux Kernel, U-Boot, Device Tree, Buildroot, Yocto/OpenEmbedded, BusyBox, QEMU, BSP, Drivers

## 참고 자료

- [Buildroot documentation](https://www.buildroot.org/docs.html)
- [Linux Kernel documentation](https://docs.kernel.org/)

## 기초 해설

- [Embedded Linux: 부팅, Device Tree와 드라이버의 경계](해설_notes/부팅과장치트리및드라이버_boot-devicetree-driver-boundaries.md)

## 이미지를 받았다는 사실과 부팅 성공의 차이

업데이트에는 서로 다른 완료 조건이 있습니다. 파일을 끝까지 받았어도 저장 중 끊길 수 있고, 이미지의 길이와 해시가 맞아도 대상 보드에서 부팅되지 않을 수 있습니다. 커널의 첫 로그가 보여도 필요한 저장장치·통신·사용자 서비스가 준비됐다는 뜻은 아닙니다. 성공 확인을 어디에 두는지가 이전 이미지로 돌아갈 수 있는지에 영향을 줍니다.

| 관측 단계 | 다음 단계로 넘기기 전에 구분할 내용 |
| --- | --- |
| 다운로드 종료 | 선언한 길이와 실제 수신 길이를 대조합니다. |
| 비활성 슬롯 기록 | 저장된 내용을 다시 읽어 검사하고 기존 정상 슬롯을 보존합니다. |
| 부팅 후보 지정 | 이미지 자체와 별개로 슬롯 선택 기록의 유효성을 확인합니다. |
| 새 이미지 첫 실행 | 시험 부팅 상태와 확정 상태를 구분합니다. |
| 응용의 정상 상태 확인 | 미리 정한 서비스·장치 조건을 만족한 뒤 성공을 확정합니다. |

A/B 슬롯은 이미지 두 개를 둘 수 있는 영역을 뜻합니다. 두 영역이 있다고 중단 복구가 저절로 되는 것은 아닙니다. 어느 슬롯이 정상인지, 어떤 후보를 한 번 시험하는지, 확인 없이 재부팅하면 무엇을 선택하는지도 보존해야 합니다. MCUboot의 [Image slots와 부팅 설계](https://docs.mcuboot.com/design.html)는 primary/secondary와 swap·overwrite·direct-XIP 등 서로 다른 구성을 설명합니다. 아래 연결한 파일 모델의 A/B 선택을 모든 MCUboot 모드의 구현으로 취급하지 않습니다.

## 재부팅 횟수의 경계와 성공 확인

[U-Boot의 Boot Count Limit 문서](https://docs.u-boot.org/en/v2025.10/api/bootcount.html)는 `bootcount`가 `bootlimit`를 초과하면 `bootcmd` 대신 `altbootcmd`를 실행한다고 설명합니다. 초과는 같은 값까지 포함하는 조건이 아닙니다. 한도를 3으로 둔 조건식만 계산해 보겠습니다.

```python
limit = 3  # =는 부팅 횟수 한도를 저장합니다.
counts = range(1, 5)  # range는 끝 5를 제외한 1·2·3·4를 만듭니다.
actions = ["altbootcmd" if count > limit else "bootcmd" for count in counts]  # 목록 내포와 조건식으로 동작을 고릅니다.
print(actions)  # ['bootcmd', 'bootcmd', 'bootcmd', 'altbootcmd']입니다.
```

U-Boot 문서에서는 정상 부팅 뒤 응용 코드가 횟수를 0으로 만드는 책임도 설명합니다. 횟수 저장 방식과 `upgrade_available` 등의 조건은 설정에 따라 확인해야 합니다. 위 Python은 이 분기 산술을 계산한 것으로 U-Boot·Linux·실제 부트 저장장치를 실행하지 않습니다. 실패 횟수를 부팅 초기에 무조건 지우면 반복 실패를 알아보지 못하고, 성공 후에도 남겨 두면 다음 정상 재부팅을 잘못 처리할 수 있습니다.

## 해시 일치와 배포 권한의 차이

해시는 바이트의 지문입니다. 기대한 지문이 신뢰할 수 있을 때 내용이 달라졌는지 대조할 수 있습니다. 그러나 이미지와 기대 지문을 함께 바꿀 수 있는 입력에서 해시 비교만 하면 배포 권한을 확인하지 못합니다. 아래는 서로 다른 짧은 바이트열로 만든 계산 예입니다.

```python
from hashlib import sha256  # from/import는 표준 라이브러리의 SHA-256 함수를 가져옵니다.
old_image, new_image = b"APP-A", b"APP-B"  # b 접두사는 문자열 대신 bytes를 만듭니다.
supplied_digest = sha256(new_image).hexdigest()  # 새 내용에서 지문을 함께 만들어 제공한 상황입니다.
print(old_image != new_image)  # !=는 다름을 비교하며 True입니다.
print(sha256(new_image).hexdigest() == supplied_digest)  # == 비교는 True지만 서명 검사는 아닙니다.
```

MCUboot의 [이미지 형식](https://docs.mcuboot.com/design.html#image-format)은 이미지 해시와 서명 관련 TLV를 구분합니다. TLV는 종류·길이·값으로 자료를 나눈 기록 형식입니다. 실제 제품에서는 신뢰할 키와 서명 검증, 버전 하한 등 정책을 별도로 정합니다. 예전의 유효한 서명 이미지가 항상 현재 정책에서도 허용되는 것은 아닙니다. 해시 계산, 배포자 인증, 이전 버전 거부, 업무상 정상 부팅은 서로 다른 질문입니다.

[중단된 업데이트의 슬롯 선택과 롤백](../../설계와검증사례_engineering-cases/중단된업데이트의슬롯선택과롤백_firmware-ab-update.md)은 파일 기록과 별도 프로세스의 재시작으로 중단 지점을 재현합니다. 파일 시스템 모형의 결과와 실제 flash의 erase/program·전원 상실 조건은 해당 실행 기록에서 구분합니다.

## English

Embedded Linux combines Linux components to fit a device's functions and resources. A working system connects a bootloader, kernel, hardware description, root filesystem, and user programs.

### Boot components

A bootloader such as U-Boot loads the kernel and required data into memory and transfers control. Device Tree is one way to describe hardware to the kernel. Drivers expose devices through operating-system interfaces. The root filesystem contains initialization programs, libraries, commands, and applications.

### Building and porting

Cross-compilation produces code for a target platform different from the development PC. A toolchain includes the compiler, linker, and supporting libraries. A board support package collects code required by a board. Buildroot builds embedded system images; the Yocto Project uses reusable metadata and recipes to construct distributions. BusyBox packages many basic commands into one small executable.

QEMU can test systems using supported board and device models. On physical boards, reading logs separately for power, boot configuration, Device Tree, drivers, and user space helps locate a boot failure.

### Foundation article

- [Embedded Linux: 부팅, Device Tree와 드라이버의 경계](해설_notes/부팅과장치트리및드라이버_boot-devicetree-driver-boundaries.md#english)


### Update completion and boot confirmation

Receiving an image, verifying stored bytes, selecting a trial slot and confirming application health are different milestones. U-Boot's documented `bootcount > bootlimit` branch gives three normal actions followed by an alternate action for a limit of three. A locally executed hash example also shows that changing an image and its supplied digest together can preserve hash equality without authenticating its publisher. The linked A/B file-model case is separate from U-Boot or MCUboot hardware execution.

## 심화 해설 | Advanced article

- [Embedded Linux의 readiness: 바이트를 끝까지 읽는 상태](해설_notes/준비이벤트와레코드_poll-record-streams.md) · [English](해설_notes/준비이벤트와레코드_poll-record-streams.md#english)
