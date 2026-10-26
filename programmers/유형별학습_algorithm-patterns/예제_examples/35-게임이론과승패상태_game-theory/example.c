#include <stdio.h>  // 표준 입력과 출력 함수

int main(void) {  // 공평 게임의 독립 합 분석
    int k, n, moves[5], piles[8], grundy[31] = {0}, maximum = 0;  // 양의 이동과 작은 상태 상한
    scanf("%d %d", &k, &n);  // 이동 종류와 무더기 수
    for (int i = 0; i < k; ++i) scanf("%d", &moves[i]);  // 허용 이동량
    for (int i = 0; i < n; ++i) {  // 각 무더기 크기 입력
        scanf("%d", &piles[i]);  // 남은 돌 수
        if (piles[i] > maximum) maximum = piles[i];  // 필요한 DP 끝 상태
    }  // 무더기 입력 끝
    for (int stones = 1; stones <= maximum; ++stones) {  // 돌이 적은 상태부터 계산
        int seen[6] = {0};  // 다음 값은 최대5이므로 mex 범위6칸
        for (int i = 0; i < k; ++i) if (moves[i] <= stones) seen[grundy[stones - moves[i]]] = 1;  // 도달 가능한 그런디 값 표시
        int mex = 0;  // 없는 최소 음이 아닌 값
        while (seen[mex]) ++mex;  // 최대k개의 다음 값 밖으로 이동
        grundy[stones] = mex;  // 현재 상태의 그런디 값
    }  // DP 구축 끝
    int combined = 0;  // 독립 합의 XOR
    printf("GRUNDY");  // 무더기별 값의 줄 시작
    for (int i = 0; i < n; ++i) {  // 각 독립 부분 게임
        printf(" %d", grundy[piles[i]]);  // 해당 그런디 값
        combined ^= grundy[piles[i]];  // 독립 합의 XOR 누적
    }  // 무더기 결합 끝
    printf("\nXOR %d\n%s\n", combined, combined ? "WIN" : "LOSE");  // 정상 규칙의 승패 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
