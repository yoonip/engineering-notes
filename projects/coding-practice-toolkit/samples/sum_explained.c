/* 시작 예제: N개 정수의 합. input.txt의 5와 1 2 3 4 5를 읽으면 15입니다.
   stdio.h는 scanf(입력), printf(출력)를 제공합니다.
   정수 합의 표현 범위는 long long을 기준으로 한다. */
#include <stdio.h>

int main(void) {
    int n;  // 앞으로 읽을 정수의 개수입니다. 합에 N 자체를 더하지 않습니다.
    // scanf 반환값은 읽어 저장한 항목 수입니다. 입력이 없으면 정상 종료합니다.
    // &n은 n의 메모리 주소: scanf가 그 위치에 입력값을 저장합니다.
    if (scanf("%d", &n) != 1) return 0;
    long long sum = 0, value;  // 합은 반드시 0에서 시작합니다. 큰 합을 위해 long long을 씁니다.
    for (int i = 0; i < n; ++i) {
        // %lld는 long long용 입력 형식입니다. i=0부터 n-1까지 정확히 N개 읽습니다.
        if (scanf("%lld", &value) != 1) return 1;
        sum += value;  // sum = sum + value. 처리한 값들의 누적 합을 유지합니다.
    }
    printf("%lld\n", sum);  // 출력에는 &를 붙이지 않습니다. \n은 출력 줄바꿈입니다.
    return 0;
}
/* scanf는 필요한 개수만 읽으므로 유효한 입력 N개를 넣으면 EOF 없이도 계산을 마칩니다.
   Python의 전체 read()와 입력을 소비하는 방식이 다릅니다. F5는 input.txt 자동 입력을 사용합니다.
   시간 O(N), 추가 메모리 O(1). 합이 long long 범위를 넘는 입력까지 지원한다는 뜻은 아닙니다. */
