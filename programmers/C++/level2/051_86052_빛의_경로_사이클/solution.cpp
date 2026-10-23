#include <algorithm>
#include <string>
#include <vector>
using namespace std;

vector<int> solution(vector<string> grid) {
    int rows = (int)grid.size(), cols = (int)grid[0].size();
    vector<vector<bool>> visited(rows, vector<bool>(cols * 4, false));
    int dr[4] = {-1, 0, 1, 0}, dc[4] = {0, 1, 0, -1};
    vector<int> answer;
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) for (int direction = 0; direction < 4; ++direction) {
        if (visited[r][c * 4 + direction]) continue;
        int x = r, y = c, d = direction, length = 0;
        while (!visited[x][y * 4 + d]) {
            visited[x][y * 4 + d] = true; ++length;
            if (grid[x][y] == 'L') d = (d + 3) % 4;
            else if (grid[x][y] == 'R') d = (d + 1) % 4;
            x = (x + dr[d] + rows) % rows; y = (y + dc[d] + cols) % cols;
        }
        answer.push_back(length);
    }
    sort(answer.begin(), answer.end());
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<string> grid) {  // 칸과 진행 방향을 상태로 빛의 순환 길이 세기
// int rows = (int)grid.size(), cols = (int)grid[0].size();  // 격자의 크기 구하기
// vector<vector<bool>> visited(rows, vector<bool>(cols * 4, false));  // 위치와 진입 방향의 방문 상태 저장
// int dr[4] = {-1, 0, 1, 0}, dc[4] = {0, 1, 0, -1};  // 위, 오른쪽, 아래, 왼쪽 방향을 순서대로 선언
// vector<int> answer;  // 발견한 사이클의 길이 저장
// for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) for (int direction = 0; direction < 4; ++direction) {  // 모든 위치와 방향 상태 검사
// if (visited[r][c * 4 + direction]) continue;  // 이미 어떤 사이클에 포함한 상태는 건너뛰기
// int x = r, y = c, d = direction, length = 0;  // 새 경로의 시작 상태와 길이 초기화
// while (!visited[x][y * 4 + d]) {  // 같은 상태에 다시 도달할 때까지 빛을 이동시키기
// visited[x][y * 4 + d] = true; ++length;  // 현재 상태를 방문 표시하고 경로 길이 늘리기
// if (grid[x][y] == 'L') d = (d + 3) % 4;  // 왼쪽 회전을 방향 인덱스로 반영
// else if (grid[x][y] == 'R') d = (d + 1) % 4;  // 오른쪽 회전을 방향 인덱스로 반영
// x = (x + dr[d] + rows) % rows; y = (y + dc[d] + cols) % cols;  // 격자 경계를 넘어가면 반대편으로 연결
// }  // 블록 끝
// answer.push_back(length);  // 새 사이클의 길이 기록
// }  // 블록 끝
// sort(answer.begin(), answer.end());  // 사이클 길이를 오름차순으로 정렬
// return answer;  // 모든 사이클 길이 반환
// }  // 블록 끝

// 풀이 요약
// 격자의 위치와 방향을 하나의 상태로 두고 방문하지 않은 상태를 따라가며 빛의 사이클 길이 세기
