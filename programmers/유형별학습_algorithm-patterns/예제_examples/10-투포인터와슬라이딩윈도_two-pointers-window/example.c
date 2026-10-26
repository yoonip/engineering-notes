#include <stdio.h> // 양수 배열 입력과 최소 길이 출력
int main(void) { // 실행 시작점
    int n, target, a[20], left = 0, best; // 배열 크기·목표·왼쪽 경계·최소 길이
    long long sum = 0; // 현재 창의 합
    scanf("%d %d", &n, &target); // 원소 수와 목표 합 읽기
    best = n + 1; // 아직 답을 못 찾은 표식
    for (int i = 0; i < n; ++i) scanf("%d", &a[i]); // 양수 원소 입력
    for (int right = 0; right < n; ++right) { // 오른쪽 끝을 한 칸씩 확장
        sum += a[right]; // 새 원소를 현재 창에 포함
        while (sum >= target) { // 목표를 만족하는 동안 왼쪽을 줄이기
            int length = right - left + 1; // 현재 닫힌 구간의 원소 수
            if (length < best) best = length; // 더 짧은 유효 창이면 답 갱신
            sum -= a[left++]; // 왼쪽 원소를 빼고 경계 전진
        } // 이번 오른쪽 끝에서 가능한 축소 끝
    } // 모든 오른쪽 끝 확인 끝
    printf("%d\n", best == n + 1 ? 0 : best); // 유효 창이 없으면0 출력
    return 0; // 정상 종료
} // 양수 슬라이딩 윈도 예제 끝
