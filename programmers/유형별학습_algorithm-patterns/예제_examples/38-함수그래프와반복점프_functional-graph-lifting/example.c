#include <stdio.h>  // 표준 입력과 출력 함수

int main(void) {  // 고정 함수의 반복 질의 처리
    int n, q, jump[20][30];  // 백만 단계까지 덮는20층
    scanf("%d %d", &n, &q);  // 정점과 질의 수
    for (int v = 0; v < n; ++v) scanf("%d", &jump[0][v]);  // 한 단계 후속 정점
    for (int bit = 1; bit < 20; ++bit) {  // 두 배 이동의 층 구축
        for (int v = 0; v < n; ++v) jump[bit][v] = jump[bit - 1][jump[bit - 1][v]];  // 첫 절반 도착점에서 두 번째 절반
    }  // 전처리 끝
    for (int i = 0; i < q; ++i) {  // 원래 질의 순서
        int vertex, steps, bit = 0;  // 현재 정점과 남은 이동
        scanf("%d %d", &vertex, &steps);  // 시작과 단계 수
        while (steps > 0) {  // 아직 처리하지 않은 비트
            if (steps & 1) vertex = jump[bit][vertex];  // 필요한 길이만 현재 정점에 적용
            steps >>= 1; ++bit;  // 처리한 비트를 제거하고 다음 층 이동
        }  // 모든 선택 점프 합성 끝
        printf("%d\n", vertex);  // 최종 후속 정점
    }  // 질의 처리 끝
    return 0;  // 정상 종료
}  // 프로그램 끝
