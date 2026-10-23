#include <algorithm>
#include <numeric>
#include <utility>
#include <vector>
using namespace std;

vector<vector<int>> solution(vector<vector<int>> nodeinfo) {
    int n = (int)nodeinfo.size(); vector<int> left(n,-1), right(n,-1), order(n); iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(), [&](int a, int b) { return nodeinfo[a][0] < nodeinfo[b][0]; });
    vector<int> stack;
    for (int node : order) {
        int last = -1;
        while (!stack.empty() && nodeinfo[stack.back()][1] < nodeinfo[node][1]) { last = stack.back(); stack.pop_back(); }
        if (!stack.empty()) right[stack.back()] = node;
        if (last != -1) left[node] = last;
        stack.push_back(node);
    }
    int root = stack.front(); vector<int> preorder, postorder; vector<pair<int,bool>> work{{root,false}};
    while (!work.empty()) {
        auto [node,finished] = work.back(); work.pop_back();
        if (finished) postorder.push_back(node + 1);
        else {
            preorder.push_back(node + 1); work.push_back({node,true});
            if (right[node] != -1) work.push_back({right[node],false});
            if (left[node] != -1) work.push_back({left[node],false});
        }
    }
    return {preorder,postorder};
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<vector<int>> solution(vector<vector<int>> nodeinfo) {  // 좌표 우선순위로 트리를 만들고 두 순회 복원
// int n = (int)nodeinfo.size(); vector<int> left(n,-1), right(n,-1), order(n); iota(order.begin(), order.end(), 0);  // 좌우 자식과 x좌표 정렬 순서 저장
// sort(order.begin(), order.end(), [&](int a, int b) { return nodeinfo[a][0] < nodeinfo[b][0]; });  // 노드를 왼쪽에서 오른쪽 순서로 정렬
// vector<int> stack;  // y좌표가 감소하는 조상 후보 스택
// for (int node : order) {  // 각 노드를 Cartesian tree에 추가
// int last = -1;  // 현재 노드의 왼쪽 서브트리가 될 마지막 제거 노드
// while (!stack.empty() && nodeinfo[stack.back()][1] < nodeinfo[node][1]) { last = stack.back(); stack.pop_back(); }  // 더 낮은 y좌표 노드를 현재 노드 아래로 내리기
// if (!stack.empty()) right[stack.back()] = node;  // 남은 조상의 오른쪽 자식으로 연결
// if (last != -1) left[node] = last;  // 제거한 서브트리를 현재 노드의 왼쪽에 연결
// stack.push_back(node);  // 현재 노드를 조상 후보에 넣기
// }  // 블록 끝
// int root = stack.front(); vector<int> preorder, postorder; vector<pair<int,bool>> work{{root,false}};  // 전위 및 후위 순회를 반복문으로 시작
// while (!work.empty()) {  // 모든 노드를 방문
// auto [node,finished] = work.back(); work.pop_back();  // 현재 노드와 자식 처리 완료 여부 읽기
// if (finished) postorder.push_back(node + 1);  // 자식을 모두 처리했으면 후위 순서에 넣기
// else {  // 처음 방문할 때는 전위 순서에 넣고 자식을 예약
// preorder.push_back(node + 1); work.push_back({node,true});  // 현재 노드를 기록하고 완료 단계도 스택에 두기
// if (right[node] != -1) work.push_back({right[node],false});  // 오른쪽을 먼저 넣어 나중에 처리
// if (left[node] != -1) work.push_back({left[node],false});  // 왼쪽이 스택 끝에서 먼저 처리됨
// }  // 블록 끝
// }  // 블록 끝
// return {preorder,postorder};  // 전위 순회와 후위 순회 결과 반환
// }  // 블록 끝

// 풀이 요약
// x좌표 순서와 y좌표 우선순위로 Cartesian tree를 만든 뒤 반복문으로 전위 및 후위 순회 구하기
