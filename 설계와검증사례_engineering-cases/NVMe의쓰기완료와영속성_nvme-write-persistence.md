# NVMe의 쓰기 완료와 영속성 / NVMe write completion and persistence

[실행 코드](../예제_examples/실무검증_practical-validation/storage_protocols/README.md) · [카드의 busy·상태](eMMC와SD의busy와쓰기실패_emmc-sd-write-status.md) · [검증 기록](검증기록_evidence/저장장치완료와영속성검사_20261021.md)

## 1. 성공 완료 뒤에도 사라지는 데이터

컨트롤러가 쓰기 성공을 보고했고 바로 읽은 값도 맞는데 전원 상실 뒤에는 이전 값이 보이는 상황을 살펴봅니다. 영속성은 전원이 끊겨도 데이터가 남는 성질입니다. 휘발성 쓰기 캐시(VWC)는 이 성질과 별도로 빨리 완료를 돌려줄 수 있습니다. 성공 CQE를 받았다는 사실과 영속성에 필요한 조건을 만족했다는 판단을 나누어야 합니다. [Linux block cache 문서의 Introduction·Explicit cache flushes·FUA](https://docs.kernel.org/block/writeback_cache_control.html)

이 글은 단일 SQ·namespace를 다루는 합성 Python 모델입니다. 실제 NVMe 명령·드라이버·SSD·전원 차단 장비를 실행하지 않았습니다. 교육용 4바이트 블록 8개를 두고, `cache`와 `media`라는 사전을 나눕니다. `power_loss()` 뒤의 `read()`는 남아 있는 내부 media를 조사하는 관측입니다. 꺼진 장치에 읽기 명령을 보낸 결과가 아닙니다. 초기 0은 직접 채운 이전 데이터이며 미기록 실제 LBA가 언제나 0이라는 가정도 아닙니다.

## 2. CID와 완료 순서를 나눕니다

CQE는 Completion Queue Entry, 즉 완료 큐의 항목입니다. 실제 완료는 SQID와 CID 조합으로 식별합니다. 모델에는 SQ가 하나이므로 CID만 키로 씁니다. 먼저 제출한 명령이 반드시 먼저 완료된다고 가정하지 않습니다. [NVMe Base 1.4c §§4.2·4.6, pp. 65–66·77–78](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf)

`nvme_out_of_order_then_flush`는 다음 리터럴을 대조합니다.

| 사건 | 추적 결과 |
|---|---|
| CID 9로 LBA 0에 `11223344` 제출 | pending의 키 9입니다. |
| CID 10으로 LBA 1에 `55667788` 제출 | pending의 키 10입니다. |
| CID 10 성공 완료 | LBA 1의 캐시 쓰기를 처리합니다. |
| CID 9 성공 완료 | LBA 0의 캐시 쓰기를 처리합니다. |
| CID 11 Flush 성공 완료 | 두 값을 media에 반영합니다. |
| 합성 전원 상실 | 두 값이 그대로 남습니다. |

중복 CID, 알 수 없는 CID, 겹치는 진행 중 쓰기는 거부합니다. 중복 완료를 다른 명령의 성공으로 오인하면 자료와 상태가 엇갈리므로, 잘못된 완료 입력이 pending이나 media를 바꾸지 않는지도 검사합니다. 정상 완료 뒤 CID 재사용은 허용하지만 reset 세대·CQ phase tag·DMA 버퍼와 경쟁 상태는 구현하지 않습니다. 동시 명령 상한 4개는 자체 제한입니다.

## 3. Flush와 FUA가 보장하는 대상을 구분합니다

Flush는 지정 namespace에서 제출 전에 완료된 명령의 캐시 자료를 대상으로 합니다. 모델은 이를 명확히 관측하려고 앞선 명령의 완료를 모두 받은 후 Flush를 제출하고, 그동안 새 쓰기도 막습니다. 이는 규격보다 좁은 자체 호스트 정책입니다. [NVMe Base 1.4c §6.8, p. 261](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf)

FUA(Force Unit Access)는 해당 Write의 자료를 비휘발 매체에 반영한 뒤 완료하도록 요구합니다. 다른 명령과의 순서를 자동으로 만들지는 않습니다. [같은 문서 §6.15, Figure 406, p. 272](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf)

| 실행한 시나리오 | 완료 직후 판정 | 합성 전원 상실 뒤 관측 |
|---|---|---|
| CID 7, VWC 켜짐, LBA 0=`aabbccdd` | SUCCESS, durable=false입니다. 읽으면 새 값입니다. | LBA 0은 이전 값 `00000000`입니다. |
| LBA 0=`01020304` 일반 쓰기 후 LBA 1=`a1a2a3a4` FUA | 첫 쓰기는 durable=false, FUA는 true입니다. | LBA 0은 이전 값, LBA 1은 새 값입니다. |
| CID 65535, VWC 꺼짐, LBA 7=`fedcba98` | SUCCESS, durable=true입니다. | 새 값이 남습니다. |
| CID 41 Flush가 ABORTED | FAILED_UNCERTAIN, durable=false입니다. | 이 fault profile에서는 해당 캐시 값이 사라집니다. |

FUA 대조에서는 총 2×4=8바이트를 썼고 그중 4바이트만 남습니다. 이 비율은 고정 입력의 계산이며 실제 SSD의 손실률 통계가 아닙니다. 배경 저장이나 전원 보호가 있는 다른 장치에서 일반 쓰기도 남을 수 있습니다. 다만 남을 수도 있다는 가능성을 필요한 보장으로 바꾸면 안 됩니다.

응용 로그에 빗대면 LBA 0을 본문, LBA 1을 완료 표시로 볼 수 있습니다. 완료 표시만 FUA로 쓰면 표시가 본문보다 먼저 남는 반례가 가능합니다. 이 모델에서 순서를 정하려면 본문 완료→성공 Flush 완료→완료 표시의 FUA 성공 완료를 관측하는 정책이 필요합니다. 이것만으로 파일시스템 전체나 여러 sector의 원자적 트랜잭션을 구현했다고 주장하지는 않습니다.

## 4. 실패는 ‘아무것도 안 바뀜’과 다릅니다

실패 시나리오는 CID 30으로 LBA 4·5에 `11111111`·`22222222`를 제출하고 MEDIA_ERROR를 넣습니다. 장치 내부 fault 주입을 한 블록으로 정했으므로 전원 상실 뒤 값은 `11111111`·`00000000`입니다. 성공은 0건이지만 내부적으로는 4바이트가 바뀌었습니다.

`fault_prefix=1`은 시험자가 아는 내부 ground truth입니다. NVMe CQE가 첫 블록만 성공했다고 알려 주는 필드가 아닙니다. 따라서 이 숫자를 근거로 호스트가 두 번째 블록부터 안전하게 재개할 수는 없습니다. 이 모델은 실패의 한 가능한 효과만 고정하며, 정상·정전 원자성 크기나 경계 보장을 계산하지 않습니다. 실제 설계에서는 장치의 원자성 조건, 애플리케이션의 버전·검사값·중복 처리, 복구 절차를 따로 정해야 합니다. [NVMe Base 1.4c §6.4의 정상 동작·전원 상실 원자성 구분](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf)

수정한 호스트 판정은 성공·실패와 `durable_ack`를 분리합니다. Flush 실패를 성공으로 바꾸거나 FUA를 전체 캐시 비우기로 구현한 의도적 오류는 리터럴 검사에 걸립니다. 실패 Flush가 실제로 어떤 자료까지 반영했는지는 이 오류 코드 하나로 확정하지 않습니다. fixture에서 효과를 0으로 정한 것은 반례를 재현하기 위한 선택입니다.

## 5. 코드에서 확인할 부분

```python
if cid not in self.pending:                  # not in은 해당 키가 없는지 확인합니다.
    raise ContractError('UNKNOWN_CID')       # raise는 잘못된 완료 입력을 예외로 거부합니다.
command = self.pending[cid]                  # []는 그 CID에 대응하는 명령을 읽습니다.
if command.fua or not self.vwc:              # or는 둘 중 하나가 참인지, not은 거짓인지 검사합니다.
    self.media.update(command.data)          # update는 해당 쓰기의 주소와 값을 반영합니다.
    for lba in command.data:                 # for는 그 쓰기의 주소만 순회합니다.
        self.cache.pop(lba, None)            # pop은 이전 캐시 값을 제거하며 없으면 None을 돌려줍니다.
```

이 코드는 정상 경로의 핵심을 발췌했습니다. 실제 소스에서는 입력을 검증하고 명령을 제거한 뒤 분기합니다. `def complete(...)`의 def는 함수 정의, self는 객체 자신, 괄호는 인자 목록입니다. `Command`는 명령 필드를 묶은 자료 클래스이며 `dict`는 주소→자료 또는 CID→명령 대응을 저장합니다. 수정의 핵심은 FUA 분기에서 `self.cache` 전체를 media로 복사하지 않는 것입니다.

최종 실행에서 전체 두 모델의 12개 시나리오·72단계·42개 입력 거부·24개 경계가 일반 Python과 `-O`에서 같은 관측값으로 PASS였습니다. NVMe 오류 구현 3종과 카드 오류 구현 2종은 두 모드 모두 ERROR/exit 1이었습니다. 자세한 실행 환경·소스 해시는 검증 기록에 있습니다. 이것은 장치 성능이나 규격 전체 적합성의 결과가 아닙니다.

## 6. 확인 문제

1. CID 9 다음 CID 10이 먼저 완료되면 순서대로 배열 앞에서 제거해도 되나요? 답: 안 됩니다. 완료 CID가 가리키는 명령을 찾아야 합니다.
2. 데이터 쓰기 후 완료 표시만 FUA로 쓰면 데이터까지 영속화되나요? 답: 그 보장은 없습니다. 다른 쓰기의 순서·영속성 조건이 필요합니다.
3. 실패 완료와 `fault_prefix=1`을 보고 응용이 첫 블록을 승인해도 되나요? 답: 안 됩니다. prefix는 시험 내부 주입값이며 호스트 완료 정보가 아닙니다.

## English

The exercise distinguishes successful completion, visible cached data and acknowledged persistence. It uses a single-SQ, single-namespace decoded model with eight four-byte teaching blocks. No NVMe command, SSD or power-cut rig is run. Reads after the loss event inspect internal media. Initial zeroes represent explicitly initialized old data.

An out-of-order CID 10 completion is matched to its own request before CID 9. Successful Flush then preserves both payloads. The FUA counterexample preserves only its own LBA: the earlier unrelated cached write is lost. Failed writes may have explicitly injected internal effects; the prefix length is never presented as a CQE field. Unknown/duplicate completions are rejected, and invalid completion input leaves state unchanged. The serialized Flush policy, fault effects and four-command limit are teaching choices, not a full controller implementation.

## 출처

- [NVM Express Base Specification 1.4c](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf), 표지 날짜 2021-03-09: §§4.2·4.6, Identify Controller VWC(Figure 251), §§6.4·6.8·6.15를 대조했습니다. 최신 규격 전체 구현을 뜻하지 않습니다. © 2007 to 2021 NVM Express, Inc. ALL RIGHTS RESERVED.
- [Linux, Explicit volatile write back cache control](https://docs.kernel.org/block/writeback_cache_control.html): 완료와 영속성, PREFLUSH·FUA·드라이버 기능 전달을 확인했습니다. Linux v6.12의 같은 RST도 대조했습니다. Linux API는 실행하지 않았습니다.
- 표·입력·내부 fault·계산은 직접 구성했습니다. 출처와 실행 확인일은 2026-10-21입니다.
