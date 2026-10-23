# 비밀 코드 해독

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/388352) · Level 2 · C

## 풀이

1..n에서 서로 다른 5개를 고른 모든 조합을 확인; 각 시도와의 교집합 크기가 ans와 모두 같으면 정답 후보
예: 후보 {1,2,3,4,5}, 시도 {1,2,6,7,8}의 일치 개수는 2; 시간 O(nC5*시도 수), 집합 크기는 5로 고정

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int n, int** q, size_t q_rows, size_t q_cols, int ans[], size_t ans_len) {
    (void)ans_len;
    int answer = 0;
    for (int a = 1; a <= n - 4; ++a) for (int b = a + 1; b <= n - 3; ++b)
    for (int c = b + 1; c <= n - 2; ++c) for (int d = c + 1; d <= n - 1; ++d) for (int e = d + 1; e <= n; ++e) {
        bool valid = true;
        for (size_t i = 0; i < q_rows; ++i) {
            int matched = 0;
            for (size_t j = 0; j < q_cols; ++j) matched += q[i][j] == a || q[i][j] == b || q[i][j] == c || q[i][j] == d || q[i][j] == e;
            if (matched != ans[i]) { valid = false; break; }
        }
        answer += valid;
    }
    return answer;
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
// int solution(int n, int** q, size_t q_rows, size_t q_cols, int ans[], size_t ans_len) {  // 1..n에서 서로 다른 5개를 고른 모든 조합을 확인; 각 시도와의 교집합 크기가 ans와 모두 같으면 정답 후보
//     (void)ans_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int answer = 0;  // 응답을 모두 만족하는 비밀 코드 수 저장
//     for (int a = 1; a <= n - 4; ++a) for (int b = a + 1; b <= n - 3; ++b)  // 첫 비밀 숫자 순서대로 확인; 둘째 비밀 숫자 갱신
//     for (int c = b + 1; c <= n - 2; ++c) for (int d = c + 1; d <= n - 1; ++d) for (int e = d + 1; e <= n; ++e) {  // 셋째 비밀 숫자 순서대로 확인; 넷째 비밀 숫자 / 다섯째 비밀 숫자 갱신
//         bool valid = true;  // 현재 다섯 숫자가 모든 응답과 맞는지 여부 저장
//         for (size_t i = 0; i < q_rows; ++i) {  // 질문 번호 순서대로 확인
//             int matched = 0;  // 이번 질문과 겹치는 숫자 수 저장
//             for (size_t j = 0; j < q_cols; ++j) matched += q[i][j] == a || q[i][j] == b || q[i][j] == c || q[i][j] == d || q[i][j] == e;  // 질문의 숫자 위치 순서대로 확인; 이번 질문과 겹치는 숫자 수 / 질문 번호 / 질문의 숫자 위치 더해 누적
//             if (matched != ans[i]) { valid = false; break; }  // 이번 질문과 일치하는 숫자 수가 응답과 다르면 후보 제외
//         }  // 이 범위 끝
//         answer += valid;  // 응답을 모두 만족하는 비밀 코드 수 / 현재 다섯 숫자가 모든 응답과 맞는지 여부 더해 누적
//     }  // 이 범위 끝
//     return answer;  // 응답을 모두 만족하는 비밀 코드 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 1..n에서 서로 다른 5개를 고른 모든 조합을 확인; 각 시도와의 교집합 크기가 ans와 모두 같으면 정답 후보
// 예: 후보 {1,2,3,4,5}, 시도 {1,2,6,7,8}의 일치 개수는 2; 시간 O(nC5*시도 수), 집합 크기는 5로 고정
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:08:11
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/008_388352_%EB%B9%84%EB%B0%80_%EC%BD%94%EB%93%9C_%ED%95%B4%EB%8F%85/README.md)
