#include <algorithm>
#include <limits>
#include <vector>

using namespace std;

struct RootedTree {
    vector<vector<int>> children;
    vector<int> order;
};

static RootedTree root_tree(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adjacent(n + 1);
    for (const auto& edge : edges) {
        adjacent[edge[0]].push_back(edge[1]);
        adjacent[edge[1]].push_back(edge[0]);
    }
    RootedTree tree{vector<vector<int>>(n + 1), {1}};
    vector<int> parent(n + 1, 0);
    for (size_t index = 0; index < tree.order.size(); ++index) {
        int node = tree.order[index];
        for (int next : adjacent[node]) {
            if (next == parent[node]) continue;
            parent[next] = node;
            tree.children[node].push_back(next);
            tree.order.push_back(next);
        }
    }
    return tree;
}

static int maximum_matching(const vector<vector<int>>& weight) {
    int rows = static_cast<int>(weight.size());
    if (rows == 0) return 0;
    int columns = static_cast<int>(weight[0].size());
    const int infinity = numeric_limits<int>::max() / 4;
    vector<int> row_potential(rows + 1), column_potential(columns + 1);
    vector<int> matched_row(columns + 1), previous_column(columns + 1);
    for (int row = 1; row <= rows; ++row) {
        matched_row[0] = row;
        int column = 0;
        vector<int> slack(columns + 1, infinity);
        vector<char> used(columns + 1, false);
        do {
            used[column] = true;
            int current_row = matched_row[column];
            int delta = infinity, next_column = 0;
            for (int candidate = 1; candidate <= columns; ++candidate) {
                if (used[candidate]) continue;
                int cost = -weight[current_row - 1][candidate - 1] - row_potential[current_row] - column_potential[candidate];
                if (cost < slack[candidate]) {
                    slack[candidate] = cost;
                    previous_column[candidate] = column;
                }
                if (slack[candidate] < delta) {
                    delta = slack[candidate];
                    next_column = candidate;
                }
            }
            for (int candidate = 0; candidate <= columns; ++candidate) {
                if (used[candidate]) {
                    row_potential[matched_row[candidate]] += delta;
                    column_potential[candidate] -= delta;
                } else {
                    slack[candidate] -= delta;
                }
            }
            column = next_column;
        } while (matched_row[column] != 0);
        do {
            int previous = previous_column[column];
            matched_row[column] = matched_row[previous];
            column = previous;
        } while (column != 0);
    }
    int total = 0;
    for (int column = 1; column <= columns; ++column) {
        if (matched_row[column] != 0) total += weight[matched_row[column] - 1][column - 1];
    }
    return total;
}

int solution(int n1, vector<vector<int>> g1, int n2, vector<vector<int>> g2) {
    RootedTree first = root_tree(n1, g1);
    RootedTree second = root_tree(n2, g2);
    vector<vector<int>> common(n1 + 1, vector<int>(n2 + 1));
    for (auto left = first.order.rbegin(); left != first.order.rend(); ++left) {
        int u = *left;
        for (auto right = second.order.rbegin(); right != second.order.rend(); ++right) {
            int v = *right;
            const auto& a = first.children[u];
            const auto& b = second.children[v];
            bool transposed = a.size() > b.size();
            int rows = static_cast<int>(min(a.size(), b.size()));
            int columns = static_cast<int>(max(a.size(), b.size()));
            vector<vector<int>> weight(rows, vector<int>(columns));
            for (int row = 0; row < rows; ++row) {
                for (int column = 0; column < columns; ++column) {
                    weight[row][column] = transposed ? common[a[column]][b[row]] : common[a[row]][b[column]];
                }
            }
            common[u][v] = 1 + maximum_matching(weight);
        }
    }
    return common[1][1];
}

