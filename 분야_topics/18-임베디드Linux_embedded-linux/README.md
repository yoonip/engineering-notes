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

- [Embedded Linux: 부팅, Device Tree와 드라이버의 경계](해설_notes/boot-devicetree-driver-boundaries.md)

## English

Embedded Linux combines Linux components to fit a device's functions and resources. A working system connects a bootloader, kernel, hardware description, root filesystem, and user programs.

### Boot components

A bootloader such as U-Boot loads the kernel and required data into memory and transfers control. Device Tree is one way to describe hardware to the kernel. Drivers expose devices through operating-system interfaces. The root filesystem contains initialization programs, libraries, commands, and applications.

### Building and porting

Cross-compilation produces code for a target platform different from the development PC. A toolchain includes the compiler, linker, and supporting libraries. A board support package collects code required by a board. Buildroot builds embedded system images; the Yocto Project uses reusable metadata and recipes to construct distributions. BusyBox packages many basic commands into one small executable.

QEMU can test systems using supported board and device models. On physical boards, reading logs separately for power, boot configuration, Device Tree, drivers, and user space helps locate a boot failure.

### Foundation article

- [Embedded Linux: 부팅, Device Tree와 드라이버의 경계](해설_notes/boot-devicetree-driver-boundaries.md#english)


## 심화 해설 | Advanced article

- [Embedded Linux의 readiness: 바이트를 끝까지 읽는 상태](해설_notes/준비이벤트와레코드_poll-record-streams.md) · [English](해설_notes/준비이벤트와레코드_poll-record-streams.md#english)
