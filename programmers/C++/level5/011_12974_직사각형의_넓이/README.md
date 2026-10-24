# 직사각형의 넓이 — C++

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/12974?language=cpp)

레벨 5 · C++

## 풀이 요약

직사각형의 왼쪽·오른쪽 변을 x순으로 훑고, 각 변 사이에서는 덮인 y 길이가 일정하다는 점을 사용.

y 좌표를 압축한 세그먼트 트리에서 겹침 횟수와 덮인 길이를 관리해 중복 면적을 한 번만 합산.

같은 x의 이벤트 사이 폭은 0이라 추가·제거 순서가 넓이에 영향을 주지 않음.

직사각형 N개에서 정렬과 구간 갱신에 O(N log N), 좌표·이벤트·트리에 O(N) 공간. 넓이는 long long으로 계산.

## 코드와 줄별 설명

[제출 코드](solution.cpp) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~cpp
#include <algorithm>
#include <array>
#include <vector>
using namespace std;

class CoverTree {
    vector<int> count;
    vector<long long> length;
    const vector<int>& y;
public:
    CoverTree(const vector<int>& coordinates)
        : count(coordinates.size() * 4), length(coordinates.size() * 4), y(coordinates) {}
    void add(int node, int left, int right, int first, int last, int change) {
        if (first <= left && right <= last) count[node] += change;
        else {
            int middle = (left + right) / 2;
            if (first <= middle) add(node * 2, left, middle, first, last, change);
            if (last > middle) add(node * 2 + 1, middle + 1, right, first, last, change);
        }
        if (count[node] > 0) length[node] = static_cast<long long>(y[right + 1]) - y[left];
        else if (left == right) length[node] = 0;
        else length[node] = length[node * 2] + length[node * 2 + 1];
    }
    long long covered() const { return length[1]; }
};

