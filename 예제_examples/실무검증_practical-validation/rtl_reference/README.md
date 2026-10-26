# RTL 내적기와 Python 기준 비교 / RTL dot-product reference comparison

실제 SystemVerilog DUT·테스트벤치를 Icarus로 컴파일하고 VVP로 실행합니다. Python 정수·거래 큐의 독립 기대값과 CSV를 비교합니다. Python 표준 라이브러리 외에 Icarus Verilog·VVP가 필요합니다. 실물 FPGA·칩·계측기는 사용하지 않습니다.

## 실행

저장소 루트에서 아직 없는 결과 경로를 지정합니다. Icarus가 PATH에 있으면 자동으로 찾고, 없으면 아래 Windows 경로를 기본값으로 사용합니다.

```shell
python -B 예제_examples/실무검증_practical-validation/rtl_reference/run_compare.py --out /new/path/rtl-run --iverilog C:/iverilog/bin/iverilog.exe --vvp C:/iverilog/bin/vvp.exe
```

다른 환경에서는 `--iverilog`·`--vvp`에 해당 실행 파일을 지정합니다. `--build-root`를 생략하면 새 임시 build 폴더를 만들며 그 경로를 보고서에 남깁니다. Windows 경로 문제를 대조하려면 ASCII인 새 경로를 `--build-root`에 명시할 수 있습니다. 설정별 TEMP/TMP와 build를 분리하고 compile을 순차 실행합니다. build 산출물은 자동 삭제하지 않습니다.

| 파일 | 역할 |
|---|---|
| [dot4.sv](dot4.sv) | signed int8 네 곱의 int32 합과 단일 거래 ready/valid 회로입니다. BUG_MODE 1~5는 의도된 결함입니다. |
| [tb_dot4.sv](tb_dot4.sv) | 하강 에지에서 입력을 구동하고 상승 에지의 nonblocking 갱신 전에 CSV를 기록합니다. |
| [run_compare.py](run_compare.py) | 입력 생성, 정수·거래 기준, 실제 compile·runtime 호출, trace 비교와 결과 보존을 수행합니다. |

계약은 한 번에 한 거래, 수락 에지 n 뒤 n+2부터 출력 전송, 소비될 때까지 출력 유지, reset에서 미소비 거래 취소입니다. 일반적인 모든 ready/valid 설계가 같은 latency·ready 동작을 가져야 한다는 뜻은 아닙니다.

## 결과와 판정

입력 JSON·텍스트, 기대 신호·수락/소비/취소 tag, 도구 버전, 설정별 compile·simulation 명령과 stdout/stderr·CSV·실행 바이너리·불일치가 저장됩니다. 소스·입력·trace의 SHA-256을 기록합니다. compile·simulation 실패를 수치 오류와 합치지 않습니다.

| 전체 CLI 종료 | 의미 |
|---|---|
| 0 | 정상은 PASS, 다섯 의도된 결함은 FAIL이며 소스 hash가 유지됐습니다. |
| 1 | 기대한 정상/결함 대조 중 적어도 하나가 맞지 않습니다. |
| 2 | 기존 결과 경로, 도구·compile·simulation·trace 형식 문제로 차단했습니다. |

288에지에서 정상 불일치 0, 다섯 결함의 불일치 수는 95·2·4·223·8이었습니다. 신호·에지별 수치이므로 서로 독립된 고장 개수가 아닙니다. 최종 소스로 두 번 실행한 결과가 같았습니다. 전체 PASS는 오류 대조의 기대와 일치한 결과이며 모든 DUT 설정이 정상이라는 뜻이 아닙니다.

모든 CSV 필드를 정수로 읽는 제한이 있습니다. X/Z·잘못된 열·짧은 trace·결과 없음은 `INFRA_ERROR`이며, 유효 출력 X/Z의 별도 기능 판정은 구현하지 않았습니다. 합성·formal equivalence·STA·CDC·layout·실물 클록·전력 측정은 실행하지 않았습니다.

- [원리·오류·해결 사례](../../../설계와검증사례_engineering-cases/RTL내적기의비트폭과전송계약_rtl-dot-handshake.md)
- [2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/RTL내적기비교검증_20261021.md)
- [EDA의 단계별 검사](../../../전자컴퓨터공학_ece/35-EDA오픈하드웨어_eda-open-hardware/해설_notes/RTL에서layout까지_rtl-netlist-timing-physical-checks.md)

## English summary

The standard-library runner invokes real Icarus compilation and VVP simulation for six RTL variants. An independent transaction oracle checks signed arithmetic, fixed transfer latency, backpressure and reset cancellation. Unknown or malformed trace data blocks comparison. No synthesis, physical implementation or hardware measurement is claimed.
