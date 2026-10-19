#include "stm32f767xx.h"
#include "../common/validation.h"
#define WORDS 1024u
#define HSI_HZ 16000000u

// F767의 DMA는 DTCM에도 접근 가능하다. 여기선 cache 경로를 검사하려 SRAM1을 선택.
__attribute__((section(".dma"), aligned(32))) static uint32_t source[WORDS];
__attribute__((section(".dma"), aligned(32))) static uint32_t destination[WORDS];
static volatile uint32_t scratch[WORDS];
static volatile uint32_t ticks;
volatile struct { uint32_t cfsr, hfsr, bfar, mmfar; } fault_record;
typedef struct { uint32_t seq, errors, signature, cycles, first, expected, actual; } result_t;
static result_t last_result;
static uint32_t last_seq = UINT32_MAX;

void SysTick_Handler(void) { ++ticks; }
void HardFault_Handler(void)
{
    fault_record.cfsr=SCB->CFSR; fault_record.hfsr=SCB->HFSR;
    fault_record.bfar=SCB->BFAR; fault_record.mmfar=SCB->MMFAR;
    // BFAR/MMFAR는 CFSR의 주소-valid bit가 설정됐을 때만 유효한 실패 주소다.
    for (;;) __WFI(); // debugger로 record와 call stack을 읽을 수 있게 정지.
}
static void uart_char(char c)
{
    uint32_t t = ticks;
    while (!(USART3->ISR & USART_ISR_TXE)) if (ticks-t > 100u) return;
    USART3->TDR = (uint8_t)c;
}
static void uart_text(const char *s) { while (*s) uart_char(*s++); }
static void uart_number(uint32_t v)
{
    char buf[10]; uint32_t n=0;
    do { buf[n++]=(char)('0'+v%10u); v/=10u; } while (v);
    while (n) uart_char(buf[--n]);
}
static void field(const char *name, uint32_t v)
{
    uart_text(",\""); uart_text(name); uart_text("\":"); uart_number(v);
}
static void emit(const result_t *r)
{
    uart_text("{\"board\":\"STM32F767ZI\",\"version\":1");
    field("seq",r->seq); field("words",WORDS); field("errors",r->errors);
    field("first",r->first); field("expected",r->expected); field("actual",r->actual);
    field("signature",r->signature); field("cycles",r->cycles);
    field("elapsed_us",r->cycles/16u); // 이 예제는 16MHz HSI: 1µs=16cycles.
    uart_text("}\n");
}

static void board_init(void)
{
    // reset 직후 HSI=16MHz, AHB/APB prescaler=1 상태를 유지하는 startup을 사용.
    SCB->VTOR=0x08000000u; __DSB(); __ISB();
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN | RCC_AHB1ENR_GPIODEN | RCC_AHB1ENR_DMA2EN;
    RCC->APB1ENR |= RCC_APB1ENR_USART3EN;
    (void)RCC->AHB1ENR; // peripheral clock enable 뒤 read-back.
    GPIOB->MODER=(GPIOB->MODER & ~3u) | 1u; // PB0: NUCLEO-F767ZI green LED.
    GPIOD->MODER=(GPIOD->MODER & ~((3u<<16)|(3u<<18))) | (2u<<16)|(2u<<18);
    GPIOD->AFR[1]=(GPIOD->AFR[1] & ~0xffu) | 0x77u; // PD8 TX, PD9 RX, AF7.
    USART3->BRR=(HSI_HZ+115200u/2u)/115200u;
    USART3->CR1=USART_CR1_UE|USART_CR1_TE|USART_CR1_RE;
    SysTick_Config(HSI_HZ/1000u); // 1ms 시간 기반: polling에도 종료 조건 필요.
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
    DWT->CYCCNT=0; DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
    SCB_EnableICache(); SCB_EnableDCache();
}

