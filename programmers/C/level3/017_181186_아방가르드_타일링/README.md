# 아방가르드 타일링

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181186) · Level 3 · C

## 풀이

높이 3의 I·L 트리오미노 타일링을 폭별 DP로 세기; 세로로 더 나눌 수 없는 끝 묶음은 폭 1·2·3에서 1·2·5가지, 이후 2·2·4가 3칸 주기로 반복됨

이 주기 누적식에서 3칸 전 식을 빼면 D[w]=D[w-1]+2D[w-2]+6D[w-3]+D[w-4]-D[w-6]으로 정리됨; 폭 0·1·2·3은 1·1·3·10으로 따로 시작하기; 시간·공간 O(N)

예: 폭 4는 10+2×3+6×1+1=23; 폭 6부터 여섯 칸 전 항을 빼 중복 누적을 보정하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int n) {
    const long long mod = 1000000007; long long* dp = calloc((size_t)n + 7, sizeof(*dp));
    dp[0] = 1; dp[1] = 1; dp[2] = 3; dp[3] = 10;
    for (int width = 4; width <= n; ++width) {
        long long subtract = width >= 6 ? dp[width - 6] : 0;
        dp[width] = (dp[width - 1] + 2 * dp[width - 2] + 6 * dp[width - 3] + dp[width - 4] - subtract + mod) % mod;
    }
    int answer = (int)dp[n]; free(dp);
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
// int solution(int n) {  // 높이 3의 I·L 트리오미노 타일링을 폭별 DP로 세기; 세로로 더 나눌 수 없는 끝 묶음은 폭 1·2·3에서 1·2·5가지, 이후 2·2·4가 3칸 주기로 반복됨
//     const long long mod = 1000000007; long long* dp = calloc((size_t)n + 7, sizeof(*dp));  // 경우의 수를 나눌 법 / 너비별 아방가르드 타일링 수 공간 확보하고 0으로 시작
//     dp[0] = 1; dp[1] = 1; dp[2] = 3; dp[3] = 10;  // 너비별 아방가르드 타일링 수 갱신
//     for (int width = 4; width <= n; ++width) {  // 채울 타일 너비 순서대로 확인
//         long long subtract = width >= 6 ? dp[width - 6] : 0;  // 겹쳐 센 여섯 칸 전 경우의 수 저장
//         dp[width] = (dp[width - 1] + 2 * dp[width - 2] + 6 * dp[width - 3] + dp[width - 4] - subtract + mod) % mod;  // 너비별 아방가르드 타일링 수 갱신
//     }  // 이 범위 끝
//     int answer = (int)dp[n]; free(dp);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 목표 너비 타일링 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 높이 3의 I·L 트리오미노 타일링을 폭별 DP로 세기; 세로로 더 나눌 수 없는 끝 묶음은 폭 1·2·3에서 1·2·5가지, 이후 2·2·4가 3칸 주기로 반복됨
// 이 주기 누적식에서 3칸 전 식을 빼면 D[w]=D[w-1]+2D[w-2]+6D[w-3]+D[w-4]-D[w-6]으로 정리됨; 폭 0·1·2·3은 1·1·3·10으로 따로 시작하기; 시간·공간 O(N)
// 예: 폭 4는 10+2×3+6×1+1=23; 폭 6부터 여섯 칸 전 항을 빼 중복 누적을 보정하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:28:38
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/017_181186_%EC%95%84%EB%B0%A9%EA%B0%80%EB%A5%B4%EB%93%9C_%ED%83%80%EC%9D%BC%EB%A7%81/README.md)
