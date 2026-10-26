#include <stdio.h> // 보드 크기 입력과 배치 수 출력
int n, columns[9] = {0}, down[17] = {0}, up[17] = {0}; // 열과 두 대각선의 사용 표시
long long search(int row) { // 이번 행에 퀸 하나를 놓는 재귀 탐색
    if (row == n) return 1; // 모든 행을 채우면 유효 배치 한 개
    long long count = 0; // 현재 접두 배치에서 완성되는 경우 수
    for (int col = 0; col < n; ++col) { // 이번 행의 모든 열을 후보로 확인
        int d = row - col + n - 1, u = row + col; // 두 대각선의 음수 없는 식별자
        if (columns[col] || down[d] || up[u]) continue; // 이미 공격받는 후보는 내려가지 않기
        columns[col] = down[d] = up[u] = 1; // 이번 퀸이 차지한 세 방향 표시
        count += search(row + 1); // 다음 행의 모든 완성 배치 수 누적
        columns[col] = down[d] = up[u] = 0; // 다음 후보를 위해 이번 선택만 복구
    } // 현재 행의 후보 탐색 끝
    return count; // 이 접두 배치의 완성 개수 반환
} // 백트래킹 함수 끝
int main(void) { // 실행 시작점
    scanf("%d", &n); // 보드 한 변의 길이 읽기
    printf("%lld\n", search(0)); // 첫 행부터 탐색해 전체 배치 수 출력
    return 0; // 정상 종료
} // N퀸 예제 끝
