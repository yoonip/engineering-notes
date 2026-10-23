# 문자열 밀기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120921) · Level 0 · C

## 풀이

오른쪽으로 shift칸 옮기면 A[i]는 위치 (i + shift) % n으로 이동. 문자열 자체를 회전시키는 대신 이 위치의 B 문자와 비교하고, 0회부터 검사해 처음 일치한 횟수를 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* A, const char* B) {
    size_t n = strlen(A);
    if (strlen(B) != n) return -1;
    for (size_t shift = 0; shift < n; ++shift) {
        bool match = true;
        for (size_t i = 0; i < n; ++i)
            if (A[i] != B[(i + shift) % n]) { match = false; break; }
        if (match) return (int)shift;
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* A, const char* B) {  // 문자열 밀기 풀이 시작
//     size_t n = strlen(A);  // 문자열 A의 길이를 strlen으로 구해 n에 저장
//     if (strlen(B) != n) return -1;  // B의 길이가 다르면 회전해도 같아질 수 없으므로 -1을 즉시 반환
//     for (size_t shift = 0; shift < n; ++shift) {  // 오른쪽으로 민 횟수 shift를 0부터 n - 1까지 작은 순서대로 검사
//         bool match = true;  // 현재 shift에서 모든 문자가 일치하는지 기록할 match를 참으로 초기화
//         for (size_t i = 0; i < n; ++i)  // A에서 비교할 원래 문자 위치 i를 0부터 n - 1까지 순회
//             if (A[i] != B[(i + shift) % n]) { match = false; break; }  // 오른쪽 회전 후 위치 (i + shift) % n의 B 문자와 다르면 실패를 기록하고 문자 비교를 끝
//         if (match) return (int)shift;  // 모든 문자가 일치한 첫 shift는 가능한 최소 이동 횟수이므로 int로 변환해 반환
//     }  // 블록 끝
//     return -1;  // 0부터 n - 1회까지 모두 불일치하면 회전으로 만들 수 없으므로 -1을 반환
// }  // 블록 끝

// 풀이 요약
// 오른쪽으로 shift칸 옮기면 A[i]는 위치 (i + shift) % n으로 이동. 문자열 자체를 회전시키는 대신 이 위치의 B 문자와 비교하고, 0회부터 검사해 처음 일치한 횟수를 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:24:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120921_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%B0%80%EA%B8%B0/README.md)
