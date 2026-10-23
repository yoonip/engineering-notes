#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<vector<int>> board) {
    vector<int> dp(board[0].size() + 1, 0);
    int best = 0;
    for (const auto& row : board) {
        int diagonal = 0;
        for (int c = 1; c <= (int)row.size(); ++c) {
            int above = dp[c];
            dp[c] = row[c - 1] ? min({above, dp[c - 1], diagonal}) + 1 : 0;
            best = max(best, dp[c]); diagonal = above;
        }
    }
    return best * best;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> board) {  // 주변 세 칸의 변 길이로 가장 큰 정사각형 갱신
// vector<int> dp(board[0].size() + 1, 0);  // 열별로 현재 칸에서 끝나는 최대 정사각형 변 저장
// int best = 0;  // 가장 긴 정사각형의 한 변 초기화
// for (const auto& row : board) {  // 행을 위에서 아래로 처리
// int diagonal = 0;  // 왼쪽 위 칸의 이전 행 값 보관
// for (int c = 1; c <= (int)row.size(); ++c) {  // 경계용 0 다음 열부터 처리
// int above = dp[c];  // 덮어쓰기 전에 위쪽 칸의 값 저장
// dp[c] = row[c - 1] ? min({above, dp[c - 1], diagonal}) + 1 : 0;  // 값이 1이면 세 이웃 중 최소 변 길이에서 한 칸 확장
// best = max(best, dp[c]); diagonal = above;  // 전체 최댓값과 다음 열의 대각선 값 갱신
// }  // 블록 끝
// }  // 블록 끝
// return best * best;  // 가장 큰 정사각형의 넓이 반환
// }  // 블록 끝

// 풀이 요약
// 현재 칸이 1이면 위, 왼쪽, 왼쪽 위의 정사각형 변 길이 중 최솟값에 1을 더하기
