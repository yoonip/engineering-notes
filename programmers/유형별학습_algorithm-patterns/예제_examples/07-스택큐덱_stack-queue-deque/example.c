#include <stdio.h> // 배열 입력과 결과 출력
int main(void) { // 실행 시작점
    int n, a[20], answer[20], stack[20], top = 0; scanf("%d", &n); // 값·결과·미해결 인덱스 스택
    for (int i = 0; i < n; ++i) { scanf("%d", &a[i]); answer[i] = -1; } // 값 입력과 답 없음 표시
    for (int i = 0; i < n; ++i) { // 다음 큰 값을 왼쪽부터 탐색
        while (top && a[stack[top - 1]] < a[i]) { // 현재 값이 맨 위 미해결 값보다 큰 동안 반복
            answer[stack[--top]] = i; // 그 인덱스의 첫 오른쪽 큰 값 위치 확정
        } // 현재 값으로 해결할 수 있는 후보 제거 끝
        stack[top++] = i; // 현재 인덱스는 아직 답이 없으므로 스택에 추가
    } // 전체 배열 처리 끝
    for (int i = 0; i < n; ++i) printf("%s%d", i ? " " : "", answer[i]); // 다음 큰 값의 인덱스 출력
    printf("\n"); // 출력 줄 끝내기
    return 0; // 정상 종료
} // 단조 스택 예제 끝
