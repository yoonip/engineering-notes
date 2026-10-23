#include <algorithm>
#include <numeric>
#include <vector>
using namespace std;

int solution(vector<vector<int>> beginning, vector<vector<int>> target) {
    int n = (int)beginning.size(), m = (int)beginning[0].size();
    vector<vector<int>> difference(n, vector<int>(m));
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) difference[r][c] = beginning[r][c] ^ target[r][c];
    vector<int> columns = difference[0], rows(n);
    for (int r = 0; r < n; ++r) rows[r] = difference[r][0] ^ columns[0];
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) if ((rows[r] ^ columns[c]) != difference[r][c]) return -1;
    int flips = accumulate(rows.begin(), rows.end(), 0) + accumulate(columns.begin(), columns.end(), 0);
    return min(flips, n + m - flips);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> beginning, vector<vector<int>> target) {  // 행·열 뒤집기의 일관성과 최소 횟수 확인
// int n = (int)beginning.size(), m = (int)beginning[0].size();  // 동전판의 크기 구하기
// vector<vector<int>> difference(n, vector<int>(m));  // 각 칸의 뒤집기 필요 여부 저장
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) difference[r][c] = beginning[r][c] ^ target[r][c];  // 시작과 목표가 다르면 XOR 결과가 1
// vector<int> columns = difference[0], rows(n);  // 첫 행을 기준으로 열 뒤집기 선택을 고정하기
// for (int r = 0; r < n; ++r) rows[r] = difference[r][0] ^ columns[0];  // 첫 열을 맞추는 각 행의 뒤집기 여부 구하기
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) if ((rows[r] ^ columns[c]) != difference[r][c]) return -1;  // 행과 열의 선택으로 모든 차이를 만들 수 있는지 검사
// int flips = accumulate(rows.begin(), rows.end(), 0) + accumulate(columns.begin(), columns.end(), 0);  // 현재 선택의 전체 뒤집기 수 구하기
// return min(flips, n + m - flips);  // 모든 행열 선택을 반전한 동등 해와 비교
// }  // 블록 끝

// 풀이 요약
// 첫 행을 기준으로 행과 열의 뒤집기 여부를 정하고 모든 칸의 차이를 만들 수 있는지 확인한 뒤 동등한 두 선택 비교
