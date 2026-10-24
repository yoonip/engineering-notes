# 방의 개수 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/49190?language=c)

레벨 5 · C

## 풀이 요약

한 방향 이동을 두 단계로 나누면 대각선끼리 만나는 중간 교점도 정수 좌표가 됨.

각 점에 이미 그은 8방향을 비트로 저장하고, 출발 방향과 도착점의 반대 방향을 함께 표시해 왕복 중복 제거.

처음 긋는 간선으로 이미 방문한 점에 도착할 때 방 하나 추가. 새 점으로 뻗거나 기존 간선을 되짚을 때는 그대로.

이동 N개에서 방문점은 최대 2N+1개. 해시 조회의 평균 비용 기준 시간 O(N), 공간 O(N).

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct {
    int x, y;
    unsigned char directions;
    unsigned char present;
} Vertex;

static uint64_t point_hash(int x, int y) {
    uint64_t key = ((uint64_t)(uint32_t)x << 32) | (uint32_t)y;
    key ^= key >> 30;
    key *= UINT64_C(0xbf58476d1ce4e5b9);
    key ^= key >> 27;
    key *= UINT64_C(0x94d049bb133111eb);
    return key ^ (key >> 31);
}

static size_t vertex_slot(Vertex *vertices, size_t mask, int x, int y) {
    size_t slot = (size_t)point_hash(x, y) & mask;
    while (vertices[slot].present && (vertices[slot].x != x || vertices[slot].y != y)) {
        slot = (slot + 1) & mask;
    }
    return slot;
}

int solution(int arrows[], size_t arrows_len) {
    const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1};
    const int dy[8] = {1, 1, 0, -1, -1, -1, 0, 1};
    size_t capacity = 8;
    while (capacity < arrows_len * 4 + 4) capacity *= 2;
    Vertex *vertices = calloc(capacity, sizeof(*vertices));
    size_t mask = capacity - 1;
    int x = 0, y = 0, rooms = 0;
    size_t current = vertex_slot(vertices, mask, x, y);
    vertices[current].present = 1;
    for (size_t i = 0; i < arrows_len; ++i) {
        int direction = arrows[i];
        unsigned int edge = 1u << direction;
        unsigned int reverse = 1u << ((direction + 4) % 8);
        for (int half = 0; half < 2; ++half) {
            int nx = x + dx[direction], ny = y + dy[direction];
            size_t next = vertex_slot(vertices, mask, nx, ny);
            int visited = vertices[next].present;
            if (!visited) {
                vertices[next].x = nx;
                vertices[next].y = ny;
                vertices[next].present = 1;
            }
            if (!(vertices[current].directions & edge)) {
                if (visited) ++rooms;
                vertices[current].directions |= edge;
                vertices[next].directions |= reverse;
            }
            x = nx;
            y = ny;
            current = next;
        }
    }
    free(vertices);
    return rooms;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 배열 길이와 해시 칸 번호에 쓸 size_t
