# 바이러스 파이프

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468373) · Level 2 · C++

## 풀이

파이프 종류별 연결 요소를 미리 구하고, 감염된 정점에 닿는 연결 요소 전체를 감염시키는 선택을 최대 k번 탐색

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(int n, int infection, vector<vector<int>> edges, int k) {
    vector<vector<vector<int>>> graph(3, vector<vector<int>>(n));
    for (const auto& edge : edges) {
        int a = edge[0] - 1, b = edge[1] - 1, type = edge[2] - 1;
        graph[type][a].push_back(b);
        graph[type][b].push_back(a);
    }
    vector<vector<vector<int>>> groups(3);
    for (int type = 0; type < 3; ++type) {
        vector<bool> visited(n, false);
        for (int start = 0; start < n; ++start) {
            if (visited[start]) continue;
            vector<int> component, stack{start};
            visited[start] = true;
            while (!stack.empty()) {
                int node = stack.back(); stack.pop_back();
                component.push_back(node);
                for (int next : graph[type][node]) if (!visited[next]) {
                    visited[next] = true;
                    stack.push_back(next);
                }
            }
            groups[type].push_back(component);
        }
    }
    int answer = 1;
    function<void(vector<bool>, int)> dfs = [&](vector<bool> infected, int remaining) {
        int count = (int)std::count(infected.begin(), infected.end(), true);
        answer = max(answer, count);
        if (remaining == 0 || answer == n) return;
        for (const auto& components : groups) {
            vector<bool> next = infected;
            for (const auto& component : components) {
                bool touched = false;
                for (int node : component) touched = touched || infected[node];
                if (touched) for (int node : component) next[node] = true;
            }
            if (next != infected) dfs(next, remaining - 1);
        }
    };
    vector<bool> initial(n, false);
    initial[infection - 1] = true;
    dfs(initial, k);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, int infection, vector<vector<int>> edges, int k) {  // 파이프 종류를 최대 k번 골라 감염 수 최대화
// vector<vector<vector<int>>> graph(3, vector<vector<int>>(n));  // 종류별 무방향 인접 리스트 만들기
// for (const auto& edge : edges) {  // 각 파이프를 종류별 그래프에 등록
// int a = edge[0] - 1, b = edge[1] - 1, type = edge[2] - 1;  // 번호를 0부터 시작하는 인덱스로 바꾸기
// graph[type][a].push_back(b);  // 정방향 이웃 등록
// graph[type][b].push_back(a);  // 역방향 이웃도 등록
// }  // 블록 끝
// vector<vector<vector<int>>> groups(3);  // 종류별 연결 요소의 정점 목록 저장
// for (int type = 0; type < 3; ++type) {  // 세 파이프 종류를 각각 처리
// vector<bool> visited(n, false);  // 현재 종류의 방문 표시 초기화
// for (int start = 0; start < n; ++start) {  // 아직 분류하지 않은 정점에서 탐색을 시작
// if (visited[start]) continue;  // 이미 연결 요소에 포함한 정점은 건너뛰기
// vector<int> component, stack{start};  // 연결 요소와 깊이 우선 탐색 스택 만들기
// visited[start] = true;  // 시작 정점을 방문 처리
// while (!stack.empty()) {  // 연결된 모든 정점 찾기
// int node = stack.back(); stack.pop_back();  // 스택 끝에서 다음 정점 꺼내기
// component.push_back(node);  // 현재 연결 요소에 정점 넣기
// for (int next : graph[type][node]) if (!visited[next]) {  // 방문하지 않은 같은 종류의 이웃 찾기
// visited[next] = true;  // 중복 삽입을 막기 위해 즉시 방문 표시
// stack.push_back(next);  // 이웃을 탐색 스택에 넣기
// }  // 블록 끝
// }  // 블록 끝
// groups[type].push_back(component);  // 완성한 연결 요소 저장
// }  // 블록 끝
// }  // 블록 끝
// int answer = 1;  // 처음 감염된 정점 한 개로 최댓값 초기화
// function<void(vector<bool>, int)> dfs = [&](vector<bool> infected, int remaining) {  // 감염 상태와 남은 횟수로 종류 선택 탐색
// int count = (int)std::count(infected.begin(), infected.end(), true);  // 현재 감염 정점 수 세기
// answer = max(answer, count);  // 감염 수의 최댓값 갱신
// if (remaining == 0 || answer == n) return;  // 횟수가 없거나 모두 감염되면 종료
// for (const auto& components : groups) {  // 다음으로 사용할 파이프 종류 선택
// vector<bool> next = infected;  // 현재 감염 상태를 복사
// for (const auto& component : components) {  // 선택한 종류의 연결 요소 처리
// bool touched = false;  // 현재 감염된 정점이 포함되는지 표시
// for (int node : component) touched = touched || infected[node];  // 기존 감염 상태와 연결 요소의 교집합 검사
// if (touched) for (int node : component) next[node] = true;  // 닿은 연결 요소 전체를 감염시키기
// }  // 블록 끝
// if (next != infected) dfs(next, remaining - 1);  // 감염이 늘어나는 선택만 이어 탐색
// }  // 블록 끝
// };  // 블록 끝
// vector<bool> initial(n, false);  // 초기 감염 상태 만들기
// initial[infection - 1] = true;  // 지정된 시작 정점만 감염시키기
// dfs(initial, k);  // 최대 k번의 종류 선택 탐색
// return answer;  // 가능한 최대 감염 수 반환
// }  // 블록 끝

// 풀이 요약
// 파이프 종류별 연결 요소를 미리 구하고, 감염된 정점에 닿는 연결 요소 전체를 감염시키는 선택을 최대 k번 탐색
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:24:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/003_468373_%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4_%ED%8C%8C%EC%9D%B4%ED%94%84/README.md)
