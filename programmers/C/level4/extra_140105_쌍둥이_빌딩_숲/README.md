# 쌍둥이 빌딩 숲

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/140105) · Level 4 · C

## 풀이

기존 빌딩 높이를 1씩 올리고 가장 낮은 빌딩 쌍을 붙여 삽입하기; 더 높은 빌딩이 사이에 올 수 없어 새 쌍은 반드시 붙어 있음
맨 앞 한 곳은 보이는 수가 1 늘고, 나머지 2*(쌍 수-1)곳은 기존 빌딩에 가려 보이는 수가 같음; 예: n=3의 결과는 [8,6,1]
시간 O(n*count), 공간 O(count)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int n, int count) {
    const int mod = 1000000007; int* dp = calloc((size_t)count + 1,sizeof(*dp)); int* next = malloc(((size_t)count + 1) * sizeof(*next)); dp[0] = 1;
    for (int pairs = 1; pairs <= n; ++pairs) {
        memset(next,0,((size_t)count + 1) * sizeof(*next));
        for (int visible = 1; visible <= pairs && visible <= count; ++visible) next[visible] = (int)((dp[visible - 1] + 2LL * (pairs - 1) * dp[visible]) % mod);
        int* temp = dp; dp = next; next = temp;
    }
    int answer = dp[count]; free(dp); free(next);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int n, int count) {  // 기존 빌딩 높이를 1씩 올리고 가장 낮은 빌딩 쌍을 붙여 삽입하기; 더 높은 빌딩이 사이에 올 수 없어 새 쌍은 반드시 붙어 있음
//     const int mod = 1000000007; int* dp = calloc((size_t)count + 1,sizeof(*dp)); int* next = malloc(((size_t)count + 1) * sizeof(*next)); dp[0] = 1;  // 보이는 빌딩 쌍 수별 현재 경우의 수 / 한 쌍 추가한 다음 경우의 수 공간 확보하고 0으로 시작
//     for (int pairs = 1; pairs <= n; ++pairs) {  // 지금까지 놓은 빌딩 쌍 수 순서대로 확인
//         memset(next,0,((size_t)count + 1) * sizeof(*next));  // 한 쌍 추가한 다음 경우의 수 초기화
//         for (int visible = 1; visible <= pairs && visible <= count; ++visible) next[visible] = (int)((dp[visible - 1] + 2LL * (pairs - 1) * dp[visible]) % mod);  // 정면에서 보일 쌍 수 순서대로 확인; 한 쌍 추가한 다음 경우의 수 갱신
//         int* temp = dp; dp = next; next = temp;  // DP 배열 교환용 포인터 / 보이는 빌딩 쌍 수별 현재 경우의 수 / 한 쌍 추가한 다음 경우의 수 저장
//     }  // 이 범위 끝
//     int answer = dp[count]; free(dp); free(next);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 정해진 쌍 수가 보이는 배치 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 기존 빌딩 높이를 1씩 올리고 가장 낮은 빌딩 쌍을 붙여 삽입하기; 더 높은 빌딩이 사이에 올 수 없어 새 쌍은 반드시 붙어 있음
// 맨 앞 한 곳은 보이는 수가 1 늘고, 나머지 2*(쌍 수-1)곳은 기존 빌딩에 가려 보이는 수가 같음; 예: n=3의 결과는 [8,6,1]
// 시간 O(n*count), 공간 O(count)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_140105_%EC%8C%8D%EB%91%A5%EC%9D%B4_%EB%B9%8C%EB%94%A9_%EC%88%B2/README.md)
