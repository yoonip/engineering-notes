# 검사와 대기 사이의 알림 유실 / Lost wakeups between checking and waiting

작업 큐가 비었는지 확인한 뒤 잠들었는데, 큐에 처리할 데이터가 남아 있는 상황을 다룹니다. 알림이 오지 않은 것이 아니라 너무 일찍 도착해 사라질 수도 있습니다. 이 사례는 “지금 자고 있으면 깨운다”는 동작과 “도착 사실을 보관하고 필요하면 깨운다”는 동작을 세 가지 사건 순서에서 비교합니다.

[실행 모델](../예제_examples/실무검증_practical-validation/rtos/models.py), [독립 검사](../예제_examples/실무검증_practical-validation/rtos/verify.py), [실행 안내](../예제_examples/실무검증_practical-validation/rtos/README.md), [검증 기록](검증기록_evidence/RTOS스케줄과알림검사_20261021.md)을 연결했습니다. Python 표준 라이브러리로 구성한 결정적 모델이며 실제 FreeRTOS·인터럽트·DMA를 실행하지 않습니다.

## 1. 빈 큐 확인과 대기 사이의 상태 변화

소비자 태스크가 큐를 확인하는 사건을 C, 작업이 없다고 생각해 기다리는 사건을 W, 생산자가 데이터 42를 공개하고 깨우는 사건을 P로 둡니다. C는 반드시 W보다 먼저이지만 P는 그 전·사이·뒤에 올 수 있습니다. 모델은 실제 메모리 읽기를 경쟁 실행하지 않고 각 사건의 상태를 직접 기록합니다.

| 순서 | 의미 | 단순 resume 경로 |
| --- | --- | --- |
| PCW | 데이터가 먼저 도착한 뒤 큐를 확인합니다. | C에서 데이터를 보고 처리하므로 잠들지 않습니다. |
| CPW | 빈 큐를 확인한 뒤 데이터가 도착하고, 그 후에 잠듭니다. | P 당시 아직 자지 않아서 깨움이 사라지고, W에서 잠듭니다. |
| CWP | 빈 큐를 확인하고 잠든 다음 데이터가 도착합니다. | P가 대기자를 깨워 처리할 수 있습니다. |

문제는 CPW입니다. C에서 확인한 값은 그 순간의 관측이며, 그 후에도 큐가 비어 있다는 보장은 아닙니다. W까지의 틈에 생산자가 들어올 수 있습니다. 이 경우 payload는 큐에 남아 있지만 소비자는 다음 알림을 기다립니다. 다음 알림이 오지 않으면 작업이 계속 남는 lost wakeup입니다.

FreeRTOS V11.1.0의 `task.h`는 정지 전에 인터럽트가 올 수 있다면 `xTaskResumeFromISR()`를 동기화 용도로 사용하는 데 문제가 있다고 설명합니다. [버전이 고정된 공식 task.h](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/include/task.h). 이 사례는 그 계약 차이를 표현한 것이며 FreeRTOS 자체의 알림 구현에서 결함을 발견했다는 주장이 아닙니다.

## 2. 대기 전에 온 알림도 남겨 둡니다

수정 경로는 P에서 도착 사실 `pending`을 증가시킵니다. W는 pending이 있으면 바로 소비하고, 없을 때만 대기자로 등록합니다. 여기서 “확인과 등록”은 하나의 동기화 연산이어야 합니다. 일반 변수 확인과 일반 변수 변경을 다시 두 동작으로 흩어 놓으면 같은 틈이 생길 수 있습니다.

```python
if retained:                   # if는 알림을 보관하는 경로를 선택합니다.
    state.pending += 1         # +=는 아직 대기하지 않아도 도착 사실을 더합니다.
```

```python
if retained and state.pending > 0:  # and는 두 조건이 모두 맞는지 확인합니다.
    state.pending = 0               # 모델의 대기 연산이 보관한 알림을 소비합니다.
    drain()                         # def로 정의한 보조 함수를 호출해 payload를 처리합니다.
else:
    state.waiting = True            # 알림이 없을 때만 대기 상태로 전환합니다.
```

실제 FreeRTOS에서는 이 규약을 제공하는 API를 사용합니다. `xTaskNotifyGive()`와 `ulTaskNotifyTake()`는 알림 값을 세마포어처럼 사용하는 한 조합입니다. V11.1.0의 `ulTaskGenericNotifyTake()`에서 알림 확인과 대기 상태 등록을 임계 구역으로 연결하는 부분을 읽었습니다. 애플리케이션에서 그 내부 동작을 일반 변수 두 개로 대체하지 않습니다. [공식 tasks.c](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/tasks.c)

