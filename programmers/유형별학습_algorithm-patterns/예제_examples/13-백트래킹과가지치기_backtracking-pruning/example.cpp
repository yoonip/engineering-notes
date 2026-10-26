#include <iostream> // 보드 크기 입력과 배치 수 출력
#include <vector> // 열과 대각선의 사용 표시
using namespace std; // 표준 이름의 접두사 생략
int n; // 보드 한 변의 길이
vector<int> columns, down, up; // 이미 놓인 퀸이 공격하는 세 방향
long long search(int row) { // 이번 행의 퀸 위치를 고르는 재귀 함수
    if (row == n) return 1; // 모든 행을 채웠으면 완성 배치 한 개
    long long count = 0; // 현재 배치에서 이어지는 완성 개수
    for (int col = 0; col < n; ++col) { // 이번 행의 모든 열 검사
        int d = row - col + n - 1, u = row + col; // 두 대각선의 배열 인덱스
        if (columns[col] || down[d] || up[u]) continue; // 공격받는 칸은 가지치기
        columns[col] = down[d] = up[u] = 1; // 선택한 열과 대각선 표시
        count += search(row + 1); // 다음 행에서 이어지는 배치 수 더하기
        columns[col] = down[d] = up[u] = 0; // 이번 퀸을 제거하고 이전 상태 복구
    } // 이번 행의 후보 탐색 끝
    return count; // 가능한 완성 개수 반환
} // 재귀 함수 끝
int main() { // 실행 시작점
    cin >> n; // 보드 크기 입력
    columns.assign(n, 0); // 모든 열을 비어 있는 상태로 초기화
    down.assign(2 * n - 1, 0); // 한 방향 대각선 표시 공간
    up.assign(2 * n - 1, 0); // 다른 방향 대각선 표시 공간
    cout << search(0) << '\n'; // 첫 행부터 놓은 전체 배치 수 출력
    return 0; // 정상 종료
} // N퀸 예제 끝
