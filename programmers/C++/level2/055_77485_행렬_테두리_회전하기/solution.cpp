#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(int rows, int columns, vector<vector<int>> queries) {
    vector<vector<int>> board(rows, vector<int>(columns));
    for (int r = 0; r < rows; ++r) for (int c = 0; c < columns; ++c) board[r][c] = r * columns + c + 1;
    vector<int> answer;
    for (const auto& query : queries) {
        int top = query[0] - 1, left = query[1] - 1, bottom = query[2] - 1, right = query[3] - 1;
        vector<pair<int, int>> path;
        for (int c = left; c < right; ++c) path.push_back({top, c});
        for (int r = top; r < bottom; ++r) path.push_back({r, right});
        for (int c = right; c > left; --c) path.push_back({bottom, c});
        for (int r = bottom; r > top; --r) path.push_back({r, left});
        vector<int> values;
        for (auto [r, c] : path) values.push_back(board[r][c]);
        for (int i = 0; i < (int)path.size(); ++i) board[path[i].first][path[i].second] = values[(i + values.size() - 1) % values.size()];
        answer.push_back(*min_element(values.begin(), values.end()));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int rows, int columns, vector<vector<int>> queries) {  // 테두리를 한 칸씩 돌리며 이동한 최솟값 기록
// vector<vector<int>> board(rows, vector<int>(columns));  // 회전할 행렬 만들기
// for (int r = 0; r < rows; ++r) for (int c = 0; c < columns; ++c) board[r][c] = r * columns + c + 1;  // 행 우선 순서의 초기 정수 채우기
// vector<int> answer;  // 회전마다 이동한 값의 최솟값 저장
// for (const auto& query : queries) {  // 요청을 순서대로 적용
// int top = query[0] - 1, left = query[1] - 1, bottom = query[2] - 1, right = query[3] - 1;  // 좌표를 0부터 시작하는 인덱스로 바꾸기
// vector<pair<int, int>> path;  // 테두리를 시계 방향으로 나열
// for (int c = left; c < right; ++c) path.push_back({top, c});  // 위쪽 변을 오른쪽으로 읽기
// for (int r = top; r < bottom; ++r) path.push_back({r, right});  // 오른쪽 변을 아래로 읽기
// for (int c = right; c > left; --c) path.push_back({bottom, c});  // 아래쪽 변을 왼쪽으로 읽기
// for (int r = bottom; r > top; --r) path.push_back({r, left});  // 왼쪽 변을 위로 읽기
// vector<int> values;  // 회전 전에 테두리 값들을 복사
// for (auto [r, c] : path) values.push_back(board[r][c]);  // 테두리의 순서에 맞춰 값 읽기
// for (int i = 0; i < (int)path.size(); ++i) board[path[i].first][path[i].second] = values[(i + values.size() - 1) % values.size()];  // 직전 위치의 값을 현재 위치로 한 칸 회전시키기
// answer.push_back(*min_element(values.begin(), values.end()));  // 이동한 값들의 최솟값 기록
// }  // 블록 끝
// return answer;  // 쿼리별 최솟값 반환
// }  // 블록 끝

// 풀이 요약
// 테두리 좌표를 시계 방향으로 나열해 이전 위치의 값으로 한 칸 회전시키고 이동한 값의 최솟값 기록
