#include <algorithm>
#include <vector>
using namespace std;

int solution(int N, vector<vector<int>> road, int K) {
    const int INF = 100000000;
    vector<vector<int>> distance(N, vector<int>(N, INF));
    for (int i = 0; i < N; ++i) distance[i][i] = 0;
    for (const auto& edge : road) {
        int a = edge[0] - 1, b = edge[1] - 1;
        distance[a][b] = distance[b][a] = min(distance[a][b], edge[2]);
    }
    for (int via = 0; via < N; ++via) for (int start = 0; start < N; ++start) for (int end = 0; end < N; ++end) distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end]);
    int answer = 0;
    for (int time : distance[0]) answer += time <= K;
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int N, vector<vector<int>> road, int K) {  // 최단 거리 계산 후 K 이내 마을 세기
// const int INF = 100000000;  // 실제 최단 거리보다 큰 도달 불가 값 정하기
// vector<vector<int>> distance(N, vector<int>(N, INF));  // 모든 마을 쌍의 거리 초기화
// for (int i = 0; i < N; ++i) distance[i][i] = 0;  // 같은 마을 사이 거리는 0
// for (const auto& edge : road) {  // 양방향 도로 등록
// int a = edge[0] - 1, b = edge[1] - 1;  // 마을 번호를 0부터 시작하는 인덱스로 바꾸기
// distance[a][b] = distance[b][a] = min(distance[a][b], edge[2]);  // 같은 두 마을의 여러 도로 중 최단 시간 저장
// }  // 블록 끝
// for (int via = 0; via < N; ++via) for (int start = 0; start < N; ++start) for (int end = 0; end < N; ++end) distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end]);  // 경유 마을을 늘리며 모든 쌍의 최단 거리 갱신
// int answer = 0;  // 배달 가능한 마을 수 초기화
// for (int time : distance[0]) answer += time <= K;  // 1번 마을에서 K시간 이내인 마을 세기
// return answer;  // 배달 가능한 마을 수 반환
// }  // 블록 끝

// 풀이 요약
// 여러 도로 중 최소 비용을 등록하고 플로이드 워셜 알고리즘으로 최단 거리를 구한 뒤 1번 마을에서 K 이하인 마을 세기
