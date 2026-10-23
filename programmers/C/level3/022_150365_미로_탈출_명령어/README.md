# 미로 탈출 명령어

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150365) · Level 3 · C

## 풀이

정확히 남은 횟수로 도착하려면 최단거리 이하의 이동 횟수를 줄 수 없고, 여분은 왕복 이동처럼 짝수여야 하기
매 칸마다 d·l·r·u 사전순으로 보면서 이 조건을 만족하는 첫 방향을 고르면 가장 앞선 경로가 됨; 시간 O(K), 공간 O(K)
예: 3×4 격자의 (2,3)에서 (3,1)까지 5칸이면 가능한 가장 작은 접두사를 차례로 확정해 dllrl을 얻기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

char* solution(int n, int m, int x, int y, int r, int c, int k) {
    int distance = abs(x - r) + abs(y - c); char* answer = malloc((size_t)k + 12);
    if (distance > k || (k - distance) % 2) { strcpy(answer, "impossible"); return answer; }
    const char letters[4] = {'d','l','r','u'}; const int dr[4] = {1,0,0,-1}, dc[4] = {0,-1,1,0};
    for (int step = 0; step < k; ++step) for (int d = 0; d < 4; ++d) {
        int nx = x + dr[d], ny = y + dc[d], remaining = k - step - 1;
        if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
        int needed = abs(nx - r) + abs(ny - c);
        if (needed <= remaining && (remaining - needed) % 2 == 0) { answer[step] = letters[d]; x = nx; y = ny; break; }
    }
    answer[k] = '\0';
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
// char* solution(int n, int m, int x, int y, int r, int c, int k) {  // 정확히 남은 횟수로 도착하려면 최단거리 이하의 이동 횟수를 줄 수 없고, 여분은 왕복 이동처럼 짝수여야 하기
//     int distance = abs(x - r) + abs(y - c); char* answer = malloc((size_t)k + 12);  // 출발점과 도착점의 맨해튼 거리 / 사전순으로 가장 빠른 탈출 명령 공간 확보
//     if (distance > k || (k - distance) % 2) { strcpy(answer, "impossible"); return answer; }  // 최소 거리보다 짧거나 남은 이동 수의 홀짝이 다르면 탈출 불가능
//     const char letters[4] = {'d','l','r','u'}; const int dr[4] = {1,0,0,-1}, dc[4] = {0,-1,1,0};  // 사전순 d l r u / 방향별 행 변화 / 방향별 열 변화 저장
//     for (int step = 0; step < k; ++step) for (int d = 0; d < 4; ++d) {  // 명령을 채울 위치 순서대로 확인; 다음 명령 후보 갱신
//         int nx = x + dr[d], ny = y + dc[d], remaining = k - step - 1;  // 다음 행 / 다음 열 / 앞으로 써야 할 명령 수 저장
//         if (nx < 1 || nx > n || ny < 1 || ny > m) continue;  // 다음 칸이 미로 범위를 벗어나면 건너뛰기
//         int needed = abs(nx - r) + abs(ny - c);  // 다음 칸에서 목표까지의 최소 거리 저장
//         if (needed <= remaining && (remaining - needed) % 2 == 0) { answer[step] = letters[d]; x = nx; y = ny; break; }  // 남은 횟수로 목표에 도착할 수 있으면 사전순 첫 방향을 선택
//     }  // 이 범위 끝
//     answer[k] = '\0';  // 문자열 끝에 널 문자 붙이기
//     return answer;  // 사전순으로 가장 빠른 탈출 명령 반환
// }  // 이 범위 끝

// 풀이 요약
// 정확히 남은 횟수로 도착하려면 최단거리 이하의 이동 횟수를 줄 수 없고, 여분은 왕복 이동처럼 짝수여야 하기
// 매 칸마다 d·l·r·u 사전순으로 보면서 이 조건을 만족하는 첫 방향을 고르면 가장 앞선 경로가 됨; 시간 O(K), 공간 O(K)
// 예: 3×4 격자의 (2,3)에서 (3,1)까지 5칸이면 가능한 가장 작은 접두사를 차례로 확정해 dllrl을 얻기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/022_150365_%EB%AF%B8%EB%A1%9C_%ED%83%88%EC%B6%9C_%EB%AA%85%EB%A0%B9%EC%96%B4/README.md)
