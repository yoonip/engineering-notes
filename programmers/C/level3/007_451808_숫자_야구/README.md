# 숫자 야구

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/451808) · Level 3 · C

## 풀이

가능한 비밀번호 3024개를 유지; 실제 단서와 모순되는 후보를 지우고, 다음 질문은 가장 큰 응답 그룹의 크기를 최소화하는 후보로 선택
서로 다른 1~9 숫자 네 개만 쓰므로 공통 숫자 수에서 스트라이크 수를 빼서 볼 수 계산; 이 선택·동률 순서의 전체 응답 트리를 검증해 최대 6번 질문이면 후보가 하나임을 확인
예: 1234에 대한 응답이 1S 1B이면 공통 숫자는 2개, 제자리 숫자는 1개인 비밀번호만 남기기; 후보가 하나면 4S 응답을 추가로 받지 않아도 정답을 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

extern char* submit(int value);
typedef struct { unsigned char digits[4]; unsigned mask; int number; } Pattern;
static unsigned char* feedback(int index, const Pattern* patterns, int count, unsigned char** cache) {
    if (cache[index]) return cache[index];
    unsigned char* row = malloc((size_t)count);
    for (int i = 0; i < count; ++i) {
        int strikes = 0; for (int d = 0; d < 4; ++d) strikes += patterns[index].digits[d] == patterns[i].digits[d];
        row[i] = (unsigned char)(__builtin_popcount(patterns[index].mask & patterns[i].mask) * 5 + strikes);
    }
    cache[index] = row;
    return row;
}
int solution(int n) {
    const int count = 3024; Pattern* patterns = malloc((size_t)count * sizeof(*patterns)); int at = 0;
    for (int a = 1; a <= 9; ++a) for (int b = 1; b <= 9; ++b) if (b != a) for (int c = 1; c <= 9; ++c) if (c != a && c != b) for (int d = 1; d <= 9; ++d) if (d != a && d != b && d != c) {
        patterns[at] = (Pattern){{(unsigned char)a,(unsigned char)b,(unsigned char)c,(unsigned char)d},(1u << a) | (1u << b) | (1u << c) | (1u << d),a * 1000 + b * 100 + c * 10 + d}; ++at;
    }
    unsigned char** cache = calloc((size_t)count, sizeof(*cache)); int* candidates = malloc((size_t)count * sizeof(*candidates)); int remaining = count;
    for (int i = 0; i < count; ++i) candidates[i] = i;
    for (int turn = 0; turn < n && remaining > 1; ++turn) {
        int selected = candidates[0];
        if (turn) {
            int best = remaining + 1;
            for (int i = 0; i < remaining; ++i) {
                int guess = candidates[i], buckets[25] = {0}, worst = 0; unsigned char* row = feedback(guess,patterns,count,cache);
                for (int j = 0; j < remaining; ++j) { int value = ++buckets[row[candidates[j]]]; if (value > worst) worst = value; if (worst >= best) break; }
                if (worst < best) { best = worst; selected = guess; if (best == 1) break; }
            }
        }
        char* clue = submit(patterns[selected].number); int strikes = clue[0] - '0', balls = clue[3] - '0', observed = (strikes + balls) * 5 + strikes;
        unsigned char* row = feedback(selected,patterns,count,cache); int next_count = 0;
        for (int i = 0; i < remaining; ++i) if (row[candidates[i]] == observed) candidates[next_count++] = candidates[i];
        remaining = next_count;
    }
    int answer = patterns[candidates[0]].number;
    for (int i = 0; i < count; ++i) free(cache[i]); free(cache); free(candidates); free(patterns);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// extern char* submit(int value);  // 채점기가 제공하는 질의 함수
// typedef struct { unsigned char digits[4]; unsigned mask; int number; } Pattern;  // 후보의 네 숫자 / 후보에 쓰인 숫자 집합 / 네 자리를 합친 정수를 한 상태로 묶기
// static unsigned char* feedback(int index, const Pattern* patterns, int count, unsigned char** cache) {  // 추측 하나와 모든 후보의 스트라이크·볼 표 만들기
//     if (cache[index]) return cache[index];  // 이미 구한 추측 결과표가 있으면 재사용
//     unsigned char* row = malloc((size_t)count);  // 이번 추측과 모든 후보의 피드백 공간 확보
//     for (int i = 0; i < count; ++i) {  // 후보 위치 순서대로 확인
//         int strikes = 0; for (int d = 0; d < 4; ++d) strikes += patterns[index].digits[d] == patterns[i].digits[d];  // 추측과 후보의 네 자리 중 같은 위치의 같은 숫자 세기
//         row[i] = (unsigned char)(__builtin_popcount(patterns[index].mask & patterns[i].mask) * 5 + strikes);  // 공통 숫자 수와 스트라이크 수를 하나의 피드백 번호로 압축
//     }  // 이 범위 끝
//     cache[index] = row;  // 추측별 미리 계산한 피드백 표 갱신
//     return row;  // 이번 추측과 모든 후보의 피드백 반환
// }  // 이 범위 끝
// int solution(int n) {  // 가능한 비밀번호 3024개를 유지; 실제 단서와 모순되는 후보를 지우고, 다음 질문은 가장 큰 응답 그룹의 크기를 최소화하는 후보로 선택
//     const int count = 3024; Pattern* patterns = malloc((size_t)count * sizeof(*patterns)); int at = 0;  // 전체 후보 수 / 중복 없는 네 자리 후보 / 후보를 채울 위치 공간 확보
//     for (int a = 1; a <= 9; ++a) for (int b = 1; b <= 9; ++b) if (b != a) for (int c = 1; c <= 9; ++c) if (c != a && c != b) for (int d = 1; d <= 9; ++d) if (d != a && d != b && d != c) {  // 1~9에서 서로 다른 네 숫자를 골라 3024개 비밀번호 후보 만들기
//         patterns[at] = (Pattern){{(unsigned char)a,(unsigned char)b,(unsigned char)c,(unsigned char)d},(1u << a) | (1u << b) | (1u << c) | (1u << d),a * 1000 + b * 100 + c * 10 + d}; ++at;  // 각 후보의 자리 배열·숫자 집합 비트·정수 표현을 함께 저장
//     }  // 이 범위 끝
//     unsigned char** cache = calloc((size_t)count, sizeof(*cache)); int* candidates = malloc((size_t)count * sizeof(*candidates)); int remaining = count;  // 추측별 미리 계산한 피드백 표 / 응답과 맞아 살아남은 후보 번호 / 남은 후보 수 공간 확보하고 0으로 시작
//     for (int i = 0; i < count; ++i) candidates[i] = i;  // 후보 위치 순서대로 확인; 응답과 맞아 살아남은 후보 번호 갱신
//     for (int turn = 0; turn < n && remaining > 1; ++turn) {  // 현재 질문 횟수 순서대로 확인
//         int selected = candidates[0];  // 이번에 제출할 추측 저장
//         if (turn) {  // 두 번째 질문부터는 최악의 후보 수가 가장 작아지는 추측 선택
//             int best = remaining + 1;  // 가장 작은 최악 분할 크기 저장
//             for (int i = 0; i < remaining; ++i) {  // 후보 위치 순서대로 확인
//                 int guess = candidates[i], buckets[25] = {0}, worst = 0; unsigned char* row = feedback(guess,patterns,count,cache);  // 시험할 추측 후보 / 피드백별 남을 후보 수 / 이번 추측의 가장 큰 분할 / 이번 추측과 모든 후보의 피드백 저장
//                 for (int j = 0; j < remaining; ++j) { int value = ++buckets[row[candidates[j]]]; if (value > worst) worst = value; if (worst >= best) break; }  // 추측의 응답별 후보 수를 세되 기존 최선보다 나쁘면 계산 중단
//                 if (worst < best) { best = worst; selected = guess; if (best == 1) break; }  // 최악의 후보 묶음을 가장 작게 만드는 추측 선택, 모두 구별되면 탐색 종료
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         char* clue = submit(patterns[selected].number); int strikes = clue[0] - '0', balls = clue[3] - '0', observed = (strikes + balls) * 5 + strikes;  // 추측과 후보의 네 자리 중 같은 위치의 같은 숫자 세기
//         unsigned char* row = feedback(selected,patterns,count,cache); int next_count = 0;  // 이번 추측과 모든 후보의 피드백 / 이번 응답과 맞는 후보 수 저장
//         for (int i = 0; i < remaining; ++i) if (row[candidates[i]] == observed) candidates[next_count++] = candidates[i];  // 관측한 스트라이크·볼 응답과 같은 후보만 앞으로 모으기
//         remaining = next_count;  // 남은 후보 수 갱신
//     }  // 이 범위 끝
//     int answer = patterns[candidates[0]].number;  // 최종 비밀 숫자 저장
//     for (int i = 0; i < count; ++i) free(cache[i]); free(cache); free(candidates); free(patterns);  // 후보 위치 순서대로 확인; 추측별 미리 계산한 피드백 표 / 후보 위치 / 응답과 맞아 살아남은 후보 번호 / 중복 없는 네 자리 후보 임시 공간 정리
//     return answer;  // 최종 비밀 숫자 반환
// }  // 이 범위 끝

// 풀이 요약
// 가능한 비밀번호 3024개를 유지; 실제 단서와 모순되는 후보를 지우고, 다음 질문은 가장 큰 응답 그룹의 크기를 최소화하는 후보로 선택
// 서로 다른 1~9 숫자 네 개만 쓰므로 공통 숫자 수에서 스트라이크 수를 빼서 볼 수 계산; 이 선택·동률 순서의 전체 응답 트리를 검증해 최대 6번 질문이면 후보가 하나임을 확인
// 예: 1234에 대한 응답이 1S 1B이면 공통 숫자는 2개, 제자리 숫자는 1개인 비밀번호만 남기기; 후보가 하나면 4S 응답을 추가로 받지 않아도 정답을 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:25:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/007_451808_%EC%88%AB%EC%9E%90_%EC%95%BC%EA%B5%AC/README.md)
