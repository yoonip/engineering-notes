#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <tuple>
#include <utility>
#include <climits>
#include <cstdlib>
using namespace std;

bool solution(int n, vector<vector<int>> path, vector<vector<int>> order) {
    vector<vector<int>> graph(n); for (const auto& edge : path) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }
    vector<int> before(n, -1), waiting(n, -1); for (const auto& pair : order) before[pair[1]] = pair[0];
    if (before[0] != -1) return false;
    vector<bool> visited(n, false); queue<int> pending; pending.push(0); int count = 0;
    while (!pending.empty()) {
        int node = pending.front(); pending.pop(); if (visited[node]) continue;
        if (before[node] != -1 && !visited[before[node]]) { waiting[before[node]] = node; continue; }
        visited[node] = true; ++count;
        if (waiting[node] != -1) pending.push(waiting[node]);
        for (int neighbor : graph[node]) if (!visited[neighbor]) pending.push(neighbor);
    }
    return count == n;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <array>  // 고정 크기 배열 array 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <map>  // 키 순서가 유지되는 맵 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <deque>  // 양 끝 삽입·삭제를 지원하는 덱 사용 준비
// #include <tuple>  // 여러 상태 값을 묶는 tuple 사용 준비
// #include <utility>  // pair·move 등 유틸리티 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// bool solution(int n, vector<vector<int>> path, vector<vector<int>> order) {  // 동굴 탐험 풀이 함수 정의
//     vector<vector<int>> graph(n); for (const auto& edge : path) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }  // 동굴 통로를 무방향 인접 리스트로 구성
//     vector<int> before(n, -1), waiting(n, -1); for (const auto& pair : order) before[pair[1]] = pair[0];  // 각 방의 선행 방 before와 선행 방을 기다리는 방 waiting 준비
//     if (before[0] != -1) return false;  // 시작 방 0에 선행 조건이 있으면 탐험을 시작할 수 없어 false
//     vector<bool> visited(n, false); queue<int> pending; pending.push(0); int count = 0;  // 방문 표시와 BFS 큐를 준비하고 시작 방 추가. 방문한 방 수는 0
//     while (!pending.empty()) {  // 탐색 대기 방이 남아 있는 동안 처리
//         int node = pending.front(); pending.pop(); if (visited[node]) continue;  // 큐에서 방을 꺼내 이미 방문했다면 중복 처리 생략
//         if (before[node] != -1 && !visited[before[node]]) { waiting[before[node]] = node; continue; }  // 선행 방이 미방문이면 그 선행 방에 자신을 대기시키고 다음 방 처리
//         visited[node] = true; ++count;  // 조건을 충족한 방을 방문 표시하고 방문 수 증가
//         if (waiting[node] != -1) pending.push(waiting[node]);  // 현재 방을 기다리던 방이 있으면 탐색 큐에 추가
//         for (int neighbor : graph[node]) if (!visited[neighbor]) pending.push(neighbor);  // 통로로 연결된 미방문 이웃을 탐색 큐에 추가
//     }  // 블록 끝
//     return count == n;  // 방문 수가 전체 방 수와 같으면 탐험 가능
// }  // 함수 끝
//

// 풀이 요약
// 방마다 선행 방문 조건을 기록. 아직 조건이 안 된 방은 선행 방의 대기 목록에 두고, 선행 방을 방문하면 다시 큐에 넣음.
