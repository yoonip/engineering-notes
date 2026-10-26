# PCIe의 태그와 분할 응답 / PCIe tags and split completions

PCIe Memory Read의 첫 응답이 왔다고 요청 전체가 끝난 것은 아닙니다. 요청별 tag를 유지하고, 조각마다 남은 바이트 수와 시작 주소를 확인해야 합니다. 이 사례는 해독된 Completion 필드를 입력하는 Python 호스트 모델이며 PCIe root port·endpoint·FPGA IP·DMA·TLP 원시 비트열은 실행하지 않았습니다.

[코드·입력·실행 안내](../예제_examples/실무검증_practical-validation/usb_pcie/README.md) · [실행 기록](검증기록_evidence/USB와PCIe전송계약검증_20261021.md) · [MMIO·DMA 해설](../전자컴퓨터공학_ece/17-펌웨어-RTOS_firmware-rtos/해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md)

## 1. 요청 번호와 돌아온 조각을 연결합니다

Requester는 읽기를 요청하는 쪽, Completer는 그 데이터를 응답하는 쪽입니다. Completion은 요청의 결과를 알려 주는 응답이며 데이터가 포함되면 CplD라고 부릅니다. tag는 미완료 요청을 식별하는 번호입니다. 여러 요청이 동시에 있으면 응답 도착 순서만으로 원래 요청을 고를 수 없습니다.