long long solution(vector<vector<int>> rectangles) {
    vector<array<int, 4>> events;
    vector<int> y;
    for (const auto& rectangle : rectangles) {
        events.push_back({rectangle[0], rectangle[1], rectangle[3], 1});
        events.push_back({rectangle[2], rectangle[1], rectangle[3], -1});
        y.push_back(rectangle[1]);
        y.push_back(rectangle[3]);
    }
    sort(y.begin(), y.end());
    y.erase(unique(y.begin(), y.end()), y.end());
    sort(events.begin(), events.end());
    CoverTree tree(y);
    long long area = 0;
    int previous_x = events.front()[0];
    int segments = static_cast<int>(y.size()) - 1;
    for (const auto& event : events) {
        area += tree.covered() * (event[0] - previous_x);
        int first = static_cast<int>(lower_bound(y.begin(), y.end(), event[1]) - y.begin());
        int last = static_cast<int>(lower_bound(y.begin(), y.end(), event[2]) - y.begin()) - 1;
        tree.add(1, 0, segments - 1, first, last, event[3]);
        previous_x = event[0];
    }
    return area;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·중복 제거·lower_bound 좌표 검색
// #include <array>  // 이벤트 네 값을 묶을 고정 길이 배열
// #include <vector>  // 좌표·이벤트·세그먼트 트리 저장
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// class CoverTree {  // 현재 세로선에서 덮인 y 구간의 길이를 관리할 트리
//     vector<int> count;  // 각 구간 전체를 덮는 직사각형의 겹침 횟수
//     vector<long long> length;  // 각 구간에서 실제로 덮인 y 길이
//     const vector<int>& y;  // 압축 인덱스에 대응하는 원래 y 좌표를 참조
// public:  // 생성자와 갱신 함수를 바깥에서 호출할 수 있게 공개
//     CoverTree(const vector<int>& coordinates)  // 정렬된 y 좌표를 받아 빈 트리 생성
//         : count(coordinates.size() * 4), length(coordinates.size() * 4), y(coordinates) {}  // 노드 배열을 0으로 초기화하고 원래 좌표 배열 연결
//     void add(int node, int left, int right, int first, int last, int change) {  // 추가·제거할 압축 y 구간을 현재 노드 범위에 반영
//         if (first <= left && right <= last) count[node] += change;  // 현재 노드 전체가 포함되면 겹침 횟수만 증감
//         else {  // 일부만 겹치는 범위는 필요한 자식으로 내려가기
//             int middle = (left + right) / 2;  // 압축 구간을 좌우로 나눌 중간 인덱스
//             if (first <= middle) add(node * 2, left, middle, first, last, change);  // 추가 범위가 왼쪽 자식과 만나면 왼쪽 갱신
//             if (last > middle) add(node * 2 + 1, middle + 1, right, first, last, change);  // 오른쪽과 만나는 부분도 갱신
//         }  // 자식 갱신 끝
//         if (count[node] > 0) length[node] = static_cast<long long>(y[right + 1]) - y[left];  // 구간 전체를 덮는 사각형이 있으면 원래 좌표의 전체 길이 사용
//         else if (left == right) length[node] = 0;  // 아무 사각형도 덮지 않는 최소 구간은 길이 0
//         else length[node] = length[node * 2] + length[node * 2 + 1];  // 전체 덮개가 없으면 자식에서 덮인 길이를 합치기
//     }  // 구간 갱신 끝
//     long long covered() const { return length[1]; }  // 루트에 저장된 현재 y 합집합 길이 반환
// };  // 구간 길이 관리 클래스 끝
//
// long long solution(vector<vector<int>> rectangles) {  // 직사각형 합집합 넓이를 64비트 정수로 계산
//     vector<array<int, 4>> events;  // x 좌표·아래 y·위 y·추가량으로 스윕 이벤트 저장
//     vector<int> y;  // 세로 구간의 경계 좌표 수집
//     for (const auto& rectangle : rectangles) {  // 각 직사각형을 시작과 끝 이벤트로 나누기
//         events.push_back({rectangle[0], rectangle[1], rectangle[3], 1});  // 왼쪽 변을 만나면 해당 y 범위를 추가
//         events.push_back({rectangle[2], rectangle[1], rectangle[3], -1});  // 오른쪽 변을 지나면 같은 y 범위를 제거
//         y.push_back(rectangle[1]);  // 직사각형 아래쪽 경계 수집
//         y.push_back(rectangle[3]);  // 위쪽 경계도 수집
//     }  // 이벤트와 좌표 수집 끝
//     sort(y.begin(), y.end());  // 실제 y 좌표를 작은 순서로 정렬
//     y.erase(unique(y.begin(), y.end()), y.end());  // 같은 경계 좌표는 하나로 압축
//     sort(events.begin(), events.end());  // 왼쪽에서 오른쪽으로 처리하도록 x 우선 정렬
//     CoverTree tree(y);  // 아직 어떤 y 구간도 덮이지 않은 상태로 시작
//     long long area = 0;  // 최대 10^18인 합집합 넓이 누적
//     int previous_x = events.front()[0];  // 첫 이벤트 전에는 덮인 영역이 없으므로 첫 x에서 시작
//     int segments = static_cast<int>(y.size()) - 1;  // 인접한 y 좌표 두 개 사이가 트리의 최소 구간 하나
//     for (const auto& event : events) {  // 정렬된 변 이벤트를 하나씩 지나가기
//         area += tree.covered() * (event[0] - previous_x);  // 직전 상태의 덮인 세로 길이에 이동한 가로 폭을 곱해 넓이 추가
//         int first = static_cast<int>(lower_bound(y.begin(), y.end(), event[1]) - y.begin());  // 아래 경계의 압축 인덱스 찾기
//         int last = static_cast<int>(lower_bound(y.begin(), y.end(), event[2]) - y.begin()) - 1;  // 위 경계 바로 전까지의 최소 구간을 갱신 대상으로 선택
//         tree.add(1, 0, segments - 1, first, last, event[3]);  // 현재 변에서 직사각형 범위를 추가하거나 제거
//         previous_x = event[0];  // 다음 이벤트까지의 폭 계산 기준을 현재 x로 이동
//     }  // 모든 세로 변 처리 끝
//     return area;  // 겹친 부분을 한 번씩만 더한 넓이 반환
// }  // solution 함수 끝

// 풀이 요약
// 직사각형의 왼쪽·오른쪽 변을 x순으로 훑고, 각 변 사이에서는 덮인 y 길이가 일정하다는 점을 사용.
// y 좌표를 압축한 세그먼트 트리에서 겹침 횟수와 덮인 길이를 관리해 중복 면적을 한 번만 합산.
// 같은 x의 이벤트 사이 폭은 0이라 추가·제거 순서가 넓이에 영향을 주지 않음.
// 직사각형 N개에서 정렬과 구간 갱신에 O(N log N), 좌표·이벤트·트리에 O(N) 공간. 넓이는 long long으로 계산.
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C++ 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
