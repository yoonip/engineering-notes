# Practical Silicon Lab

펌웨어 시작 코드, JTAG TAP 상태 전이, Linux character device, 검증 결과 판정을 다루는 작은 예제 모음이다. 실행 위치와 필요한 환경에 따라 Python 모델, QEMU 가상 타깃, 물리 보드 참조 코드를 나누었다.

| 폴더 | 내용 | 실행 환경 |
| --- | --- | --- |
| `arm64/` | Assembly 진입 → C → PL011 UART, 정상·오류 이미지 | Linux 빌드 호스트와 QEMU `virt` |
| `jtag/` | 16-state TAP 모델, Cortex-M4 펌웨어, OpenOCD/GDB 설정 | TAP는 Python, 펌웨어 실행은 NUCLEO-F401RE |
| `linux/` | `/dev/valdemo` misc driver와 Python client | 같은 release의 kernel build tree가 있는 Linux |
| `validation/` | 가상 bench, 연산 오류, BER, coverage, 합성 ATE/SLT 결과 | Python 표준 라이브러리 |
| `tests/` | 오프라인 회귀 검사와 장비·장치 mock | Python 표준 라이브러리 |

## 오프라인 테스트

Python 3.10 이상에서 저장소 루트를 기준으로 실행한다. 환경에 따라 `python` 대신 `python3`를 사용한다.

```sh
python -B tests/test_offline.py --report verification.local.json
```

테스트는 임시 폴더에서 모델을 실행하고 종료 코드·정답·오류 분류·자원 정리를 검사한다. USB 프로브, `/dev/valdemo`, 네트워크 계측기에는 연결하지 않는다. PyVISA는 mock으로 대체되므로 설치가 필요 없다. C 컴파일러·QEMU·OpenOCD도 이 테스트에는 필요 없다.

`verification.json`은 이 배포본을 검사한 기록이다. `SOURCE_MANIFEST.json`은 원본에서 가져온 28개 파일의 전후 SHA256과 텍스트 변경 내역을 담는다. `SHA256SUMS`는 자기 자신을 제외한 배포 파일의 SHA256 목록이다.

## 모델을 개별 실행하기

```sh
python -B jtag/tap_walk.py --start Shift-DR --tms 1111101100
python -B validation/check_examples.py
python -B validation/training_ber.py
python -B validation/coverage_account.py
python -B validation/npu.py --fault none --out results/npu-normal
python -B validation/npu.py --fault layout --out results/npu-layout
python -B validation/bench.py --fault none --out results/bench-normal
python -B validation/correlation.py --out results/correlation --with-truth
```

NPU와 bench의 `--out`에는 아직 존재하지 않는 폴더를 지정한다. 정상 NPU의 종료 코드는 0이고, `layout` 오류 주입은 오류를 검출하여 1을 반환한다. Bench는 PASS=0, 기능/한계 실패=1, 통신·파싱 모델 오류=2로 나눈다. 의도한 실패를 검출한 경우와 테스트 프로그램 자체가 실패한 경우는 구별된다.

## 검증 범위

Python 회귀검사의 대상은 모델의 상태 전이, 연산 결과와 오류 판정이다. TAP 모델은 상태 전이를 계산하고, QEMU 예제는 RAM 4개 word의 실행을 확인한다. `linux/valdemo.c`는 외부 하드웨어 없이 driver I/O 경로를 다루는 모듈이다.

물리 보드의 flash·SWD·GPIO, 커널 모듈 삽입, 실제 계측기 통신은 이번 배포 검증에서 실행하지 않았다. 보드와 커널에 필요한 조건·명령은 각 폴더 README에 기록했다. 외부 도구, vendor 소스, 장치 식별 데이터베이스, 컴파일된 파일은 포함하지 않는다.

## English

Small firmware, TAP-state, Linux-driver and validation examples. Run `python -B tests/test_offline.py` for standard-library-only tests. These use synthetic inputs and mocked device/instrument access. Hardware execution and electrical measurements are separate from model results; see each directory for target-specific requirements.
