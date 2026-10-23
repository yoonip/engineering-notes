#include <algorithm>
#include <set>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<vector<int>> land) {
    int rows = (int)land.size(), cols = (int)land[0].size();
    vector<int> totals(cols, 0);
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {
        if (land[r][c] == 0) continue;
        vector<pair<int, int>> stack{{r, c}};
        land[r][c] = 0;
        set<int> columns;
        int amount = 0;
        while (!stack.empty()) {
            auto [x, y] = stack.back(); stack.pop_back();
            ++amount; columns.insert(y);
            for (int d = 0; d < 4; ++d) {
                int nx = x + dr[d], ny = y + dc[d];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && land[nx][ny] == 1) {
                    land[nx][ny] = 0;
                    stack.push_back({nx, ny});
                }
            }
        }
        for (int column : columns) totals[column] += amount;
    }
    return *max_element(totals.begin(), totals.end());
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <set>  // 정렬된 집합과 중복을 허용하는 multiset
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> land) {  // 각 열에서 얻을 수 있는 유전 크기 합 비교
// int rows = (int)land.size(), cols = (int)land[0].size();  // 격자의 행과 열 크기 구하기
// vector<int> totals(cols, 0);  // 각 열에서 시추할 수 있는 석유량 저장
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 상하좌우 이동량 선언
// for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {  // 모든 칸에서 아직 찾지 않은 유전 탐색
// if (land[r][c] == 0) continue;  // 빈 칸이나 이미 탐색한 칸은 건너뛰기
// vector<pair<int, int>> stack{{r, c}};  // 현재 유전의 깊이 우선 탐색 스택 만들기
// land[r][c] = 0;  // 시작 칸을 방문 처리
// set<int> columns;  // 같은 유전에 닿는 열을 중복 없이 저장
// int amount = 0;  // 현재 연결 유전의 석유량 초기화
// while (!stack.empty()) {  // 연결된 석유 칸을 모두 찾기
// auto [x, y] = stack.back(); stack.pop_back();  // 스택에서 다음 칸 꺼내기
// ++amount; columns.insert(y);  // 석유량을 늘리고 현재 열 등록
// for (int d = 0; d < 4; ++d) {  // 네 방향의 연결 검사
// int nx = x + dr[d], ny = y + dc[d];  // 이웃 좌표 계산
// if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && land[nx][ny] == 1) {  // 격자 안의 방문하지 않은 석유 칸만 고르기
// land[nx][ny] = 0;  // 중복 방문을 막기 위해 표시
// stack.push_back({nx, ny});  // 이웃 칸을 스택에 넣기
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// for (int column : columns) totals[column] += amount;  // 유전에 닿는 각 열에 전체 석유량을 한 번씩 더하기
// }  // 블록 끝
// return *max_element(totals.begin(), totals.end());  // 열별 시추량의 최댓값 반환
// }  // 블록 끝

// 풀이 요약
// 연결된 유전의 전체 크기와 닿는 열을 구한 뒤 각 열에 해당 크기를 한 번씩 더해 최대 시추량 구하기
