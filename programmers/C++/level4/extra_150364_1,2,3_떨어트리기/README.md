# 1,2,3 떨어트리기

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150364) · Level 4 · C++

## 풀이

공이 떨어지는 리프 순서를 먼저 시뮬레이션. 각 리프가 count ≤ target ≤ 3 × count를 만족할 때 멈추고, 뒤에서 만들 수 있는 최대 합을 남기며 앞에서 작은 숫자부터 배정.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <tuple>
#include <utility>
#include <climits>
#include <cstdlib>
using namespace std;

vector<int> solution(vector<vector<int>> edges, vector<int> target) {
    int n = (int)target.size(); vector<vector<int>> children(n);
    for (const auto& edge : edges) children[edge[0] - 1].push_back(edge[1] - 1);
    for (auto& branch : children) sort(branch.begin(), branch.end());
    vector<int> pointers(n, 0), counts(n, 0), order;
    int unmet = count_if(target.begin(), target.end(), [](int value) { return value > 0; });
    while (unmet) {
        int node = 0;
        while (!children[node].empty()) { int index = pointers[node]; pointers[node] = (index + 1) % children[node].size(); node = children[node][index]; }
        ++counts[node]; order.push_back(node);
        if (counts[node] > target[node]) return {-1};
        if (3 * (counts[node] - 1) < target[node] && target[node] <= 3 * counts[node]) --unmet;
    }
    vector<int> answer;
    for (int node : order) { --counts[node]; int value = max(1, target[node] - 3 * counts[node]); answer.push_back(value); target[node] -= value; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <array>  // 고정 크기 배열 array 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <map>  // 키 순서가 유지되는 맵 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <deque>  // 양 끝 삽입·삭제를 지원하는 덱 사용 준비
// #include <tuple>  // 여러 상태 값을 묶는 tuple 사용 준비
// #include <utility>  // pair·move 등 유틸리티 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// vector<int> solution(vector<vector<int>> edges, vector<int> target) {  // 1,2,3 떨어트리기 풀이 함수 정의
//     int n = (int)target.size(); vector<vector<int>> children(n);  // 노드 수와 노드별 자식 목록 준비
//     for (const auto& edge : edges) children[edge[0] - 1].push_back(edge[1] - 1);  // 1기준 간선을 0기준 자식 목록으로 변환
//     for (auto& branch : children) sort(branch.begin(), branch.end());  // 작은 번호 자식부터 길을 바꾸도록 자식 목록 정렬
//     vector<int> pointers(n, 0), counts(n, 0), order;  // 각 노드의 다음 자식 포인터, 리프별 낙하 횟수, 전체 낙하 순서 준비
//     int unmet = count_if(target.begin(), target.end(), [](int value) { return value > 0; });  // 목표가 양수여서 아직 필요한 낙하 횟수가 부족한 리프 수 집계
//     while (unmet) {  // 모든 리프에 충분한 횟수가 쌓일 때까지 공을 떨어뜨림
//         int node = 0;  // 이번 공을 루트 0에서 시작
//         while (!children[node].empty()) { int index = pointers[node]; pointers[node] = (index + 1) % children[node].size(); node = children[node][index]; }  // 현재 자식 포인터를 따라 내려가고 사용한 노드의 포인터를 다음 자식으로 순환 갱신
//         ++counts[node]; order.push_back(node);  // 도착한 리프의 낙하 횟수를 늘리고 방문 순서에 기록
//         if (counts[node] > target[node]) return {-1};  // 모두 1을 넣어도 목표를 초과하면 불가능하므로 {-1} 반환
//         if (3 * (counts[node] - 1) < target[node] && target[node] <= 3 * counts[node]) --unmet;  // 이번 낙하로 목표를 최대값 3의 합으로 채울 수 있게 됐다면 미충족 리프 수 감소
//     }  // 블록 끝
//     vector<int> answer;  // 낙하 순서에 맞춰 숫자를 담을 결과 배열 준비
//     for (int node : order) { --counts[node]; int value = max(1, target[node] - 3 * counts[node]); answer.push_back(value); target[node] -= value; }  // 남은 낙하에 최대 3씩 배정할 수 있도록 현재 값을 최대한 작게 선택하고 목표 잔여량 차감
//     return answer;  // 사전순으로 가장 작은 숫자 배열 반환
// }  // 함수 끝
//

// 풀이 요약
// 공이 떨어지는 리프 순서를 먼저 시뮬레이션. 각 리프가 count ≤ target ≤ 3 × count를 만족할 때 멈추고, 뒤에서 만들 수 있는 최대 합을 남기며 앞에서 작은 숫자부터 배정.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_150364_1%2C2%2C3_%EB%96%A8%EC%96%B4%ED%8A%B8%EB%A6%AC%EA%B8%B0/README.md)
