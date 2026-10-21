# 비동기 FIFO의 포인터와 reset | Asynchronous FIFO pointers and reset

서로 다른 write/read 클록으로 동작하는 깊이 4·32비트 FIFO를 Icarus Verilog로 컴파일하고 실행합니다. Python `deque`는 수락된 거래의 순서를 따로 추적합니다. 정상 회로와 의도적으로 만든 세 기능 결함을 같은 입력으로 대조합니다.

| 파일 | 역할 |
| --- | --- |
| [async_fifo.sv](async_fifo.sv) | binary/Gray 포인터, 양방향 2단 포인터 동기화, 도메인별 full/empty, 두 도메인의 flush reset입니다. |
| [tb_async_fifo.sv](tb_async_fifo.sv) | 10/14ns 클록, 하강 edge 입력 구동, reset 요청, 상승 edge의 NBA 갱신 전 trace를 생성합니다. |
| [run_compare.py](run_compare.py) | 실제 compile/sim, 독립 거래 큐, 포인터·동기화·reset 성질, 오류 trace 대조, 해시와 종료 상태를 기록합니다. |

## 실행

Python 3.10 이상 표준 라이브러리와 Icarus Verilog가 필요합니다. 이번 실행 환경은 Python 3.12.14, Icarus 12.0 devel입니다. 아래 명령은 저장소 루트의 PowerShell에서 실행합니다. `python`에는 실제 Python 실행 파일 경로를 사용할 수 있습니다.

```powershell
python '예제_examples/실무검증_practical-validation/cdc_async_fifo/run_compare.py' `
  --out 'tmp/cdc-fifo-run-1' `
  --iverilog 'C:/iverilog/bin/iverilog.exe' `
  --vvp 'C:/iverilog/bin/vvp.exe' `
  --build-root 'C:/temp/cdc-fifo-build'
```

`--out`은 새 폴더여야 합니다. 이미 있는 폴더는 종료 코드 2로 거절합니다. compiler/runtime을 PATH에서 찾을 수 있다면 두 도구 옵션을 생략할 수 있습니다. Linux에서는 `--build-root /tmp/cdc-fifo-build`와 같은 경로를 사용합니다. 소스와 입력 파일을 별도 build 폴더에 복사한 후 상대 파일명으로 차례대로 컴파일하며, 자식 프로세스의 `TEMP`와 `TMP`도 그 build 폴더로 지정합니다.

| RTL 설정 | 로컬 결과 | 의미 |
| --- | --- | --- |
| correct | PASS, 불일치 0 | 64건 쓰기 수락, 58건 읽기, reset 취소 6건입니다. |
| full_one_bit | FUNCTIONAL_FAIL, 160건 | Gray full 비교의 상위 두 비트 중 하나만 반전합니다. |
| read_empty | FUNCTIONAL_FAIL, 66건 | empty gate를 무시하여 읽기 포인터를 잘못 전진시킵니다. |
| one_sided_reset | FUNCTIONAL_FAIL, 27건 | write reset 요청을 read 도메인에 전달하지 않습니다. |

네 설정 모두 실제 compile/sim의 종료 코드는 0입니다. 회귀 명령의 최종 `PASS`는 정상 일치와 세 결함 검출이 예상대로 이루어졌다는 뜻입니다. 결함 회로가 기능 시험을 통과했다는 뜻으로 읽지 않습니다. 정상/기능 결과가 예상과 다르면 종료 1, 도구·실행·trace 수집이 실패하면 종료 2입니다.

## 결과와 계약

- `inputs.json`에는 입력값·클록·reset 구간을 저장합니다. `report.json`에는 환경, 명령, 종료 코드, 표준 출력/오류, 소스·입력·trace SHA256, 수락·읽기·취소 자료와 오류 이유가 들어갑니다.
- 각 설정 폴더에는 `trace.csv`, 실제 구동 파일, `sim.vvp`, `result.json`이 있습니다. `checker-controls`는 누락·중복 edge, 열 오류, X control, 다른 입력 echo, 유효 자료 X와 잘못된 값의 거절을 별도로 시험합니다.
- 한 시각의 read/write는 모두 NBA 갱신 전을 관측합니다. 큐 비교에서는 read를 먼저 처리하므로 같은 시각에 새로 쓴 값을 즉시 읽는 bypass를 허용하지 않습니다.
- 포인터는 3비트이고 주소는 하위 2비트입니다. full/empty가 실제 큐 점유량과 즉시 같을 필요는 없습니다. 상대 포인터의 전달 지연에 따른 보수적 대기를 허용합니다.
- 어느 reset 요청이든 정상 설정에서는 양쪽 포인터·동기화기·flags를 함께 비웁니다. 비동기 assert 후 각 도메인 두 상승 edge에서 release를 진행하고 그 다음 edge부터 회로가 연산합니다. 메모리 배열 자체는 지우지 않습니다.
- 알 수 없는 control/pointer, trace 누락·중복·형식 오류는 `INFRA_ERROR`입니다. 수락된 read 자료의 X/Z는 `FUNCTIONAL_FAIL`입니다. 수락하지 않은 read 자료는 검사 대상이 아닙니다.

이 예제는 고정 깊이·클록 조건의 디지털 기능 시험입니다. 비동기 읽기 배열의 실제 RAM 추론, metastability, MTBF, 배치·배선, pointer bit skew, STA 및 CDC signoff는 실행하지 않았습니다. binary 포인터 전송이나 동기화기 제거가 이상적인 디지털 시뮬레이션에서 반드시 실패한다고 가정하지 않습니다.

[원리와 오류 흐름](../../../설계와검증사례_engineering-cases/비동기FIFO의Gray포인터와reset_cdc-async-fifo.md) · [검증 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/비동기FIFO비교검증_20261021.md)

## English

The depth-four, 32-bit DUT has separate 10ns write and 14ns read clocks. Actual Icarus compilation and simulation produce traces checked against a transaction `deque`, not a second pointer-based FIFO. The correct design accepts 64 writes, delivers 58 reads, and flushes six queued values. Three controlled defects fail: an incorrect Gray full comparison, reads that ignore empty, and a reset request applied only to the writer.

Local full/empty flags may remain conservative while remote pointers cross two synchronizer stages. Any reset request flushes both domains; reset asserts asynchronously and releases locally through two stages. Tests cover this functional contract, not analog metastability, physical timing, CDC signoff, or FPGA measurements. See the linked case and evidence for the source provenance and exact observations.
