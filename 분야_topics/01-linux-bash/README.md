# Linux·Bash

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

Linux 커널은 프로세스 실행, 메모리 관리, 파일 접근, 장치 제어를 맡습니다. Ubuntu·Debian·Fedora·Arch Linux 같은 배포판은 이 커널에 패키지 관리 도구와 사용자 프로그램을 묶어 운영체제 환경을 제공합니다. 서버, 임베디드 장치, 개발용 PC, GPU 학습 서버에서 널리 쓰입니다.

## 터미널, 셸, Bash

터미널은 글자로 명령을 입력하고 출력을 보는 창입니다. 셸은 입력을 해석하고 프로그램을 실행하는 명령 처리기이며, Bash는 그중 하나입니다. Zsh도 셸이고, SSH는 원격 컴퓨터에 접속하는 도구입니다. 터미널을 열었다고 해서 항상 Bash가 실행되는 것은 아닙니다.

파이프 `|`는 한 프로그램의 표준 출력을 다음 프로그램의 표준 입력으로 보냅니다. `>`는 출력을 파일에 쓰며 기존 내용을 덮어씁니다. `>>`는 뒤에 덧붙입니다. `2>`는 표준 오류를 따로 저장합니다. 경로에 공백이 있을 수 있으므로 변수로 경로를 넘길 때는 `"$path"`처럼 따옴표를 사용합니다.

```bash
pwd                         # 현재 작업 디렉터리
mkdir -p notes
printf 'voltage,current\n3.3,0.02\n' > notes/data.csv
cat notes/data.csv
find notes -type f -name '*.csv'
```

## 파일과 권한

Linux의 경로는 `/`에서 시작합니다. `/home`은 일반 사용자 데이터, `/etc`는 시스템 설정, `/dev`는 장치 접근, `/proc`는 실행 중인 시스템 정보를 다루는 데 사용됩니다. 읽기·쓰기·실행 권한은 소유자, 그룹, 그 외 사용자로 나뉩니다. 디렉터리의 실행 권한은 그 경로를 통과할 수 있는 권한입니다.

패키지 관리자는 의존성과 설치 파일을 함께 관리합니다. Ubuntu·Debian은 APT, Fedora는 DNF, Arch Linux는 pacman을 사용합니다. 배포판 패키지와 Python의 pip 패키지는 관리 범위가 다릅니다.

## 프로세스와 개발 환경

프로세스는 실행 중인 프로그램이며 PID로 구분됩니다. 환경변수 `PATH`는 실행 파일을 찾는 경로 목록입니다. `ps`·`top`은 프로세스 관찰, `systemd`는 여러 배포판에서 서비스 관리, `tmux`는 터미널 세션 유지, `rsync`는 파일 동기화에 쓰입니다.

Windows에서는 WSL2로 Linux 개발 환경을 구성할 수 있습니다. 실제 장치 접근, USB 디버거, GPU 사용은 WSL과 호스트 드라이버의 지원 조건도 함께 영향을 받습니다. 겉으로 같은 Linux 환경처럼 보여도 배포판, 커널, 드라이버, 패키지 버전에 따라 실행 결과가 달라질 수 있습니다.

## 관련 기술

Ubuntu, Debian, Fedora, Arch Linux, WSL2, Bash, Zsh, systemd, SSH, tmux, rsync

## 참고 자료

- [Linux Kernel documentation](https://docs.kernel.org/)
- [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html)

## 기초 해설

- [Linux에서 프로그램, 권한과 파이프가 만나는 곳](해설_notes/프로세스-권한-파이프_processes-permissions-pipelines.md)

## English

Linux is the kernel that manages processes, memory, file access, and devices. Distributions such as Ubuntu, Debian, Fedora, and Arch Linux combine it with package managers and user programs to provide a complete operating environment. Linux is widely used on servers, embedded devices, development PCs, and GPU training machines.

### Terminal, shell, and Bash

A terminal provides a place to type commands and read their output. A shell interprets those commands and launches programs; Bash and Zsh are two shells. SSH connects to a remote machine. Opening a terminal does not always mean that Bash is running.

A pipe, `|`, sends one program's standard output to the next program's standard input. `>` writes output to a file and replaces its previous contents, while `>>` appends. `2>` redirects standard error. Quoting a path variable as `"$path"` keeps spaces in the path from splitting it into separate arguments. The example above creates a directory, writes a small CSV file, displays it, and searches for CSV files.

### Files and permissions

Linux paths begin at `/`. `/home` holds user data, `/etc` contains system configuration, `/dev` exposes devices, and `/proc` provides information about the running system. Read, write, and execute permissions are assigned separately to the owner, group, and other users. Execute permission on a directory allows traversal through it.

Package managers track installed files and their dependencies. Ubuntu and Debian use APT, Fedora uses DNF, and Arch Linux uses pacman. Distribution packages and Python packages installed with pip belong to different management layers.

### Processes and development environments

A process is a running program identified by a PID. The `PATH` environment variable lists directories searched for executable files. `ps` and `top` help inspect processes, `systemd` manages services on many distributions, `tmux` keeps terminal sessions available, and `rsync` synchronizes files.

WSL2 provides a Linux development environment on Windows. Access to physical devices, USB debuggers, and GPUs also depends on WSL and host driver support. Distribution, kernel, driver, and package versions can affect behavior even when two Linux environments look similar.

### Foundation article

- [Linux에서 프로그램, 권한과 파이프가 만나는 곳](해설_notes/프로세스-권한-파이프_processes-permissions-pipelines.md#english)


## 심화 해설 | Advanced article

- [파이프가 꽉 찼을 때: backpressure와 종료 조건](해설_notes/파이프역압력_pipe-backpressure.md) · [English](해설_notes/파이프역압력_pipe-backpressure.md#english)
