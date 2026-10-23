#include <algorithm>
#include <numeric>
#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> costs) {
    sort(costs.begin(), costs.end(), [](const auto& a, const auto& b) { return a[2] < b[2]; });
    vector<int> parent(n), sizes(n,1); iota(parent.begin(), parent.end(), 0);
    auto find = [&](int node) { while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; } return node; };
    int answer = 0, used = 0;
    for (const auto& edge : costs) {
        int first = find(edge[0]), second = find(edge[1]); if (first == second) continue;
        if (sizes[first] < sizes[second]) swap(first, second); parent[second] = first; sizes[first] += sizes[second];
        answer += edge[2]; if (++used == n - 1) break;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> costs) {  // 서로 다른 연결 요소를 싼 간선부터 합치기
// sort(costs.begin(), costs.end(), [](const auto& a, const auto& b) { return a[2] < b[2]; });  // 다리 비용이 작은 순서로 정렬
// vector<int> parent(n), sizes(n,1); iota(parent.begin(), parent.end(), 0);  // 섬별 서로소 집합 초기화
// auto find = [&](int node) { while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; } return node; };  // 경로 압축으로 연결 요소의 대표 구하기
// int answer = 0, used = 0;  // 선택한 다리의 총비용과 수 저장
// for (const auto& edge : costs) {  // 저렴한 다리부터 연결 여부 확인
// int first = find(edge[0]), second = find(edge[1]); if (first == second) continue;  // 이미 연결된 섬 사이의 간선은 제외
// if (sizes[first] < sizes[second]) swap(first, second); parent[second] = first; sizes[first] += sizes[second];  // 두 연결 요소를 크기 기준으로 합치기
// answer += edge[2]; if (++used == n - 1) break;  // 비용을 더하고 모든 섬이 연결되면 끝
// }  // 블록 끝
// return answer;  // 최소 신장 트리의 총 다리 비용 반환
// }  // 블록 끝

// 풀이 요약
// 다리 비용 순서로 서로 다른 연결 요소만 합치는 크루스칼 알고리즘으로 최소 신장 트리 구하기
