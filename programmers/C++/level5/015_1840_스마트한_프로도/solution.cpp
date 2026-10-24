#include <queue>
#include <vector>
using namespace std;

vector<vector<int>> solution(int n, int m, vector<int> a, vector<int> b, int k, int m1, int m2, vector<int> e1, vector<int> e2) {
    (void)m; (void)k; (void)m1;
    vector<int> current(n + 1), goal(n + 1, -1), degree(m2);
    vector<char> done(m2, 0);
    vector<vector<int>> answer;
    queue<int> ready;
    for (int id : e1) current[a[id - 1]] = current[b[id - 1]] = id;
    for (int i = 0; i < m2; ++i) {
        int id = e2[i];
        goal[a[id - 1]] = goal[b[id - 1]] = i;
    }
    int remaining = m2;
    for (int i = 0; i < m2; ++i) {
        int id = e2[i], u = a[id - 1], v = b[id - 1];
        if (current[u] == id) { done[i] = 1; --remaining; }
        else {
            degree[i] = (current[u] != 0) + (current[v] != 0);
            if (degree[i] <= 1) ready.push(i);
        }
    }
    auto remove_edge = [&](int id) {
        if (id == 0) return;
        int u = a[id - 1], v = b[id - 1];
        answer.push_back({0, id});
        current[u] = current[v] = 0;
        for (int vertex : {u, v}) {
            int target = goal[vertex];
            if (target >= 0 && !done[target] && --degree[target] == 1) ready.push(target);
        }
    };
    int next = 0;
    while (remaining > 0) {
        while (!ready.empty() && done[ready.front()]) ready.pop();
        int target;
        if (!ready.empty()) { target = ready.front(); ready.pop(); }
        else {
            while (done[next]) ++next;
            target = next;
        }
        done[target] = 1; --remaining;
        int id = e2[target], u = a[id - 1], v = b[id - 1];
        remove_edge(current[u]);
        remove_edge(current[v]);
        current[u] = current[v] = id;
        answer.push_back({1, id});
    }
    for (int id : e1) {
        int u = a[id - 1];
        if (current[u] == id && (goal[u] < 0 || e2[goal[u]] != id)) remove_edge(id);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <queue>  // 충돌 간선이 적은 목표 간선을 먼저 처리할 큐
// #include <vector>  // 현재 매칭·목표 매칭·변환 연산 저장
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<vector<int>> solution(int n, int m, vector<int> a, vector<int> b, int k, int m1, int m2, vector<int> e1, vector<int> e2) {  // 현재 매칭을 목표 매칭으로 바꾸는 간선 삭제·추가 목록 계산
//     (void)m; (void)k; (void)m1;  // 간선 벡터의 크기와 입력의 매칭 크기 보장을 사용하므로 이 인자는 따로 계산하지 않음
//     vector<int> current(n + 1), goal(n + 1, -1), degree(m2);  // 정점별 현재 간선·목표 간선 번호와 목표 간선의 충돌 수
//     vector<char> done(m2, 0);  // 이미 보존하거나 추가한 목표 간선을 표시
//     vector<vector<int>> answer;  // 변환 순서대로 삭제 0·추가 1과 간선 번호 저장
//     queue<int> ready;  // 지금 충돌하는 현재 간선이 0~1개인 목표 간선의 대기열
//     for (int id : e1) current[a[id - 1]] = current[b[id - 1]] = id;  // 초기 매칭 간선을 두 끝점에 등록
//     for (int i = 0; i < m2; ++i) {  // 각 정점이 최종적으로 속할 목표 간선 인덱스 등록
//         int id = e2[i];  // 입력의 간선 번호를 가져와 좌표 배열에서는 1을 빼서 사용
//         goal[a[id - 1]] = goal[b[id - 1]] = i;  // 목표 매칭은 정점마다 간선이 최대 하나라 한 칸에 기록 가능
//     }  // 목표 끝점 등록 끝
//     int remaining = m2;  // 아직 현재 매칭에 확정하지 않은 목표 간선 수
//     for (int i = 0; i < m2; ++i) {  // 공통 간선과 각 목표 간선의 초기 충돌 수 계산
//         int id = e2[i], u = a[id - 1], v = b[id - 1];  // 목표 간선의 양끝 정점 조회
//         if (current[u] == id) { done[i] = 1; --remaining; }  // 이미 들어 있는 공통 간선은 그대로 남기기
//         else {  // 아직 없는 목표 간선만 작업 대상으로 등록
//             degree[i] = (current[u] != 0) + (current[v] != 0);  // 두 끝점에서 제거해야 할 현재 매칭 간선 수 계산
//             if (degree[i] <= 1) ready.push(i);  // 한 간선 이하만 지우면 되는 목표부터 우선 처리
//         }  // 초기 충돌 계산 끝
//     }  // 초기 작업 대기열 구성 끝
//     auto remove_edge = [&](int id) {  // 현재 매칭 간선 하나를 지우고 영향을 받은 목표의 충돌 수 갱신
//         if (id == 0) return;  // 끝점이 이미 비어 있으면 지울 간선 없음
//         int u = a[id - 1], v = b[id - 1];  // 삭제할 간선의 양끝 조회
//         answer.push_back({0, id});  // 이번 삭제 연산을 정답 순서에 추가
//         current[u] = current[v] = 0;  // 두 정점을 현재 매칭에서 비우기
//         for (int vertex : {u, v}) {  // 삭제한 간선과 접해 있던 목표 간선들을 확인
//             int target = goal[vertex];  // 해당 끝점의 목표 간선 인덱스 조회
//             if (target >= 0 && !done[target] && --degree[target] == 1) ready.push(target);  // 미완료 목표의 충돌이 하나로 줄었으면 대기열에 추가
//         }  // 이웃 목표의 충돌 갱신 끝
//     };  // 간선 삭제 보조 함수 끝
//     int next = 0;  // 대기열이 비었을 때 새 교대 성분을 시작할 목표 인덱스
//     while (remaining > 0) {  // 모든 목표 간선을 현재 매칭에 확정할 때까지 반복
//         while (!ready.empty() && done[ready.front()]) ready.pop();  // 다른 처리로 이미 끝난 대기열 항목 제거
//         int target;  // 이번에 추가할 목표 간선의 인덱스
//         if (!ready.empty()) { target = ready.front(); ready.pop(); }  // 충돌 0~1개인 목표를 먼저 선택
//         else {  // 남은 교대 성분의 모든 목표가 두 현재 간선과 충돌하는 경우
//             while (done[next]) ++next;  // 아직 확정하지 않은 목표 간선 찾기
//             target = next;  // 현재 크기에서 최대 두 간선만 지워 새 성분 시작
//         }  // 처리할 목표 선택 끝
//         done[target] = 1; --remaining;  // 자기 자신의 충돌 감소는 세지 않도록 먼저 완료 표시
//         int id = e2[target], u = a[id - 1], v = b[id - 1];  // 목표 간선 번호와 끝점 조회
//         remove_edge(current[u]);  // 첫 끝점을 차지한 이전 매칭 간선 삭제
//         remove_edge(current[v]);  // 두 번째 끝점도 비우기
//         current[u] = current[v] = id;  // 비워진 두 끝점에 목표 간선 확정
//         answer.push_back({1, id});  // 추가 연산을 삭제 연산 뒤에 기록
//     }  // 모든 목표 간선 확정 끝
//     for (int id : e1) {  // 목표와 접하지 않아 아직 남은 초기 간선 정리
//         int u = a[id - 1];  // 현재 매칭에 이 간선이 남았는지 확인할 끝점
//         if (current[u] == id && (goal[u] < 0 || e2[goal[u]] != id)) remove_edge(id);  // 목표 공통 간선은 보존하고 초기 간선만 삭제
//     }  // 초기 잔여 간선 정리 끝
//     return answer;  // 매 단계가 매칭인 변환 연산 목록 반환
// }  // solution 함수 끝

// 풀이 요약
// 초기·목표 매칭의 대칭 차이는 교대 경로와 교대 사이클로 나뉨. 목표 간선을 넣기 전에 끝점의 기존 간선만 삭제.
// 충돌이 0~1개인 목표 간선을 먼저 처리하고, 그런 간선이 없을 때만 두 간선을 지워 새 교대 성분을 시작.
// 두 충돌 성분을 시작할 때는 현재 크기가 최종 목표 크기 이상. 이후 교대 성분을 따라가는 동안의 일시 감소까지 합쳐도 k-2 아래로 내려가지 않음.
// 공통 목표 간선은 남기고, 모든 목표를 넣은 뒤 남은 초기 간선만 제거. 삭제·추가는 각각 간선당 최대 한 번.
// 정점 수 N, 초기·목표 간선 수 M1·M2에서 보조 처리 시간 O(N+M1+M2), 입력 간선 배열 보관까지 공간 O(N+M).
