# 옹알이 (1)

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120956) · Level 0 · C

## 풀이

각 문자열의 앞부분부터 허용 발음과 비교하고 일치한 길이만큼 포인터를 옮기기. 네 발음의 사용 여부를 비트 집합에 기록해 한 발음을 중복 사용하지 않으며, 문자열 끝까지 도달한 경우만 세기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* babbling[], size_t babbling_len) {
    const char* sounds[] = {"aya", "ye", "woo", "ma"};
    int answer = 0;
    for (size_t i = 0; i < babbling_len; ++i) {
        const char* p = babbling[i];
        unsigned used = 0;
        while (*p) {
            bool matched = false;
            for (int j = 0; j < 4; ++j) {
                size_t len = strlen(sounds[j]);
                if (!(used & (1u << j)) && strncmp(p, sounds[j], len) == 0) {
                    p += len; used |= 1u << j; matched = true; break;
                }
            }
            if (!matched) break;
        }
        answer += *p == '\0';
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
// int solution(const char* babbling[], size_t babbling_len) {  // 옹알이 (1) 풀이 시작
//     const char* sounds[] = {"aya", "ye", "woo", "ma"};  // 허용된 네 발음 aya, ye, woo, ma를 가리키는 문자열 포인터 배열 sounds를 정의
//     int answer = 0;  // 문자열 전체를 허용 발음으로 읽을 수 있는 경우의 수 answer를 0으로 초기화
//     for (size_t i = 0; i < babbling_len; ++i) {  // 옹알이 문자열의 인덱스 i를 순서대로 순회
//         const char* p = babbling[i];  // 현재 문자열에서 아직 읽지 않은 부분의 시작을 가리킬 포인터 p를 설정
//         unsigned used = 0;  // 현재 문자열에서 이미 사용한 발음을 표시할 비트 집합 used를 0으로 초기화
//         while (*p) {  // p가 널 문자를 가리키기 전까지 남은 부분에서 다음 발음을 찾기
//             bool matched = false;  // 이번 위치에서 허용 발음을 찾았는지 나타낼 matched를 거짓으로 초기화
//             for (int j = 0; j < 4; ++j) {  // 허용 발음의 번호 j를 0부터 3까지 순회
//                 size_t len = strlen(sounds[j]);  // 현재 후보 발음 sounds[j]의 문자 수를 len에 저장
//                 if (!(used & (1u << j)) && strncmp(p, sounds[j], len) == 0) {  // 해당 발음을 아직 사용하지 않았고 남은 문자열의 앞 len글자가 일치할 때만 선택
//                     p += len; used |= 1u << j; matched = true; break;  // 일치한 길이만큼 p를 옮기고 발음 사용 비트를 켠 뒤 성공을 기록하고 후보 탐색을 끝
//                 }  // 블록 끝
//             }  // 블록 끝
//             if (!matched) break;  // 어떤 발음도 일치하지 않으면 더 읽을 수 없으므로 현재 문자열의 처리를 중단
//         }  // 블록 끝
//         answer += *p == '\0';  // p가 널 문자에 도달해 문자열을 끝까지 읽었다면 참의 값 1을 answer에 더하기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자열의 앞부분부터 허용 발음과 비교하고 일치한 길이만큼 포인터를 옮기기. 네 발음의 사용 여부를 비트 집합에 기록해 한 발음을 중복 사용하지 않으며, 문자열 끝까지 도달한 경우만 세기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:24:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120956_%EC%98%B9%EC%95%8C%EC%9D%B4_%281%29/README.md)
