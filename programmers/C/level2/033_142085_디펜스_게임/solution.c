#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static void push(int* heap, size_t* count, int value) {
    size_t pos = (*count)++;
    while (pos && heap[(pos - 1) / 2] > value) { heap[pos] = heap[(pos - 1) / 2]; pos = (pos - 1) / 2; }
    heap[pos] = value;
}
static int pop(int* heap, size_t* count) {
    int result = heap[0], value = heap[--*count]; size_t pos = 0;
    while (pos * 2 + 1 < *count) {
        size_t child = pos * 2 + 1;
        if (child + 1 < *count && heap[child + 1] < heap[child]) ++child;
        if (heap[child] >= value) break;
        heap[pos] = heap[child]; pos = child;
    }
    if (*count) heap[pos] = value;
    return result;
}
int solution(int n, int k, int enemy[], size_t enemy_len) {
    int* heap = malloc((enemy_len + 1) * sizeof(*heap)); size_t count = 0;
    for (size_t i = 0; i < enemy_len; ++i) {
        push(heap, &count, enemy[i]);
        if (count > (size_t)k) n -= pop(heap, &count);
        if (n < 0) { free(heap); return (int)i; }
    }
    free(heap);
    return (int)enemy_len;
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
// static void push(int* heap, size_t* count, int value) {  // 새 상태를 힙에 넣고 부모 방향으로 자리 찾기
//     size_t pos = (*count)++;  // 힙에서 값을 둘 위치 저장
//     while (pos && heap[(pos - 1) / 2] > value) { heap[pos] = heap[(pos - 1) / 2]; pos = (pos - 1) / 2; }  // 무적권으로 막아 둔 적 수의 최소 힙에 남은 경로를 비용순으로 처리
//     heap[pos] = value;  // 무적권으로 막아 둔 적 수의 최소 힙 갱신
// }  // 이 범위 끝
// static int pop(int* heap, size_t* count) {  // 힙의 첫 값을 꺼내고 마지막 값으로 빈자리 메우기
//     int result = heap[0], value = heap[--*count]; size_t pos = 0;  // 힙의 최솟값 / 자리로 내려 보낼 힙 값 / 힙에서 값을 둘 위치 저장
//     while (pos * 2 + 1 < *count) {  // 왼쪽 자식이 있는 동안 마지막 값을 내려놓을 자리 찾기
//         size_t child = pos * 2 + 1;  // 더 작은 자식 위치 저장
//         if (child + 1 < *count && heap[child + 1] < heap[child]) ++child;  // 오른쪽 자식이 더 작으면 비교할 자식을 오른쪽으로 바꾸기
//         if (heap[child] >= value) break;  // 부모와 자식의 힙 순서가 이미 맞으면 이번 후보 확인을 끝내기
//         heap[pos] = heap[child]; pos = child;  // 무적권으로 막아 둔 적 수의 최소 힙 / 힙에서 값을 둘 위치 갱신
//     }  // 이 범위 끝
//     if (*count) heap[pos] = value;  // 꺼낸 뒤 힙이 남아 있으면 찾은 자리에 마지막 값 넣기
//     return result;  // 힙의 최솟값 반환
// }  // 이 범위 끝
// int solution(int n, int k, int enemy[], size_t enemy_len) {  // 진행한 공격 중 큰 k개에 무적권을 배정하고 나머지를 병사로 막기; 최소 힙에서 가장 작은 공격을 병사 비용으로 옮기기
//     int* heap = malloc((enemy_len + 1) * sizeof(*heap)); size_t count = 0;  // 무적권으로 막아 둔 적 수의 최소 힙 / 힙에 담긴 라운드 수 공간 확보
//     for (size_t i = 0; i < enemy_len; ++i) {  // 현재 라운드 번호 순서대로 확인
//         push(heap, &count, enemy[i]);  // 다음에 확인할 경로를 힙에 추가
//         if (count > (size_t)k) n -= pop(heap, &count);  // 무적권 수보다 많은 라운드를 담았으면 가장 작은 적 수만 병사로 막기
//         if (n < 0) { free(heap); return (int)i; }  // 아직 남은 병사 수가 0보다 작으면 무적권으로 막아 둔 적 수의 최소 힙 / 현재 라운드 번호 임시 공간 정리
//     }  // 이 범위 끝
//     free(heap);  // 무적권으로 막아 둔 적 수의 최소 힙 임시 공간 정리
//     return (int)enemy_len;  // 모든 라운드를 막았으면 전체 라운드 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 진행한 공격 중 큰 k개에 무적권을 배정하고 나머지를 병사로 막기; 최소 힙에서 가장 작은 공격을 병사 비용으로 옮기기
// 예: 병사 7·무적권 3이면 예제에서 5라운드 성공.; 라운드 N개일 때 시간 O(N log(min(k,N)+1)), 공간 O(min(k,N))
