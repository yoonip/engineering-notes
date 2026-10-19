# Linux에서 프로그램, 권한과 파이프가 만나는 곳

[Linux & Bash](../README.md) · [실행 모형](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 명령 한 줄에도 실행 주체가 있다

터미널은 명령을 입력하고 출력을 보는 창이며, Bash는 그 명령을 해석하는 셸이다. 프로그램 파일과 실행 중인 프로세스도 구분한다. 같은 Python 파일을 두 번 실행하면 별도의 프로세스와 메모리 상태가 생길 수 있다. 프로세스에는 PID, 주소 공간, 환경 변수, 현재 디렉터리와 열린 파일들이 있다.

Linux의 `fork()`는 자식 프로세스를 만들고, `execve()` 계열은 현재 프로세스의 실행 이미지를 다른 프로그램으로 바꾼다. 모든 셸 실행이 반드시 이 두 호출의 단순 조합인 것은 아니다. 중요한 점은 메모리와 파일의 관계가 다르다는 것이다. `fork()` 후 일반적인 사적 메모리 변경은 서로 분리되지만, 상속된 파일 디스크립터가 같은 열린 파일 기술을 가리키면 파일 위치를 공유할 수 있다. [Linux fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html)

### 권한은 비트와 경로를 함께 읽는다

일반 권한은 소유자·그룹·기타의 `rwx` 세 묶음이다. `640`은 소유자 읽기·쓰기, 그룹 읽기, 기타 없음이다. 소유자에게 해당하면 그룹 권한이 더 넓더라도 그쪽으로 다시 판정하지 않는다. [GNU 권한 구조](https://www.gnu.org/software/coreutils/manual/html_node/Mode-Structure.html)

| 대상 | 읽기 r | 쓰기 w | 실행·탐색 x |
| --- | --- | --- | --- |
| 일반 파일 | 내용 읽기 | 내용 변경 | 실행 허용의 한 조건 |
| 디렉터리 | 이름 목록 읽기 | 항목 추가·삭제의 한 조건 | 경로 구성요소 탐색 |

파일을 읽으려면 상위 디렉터리의 탐색 권한도 필요하다. 파일 삭제는 일반적으로 파일 자체의 쓰기 비트가 아니라 부모 디렉터리의 권한과 관계된다. ACL, sticky bit, capabilities, 마운트 옵션과 보안 정책도 판정에 영향을 줄 수 있다. 따라서 `rwx`만으로 모든 접근 결과를 예측하지 않는다. [Linux 경로 해석](https://man7.org/linux/man-pages/man7/path_resolution.7.html)

### 파이프는 메모리를 공유하는 선이 아니다

`producer | consumer`는 앞 명령의 표준출력을 뒤 명령의 표준입력으로 연결한다. 표준에러는 별도 리다이렉션이 없으면 함께 연결되지 않는다. 파이프는 유한 버퍼를 가진 바이트 스트림이며 쓰기 호출마다 메시지 경계를 보존하지 않는다. 버퍼가 가득 차면 쓰기가 기다릴 수 있고, 모든 쓰기 끝이 닫혀야 읽는 쪽에서 EOF를 확인할 수 있다. 읽는 쪽이 모두 사라졌을 때의 쓰기는 SIGPIPE 또는 EPIPE와 관련된다. 작은 쓰기의 원자성 한계인 `PIPE_BUF`와 파이프 전체 용량도 다른 개념이다. [Linux pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html)

오류 처리도 연결해야 한다. Bash 파이프라인은 기본적으로 마지막 명령의 상태를 사용한다. `pipefail`을 켜면 실패한 명령 중 가장 오른쪽의 종료 상태를 사용하며, 전부 성공하면 0이다. [Bash Pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)

```bash
# Bash에서 앞 명령의 실패가 가려지는지 확인한다.
false | cat
printf '%s\n' "$?"
set -o pipefail
false | cat
printf '%s\n' "$?"
```

앞 두 줄의 상태는 0, `pipefail` 이후 상태는 1이 된다. 다만 `grep`의 검색 결과 없음이나 `head`가 일찍 닫은 파이프는 작업 목적에 따라 예상된 종료일 수도 있다. 모든 0이 아닌 상태를 똑같은 장애로 묶기보다 각 프로그램의 종료 규약을 읽는다.

### 구현과 검증의 범위

예제의 `unix_mode_allows`는 일반 `rwx`의 주체 선택을, `pipeline_status`는 Bash 종료 상태 규칙을 모형화한다. 테스트는 512개 권한 조합과 요구 비트를 대조하고 앞 단계의 실패가 가려지는 경우를 확인한다. 실제 파일 접근이나 Linux 프로세스를 에뮬레이션하는 모형은 아니다. 위 Bash 명령의 실제 확인에는 Bash와 `cat`이 필요하며, Windows에서 실행한 Python 테스트가 Linux 권한·신호의 실측 결과를 대신하지 않는다.

## English

### A command has an execution context

A terminal provides input and output; Bash interprets commands. A program file differs from a running process. Two executions of one Python file can have separate processes and memory. A process has a PID, address space, environment, working directory, and open files.

Linux `fork()` creates a child, while the `execve()` family replaces the current process image. Shell execution need not always be a simple pair of those calls. Private memory changes after a fork are normally separate, but inherited descriptors can refer to the same open file description and therefore share a file offset. [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html)

### Read permission bits and the path together

Ordinary permissions contain owner, group, and other `rwx` sets. Mode `640` grants owner read/write, group read, and no other permissions. An owner does not fall through to more generous group bits. [GNU mode structure](https://www.gnu.org/software/coreutils/manual/html_node/Mode-Structure.html)

For a regular file, the bits concern reading content, changing content, and one condition for execution. For a directory, they concern listing names, modifying entries, and traversing the path. Reading a file also requires traversal of its parent path. Deleting a file generally depends on its parent directory rather than the file's own write bit. ACLs, sticky bits, capabilities, mount options, and security policy can affect the result, so ordinary mode bits are not a complete access-control simulator. [Path resolution](https://man7.org/linux/man-pages/man7/path_resolution.7.html)

### A pipe is a bounded byte stream

`producer | consumer` connects standard output to standard input, leaving standard error separate unless redirected. The pipe has finite capacity and does not preserve a message boundary for each write call. A full buffer can block a writer. EOF requires all write ends to close; writing with no readers relates to SIGPIPE or EPIPE. The small-write atomicity bound `PIPE_BUF` differs from total pipe capacity. [pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html)

By default Bash reports the last command's pipeline status. With `pipefail`, it reports the rightmost failed command's status, or zero if none failed. The Bash example first produces status zero for `false | cat`, then one after enabling `pipefail`. [Bash pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)

Nonzero status still needs context: an unsuccessful `grep` search or an upstream SIGPIPE after `head` closes early can be expected for a particular task. Interpret each program's exit contract.

### Model and verification

`unix_mode_allows` models only ordinary permission-class selection, and `pipeline_status` models pipeline status selection. Tests cross-check all 512 modes and requested bit sets and cover hidden upstream failure. These are not Linux process or filesystem emulators. Actual execution of the shell example requires Bash and `cat`; the portable Python tests do not measure Linux permissions or signals.

## 출처 / Sources

Linux man-pages의 프로세스·경로·파이프 규약을 GNU Bash·Coreutils의 셸·권한 규칙과 대조했다. / Linux process, path, and pipe contracts were checked against GNU shell and permission rules. 확인 / checked: 2026-10-19.
