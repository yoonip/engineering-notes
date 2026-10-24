#include <algorithm>
#include <vector>

using namespace std;

int solution(int k, vector<int> num, vector<vector<int>> links) {
    int n = static_cast<int>(num.size());
    vector<bool> has_parent(n, false);
    vector<int> order;
    order.reserve(n);
    vector<int> remaining(n);
    int total = 0, largest = 0;
    for (int node = 0; node < n; ++node) {
        total += num[node];
        largest = max(largest, num[node]);
        for (int child : links[node]) {
            if (child != -1) has_parent[child] = true;
        }
    }
    int root = 0;
    while (has_parent[root]) ++root;
    order.push_back(root);
    for (size_t at = 0; at < order.size(); ++at) {
        int node = order[at];
        for (int child : links[node]) {
            if (child != -1) order.push_back(child);
        }
    }
    int low = max(largest, (total + k - 1) / k);
    int high = total;
    while (low < high) {
        int limit = low + (high - low) / 2;
        int groups = 1;
        for (int at = n - 1; at >= 0; --at) {
            int node = order[at];
            int left = links[node][0], right = links[node][1];
            int a = left == -1 ? 0 : remaining[left];
            int b = right == -1 ? 0 : remaining[right];
            if (a > b) swap(a, b);
            int people = num[node];
            if (people + a + b <= limit) {
                remaining[node] = people + a + b;
            } else if (people + a <= limit) {
                remaining[node] = people + a;
                ++groups;
            } else {
                remaining[node] = people;
                groups += 2;
            }
            if (groups > k) break;
        }
        if (groups <= k) high = limit;
        else low = limit + 1;
    }
    return low;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 자식 그룹 크기를 정렬하는 swap과 경계 최댓값 비교
// #include <vector>  // 부모 표시, 방문 순서, 열린 그룹 인원을 담을 vector
// 
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// 
// int solution(int k, vector<int> num, vector<vector<int>> links) {  // k개 그룹으로 나눌 때 가능한 최소의 최대 그룹 인원 계산
//     int n = static_cast<int>(num.size());  // 최대 10000개의 시험장 수를 반복문용 int로 저장
//     vector<bool> has_parent(n, false);  // 자식으로 등장한 노드를 표시할 배열을 false로 초기화
//     vector<int> order;  // 부모가 자식보다 먼저 나오는 방문 순서
//     order.reserve(n);  // 모든 시험장을 담을 공간을 한 번에 확보
//     vector<int> remaining(n);  // 부모에게 이어 붙일 열린 그룹 인원을 노드별로 저장
//     int total = 0, largest = 0;  // 전체 인원 합과 가장 큰 시험장 인원은 이분 탐색 경계에 사용
//     for (int node = 0; node < n; ++node) {  // 각 시험장의 인원과 자식 관계 확인
//         total += num[node];  // 한 그룹에 모두 넣었을 때의 인원 상한 계산
//         largest = max(largest, num[node]);  // 어느 그룹도 가장 큰 시험장 하나보다 작을 수 없음
//         for (int child : links[node]) {  // 왼쪽과 오른쪽 자식 두 칸 확인
//             if (child != -1) has_parent[child] = true;  // -1이 아닌 실제 자식에만 부모가 있다고 표시
//         }  // 현재 시험장의 자식 표시 끝
//     }  // 전체 인원과 부모 존재 정보 계산 끝
//     int root = 0;  // 부모가 없는 유일한 시험장을 찾을 시작 번호
//     while (has_parent[root]) ++root;  // 부모가 있는 노드를 건너뛰면 트리 루트가 남음
//     order.push_back(root);  // 루트부터 부모 우선 방문 순서 시작
//     for (size_t at = 0; at < order.size(); ++at) {  // 순서 앞에서 읽고 자식은 뒤에 붙여 재귀 없이 트리 방문
//         int node = order[at];  // 이번에 자식을 등록할 시험장 번호
//         for (int child : links[node]) {  // 두 자식을 방문 순서 뒤에 추가
//             if (child != -1) order.push_back(child);  // 존재하는 자식은 반드시 부모보다 뒤에 기록
//         }  // 현재 시험장의 자식 등록 끝
//     }  // 이 순서를 뒤에서 읽으면 모든 자식 계산이 부모보다 먼저 끝남
//     int low = max(largest, (total + k - 1) / k);  // 가장 큰 시험장과 전체 인원의 k등분 평균 올림을 하한으로 사용
//     int high = total;  // 모든 시험장을 한 그룹으로 묶는 인원은 항상 가능한 상한
//     while (low < high) {  // 가능한 최소 인원 제한 하나로 탐색 구간을 좁히기
//         int limit = low + (high - low) / 2;  // 이번에 가능한지 검사할 최대 그룹 인원
//         int groups = 1;  // 트리 전체 한 그룹에서 간선을 끊을 때마다 그룹 수 증가
//         for (int at = n - 1; at >= 0; --at) {  // 방문 순서를 거꾸로 읽어 자식의 열린 그룹부터 계산
//             int node = order[at];  // 두 자식 결과를 합칠 현재 시험장
//             int left = links[node][0], right = links[node][1];  // 왼쪽과 오른쪽 자식 번호
//             int a = left == -1 ? 0 : remaining[left];  // 왼쪽 자식이 없으면 열린 그룹 인원은 0
//             int b = right == -1 ? 0 : remaining[right];  // 오른쪽 자식이 없으면 열린 그룹 인원은 0
//             if (a > b) swap(a, b);  // 자식 하나만 남겨야 할 때 작은 그룹을 고르도록 a를 작은 값으로 정렬
//             int people = num[node];  // 현재 시험장 자체의 인원
//             if (people + a + b <= limit) {  // 두 자식의 열린 그룹을 모두 붙여도 제한 이내이면
//                 remaining[node] = people + a + b;  // 간선을 끊지 않고 두 자식 모두 부모 쪽 그룹에 포함
//             } else if (people + a <= limit) {  // 둘 다는 못 붙여도 작은 자식 하나는 붙일 수 있으면
//                 remaining[node] = people + a;  // 부모에게 넘길 인원을 작게 남겨 이후 합치기에 유리하게 만들기
//                 ++groups;  // 큰 자식 쪽 간선을 한 개 끊어 별도 그룹 생성
//             } else {  // 작은 자식도 붙일 수 없으면 두 자식 모두 분리
//                 remaining[node] = people;  // 현재 시험장만 열린 그룹에 남기기
//                 groups += 2;  // 두 자식 간선을 끊어 그룹 두 개 추가
//             }  // 현재 시험장의 열린 그룹과 필요한 절단 수 확정
//             if (groups > k) break;  // 그룹이 이미 너무 많으면 남은 부모를 계산해도 줄일 수 없으므로 중단
//         }  // 현재 인원 제한에서 필요한 그룹 수 검사 끝
//         if (groups <= k) high = limit;  // 가능한 제한이면 더 작은 인원을 시도
//         else low = limit + 1;  // 불가능한 제한 이하를 버리고 인원 제한을 늘리기
//     }  // low와 high가 가능한 최소 최대 인원에 도달
//     return low;  // 최소화한 최대 그룹 인원 반환, vector 메모리는 함수 종료 때 자동 해제
// }  // 시험장 분할 계산 끝

// 풀이 요약
// 최대 그룹 인원을 이분 탐색하고, 부모 우선 방문 순서를 뒤에서 읽어 자식부터 필요한 절단 수 계산
// 둘 다 붙일 수 있으면 유지하고, 하나만 붙일 때는 작은 자식 그룹을 남겨 부모에게 넘길 인원을 최소화
// k개 이하로 나눌 수 있으면 간선을 더 끊어 정확히 k개로 만들 수 있으므로 그 인원 제한은 가능
// 전체 인원 S, 시험장 수 N에 대해 시간 O(N log S), 공간 O(N); 재귀 없이 깊이 10000인 트리도 처리
// 공식 예제의 답은 40, 27, 14, 9
