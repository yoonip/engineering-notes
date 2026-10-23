#include <algorithm>
#include <string>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(vector<string> maps) {
    int rows = (int)maps.size(), cols = (int)maps[0].size();
    vector<int> answer;
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {
        if (maps[r][c] == 'X') continue;
        int food = maps[r][c] - '0';
        maps[r][c] = 'X';
        vector<pair<int, int>> stack{{r, c}};
        while (!stack.empty()) {
            auto [x, y] = stack.back(); stack.pop_back();
            for (int d = 0; d < 4; ++d) {
                int nx = x + dr[d], ny = y + dc[d];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && maps[nx][ny] != 'X') {
                    food += maps[nx][ny] - '0';
                    maps[nx][ny] = 'X';
                    stack.push_back({nx, ny});
                }
            }
        }
        answer.push_back(food);
    }
    sort(answer.begin(), answer.end());
    if (answer.empty()) answer.push_back(-1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<string> maps) {  // 섬별 식량 합을 구해 오름차순으로 정렬
// int rows = (int)maps.size(), cols = (int)maps[0].size();  // 지도의 크기 구하기
// vector<int> answer;  // 섬별 식량 합계 저장
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 네 방향의 이동량 선언
// for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {  // 아직 탐색하지 않은 섬의 시작 칸 찾기
// if (maps[r][c] == 'X') continue;  // 바다이거나 방문한 칸이면 건너뛰기
// int food = maps[r][c] - '0';  // 시작 칸의 식량을 숫자로 바꾸기
// maps[r][c] = 'X';  // 시작 칸을 방문 처리
// vector<pair<int, int>> stack{{r, c}};  // 섬을 찾을 깊이 우선 탐색 스택 만들기
// while (!stack.empty()) {  // 연결된 모든 육지 탐색
// auto [x, y] = stack.back(); stack.pop_back();  // 다음 칸을 스택 끝에서 꺼내기
// for (int d = 0; d < 4; ++d) {  // 네 방향의 이웃 검사
// int nx = x + dr[d], ny = y + dc[d];  // 이웃 좌표 계산
// if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && maps[nx][ny] != 'X') {  // 지도 안의 방문하지 않은 육지만 고르기
// food += maps[nx][ny] - '0';  // 이웃 칸의 식량을 합계에 더하기
// maps[nx][ny] = 'X';  // 중복 집계를 막기 위해 방문 처리
// stack.push_back({nx, ny});  // 이웃 칸을 스택에 넣기
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// answer.push_back(food);  // 현재 섬의 총식량 기록
// }  // 블록 끝
// sort(answer.begin(), answer.end());  // 섬별 식량을 오름차순으로 정렬
// if (answer.empty()) answer.push_back(-1);  // 섬이 없으면 -1 기록
// return answer;  // 섬별 식량 목록 반환
// }  // 블록 끝

// 풀이 요약
// 상하좌우로 연결된 육지를 깊이 우선 탐색해 섬별 식량을 더하고 오름차순으로 정렬
