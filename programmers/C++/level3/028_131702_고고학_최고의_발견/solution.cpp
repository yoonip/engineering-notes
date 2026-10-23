#include <algorithm>
#include <numeric>
#include <vector>
using namespace std;

int solution(vector<vector<int>> clockHands) {
    int n = (int)clockHands.size(), answer = 3 * n * n + 1;
    for (int mask = 0; mask < (1 << (2 * n)); ++mask) {
        vector<int> previous(n, 0), current(n); int cost = 0;
        for (int c = 0; c < n; ++c) { current[c] = (mask >> (2 * c)) & 3; cost += current[c]; }
        for (int r = 0; r < n; ++r) {
            if (cost >= answer) break;
            vector<int> needed(n);
            for (int c = 0; c < n; ++c) { int value = clockHands[r][c] + previous[c] + current[c] + (c ? current[c - 1] : 0) + (c + 1 < n ? current[c + 1] : 0); needed[c] = (4 - value % 4) % 4; }
            if (r == n - 1) { if (accumulate(needed.begin(), needed.end(), 0) == 0) answer = cost; break; }
            cost += accumulate(needed.begin(), needed.end(), 0); previous = current; current = move(needed);
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> clockHands) {  // 첫 행 회전 조합으로 나머지 행의 회전 결정
// int n = (int)clockHands.size(), answer = 3 * n * n + 1;  // 격자 크기와 최소 회전 수 초기화
// for (int mask = 0; mask < (1 << (2 * n)); ++mask) {  // 첫 행의 각 시계를 0부터 3번 돌리는 모든 조합 검사
// vector<int> previous(n, 0), current(n); int cost = 0;  // 직전 행, 현재 행의 회전 수와 비용 초기화
// for (int c = 0; c < n; ++c) { current[c] = (mask >> (2 * c)) & 3; cost += current[c]; }  // 두 비트씩 읽어 첫 행의 회전 수 구하기
// for (int r = 0; r < n; ++r) {  // 위 행을 맞추도록 다음 행의 회전을 강제
// if (cost >= answer) break;  // 이미 최선 이상인 조합은 중단
// vector<int> needed(n);  // 아래 행에서 필요한 회전 수 저장
// for (int c = 0; c < n; ++c) { int value = clockHands[r][c] + previous[c] + current[c] + (c ? current[c - 1] : 0) + (c + 1 < n ? current[c + 1] : 0); needed[c] = (4 - value % 4) % 4; }  // 위, 자기, 좌우의 영향을 뺀 나머지를 아래 행 회전으로 맞추기
// if (r == n - 1) { if (accumulate(needed.begin(), needed.end(), 0) == 0) answer = cost; break; }  // 마지막 행은 추가 회전 없이 모두 0이어야 함
// cost += accumulate(needed.begin(), needed.end(), 0); previous = current; current = move(needed);  // 필요한 다음 행 회전을 더하고 한 행 내려가기
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 모든 시계를 12시로 만드는 최소 회전 수 반환
// }  // 블록 끝

// 풀이 요약
// 첫 행의 모든 회전 조합을 고르면 아래 행의 회전이 순서대로 결정되는 성질을 이용해 최소 회전 수 구하기
