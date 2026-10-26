# 펌웨어·통신 검사와 공개 코드 | Firmware and communication tests with upstream code

[직무 목차](../README.md) · [DX 직무](../01-삼성DX의직무와요구역량_samsung-dx-role-map.md) · [DS 직무](../02-삼성DS의직무와요구역량_samsung-ds-role-map.md) · [SK하이닉스 직무](../03-SK하이닉스의직무와요구역량_sk-hynix-role-map.md) · [펌웨어·SW 기초](../05-펌웨어와소프트웨어검증_firmware-software-validation.md)

펌웨어 검사는 보드에 전원이 들어오는지 확인하는 데서 끝나지 않습니다. 같은 데이터가 전선·주변장치·인터럽트·큐·응용을 지나면서 어느 지점에서 달라지는지 나누어야 합니다. 이 글은 실제 공개 RTOS인 Zephyr의 공식 C 샘플과 Python 검사 코드를 읽고, 그 코드로 관찰할 수 있는 업무 문제를 연결합니다. [Zephyr의 상용 제품 목록](https://www.zephyrproject.org/products-running-zephyr/)은 RTOS의 실제 제품 활용을 보여 줍니다. 아래 `samples` 코드 자체가 그 제품에 그대로 들어갔거나 삼성·SK하이닉스가 사용한다는 근거는 아닙니다.

코드는 Zephyr `v4.2.0`, commit `413b789deb391d3a37d06b463288a5fe765ee57e`에서 발췌했습니다. 표와 고장 분석 순서는 이 코드의 동작을 설명하기 위해 구성한 검사 계획이며, 회사의 실제 장애 보고서나 이번 작업에서 측정한 결과가 아닙니다. 새 C·Python 알고리즘은 만들지 않았습니다.

| 직무와 연결할 업무 | 사례 | 확인할 결과물 |
| --- | --- | --- |
| DX 미래로봇추진단 시스템 SW, 보드·제어기 펌웨어 | [UART 수신 누락](#uart) | 입력 바이트, 인터럽트 수신, 큐 전달, 응용 처리의 대응입니다. |
| DX 미래로봇추진단의 CAN 연동, 제어·설비 장치 통신 | [CAN 수신 실패](#can) | 버스 파형·프레임·필터·길이·컨트롤러 상태를 연결한 원인 분리입니다. |
| DX 품질/서비스의 SW 시험 플랫폼, SK Solution SW의 검증 인프라, DS SW 품질 | [Python 호스트와 기기 시험](#python-harness) | 빌드·기기 준비·명령·응답·판정·보고서를 잇는 실행 기록입니다. |

직무 이름은 담당 업무의 연결을 위한 것입니다. 예를 들어 SK Solution SW의 SSD 검증을 UART echo 시험 하나로 대신하거나, DS의 보안 직무를 CAN 개발 직무로 바꾸는 뜻은 아닙니다.

<a id="uart"></a>

## 1. UART 파형은 정상인데 수신한 문장이 빠집니다

### 검사 대상과 기초 원리

UART는 송신·수신 장치가 같은 전송 속도와 프레임 형식을 정하고 바이트를 주고받는 직렬 인터페이스입니다. 통신선에서 바이트를 수신하는 일과 그 바이트를 응용이 처리하는 일은 별도입니다. 인터럽트는 수신 사건이 생겼을 때 실행되는 처리 경로이고, 큐는 나중에 처리할 고정 크기 메시지를 잠시 보관하는 공간입니다.

공식 [UART echo 예제 설명](https://docs.zephyrproject.org/4.2.0/samples/drivers/uart/echo_bot/README.html)은 수신에는 인터럽트 API를, 송신에는 polling API를 사용합니다. [원본 C 파일 14–59행](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/drivers/uart/echo_bot/src/main.c#L14-L59)을 보면 줄바꿈을 만날 때 완성한 문자열을 메시지 큐에 넣습니다. 다른 실행 경로인 `main()`은 큐에서 꺼낸 문자열을 전송합니다.

| 검사 장비·도구 | 직접 확인할 항목 | 구분하려는 문제 |
| --- | --- | --- |
| 대상 보드와 UART 어댑터 | 보드의 I/O 전압, 접지, TX/RX 연결, baud·parity·stop bit 설정입니다. | 전기적 연결·설정 오류와 SW 처리 오류를 나눕니다. |
| 로직 분석기 | 수신 핀의 바이트, 줄바꿈, 전송 간격과 프레임 오류입니다. | PC가 보낸 내용과 보드 핀에 도착한 내용이 같은지 봅니다. |
| 오실로스코프 | 수신 핀의 전압·에지·노이즈·ground 기준입니다. | 디지털 디코더가 보여 주지 않는 전기적 원인을 찾습니다. |
| 디버거·RTOS 관측 도구 | 실제 적용된 설정, 수신 위치, 큐 상태, 응용의 실행 상태입니다. | 바이트 수신 뒤의 잘림·큐 포화·소비 지연을 나눕니다. |

UART 어댑터라는 이름만 보고 전압이 호환된다고 판단하지 않습니다. MCU 핀의 논리 전압과 RS-232 같은 별도 전기 규격은 다릅니다. 분석기의 디지털 디코딩과 오실로스코프의 실제 전압 관측도 서로 다른 근거입니다.

### 공식 C 코드에서 경계를 읽습니다

원본의 14–59행에서 빈 줄과 기존 영어 설명 주석을 덜어내고 한국어 줄 설명을 붙였습니다. 선언·식·함수 호출·조건은 원문과 같습니다. 전체 빌드에는 원문의 헤더·보드 설정·`main()`이 필요하므로 아래는 독립 실행 파일이 아닌 발췌입니다.

저작권은 `Copyright (c) 2022 Libre Solar Technologies GmbH`, 코드 라이선스는 `Apache-2.0`입니다. [라이선스 전문](licenses/Apache-2.0.txt)을 함께 제공합니다.

```c
#define UART_DEVICE_NODE DT_CHOSEN(zephyr_shell_uart) // #define은 매크로이며 장치 트리의 shell UART를 선택합니다.
#define MSG_SIZE 32                                 // 한 메시지를 저장할 배열 크기를 32바이트로 정합니다.
K_MSGQ_DEFINE(uart_msgq, MSG_SIZE, 10, 4);            // Zephyr 매크로로 32바이트 메시지 10개와 정렬 조건을 정의합니다.
static const struct device *const uart_dev = DEVICE_DT_GET(UART_DEVICE_NODE); // 장치 구조체를 가리키는 포인터를 얻습니다.
static char rx_buf[MSG_SIZE];                       // []는 배열이며 수신 문자를 임시 보관합니다.
static int rx_buf_pos;                             // static 변수는 수명을 유지하며 초기값은 0입니다.
void serial_cb(const struct device *dev, void *user_data) // void는 반환값 없음, *는 포인터 인수입니다.
{                                                  // 함수 본문을 시작합니다.
    uint8_t c;                                     // 부호 없는 8비트 정수로 수신 바이트를 받습니다.
    if (!uart_irq_update(uart_dev)) {               // if는 조건 분기, !는 참·거짓 반전이며 IRQ 상태를 갱신합니다.
        return;                                   // 갱신 조건을 만족하지 않으면 callback을 끝냅니다.
    }                                              // 첫 조건문을 닫습니다.
    if (!uart_irq_rx_ready(uart_dev)) {             // 수신 데이터가 준비됐는지 확인합니다.
        return;                                   // 수신 준비가 아니면 함수에서 나옵니다.
    }                                              // 두 번째 조건문을 닫습니다.
    while (uart_fifo_read(uart_dev, &c, 1) == 1) {   // &로 저장 주소를 전달하고 FIFO에서 1바이트씩 반복해 읽습니다.
        if ((c == '\n' || c == '\r') && rx_buf_pos > 0) { // ||는 또는, &&는 그리고이며 비어 있지 않은 줄의 끝을 찾습니다.
            rx_buf[rx_buf_pos] = '\0';             // 배열의 현재 위치에 C 문자열 종료 문자를 넣습니다.
            k_msgq_put(&uart_msgq, &rx_buf, K_NO_WAIT); // 큐로 복사하며 공간이 없어도 기다리지 않습니다.
            rx_buf_pos = 0;                       // 다음 문장을 받도록 위치를 되돌립니다.
        } else if (rx_buf_pos < (sizeof(rx_buf) - 1)) { // sizeof로 배열 크기를 구하고 종료 문자 1칸을 남깁니다.
            rx_buf[rx_buf_pos++] = c;             // 현재 칸에 저장한 뒤 ++로 위치를 하나 늘립니다.
        }                                          // 문장 끝·문자 저장의 분기를 닫습니다.
    }                                              // FIFO 읽기 반복을 닫습니다.
}                                                  // callback 함수를 닫습니다.
```

`const struct device *const`에는 서로 다른 두 제한이 있습니다. 앞의 `const`는 이 포인터를 통해 장치 구조체를 수정하지 않겠다는 뜻이고, 뒤의 `const`는 포인터가 다른 장치를 가리키도록 바뀌지 않게 합니다. `&rx_buf`는 원본이 사용하는 배열의 주소이며, `k_msgq_put()`은 정해진 크기의 내용을 복사합니다. 포인터를 큐에 보관한다는 뜻이 아닙니다. [Zephyr 메시지 큐의 복사·용량 설명](https://docs.zephyrproject.org/4.2.0/kernel/services/data_passing/message_queues.html)을 함께 읽으시면 됩니다.

### 정상·이상 결과를 어떻게 해석하나요

| 관측 또는 시험 입력 | 코드에서 확인할 수 있는 동작 | 결과 해석 |
| --- | --- | --- |
| 짧은 문장 뒤에 줄바꿈을 보냅니다. | 문장을 종료하고 큐로 전달합니다. | 보드 수신·큐 전달·응용 송신이 연결됐는지 비교하는 기본 입력입니다. 공식 README의 echo 출력은 제작자가 제시한 예시입니다. |
| 줄바꿈 없이 바이트만 보냅니다. | 문장이 완성되지 않아 아직 큐에 넣지 않습니다. | echo가 없다는 사실만으로 UART 수신 불량이라고 판단하지 않습니다. |
| 31바이트를 넘는 한 줄의 데이터를 보냅니다. | 종료 문자 자리를 남기고 추가 문자를 버립니다. | 이 샘플의 길이 제한입니다. 이 동작을 전기적 바이트 손상과 구분합니다. |
| 완성 문장이 소비 속도보다 빨리 쌓입니다. | 큐 공간이 없을 때 `K_NO_WAIT` 삽입은 기다리지 않습니다. 원문은 그 반환값을 사용하지 않고 버퍼를 초기화합니다. | 실제로 삽입이 실패했다면 문장이 사라질 수 있습니다. 핀의 파형이 정상이어도 응용의 수신 수가 작아지는 경로입니다. |
| 응용이 느려진 순간만 누락됩니다. | 수신 경로와 큐를 비우는 경로는 분리돼 있습니다. | 스케줄링·출력 지연·큐 포화를 후보로 두고 시간 관계를 확인합니다. |

32바이트라는 수는 이 코드의 배열 크기이고 유효 문자열 데이터의 최대 길이는 31바이트입니다. UTF-8 문자는 여러 바이트를 사용할 수 있어 글자 수와 배열 용량을 같게 세지 않습니다. 또 수신 버퍼가 비었을 때의 CR·LF는 첫 조건을 만족하지 않아 `else if`에서 저장될 수 있습니다. 이 코드를 빈 줄 무시나 CRLF 정규화 구현으로 읽지 않고 CR·LF·CRLF·빈 줄을 각각 경계 입력으로 비교해야 합니다.

큐 용량 10개 역시 이 예제의 설정이지 UART 하드웨어가 열 바이트만 받는다는 뜻이 아닙니다. 대기 중인 수신자 없이 이미 완성한 메시지 10개가 큐에 쌓여 있다고 가정하면 다음 메시지는 추가 공간을 얻지 못합니다. 이는 코드에서 도출한 조건 설명이며 실물에서 확인한 유실 개수는 아닙니다.

### 원인 분리와 수정 확인

1. 전송한 원시 바이트와 보드 핀의 디코딩 결과를 먼저 비교합니다. 이 단계가 다르면 설정·배선·전압·잡음을 조사합니다.
2. 핀의 내용이 같으면 줄바꿈과 길이 제한을 비교합니다. 같은 입력이 항상 같은 지점에서 잘리는지 확인합니다.
3. 짧고 유효한 문장도 부하에서 빠지면 큐 삽입 실패·소비 속도·인터럽트 및 task 실행을 관측합니다. 큐 크기만 늘리기 전에 생산 속도와 소비 속도를 나눕니다.
4. 수정 설계에서는 삽입 실패의 기록, 흐름 제어·송신 속도 계약, 과부하 정책, 소비 경로의 지연을 검토합니다. 여기에는 새 구현 코드를 제시하지 않았으며, 원본 샘플을 이미 제품용으로 수정했다고 표시하지 않습니다.
5. 길이 경계, 빈 줄·CR/LF 조합, 짧은 burst, 지속 부하와 재시작을 같은 판본·입력으로 다시 비교합니다. 처리한 문장 수와 버린 문장 수의 합이 입력과 맞는지 기록합니다.

Python이 들어간다면 PC의 송신 시나리오·원시 로그·반복 실행을 관리하는 위치입니다. Python의 실행 시각만으로 MCU의 인터럽트 지연을 측정할 수는 없습니다. 보드 안의 사건과 실제 핀 전환 시각을 보려면 그 목적에 맞는 추적·계측이 필요합니다.

<a id="can"></a>

## 2. CAN 분석기에는 프레임이 보이는데 제어기는 값을 받지 못합니다

### 검사 대상과 기초 원리

CAN에서는 컨트롤러가 프레임 형식·중재·오류 처리를 담당하고, 트랜시버가 CAN_H·CAN_L의 전기 신호와 연결합니다. 그 위의 수신 필터는 응용에 필요한 ID만 받도록 고릅니다. ID는 프레임을 식별하는 값이며 단순한 장치의 주소와 같지 않습니다. 수신 대기열과 응용의 값 해석도 다시 별도 단계입니다.

[공식 CAN counter 샘플의 README](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/drivers/can/counter/README.rst)는 standard·extended ID의 송수신, 메시지 큐·work queue, loopback 구성을 설명합니다. [같은 판본의 CAN API 설명](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/doc/hardware/peripherals/can/controller.rst)은 ID·mask·전송 완료와 컨트롤러 상태를 나눕니다.

| 장비·설정 | 측정·기록할 항목 | 원인 분리 |
| --- | --- | --- |
| CAN 분석기와 두 번째 정상 노드 | ID 종류, DLC, payload, 시간, 오류 프레임·ACK 관련 상태입니다. | 실제 버스 교환과 응용 수신을 비교합니다. |
| 오실로스코프·적절한 차동 측정 | CAN_H/CAN_L의 파형·반사·노이즈와 신호 기준입니다. | 프레임 해석 전에 전기적 문제를 찾습니다. |
| 보드 회로도·트랜시버 설정 | 배선·종단·전원·standby·enable 설정입니다. | 컨트롤러가 정상이어도 버스에 연결되지 않는 경로를 확인합니다. |
| CAN 컨트롤러 상태·드라이버 로그 | error-active·error-passive·bus-off, 송수신 오류 카운터와 API 반환값입니다. | 정상 수신, 송신 실패, 상태 조회 실패를 구분합니다. |
| 응용 수신 로그 | 적용 필터, 큐 전달, payload 길이·값·처리 시각입니다. | 유효 프레임이 필터·큐·파서 중 어디서 제외되는지 봅니다. |

loopback은 장치가 자기 메시지를 받아보는 설정입니다. 이 샘플이 loopback에서 동작한다고 외부 트랜시버·케이블·상대 노드까지 정상이라고 결론 내릴 수는 없습니다. 반대로 외부 분석기에 프레임이 보이더라도 원하는 제어기가 해당 ID를 응용에 전달했다는 증거는 아닙니다.

### 공식 C 코드의 필터와 데이터 길이

다음은 [원본 `main.c` 60–91행](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/drivers/can/counter/src/main.c#L60-L91)입니다. 빈 줄을 생략하고 한국어 주석을 추가했습니다. 함수·조건·식은 바꾸지 않았습니다. 파일 앞의 `COUNTER_MSG_ID`는 `0x12345`이고 `counter_msgq`의 용량은 2프레임입니다. 선언과 장치 초기화는 원본 전체에서 확인합니다.

저작권은 `Copyright (c) 2018 Alexander Wachter`, 라이선스는 `Apache-2.0`입니다. [라이선스 전문](licenses/Apache-2.0.txt)을 함께 제공합니다.

```c
void rx_thread(void *arg1, void *arg2, void *arg3) { // void *는 범용 포인터이며 Zephyr thread 인수를 받습니다.
    ARG_UNUSED(arg1);                              // 사용하지 않는 인수를 명시하는 Zephyr 매크로입니다.
    ARG_UNUSED(arg2);                              // 두 번째 인수도 이 함수에서는 사용하지 않습니다.
    ARG_UNUSED(arg3);                              // 세 번째 인수도 사용하지 않습니다.
    const struct can_filter filter = {             // struct는 필드 묶음이며 수신 필터를 초기화합니다.
        .flags = CAN_FILTER_IDE,                   // .필드 문법으로 extended ID를 고릅니다.
        .id = COUNTER_MSG_ID,                      // 이 예제가 받을 ID 상수를 지정합니다.
        .mask = CAN_EXT_ID_MASK                    // extended ID 전체를 비교할 mask를 지정합니다.
    };                                             // 구조체 초기화를 끝냅니다.
    struct can_frame frame;                        // 수신한 프레임을 보관할 구조체 변수입니다.
    int filter_id;                                 // 필터 등록의 반환값을 받을 정수입니다.
    filter_id = can_add_rx_filter_msgq(can_dev, &counter_msgq, &filter); // 필터와 수신 큐의 주소를 드라이버에 전달합니다.
    printf("Counter filter id: %d\n", filter_id);    // %d로 등록 결과를 출력합니다.
    while (1) {                                    // 1은 참이므로 수신 처리를 반복합니다.
        k_msgq_get(&counter_msgq, &frame, K_FOREVER); // 큐에 프레임이 들어올 때까지 기다립니다.
        if (IS_ENABLED(CONFIG_CAN_ACCEPT_RTR) && (frame.flags & CAN_FRAME_RTR) != 0U) { // 설정·비트 flag로 RTR 여부를 검사합니다.
            continue;                              // 해당 프레임을 건너뛰고 다음 반복으로 갑니다.
        }                                          // RTR 분기를 닫습니다.
        if (frame.dlc != 2U) {                      // !=는 다름, U는 unsigned이며 이 형식은 길이 2를 기대합니다.
            printf("Wrong data length: %u\n", frame.dlc); // %u로 실제 길이를 출력합니다.
            continue;                              // 예상 형식이 아니면 값을 읽지 않습니다.
        }                                          // 길이 검사를 닫습니다.
        printf("Counter received: %u\n",           // 정상 경로에서 해석한 카운터를 출력합니다.
               sys_be16_to_cpu(UNALIGNED_GET((uint16_t *)&frame.data))); // 정렬을 고려해 16비트를 읽고 big-endian에서 CPU 형식으로 바꿉니다.
    }                                              // 수신 반복을 닫습니다.
}                                                  // thread 함수를 닫습니다.
```

big-endian은 여러 바이트로 된 수에서 큰 자릿수 바이트가 먼저 오는 표현입니다. 이 코드의 형식에 맞춰 payload를 `01 02`로 정하면 16비트 값은 `1×256+2=258`입니다. 이는 직접 계산한 해석 예이며 이 장치에서 측정한 값은 아닙니다. DLC를 확인하지 않고 무조건 두 바이트를 읽으면 짧은 프레임의 의미를 잘못 해석할 수 있습니다.

### 관측 결과와 경쟁 원인

| 관측 결과 | 우선 비교할 원인 | 다음 확인 |
| --- | --- | --- |
| 분석기에는 프레임이 있지만 이 callback 경로에는 없습니다. | standard/extended 구분·ID·mask·필터 등록 실패입니다. | 필터의 반환값과 실제 프레임 속성을 나란히 저장합니다. 같은 숫자처럼 보여도 ID 형식이 맞는지 봅니다. |
| `Wrong data length`가 나옵니다. | 송신기와 수신기의 payload 계약이 다릅니다. | 이 코드의 2바이트 형식과 송신기 판본·DLC를 비교합니다. |
| 수신은 되지만 값이 다릅니다. | endian·폭·부호·판본 또는 송신 데이터 자체의 문제입니다. | 분석기의 raw payload와 응용이 해석한 정수를 같은 프레임에 대응합니다. |
| 부하에서만 카운터 값이 건너뜁니다. | 실제 송신 누락, 버스·드라이버 오류, 수신 큐 포화, 응용 소비 지연입니다. | 버스의 프레임 개수와 수신 큐·응용 개수를 나누어 비교합니다. |
| 송신 오류와 bus-off가 관측됩니다. | 물리 연결·bit timing·상대 노드·전원·종단 등 여러 원인이 남습니다. | 상태 변화 전후의 파형·오류 카운터·설정을 함께 확인합니다. bus-off를 단일 부품 불량의 확정 증거로 쓰지 않습니다. |
| 상태 조회 API 자체가 실패합니다. | 미지원 기능·드라이버 상태·장치 접근 문제입니다. | 조회 실패를 오류 카운터 0으로 저장하지 않고 별도 오류로 기록합니다. |

원본의 [상태 조회 경로 135–167행](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/drivers/can/counter/src/main.c#L135-L167)은 `can_get_state()`의 반환값을 검사한 뒤 상태·송수신 오류 수가 변했을 때 출력합니다. 상태 조회가 성공했는지와 읽힌 값이 정상인지가 다른 질문이라는 실제 코드 예입니다.

### 원인 분리와 수정 확인

1. loopback과 외부 두 노드 구성을 나누어 비교합니다. 내부 경로가 정상인 것과 외부 버스가 정상인 것을 별도 결과로 남깁니다.
2. 하나의 유효 ID·정한 길이·낮은 부하로 필터와 값 해석을 확인합니다. 그 뒤 필터 경계·다른 ID 형식·잘못된 길이를 대조합니다.
3. 통신 오류가 있으면 전원·트랜시버 모드·배선·종단·bit timing을 실제 구성과 맞춥니다. 송신 성공·ACK와 상대 응용의 처리 완료도 나누어 기록합니다.
4. 유효 프레임만 부하에서 누락되면 큐와 소비 경로를 조사합니다. 큐를 늘리는 것, 송신 부하를 제한하는 것, 처리 시간을 줄이는 것은 다른 조치이며 어느 조건에 필요한지 비교합니다.
5. 조치 뒤에는 같은 입력 부하·케이블·노드·판본에서 프레임 수·오류·응답 시간·복구를 다시 확인합니다. 재시작으로 bus-off 표시만 사라졌다고 원인 제거를 선언하지 않습니다.

<a id="python-harness"></a>

## 3. C 펌웨어와 Python 호스트를 연결해 기기 시험을 반복합니다

### 검사 대상과 기초 원리

기기 안의 C 코드는 실제 명령을 처리하고, PC의 Python 코드는 명령을 보내고 응답을 검사할 수 있습니다. 이때 Python이 하드웨어 제어 루프를 대신하는 것은 아닙니다. pytest는 시험 함수를 찾아 실행하고 assertion으로 기대한 조건을 확인하는 프레임워크입니다. fixture는 시험에 필요한 기기 연결 같은 준비·정리된 자원을 함수에 전달하는 장치입니다.

[Zephyr 4.2.0의 pytest 통합 설명](https://docs.zephyrproject.org/4.2.0/develop/test/pytest.html)은 Twister가 빌드·기기 실행과 pytest 호출을 연결하고 보고서를 읽는 구조를 설명합니다. [공식 shell 시험의 README](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/subsys/testsuite/pytest/shell/README.rst)는 `help` 응답과 kernel version 응답을 검사하는 예입니다.

| 위치·장비 | 실제 역할 | 기록할 항목 |
| --- | --- | --- |
| PC의 Twister·pytest | 빌드 조건과 시험 실행을 관리합니다. | commit·도구판본·보드·설정·시험 ID·보고서입니다. |
| 대상 보드·디버그 프로브 | 이미지 실행·reset·flash를 수행합니다. | 보드 식별·실행 이미지·전원/reset·flash 결과입니다. |
| UART 연결 또는 native/QEMU adapter | 명령·응답을 전달합니다. | 연결 형식·원시 출력·timeout·prompt와 실제 DUT 종류입니다. |
| 기기의 shell 기능 | `kernel version` 같은 명령을 처리합니다. | 받은 명령과 결과를 처리한 펌웨어 판본입니다. |

공식 [`testcase.yaml`](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/subsys/testsuite/pytest/shell/testcase.yaml)에는 `native_sim`·`qemu_cortex_m3` 등의 시험 구성이 있습니다. native simulator에서 성공한 기록과 실제 보드에서 성공한 기록은 측정 대상이 다릅니다. 여기서는 Twister를 실행하거나 기기에 새 이미지를 기록하지 않았습니다.

### 공식 Python 시험 코드

다음은 [원본 `test_shell.py` 5–9·19–23행](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/subsys/testsuite/pytest/shell/pytest/test_shell.py#L5-L23)의 imports·logger와 version 검사 함수입니다. 가운데 `help` 검사 함수와 빈 줄만 생략하고 한국어 주석을 추가했습니다. 명령·판정식은 원문과 같습니다.

저작권은 `Copyright (c) 2023 Nordic Semiconductor ASA`, 라이선스는 `Apache-2.0`입니다. [라이선스 전문](licenses/Apache-2.0.txt)을 함께 제공합니다.

```python
import logging  # import는 모듈을 가져오며 logging은 실행 경로를 기록하는 표준 라이브러리입니다.
from twister_harness import Shell  # from ... import는 모듈에서 Shell이라는 기기 shell 도우미를 가져옵니다.
logger = logging.getLogger(__name__)  # 현재 모듈 이름에 대응하는 logger를 얻고 =로 변수에 저장합니다.
def test_shell_print_version(shell: Shell):  # def는 함수 정의이며 shell: Shell은 인수의 타입 힌트입니다.
    logger.info('send "kernel version" command')  # 작은따옴표 문자열을 정보 수준의 로그로 남깁니다.
    lines = shell.exec_command('kernel version')  # .로 메서드를 호출하고 기기의 응답 문자열 목록을 받습니다.
    assert any(['Zephyr version' in line for line in lines]), 'expected response not found'  # []는 리스트 내포, in은 포함 검사, any는 하나라도 참인지 확인하며 assert로 판정합니다.
    logger.info('response is valid')  # assertion을 통과한 뒤 응답이 확인됐다는 로그를 남깁니다.
```

여기서 `shell` 인수는 이 파일에서 새 장치를 만드는 변수가 아닙니다. pytest의 fixture가 준비한 객체를 주입합니다. [같은 commit의 `Shell.exec_command()` 구현](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/scripts/pylib/pytest-twister-harness/src/twister_harness/helpers/shell.py)은 전송·echo·prompt·timeout을 다룹니다. Python 발췌만 일반 인터프리터에서 실행한다고 기기 시험이 준비되는 것은 아닙니다.

### 코드가 통과했다고 무엇을 확인한 것인가요

이 assertion은 응답 목록 어딘가에 `Zephyr version` 문자열이 있는지 검사합니다. 정확한 commit·제품 firmware ID·하드웨어 revision이 일치하는지까지 검사하지 않습니다. 원문에서 하지 않는 비교를 이 코드의 기능으로 덧붙이지 않습니다.

| 결과 | 해석 | 추가로 구분할 원인 |
| --- | --- | --- |
| 기대 문자열이 포함됩니다. | 이 입력에서 version 응답의 존재를 확인했습니다. | 의도한 보드·이미지인지, 정확한 판본 값까지 일치하는지는 별도입니다. |
| prompt를 기다리다 timeout이 납니다. | 기기를 사용할 준비가 됐다는 신호를 확인하지 못했습니다. | 부팅·flash·reset·UART 설정·잘못된 포트·다른 prompt를 나눕니다. |
| 명령 응답은 있지만 assertion이 실패합니다. | 받아온 출력이 이 시험의 기대 표현과 다릅니다. | 잘못된 이미지, 기능 구성, 출력 형식 변경, 응답 유실을 대조합니다. |
| 한 번 성공하고 다음 시험에서 실패합니다. | 재현 조건·자원 공유·reset·이전 출력의 영향을 조사해야 합니다. | fixture 범위, 연결 점유, 이전 시험 상태와 원시 출력의 시점을 봅니다. |
| PC 로그에는 명령 전송만 있습니다. | 전송 요청과 기기의 실행 완료를 아직 연결하지 못했습니다. | 실제 수신, 실행, 응답, 호스트 취득 단계의 어느 경계인지 조사합니다. |

### 불량 분석과 재검사 계획

시작점은 ‘Python 시험이 빨갛게 나왔다’가 아니라 실패한 단계입니다. 빌드 실패, 기기 준비 실패, 전송·수신 timeout, 내용 불일치는 다른 사건으로 저장합니다. 기기 준비 실패를 제품 기능 불량으로 집계하면 기능 실패율도 틀어집니다.

실무에 맞게 시험을 확장한다면 기대 firmware ID·기능 구성·응답 형식·명령의 부작용·timeout을 별도 계약으로 정해야 합니다. 이 글에는 그 확장 코드를 추측해서 추가하지 않았습니다. 원문 시험의 판단 범위와 추가로 설계해야 할 범위를 구분했습니다.

재검사에는 같은 이미지·보드·전원/reset 순서·명령·기대 응답·호스트 도구 판본을 남깁니다. 통과한 보고서뿐 아니라 실패한 원시 serial 출력과 fixture 준비 로그도 보존합니다. 결과의 공통 구분은 [검사 결과 판정과 기록](../11-검사결과의판정과기록_test-decisions-evidence.md)에서 이어집니다.

## 출처·라이선스와 확인 범위

| 자료 | 사용한 범위와 코드의 성격 |
| --- | --- |
| [Zephyr v4.2.0 commit](https://github.com/zephyrproject-rtos/zephyr/tree/413b789deb391d3a37d06b463288a5fe765ee57e) | 태그가 가리키는 commit을 고정했습니다. 현재 최신판이라고 표시하지 않았습니다. |
| [UART `echo_bot/src/main.c`](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/drivers/uart/echo_bot/src/main.c) | 공식 API 사용 샘플입니다. 14–59행의 장치·큐·버퍼·callback을 설명하며 queue-full 및 길이 제한 동작을 읽었습니다. |
| [CAN `counter/src/main.c`](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/drivers/can/counter/src/main.c) | 공식 송수신 샘플입니다. 60–91행의 수신 함수와 135–167행의 상태 조회, 앞부분의 ID·큐 선언을 확인했습니다. |
| [Python `test_shell.py`](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/subsys/testsuite/pytest/shell/pytest/test_shell.py) · [실행 구성](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/samples/subsys/testsuite/pytest/shell/testcase.yaml) | 저장소에 있는 실제 pytest 시험 예제입니다. imports·logger와 version 시험을 발췌하고 공식 harness 구현·실행 종류를 대조했습니다. |
| [Zephyr 원문 LICENSE](https://github.com/zephyrproject-rtos/zephyr/blob/413b789deb391d3a37d06b463288a5fe765ee57e/LICENSE) · [제공 사본](licenses/Apache-2.0.txt) | 발췌 코드의 Apache-2.0 표시와 저작권을 보존했습니다. 수정은 빈 줄·기존 설명 주석 생략과 한국어 설명 주석 추가입니다. |

확인일은 2026-10-26입니다. 원본 코드·라이선스·설명 문서를 대조했으며 Zephyr 빌드, 실기기 UART/CAN 전송, 오실로스코프 측정, Twister 실행은 이번 자료 작성에서 수행하지 않았습니다. 현장에 적용할 때 남길 시험 조건과 판단 순서를 정리한 글입니다.

## English

The cases follow UART reception through an interrupt and fixed-size message queue, CAN frames through filters and payload validation, and a C device application through Zephyr's Python Twister/pytest harness. Every code excerpt is pinned to Zephyr v4.2.0 commit `413b789deb391d3a37d06b463288a5fe765ee57e` and carries its upstream attribution and Apache-2.0 license. Functional statements are retained; Korean line comments were added and omitted context is identified. Fault scenarios and investigation plans are explanatory, not measurements or evidence of internal Samsung or SK hynix adoption.
