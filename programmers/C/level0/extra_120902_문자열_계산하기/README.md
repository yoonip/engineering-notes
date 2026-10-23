# 문자열 계산하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120902) · Level 0 · C

## 풀이

strtol로 첫 정수를 읽은 뒤 연산자와 다음 정수를 차례로 읽기. 공백을 건너뛰며 덧셈·뺄셈을 왼쪽부터 누적

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* my_string) {
    const char* p = my_string;
    char* end;
    int answer = (int)strtol(p, &end, 10);
    p = end;
    while (*p) {
        while (*p == ' ') ++p;
        if (!*p) break;
        char operation = *p++;
        int value = (int)strtol(p, &end, 10);
        answer += operation == '+' ? value : -value;
        p = end;
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
// int solution(const char* my_string) {  // 문자열 계산하기 풀이 시작
//     const char* p = my_string;  // const char* 포인터 p를 식의 시작에 두어 다음에 읽을 숫자나 연산자의 위치를 추적
//     char* end;  // char* 포인터 end는 strtol이 정수를 읽은 직후의 문자열 위치를 받을 변수임
//     int answer = (int)strtol(p, &end, 10);  // strtol로 p에서 첫 십진 정수를 읽어 answer의 초깃값으로 저장하며, &end로 다음 읽기 위치를 함께 받기
//     p = end;  // p를 end로 옮겨 첫 정수 다음의 공백 또는 문자열 끝부터 처리를 이어갑니다
//     while (*p) {  // while은 p가 문자열 종료 문자를 가리키기 전까지 다음 연산자와 피연산자를 처리
//         while (*p == ' ') ++p;  // 안쪽 while로 연산자 앞의 공백들을 건너뛰어 p를 다음 기호로 옮기기
//         if (!*p) break;  // 공백을 건너뛴 뒤 문자열 끝이면 break로 더 읽을 연산이 없음을 처리
//         char operation = *p++;  // *p로 현재 연산자를 operation에 저장하고 후위 증가 p++로 다음 정수를 읽을 위치로 이동
//         int value = (int)strtol(p, &end, 10);  // strtol로 다음 십진 정수를 value에 저장. 함수가 숫자 앞 공백을 건너뛰고, end에 숫자 다음 위치를 기록
//         answer += operation == '+' ? value : -value;  // operation이 +이면 value를 더하고, -이면 -value를 더하여 현재까지의 계산 결과 answer를 갱신
//         p = end;  // p를 end로 옮겨 방금 읽은 정수 다음의 연산 처리를 준비
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// strtol로 첫 정수를 읽은 뒤 연산자와 다음 정수를 차례로 읽기. 공백을 건너뛰며 덧셈·뺄셈을 왼쪽부터 누적
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:26:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120902_%EB%AC%B8%EC%9E%90%EC%97%B4_%EA%B3%84%EC%82%B0%ED%95%98%EA%B8%B0/README.md)
