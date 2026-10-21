# eMMC·SD의 busy 해제와 쓰기 실패 / eMMC and SD busy release and write failure

[실행 코드](../예제_examples/실무검증_practical-validation/storage_protocols/README.md) · [NVMe의 영속성](NVMe의쓰기완료와영속성_nvme-write-persistence.md) · [검증 기록](검증기록_evidence/저장장치완료와영속성검사_20261021.md)

## 1. 기다림의 끝과 성공 판정

카드에 자료를 보낸 뒤 busy가 끝났다는 이유만으로 ‘저장 완료’를 표시하는 오류를 재현합니다. busy는 장치가 아직 처리 중임을 알리는 관측이고, 성공 여부와 캐시 영속성은 별도 질문입니다. 모델은 이미 해석한 `busy`, `ready`, `state`, `error`를 받습니다. eMMC와 SD의 raw 명령·전압·DAT0 파형·드라이버는 실행하지 않았습니다.

기본 정책은 busy가 없어야 하고, ready가 참이며, state가 TRAN이고, 오류가 없어야 쓰기를 성공 처리하는 것입니다. Linux v6.12의 `mmc_busy_cb()`와 `mmc_ready_for_data()`가 busy 감지와 상태 판단을 구분하는 부분을 참고했습니다. 실제 호스트의 HW busy 기능·native/SPI 모드에 따라 경로가 달라지므로 모든 장치에 동일한 관측 절차를 강제하지 않습니다. [Linux mmc_ops.c](https://github.com/torvalds/linux/blob/v6.12/drivers/mmc/core/mmc_ops.c), [mmc.h의 준비 상태 정의](https://github.com/torvalds/linux/blob/v6.12/include/linux/mmc/mmc.h)

## 2. busy가 풀려도 기다려야 하는 상태

고정 SD 시나리오는 request 1로 `10203040`을 쓰고 다음 관측을 넣습니다. 각 행은 논리적 단계이며 실제 경과 시간이나 장치 응답 속도 측정이 아닙니다. TRAN은 전송 가능 상태, PRG는 프로그래밍 중 상태를 나타내는 해석된 이름입니다.

| 단계 | busy | ready | state | 수정한 판정 |
|---|---|---|---|---|
| 1 | 참 | 거짓 | PRG | WAIT_BUSY입니다. |
| 2 | 거짓 | 거짓 | PRG | WAIT_STATUS입니다. |
| 3 | 거짓 | 참 | PRG | WAIT_STATUS입니다. |
| 4 | 거짓 | 거짓 | TRAN | WAIT_STATUS입니다. |
| 5 | 거짓 | 참 | TRAN | 오류가 없으므로 SUCCESS입니다. |

`card-busy-is-done` 변이는 2단계에서 성급하게 SUCCESS를 반환합니다. 검사기는 직접 적은 WAIT_STATUS와 다르므로 실패시킵니다. 준비 비트만 보거나 상태 이름만 보는 오류도 3·4단계가 구분합니다. 상태 조회 자체의 전송 오류, 실제 비트 clear 규칙, 카드 제거 세대는 이 모델에 없습니다.

쓰기 오류는 상태에서 먼저 판정합니다. request 2는 busy가 풀렸고 TRAN·ready도 맞지만 WRITE_ERROR가 있습니다. 결과는 `FAILED_UNCERTAIN`, 영속성 승인=false입니다. `card-ignore-status-error` 변이는 이를 SUCCESS로 바꾸므로 리터럴 검사가 발견합니다. WP_VIOLATION도 별도 경로에서 거부하는지 확인했습니다.

## 3. 부분 효과와 timeout을 따로 기록합니다

request 2는 LBA 2·3에 `abababab`·`cdcdcdcd`를 요청합니다. 합성 장치의 오류 효과를 한 블록으로 주입했으므로 전원 상실 뒤에는 `abababab`·`00000000`이 남습니다. 교육 블록이 4바이트이므로 요청 8바이트 중 내부 효과는 4바이트입니다. 호스트가 4바이트 성공을 보고받았다는 뜻은 아닙니다.

별도 eMMC 시나리오는 LBA 5·6의 `12345678`·`87654321` 요청을 timeout시킵니다. 같은 한 블록 효과를 주입해 결과는 `TIMED_OUT_UNKNOWN`, 남은 값은 `12345678`·`00000000`입니다. timeout은 관측한 완료가 없다는 의미이지 저장이 전혀 진행되지 않았다는 증거가 아닙니다. 여기서는 Python의 실제 시간 제한을 실행하지 않고 `timeout()` 사건을 명시적으로 넣습니다.

오류·timeout 뒤에는 `recovery_required`를 세워 다음 쓰기를 거부합니다. 원인은 결과가 불명확한 상태에서 조용히 새 작업을 시작하면 이전 작업과 새 작업의 효과를 구분하기 어렵기 때문입니다. 이는 진단을 위해 멈추는 자체 정책이며 재초기화·복구·재시도는 구현하지 않습니다. 실제 복구는 장치 상태, 응용의 버전·검사값·중복 처리 조건을 확인한 다음 설계해야 합니다. 같은 데이터를 다시 쓰는 것과 새로운 응용 명령을 두 번 실행하는 것도 구분해야 합니다.

## 4. 캐시 지원과 캐시 사용을 구분합니다

캐시가 있는지, 현재 켜졌는지, flush가 성공했는지는 서로 다른 조건입니다. SD Association의 A2 설명은 캐시 수신 후 busy를 풀고 뒤에서 자료를 저장하는 경우와 flush 완료 전 손실 가능성을 설명합니다. A2 기능을 사용하려면 호스트 지원도 필요하므로 카드의 성능 등급만으로 현재 활성화를 추정하지 않습니다. [SD Association, 2017-03-24, Cache function·For manufacturers](https://www.sdcard.org/press/thoughtleadership/applications-in-action-introducing-the-newest-application-performance-class/)

eMMC의 예로 Delkin G630 Rev A는 CACHE_CTRL과 flush·barrier를 구별합니다. barrier의 순서 제약과 지금 당장 자료를 영속화하는 일은 같지 않습니다. 이 문서는 한 제품의 5.1 설명이므로 다른 카드의 실제 지원 기능을 대신하지 않습니다. [G630 Engineering Specification §§4.4–4.6, pp. 10–12](https://www.delkin.com/wp-content/uploads/2020/10/401-0511-00_Rev-A_G630-Series-Industrial-eMMC-5.1-Engineering-Specification.pdf)

| 모델 입력과 실행 | 쓰기 완료 판정 | 합성 전원 상실 뒤 |
|---|---|---|
| 캐시 미지원 SD, 정상 상태 | SUCCESS, durable=true입니다. | `10203040`이 남습니다. |
| 캐시 지원 eMMC, enable 후 쓰기 | SUCCESS, durable=false입니다. | 성공 Flush 후 `deadbeef`가 남습니다. |
| 캐시 지원 SD, enable 후 쓰기 | SUCCESS, durable=false입니다. | Flush 없이 `99887766`이 사라집니다. |
| 캐시 지원 eMMC, Flush 실패 | FAILED_UNCERTAIN, durable=false입니다. | 이 fault profile에서는 캐시 값이 사라집니다. |

`cache_supported=true`는 기능 확인을 끝냈다고 가정한 decoded 입력입니다. SD 확장 레지스터와 eMMC EXT_CSD의 해석은 하지 않습니다. 둘의 캐시 활성화·flush wire 명령이 같다는 의미도 아닙니다. 미지원 카드의 enable은 CACHE_UNSUPPORTED, 활성화 전 flush는 CACHE_NOT_ENABLED로 거부됩니다. `flush(success)`는 장치별 busy·최종 상태 절차를 마친 결과를 받는 추상 경계이며 그 절차 자체를 구현하지 않습니다.

이번 fault profile은 캐시를 잃도록 고정했습니다. 실제 캐시의 매체·배경 저장·전원 보호에 따라 보존 결과가 달라질 수 있습니다. 캐시 미사용 정상 쓰기의 media 반영도 자체 정상 동작 계약이며, 카드 내부 원자성·수명·ECC·불량 블록 관리·정전 손상 전체를 보장하는 결과가 아닙니다.

## 5. 코드와 확인 결과

```python
if busy:                                      # if는 busy가 참일 때 아래 분기를 실행합니다.
    return {'result': 'WAIT_BUSY'}             # return은 사전 {}을 돌려주고 함수를 끝냅니다.
if not ready or state != 'TRAN':               # not·or·!=로 준비 조건 중 하나라도 틀렸는지 검사합니다.
    return {'result': 'WAIT_STATUS'}           # busy가 풀렸어도 성공으로 바꾸지 않습니다.
if self.cache_enabled:                        # 점 표기로 이 카드 객체의 캐시 상태를 읽습니다.
    self.cache.update(data)                   # update는 주소와 자료를 휘발 사전에 반영합니다.
else:                                         # else는 캐시가 꺼진 경우입니다.
    self.media.update(data)                   # 정상 쓰기의 비휘발 상태를 반영합니다.
```

입문용으로 반환값의 일부만 보인 발췌입니다. 실제 `poll()`은 먼저 입력·오류를 검사하고 반환값에 request_id와 durable_ack도 넣습니다. `None`은 오류가 없음을 나타내는 이 API의 값입니다. `def`는 함수 정의, `self.active = None`의 `=`는 진행 중 작업을 해제하는 대입입니다. `is None`은 그 특수값인지를 검사합니다. 카드 request_id는 자체 번호이며 Card Identification 레지스터를 뜻하는 카드의 CID와 다릅니다.

전체 저장장치 실습은 12개 리터럴 시나리오, 42개 거부 입력, 24개 경계를 검사했습니다. 카드 경계에는 마지막 LBA 7, 범위를 넘는 쓰기, bool을 정수 대신 넣는 입력, 중복 진행, 없는 작업의 상태 조회, 미지원 오류값, timeout 뒤 새 쓰기 등이 포함됩니다. 정상과 `-O` 관측값이 같았으며, 카드 오류 변이 2종도 두 모드에서 모두 검출했습니다. 실물 카드 시험이나 파일시스템 복구 성공을 뜻하지 않습니다.

## 6. 확인 문제

1. busy=false, ready=true, PRG이면 성공인가요? 답: 이 정책에서는 WAIT_STATUS입니다. ready와 TRAN을 함께 확인합니다.
2. 캐시 기능을 지원한다면 바로 flush를 호출해도 되나요? 답: 이 API에서는 명시적으로 활성화되어 있어야 하며 진행 중 쓰기나 복구 필요 상태도 없어야 합니다.
3. 부분 효과를 한 블록 주입했으므로 두 번째 블록부터 재개하면 되나요? 답: 아닙니다. 주입값은 내부 시험 정보이며 실제 완료 응답으로 확인한 재개 지점이 아닙니다.

## English

The decoded card model separates busy release, ready/state, error status and persistence. It does not send eMMC/SD commands or sample DAT0. Five logical observations show that clearing busy alone is insufficient for the chosen conservative host policy. Error status is checked before success, and a timeout remains an unknown result even when the injected device effect changed some blocks.

Cache capability and activation are separate inputs. eMMC and SD use a shared teaching interface, not a shared on-wire command. A decoded successful flush preserves the teaching cache; a normal cached completion does not acknowledge persistence. Device-specific flush execution, automatic recovery, atomicity and physical media behavior are outside scope. Error and timeout latch a policy stop rather than silently allowing the next write. Post-loss reads inspect internal media. The data, timing-free events and fault prefixes are constructed examples rather than product measurements.

## 출처

- [Linux v6.12 mmc_ops.c](https://github.com/torvalds/linux/blob/v6.12/drivers/mmc/core/mmc_ops.c): `mmc_busy_cb()`·`__mmc_poll_for_busy()`·`__mmc_switch()`의 busy·오류·최종 상태 경로를 읽었습니다. native/SPI 차이를 한 API로 구현했다고 주장하지 않습니다.
- [Linux v6.12 mmc.h](https://raw.githubusercontent.com/torvalds/linux/v6.12/include/linux/mmc/mmc.h): 109–168행의 native 상태 이름·`mmc_ready_for_data()`의 ready와 TRAN 비교·SPI 구분을 대조했습니다.
- [SD Association의 A2 설명](https://www.sdcard.org/press/thoughtleadership/applications-in-action-introducing-the-newest-application-performance-class/), Yosi Pinto, 2017-03-24: Cache function과 호스트 지원 조건을 읽었습니다. 전체 SD 규격을 열람했다고 표기하지 않습니다.
- [Delkin G630 eMMC 5.1, 401-0511-00 Rev A](https://www.delkin.com/wp-content/uploads/2020/10/401-0511-00_Rev-A_G630-Series-Industrial-eMMC-5.1-Engineering-Specification.pdf), 2020: §§4.4–4.6과 §5.2를 읽었습니다. 표·그림을 전재하지 않고 자체 예제를 썼습니다.
- 출처와 실행 확인일은 2026-10-21입니다.
