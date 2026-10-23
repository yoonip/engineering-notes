# 주차 요금 계산

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92341) · Level 2 · C

## 풀이

입출차를 짝지어 차량별 총 시간을 모으고, 미출차는 23:59로 마감하기; 기본 초과 시간에만 단위 요금을 올림 적용하기
예: 총 334분이면 5000+ceil(154/10)×600=14600.; 기록 R개·차량 C대일 때 시간 O(R+C log C), 공간 O(C)

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

int* solution(int fees[], size_t fees_len, const char* records[], size_t records_len) {
    (void)fees_len;
    int entered[10000], totals[10000] = {0}; bool seen[10000] = {false};
    for (int i = 0; i < 10000; ++i) entered[i] = -1;
    for (size_t i = 0; i < records_len; ++i) {
        int hour, minute, car; char action[4];
        sscanf(records[i], "%d:%d %d %3s", &hour, &minute, &car, action);
        int now = hour * 60 + minute; seen[car] = true;
        if (action[0] == 'I') entered[car] = now;
        else { totals[car] += now - entered[car]; entered[car] = -1; }
    }
    int* answer = malloc(10000 * sizeof(*answer)); size_t pos = 0;
    for (int car = 0; car < 10000; ++car) if (seen[car]) {
        if (entered[car] >= 0) totals[car] += 1439 - entered[car];
        int extra = totals[car] > fees[0] ? totals[car] - fees[0] : 0;
        answer[pos++] = fees[1] + (extra + fees[2] - 1) / fees[2] * fees[3];
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
// int* solution(int fees[], size_t fees_len, const char* records[], size_t records_len) {  // 입출차를 짝지어 차량별 총 시간을 모으고, 미출차는 23:59로 마감하기; 기본 초과 시간에만 단위 요금을 올림 적용하기
//     (void)fees_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int entered[10000], totals[10000] = {0}; bool seen[10000] = {false};  // 차량별 누적 주차 시간 / 입차 기록이 있는 차량 저장
//     for (int i = 0; i < 10000; ++i) entered[i] = -1;  // 주차 기록 위치 순서대로 확인; 차량별 마지막 입차 시각 갱신
//     for (size_t i = 0; i < records_len; ++i) {  // 주차 기록 위치 순서대로 확인
//         int hour, minute, car; char action[4];  // 기록의 시 / 기록의 분 / 차량 번호 / 입차 또는 출차 표시 확인
//         sscanf(records[i], "%d:%d %d %3s", &hour, &minute, &car, action);  // sscanf로 시각·차량번호·입출차 상태 등의 입력 항목을 형식에 맞게 읽기
//         int now = hour * 60 + minute; seen[car] = true;  // 이번 기록을 분으로 바꾼 시각 / 입차 기록이 있는 차량 저장
//         if (action[0] == 'I') entered[car] = now;  // IN 기록이면 해당 차량의 입차 시각 저장
//         else { totals[car] += now - entered[car]; entered[car] = -1; }  // 앞 조건이 아니면 차량별 누적 주차 시간 / 차량 번호 / 이번 기록을 분으로 바꾼 시각 더해 누적
//     }  // 이 범위 끝
//     int* answer = malloc(10000 * sizeof(*answer)); size_t pos = 0;  // 차량 번호순 주차 요금 / 번호순 요금 배열의 다음 위치 공간 확보
//     for (int car = 0; car < 10000; ++car) if (seen[car]) {  // 실제 입차 기록이 있는 차량만 번호순으로 요금 계산
//         if (entered[car] >= 0) totals[car] += 1439 - entered[car];  // 출차 기록 없이 남은 차량은 23시 59분까지 주차 시간 추가
//         int extra = totals[car] > fees[0] ? totals[car] - fees[0] : 0;  // 기본 시간을 넘긴 주차 시간 저장
//         answer[pos++] = fees[1] + (extra + fees[2] - 1) / fees[2] * fees[3];  // 차량 번호순 주차 요금 갱신
//     }  // 이 범위 끝
//     return answer;  // 차량 번호순 주차 요금 반환
// }  // 이 범위 끝

// 풀이 요약
// 입출차를 짝지어 차량별 총 시간을 모으고, 미출차는 23:59로 마감하기; 기본 초과 시간에만 단위 요금을 올림 적용하기
// 예: 총 334분이면 5000+ceil(154/10)×600=14600.; 기록 R개·차량 C대일 때 시간 O(R+C log C), 공간 O(C)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/045_92341_%EC%A3%BC%EC%B0%A8_%EC%9A%94%EA%B8%88_%EA%B3%84%EC%82%B0/README.md)
