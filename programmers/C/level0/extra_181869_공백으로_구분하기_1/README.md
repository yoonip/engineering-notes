# 공백으로 구분하기 1

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181869) · Level 0 · C

## 풀이

공백을 기준으로 단어들을 나누기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char** solution(const char* my_string) {
    size_t count = 0;
    for (size_t i = 0; my_string[i]; ) {
        while (my_string[i] == ' ') ++i;
        if (!my_string[i]) break;
        ++count;
        while (my_string[i] && my_string[i] != ' ') ++i;
    }
    char** answer = malloc(count * sizeof(char*));
    size_t out = 0;
    for (size_t i = 0; my_string[i]; ) {
        while (my_string[i] == ' ') ++i;
        if (!my_string[i]) break;
        size_t start = i;
        while (my_string[i] && my_string[i] != ' ') ++i;
        size_t n = i - start;
        answer[out] = malloc(n + 1);
        memcpy(answer[out], my_string + start, n);
        answer[out++][n] = '\0';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char** solution(const char* my_string) {  // 공백으로 구분하기 1 풀이 시작
//     size_t count = 0;  // 공백으로 나뉘는 빈칸 아닌 단어 수를 0으로 시작
//     for (size_t i = 0; my_string[i]; ) {  // 문자열 끝까지 각 단어의 시작과 끝을 찾아 이동
//         while (my_string[i] == ' ') ++i;  // 단어 앞의 공백을 모두 건너뜀
//         if (!my_string[i]) break;  // 공백을 건너뛴 뒤 문자열 끝이면 더 읽을 단어가 없어 종료
//         ++count;  // 새로 찾은 단어 하나를 전체 단어 수에 추가
//         while (my_string[i] && my_string[i] != ' ') ++i;  // 공백이나 문자열 끝을 만날 때까지 현재 단어의 끝 탐색
//     }  // 블록 끝
//     char** answer = malloc(count * sizeof(char*));  // answer를 저장할 메모리 확보
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; my_string[i]; ) {  // 문자열 끝까지 각 단어의 시작과 끝을 찾아 이동
//         while (my_string[i] == ' ') ++i;  // 단어 앞의 공백을 모두 건너뜀
//         if (!my_string[i]) break;  // 공백을 건너뛴 뒤 문자열 끝이면 더 읽을 단어가 없어 종료
//         size_t start = i;  // 공백 다음 단어의 시작 위치 기억
//         while (my_string[i] && my_string[i] != ' ') ++i;  // 공백이나 문자열 끝을 만날 때까지 현재 단어의 끝 탐색
//         size_t n = i - start;  // 현재 단어의 시작과 끝 인덱스 차이로 문자 수 계산
//         answer[out] = malloc(n + 1);  // 결과를 저장할 메모리 확보
//         memcpy(answer[out], my_string + start, n);  // 현재 단어의 시작 위치부터 n글자를 새 단어 버퍼에 복사
//         answer[out++][n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 공백을 기준으로 단어들을 나누기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:16:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181869_%EA%B3%B5%EB%B0%B1%EC%9C%BC%EB%A1%9C_%EA%B5%AC%EB%B6%84%ED%95%98%EA%B8%B0_1/README.md)
