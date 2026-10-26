#include <stdio.h> // 정수 입력과 합 출력
int main(void) { // 실행 시작점
    int n, q, left, right; // 배열 크기와 갱신 수 및 최종 질의 경계
    long long a[10], diff[11] = {0}, prefix[11] = {0}, running = 0; // 값·차분·접두 합과 누적 증가량
    scanf("%d %d", &n, &q); // 원소 수와 구간 갱신 수 읽기
    for (int i = 0; i < n; ++i) scanf("%lld", &a[i]); // 원래 값 입력
    for (int i = 0; i < q; ++i) { // 모든 반열린 구간 갱신 처리
        int l, r; long long delta; // 갱신 시작·끝과 더할 값
        scanf("%d %d %lld", &l, &r, &delta); // 이번 갱신 읽기
        diff[l] += delta; // 구간 시작에서 증가량 켜기
        diff[r] -= delta; // 구간 끝에서 같은 증가량 끄기
    } // 차분 기록 끝
    scanf("%d %d", &left, &right); // 최종 합 질의 경계 읽기
    for (int i = 0; i < n; ++i) { // 차분을 복원하며 최종 값과 접두 합 생성
        running += diff[i]; // 현재 위치에 겹치는 증가량 누적
        a[i] += running; // 원래 값에 전체 증가량 반영
        prefix[i + 1] = prefix[i] + a[i]; // 최종 배열의 접두 합 누적
        printf("%s%lld", i ? " " : "", a[i]); // 복원한 값을 왼쪽부터 출력
    } // 최종 배열 복원 끝
    printf("\n%lld\n", prefix[right] - prefix[left]); // 배열 줄 다음에 최종 구간 합 출력
    return 0; // 정상 종료
} // 차분과 누적합 예제 끝
