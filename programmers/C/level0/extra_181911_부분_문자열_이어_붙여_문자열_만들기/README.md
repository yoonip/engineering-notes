# 부분 문자열 이어 붙여 문자열 만들기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181911) · Level 0 · C

## 풀이

각 문자열에서 양 끝을 포함하는 부분 구간을 추출해 이어 붙이기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

char* solution(const char* my_strings[], size_t my_strings_len, int** parts, size_t parts_rows, size_t parts_cols) {
    (void)parts_rows;
    (void)parts_cols;
    size_t total = 0, used = 0;
    for (size_t i = 0; i < my_strings_len; ++i) total += parts[i][1] - parts[i][0] + 1;
    char* answer = malloc(total + 1);
    for (size_t i = 0; i < my_strings_len; ++i) {
        size_t len = (size_t)(parts[i][1] - parts[i][0] + 1);
        memcpy(answer + used, my_strings[i] + parts[i][0], len);
        used += len;
    }
    answer[used] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// char* solution(const char* my_strings[], size_t my_strings_len, int** parts, size_t parts_rows, size_t parts_cols) {  // 부분 문자열 이어 붙여 문자열 만들기 풀이 시작
//     (void)parts_rows;  // 사용하지 않는 배열 크기 매개변수를 명시적으로 무시
//     (void)parts_cols;  // 사용하지 않는 배열 크기 매개변수를 명시적으로 무시
//     size_t total = 0, used = 0;  // 최종 문자열 길이와 현재 복사한 문자 개수를 0으로 초기화
//     for (size_t i = 0; i < my_strings_len; ++i) total += parts[i][1] - parts[i][0] + 1;  // for로 모든 범위의 포함 길이를 구하고 +=로 최종 결과 길이를 합산
//     char* answer = malloc(total + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     for (size_t i = 0; i < my_strings_len; ++i) {  // for로 부분 문자열을 추출할 문자열 배열을 순회
//         size_t len = (size_t)(parts[i][1] - parts[i][0] + 1);  // 양 끝을 포함하는 부분 문자열의 길이를 구하고 size_t형으로 변환
//         memcpy(answer + used, my_strings[i] + parts[i][0], len);  // 포인터 덧셈으로 시작 위치를 찾아 memcpy로 지정된 길이만큼 연결
//         used += len;  // 방금 복사한 길이를 현재 결과 길이에 더하기
//     }  // 블록 끝
//     answer[used] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자열에서 양 끝을 포함하는 부분 구간을 추출해 이어 붙이기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:07:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181911_%EB%B6%80%EB%B6%84_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%9D%B4%EC%96%B4_%EB%B6%99%EC%97%AC_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
