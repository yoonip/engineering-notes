#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

int solution(int n, int s, int a, int b, vector<vector<int>> fares) {
    const int INF = 1000000000; vector<vector<int>> distance(n, vector<int>(n, INF));
    for (int i = 0; i < n; ++i) distance[i][i] = 0;
    for (const auto& fare : fares) distance[fare[0] - 1][fare[1] - 1] = distance[fare[1] - 1][fare[0] - 1] = fare[2];
    for (int via = 0; via < n; ++via) for (int start = 0; start < n; ++start) for (int end = 0; end < n; ++end) distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end]);
    long long answer = LLONG_MAX;
    for (int split = 0; split < n; ++split) answer = min(answer, 1LL * distance[s - 1][split] + distance[a - 1][split] + distance[b - 1][split]);
    return (int)answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, int s, int a, int b, vector<vector<int>> fares) {  // 합승 분기점마다 공통·개별 경로 비용 비교
// const int INF = 1000000000; vector<vector<int>> distance(n, vector<int>(n, INF));  // 모든 지점 쌍의 최단 요금 초기화
// for (int i = 0; i < n; ++i) distance[i][i] = 0;  // 같은 지점 사이의 요금은 0
// for (const auto& fare : fares) distance[fare[0] - 1][fare[1] - 1] = distance[fare[1] - 1][fare[0] - 1] = fare[2];  // 택시 요금을 양방향으로 등록
// for (int via = 0; via < n; ++via) for (int start = 0; start < n; ++start) for (int end = 0; end < n; ++end) distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end]);  // 플로이드 워셜로 경유 지점별 최단 요금 갱신
// long long answer = LLONG_MAX;  // 합승 후 분리하는 전체 최소 요금 초기화
// for (int split = 0; split < n; ++split) answer = min(answer, 1LL * distance[s - 1][split] + distance[a - 1][split] + distance[b - 1][split]);  // 모든 분리 지점에서 합승 구간과 두 개별 구간을 더하기
// return (int)answer;  // 두 사람이 귀가하는 최소 총요금 반환
// }  // 블록 끝

// 풀이 요약
// 모든 지점 쌍의 최단 요금을 구하고 가능한 합승 분리 지점마다 공통 구간과 두 개별 귀가 구간의 합 비교
