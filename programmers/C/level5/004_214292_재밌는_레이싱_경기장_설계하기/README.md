# 재밌는 레이싱 경기장 설계하기 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/214292?language=c)

레벨 5 · C

## 풀이 요약

높이를 오름차순으로 정렬하고 m=floor(N/2)칸 떨어진 차이 heights[i+m]-heights[i]만 살펴보기.

N=2m이면 정답은 이 차이들의 최솟값. m+1개 지점 사이에 나머지 m-1개를 끼워 넣어도 내부 이웃 하나는 남기 때문에 이보다 클 수 없음.

작은 쪽 m개와 큰 쪽 m개를 큰 값0, 작은 값0, 큰 값1, 작은 값1, ... 순서로 교대하면 모든 이웃 차이가 이 최솟값 이상.

N=2m+1이면 정답은 두 번째 작은 차이. 같은 차이가 여러 번 나오면 중복을 그대로 세기.

m+1개 연속구간 둘의 내부 이웃을 모두 피하는 배치는 불가능. 가장 짧은 두 구간 중 하나에는 내부 이웃이 남아 두 번째 길이가 상한.

가장 짧은 구간부터 원형으로 번호를 다시 붙여 0,m+1,1,m+2,...,m 순서로 교대하면 그 구간 내부만 피할 수 있어 상한을 달성.

정렬 O(N log N), 이후 차이 조사 O(N). 입력 배열 외에 새 배열은 만들지 않고 작은 값 두 개만 저장.

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stdlib.h>
#include <limits.h>

static int compare_height(const void* left, const void* right) {
    int a = *(const int*)left, b = *(const int*)right;
    return (a > b) - (a < b);
}

int solution(int heights[], size_t heights_len) {
    qsort(heights, heights_len, sizeof(*heights), compare_height);
    int smallest = INT_MAX, second = INT_MAX;
    size_t half = heights_len / 2;
    for (size_t left = 0; left + half < heights_len; ++left) {
        int gap = heights[left + half] - heights[left];
        if (gap < smallest) {
            second = smallest;
            smallest = gap;
        } else if (gap < second) {
            second = gap;
        }
    }
    return heights_len % 2 == 0 ? smallest : second;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // qsort로 높이를 오름차순 정렬
// #include <limits.h>  // 작은 차이 두 개를 초기화할 INT_MAX
// 
// static int compare_height(const void* left, const void* right) {  // qsort가 두 높이의 정렬 순서를 비교할 함수
//     int a = *(const int*)left, b = *(const int*)right;  // 일반 포인터를 정수 포인터로 바꿔 실제 높이 읽기
//     return (a > b) - (a < b);  // 큰 값은 1, 작은 값은 -1, 같으면 0을 돌려 오름차순 비교
// }  // 높이 비교 함수 끝
// 
// int solution(int heights[], size_t heights_len) {  // 높이 배열과 길이를 받아 최대화한 최소 이웃 차이 계산
//     qsort(heights, heights_len, sizeof(*heights), compare_height);  // 높이 순위를 기준으로 m칸 간격의 구간을 찾을 준비
//     int smallest = INT_MAX, second = INT_MAX;  // m칸 간격 차이 중 가장 작은 값과 두 번째 작은 값; 같은 값도 두 번 세기
//     size_t half = heights_len / 2;  // 짝수 2m개와 홀수 2m+1개 모두에서 사용할 간격 m
//     for (size_t left = 0; left + half < heights_len; ++left) {  // 정렬된 연속 m+1개 구간을 하나씩 확인
//         int gap = heights[left + half] - heights[left];  // 이 구간 안에서 만들 수 있는 가장 큰 높이 차이
//         if (gap < smallest) {  // 지금까지의 최솟값보다 더 작은 구간을 찾은 경우
//             second = smallest;  // 이전 최솟값을 두 번째 자리로 이동
//             smallest = gap;  // 새 최솟값 저장
//         } else if (gap < second) {  // 최솟값과 같은 경우도 포함해 두 번째 작은 값을 갱신
//             second = gap;  // 가장 짧은 구간 하나를 제외했을 때의 최솟값
//         }  // 작은 차이 두 개 갱신 끝
//     }  // 모든 m칸 간격의 차이 조사 끝
//     return heights_len % 2 == 0 ? smallest : second;  // 짝수는 최단구간을 피할 수 없고, 홀수는 최단구간 하나까지 피할 수 있음
// }  // 최대화한 이웃 높이 차이의 최솟값 반환 끝

// 풀이 요약
// 높이를 오름차순으로 정렬하고 m=floor(N/2)칸 떨어진 차이 heights[i+m]-heights[i]만 살펴보기.
// N=2m이면 정답은 이 차이들의 최솟값. m+1개 지점 사이에 나머지 m-1개를 끼워 넣어도 내부 이웃 하나는 남기 때문에 이보다 클 수 없음.
// 작은 쪽 m개와 큰 쪽 m개를 큰 값0, 작은 값0, 큰 값1, 작은 값1, ... 순서로 교대하면 모든 이웃 차이가 이 최솟값 이상.
// N=2m+1이면 정답은 두 번째 작은 차이. 같은 차이가 여러 번 나오면 중복을 그대로 세기.
// m+1개 연속구간 둘의 내부 이웃을 모두 피하는 배치는 불가능. 가장 짧은 두 구간 중 하나에는 내부 이웃이 남아 두 번째 길이가 상한.
// 가장 짧은 구간부터 원형으로 번호를 다시 붙여 0,m+1,1,m+2,...,m 순서로 교대하면 그 구간 내부만 피할 수 있어 상한을 달성.
// 정렬 O(N log N), 이후 차이 조사 O(N). 입력 배열 외에 새 배열은 만들지 않고 작은 값 두 개만 저장.
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
