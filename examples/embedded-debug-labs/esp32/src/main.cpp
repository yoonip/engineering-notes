#include <Arduino.h>
#include <esp_timer.h>
#include <esp_heap_caps.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <freertos/semphr.h>
#include "../../common/validation.h"

struct Request { uint32_t sequence; };
static QueueHandle_t requests;
static SemaphoreHandle_t tx_mutex;
static char line[64];
static size_t used;
static bool discard;
static void print_line(const char *s)
{
    xSemaphoreTake(tx_mutex, portMAX_DELAY);
    Serial.println(s); // 문자열과 newline을 하나의 critical section으로 보호.
    xSemaphoreGive(tx_mutex);
}

static void worker(void *)
{
    // 내부 RAM을 명시적으로 선택한다. PSRAM인지 내부 SRAM인지 테스트 경계가 달라짐.
    auto *scratch = static_cast<uint32_t *>(
        heap_caps_malloc(1024 * sizeof(uint32_t), MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT));
    if (!scratch) { print_line("{\"fatal\":\"no_scratch_ram\"}"); vTaskDelete(nullptr); return; }
    uint32_t last = UINT32_MAX;
    char cached[320] = {0};
    Request req;
    for (;;) {
        if (xQueueReceive(requests, &req, portMAX_DELAY) != pdTRUE) continue;
        // timeout 후 같은 sequence 재요청은 결과만 재전송하여 중복 실행을 방지한다.
        if (req.sequence == last) { print_line(cached); continue; }
        const int64_t start = esp_timer_get_time();  // boot 이후의 µs, wall clock 아님.
        memory_result_t m = march_c_minus(scratch, 1024);
        volatile uint32_t sig = alu_signature();
        const int64_t elapsed = esp_timer_get_time() - start;
        snprintf(cached, sizeof(cached),
          "{\"board\":\"ESP32\",\"version\":1,\"seq\":%lu,\"words\":1024,"
          "\"errors\":%lu,\"first\":%lu,\"expected\":%lu,\"actual\":%lu,"
          "\"signature\":%lu,\"elapsed_us\":%lld}",
          (unsigned long)req.sequence, (unsigned long)m.errors,
          (unsigned long)m.first_index, (unsigned long)m.expected,
          (unsigned long)m.actual, (unsigned long)sig, (long long)elapsed);
        last = req.sequence;
        print_line(cached);
        // 실제 장치의 다른 task가 실행할 기회를 줘 task watchdog을 만족시킨다.
        vTaskDelay(pdMS_TO_TICKS(1));
    }
}

void setup()
{
    Serial.begin(115200);
    tx_mutex = xSemaphoreCreateMutex();
    if (!tx_mutex) { Serial.println("{\"fatal\":\"no_mutex\"}"); abort(); }
    requests = xQueueCreate(4, sizeof(Request));  // FIFO queue: 명령 burst를 버퍼링.
    if (!requests) { print_line("{\"fatal\":\"no_queue\"}"); abort(); }
    BaseType_t ok = xTaskCreatePinnedToCore(worker, "validation", 4096,
                                           nullptr, 1, nullptr, 0); // worker=core0, 기본 loop=core1.
    if (ok != pdPASS) { print_line("{\"fatal\":\"no_task\"}"); abort(); }
}

void loop()
{
    while (Serial.available()) {
        char ch = static_cast<char>(Serial.read());
        if (discard) { if (ch == '\n') { discard = false; used = 0; } continue; }
        if (ch == '\r') continue;
        if (ch == '\n') {
            line[used] = '\0';
            unsigned long seq; char extra;
            // %c가 읽히면 숫자 뒤에 쓰레기 문자가 있음을 뜻하므로 거절한다.
            if (sscanf(line, "RUN,%lu%c", &seq, &extra) == 1 && seq <= 0x7fffffffu) {
                Request r{static_cast<uint32_t>(seq)};
                if (xQueueSend(requests, &r, 0) != pdTRUE)
                    print_line("{\"error\":\"queue_full\"}");
            } else print_line("{\"error\":\"bad_command\"}");
            used = 0;
        } else if (used + 1 < sizeof(line)) line[used++] = ch;
        else { used = 0; discard = true; print_line("{\"error\":\"line_too_long\"}"); }
    }
    delay(1);  // busy-loop로 UART 수신 task를 굶기지 않는다.
}
