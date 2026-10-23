# 외계어 사전

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120869) · Level 0 · C

## 풀이

spell의 글자별 필요 개수와 각 사전 단어의 등장 횟수를 비교. 길이와 빈도가 모두 같은 단어가 있으면 1, 없으면 2를 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* spell[], size_t spell_len, const char* dic[], size_t dic_len) {
    int need[26] = {0};
    for (size_t i = 0; i < spell_len; ++i) ++need[spell[i][0] - 'a'];
    for (size_t i = 0; i < dic_len; ++i) {
        int count[26] = {0};
        if (strlen(dic[i]) != spell_len) continue;
        for (size_t j = 0; dic[i][j]; ++j) ++count[dic[i][j] - 'a'];
        if (memcmp(need, count, sizeof(need)) == 0) return 1;
    }
    return 2;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* spell[], size_t spell_len, const char* dic[], size_t dic_len) {  // 외계어 사전 풀이 시작
//     int need[26] = {0};  // int 배열 need의 26개 값을 0으로 초기화하여 spell에 필요한 소문자별 개수를 저장
//     for (size_t i = 0; i < spell_len; ++i) ++need[spell[i][0] - 'a'];  // for로 한 글자 문자열 spell[i]의 첫 문자를 읽고 a를 뺀 인덱스에 필요한 개수를 1씩 누적
//     for (size_t i = 0; i < dic_len; ++i) {  // 바깥 for로 사전 단어의 인덱스 i를 순회하여 조건에 맞는 단어가 있는지 검사
//         int count[26] = {0};  // 현재 사전 단어의 문자 빈도를 담을 count 배열 26칸을 0으로 초기화
//         if (strlen(dic[i]) != spell_len) continue;  // 단어 길이가 사용할 글자 수 spell_len과 다르면 모든 글자를 정확히 한 번씩 쓸 수 없으므로 continue로 다음 단어를 검사
//         for (size_t j = 0; dic[i][j]; ++j) ++count[dic[i][j] - 'a'];  // 안쪽 for로 dic[i]의 각 문자를 문자열 끝까지 읽어 count에 소문자별 등장 횟수를 누적
//         if (memcmp(need, count, sizeof(need)) == 0) return 1;  // memcmp로 26개 정수의 빈도 배열을 비교. 필요한 빈도 need와 현재 빈도 count가 모두 같으면 조건을 만족하므로 즉시 1을 반환
//     }  // 블록 끝
//     return 2;  // 사전의 모든 단어를 확인해도 일치하는 빈도가 없으면 2를 반환
// }  // 블록 끝

// 풀이 요약
// spell의 글자별 필요 개수와 각 사전 단어의 등장 횟수를 비교. 길이와 빈도가 모두 같은 단어가 있으면 1, 없으면 2를 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:29:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120869_%EC%99%B8%EA%B3%84%EC%96%B4_%EC%82%AC%EC%A0%84/README.md)
