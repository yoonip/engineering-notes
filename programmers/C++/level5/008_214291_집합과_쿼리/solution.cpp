#include <cstdint>
#include <string>
#include <vector>

using namespace std;

typedef struct { int left, right, parent, entered, lazy; uint64_t priority; } Node;

static uint64_t priority_of(uint64_t value) {
    value += UINT64_C(0x9e3779b97f4a7c15);
    value = (value ^ (value >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
    value = (value ^ (value >> 27)) * UINT64_C(0x94d049bb133111eb);
    return value ^ (value >> 31);
}

static void apply_time(Node* tree, int root, int when) {
    if (!root) return;
    tree[root].entered = when;
    tree[root].lazy = when;
}

static void push_time(Node* tree, int root) {
    int when = tree[root].lazy;
    if (when < 0) return;
    apply_time(tree, tree[root].left, when);
    apply_time(tree, tree[root].right, when);
    tree[root].lazy = -1;
}

static int merge_sets(Node* tree, int left, int right) {
    if (!left) {
        if (right) tree[right].parent = 0;
        return right;
    }
    if (!right) { tree[left].parent = 0; return left; }
    if (tree[left].priority < tree[right].priority) {
        push_time(tree, left);
        int child = merge_sets(tree, tree[left].right, right);
        tree[left].right = child;
        if (child) tree[child].parent = left;
        tree[left].parent = 0;
        return left;
    }
    push_time(tree, right);
    int child = merge_sets(tree, left, tree[right].left);
    tree[right].left = child;
    if (child) tree[child].parent = right;
    tree[right].parent = 0;
    return right;
}

static void split_time(Node* tree, int root, int bound, int* left, int* right) {
    if (!root) { *left = 0; *right = 0; return; }
    push_time(tree, root);
    if (tree[root].entered <= bound) {
        int child;
        split_time(tree, tree[root].right, bound, &child, right);
        tree[root].right = child;
        if (child) tree[child].parent = root;
        *left = root;
    } else {
        int child;
        split_time(tree, tree[root].left, bound, left, &child);
        tree[root].left = child;
        if (child) tree[child].parent = root;
        *right = root;
    }
    tree[root].parent = 0;
}

static int locate(const Node* tree, int node, int* when) {
    *when = tree[node].entered;
    while (1) {
        if (tree[node].lazy > *when) *when = tree[node].lazy;
        if (!tree[node].parent) return node;
        node = tree[node].parent;
    }
}

vector<string> solution(int n, vector<vector<int>> queries) {
    vector<Node> storage(n + 1);
    Node* tree = storage.data();
    for (int node = 1; node <= n; ++node) {
        tree[node].lazy = -1;
        tree[node].priority = priority_of(static_cast<uint64_t>(node));
    }
    vector<string> answer;
    answer.reserve(queries.size());
    for (size_t index = 0; index < queries.size(); ++index) {
        int kind = queries[index][0], x = queries[index][1] + 1, y = queries[index][2] + 1;
        int time_x, time_y;
        int root_x = locate(tree, x, &time_x), root_y = locate(tree, y, &time_y);
        int now = static_cast<int>(index) + 1;
        if (kind == 1) {
            if (root_x == root_y) continue;
            apply_time(tree, root_y, now);
            (void)merge_sets(tree, root_x, root_y);
        } else if (kind == 2) {
            if (time_x > time_y) continue;
            int before, middle, after, tail;
            split_time(tree, root_x, time_x - 1, &before, &tail);
            split_time(tree, tail, time_y, &middle, &after);
            apply_time(tree, middle, now);
            (void)merge_sets(tree, before, after);
        } else {
            answer.push_back(root_x == root_y ? "Yes" : "No");
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <cstdint>  // 트립 우선순위에 쓸 uint64_t와 64비트 상수
// #include <string>  // Yes 또는 No 응답 문자열
// #include <vector>  // 고정된 트립 노드 배열과 응답 목록
// 
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// 
// typedef struct { int left, right, parent, entered, lazy; uint64_t priority; } Node;  // 트립의 두 자식·부모, 현재 집합에 들어온 시각, 지연 시각, 균형 우선순위
// 
// static uint64_t priority_of(uint64_t value) {  // 원소 번호를 64비트로 섞어 트립 우선순위 만들기
//     value += UINT64_C(0x9e3779b97f4a7c15);  // 가까운 원소 번호도 서로 다른 비트 패턴에서 시작
//     value = (value ^ (value >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);  // 위쪽 비트를 아래쪽과 섞어 첫 번째 확산
//     value = (value ^ (value >> 27)) * UINT64_C(0x94d049bb133111eb);  // 비트를 다시 섞어 연속 번호의 우선순위 상관 줄이기
//     return value ^ (value >> 31);  // 섞인 64비트 우선순위 반환
// }  // 우선순위 생성 끝
// 
// static void apply_time(Node* tree, int root, int when) {  // 이동한 부분 집합 전체의 도착 시각을 한 번에 바꾸기
//     if (!root) return;  // 빈 부분 트리에는 적용할 원소가 없음
//     tree[root].entered = when;  // 부분 트리 루트 자체의 도착 시각 변경
//     tree[root].lazy = when;  // 자손도 같은 시각으로 바뀌었다는 일괄 대입 표시
// }  // 부분 집합 도착 시각 변경 끝
// 
// static void push_time(Node* tree, int root) {  // 트립을 나누거나 자식을 바꾸기 전에 지연 시각 전달
//     int when = tree[root].lazy;  // 이 부분 트리에 아직 내려보내지 않은 도착 시각
//     if (when < 0) return;  // -1이면 자손에게 전달할 일괄 대입이 없음
//     apply_time(tree, tree[root].left, when);  // 왼쪽 부분 집합에 같은 도착 시각 적용
//     apply_time(tree, tree[root].right, when);  // 오른쪽 부분 집합에도 같은 도착 시각 적용
//     tree[root].lazy = -1;  // 자식에게 넘겼으므로 현재 지연 표시는 해제
// }  // 도착 시각 지연 전파 끝
// 
// static int merge_sets(Node* tree, int left, int right) {  // 앞 집합과 뒤 집합을 도착 시각 순서대로 이어 붙이기
//     if (!left) {  // 앞부분이 없으면 뒤 트리 전체가 결과
//         if (right) tree[right].parent = 0;  // 반환할 트리 루트는 부모가 없음
//         return right;  // 뒤 트리의 루트 반환
//     }  // 앞부분이 빈 경우 처리 끝
//     if (!right) { tree[left].parent = 0; return left; }  // 뒤가 비었으면 앞 트리를 그대로 독립 루트로 반환
//     if (tree[left].priority < tree[right].priority) {  // 작은 우선순위를 루트로 써 트립 균형 유지
//         push_time(tree, left);  // 왼쪽 루트의 자식을 바꾸기 전에 도착 시각 전파
//         int child = merge_sets(tree, tree[left].right, right);  // 앞 트리의 오른쪽과 뒤 트리를 재귀적으로 연결
//         tree[left].right = child;  // 연결 결과를 왼쪽 루트의 오른쪽 자식으로 배치
//         if (child) tree[child].parent = left;  // 연결된 자식의 부모 포인터도 함께 갱신
//         tree[left].parent = 0;  // 반환할 전체 트리의 루트에는 부모가 없음
//         return left;  // 이어 붙인 트리의 루트 반환
//     }  // 앞 트리가 루트인 경우 처리 끝
//     push_time(tree, right);  // 뒤쪽 루트의 자식을 바꾸기 전에 도착 시각 전파
//     int child = merge_sets(tree, left, tree[right].left);  // 앞 트리와 뒤 트리의 왼쪽을 재귀적으로 연결
//     tree[right].left = child;  // 연결 결과를 오른쪽 루트의 왼쪽 자식으로 배치
//     if (child) tree[child].parent = right;  // 연결된 자식의 부모 포인터도 함께 갱신
//     tree[right].parent = 0;  // 반환할 전체 트리의 루트에는 부모가 없음
//     return right;  // 이어 붙인 트리의 루트 반환
// }  // 시각 순서에 따른 두 집합 병합 끝
// 
// static void split_time(Node* tree, int root, int bound, int* left, int* right) {  // 도착 시각이 bound 이하인 원소와 큰 원소로 분리
//     if (!root) { *left = 0; *right = 0; return; }  // 빈 트리를 나누면 양쪽 모두 빈 트리
//     push_time(tree, root);  // 자식의 시각과 연결을 확인하기 전에 지연 대입 전파
//     if (tree[root].entered <= bound) {  // 루트가 앞 구간에 속하면 오른쪽 자식만 더 나눔
//         int child;  // 분리 후에도 현재 루트에 남을 오른쪽 자식
//         split_time(tree, tree[root].right, bound, &child, right);  // 오른쪽에서 bound를 넘는 뒷부분 떼어내기
//         tree[root].right = child;  // bound 이하 부분만 현재 루트에 다시 연결
//         if (child) tree[child].parent = root;  // 남은 자식의 부모 포인터 복원
//         *left = root;  // 현재 루트가 앞 구간의 결과
//     } else {  // 루트가 뒤 구간에 속하면 왼쪽 자식만 더 나눔
//         int child;  // 분리 후에도 현재 루트에 남을 왼쪽 자식
//         split_time(tree, tree[root].left, bound, left, &child);  // 왼쪽에서 bound 이하의 앞부분 떼어내기
//         tree[root].left = child;  // bound를 넘는 부분만 현재 루트에 다시 연결
//         if (child) tree[child].parent = root;  // 남은 자식의 부모 포인터 복원
//         *right = root;  // 현재 루트가 뒤 구간의 결과
//     }  // 루트의 도착 시각에 따른 분리 끝
//     tree[root].parent = 0;  // 분리된 각 결과의 루트는 이전 부모와 끊기
// }  // 도착 시각 경계 분리 끝
// 
// static int locate(const Node* tree, int node, int* when) {  // 원소가 속한 집합의 루트와 실제 도착 시각 찾기
//     *when = tree[node].entered;  // 우선 원소 자신에게 저장된 도착 시각 읽기
//     while (1) {  // 부모 포인터를 따라 현재 집합의 트립 루트까지 이동
//         if (tree[node].lazy > *when) *when = tree[node].lazy;  // 더 최근의 조상 일괄 대입이 있으면 그 시각이 실제 도착 시각
//         if (!tree[node].parent) return node;  // 부모가 없으면 현재 집합의 루트에 도착
//         node = tree[node].parent;  // 다음 조상의 지연 시각 확인
//     }  // 루트를 반환할 때까지 조상 경로 확인
// }  // 집합과 도착 시각 조회 끝
// 
// vector<string> solution(int n, vector<vector<int>> queries) {  // 합치기·시각 구간 분리·같은 집합 조회를 순서대로 처리
//     vector<Node> storage(n + 1);  // 원소마다 트립 노드 하나를 만들고 0번은 빈 트리 표시로 사용
//     Node* tree = storage.data();  // 크기가 바뀌지 않는 노드 배열을 공통 트립 함수에 전달
//     for (int node = 1; node <= n; ++node) {  // 입력 원소 0부터 n-1을 내부 노드 1부터 n에 대응
//         tree[node].lazy = -1;  // 초기에는 전달할 도착 시각 변경이 없음
//         tree[node].priority = priority_of(static_cast<uint64_t>(node));  // 노드마다 고정된 균형 우선순위 배정
//     }  // 도착 시각 0의 단일 원소 집합 n개 준비 끝
//     vector<string> answer;  // 3번 쿼리의 Yes·No 결과를 순서대로 모을 목록
//     answer.reserve(queries.size());  // 결과 추가 중 배열을 반복 재할당하지 않도록 최대 크기 확보
//     for (size_t index = 0; index < queries.size(); ++index) {  // 입력 쿼리를 주어진 순서대로 실행
//         int kind = queries[index][0], x = queries[index][1] + 1, y = queries[index][2] + 1;  // 연산 종류와 내부 1부터 시작하는 두 원소 번호
//         int time_x, time_y;  // 두 원소가 현재 집합에 들어온 실제 쿼리 시각
//         int root_x = locate(tree, x, &time_x), root_y = locate(tree, y, &time_y);  // 두 원소의 집합 루트와 지연 대입을 반영한 시각 조회
//         int now = static_cast<int>(index) + 1;  // 현재 이동이 일어나면 새 도착 시각으로 쓸 쿼리 번호
//         if (kind == 1) {  // y의 집합 전체를 x의 집합으로 이동
//             if (root_x == root_y) continue;  // 이미 같은 집합이면 시각도 바꾸지 않고 건너뛰기
//             apply_time(tree, root_y, now);  // 이동하는 y 집합의 모든 원소를 현재 시각에 들어온 것으로 표시
//             (void)merge_sets(tree, root_x, root_y);  // 기존 x 집합 뒤에 새로 들어온 y 집합을 연결
//         } else if (kind == 2) {  // 같은 집합에서 x 시각부터 y 시각까지 새 집합으로 분리
//             if (time_x > time_y) continue;  // 시작 시각이 끝보다 늦으면 조건을 만족하는 원소가 없음
//             int before, middle, after, tail;  // 이동 구간 앞·이동 구간·뒤와 첫 분리의 뒷부분 루트
//             split_time(tree, root_x, time_x - 1, &before, &tail);  // x보다 먼저 들어온 원소를 앞부분으로 분리
//             split_time(tree, tail, time_y, &middle, &after);  // y와 같은 시각까지 들어온 원소를 이동 구간으로 분리
//             apply_time(tree, middle, now);  // 새 집합으로 옮긴 원소들은 모두 같은 현재 시각으로 변경
//             (void)merge_sets(tree, before, after);  // 원래 집합에 남은 앞뒤 구간을 다시 연결
//         } else {  // 3번 쿼리는 두 원소의 집합이 같은지 문자열로 기록
//             answer.push_back(root_x == root_y ? "Yes" : "No");  // 트립 루트가 같으면 Yes, 다르면 No를 결과 뒤에 추가
//         }  // 현재 쿼리 처리 끝
//     }  // 모든 쿼리 처리 끝
//     return answer;  // 응답 목록 반환, 노드 배열 메모리는 함수 종료 때 자동 해제
// }  // 집합과 쿼리 처리 끝

// 풀이 요약
// 각 집합을 들어온 시각의 비내림차순 트립으로 유지하고 부모 포인터로 원소의 현재 집합 조회
// 1번 쿼리는 y 집합의 시각을 현재 번호로 일괄 대입한 뒤 x 집합 뒤에 연결
// 2번 쿼리는 x 시각 미만, x~y 시각, y 시각 초과로 두 번 나누고 가운데만 새 집합으로 이동
// 같은 쿼리로 들어온 원소는 같은 시각이므로 경계에서 함께 이동; x가 더 늦게 들어왔으면 빈 구간
// 시각은 쿼리 번호에 따라 증가하므로 조상에 남은 가장 최근 지연 대입을 조회해 실제 도착 시각 계산
// 우선순위를 섞은 트립의 기대 높이 O(log N); 원소 N·쿼리 Q에 대해 기대 시간 O(N+Q log N), 공간 O(N+Q)
