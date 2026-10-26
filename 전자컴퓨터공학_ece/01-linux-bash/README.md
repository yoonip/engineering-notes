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

## 파일시스템의 구조와 파일 내용을 따로 확인합니다

파일 경로는 이름→inode→데이터 블록으로 이어집니다. inode는 길이와 저장 위치를 담는 관리 레코드이며, 할당 bitmap은 사용 중인 저장 구간을 표시합니다. 이름이 없어진 파일, 길이와 블록 용량이 다른 파일, 서로 다른 파일의 블록 충돌은 각각 다른 문제입니다. 실제 파일시스템마다 허용 기능과 복구 정책도 다릅니다.

[이미지 검사 실습](../../예제_examples/실무검증_practical-validation/filesystem_repair/README.md)은 새 호스트 파일에 자체 EDUFS1 JSON을 기록합니다. 실제 mount·ext4·e2fsck는 실행하지 않습니다. 손상 원본은 읽기만 하고, 원본/외부 목록 SHA에 묶인 계획을 새 사본에 적용한 뒤 다시 검사합니다. 블록 8바이트 두 개가 있어도 파일 길이는 10바이트일 수 있습니다. 길이를 용량 16으로 바꾸는 것만으로 원문을 복구한 것은 아닙니다.

```python
from pathlib import Path  # from/import는 파일 경로 객체를 가져옵니다.
import json  # json은 저장한 계획의 문자열을 사전으로 읽습니다.
def planned_actions(plan_path):  # def는 계획 파일 경로를 받는 함수를 정의합니다.
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))  # UTF-8 파일을 읽어 JSON을 해석합니다.
    return plan["status"], len(plan["actions"])  # []로 상태를 읽고 len으로 동작 수를 셉니다.
```

정상 실습 출력의 metadata_damage/plan.json을 읽으면 `('READY', 4)`입니다. 끊어진 항목 제거·근거 있는 크기 정정·이름 참조 수 정정·누락 할당 비트 설정의 네 동작입니다. 복구 사본은 seed와 bytes가 같고 두 번째 계획은 비어 있습니다. [검사와 복구 계획](../../설계와검증사례_engineering-cases/파일시스템의손상검사와복구계획_filesystem-check-repair.md)에 원인과 실제 명령을 연결했습니다.

[이름과 블록 소유권 사례](../../설계와검증사례_engineering-cases/파일이름과블록소유권의복구_filesystem-orphans-block-ownership.md)에서는 두 이름이 같은 inode를 가리키는 hard link와 다른 inode가 같은 데이터 블록을 가리키는 충돌을 구분합니다. 이름을 잃은 일반 파일은 새 이름으로 연결할 수 있지만 옛 이름까지 알게 된 것은 아닙니다. 내용이 사라진 파일은 metadata나 digest만으로 되살리지 않습니다. 외부 목록 없이 구조만 맞으면 원래 자료의 동일성은 NOT_ESTABLISHED입니다.

[e2fsck 공식 매뉴얼](https://man7.org/linux/man-pages/man8/e2fsck.8.html)은 읽기 전용 모드와 수정·미수정 오류의 종료값을 구분합니다. 이 자체 예제의 CHECKED·종료 0도 명령이 처리됐다는 뜻이므로 structural/identity 결과를 별도로 읽습니다. 실제 장치 검사나 전원 오류 내구성을 확인한 실습은 아닙니다.

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


### Filesystem structure and historical content

Names reference inodes, and inode block lists locate logical content. The separate EDUFS1 host-file example checks those relations, allocation bits and an external content inventory. A read-only plan binds input hashes and writes only a new repaired copy. Reading metadata_damage/plan.json returns `('READY', 4)`; the repaired bytes equal the seed and a second repair has no changes.

The companion case distinguishes valid hard links from conflicting block owners. A new salvage name preserves an intact unreachable file without reconstructing its old name. Consistent metadata and checksums can coexist with changed or missing historical bytes; an external digest detects a mismatch but supplies no backup payload. No mounted disk, ext4, e2fsck or hardware power-loss test is executed.

## 심화 해설 | Advanced article

- [파이프가 꽉 찼을 때: backpressure와 종료 조건](해설_notes/파이프역압력_pipe-backpressure.md) · [English](해설_notes/파이프역압력_pipe-backpressure.md#english)