static uint32_t dma_copy(void)
{
    DMA2_Stream0->CR &= ~DMA_SxCR_EN;
    uint32_t t=ticks;
    while (DMA2_Stream0->CR & DMA_SxCR_EN) if (ticks-t > 100u) return 1;
    DMA2->LIFCR=0x3du; // Stream0 FE/DME/TE/HT/TC flags를 write-one-to-clear.
    DMA2_Stream0->PAR=(uint32_t)source;
    DMA2_Stream0->M0AR=(uint32_t)destination;
    DMA2_Stream0->NDTR=WORDS;
    DMA2_Stream0->CR=(2u<<DMA_SxCR_DIR_Pos)|DMA_SxCR_PINC|DMA_SxCR_MINC|
                     (2u<<DMA_SxCR_PSIZE_Pos)|(2u<<DMA_SxCR_MSIZE_Pos);
    DMA2_Stream0->FCR=DMA_SxFCR_DMDIS|DMA_SxFCR_FTH; // M2M는 FIFO mode.
    // cache와 RAM 사이의 일관성은 volatile만으로 보장되지 않는다.
    SCB_CleanDCache_by_Addr((uint32_t *)source,sizeof(source));
    SCB_CleanInvalidateDCache_by_Addr((uint32_t *)destination,sizeof(destination));
    __DSB();
    DMA2_Stream0->CR |= DMA_SxCR_EN;
    t=ticks;
    while (!(DMA2->LISR & DMA_LISR_TCIF0)) {
        if ((DMA2->LISR & (DMA_LISR_TEIF0|DMA_LISR_DMEIF0|DMA_LISR_FEIF0)) ||
            ticks-t > 100u) { DMA2_Stream0->CR &= ~DMA_SxCR_EN; return 1; }
    }
    __DSB();
    SCB_InvalidateDCache_by_Addr((uint32_t *)destination,sizeof(destination));
    __DSB(); // 이제 CPU가 새 RAM 값을 읽게 한다.
    return 0;
}

static result_t run(uint32_t sequence)
{
    result_t r={0}; r.seq=sequence;
    uint32_t start=DWT->CYCCNT;
    memory_result_t m=march_c_minus(scratch,WORDS);
    r.errors=m.errors; r.first=m.first_index; r.expected=m.expected; r.actual=m.actual;
    for (uint32_t i=0;i<WORDS;i++) { source[i]=i^0xa5a55a5au; destination[i]=0; }
    if (dma_copy()) r.errors++;
    else for (uint32_t i=0;i<WORDS;i++) {
        if (destination[i]!=source[i]) {
            if (!r.errors) { r.first=i; r.expected=source[i]; r.actual=destination[i]; }
            r.errors++;
        }
    }
    r.signature=alu_signature();
    r.cycles=DWT->CYCCNT-start; // unsigned 뺄셈으로 32bit counter wrap 1회를 처리.
    GPIOB->BSRR=r.errors ? (1u<<16) : 1u;
    return r;
}

static int parse_sequence(const char *s, uint32_t *value)
{
    if (s[0]!='R'||s[1]!='U'||s[2]!='N'||s[3]!=','||!s[4]) return 0;
    uint32_t v=0;
    for (size_t i=4;s[i];i++) {
        if (s[i]<'0'||s[i]>'9') return 0;
        uint32_t digit=(uint32_t)(s[i]-'0');
        if (v>(0x7fffffffu-digit)/10u) return 0; // overflow 전에 입력을 거절.
        v=v*10u+digit;
    }
    *value=v; return 1;
}

int main(void)
{
    board_init(); char line[64]={0}; size_t used=0; int discard=0;
    for (;;) {
        if (USART3->ISR & USART_ISR_ORE) { USART3->ICR=USART_ICR_ORECF; discard=1; }
        if (!(USART3->ISR & USART_ISR_RXNE)) continue;
        char c=(char)USART3->RDR;
        if (discard) { if(c=='\n') { discard=0;used=0; } continue; }
        if (c=='\r') continue;
        if (c=='\n') {
            line[used]=0; uint32_t seq;
            if (used>=5 && parse_sequence(line,&seq)) {
                if (seq!=last_seq) { last_result=run(seq);last_seq=seq; }
                emit(&last_result);
            } else uart_text("{\"error\":\"bad_command\"}\n");
            used=0;
        } else if(used+1<sizeof(line)) line[used++]=c;
        else { discard=1; used=0; uart_text("{\"error\":\"line_too_long\"}\n"); }
    }
}
