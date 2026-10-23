# 글자 이어 붙여 문자열 만들기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181915) · Level 0 · C

## 풀이

주어진 인덱스 순서대로 원본 문자를 연결

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <stddef.h>

char* solution(const char* my_string, int index_list[], size_t index_list_len) {
    char* answer = malloc(index_list_len + 1);
    for (size_t i = 0; i < index_list_len; ++i) answer[i] = my_string[index_list[i]];
    answer[index_list_len] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// char* solution(const char* my_string, int index_list[], size_t index_list_len) {  // 글자 이어 붙여 문자열 만들기 풀이 시작
//     char* answer = malloc(index_list_len + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     for (size_t i = 0; i < index_list_len; ++i) answer[i] = my_string[index_list[i]];  // for로 인덱스 목록을 순회하고 중첩 []로 선택한 문자를 결과에 저장
//     answer[index_list_len] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 주어진 인덱스 순서대로 원본 문자를 연결
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:53:42
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181915_%EA%B8%80%EC%9E%90_%EC%9D%B4%EC%96%B4_%EB%B6%99%EC%97%AC_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
