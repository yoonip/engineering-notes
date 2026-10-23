# 중복된 문자 제거

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120888) · Level 0 · C

## 풀이

문자 코드별로 결과에 이미 넣었는지 표시. 입력을 왼쪽부터 읽으며 처음 만난 문자만 추가하여 최초 등장 순서를 유지

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string) {
    bool seen[256] = {false};
    char* answer = malloc(strlen(my_string) + 1);
    size_t pos = 0;
    for (size_t i = 0; my_string[i]; ++i) {
        unsigned char c = (unsigned char)my_string[i];
        if (!seen[c]) { seen[c] = true; answer[pos++] = c; }
    }
    answer[pos] = '\0';
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
// char* solution(const char* my_string) {  // 중복된 문자 제거 풀이 시작
//     bool seen[256] = {false};  // bool 배열 seen의 256개 값을 false로 초기화하여 각 문자 코드가 이미 결과에 들어갔는지 표시
//     char* answer = malloc(strlen(my_string) + 1);  // 입력의 모든 문자를 남기는 경우와 마지막 널 문자까지 담도록 strlen(my_string) + 1바이트를 확보
//     size_t pos = 0;  // size_t 변수 pos는 중복 없이 저장한 문자 수이자 다음 문자를 기록할 결과 인덱스임
//     for (size_t i = 0; my_string[i]; ++i) {  // for로 my_string을 왼쪽부터 널 문자 전까지 읽어 최초 등장 순서를 유지
//         unsigned char c = (unsigned char)my_string[i];  // 현재 문자를 unsigned char c로 바꿔 seen의 인덱스로 사용할 0부터 255 사이의 문자 코드를 얻기
//         if (!seen[c]) { seen[c] = true; answer[pos++] = c; }  // 아직 등장하지 않은 c만 seen에 표시하고 answer[pos]에 저장. pos++는 저장한 뒤 다음 결과 위치로 이동
//     }  // 블록 끝
//     answer[pos] = '\0';  // 결과가 끝나는 pos 위치에 널 문자를 기록하여 C 문자열을 완성
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자 코드별로 결과에 이미 넣었는지 표시. 입력을 왼쪽부터 읽으며 처음 만난 문자만 추가하여 최초 등장 순서를 유지
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:28:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120888_%EC%A4%91%EB%B3%B5%EB%90%9C_%EB%AC%B8%EC%9E%90_%EC%A0%9C%EA%B1%B0/README.md)