AMD PG346 3.3의 Completer Memory Read Operation은 서로 다른 요청의 응답은 다른 순서로 올 수 있고, 같은 요청의 Split Completions는 순서를 유지한다고 설명합니다. Descriptor의 Byte Count는 현재 조각을 포함해 아직 돌려줄 바이트 수, Lower Address는 현재 조각의 시작 byte address 하위 7비트입니다. [PG346 Memory Read](https://docs.amd.com/r/3.3-English/pg346-cpm-pcie/Completer-Memory-Read-Operation?contentId=HESS8S8G5krVslhhZyT87w), [Completion descriptor](https://docs.amd.com/r/3.3-English/pg346-cpm-pcie/Completer-Completion-Descriptor-Format?contentId=pEh4XcohN3uFqiFePvYL_A)

모델은 단일 Requester만 가정합니다. tag는 0~31, 주소는 32비트, 읽기 길이는 4~256바이트이고 주소·길이가 모두 4바이트 정렬입니다. DW는 Dword, 4바이트 단위입니다. 모든 요청 byte-enable은 유효하다고 가정해 DW 앞뒤의 무효 padding은 없습니다. Successful Completion인 SC만 받으며 error status는 거부합니다. MPS는 128바이트, RCB도 128바이트로 따로 정했습니다.

## 2. 32바이트 요청을 16+16으로 받는 흐름

tag 5는 주소 `0x1070`부터 32바이트, tag 9는 `0x2000`부터 8바이트를 요청합니다. fixture는 서로 다른 요청의 응답을 중간에 끼워 넣습니다.

| 도착 순서 | tag·Lower Address·Byte Count | 유효 payload | 요청별 판정 |
| --- | --- | --- | --- |
| 1 | 5·112·32 | 00~0F, 16바이트 | tag 5는 받은 16·남은 16·ACTIVE입니다. |
| 2 | 9·0·8 | A0~A7, 8바이트 | tag 9만 DONE입니다. |
| 3 | 5·0·16 | 10~1F, 16바이트 | tag 5도 받은 32·남은 0·DONE입니다. |

`0x1070 & 0x7F = 0x70 = 112`이고 첫 조각 뒤 주소는 `0x1080`, 하위 7비트는 0입니다. 첫 Byte Count 32는 현재 payload 16과 같지 않습니다. 다음 응답에서 16으로 줄어듭니다. 최종 tag 5 데이터는 `000102...1E1F`이고 tag 9 데이터와 섞이지 않습니다.

첫 조각만 보고 CPU에 공개하면 뒤 16바이트가 빠집니다. `cpu_read(5)`는 DEVICE_OWNED로 거부하며, 전체 요청 길이를 확인한 뒤에만 읽습니다. 이 소유권은 조립 버퍼의 응용 계약입니다. 실제 CPU cache·DMA mapping·메모리 배리어를 실행한 결과가 아닙니다.

## 3. 수정: 저장하기 전에 모든 필드를 확인합니다

```python
received = len(request['data'])  # len은 이 tag로 검증해 받은 바이트 수입니다.
remaining = request['length'] - received  # 요청 길이에서 받은 양을 빼 기대 Byte Count를 구합니다.
next_address = request['address'] + received  # 다음 조각이 시작해야 할 주소입니다.
if byte_count != remaining:  # !=는 다름 비교이며 조각 자체의 크기와 혼동하지 않습니다.
    raise ContractError('BYTE_COUNT')  # raise는 잘못된 조각을 저장하지 않고 거부합니다.
if lower_address != next_address & 127:  # &는 하위 7비트만 남기는 마스크입니다.
    raise ContractError('LOWER_ADDRESS')  # 앞 조각 다음 주소와 다른 응답을 거부합니다.
request['data'].extend(data)  # 모든 길이·분할 검사를 통과한 뒤 bytes를 이어 붙입니다.
```

실제 함수는 위 비교 외에 tag의 존재·ACTIVE 상태·SC status·payload의 4바이트 배수·남은 길이·MPS·중간 분할 경계를 확인합니다. 거부한 조각에서는 버퍼가 16바이트 그대로인지도 검사합니다. 예외가 난 뒤 일부만 저장하는 오류를 막기 위한 대조입니다.

| 오류 입력 | 결과 | 놓치기 쉬운 점 |
| --- | --- | --- |
| 둘째 tag 5 조각의 Byte Count를 32로 유지합니다. | BYTE_COUNT | 현재 payload 길이가 맞아도 남은 양이 틀립니다. |
| 둘째 Lower Address를 16으로 둡니다. | LOWER_ADDRESS | 다음 주소의 하위 비트와 다릅니다. |
| 첫 조각을 다시 보냅니다. | BYTE_COUNT | 두 번째 복사로 조립량을 늘리지 않습니다. |
| UR status를 보냅니다. | COMPLETION_STATUS | error를 정상 데이터로 넘기지 않습니다. |
| 빈 값·3바이트·남은 16보다 긴 20바이트 | PAYLOAD_LENGTH | 부족·과잉·정렬을 구분해 거부합니다. |
| 완료 뒤 같은 응답을 다시 보냅니다. | NOT_ACTIVE | 이미 DONE인 tag에 덧붙이지 않습니다. |

오류가 난 요청을 자동 복구하거나 timeout시키지는 않습니다. 데이터는 격리된 채 ACTIVE이고, 실제 드라이버의 error retirement·AER·상위 재요청 정책은 범위 밖입니다. 영원히 대기해도 된다는 설계 권고가 아닙니다.

## 4. RCB와 MPS를 같은 값으로 외우지 않습니다

MPS는 한 payload의 크기 상한입니다. RCB는 분할할 때의 자연 정렬 경계입니다. PG054 3.3의 Read Completion Boundary는 중간 조각의 시작·끝 정렬과 원 요청 시작·끝의 예외를 설명합니다. [PG054 RCB](https://docs.amd.com/r/en-US/pg054-7series-pcie/Read-Completion-Boundary)

이 요청은 `0x1070`에서 다음 128바이트 경계 `0x1080`까지 16바이트입니다. 중간에 나누면 첫 조각은 그 경계에서 끝납니다. 첫 조각을 4바이트에서 끊으면 끝 주소 `0x1074`가 경계가 아니어서 RCB_SPLIT로 거부합니다. 반면 32바이트를 단일 Completion으로 돌려주면 원 요청의 시작과 끝을 모두 처리하므로 같은 128 경계를 가로질러도 이 계약에서 허용합니다. MPS 128보다 작은 32바이트입니다. RCB가 무조건 한 조각 최대 크기라는 오해를 드러내는 정상 대조입니다.

256바이트의 정렬된 요청은 128+128로 받고, 132바이트 payload는 자체 MPS를 초과해 거부합니다. `0x1FFC`부터 4바이트는 4KiB 끝에 맞아 허용하지만 8바이트 요청은 경계를 넘어 입력 오류입니다. RCB·MPS·4KiB 요청 경계는 각각 다른 조건입니다.

## 5. tag 재사용과 DMA 완료를 연결할 때

같은 tag를 미완료 요청에 다시 배정하면 TAG_BUSY입니다. 완료 뒤에도 `retire(tag)`로 정리하기 전에는 재배정하지 않습니다. retire 뒤 옛 Completion은 UNKNOWN_TAG이고, 새 요청에 tag 5를 쓰는 정상 경로도 따로 확인했습니다. 다만 wire에는 이 모델의 별도 세대 번호가 없습니다. tag를 새 요청에 배정한 뒤 같은 tag의 비정상적인 늦은 응답이 도착하는 상황을 tag만으로 완전히 구분한 모델은 아닙니다.

실제 PCIe DMA는 Requester ID·tag·TC 등 적용되는 규칙과 controller의 완료 의미를 함께 확인해야 합니다. 일반 RAM·DMA bus address·MMIO 주소도 구분해야 합니다. Linux DMA API는 CPU virtual address와 장치용 DMA 주소가 일반적으로 같다고 가정하지 않으며, coherent memory라도 적절한 순서 보장이 필요하다고 설명합니다. [Linux 6.12 DMA mapping Guide](https://docs.kernel.org/6.12/core-api/dma-api-howto.html)

이 사례의 DONE은 요청한 데이터가 합성 조립기에 모두 들어온 상태입니다. posted write 완료·doorbell 도달·DMA engine 전체 작업 완료·CPU cache 최신성·응용 계산 완료를 대신하지 않습니다. 원시 TLP header·byte-enable padding·BCM·Poisoned/ECRC·확장 tag·zero-length read·raw Byte Count 0의 4096 인코딩·flow credit·링크 재시도·reset은 구현하지 않았습니다. AMD AXI descriptor의 필드 폭을 wire TLP 비트 배치와 섞지도 않습니다.

## 6. 성공 판정과 변이 검사

fixture의 요청·응답·각 단계 상태·최종 데이터는 직접 적은 리터럴입니다. `pcie-finish-first`는 첫 조각에서 DONE으로 바꾸므로 첫 상태 기대값과 다릅니다. `pcie-ignore-byte-count`는 나머지 필드가 정상인 둘째 조각의 잘못된 Byte Count를 수락해 검증기가 실패합니다. Python의 일반 assert에 기대지 않아 -O에서도 두 오류를 검출합니다. 자세한 명령·해시·종료값은 검증 기록에 있습니다.

## 확인 문제

1. 첫 payload가 16바이트인데 Byte Count가 왜 32인가요? 그 조각을 포함해 아직 반환할 전체 바이트 수이기 때문입니다.
2. tag 9가 먼저 완료되면 tag 5도 읽어도 되나요? 안 됩니다. 요청별 누적 길이와 소유권을 확인합니다.
3. RCB가 128이면 모든 응답을 128바이트로 잘라야 하나요? 아닙니다. 중간 분할 위치의 제약이며 원 요청 시작·끝의 예외와 MPS를 따로 확인합니다.

## English

A decoded-field host model tracks one requester, tags 0–31, aligned full-byte reads, SC responses, MPS 128 and RCB 128. Interleaved completions preserve request-specific data; Byte Count and Lower Address are checked before committing each piece. A single completion may span the modeled RCB boundary, while interior splits must align. Partial data stays private until the declared request completes. This is neither raw TLP conformance nor PCIe/DMA hardware execution.

## 읽은 판본과 범위

2026-10-21에 PG346 3.3(2023-05-16)의 Completer Completion Descriptor Format·Completer Memory Read Operation, PG156 4.4(2024-12-06)의 같은 descriptor 표, PG054 3.3(2024-12-06)의 Read Completion Boundary를 확인했습니다. Lower Address·Byte Count·DW count·Requester ID/tag·SC/UR/CA·같은 요청의 순서·RCB 시작/끝 예외를 대조했습니다. PCI-SIG Base Specification 전체를 읽거나 적합성을 시험했다는 뜻은 아닙니다.
