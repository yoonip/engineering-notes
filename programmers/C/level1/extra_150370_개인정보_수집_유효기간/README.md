# 개인정보 수집 유효기간

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150370) · Level 1 · C

## 풀이

모든 달을 28일로 바꾸어 날짜를 비교; 수집일에 약관 개월 수만큼 더한 날짜가 오늘 이하이면 파기 대상으로 선택

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

static int date_days(const char* date) {
    int y, m, d; sscanf(date, "%d.%d.%d", &y, &m, &d); return y * 336 + m * 28 + d;
}
int* solution(const char* today, const char* terms[], size_t terms_len, const char* privacies[], size_t privacies_len) {
    int months[26] = {0};
    for (size_t i = 0; i < terms_len; ++i) { char kind; int duration; sscanf(terms[i], "%c %d", &kind, &duration); months[kind - 'A'] = duration; }
    int now = date_days(today); int* work = malloc(privacies_len * sizeof(int)); size_t length = 0;
    for (size_t i = 0; i < privacies_len; ++i) {
        char kind = privacies[i][strlen(privacies[i]) - 1];
        int expiration = date_days(privacies[i]) + months[kind - 'A'] * 28;
        if (now >= expiration) work[length++] = (int)i + 1;
    }
    int* answer = malloc(length * sizeof(int)); memcpy(answer, work, length * sizeof(int)); free(work);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// static int date_days(const char* date) {  // 한 달 28일 기준으로 날짜를 정수화
//     int y, m, d; sscanf(date, "%d.%d.%d", &y, &m, &d); return y * 336 + m * 28 + d;  // 연·월·일을 읽어 1년 336일, 한 달 28일 기준 날짜로 바꾸기
// }  // 이 범위 끝
// int* solution(const char* today, const char* terms[], size_t terms_len, const char* privacies[], size_t privacies_len) {  // 모든 달을 28일로 바꾸어 날짜를 비교; 수집일에 약관 개월 수만큼 더한 날짜가 오늘 이하이면 파기 대상으로 선택
//     int months[26] = {0};  // 약관 문자별 보관 개월 수 저장
//     for (size_t i = 0; i < terms_len; ++i) { char kind; int duration; sscanf(terms[i], "%c %d", &kind, &duration); months[kind - 'A'] = duration; }  // 약관 문자별 보관 개월 수 기록
//     int now = date_days(today); int* work = malloc(privacies_len * sizeof(int)); size_t length = 0;  // 오늘을 28일 기준으로 바꾼 날짜 / 파기 대상 번호를 모을 임시 배열 / 파기 대상 수 공간 확보
//     for (size_t i = 0; i < privacies_len; ++i) {  // 약관 또는 개인정보 위치 순서대로 확인
//         char kind = privacies[i][strlen(privacies[i]) - 1];  // 개인정보의 약관 종류 저장
//         int expiration = date_days(privacies[i]) + months[kind - 'A'] * 28;  // 보관 기간이 끝나는 다음 날 저장
//         if (now >= expiration) work[length++] = (int)i + 1;  // 오늘이 보관 종료일 이상이면 파기 대상의 1부터 시작하는 번호 추가
//     }  // 이 범위 끝
//     int* answer = malloc(length * sizeof(int)); memcpy(answer, work, length * sizeof(int)); free(work);  // 파기할 개인정보 번호 공간 확보
//     return answer;  // 파기할 개인정보 번호 반환
// }  // 이 범위 끝

// 풀이 요약
// 모든 달을 28일로 바꾸어 날짜를 비교; 수집일에 약관 개월 수만큼 더한 날짜가 오늘 이하이면 파기 대상으로 선택
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:48:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_150370_%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4_%EC%88%98%EC%A7%91_%EC%9C%A0%ED%9A%A8%EA%B8%B0%EA%B0%84/README.md)
