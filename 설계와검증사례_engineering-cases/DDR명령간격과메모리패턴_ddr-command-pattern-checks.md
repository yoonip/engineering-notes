# DDR 명령 간격과 메모리 패턴 | DDR command timing and memory patterns

## 값이 맞는 것과 명령이 적법한 것은 다른 검사입니다

메모리 시험에서 쓴 값과 읽은 값이 같아도 명령 간격을 어겼을 수 있습니다. 반대로 실행 프로그램이 정상 종료했어도 읽기 응답을 전혀 검사하지 않았을 수 있습니다. 이 사례는 ACT·WR·RD·PRE·REF의 간격을 확인하는 감시기와 주소·자료·응답 개수를 확인하는 기준 모델을 함께 실행합니다.

[공개 코드](../예제_examples/실무검증_practical-validation/ddr_validation/README.md)의 SystemVerilog 명령·배열 fixture를 실제 Icarus Verilog로 컴파일하고 실행했습니다. Python은 출력 trace를 읽어 독립적으로 판정합니다. fixture는 비합성 학습 코드이며 실제 DDR controller나 DRAM 소자의 대체품은 아닙니다. [AMD PG150의 PHY Only Interface](https://docs.amd.com/r/en-US/pg150-ultrascale-memory-ip/PHY-Only-Interface)는 transaction을 명령으로 바꾸는 controller와 명령을 전달하는 PHY의 책임을 구별합니다. 여기서는 그중 명령·자료 확인의 일부만 다룹니다.

## bank·row·column을 먼저 구별합니다

bank는 별도로 행을 열 수 있는 메모리 구역, row는 그 구역에서 선택한 행, column은 열린 행 안의 위치입니다. 이 예제는 `2banks × 4rows × 4columns × 16bits`이므로 총 32워드, 64byte입니다. ACT는 행을 열고 WR/RD는 그 행의 열에 접근하며 PRE는 행을 닫습니다. REF는 이 자체 계약에서 두 bank가 닫힌 상태에 발행합니다.

SV는 배열 index를 `bank*16 + row*4 + column`으로 만들지만 Python 기준 모델은 `(bank, row, column)` tuple을 사전 키로 사용합니다. tuple은 여러 값을 순서대로 묶은 변경 불가능한 자료형이고, 사전은 키로 값을 찾는 자료구조입니다. 배열의 잘못된 주소 식을 기준 모델에 그대로 복사하면 같은 실수를 함께 재현할 수 있어 주소 표현을 나누었습니다.

## 시간 수치는 자체 cycle 계약입니다

| 이름 | 확인하는 간격 | 자체 최소값 |
| --- | --- | --- |
| tRCD | ACT 후 같은 bank의 WR/RD까지입니다. | 3cycle |
| tRAS | ACT 후 같은 bank를 PRE하기까지입니다. | 6cycle |
| tRP | PRE 후 같은 bank의 ACT 또는 전체 REF까지입니다. | 2cycle |
| tRFC | REF 후 다음 NOP 이외 명령까지입니다. | 8cycle |
| tWR·tRTP | 마지막 WR·RD 후 같은 bank의 PRE까지입니다. | 각각 2cycle |

AL, additive latency는 명령 처리에 추가하는 지연을 뜻하며 여기서는 0으로 둡니다. RD 응답은 정확히 2cycle 뒤, WR은 배열에 즉시 반영하도록 단순화했습니다. SV의 cycle은 10ns이지만 위 수치는 특정 Micron 부품의 정격이 아닙니다. 실제 부품은 speed grade·동작 조건·burst·CL/CWL·bank group과 다른 명령 간격도 함께 적용합니다. [Micron DDR4 공식 자료 목록](https://www.micron.com/products/memory/dram-components/ddr4-sdram)과 [AMD의 부품 timing 설정 안내](https://docs.amd.com/r/en-US/pg150-ultrascale-memory-ip/Setting-Timing-Parameters-for-DDR4-Non-Custom-Memory-Parts)를 참고하되, 읽지 못한 부품 데이터시트의 수치를 가져오지 않았습니다.

refresh는 저장 정보를 유지하기 위해 주기적으로 수행하는 동작입니다. 이 예제의 엄격한 규칙은 REF 발행 간격 최대 40cycle이며 idle도 셉니다. 실제 규격의 tREFI는 평균 간격과 허용된 postpone/pull-in 조건을 포함할 수 있으므로 이 규칙과 같지 않습니다. 셀의 전하 감소도 모델링하지 않습니다. REF를 빠뜨려도 배열 값은 그대로일 수 있으며 명령 감시기가 그 누락을 검출합니다.

첫 행의 정상 명령은 다음과 같습니다.

| cycle | 명령 | 계산 |
| --- | --- | --- |
| 0 | REF | 다음 명령은 8 이상에서 허용합니다. |
| 8 | ACT bank0 row0 | REF 이후 8cycle을 채웁니다. |
| 11~14 | column0~3 WR | 첫 WR은 `11−8=3`으로 tRCD 경계와 같습니다. |
| 16·18·20·22 | column0~3 RD | 응답은 18·20·22·24에 도착해야 합니다. |
| 26 | PRE | ACT 후 18, 마지막 RD 후 4cycle입니다. |
| 32 | REF | 이전 REF와 간격 32이며 두 bank가 닫혀 있습니다. |

최소값을 검사할 때 `elapsed <= minimum`으로 거절하면 경계와 같은 정상 명령까지 막습니다. 올바른 조건은 `elapsed < minimum`입니다.

```python
if c - activated[bank] < timing["tRCD"]:  # []로 마지막 ACT와 제한을 찾고, 최소값 미만만 거절합니다.
    fail(c, "tRCD", elapsed=c-activated[bank])  # 함수 호출에 실제 경과 cycle을 이름 붙여 넘깁니다.
```

tRCD 오류 표는 첫 WR을 11에서 10으로 옮겨 `10−8=2<3`을 만듭니다. tRAS는 PRE를 9로, tRP는 다음 ACT를 27로, tRFC는 첫 ACT를 7로 옮깁니다. 각각 첫 오류가 cycle 10/9/27/7에 기록됩니다. 두 번째 REF를 지우면 cycle 40까지 허용하고 41에서 deadline을 위반합니다. 이 명령표는 정상과 오류를 직접 만든 fixture이며 실제 장비에서 수집한 실패 명령이 아닙니다.

## 값은 주소와 함께 달라져야 alias를 찾습니다

주소 패턴은 16비트 값 `0xA500 ^ (address*0x101)`입니다. 앞 네 주소의 값은 A500/A401/A702/A603입니다. 먼저 네 column에 모두 쓴 뒤 읽으므로, 서로 다른 주소가 같은 셀에 연결되는 alias를 드러낼 수 있습니다. alias는 별칭이라는 뜻이며 메모리에서는 서로 다른 논리 주소가 같은 저장 위치를 가리키는 오류를 뜻합니다.

stuck bit 0 변이는 쓰기 값의 bit0을 항상 0으로 만듭니다. 주소1에 기대한 A401은 A400으로 바뀌며 cycle 20에서 1bit 불일치를 검출합니다. 32주소 중 bit0이 1인 16주소에서 불일치가 납니다.

column bit1을 지우는 주소 변이는 column0/2, column1/3을 같은 위치로 보냅니다. column2에 A702를 쓸 때 column0의 A500을 덮으므로 cycle 18의 첫 응답이 A702입니다. 값이 구별되는 주소 패턴에서는 16건을 검출하지만, 모든 주소에 0만 쓰면 덮여도 결과가 같아 검출하지 못합니다. write 직후 같은 주소만 바로 read하는 순서 역시 다른 주소의 덮어쓰기를 놓칠 수 있으므로 순서까지 설계해야 합니다.

checkerboard는 0과 1이 교대로 놓인 AA55/55AA 같은 패턴이고, 역패턴은 각 비트를 반전한 값입니다. 정상 회로에 두 순서를 실행해 각 주소가 다른 비트값도 저장하도록 했습니다. 다만 현재 패턴의 선택은 주소 bit0에 달려 있으므로 bit1만 다른 column0/2에는 같은 값이 놓입니다. 따라서 역패턴까지 쓴다는 사실만으로 모든 주소 alias를 검출한다고 결론 내릴 수 없습니다. 이번 실제 결함 대조는 주소 패턴과 전체 0 패턴을 비교한 것입니다.

## 읽기 검사가 사라졌는데 오류 0이라고 쓰면 안 됩니다

Python은 WR에서 원래 값을 저장하고 RD에서 그 시점의 기대값을 확정합니다. 나중의 WR로 바뀐 값을 잘못 기대하지 않도록 RD 발행 시점의 값을 응답 예정표에 넣습니다.

```python
key = (bank, opened[bank], row["col"])     # ()로 bank·열린 row·column을 묶어 독립 주소를 만듭니다.
memory[key] = row["wdata"]                # 사전에 이번 쓰기 값을 저장합니다.
due[c+2] = {"tag": row["tag"], "value": memory.get(key)}  # {}는 사전이며 get은 없는 키에 None을 돌려줍니다.
want = due.pop(c, None)                   # pop은 해당 cycle의 기대 응답을 꺼내고 예정표에서 지웁니다.
```

응답 누락 변이는 RD 32건을 발행해도 `rvalid`를 항상 0으로 출력합니다. 관측값끼리만 비교하는 단순 검사에서는 값 불일치가 0건입니다. 독립 예정표는 정확히 도착해야 할 32응답을 알고 있으므로 `missing_response` 32건으로 실패시킵니다. tag는 거래를 구별하는 번호이며, 값이 같아도 순서가 바뀌면 검출합니다.

첫 WR을 지우는 별도 표에서는 아직 쓰지 않은 셀을 읽습니다. 기준 사전의 `None`과 SV 배열의 X를 초기값 0으로 바꾸지 않고 각각 미초기화·유효 자료 불명확으로 기록합니다. X/Z가 유효 read 자료에 있으면 기능 실패이고, 명령/control에 X가 있거나 trace가 누락·중복·잘못된 열로 수집되면 `INFRA_ERROR`입니다. 후자는 기능을 평가할 증거 자체가 부족한 상태입니다.

## 실행 결과와 해석

| 대조 | 기능 결과 | 불일치 기록 수 |
| --- | --- | --- |
| 정상 주소 패턴·정상 checkerboard/역패턴 | PASS | 각각 0입니다. |
| tRCD / tRAS / tRP / tRFC / REF 누락 | FUNCTIONAL_FAIL | 1 / 17 / 2 / 1 / 1입니다. |
| stuck bit / column alias, 주소 패턴 | FUNCTIONAL_FAIL | 각각 16입니다. |
| 동일 결함, 전체 0 패턴 | PASS | 각각 0이며 이 패턴의 검출 한계입니다. |
| 미초기화 / 응답 누락 / 유효 X | FUNCTIONAL_FAIL | 2 / 32 / 32입니다. |
| 정상 종료하지만 trace 절반 중단 | INFRA_ERROR | 기능 비교 결과를 계산하지 않습니다. |

정상 주소 시험은 256행, WR/RD/응답 각 32건, REF 8건이며 32개의 논리 주소를 초기화합니다. alias 설정에서도 기준 사전은 의도한 논리 주소 32개를 보관합니다. 이 숫자를 실제 서로 다른 물리 셀 32개가 확인됐다는 증거로 쓰지 않습니다. 한 timing 위반 이후 후속 오류도 생기므로 불일치 기록 수는 독립적인 고장 개수나 수율이 아닙니다.

동일 소스를 일반 Python과 `-O`에서 실행했으며 15설정의 입력·trace 해시는 같았습니다. 모든 compile/sim은 종료 0이었지만 기능 결과와 미완성 결과는 표처럼 나뉩니다. 별도 7개 trace 대조는 파일 없음·누락·중복·열 오류·X control·다른 입력 echo·응답 tag 순서 교환을 확인합니다. 실행 파일 누락과 기존 출력 폴더 재사용은 종료 2로 차단했습니다. [명령·해시·검증 기록](검증기록_evidence/DDR명령과패턴검증_20261021.md)에 최종 조건을 남겼습니다.

CPU 캐시에서 반복 읽기가 빠르다는 사실은 DDR 셀을 다시 읽었다는 증거가 아닙니다. cache hit, controller 대기, command timing, PHY margin, 실제 자료 보존은 관측 층이 다릅니다. [AMD의 데이터 오류 분리 절](https://docs.amd.com/r/en-US/pg150-ultrascale-memory-ip/Isolating-the-Data-Error)처럼 주소·bit·패턴·read/write를 나누어 원인을 좁히되, 이 fixture만으로 PCB 결함이나 장치 정격 문제를 판정하지 않습니다.

## 확인 문제

1. ACT가 cycle 8, tRCD가 3이면 cycle 11의 WR은 허용하나요? `11−8=3`이므로 허용합니다. 10의 WR은 2cycle뿐이어서 거절합니다. 실제 시스템은 해당 부품과 AL 등의 조건에 맞는 명령 계약을 사용해야 합니다.
2. 전체 0을 32주소에 쓰고 읽었는데 일치하면 주소선이 정상인가요? 서로 다른 주소가 같은 셀을 가리켜도 값이 모두 0이면 일치합니다. 구별되는 주소 값과 다른 주소의 쓰기 뒤에 읽는 순서가 필요합니다.
3. 값 불일치가 0인데 RD 응답도 0개라면 통과인가요? 아닙니다. 예정한 32응답의 부재를 실패로 기록해야 합니다. 비교한 표본이 없다는 사실과 비교가 모두 일치했다는 사실을 구별합니다.

## English

This case executes a nonsynthesizable SystemVerilog command/array fixture with Icarus and checks its trace using an independent Python timing and transaction oracle. It models two banks, four rows per bank and four sixteen-bit columns. AL is zero. Timing numbers and the strict 40-cycle REF issue deadline are self-defined teaching rules, not device ratings or JEDEC refresh policy.

The monitor checks command state and minimum gaps separately from returned data. Tuple-addressed reference storage avoids copying the fixture's linear address calculation. Expected read values are captured when RD issues, then matched by cycle, tag and value. Missing responses fail even when the number of observed value mismatches is zero.

Address-dependent patterns detect sixteen stuck-bit errors and sixteen column-alias errors. All-zero traffic misses both faults. Checkerboard and its inverse exercise different bit values but do not guarantee detection of aliases between addresses assigned the same pattern. Actual runs include those limited blind spots rather than presenting every PASS as fault-free hardware.

All fifteen compiler/simulator settings exit successfully; functional results include timing/data failures and an intentionally incomplete trace. Normal and optimized Python runs have identical input and trace hashes. The scope excludes physical DDR signaling, bursts, cell retention, training, ECC, cache behavior, board measurements and compliance certification.

## 출처

- [AMD PG150 v1.4, PHY Only Interface](https://docs.amd.com/r/en-US/pg150-ultrascale-memory-ip/PHY-Only-Interface): controller/PHY와 protocol·timing 책임의 차이를 대조했습니다.
- [AMD PG150 v1.4, Setting Timing Parameters for DDR4 Non-Custom Memory Parts](https://docs.amd.com/r/en-US/pg150-ultrascale-memory-ip/Setting-Timing-Parameters-for-DDR4-Non-Custom-Memory-Parts): tREFI/tRFC 설정의 단위와 값 확인 책임을 읽었습니다. 본문의 cycle 숫자는 자체 계약입니다.
- [AMD PG150 v1.4, Isolating the Data Error](https://docs.amd.com/r/en-US/pg150-ultrascale-memory-ip/Isolating-the-Data-Error): 기대값·관측값, bit·주소·패턴·read/write 구분을 읽었습니다. 문서 표시일은 2025-12-03입니다.
- [Micron DDR4 SDRAM 공식 페이지](https://www.micron.com/products/memory/dram-components/ddr4-sdram): 제품·자료 목록을 확인했습니다. 연결된 TN-40-40은 접근 페이지로 이동해 PDF 본문을 읽지 못했으므로 timing 근거로 사용하지 않았습니다. 출처 확인일은 2026-10-21입니다.
