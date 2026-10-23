#include <vector>
using namespace std;

int solution(int m, int n, vector<vector<int>> city_map) {
    const int MOD = 20170805; vector<int> vertical(n,0); vertical[0] = 1; int horizontal = 0;
    for (int row = 0; row < m; ++row) {
        horizontal = 0;
        for (int col = 0; col < n; ++col) {
            int kind = city_map[row][col];
            if (kind == 1) vertical[col] = horizontal = 0;
            else if (kind == 0) { int total = (vertical[col] + horizontal) % MOD; vertical[col] = horizontal = total; }
        }
    }
    return horizontal;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int m, int n, vector<vector<int>> city_map) {  // 직진 칸에서는 방향을 유지하며 경로 수 누적
// const int MOD = 20170805; vector<int> vertical(n,0); vertical[0] = 1; int horizontal = 0;  // 열별 아래 방향 경로와 현재 오른쪽 방향 경로 저장
// for (int row = 0; row < m; ++row) {  // 위 행부터 아래 행으로 이동
// horizontal = 0;  // 새 행의 왼쪽 바깥에서 오는 경로는 없음
// for (int col = 0; col < n; ++col) {  // 행 안에서는 왼쪽에서 오른쪽으로 처리
// int kind = city_map[row][col];  // 현재 도로의 이동 규칙 읽기
// if (kind == 1) vertical[col] = horizontal = 0;  // 통행 금지 칸으로 들어오는 경로를 모두 없애기
// else if (kind == 0) { int total = (vertical[col] + horizontal) % MOD; vertical[col] = horizontal = total; }  // 회전 가능 칸에서는 두 진입 방향의 경로 합치기
// }  // 블록 끝
// }  // 블록 끝
// return horizontal;  // 목적지에 도달하는 경로 수 반환
// }  // 블록 끝

// 풀이 요약
// 위쪽과 왼쪽에서 들어오는 방향별 경로 수를 따로 유지하고 회전 가능한 칸에서만 두 방향 합치기
