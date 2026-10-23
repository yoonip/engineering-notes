# 홀짝트리

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/388354) · Level 3 · C++

## 풀이

연결 트리별로 정점 번호와 무방향 차수의 홀짝 일치 개수를 세어 루트가 될 수 있는 정점의 조건 확인

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <numeric>
#include <unordered_map>
#include <vector>
using namespace std;

vector<int> solution(vector<int> nodes, vector<vector<int>> edges) {
    int n = (int)nodes.size(); unordered_map<int, int> index;
    for (int i = 0; i < n; ++i) index[nodes[i]] = i;
    vector<int> parent(n), sizes(n, 1), degrees(n, 0); iota(parent.begin(), parent.end(), 0);
    auto find = [&](int node) {
        while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; }
        return node;
    };
    for (const auto& edge : edges) {
        int a = index[edge[0]], b = index[edge[1]]; ++degrees[a]; ++degrees[b];
        int first = find(a), second = find(b);
        if (first != second) { if (sizes[first] < sizes[second]) swap(first, second); parent[second] = first; sizes[first] += sizes[second]; }
    }
    vector<int> matches(n, 0), answer(2, 0);
    for (int i = 0; i < n; ++i) if (nodes[i] % 2 == degrees[i] % 2) ++matches[find(i)];
    for (int root = 0; root < n; ++root) if (parent[root] == root) {
        answer[0] += matches[root] == 1;
        answer[1] += matches[root] == sizes[root] - 1;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<int> nodes, vector<vector<int>> edges) {  // 트리마다 홀짝 조건을 만족하는 루트 개수 판정
// int n = (int)nodes.size(); unordered_map<int, int> index;  // 실제 정점 번호를 압축 인덱스와 연결
// for (int i = 0; i < n; ++i) index[nodes[i]] = i;  // 각 정점의 배열 위치 등록
// vector<int> parent(n), sizes(n, 1), degrees(n, 0); iota(parent.begin(), parent.end(), 0);  // 서로소 집합과 정점별 차수 초기화
// auto find = [&](int node) {  // 현재 정점의 연결 트리 대표 구하기
// while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; }  // 경로를 압축하며 대표로 이동
// return node;  // 대표 인덱스 반환
// };  // 블록 끝
// for (const auto& edge : edges) {  // 숲의 간선을 하나씩 등록
// int a = index[edge[0]], b = index[edge[1]]; ++degrees[a]; ++degrees[b];  // 양 끝 정점의 차수 늘리기
// int first = find(a), second = find(b);  // 두 정점이 속한 트리의 대표 구하기
// if (first != second) { if (sizes[first] < sizes[second]) swap(first, second); parent[second] = first; sizes[first] += sizes[second]; }  // 두 연결 요소를 크기 기준으로 합치기
// }  // 블록 끝
// vector<int> matches(n, 0), answer(2, 0);  // 트리별 홀짝 일치 정점 수와 두 종류 트리 수 저장
// for (int i = 0; i < n; ++i) if (nodes[i] % 2 == degrees[i] % 2) ++matches[find(i)];  // 번호와 무방향 차수의 홀짝이 같은 정점 세기
// for (int root = 0; root < n; ++root) if (parent[root] == root) {  // 각 연결 트리의 대표만 처리
// answer[0] += matches[root] == 1;  // 일치 정점이 하나이면 그 정점을 루트로 한 홀짝트리가 가능
// answer[1] += matches[root] == sizes[root] - 1;  // 불일치 정점이 하나이면 역홀짝트리가 가능
// }  // 블록 끝
// return answer;  // 홀짝트리와 역홀짝트리의 개수 반환
// }  // 블록 끝

// 풀이 요약
// 연결 트리별로 정점 번호와 무방향 차수의 홀짝 일치 개수를 세어 루트가 될 수 있는 정점의 조건 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:24
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/009_388354_%ED%99%80%EC%A7%9D%ED%8A%B8%EB%A6%AC/README.md)
