# 영어가 싫어요

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120894) · Level 0 · C

## 풀이

현재 위치의 접두사를 zero부터 nine까지의 영어 이름과 비교. 일치한 숫자를 기존 결과의 10배에 더하고, 읽기 포인터를 다음 단어로 옮기기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

long long solution(const char* numbers) {
    const char* words[] = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    long long answer = 0;
    const char* p = numbers;
    while (*p) {
        for (int d = 0; d < 10; ++d) {
            size_t len = strlen(words[d]);
            if (strncmp(p, words[d], len) == 0) {
                answer = answer * 10 + d; p += len; break;
            }
        }
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
// long long solution(const char* numbers) {  // 영어가 싫어요 풀이 시작
//     const char* words[] = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};  // 문자열 포인터 배열 words의 인덱스 0부터 9에 각 숫자의 영어 이름을 저장하여 이름과 숫자를 대응시킵니다
//     long long answer = 0;  // long long 변수 answer를 0으로 초기화하여 읽은 숫자들을 십진 정수로 누적
//     const char* p = numbers;  // const char* 포인터 p를 numbers의 시작에 두어 아직 변환하지 않은 첫 단어의 위치를 가리킵니다
//     while (*p) {  // while은 p가 문자열 끝에 도달할 때까지 영어 숫자 이름을 한 단어씩 읽기
//         for (int d = 0; d < 10; ++d) {  // for로 숫자 후보 d를 0부터 9까지 검사하여 현재 위치에서 시작하는 영어 이름을 찾기
//             size_t len = strlen(words[d]);  // strlen으로 후보 words[d]의 문자 수를 구해 len에 저장
//             if (strncmp(p, words[d], len) == 0) {  // strncmp로 p에서 len글자가 words[d]와 같은지 검사. 반환값 0은 해당 영어 숫자 이름이 일치한다는 뜻임
//                 answer = answer * 10 + d; p += len; break;  // 기존 answer를 10배하고 찾은 숫자 d를 더하기. p를 단어 길이 len만큼 옮기고 break로 후보 검색을 끝내 다음 단어로 넘어갑니다
//             }  // 블록 끝
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 현재 위치의 접두사를 zero부터 nine까지의 영어 이름과 비교. 일치한 숫자를 기존 결과의 10배에 더하고, 읽기 포인터를 다음 단어로 옮기기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:27:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120894_%EC%98%81%EC%96%B4%EA%B0%80_%EC%8B%AB%EC%96%B4%EC%9A%94/README.md)
