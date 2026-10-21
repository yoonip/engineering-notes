# 읽기 교란의 징후와 데이터 이동 / Read-disturb indicators and data relocation

[실행 코드](../예제_examples/실무검증_practical-validation/nand_management/README.md) · [불량 블록과 마모 분산](NAND의불량블록과마모분산_nand-bad-block-wear.md) · [실행 기록](검증기록_evidence/NAND블록과교란모델검사_20261021.md)

## 1. 읽기만 하는 자료도 관리해야 합니다

읽기 교란(read disturb)은 반복 읽기가 같은 블록의 읽지 않은 셀 상태에도 영향을 주는 현상입니다. 쓰지 않는 cold 자료가 언제까지나 안전하다고 볼 수 없는 이유입니다. Micron의 NAND FAQ는 반복 읽기와 자료 refresh를 설명합니다. Cai 등의 연구 초록은 읽기 횟수뿐 아니라 P/E 이력과 보존 시간도 영향을 준다고 구분합니다. 해당 연구의 구체적인 대상은 2Y-nm MLC이며 그 결과를 모든 최신 NAND의 한계값으로 옮기지 않습니다. [Micron FAQ](https://www.micron.com/sales-support/sales/faqs), [Cai 외, arXiv:1805.03283v1의 초록](https://arxiv.org/abs/1805.03283)

이 글의 프로그램은 물리 오류를 만들어 내는 시뮬레이터가 아닙니다. 읽기 횟수와 이미 해석된 ECC 관측값을 받아 ‘계속 사용·이동 시도·자료 공개 중단’을 구분하는 합성 정책 모델입니다. 전압·온도·셀 상태·raw 오류율·ECC 계산·실물 NAND·MTD 드라이버를 실행하지 않았습니다. 같은 ECC 징후만으로 읽기 교란인지 retention·마모 등 다른 원인인지를 확정하지 않습니다.

## 2. 합계·최댓값·오류 상태를 구분합니다

CE는 정정 가능하다고 들어온 읽기 결과, UE는 신뢰할 수 있는 자료를 얻지 못했다고 들어온 결과입니다. 실제 Linux UBI도 정정된 bit flip과 자료 무결성 오류의 반환을 나눕니다. 이 모델의 문자열 CE/UE가 커널 반환 코드와 일대일 대응하는 raw decoder는 아닙니다. [Linux v6.12 io.c의 ubi_io_read 설명, 86–106행](https://raw.githubusercontent.com/torvalds/linux/v6.12/drivers/mtd/ubi/io.c)

| 모델 변수 | 뜻 | 이번 입력의 정책 |
|---|---|---|
| reads | 해당 물리 블록에서 수행한 페이지 읽기 합계입니다. | 4회 이상이면 이동을 검토합니다. |
| corrected_max | 이 블록의 한 읽기에서 입력받은 정정 비트 수의 최댓값입니다. | 2 이상이면 이동을 검토합니다. |
| unreadable | UE 관측 뒤 그 블록의 자료 공개를 막는 표시입니다. | 후속 읽기에도 유지합니다. |

읽기 4회와 CE 2는 짧은 반례를 위한 자체 숫자입니다. 지원하는 corrected 입력 범위 0~8도 부품의 ECC 정정 강도를 주장하는 값이 아닙니다. CE를 실제 bit flip으로 변환하거나 읽기 횟수가 어떤 확률로 UE를 만든다고 계산하지 않습니다. 행별 pass 전압·선택/비선택 페이지의 비대칭도 모델에 없습니다.

고정 입력은 논리 블록 0→물리 블록 0에 `cafebabe`·`11223344`를 놓습니다. 같은 첫 페이지를 네 번 읽었을 때 자료는 계속 같지만 `scrub_due`는 false·false·false·true입니다. 다른 실행에서는 첫 읽기에 corrected=2를 넣어 읽기 횟수 1에서도 due=true가 됩니다. 개수와 ECC 징후를 독립된 입력으로 다루는 대조입니다.

```python
reads = 0                                      # =는 누적 읽기 수의 시작값을 대입합니다.
corrected_max = 0                              # 정정 비트 수의 합계 대신 최댓값을 저장합니다.
for corrected in [0, 1, 0, 2]:                 # for는 리스트의 관측값을 차례대로 꺼냅니다.
    reads += 1                                # +=는 읽기 합계를 1 늘립니다.
    corrected_max = max(corrected_max, corrected)  # max는 이전·이번 값 중 큰 값을 남깁니다.
    due = reads >= 4 or corrected_max >= 2      # >=는 이상 비교, or는 둘 중 하나가 참인 조건입니다.
```

정책의 누적 방식을 설명하는 별도 예입니다. 최종 `reads=4`, `corrected_max=2`이며 정정 입력의 합 3과 구분됩니다. 실제 fixture는 위에서 설명한 두 경로를 별도로 검사합니다. `due()`는 이동 필요 여부만 알려 주고 자동으로 이동하지 않습니다. 예제 호출자가 `scrub()`을 실행합니다. 백그라운드 작업 큐·동시 호스트 I/O·시간 제한은 없습니다.

## 3. 정정 가능한 동안 이동합니다

scrub은 읽은 자료를 다른 위치로 옮겨 관리하는 작업입니다. 단순히 ECC 숫자만 0으로 지우거나 같은 위치에 다시 쓰는 동작이 아닙니다. Linux UBI에서도 scrub을 마모 이동과 같은 worker로 처리하는 설명이 있습니다. 이 모델은 필요한 원리만 동기 함수로 좁혔습니다. [Linux v6.12 wl.c의 1274–1331행](https://raw.githubusercontent.com/torvalds/linux/v6.12/drivers/mtd/ubi/wl.c)

정상 이동은 다음 순서로 실행됩니다.

1. 원본의 두 페이지를 읽습니다. CE 자료는 이미 정정되어 있다는 입력 계약을 사용합니다.
2. GOOD이며 소거된 free 블록 1에 두 페이지를 씁니다.
3. 목적지 두 페이지를 다시 읽어 복사 자료와 비교합니다.
4. 두 페이지가 맞으면 논리 블록 0의 매핑을 0→1로 바꿉니다.
5. 옛 블록 0을 소거해 free pool로 돌립니다.

이 실행에서 복사한 자료량은 `2×4=8바이트`, program 시도량도 8바이트, 옛 블록의 성공 erase는 1회입니다. 새 목적지의 reads는 0이 아니라 2입니다. 검증 읽기도 실제 모델의 읽기 경로를 거치기 때문입니다. 따라서 임계값 4를 그대로 적용하면 그 위치를 추가 두 번 읽을 때 다시 due가 될 수 있습니다. 이 작은 숫자로 잦은 이동 비용까지 드러내며 실제 제품 정책으로 추천하지 않습니다.

대상 블록의 corrected_max=0은 새 위치의 검증 결과를 OK로 고정했기 때문입니다. 전하 상태가 얼마나 회복되었는지를 계산한 결과가 아닙니다. 원본 CE 입력도 바이트 배열을 실제 손상시키지 않고 이미 정정된 자료를 돌려줍니다. ECC가 오정정하거나 상위 검사값이 필요한 상황은 이 모델 밖입니다.

## 4. 이동 실패에서 원본을 지우지 않습니다

각 실패는 새 모델에서 CE 입력으로 due를 만든 뒤 넣습니다. 모두 같은 입력 자료를 사용하되 실패 지점과 공개 결과를 나눕니다.

| 주입 지점 | 실행 결과 | 매핑·원본·공개 자료 |
|---|---|---|
| 원본 두 번째 페이지 UE | SOURCE_UE입니다. | 매핑 0, 원본 erase 0회, 반환 자료는 두 페이지 모두 None입니다. |
| 목적지 두 번째 페이지 program | DEST_PROGRAM_FAILED입니다. | 목적지 1 격리, 매핑 0 유지, 원본 두 값이 정상 경로에서 읽힙니다. |
| 목적지 검증 | DEST_VERIFY_FAILED입니다. | 목적지 1 격리, 매핑 0 유지, 원본 두 값이 유지됩니다. |
| 새 매핑 공개 뒤 옛 블록 erase | MAPPED·ERASE_FAILED_RETIRED입니다. | 매핑 1을 유지하며 옛 0은 재사용하지 않습니다. |

UE가 들어오면 이 정책은 해당 물리 블록 전체의 자료 공개를 막습니다. 실제 ECC 오류는 페이지·codeword 등 다른 단위일 수 있으므로 모든 페이지가 물리적으로 손상됐다는 뜻으로 읽지 않습니다. 보수적인 관리 표시이며 다른 페이지의 실제 상태를 진단한 것은 아닙니다.

UE 경로에서 원본 배열이 바뀌지 않았고 소거도 하지 않았다는 검사를 합니다. 이것은 복구 가능성의 증명이 아닙니다. 이미 신뢰할 수 없는 읽기이므로 알려진 입력 배열을 그대로 갖고 있어도 호스트 반환값은 None입니다. 백업·중복 복사본·장치별 read retry·오프라인 분석을 통한 복구는 구현하지 않습니다. `publish-ue` 변이는 이 금지를 깨고 바이트를 반환하므로 검사가 발견합니다.

## 5. 같은 free pool을 쓰는 정책들의 비용

불량 블록 retire, 정적 마모 이동, scrub은 모두 사용 가능한 목적지가 필요합니다. 실패 목적지를 free에 다시 넣으면 문제가 반복되고, 여유 블록이 없는데 원본부터 지우면 자료를 잃을 수 있습니다. 이번 모델은 NO_FREE_BLOCK으로 중단하며 매핑과 프로그램 자료를 바꾸지 않습니다. scrub을 시도하며 읽기 계수는 늘 수 있으므로 모든 내부 카운터가 불변이라고 주장하지 않습니다.

마모 분산 사례에서는 호스트 32바이트에 정적 이동 8바이트를 더해 비율 1.25를 계산했습니다. 이번 scrub만 하는 비교 창에는 host_bytes=0이고 move_bytes=8입니다. `8/0`으로 WAF를 계산하지 않습니다. 복사 프로그램량 8바이트·추가 읽기·소거 1회를 따로 적는 편이 의미가 있습니다. 목적지 실패 시 발행한 program 시도량도 남지만 실제 셀에 반영된 양은 알 수 없는 모델 경계입니다.

실무 기록에서도 자료 공개 여부, 원본/목적지, 매핑 변경 여부, 상태 오류, free 블록 수, 이동 자료량을 나누면 원인을 좁히는 데 도움이 됩니다. 이 실습 JSON은 그 항목의 고정 사례이며 실물 장비의 수명·고장 확률·복구 성공률을 측정한 로그가 아닙니다.

## 6. 확인 결과와 확인 문제

일반·`-O` 실행에서 읽기 횟수 경로, CE 경로, UE 비공개, 네 이동 오류의 매핑·블록 상태·free pool이 직접 적은 기대값과 같았습니다. 임계값 무시·성급한 매핑·UE 공개를 포함한 오류 변이 5종은 두 모드 모두 실패로 검출됐습니다. 상세 명령·SHA-256·종료값은 연결한 실행 기록에 있습니다.

1. CE가 나왔으므로 읽기 교란이 원인이라고 확정할 수 있나요? 답: 아닙니다. CE는 관측된 정정 상태이며 여러 원인과 조건을 따로 조사해야 합니다.
2. 성공 scrub 뒤 읽기 계수는 반드시 0인가요? 답: 이 모델에서는 목적지 검증 읽기 2회가 남습니다.
3. 목적지 검증 실패 시 원본을 먼저 소거하면 다시 복사할 수 있나요? 답: 원본이 사라질 수 있습니다. 이 정책은 검증 전 매핑·원본을 유지합니다.

## English

The exercise consumes externally supplied corrected-error and UE telemetry. It does not generate physical read-disturb errors, run an ECC decoder or measure a universal threshold. Four block-level page reads or a maximum corrected count of two trigger the chosen policy. These are teaching values. A due flag requests consideration of a synchronous scrub; it does not automatically schedule background work.

A successful scrub reads the two source pages, programs and verifies a free destination, publishes the new mapping, then erases the old block. Destination verification leaves two reads on the new block. Source UE withholds data and prevents relocation; destination program/verification failures retain the old mapping and source array. Preserving that array is not evidence that UE data is recoverable. Old-block erase failure after publication retires the old block while retaining the verified destination. Scrub-only traffic has zero host-write bytes, so the example reports copy/read/erase work rather than dividing by zero for WAF.

## 출처

- [Micron NAND FAQ](https://www.micron.com/sales-support/sales/faqs): READ DISTURB·refresh와 ECC 요구의 부품별 차이를 읽었습니다.
- [Cai 외, Read Disturb Errors in MLC NAND Flash Memory](https://arxiv.org/abs/1805.03283), arXiv v1, 2018-05-08: DSN 2015 연구를 요약한 초록의 현상·대상·영향 인자를 확인했습니다. 논문 전체 실험을 재현하거나 수치 곡선을 가져오지 않았습니다.
- [Linux v6.12 io.c](https://raw.githubusercontent.com/torvalds/linux/v6.12/drivers/mtd/ubi/io.c): 86–106행의 정상·정정 bit flip·무결성 오류 구분과 146–161행을 읽었습니다.
- [Linux v6.12 wl.c](https://raw.githubusercontent.com/torvalds/linux/v6.12/drivers/mtd/ubi/wl.c): 7–83행의 마모·scrub·오류 상태와 1274–1331행의 scrub 요청을 읽었습니다. 보호 큐·thread·동시성·on-flash 형식을 구현하지 않았습니다. 확인일은 2026-10-21입니다.
