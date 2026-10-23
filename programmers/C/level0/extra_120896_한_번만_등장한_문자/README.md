# 한 번만 등장한 문자

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120896) · Level 0 · C

## 풀이

각 문자의 출현 횟수가 1인지 검사한 뒤 사전순으로 연결

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* s) {
    int counts[26] = {0};
    for (size_t i = 0; s[i]; ++i) ++counts[s[i] - 'a'];
    char* answer = malloc(27);
    size_t pos = 0;
    for (int i = 0; i < 26; ++i) if (counts[i] == 1) answer[pos++] = 'a' + i;
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
// char* solution(const char* s) {  // 한 번만 등장한 문자 풀이 시작
//     int counts[26] = {0};  // 각 소문자가 전체 문자열에 나온 횟수를 저장할 배열 준비
//     for (size_t i = 0; s[i]; ++i) ++counts[s[i] - 'a'];  // 입력 문자열의 알파벳별 등장 횟수 세기
//     char* answer = malloc(27);  // answer를 저장할 메모리 확보
//     size_t pos = 0;  // 다음 문자를 쓸 위치는 0부터 시작
//     for (int i = 0; i < 26; ++i) if (counts[i] == 1) answer[pos++] = 'a' + i;  // 한 번만 나온 문자를 a부터 z 순서로 결과에 추가
//     answer[pos] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 문자의 출현 횟수가 1인지 검사한 뒤 사전순으로 연결
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120896_%ED%95%9C_%EB%B2%88%EB%A7%8C_%EB%93%B1%EC%9E%A5%ED%95%9C_%EB%AC%B8%EC%9E%90/README.md)
