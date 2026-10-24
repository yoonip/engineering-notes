#include <algorithm>
#include <array>
#include <vector>

using namespace std;
using Choices = array<array<int, 2>, 3>;

static void add_child(Choices& choices, int limit, int branch_value, int line_value) {
    for (int branches = limit; branches >= 0; --branches) {
        for (int lines = 1; lines >= 0; --lines) {
            int value = choices[branches][lines];
            if (value < 0) continue;
            if (branches < limit) choices[branches + 1][lines] = max(choices[branches + 1][lines], value + branch_value);
            if (lines == 0) choices[branches][1] = max(choices[branches][1], value + line_value);
        }
    }
}

int solution(vector<vector<int>> t) {
    int n = static_cast<int>(t.size()) + 1;
    vector<vector<int>> adjacent(n);
    for (const auto& edge : t) {
        adjacent[edge[0]].push_back(edge[1]);
        adjacent[edge[1]].push_back(edge[0]);
    }
    vector<int> parent(n, -1), order{0};
    parent[0] = 0;
    for (size_t index = 0; index < order.size(); ++index) {
        int node = order[index];
        for (int child : adjacent[node]) {
            if (child == parent[node]) continue;
            parent[child] = node;
            order.push_back(child);
        }
    }
    vector<int> line(n, 1), stem(n, 1), branch(n, 1);
    int answer = 1;
    for (auto it = order.rbegin(); it != order.rend(); ++it) {
        int node = *it;
        Choices on_spine, off_spine;
        for (auto& row : on_spine) row.fill(-1);
        for (auto& row : off_spine) row.fill(-1);
        on_spine[0][0] = off_spine[0][0] = 0;
        int best_branch = 0;
        for (int child : adjacent[node]) {
            if (child == parent[node]) continue;
            line[node] = max(line[node], 1 + line[child]);
            best_branch = max(best_branch, branch[child]);
            add_child(on_spine, 2, stem[child], line[child]);
            add_child(off_spine, 1, branch[child], line[child]);
        }
        branch[node] = 1 + best_branch;
        for (int branches = 0; branches <= 2; ++branches) {
            for (int lines = 0; lines <= 1; ++lines) {
                int value = on_spine[branches][lines];
                if (value >= 0) {
                    answer = max(answer, 1 + value);
                    if (branches <= 1) stem[node] = max(stem[node], 1 + value);
                    if (lines == 0) branch[node] = max(branch[node], 1 + value);
                }
                if (branches <= 1 && off_spine[branches][lines] >= 0) answer = max(answer, 1 + off_spine[branches][lines]);
            }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 자식 상태와 전체 답의 최댓값 선택
// #include <array>  // 크기가 3×2로 고정된 자식 조합표
// #include <vector>  // 인접 목록·방문 순서·세 가지 DP 배열
//
// using namespace std;  // 표준 라이브러리 이름 앞의 std:: 생략
// using Choices = array<array<int, 2>, 3>;  // 별도 상태의 가지 수와 옆 단순 경로 유무로 구분한 작은 배낭
//
// static void add_child(Choices& choices, int limit, int branch_value, int line_value) {  // 자식 하나를 별도 상태의 가지 또는 단순 경로 중 한 역할로만 배치
//     for (int branches = limit; branches >= 0; --branches) {  // 큰 개수부터 갱신해 같은 자식의 중복 선택 방지
//         for (int lines = 1; lines >= 0; --lines) {  // 단순 경로 역할도 역순 갱신
//             int value = choices[branches][lines];  // 이번 자식을 쓰기 전의 기존 조합 값
//             if (value < 0) continue;  // -1인 불가능 상태는 건너뛰기
//             if (branches < limit) choices[branches + 1][lines] = max(choices[branches + 1][lines], value + branch_value);  // 부모 상태에 맞는 stem 또는 branch 역할로 이번 자식을 추가
//             if (lines == 0) choices[branches][1] = max(choices[branches][1], value + line_value);  // 아직 옆 경로가 없으면 이번 자식을 단순 경로로 추가
//         }  // 현재 가지 개수의 선택 처리 끝
//     }  // 자식 하나에 대한 배낭 갱신 끝
// }  // 자식 조합 갱신 함수 끝
//
// int solution(vector<vector<int>> t) {  // 각 정점을 최대 두 번 방문할 수 있는 가장 큰 부분 트리 크기 반환
//     int n = static_cast<int>(t.size()) + 1;  // 트리의 정점 수는 간선 수에 1을 더한 값
//     vector<vector<int>> adjacent(n);  // 무방향 인접 목록
//     for (const auto& edge : t) {  // 입력 간선을 양쪽 끝점에 모두 등록
//         adjacent[edge[0]].push_back(edge[1]);  // 첫 끝점에서 둘째 끝점으로 이동 가능
//         adjacent[edge[1]].push_back(edge[0]);  // 반대 방향도 이동 가능
//     }  // 인접 목록 완성
//     vector<int> parent(n, -1), order{0};  // 부모 번호는 미정으로 두고 계산용 루트 0부터 방문
//     parent[0] = 0;  // 루트의 부모는 자기 자신으로 표시
//     for (size_t index = 0; index < order.size(); ++index) {  // 자식을 뒤에 붙이며 부모부터 방문 순서 만들기
//         int node = order[index];  // 이번에 아래쪽 자식들을 찾을 정점
//         for (int child : adjacent[node]) {  // 연결된 정점 중 부모를 제외한 나머지가 자식
//             if (child == parent[node]) continue;  // 부모로 되돌아가는 간선 제외
//             parent[child] = node;  // 자식의 부모 기록
//             order.push_back(child);  // 자식을 방문 순서 뒤에 추가
//         }  // 현재 정점의 자식 등록 끝
//     }  // 부모 관계와 방문 순서 결정 끝
//     vector<int> line(n, 1), stem(n, 1), branch(n, 1);  // 단순 경로·부모에서 들어오는 중심 경로·왕복 접근 상태의 최댓값
//     int answer = 1;  // 정점 하나를 남긴 부분 트리부터 시작
//     for (auto it = order.rbegin(); it != order.rend(); ++it) {  // 긴 트리에서도 재귀 없이 자식부터 DP 계산
//         int node = *it;  // 현재 세 상태를 계산할 정점
//         Choices on_spine, off_spine;  // 현재 점이 양끝 사이 중심 경로 위·밖일 때의 자식 조합
//         for (auto& row : on_spine) row.fill(-1);  // 중심 경로 위 조합을 불가능 상태로 초기화
//         for (auto& row : off_spine) row.fill(-1);  // 중심 경로 밖 조합도 불가능 상태로 초기화
//         on_spine[0][0] = off_spine[0][0] = 0;  // 아무 자식도 고르지 않은 조합은 정점 수 0
//         int best_branch = 0;  // 왕복 접근 경로를 연장할 가장 좋은 자식 상태
//         for (int child : adjacent[node]) {  // 이미 계산된 각 자식의 세 상태를 조합
//             if (child == parent[node]) continue;  // 부모 쪽은 현재 부분 트리에 포함하지 않기
//             line[node] = max(line[node], 1 + line[child]);  // 단순 경로는 가장 긴 자식 경로 하나만 연장
//             best_branch = max(best_branch, branch[child]);  // 중심 경로 밖에서 접근 경로를 연장할 자식 하나 선택
//             add_child(on_spine, 2, stem[child], line[child]);  // 중심 경로를 잇는 자식 둘과 옆 단순 경로 하나까지 서로 겹치지 않게 선택
//             add_child(off_spine, 1, branch[child], line[child]);  // 중심 경로를 포함한 자식 하나와 반대편 단순 경로 하나 선택
//         }  // 모든 자식 조합 끝
//         branch[node] = 1 + best_branch;  // 현재 점이 중심 경로 밖이면 아래 자식 하나로 왕복 접근 경로 연장
//         for (int branches = 0; branches <= 2; ++branches) {  // 중심 경로에 연결하는 자식 수에 따라 상태별 최댓값 추출
//             for (int lines = 0; lines <= 1; ++lines) {  // 옆에 단순 경로를 붙였는지 두 경우 확인
//                 int value = on_spine[branches][lines];  // 자식들에서 얻은 정점 수의 합
//                 if (value >= 0) {  // 만들 수 있는 조합만 전체 답과 DP에 반영
//                     answer = max(answer, 1 + value);  // 현재 점이 중심 경로 위인 완성 부분 트리 후보
//                     if (branches <= 1) stem[node] = max(stem[node], 1 + value);  // 중심 경로의 한 방향을 부모가 쓰면 자식 쪽은 최대 한 방향
//                     if (lines == 0) branch[node] = max(branch[node], 1 + value);  // 부모가 옆 왕복 가지를 쓰는 경우 자식 쪽은 중심 경로 두 방향까지만 허용
//                 }  // 중심 경로 위 조합 반영 끝
//                 if (branches <= 1 && off_spine[branches][lines] >= 0) answer = max(answer, 1 + off_spine[branches][lines]);  // 중심 경로 밖에서는 왕복 가지가 현재 점에서 다른 자식 쪽으로 꺾이는 경우도 전체 답에 포함
//             }  // 옆 경로 포함 여부 처리 끝
//         }  // 현재 정점의 DP 계산 끝
//     }  // 전체 정점 처리 끝
//     return answer;  // 방문 제한을 만족하는 최대 부분 트리 크기 반환
// }  // 지역 컨테이너는 호출이 끝나면 해제되어 다음 채점에 상태가 남지 않음

// 풀이 요약
// 선택 정점이 둘 이상이면 시작·끝을 다르게 잡을 수 있음. 그 사이 단순 경로 P의 간선은 한 번, 나머지 간선은 왕복해서 모든 선택 정점 방문.
// 선택 차수를 d라 할 때 P 내부점의 방문 수는 d-1, P 양끝과 P 밖 정점은 d. 따라서 중심 경로 내부는 가지 하나를 옆에 붙일 수 있고, 옆 가지 자체는 갈라지지 않는 단순 경로여야 함.
// line은 아래로 뻗는 한 줄, stem은 부모 간선이 중심 경로인 상태, branch는 부모 간선을 왕복하고 중심 경로는 아래에 있는 상태.
// stem은 자식 stem 하나와 line 하나, branch는 자식 branch 하나 또는 stem 둘. 현재 점이 완성 트리의 맨 위이면 stem 둘+line 하나와 branch 하나+line 하나를 모두 비교.
// 각 조합을 3×2 배낭으로 역순 갱신해 같은 자식의 중복 사용 방지. 방문 순서를 뒤집어 재귀 없이 계산하므로 시간 O(N), 공간 O(N).