Python 모델의 W는 이 확인·등록 계약을 한 사건으로 가정합니다. P가 대기자를 깨우는 경우에는 소비자가 다시 실행해 큐를 비우는 단계까지 같은 추상 사건에 묶었습니다. 실제 선점 지점이나 커널의 모든 목록 변경을 시뮬레이션한 것은 아닙니다.

## 3. 실행 결과와 독립 판정

정상 검사에서는 세 배치를 순열로 생성하고 C가 W보다 앞선 것만 선택합니다. 단순 resume의 유실 여부는 시뮬레이터와 별도로 `C의 위치 < P의 위치 < W의 위치`라는 순서 조건으로 판정합니다. 수정 경로에는 생산한 payload 42가 정확히 소비됐는지, 큐에 남아 잠들어 있지 않은지를 요구합니다.

| 배치 | 단순 resume의 유실 | 알림 보존의 유실 | 보존 경로의 소비 값 |
| --- | --- | --- | --- |
| PCW | false | false | `[42]` |
| CPW | true | false | `[42]` |
| CWP | false | false | `[42]` |

이 결과는 2026-10-21 Windows x86-64·Python 3.12.14에서 얻었습니다. 세 순서의 발생 확률을 측정한 것은 아니므로 유실률이 1/3이라고 해석하지 않습니다. 실제 ISR 수, 우선순위, 큐 구현과 메모리 순서가 추가되면 더 많은 상태를 확인해야 합니다.

PCW의 보존 경로에서는 payload를 먼저 처리한 뒤 pending 1이 남을 수 있습니다. 다음 반복에서 알림을 한 번 더 소비하고 빈 큐를 확인하는 것은 허용되는 추가 깨움입니다. 알림 숫자를 곧바로 payload의 정확한 개수나 ID로 해석하지 않는 이유입니다. 반대로 이미 도착한 pending을 W 직전에 0으로 지우는 결함 경로는 CPW를 다시 실패시켰습니다.

`--inject notify-clear` 실행은 실제로 종료 코드 1을 반환했고 JSON에 `ContractError: payload not consumed: []`를 남겼습니다. 이는 모델에 넣은 임의 삭제의 실패이며, `xTaskNotifyWait()`의 특정 비트 소거 옵션이 잘못됐다는 뜻은 아닙니다.

## 4. 깨움과 데이터 보관을 구별합니다

알림은 작업 도착을 알려 주는 신호이고, DMA 버퍼나 작업 객체는 payload입니다. 알림 하나만으로 여러 완료 버퍼의 주소·크기·소유권을 모두 저장할 수는 없습니다. payload는 별도의 올바른 큐나 버퍼 소유권 규약으로 유지해야 합니다.

자체 묶음 예제에는 payload 42·43과 도착 알림 값 2가 있습니다. `ulTaskNotifyTake(pdTRUE, ...)`처럼 종료할 때 알림 값을 모두 지우는 형태를 가정합니다. 반환값 2를 얻고 pending은 0이 됩니다. 그런데 큐에서 42 한 개만 처리하고 다음 알림을 기다리면 43이 남습니다.

| 처리 정책 | 소비 값 | 남은 payload | 남은 알림 | 다시 기다리면 |
| --- | --- | --- | --- | --- |
| 한 건만 처리 | `[42]` | `[43]` | 0 | 일이 남아도 잠들 수 있습니다. |
| 큐를 비울 때까지 처리 | `[42, 43]` | `[]` | 0 | 이 묶음의 작업은 남지 않습니다. |

