# 방의 개수 — C++

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/49190?language=cpp)

레벨 5 · C++

## 풀이 요약

한 방향 이동을 두 단계로 나누면 대각선끼리 만나는 중간 교점도 정수 좌표가 됨.

각 점에 이미 그은 8방향을 비트로 저장하고, 출발 방향과 도착점의 반대 방향을 함께 표시해 왕복 중복 제거.

처음 긋는 간선으로 이미 방문한 점에 도착할 때 방 하나 추가. 새 점으로 뻗거나 기존 간선을 되짚을 때는 그대로.

이동 N개에서 방문점은 최대 2N+1개. 해시 조회의 평균 비용 기준 시간 O(N), 공간 O(N).

## 코드와 줄별 설명

[제출 코드](solution.cpp) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~cpp
#include <cstdint>
#include <unordered_map>
#include <vector>

using namespace std;

static uint64_t point_key(int x, int y) {
    return (uint64_t(static_cast<uint32_t>(x)) << 32) | static_cast<uint32_t>(y);
}

int solution(vector<int> arrows) {
    const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1};
    const int dy[8] = {1, 1, 0, -1, -1, -1, 0, 1};
    unordered_map<uint64_t, unsigned int> directions;
    directions.reserve(arrows.size() * 2 + 1);
    int x = 0, y = 0, rooms = 0;
    directions.emplace(point_key(x, y), 0);
    for (int direction : arrows) {
        unsigned int edge = 1u << direction;
        unsigned int reverse = 1u << ((direction + 4) % 8);
        for (int half = 0; half < 2; ++half) {
            int nx = x + dx[direction], ny = y + dy[direction];
            auto next = directions.emplace(point_key(nx, ny), 0);
            auto current = directions.find(point_key(x, y));
            if (!(current->second & edge)) {
                if (!next.second) ++rooms;
                current->second |= edge;
                next.first->second |= reverse;
            }
            x = nx;
            y = ny;
        }
    }
    return rooms;
}

// 전체 코드 줄별 설명
// #include <cstdint>  // 두 정수 좌표를 하나로 묶을 uint32_t·uint64_t
// #include <unordered_map>  // 방문한 좌표와 그 점에서 그은 방향 비트를 해시로 저장
// #include <vector>  // 입력 방향 배열을 받을 vector
//
// using namespace std;  // 표준 라이브러리 이름 앞의 std:: 생략
//
// static uint64_t point_key(int x, int y) {  // 두 좌표가 서로 다른 점이면 키도 다르게 만드는 함수
//     return (uint64_t(static_cast<uint32_t>(x)) << 32) | static_cast<uint32_t>(y);  // 음수의 비트도 보존하고 x·y를 각각 32비트씩 이어 붙이기
// }  // 좌표 키 만들기 끝
//
// int solution(vector<int> arrows) {  // 입력 방향들을 따라 그렸을 때 생기는 방 수를 반환
//     const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1};  // 위쪽부터 시계 방향으로 각 방향의 가로 이동량
//     const int dy[8] = {1, 1, 0, -1, -1, -1, 0, 1};  // 같은 방향 번호에 대응하는 세로 이동량
//     unordered_map<uint64_t, unsigned int> directions;  // 좌표 키마다 이미 그은 8방향을 비트로 기록
//     directions.reserve(arrows.size() * 2 + 1);  // 최대 2N+1개 방문점을 미리 확보해 반복 재해시를 줄이기
//     int x = 0, y = 0, rooms = 0;  // 현재 좌표는 원점, 새로 닫힌 영역 수는 0
//     directions.emplace(point_key(x, y), 0);  // 시작점은 방문했지만 아직 나가는 간선은 없음
//     for (int direction : arrows) {  // 범위 for문으로 방향을 입력 순서대로 따라가기
//         unsigned int edge = 1u << direction;  // 출발점에서 이번 방향으로 나가는 간선에 대응하는 비트
//         unsigned int reverse = 1u << ((direction + 4) % 8);  // 도착점의 반대 방향 비트도 켜 왕복을 한 간선으로 취급
//         for (int half = 0; half < 2; ++half) {  // 이동을 두 조각으로 나눠 대각선 중간 교점도 방문점으로 처리
//             int nx = x + dx[direction], ny = y + dy[direction];  // 작은 한 걸음 뒤의 좌표
//             auto next = directions.emplace(point_key(nx, ny), 0);  // 도착점을 삽입하고 iterator와 신규 삽입 여부를 함께 받기
//             auto current = directions.find(point_key(x, y));  // emplace가 재해시했을 수 있으니 삽입 뒤에 현재 점 iterator 조회
//             if (!(current->second & edge)) {  // 이 간선을 처음 그릴 때만 방 생성 여부 확인
//                 if (!next.second) ++rooms;  // 삽입되지 않았다면 기존 점이므로 새 간선이 방 하나를 닫음
//                 current->second |= edge;  // 출발점의 이번 방향을 이미 그은 간선으로 표시
//                 next.first->second |= reverse;  // 도착점의 반대 방향에도 같은 간선 표시
//             }  // 새 간선 처리 끝
//             x = nx;  // 가로 좌표를 도착점으로 갱신
//             y = ny;  // 세로 좌표도 도착점으로 갱신
//         }  // 원래 한 이동을 두 단계로 처리한 반복 끝
//     }  // 입력 방향 처리 끝
//     return rooms;  // 새 간선으로 닫은 방 수 반환
// }  // 지역 해시 컨테이너는 함수가 끝나면 자동으로 해제

// 풀이 요약
// 한 방향 이동을 두 단계로 나누면 대각선끼리 만나는 중간 교점도 정수 좌표가 됨.
// 각 점에 이미 그은 8방향을 비트로 저장하고, 출발 방향과 도착점의 반대 방향을 함께 표시해 왕복 중복 제거.
// 처음 긋는 간선으로 이미 방문한 점에 도착할 때 방 하나 추가. 새 점으로 뻗거나 기존 간선을 되짚을 때는 그대로.
// 이동 N개에서 방문점은 최대 2N+1개. 해시 조회의 평균 비용 기준 시간 O(N), 공간 O(N).
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C++ 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