// 전체 코드 줄별 설명
// #include <algorithm>  // min·max로 두 자식 집합의 작은 쪽과 큰 쪽을 구분
// #include <limits>  // 매칭에서 아직 찾지 못한 비용을 표시할 큰 정수
// #include <vector>  // 인접 목록·트리 DP·매칭 배열을 동적으로 보관
//
// using namespace std;  // 표준 라이브러리 이름 앞의 std:: 생략
//
// struct RootedTree {  // 무방향 간선을 루트 기준 자식 목록과 방문 순서로 바꿔 보관
//     vector<vector<int>> children;  // 각 정점에서 아래로 내려가는 자식 번호들
//     vector<int> order;  // 부모가 자식보다 먼저 나오는 방문 순서
// };  // 루트 트리 자료형 끝
//
// static RootedTree root_tree(int n, const vector<vector<int>>& edges) {  // 1번을 루트로 삼아 부모·자식 방향 결정
//     vector<vector<int>> adjacent(n + 1);  // 정점 번호 1~n에 대응하는 양방향 인접 목록
//     for (const auto& edge : edges) {  // 입력 간선의 두 끝점은 어느 쪽이 부모인지 아직 모르는 상태
//         adjacent[edge[0]].push_back(edge[1]);  // 첫 번째 끝점에서 두 번째 끝점으로 갈 수 있게 등록
//         adjacent[edge[1]].push_back(edge[0]);  // 반대 방향도 등록해 입력 순서의 영향을 없애기
//     }  // 무방향 인접 목록 완성
//     RootedTree tree{vector<vector<int>>(n + 1), {1}};  // 자식 목록은 비우고 방문 순서는 루트 1번부터 시작
//     vector<int> parent(n + 1, 0);  // 부모로 다시 올라가는 간선을 걸러낼 배열
//     for (size_t index = 0; index < tree.order.size(); ++index) {  // 뒤에 새 자식을 붙이면서 부모부터 순회
//         int node = tree.order[index];  // 이번에 자식들을 찾을 정점
//         for (int next : adjacent[node]) {  // 연결된 정점 중 부모를 제외한 나머지가 자식
//             if (next == parent[node]) continue;  // 부모로 되돌아가는 간선은 자식 목록에서 제외
//             parent[next] = node;  // 다음 정점에서 되돌아갈 부모 번호 기록
//             tree.children[node].push_back(next);  // 현재 정점 아래의 자식으로 등록
//             tree.order.push_back(next);  // 자식은 부모 뒤에 방문하도록 순서 끝에 추가
//         }  // 현재 정점의 모든 자식 등록 끝
//     }  // 루트 기준 방향 결정 끝
//     return tree;  // 자식 목록과 방문 순서를 함께 반환
// }  // 루트 트리 만들기 끝
//
// static int maximum_matching(const vector<vector<int>>& weight) {  // 작은 자식 집합을 행으로 둔 최대 가중치 이분매칭
//     int rows = static_cast<int>(weight.size());  // 반드시 하나씩 상대를 고를 작은 쪽 자식 수
//     if (rows == 0) return 0;  // 한쪽에 자식이 없으면 더 붙일 공통 정점도 없음
//     int columns = static_cast<int>(weight[0].size());  // 각 행이 선택할 수 있는 큰 쪽 자식 수
//     const int infinity = numeric_limits<int>::max() / 4;  // 아직 연결 경로를 찾지 못한 열의 비용 상한
//     vector<int> row_potential(rows + 1), column_potential(columns + 1);  // Hungarian의 축약 비용을 유지할 행·열 잠재값
//     vector<int> matched_row(columns + 1), previous_column(columns + 1);  // 열에 배정된 행과 최단 증대 경로의 직전 열
//     for (int row = 1; row <= rows; ++row) {  // 작은 쪽 자식을 하나씩 현재 최적 매칭에 추가
//         matched_row[0] = row;  // 0번 가상 열에서 이번 미배정 행의 탐색 시작
//         int column = 0;  // 현재 증대 경로 탐색의 끝 열
//         vector<int> slack(columns + 1, infinity);  // 현재 탐색 트리에서 각 열로 넘어갈 최소 축약 비용
//         vector<char> used(columns + 1, false);  // 이미 탐색 트리에 들어온 열 표시
//         do {  // 비어 있는 열을 찾을 때까지 번갈아 행·열을 확장
//             used[column] = true;  // 현재 열을 탐색 트리에 포함
//             int current_row = matched_row[column];  // 이 열에 묶인 행에서 다음 후보 열을 살펴보기
//             int delta = infinity, next_column = 0;  // 가장 작은 남은 축약 비용과 그 열을 찾을 준비
//             for (int candidate = 1; candidate <= columns; ++candidate) {  // 아직 탐색하지 않은 모든 상대 자식 검사
//                 if (used[candidate]) continue;  // 이미 들어온 열은 새 경로 후보에서 제외
//                 int cost = -weight[current_row - 1][candidate - 1] - row_potential[current_row] - column_potential[candidate];  // 공통부분 크기에 음수를 붙여 최대합을 최소비용 문제로 바꾸기
//                 if (cost < slack[candidate]) {  // 이 행을 거치면 해당 열까지 더 작은 축약 비용으로 도달
//                     slack[candidate] = cost;  // 그 열까지의 최선 비용 갱신
//                     previous_column[candidate] = column;  // 나중에 매칭을 뒤집을 때 따라갈 직전 열 기록
//                 }  // 후보 열의 최선 경로 갱신 끝
//                 if (slack[candidate] < delta) {  // 다음에 확장할 열은 남은 비용이 가장 작은 열
//                     delta = slack[candidate];  // 잠재값을 이동시킬 최소 비용 차이
//                     next_column = candidate;  // 그 차이로 도달할 열 번호 저장
//                 }  // 다음 확장 열 선택 끝
//             }  // 모든 미방문 열 검사 끝
//             for (int candidate = 0; candidate <= columns; ++candidate) {  // 최소 비용 차이만큼 잠재값과 남은 비용을 함께 조정
//                 if (used[candidate]) {  // 탐색 트리 안의 행·열은 잠재값을 반대 방향으로 이동
//                     row_potential[matched_row[candidate]] += delta;  // 탐색에 포함된 행의 잠재값 조정
//                     column_potential[candidate] -= delta;  // 짝을 이루는 열의 잠재값은 반대로 조정
//                 } else {  // 탐색 밖의 열은 도달에 필요한 남은 비용만 감소
//                     slack[candidate] -= delta;  // 최소 비용 열 중 하나의 slack이 0이 되도록 조정
//                 }  // 한 열의 잠재값·남은 비용 조정 끝
//             }  // 이번 잠재값 갱신 끝
//             column = next_column;  // 비용 0으로 확장 가능한 다음 열로 이동
//         } while (matched_row[column] != 0);  // 이미 배정된 열이면 그 행을 거쳐 계속 탐색
//         do {  // 빈 열에서 가상 시작 열까지 경로를 거꾸로 따라 매칭 변경
//             int previous = previous_column[column];  // 현재 열로 들어오기 직전의 열
//             matched_row[column] = matched_row[previous];  // 직전 열의 행을 현재 열로 옮겨 새 매칭 구성
//             column = previous;  // 경로의 앞쪽 열도 같은 방식으로 갱신
//         } while (column != 0);  // 가상 시작 열에 닿으면 이번 행 배정 완료
//     }  // 작은 쪽의 모든 자식 배정 끝
//     int total = 0;  // 선택된 자식 쌍들의 공통부분 크기 합
//     for (int column = 1; column <= columns; ++column) {  // 실제로 짝이 배정된 열의 원래 가중치를 더하기
//         if (matched_row[column] != 0) total += weight[matched_row[column] - 1][column - 1];  // 가상 행 0은 제외하고 선택된 자식 쌍의 DP값만 합산
//     }  // 매칭 가중치 합산 끝
//     return total;  // 자식들을 일대일로 연결해 얻는 최대 공통 정점 수
// }  // 최대 가중치 매칭 끝
//
// int solution(int n1, vector<vector<int>> g1, int n2, vector<vector<int>> g2) {  // 두 트리의 1번 루트를 포함하는 최대 공통부분 크기 반환
//     RootedTree first = root_tree(n1, g1);  // 첫 트리의 부모·자식 관계 결정
//     RootedTree second = root_tree(n2, g2);  // 둘째 트리도 같은 방식으로 루트 방향 결정
//     vector<vector<int>> common(n1 + 1, vector<int>(n2 + 1));  // common[u][v]는 두 정점을 대응시켰을 때의 최대 공통부분 크기
//     for (auto left = first.order.rbegin(); left != first.order.rend(); ++left) {  // 첫 트리의 자식 DP가 부모보다 먼저 나오도록 방문 순서를 뒤집기
//         int u = *left;  // 첫 트리에서 이번에 비교할 부분 트리의 루트
//         for (auto right = second.order.rbegin(); right != second.order.rend(); ++right) {  // 둘째 트리도 자식부터 올라오며 정점 쌍 처리
//             int v = *right;  // 둘째 트리에서 대응시킬 부분 트리의 루트
//             const auto& a = first.children[u];  // 첫 부분 트리의 바로 아래 자식들
//             const auto& b = second.children[v];  // 둘째 부분 트리의 바로 아래 자식들
//             bool transposed = a.size() > b.size();  // Hungarian의 행이 더 작도록 필요하면 두 자식 집합의 방향 교체
//             int rows = static_cast<int>(min(a.size(), b.size()));  // 짝을 고를 작은 쪽 자식 수
//             int columns = static_cast<int>(max(a.size(), b.size()));  // 상대 후보가 되는 큰 쪽 자식 수
//             vector<vector<int>> weight(rows, vector<int>(columns));  // 각 자식 쌍을 대응시켰을 때 얻는 정점 수로 매칭 행렬 구성
//             for (int row = 0; row < rows; ++row) {  // 작은 쪽 자식마다 가능한 모든 상대 자식 검사
//                 for (int column = 0; column < columns; ++column) {  // 서로 다른 상대 자식들이 열을 하나씩 차지하도록 가중치 준비
//                     weight[row][column] = transposed ? common[a[column]][b[row]] : common[a[row]][b[column]];  // 행렬을 전치해도 DP의 첫 인덱스는 항상 첫 트리 정점으로 유지
//                 }  // 현재 자식의 상대별 가중치 계산 끝
//             }  // 자식 쌍 가중치 행렬 완성
//             common[u][v] = 1 + maximum_matching(weight);  // 현재 루트 한 개에 최선의 자식 일대일 대응 결과를 더하기
//         }  // 현재 첫 트리 정점과 둘째 트리의 모든 정점 비교 끝
//     }  // 모든 부분 트리 쌍의 DP 계산 끝
//     return common[1][1];  // 두 원래 루트가 대응하는 최대 공통부분 크기 반환
// }  // 지역 배열들은 호출이 끝나면 해제되어 다음 채점에 상태가 남지 않음

// 풀이 요약
// 루트를 포함하는 공통부분에서는 서로 다른 자식 가지가 서로 다른 상대 가지에 대응해야 함.
// common[u][v]를 두 정점이 같은 사람이라고 볼 때 남길 수 있는 최대 정점 수로 두고, 자식 쌍 DP를 가중치로 한 최대 이분매칭에 루트 1개를 더함.
// 자식 쌍은 최소 루트 한 개를 공유하므로 작은 쪽 자식을 모두 매칭해도 손해가 없음. 가중치에 음수를 붙인 직사각 Hungarian으로 최대합 계산.
// 부모부터 만든 방문 순서를 뒤집어 자식 DP를 먼저 계산. 입력 간선의 두 끝점 순서나 자식 번호에는 영향받지 않음.
// 정점 수 n1·n2에서 시간 O(n1*n2*min(n1,n2)), 공간 O(n1*n2). n1,n2<=100 범위에서 재귀 없이 처리.

