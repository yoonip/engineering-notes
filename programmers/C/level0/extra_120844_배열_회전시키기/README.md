# 배열 회전시키기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120844) · Level 0 · C

## 풀이

회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮기기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int numbers[], size_t numbers_len, const char* direction) {
    int* answer = malloc(numbers_len * sizeof(*answer));
    for (size_t i = 0; i < numbers_len; ++i) {
        size_t source = strcmp(direction, "right") == 0 ? (i + numbers_len - 1) % numbers_len : (i + 1) % numbers_len;
        answer[i] = numbers[source];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int* solution(int numbers[], size_t numbers_len, const char* direction) {  // 배열 회전시키기 풀이 시작
//     int* answer = malloc(numbers_len * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < numbers_len; ++i) {  // 회전 결과의 각 칸을 채울 원본 위치 선택
//         size_t source = strcmp(direction, "right") == 0 ? (i + numbers_len - 1) % numbers_len : (i + 1) % numbers_len;  // 오른쪽 회전은 이전 칸, 왼쪽 회전은 다음 칸에서 가져오기. 양 끝은 나머지로 연결
//         answer[i] = numbers[source];  // 회전 후 이 칸에 올 원래 원소 복사
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮기기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:54:14
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120844_%EB%B0%B0%EC%97%B4_%ED%9A%8C%EC%A0%84%EC%8B%9C%ED%82%A4%EA%B8%B0/README.md)
