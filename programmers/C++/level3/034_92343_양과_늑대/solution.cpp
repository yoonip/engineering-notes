#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(vector<int> info, vector<vector<int>> edges) {
    int n = (int)info.size(), sheep_mask = 0; vector<int> children(n, 0);
    for (const auto& edge : edges) children[edge[0]] |= 1 << edge[1];
    for (int node = 0; node < n; ++node) if (info[node] == 0) sheep_mask |= 1 << node;
    vector<int> memo(1 << n, -1);
    function<int(int)> dfs = [&](int visited) {
        int& answer = memo[visited]; if (answer != -1) return answer;
        int sheep = __builtin_popcount((unsigned)(visited & sheep_mask)), wolves = __builtin_popcount((unsigned)visited) - sheep;
        if (wolves >= sheep) return answer = 0;
        answer = sheep; int available = 0;
        for (int node = 0; node < n; ++node) if (visited & (1 << node)) available |= children[node];
        available &= ~visited;
        while (available) { int bit = available & -available; available ^= bit; answer = max(answer, dfs(visited | bit)); }
        return answer;
    };
    return dfs(1);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> info, vector<vector<int>> edges) {  // 늑대보다 양이 많은 방문 집합만 확장
// int n = (int)info.size(), sheep_mask = 0; vector<int> children(n, 0);  // 정점 수와 양 및 자식의 비트 마스크 저장
// for (const auto& edge : edges) children[edge[0]] |= 1 << edge[1];  // 부모별 자식 정점 등록
// for (int node = 0; node < n; ++node) if (info[node] == 0) sheep_mask |= 1 << node;  // 양이 있는 정점의 비트를 켜기
// vector<int> memo(1 << n, -1);  // 방문 집합별로 구할 수 있는 최대 양 수를 기억
// function<int(int)> dfs = [&](int visited) {  // 이미 방문한 정점 집합에서 다음 정점 고르기
// int& answer = memo[visited]; if (answer != -1) return answer;  // 계산한 방문 집합은 재사용
// int sheep = __builtin_popcount((unsigned)(visited & sheep_mask)), wolves = __builtin_popcount((unsigned)visited) - sheep;  // 현재 양과 늑대 수를 비트 수로 세기
// if (wolves >= sheep) return answer = 0;  // 늑대가 양 이상이면 더 진행할 수 없음
// answer = sheep; int available = 0;  // 현재 양 수와 다음 방문 후보 초기화
// for (int node = 0; node < n; ++node) if (visited & (1 << node)) available |= children[node];  // 방문한 모든 정점의 자식을 후보에 넣기
// available &= ~visited;  // 이미 방문한 정점은 후보에서 제외
// while (available) { int bit = available & -available; available ^= bit; answer = max(answer, dfs(visited | bit)); }  // 후보 정점을 하나씩 추가하며 최댓값 구하기
// return answer;  // 현재 집합에서의 최대 양 수 반환
// };  // 블록 끝
// return dfs(1);  // 루트 정점을 방문한 상태에서 시작
// }  // 블록 끝

// 풀이 요약
// 방문한 정점의 비트 마스크에서 양과 늑대 수를 검사하고 이미 방문한 정점의 자식 중 다음 방문 선택
