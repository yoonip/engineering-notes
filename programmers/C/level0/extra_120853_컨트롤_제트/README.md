# 컨트롤 제트

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120853) · Level 0 · C

## 풀이

문자열에서 숫자를 읽을 때 합과 가장 최근 숫자를 갱신. Z를 만나면 최근 숫자를 합에서 빼고, 다음 숫자나 명령을 읽도록 포인터를 옮기기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* s) {
    int sum = 0, last = 0;
    const char* p = s;
    while (*p) {
        if (*p == ' ') { ++p; continue; }
        if (*p == 'Z') { sum -= last; last = 0; ++p; }
        else {
            char* end;
            last = (int)strtol(p, &end, 10);
            sum += last; p = end;
        }
    }
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* s) {  // 컨트롤 제트 풀이 시작
//     int sum = 0, last = 0;  // int 변수 sum에는 취소를 반영한 합을, last에는 가장 최근에 더한 숫자를 저장하며 둘 다 0으로 시작
//     const char* p = s;  // const char* 포인터 p를 문자열 s의 첫 문자에 연결하여 다음에 읽을 위치를 추적
//     while (*p) {  // p가 가리키는 문자가 문자열 종료 문자가 아닌 동안 숫자 또는 취소 명령을 읽기
//         if (*p == ' ') { ++p; continue; }  // 현재 문자가 공백이면 p를 한 칸 옮기고 continue로 다음 문자를 읽기
//         if (*p == 'Z') { sum -= last; last = 0; ++p; }  // 현재 문자가 Z이면 마지막에 더한 last를 sum에서 빼기. last를 0으로 초기화하고 p를 다음 문자로 옮기기
//         else {  // 공백이나 Z가 아닌 경우에는 부호가 포함될 수 있는 십진 정수를 읽는 처리를 시작
//             char* end;  // char* 포인터 end를 선언하여 숫자를 읽은 직후의 문자 위치를 받을 준비
//             last = (int)strtol(p, &end, 10);  // strtol로 p부터 십진 정수를 읽어 int로 변환해 last에 저장. &end를 전달하여 변환이 끝난 위치도 받기
//             sum += last; p = end;  // 읽은 숫자 last를 sum에 더하고, p를 end로 옮겨 이미 변환한 숫자를 다시 읽지 않게 처리
//         }  // 블록 끝
//     }  // 블록 끝
//     return sum;  // 모든 취소 명령을 반영한 최종 합 sum을 반환
// }  // 블록 끝

// 풀이 요약
// 문자열에서 숫자를 읽을 때 합과 가장 최근 숫자를 갱신. Z를 만나면 최근 숫자를 합에서 빼고, 다음 숫자나 명령을 읽도록 포인터를 옮기기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:36:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120853_%EC%BB%A8%ED%8A%B8%EB%A1%A4_%EC%A0%9C%ED%8A%B8/README.md)