`pdTRUE`는 종료 시 값을 0으로 지우는 선택이고 `pdFALSE`는 값을 하나 감소시키는 선택입니다. 사용하는 방식에 맞춰 소비 정책을 정해야 합니다. 이 예제는 최대 두 알림만 다루며 실제 32비트 알림 값의 넘침이나 포화 정책은 모델링하지 않습니다. [FreeRTOS 공식 ulTaskNotifyTake 설명](https://freertos.org/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake)

## 5. 실제 코드에 적용할 때의 형태

이미 FreeRTOS queue를 사용한다면 대기 시간을 지정한 `xQueueReceive()` 하나로 데이터 전달과 대기를 묶는 방법을 먼저 살펴볼 수 있습니다. 알림과 큐 두 개가 반드시 필요한 것은 아닙니다. 별도의 완료 버퍼 목록이나 SPSC 링을 쓰며 태스크 알림으로 깨우는 경우에는 다음 계약이 필요합니다.

아래 C 형태는 API 연결을 설명하기 위한 예시이며, Python 검사에서 빌드한 코드는 아닙니다. `pop_completed_buffer()`와 `process_buffer()`는 여기서 구현한 드라이버 함수가 아니며 실제 큐 동기화·반환 규약이 필요합니다.

```c
for (;;) { // for(;;)는 종료 조건이 없는 반복입니다.
    ulTaskNotifyTake(pdTRUE, portMAX_DELAY); // 대기 전에 도착한 알림도 API 규약에 따라 소비합니다.
    while (pop_completed_buffer(&item)) { // while은 큐에서 꺼낼 수 있는 동안 반복합니다.
        process_buffer(&item); // 처리 뒤 버퍼를 반환할 책임도 실제 설계에서 정합니다.
    }
}
```

생산자는 payload 공개에 성공한 다음 알림을 보냅니다. 큐가 가득 차 공개가 실패하면 손실·재시도 정책을 실행해야 하며 성공 알림으로 감추지 않습니다. 실제 ISR에서는 태스크용 `xTaskNotifyGive()` 대신 해당 `FromISR` API와 포트의 문맥 전환 규약을 확인합니다. 같은 태스크 알림 인덱스를 다른 용도로 함께 덮어쓰는 일도 피해야 합니다.

## 6. 지연을 넣어서 안 보이게 하는 방법과 구분합니다

W 직전 sleep을 넣거나 타임아웃을 짧게 만들어 큐를 다시 확인하면 특정 실행에서 증상이 사라질 수 있습니다. 하지만 검사와 등록의 계약을 묶은 것은 아닙니다. 타임아웃으로 재확인하는 정책을 택했다면 최악 추가 지연과 반복 비용을 허용 요구에 포함해야 합니다.

실제 추적에는 payload ID, 공개 시각, 알림 인덱스·값, 대기 진입/복귀, 소비·버퍼 반환, 큐 가득 참을 함께 기록합니다. 마지막 로그에 “알림 보냄”만 남아 있으면 대상 태스크가 그때 대기 중이었는지, 값이 저장됐는지, 뒤에서 소거됐는지 구별하기 어렵습니다. 단순 재부팅으로 복구한 결과와 원인을 제거한 결과도 분리해 남깁니다.

## 확인 문제

1. 큐가 비었다고 확인한 직후의 `vTaskSuspend()`가 안전한 이유를 그 확인만으로 만들 수 있습니까?
2. 알림 값 2를 지운 뒤 payload 한 건만 처리하면 어떤 일이 남습니까?
3. 보존된 알림을 소비했지만 큐가 비어 있다면 반드시 오류입니까?

답: 1. 아닙니다. 검사와 대기 사이에 생산자가 올 수 있습니다. 2. 나머지 payload를 깨울 알림이 없어 다음 도착까지 처리하지 못할 수 있습니다. 3. 아닙니다. 이미 payload를 처리한 동안 알림이 남았다면 추가 깨움일 수 있으므로 실제 작업 조건을 다시 확인합니다.

## English

The fixture enumerates publication before, between, and after a queue check and wait. Resume-only signaling loses the CPW arrival, while a retained notification permits all three payloads to be consumed. A separate batch exposes clearing two notifications but processing only one queued item. Fault injection that clears pending state before waiting fails verification. The model assumes atomic notification-check/wait registration and abstracts wake-to-consume scheduling; it does not execute FreeRTOS or an ISR.

## 출처와 실제 열람 범위

- [FreeRTOS-Kernel V11.1.0 task.h](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/include/task.h): `vTaskSuspend`·`vTaskResume`·`xTaskResumeFromISR`의 계약을 읽었습니다.
- [V11.1.0 tasks.c](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/V11.1.0/tasks.c): `ulTaskGenericNotifyTake()`의 확인·대기 등록·종료 시 소거/감소, `xTaskGenericNotify()`의 값을 증가시키는 경로를 읽었습니다.
- [공식 ulTaskNotifyTake 문서 원문](https://github.com/FreeRTOS/FreeRTOS-Website-Content/blob/main/content/en-us/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake.md): 반환값·인덱스·소거 선택을 2026-10-21에 대조했습니다. 웹의 현행 설명과 고정 커널 태그를 구분합니다.
- 세 사건·payload 42/43·임의 소거 결함·oracle은 자체 교육 예제입니다. 커널 전체나 대상 포트의 실행 검증은 수행하지 않았습니다.
