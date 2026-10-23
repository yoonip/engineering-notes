#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int cards[], size_t cards_len) {
    bool* visited = calloc(cards_len, sizeof(*visited)); int first = 0, second = 0;
    for (size_t start = 0; start < cards_len; ++start) {
        int node = (int)start, count = 0;
        while (!visited[node]) { visited[node] = true; ++count; node = cards[node] - 1; }
        if (count >= first) { second = first; first = count; }
        else if (count > second) second = count;
    }
    free(visited);
    return first * second;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// int solution(int cards[], size_t cards_len) {  // 카드가 중복 없는 순열이므로 연결을 따라가면 서로 겹치지 않는 사이클 그룹이 됨; 가장 큰 두 그룹을 선택
//     bool* visited = calloc(cards_len, sizeof(*visited)); int first = 0, second = 0;  // 이미 연 상자 표시 / 가장 큰 상자 그룹 크기 / 두 번째로 큰 그룹 크기 공간 확보하고 0으로 시작
//     for (size_t start = 0; start < cards_len; ++start) {  // 새 그룹을 시작할 상자 순서대로 확인
//         int node = (int)start, count = 0;  // 현재 열 상자 / 이번 그룹에서 연 상자 수 저장
//         while (!visited[node]) { visited[node] = true; ++count; node = cards[node] - 1; }  // 이미 연 상자에 닿을 때까지 방문 표시하고 카드가 가리키는 상자로 이동
//         if (count >= first) { second = first; first = count; }  // 현재 그룹이 가장 크면 기존 1위를 2위로 밀고 새 1위 기록
//         else if (count > second) second = count;  // 현재 그룹이 1위보다 작아도 2위보다 크면 2위 교체
//     }  // 이 범위 끝
//     free(visited);  // 이미 연 상자 표시 임시 공간 정리
//     return first * second;  // 가장 큰 상자 그룹 크기 / 두 번째로 큰 그룹 크기로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 카드가 중복 없는 순열이므로 연결을 따라가면 서로 겹치지 않는 사이클 그룹이 됨; 가장 큰 두 그룹을 선택
// 예: 그룹 크기 4,3,1이면 4×3=12.; 시간 O(N log N), 공간 O(N)
