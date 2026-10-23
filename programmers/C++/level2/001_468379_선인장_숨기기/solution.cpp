#include <algorithm>
#include <deque>
#include <vector>
using namespace std;

static vector<int> window_minimum(const vector<int>& values, int width) {
    deque<int> indices;
    vector<int> result;
    for (int i = 0; i < (int)values.size(); ++i) {
        while (!indices.empty() && indices.front() <= i - width) indices.pop_front();
        while (!indices.empty() && values[indices.back()] >= values[i]) indices.pop_back();
        indices.push_back(i);
        if (i + 1 >= width) result.push_back(values[indices.front()]);
    }
    return result;
}

vector<int> solution(int m, int n, int h, int w, vector<vector<int>> drops) {
    int never = (int)drops.size() + 1;
    vector<int> rain(m * n, never);
    for (int t = 0; t < (int)drops.size(); ++t) rain[drops[t][0] * n + drops[t][1]] = t + 1;
    int columns = n - w + 1;
    vector<vector<int>> horizontal(m);
    for (int r = 0; r < m; ++r) horizontal[r] = window_minimum(vector<int>(rain.begin() + r * n, rain.begin() + (r + 1) * n), w);
    int best = -1;
    vector<int> answer{0, 0};
    for (int c = 0; c < columns; ++c) {
        vector<int> column;
        for (int r = 0; r < m; ++r) column.push_back(horizontal[r][c]);
        vector<int> areas = window_minimum(column, h);
        for (int r = 0; r < (int)areas.size(); ++r) {
            vector<int> candidate{r, c};
            if (areas[r] > best || (areas[r] == best && candidate < answer)) {
                best = areas[r];
                answer = candidate;
            }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <deque>  // 양 끝에서 넣고 뺄 수 있는 deque
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// static vector<int> window_minimum(const vector<int>& values, int width) {  // 폭 width의 각 창에서 최솟값을 뽑는 보조 함수
// deque<int> indices;  // deque에 현재 창의 최솟값 후보 인덱스 저장
// vector<int> result;  // 각 창의 최솟값을 순서대로 저장
// for (int i = 0; i < (int)values.size(); ++i) {  // for로 오른쪽 끝 인덱스를 한 칸씩 이동
// while (!indices.empty() && indices.front() <= i - width) indices.pop_front();  // 창 밖으로 나간 후보를 앞에서 제거
// while (!indices.empty() && values[indices.back()] >= values[i]) indices.pop_back();  // 새 값보다 크거나 같은 뒤쪽 후보 제거
// indices.push_back(i);  // 현재 인덱스를 후보 deque 뒤에 추가
// if (i + 1 >= width) result.push_back(values[indices.front()]);  // 창이 완성되면 맨 앞 후보의 값 기록
// }  // 블록 끝
// return result;  // 창별 최솟값 반환
// }  // 블록 끝
// vector<int> solution(int m, int n, int h, int w, vector<vector<int>> drops) {  // 가장 늦게 젖는 h×w 구간의 시작 좌표 찾기
// int never = (int)drops.size() + 1;  // 비가 내리지 않은 칸에 마지막 시각보다 큰 값을 배정하기
// vector<int> rain(m * n, never);  // 격자를 일차원으로 펴 각 칸에 비가 오는 시각 저장
// for (int t = 0; t < (int)drops.size(); ++t) rain[drops[t][0] * n + drops[t][1]] = t + 1;  // 행과 열을 인덱스로 바꾸어 비의 순서 기록
// int columns = n - w + 1;  // 폭 w의 직사각형을 놓을 수 있는 시작 열의 개수
// vector<vector<int>> horizontal(m);  // 각 행에서 폭 w인 창의 최솟값 저장
// for (int r = 0; r < m; ++r) horizontal[r] = window_minimum(vector<int>(rain.begin() + r * n, rain.begin() + (r + 1) * n), w);  // 행별 최소 시각을 단조 deque로 계산
// int best = -1;  // 현재까지 가장 늦은 첫 비 시각 초기화
// vector<int> answer{0, 0};  // 선택한 직사각형의 시작 행과 열 저장
// for (int c = 0; c < columns; ++c) {  // 가능한 시작 열을 차례대로 검사
// vector<int> column;  // 해당 열에 대응하는 행별 최솟값 모으기
// for (int r = 0; r < m; ++r) column.push_back(horizontal[r][c]);  // 고정된 시작 열의 최소 시각들을 세로로 읽기
// vector<int> areas = window_minimum(column, h);  // 높이 h인 창의 최솟값으로 직사각형의 첫 비 시각 구하기
// for (int r = 0; r < (int)areas.size(); ++r) {  // 가능한 시작 행 검사
// vector<int> candidate{r, c};  // 현재 직사각형의 시작 좌표 만들기
// if (areas[r] > best || (areas[r] == best && candidate < answer)) {  // 첫 비가 더 늦거나 동률에서 좌표가 작으면 선택
// best = areas[r];  // 가장 늦은 첫 비 시각 갱신
// answer = candidate;  // 선택한 시작 좌표 갱신
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 최종 시작 좌표 반환
// }  // 블록 끝

// 풀이 요약
// 행과 열에 단조 deque를 적용해 모든 h×w 구간의 첫 비 시각을 구하고 가장 늦게 젖는 시작 좌표 선택
