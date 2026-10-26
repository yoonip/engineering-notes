#include <stdio.h> // 정수 배열 입력과 정렬 결과 출력
int values[20], buffer[20]; // 원래 배열과 병합용 공유 버퍼
void sort_range(int left, int right) { // 반열린 구간을 정렬하는 재귀 함수
    if (right - left <= 1) return; // 원소가0개나1개면 이미 정렬된 상태
    int middle = left + (right - left) / 2; // 두 부분 문제의 경계
    sort_range(left, middle); // 왼쪽 절반 정렬
    sort_range(middle, right); // 오른쪽 절반 정렬
    int i = left, j = middle, out = left; // 양쪽 읽기 위치와 버퍼 쓰기 위치
    while (i < middle && j < right) { // 두 절반 모두 남아 있을 때 비교
        if (values[i] <= values[j]) buffer[out++] = values[i++]; // 같으면 왼쪽을 먼저 골라 안정 순서 유지
        else buffer[out++] = values[j++]; // 오른쪽 값이 작으면 먼저 배치
    } // 두 절반의 값 비교 끝
    while (i < middle) buffer[out++] = values[i++]; // 남은 왼쪽 원소를 순서대로 복사
    while (j < right) buffer[out++] = values[j++]; // 남은 오른쪽 원소를 순서대로 복사
    for (int pos = left; pos < right; ++pos) values[pos] = buffer[pos]; // 완성된 병합 결과를 원래 구간에 반영
} // 구간 병합 정렬 끝
int main(void) { // 실행 시작점
    int n; scanf("%d", &n); // 원소 수 읽기
    for (int i = 0; i < n; ++i) scanf("%d", &values[i]); // 정렬할 값 입력
    sort_range(0, n); // 전체 반열린 구간 정렬
    for (int i = 0; i < n; ++i) printf("%s%d", i ? " " : "", values[i]); // 정렬 결과를 한 줄에 출력
    printf("\n"); // 빈 배열도 빈 줄 하나 출력
    return 0; // 정상 종료
} // 병합 정렬 예제 끝
