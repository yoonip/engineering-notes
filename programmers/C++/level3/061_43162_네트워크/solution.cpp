#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> computers) {
    vector<bool> visited(n, false); int answer = 0;
    for (int start = 0; start < n; ++start) if (!visited[start]) {
        ++answer; vector<int> stack{start}; visited[start] = true;
        while (!stack.empty()) {
            int node = stack.back(); stack.pop_back();
            for (int next = 0; next < n; ++next) if (computers[node][next] && !visited[next]) { visited[next] = true; stack.push_back(next); }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> computers) {  // 방문하지 않은 컴퓨터에서 연결 요소 세기
// vector<bool> visited(n, false); int answer = 0;  // 방문 상태와 네트워크 수 초기화
// for (int start = 0; start < n; ++start) if (!visited[start]) {  // 새로운 연결 요소의 시작 컴퓨터 찾기
// ++answer; vector<int> stack{start}; visited[start] = true;  // 네트워크 하나를 세고 탐색을 시작
// while (!stack.empty()) {  // 연결된 컴퓨터를 모두 방문
// int node = stack.back(); stack.pop_back();  // 다음 컴퓨터를 스택에서 꺼내기
// for (int next = 0; next < n; ++next) if (computers[node][next] && !visited[next]) { visited[next] = true; stack.push_back(next); }  // 연결된 미방문 컴퓨터 넣기
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 전체 네트워크 개수 반환
// }  // 블록 끝

// 풀이 요약
// 인접 행렬에서 방문하지 않은 컴퓨터의 연결 요소를 깊이 우선 탐색하고 시작한 횟수 세기