// #include <stdint.h>  // 좌표 두 개를 담고 섞을 64비트 부호 없는 정수
// #include <stdlib.h>  // 해시 배열을 0으로 할당하고 마지막에 해제
//
// typedef struct {  // 한 좌표의 방문 여부와 연결 방향을 묶을 구조체
//     int x, y;  // 두 배로 확대한 격자에서 이 점의 좌표
//     unsigned char directions;  // 0~7번 방향에 이미 그은 간선이 있으면 해당 비트를 1로 표시
//     unsigned char present;  // 좌표가 (0,0)일 수도 있으니 빈 칸 여부는 별도 표시
// } Vertex;  // 구조체 이름을 Vertex로 줄여 사용
//
// static uint64_t point_hash(int x, int y) {  // 음수도 구분되는 좌표 키를 만들어 해시 칸을 고르게 선택
//     uint64_t key = ((uint64_t)(uint32_t)x << 32) | (uint32_t)y;  // 각 좌표의 32비트를 위아래로 이어 붙여 서로 다른 점을 구분
//     key ^= key >> 30;  // 상위 비트도 하위 비트에 섞어 규칙적인 격자 좌표를 분산
//     key *= UINT64_C(0xbf58476d1ce4e5b9);  // 64비트 곱셈으로 인접 좌표의 해시 패턴을 흩뜨리기
//     key ^= key >> 27;  // 곱셈 결과를 다시 비트 단위로 혼합
//     key *= UINT64_C(0x94d049bb133111eb);  // 좌표가 한 방향으로 길게 늘어나도 해시가 몰리지 않게 한 번 더 혼합
//     return key ^ (key >> 31);  // 마지막 비트 혼합 결과를 해시값으로 반환
// }  // 좌표 해시 함수 끝
//
// static size_t vertex_slot(Vertex *vertices, size_t mask, int x, int y) {  // 해시 배열에서 이 좌표가 있거나 새로 들어갈 칸을 찾기
//     size_t slot = (size_t)point_hash(x, y) & mask;  // 크기가 2의 거듭제곱이므로 비트 AND로 배열 범위에 맞추기
//     while (vertices[slot].present && (vertices[slot].x != x || vertices[slot].y != y)) {  // 사용 중인 칸의 좌표가 다르면 해시 충돌이므로 다음 칸 확인
//         slot = (slot + 1) & mask;  // 끝에 도달하면 첫 칸으로 돌아가는 선형 탐사
//     }  // 같은 좌표 또는 빈 칸을 찾으면 탐사 종료
//     return slot;  // 찾은 칸 번호를 호출한 쪽에서 조회·삽입에 사용
// }  // 해시 칸 찾기 끝
//
// int solution(int arrows[], size_t arrows_len) {  // 방향 배열과 길이를 받아 닫힌 방 수를 반환
//     const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1};  // 위쪽부터 시계 방향으로 각 방향의 가로 이동량
//     const int dy[8] = {1, 1, 0, -1, -1, -1, 0, 1};  // 같은 방향 번호에 대응하는 세로 이동량
//     size_t capacity = 8;  // 선형 탐사에 사용할 해시 크기를 작은 2의 거듭제곱에서 시작
//     while (capacity < arrows_len * 4 + 4) capacity *= 2;  // 최대 2N+1개 점이 들어가므로 절반 이상은 빈 칸으로 확보
//     Vertex *vertices = calloc(capacity, sizeof(*vertices));  // 좌표와 방문·방향 비트를 모두 0으로 초기화한 해시 배열
//     size_t mask = capacity - 1;  // 해시 칸 번호를 0~capacity-1로 감쌀 비트 마스크
//     int x = 0, y = 0, rooms = 0;  // 원점에서 출발하고 새로 닫힌 영역을 rooms에 누적
//     size_t current = vertex_slot(vertices, mask, x, y);  // 현재 좌표인 원점의 해시 칸을 기억
//     vertices[current].present = 1;  // 시작점도 이미 방문한 점으로 등록
//     for (size_t i = 0; i < arrows_len; ++i) {  // 입력에 적힌 방향을 순서대로 따라가기
//         int direction = arrows[i];  // 이번 이동의 방향 번호를 다음 두 단계에서 함께 사용
//         unsigned int edge = 1u << direction;  // 현재 점에서 나가는 방향에 대응하는 한 비트
//         unsigned int reverse = 1u << ((direction + 4) % 8);  // 도착점에서 되돌아오는 반대 방향도 같은 간선으로 표시
//         for (int half = 0; half < 2; ++half) {  // 한 이동을 두 조각으로 나눠 대각선 교점도 정수 좌표로 방문
//             int nx = x + dx[direction], ny = y + dy[direction];  // 작은 한 걸음 뒤의 좌표
//             size_t next = vertex_slot(vertices, mask, nx, ny);  // 도착 좌표가 저장될 해시 칸 조회
//             int visited = vertices[next].present;  // 이번 간선을 긋기 전에 이미 도착점을 방문했는지 보관
//             if (!visited) {  // 처음 도착한 점이면 좌표와 방문 표시를 새로 등록
//                 vertices[next].x = nx;  // 새 점의 가로 좌표 저장
//                 vertices[next].y = ny;  // 새 점의 세로 좌표 저장
//                 vertices[next].present = 1;  // 이 칸을 빈 칸이 아닌 방문 좌표로 표시
//             }  // 도착점 등록 끝
//             if (!(vertices[current].directions & edge)) {  // 이미 그은 간선을 되짚을 때는 방 수를 늘리지 않기
//                 if (visited) ++rooms;  // 새 간선으로 기존 점에 닿으면 연결된 그림 안에 방 하나가 생김
//                 vertices[current].directions |= edge;  // 출발점에서 이 방향으로 간선을 그었다고 기록
//                 vertices[next].directions |= reverse;  // 도착점의 반대 방향도 표시해 왕복을 한 간선으로 취급
//             }  // 새 간선 처리 끝
//             x = nx;  // 다음 작은 걸음은 도착한 가로 좌표에서 시작
//             y = ny;  // 세로 좌표도 도착점으로 갱신
//             current = next;  // 현재 좌표의 해시 칸도 도착점 칸으로 교체
//         }  // 원래 한 이동에 필요한 두 단계 처리 끝
//     }  // 전체 방향 처리 끝
//     free(vertices);  // 채점 함수가 반복 호출돼도 메모리가 남지 않게 해시 배열 해제
//     return rooms;  // 새 간선으로 닫은 방의 총수 반환
// }  // solution 함수 끝

// 풀이 요약
// 한 방향 이동을 두 단계로 나누면 대각선끼리 만나는 중간 교점도 정수 좌표가 됨.
// 각 점에 이미 그은 8방향을 비트로 저장하고, 출발 방향과 도착점의 반대 방향을 함께 표시해 왕복 중복 제거.
// 처음 긋는 간선으로 이미 방문한 점에 도착할 때 방 하나 추가. 새 점으로 뻗거나 기존 간선을 되짚을 때는 그대로.
// 이동 N개에서 방문점은 최대 2N+1개. 해시 조회의 평균 비용 기준 시간 O(N), 공간 O(N).
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
