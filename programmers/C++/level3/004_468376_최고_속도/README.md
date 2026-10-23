# 최고 속도

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468376) · Level 3 · C++

## 풀이

도로를 카메라 위치에서 나누고 카메라 없는 교차 구간을 서로소 집합으로 합친 뒤 경로의 최소 제한 속도를 최대화하는 탐색

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <map>
#include <numeric>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(vector<vector<int>> city, vector<vector<int>> road) {
    map<pair<int, int>, int> cameras;
    for (const auto& r : road) {
        pair<int, int> point{int((1LL * r[0] + r[2]) / 2), int((1LL * r[1] + r[3]) / 2)};
        auto found = cameras.find(point);
        if (found == cameras.end()) cameras[point] = r[4];
        else found->second = min(found->second, r[4]);
    }
    vector<pair<int, int>> camera_points;
    for (const auto& entry : cameras) camera_points.push_back(entry.first);
    vector<vector<long long>> cuts; vector<int> bases, parent; vector<pair<int, int>> links;
    for (const auto& r : road) {
        vector<pair<long long, int>> positions;
        vector<long long> boundaries{1LL * r[0] + r[1], 1LL * r[2] + r[3]};
        for (int i = 0; i < (int)camera_points.size(); ++i) {
            auto [x, y] = camera_points[i];
            if (r[0] <= x && x <= r[2] && r[1] <= y && y <= r[3]) { positions.push_back({1LL * x + y, i}); boundaries.push_back(1LL * x + y); }
        }
        sort(boundaries.begin(), boundaries.end()); boundaries.erase(unique(boundaries.begin(), boundaries.end()), boundaries.end());
        int base = (int)parent.size(); bases.push_back(base);
        for (int i = 0; i + 1 < (int)boundaries.size(); ++i) parent.push_back((int)parent.size());
        cuts.push_back(boundaries);
        for (auto [position, camera] : positions) {
            int index = int(lower_bound(boundaries.begin(), boundaries.end(), position) - boundaries.begin());
            if (index > 0) links.push_back({base + index - 1, camera});
            if (index + 1 < (int)boundaries.size()) links.push_back({base + index, camera});
        }
    }
    vector<int> sizes(parent.size(), 1);
    auto find = [&](int node) {
        while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; }
        return node;
    };
    auto piece = [&](int index, int x, int y) {
        int offset = min(int(upper_bound(cuts[index].begin(), cuts[index].end(), 1LL * x + y) - cuts[index].begin()) - 1, int(cuts[index].size()) - 2);
        return bases[index] + offset;
    };
    for (int i = 0; i < (int)road.size(); ++i) for (int j = 0; j < i; ++j) {
        int x = max(road[i][0], road[j][0]), y = max(road[i][1], road[j][1]);
        if (x > min(road[i][2], road[j][2]) || y > min(road[i][3], road[j][3]) || cameras.count({x, y})) continue;
        int first = find(piece(i, x, y)), second = find(piece(j, x, y));
        if (first != second) { if (sizes[first] < sizes[second]) swap(first, second); parent[second] = first; sizes[first] += sizes[second]; }
    }
    int offset = (int)parent.size();
    vector<vector<pair<int, int>>> graph(offset + cameras.size());
    for (auto [node, camera] : links) {
        node = find(node); int limit = cameras[camera_points[camera]];
        graph[node].push_back({offset + camera, limit}); graph[offset + camera].push_back({node, limit});
    }
    vector<int> cities;
    for (const auto& point : city) for (int i = 0; i < (int)road.size(); ++i) {
        const auto& r = road[i];
        if (r[0] <= point[0] && point[0] <= r[2] && r[1] <= point[1] && point[1] <= r[3]) { cities.push_back(find(piece(i, point[0], point[1]))); break; }
    }
    const int INF = 1000001; vector<int> best(graph.size(), 0);
    priority_queue<pair<int, int>> heap; best[cities[0]] = INF; heap.push({INF, cities[0]});
    while (!heap.empty()) {
        auto [speed, node] = heap.top(); heap.pop();
        if (speed != best[node]) continue;
        for (auto [neighbor, limit] : graph[node]) {
            int candidate = min(speed, limit);
            if (candidate > best[neighbor]) { best[neighbor] = candidate; heap.push({candidate, neighbor}); }
        }
    }
    vector<int> answer;
    for (int i = 1; i < (int)cities.size(); ++i) answer.push_back(best[cities[i]] == INF ? 0 : best[cities[i]]);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <map>  // 키를 정렬해 보관하는 map
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<vector<int>> city, vector<vector<int>> road) {  // 경로에서 가장 낮은 제한 속도를 최대화
// map<pair<int, int>, int> cameras;  // 카메라 위치별로 가장 낮은 제한 속도 저장
// for (const auto& r : road) {  // 도로마다 중앙의 카메라 등록
// pair<int, int> point{int((1LL * r[0] + r[2]) / 2), int((1LL * r[1] + r[3]) / 2)};  // 중앙 좌표를 넓은 정수형으로 계산
// auto found = cameras.find(point);  // 같은 위치에 다른 카메라가 있는지 확인
// if (found == cameras.end()) cameras[point] = r[4];  // 처음인 위치에 제한 속도 등록
// else found->second = min(found->second, r[4]);  // 중복 위치는 더 낮은 제한 적용
// }  // 블록 끝
// vector<pair<int, int>> camera_points;  // 카메라 번호와 좌표를 대응시키기
// for (const auto& entry : cameras) camera_points.push_back(entry.first);  // 고정된 순서로 좌표를 배열에 넣기
// vector<vector<long long>> cuts; vector<int> bases, parent; vector<pair<int, int>> links;  // 도로 분할점과 구간 번호 및 카메라 연결 저장
// for (const auto& r : road) {  // 각 도로를 카메라 위치에서 나누기
// vector<pair<long long, int>> positions;  // 도로 위 카메라의 위치와 번호 저장
// vector<long long> boundaries{1LL * r[0] + r[1], 1LL * r[2] + r[3]};  // 도로 양 끝의 일차원 좌표 기록
// for (int i = 0; i < (int)camera_points.size(); ++i) {  // 모든 카메라가 현재 도로 위인지 검사
// auto [x, y] = camera_points[i];  // 카메라 좌표 읽기
// if (r[0] <= x && x <= r[2] && r[1] <= y && y <= r[3]) { positions.push_back({1LL * x + y, i}); boundaries.push_back(1LL * x + y); }  // 도로 위 카메라를 분할 경계에 추가
// }  // 블록 끝
// sort(boundaries.begin(), boundaries.end()); boundaries.erase(unique(boundaries.begin(), boundaries.end()), boundaries.end());  // 분할 좌표를 중복 없이 정렬
// int base = (int)parent.size(); bases.push_back(base);  // 현재 도로의 첫 구간 번호 기록
// for (int i = 0; i + 1 < (int)boundaries.size(); ++i) parent.push_back((int)parent.size());  // 분할된 각 구간에 서로소 집합 원소 만들기
// cuts.push_back(boundaries);  // 도로별 분할 좌표 저장
// for (auto [position, camera] : positions) {  // 카메라 양쪽 구간을 연결 후보에 넣기
// int index = int(lower_bound(boundaries.begin(), boundaries.end(), position) - boundaries.begin());  // 카메라의 경계 인덱스 찾기
// if (index > 0) links.push_back({base + index - 1, camera});  // 카메라 앞 구간과 연결
// if (index + 1 < (int)boundaries.size()) links.push_back({base + index, camera});  // 카메라 뒤 구간과 연결
// }  // 블록 끝
// }  // 블록 끝
// vector<int> sizes(parent.size(), 1);  // 서로소 집합의 구간 수 초기화
// auto find = [&](int node) {  // 카메라 없이 연결된 구간의 대표 구하기
// while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; }  // 경로 압축으로 대표까지 올라가기
// return node;  // 대표 구간 번호 반환
// };  // 블록 끝
// auto piece = [&](int index, int x, int y) {  // 도로 위 좌표가 속한 분할 구간 찾기
// int offset = min(int(upper_bound(cuts[index].begin(), cuts[index].end(), 1LL * x + y) - cuts[index].begin()) - 1, int(cuts[index].size()) - 2);  // 오른쪽 끝점은 마지막 구간에 포함
// return bases[index] + offset;  // 전체 구간 번호로 바꾸기
// };  // 블록 끝
// for (int i = 0; i < (int)road.size(); ++i) for (int j = 0; j < i; ++j) {  // 모든 도로 쌍의 교차점 검사
// int x = max(road[i][0], road[j][0]), y = max(road[i][1], road[j][1]);  // 두 도로가 만날 수 있는 좌표 구하기
// if (x > min(road[i][2], road[j][2]) || y > min(road[i][3], road[j][3]) || cameras.count({x, y})) continue;  // 만나지 않거나 카메라가 있는 교차점은 합치지 않음
// int first = find(piece(i, x, y)), second = find(piece(j, x, y));  // 두 교차 구간의 대표 구하기
// if (first != second) { if (sizes[first] < sizes[second]) swap(first, second); parent[second] = first; sizes[first] += sizes[second]; }  // 카메라 없이 이어지는 구간을 크기 기준으로 합치기
// }  // 블록 끝
// int offset = (int)parent.size();  // 구간 노드 뒤에서 카메라 노드 번호를 시작
// vector<vector<pair<int, int>>> graph(offset + cameras.size());  // 구간 대표와 카메라 사이의 제한 속도 그래프 만들기
// for (auto [node, camera] : links) {  // 카메라의 양쪽 구간 연결 등록
// node = find(node); int limit = cameras[camera_points[camera]];  // 구간 대표와 해당 제한 속도 읽기
// graph[node].push_back({offset + camera, limit}); graph[offset + camera].push_back({node, limit});  // 카메라 통과 간선을 양방향으로 두기
// }  // 블록 끝
// vector<int> cities;  // 각 도시가 속한 구간 대표 저장
// for (const auto& point : city) for (int i = 0; i < (int)road.size(); ++i) {  // 도시를 포함하는 도로 찾기
// const auto& r = road[i];  // 현재 도로의 경계 읽기
// if (r[0] <= point[0] && point[0] <= r[2] && r[1] <= point[1] && point[1] <= r[3]) { cities.push_back(find(piece(i, point[0], point[1]))); break; }  // 처음 찾은 포함 구간의 대표 기록
// }  // 블록 끝
// const int INF = 1000001; vector<int> best(graph.size(), 0);  // 무제한 속도와 정점별 최대 통과 가능 속도 초기화
// priority_queue<pair<int, int>> heap; best[cities[0]] = INF; heap.push({INF, cities[0]});  // 출발 도시에서 최대 병목 경로 탐색을 시작
// while (!heap.empty()) {  // 현재 가능한 속도가 큰 상태부터 처리
// auto [speed, node] = heap.top(); heap.pop();  // 최대 속도 후보 꺼내기
// if (speed != best[node]) continue;  // 오래된 탐색 상태는 건너뛰기
// for (auto [neighbor, limit] : graph[node]) {  // 인접 카메라 또는 구간으로 이동
// int candidate = min(speed, limit);  // 경로의 가장 낮은 제한 속도 적용
// if (candidate > best[neighbor]) { best[neighbor] = candidate; heap.push({candidate, neighbor}); }  // 더 빠른 경로이면 갱신
// }  // 블록 끝
// }  // 블록 끝
// vector<int> answer;  // 출발 도시를 제외한 도착 도시별 답 저장
// for (int i = 1; i < (int)cities.size(); ++i) answer.push_back(best[cities[i]] == INF ? 0 : best[cities[i]]);  // 카메라 없이 갈 수 있으면 0으로 표시
// return answer;  // 도시별 최고 속도 반환
// }  // 블록 끝

// 풀이 요약
// 도로를 카메라 위치에서 나누고 카메라 없는 교차 구간을 서로소 집합으로 합친 뒤 경로의 최소 제한 속도를 최대화하는 탐색
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/004_468376_%EC%B5%9C%EA%B3%A0_%EC%86%8D%EB%8F%84/README.md)
