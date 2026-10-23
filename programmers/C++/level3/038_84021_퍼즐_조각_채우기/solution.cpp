#include <algorithm>
#include <climits>
#include <map>
#include <utility>
#include <vector>
using namespace std;

static vector<pair<int, int>> puzzle_shape(vector<pair<int, int>> cells) {
    vector<pair<int, int>> best;
    for (int turn = 0; turn < 4; ++turn) {
        int min_r = INT_MAX, min_c = INT_MAX;
        for (auto [r, c] : cells) { min_r = min(min_r, r); min_c = min(min_c, c); }
        vector<pair<int, int>> form; for (auto [r, c] : cells) form.push_back({r - min_r, c - min_c});
        sort(form.begin(), form.end()); if (best.empty() || form < best) best = form;
        for (auto& cell : cells) cell = {cell.second, -cell.first};
    }
    return best;
}

static vector<vector<pair<int, int>>> puzzle_components(vector<vector<int>> board, int target) {
    int n = (int)board.size(), dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    vector<vector<pair<int, int>>> result;
    for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) if (board[r][c] == target) {
        vector<pair<int, int>> stack{{r,c}}, cells; board[r][c] = 1 - target;
        while (!stack.empty()) {
            auto [x,y] = stack.back(); stack.pop_back(); cells.push_back({x,y});
            for (int d = 0; d < 4; ++d) { int nx = x + dr[d], ny = y + dc[d]; if (nx >= 0 && nx < n && ny >= 0 && ny < n && board[nx][ny] == target) { board[nx][ny] = 1 - target; stack.push_back({nx,ny}); } }
        }
        result.push_back(puzzle_shape(cells));
    }
    return result;
}

int solution(vector<vector<int>> game_board, vector<vector<int>> table) {
    map<vector<pair<int,int>>, int> pieces;
    for (const auto& piece : puzzle_components(table, 1)) ++pieces[piece];
    int answer = 0;
    for (const auto& hole : puzzle_components(game_board, 0)) if (pieces[hole] > 0) { answer += (int)hole.size(); --pieces[hole]; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <map>  // 키를 정렬해 보관하는 map
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// static vector<pair<int, int>> puzzle_shape(vector<pair<int, int>> cells) {  // 조각 좌표를 같은 원점으로 옮겨 모양 비교
// vector<pair<int, int>> best;  // 네 회전 중 사전순으로 가장 작은 표준 모양 저장
// for (int turn = 0; turn < 4; ++turn) {  // 네 방향의 회전을 모두 구하기
// int min_r = INT_MAX, min_c = INT_MAX;  // 현재 회전의 좌표 최솟값 초기화
// for (auto [r, c] : cells) { min_r = min(min_r, r); min_c = min(min_c, c); }  // 모양을 원점으로 옮길 기준 구하기
// vector<pair<int, int>> form; for (auto [r, c] : cells) form.push_back({r - min_r, c - min_c});  // 왼쪽 위 기준의 상대 좌표로 바꾸기
// sort(form.begin(), form.end()); if (best.empty() || form < best) best = form;  // 정렬한 좌표 목록 중 최소 표현 고르기
// for (auto& cell : cells) cell = {cell.second, -cell.first};  // 각 좌표를 90도 회전
// }  // 블록 끝
// return best;  // 회전에 관계없는 표준 모양 반환
// }  // 블록 끝
// static vector<vector<pair<int, int>>> puzzle_components(vector<vector<int>> board, int target) {  // 같은 target 값으로 연결된 조각 좌표 모으기
// int n = (int)board.size(), dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 보드 크기와 인접 방향 선언
// vector<vector<pair<int, int>>> result;  // 연결 요소별 표준 모양 저장
// for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) if (board[r][c] == target) {  // 아직 찾지 않은 대상 칸에서 조각을 시작
// vector<pair<int, int>> stack{{r,c}}, cells; board[r][c] = 1 - target;  // 깊이 우선 탐색을 시작하고 방문 표시
// while (!stack.empty()) {  // 연결된 대상 칸을 모두 찾기
// auto [x,y] = stack.back(); stack.pop_back(); cells.push_back({x,y});  // 현재 칸을 조각에 추가
// for (int d = 0; d < 4; ++d) { int nx = x + dr[d], ny = y + dc[d]; if (nx >= 0 && nx < n && ny >= 0 && ny < n && board[nx][ny] == target) { board[nx][ny] = 1 - target; stack.push_back({nx,ny}); } }  // 같은 대상 값의 미방문 이웃 넣기
// }  // 블록 끝
// result.push_back(puzzle_shape(cells));  // 연결 요소를 회전 표준형으로 저장
// }  // 블록 끝
// return result;  // 모든 연결 조각의 표준형 반환
// }  // 블록 끝
// int solution(vector<vector<int>> game_board, vector<vector<int>> table) {  // 빈칸과 조각의 좌표를 정규화해 회전별 비교
// map<vector<pair<int,int>>, int> pieces;  // 표준 모양별 사용 가능한 퍼즐 조각 수 세기
// for (const auto& piece : puzzle_components(table, 1)) ++pieces[piece];  // 테이블의 조각들 등록
// int answer = 0;  // 채운 칸 수 초기화
// for (const auto& hole : puzzle_components(game_board, 0)) if (pieces[hole] > 0) { answer += (int)hole.size(); --pieces[hole]; }  // 같은 표준형의 조각 하나를 빈칸에 넣기
// return answer;  // 최대한 채운 칸 수 반환
// }  // 블록 끝

// 풀이 요약
// 빈칸과 퍼즐 조각의 연결 요소를 네 회전 중 최소 상대 좌표 목록으로 표준화해 같은 모양을 한 번씩 맞추기
