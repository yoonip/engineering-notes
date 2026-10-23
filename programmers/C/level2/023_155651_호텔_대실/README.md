# 호텔 대실

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/155651) · Level 2 · C

## 풀이

입실에 +1, 청소 종료에 -1을 기록하고 시간별 누적 합의 최댓값을 계산
예: 10:10 퇴실한 방은 10:20부터 다시 사용 가능해 방 1개면 됨; 예약 N개일 때 시간 O(N+1450), 공간 O(1450)

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

static int minute(const char* time) { return ((time[0] - '0') * 10 + time[1] - '0') * 60 + (time[3] - '0') * 10 + time[4] - '0'; }
int solution(const char*** book_time, size_t book_time_rows, size_t book_time_cols) {
    (void)book_time_cols;
    int changes[1451] = {0}, active = 0, answer = 0;
    for (size_t i = 0; i < book_time_rows; ++i) { ++changes[minute(book_time[i][0])]; --changes[minute(book_time[i][1]) + 10]; }
    for (int i = 0; i < 1451; ++i) { active += changes[i]; if (active > answer) answer = active; }
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
// static int minute(const char* time) { return ((time[0] - '0') * 10 + time[1] - '0') * 60 + (time[3] - '0') * 10 + time[4] - '0'; }  // 시:분 표기를 전체 분 수로 바꾸기
// int solution(const char*** book_time, size_t book_time_rows, size_t book_time_cols) {  // 입실에 +1, 청소 종료에 -1을 기록하고 시간별 누적 합의 최댓값을 계산
//     (void)book_time_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int changes[1451] = {0}, active = 0, answer = 0;  // 시각별 대실 시작과 종료 변화량 / 현재 사용 중인 방 수 / 동시에 필요한 최대 방 수 저장
//     for (size_t i = 0; i < book_time_rows; ++i) { ++changes[minute(book_time[i][0])]; --changes[minute(book_time[i][1]) + 10]; }  // 예약 또는 분 단위 시각 순서대로 확인; 시각별 대실 시작과 종료 변화량 갱신
//     for (int i = 0; i < 1451; ++i) { active += changes[i]; if (active > answer) answer = active; }  // 예약 또는 분 단위 시각 순서대로 확인; 현재 사용 중인 방 수 / 시각별 대실 시작과 종료 변화량 / 예약 또는 분 단위 시각 더해 누적
//     return answer;  // 동시에 필요한 최대 방 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 입실에 +1, 청소 종료에 -1을 기록하고 시간별 누적 합의 최댓값을 계산
// 예: 10:10 퇴실한 방은 10:20부터 다시 사용 가능해 방 1개면 됨; 예약 N개일 때 시간 O(N+1450), 공간 O(1450)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:12:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/023_155651_%ED%98%B8%ED%85%94_%EB%8C%80%EC%8B%A4/README.md)
