#include <stdio.h> // 정수 입력과 결과 출력에 쓸 표준 함수
int main(void) { // 실행 시작점
    int n, q, a[50], l[50], r[50]; // 최대 50개 값과 질의의 반열린 경계
    long long prefix[51] = {0}, direct[50]; // 빈 접두 합과 직접 계산 결과
    scanf("%d %d", &n, &q); // 값 개수와 질의 개수 읽기
    for (int i = 0; i < n; ++i) scanf("%d", &a[i]); // 원래 배열 입력
    for (int i = 0; i < q; ++i) scanf("%d %d", &l[i], &r[i]); // 모든 질의의 시작과 끝 저장
    for (int i = 0; i < q; ++i) { // 직접 합산 방식으로 각 질의 처리
        direct[i] = 0; // 이번 질의의 합 초기화
        for (int j = l[i]; j < r[i]; ++j) direct[i] += a[j]; // 대상 구간의 원소를 하나씩 더하기
        printf("%s%lld", i ? " " : "", direct[i]); // 직접 구한 합을 질의 순서대로 출력
    } // 직접 합산 결과 한 줄 완성
    printf("\n"); // 첫 결과 줄 끝내기
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + a[i]; // 배열을 한 번 읽어 접두 합 구축
    for (int i = 0; i < q; ++i) printf("%s%lld", i ? " " : "", prefix[r[i]] - prefix[l[i]]); // 두 접두 합 차이로 같은 질의 출력
    printf("\n"); // 누적합 결과 줄 끝내기
    return 0; // 정상 종료
} // 두 방식의 비교 끝
