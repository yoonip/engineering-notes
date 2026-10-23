# 로그인 성공?

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120883) · Level 0 · C

## 풀이

코딩 문제의 입력 데이터에서 아이디 존재 여부를 먼저 확인하고 비밀번호를 비교

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* id_pw[], size_t id_pw_len, const char*** db, size_t db_rows, size_t db_cols) {
    (void)id_pw_len; (void)db_cols;
    const char* result = "fail";
    for (size_t i = 0; i < db_rows; ++i)
        if (strcmp(id_pw[0], db[i][0]) == 0) {
            result = strcmp(id_pw[1], db[i][1]) == 0 ? "login" : "wrong pw";
            break;
        }
    char* answer = malloc(strlen(result) + 1);
    strcpy(answer, result);
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
// char* solution(const char* id_pw[], size_t id_pw_len, const char*** db, size_t db_rows, size_t db_cols) {  // 로그인 성공? 풀이 시작
//     (void)id_pw_len; (void)db_cols;  // 배열 크기처럼 함수 형식에 포함되지만 본문에서 사용하지 않는 매개변수임을 표시
//     const char* result = "fail";  // 같은 아이디를 못 찾았을 때 반환할 기본 결과 fail 준비
//     for (size_t i = 0; i < db_rows; ++i)  // 등록된 계정을 차례로 검색
//         if (strcmp(id_pw[0], db[i][0]) == 0) {  // 입력 아이디와 같은 계정을 찾으면 그 계정의 비밀번호 비교
//             result = strcmp(id_pw[1], db[i][1]) == 0 ? "login" : "wrong pw";  // 아이디가 같은 계정의 비밀번호를 비교해 로그인 성공·실패 구분
//             break;  // break는 현재 계산을 마친 뒤 가장 안쪽 반복문을 종료
//         }  // 블록 끝
//     char* answer = malloc(strlen(result) + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     strcpy(answer, result);  // strcpy는 종료 문자까지 포함하여 문자열을 결과 공간에 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 코딩 문제의 입력 데이터에서 아이디 존재 여부를 먼저 확인하고 비밀번호를 비교
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120883_%EB%A1%9C%EA%B7%B8%EC%9D%B8_%EC%84%B1%EA%B3%B5_/README.md)
