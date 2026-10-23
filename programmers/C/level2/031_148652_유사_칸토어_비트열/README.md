# 유사 칸토어 비트열

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/148652) · Level 2 · C

## 풀이

비트열은 이전 단계 네 덩어리와 가운데 0 덩어리로 나뉨; 완전한 덩어리는 4의 거듭제곱으로 세고 남은 부분만 재귀 처리
예: n=2의 [4,17]은 8개.; 비트열을 직접 만들지 않으며 시간·재귀 공간 O(n)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static long long prefix(int level, long long length, const long long* five, const long long* four) {
    if (!level) return length;
    long long block = five[level - 1], groups = length / block, rest = length % block;
    long long total = (groups - (groups > 2)) * four[level - 1];
    return groups == 2 ? total : total + prefix(level - 1, rest, five, four);
}
int solution(int n, long long l, long long r) {
    long long five[21] = {1}, four[21] = {1};
    for (int i = 1; i <= n; ++i) { five[i] = five[i - 1] * 5; four[i] = four[i - 1] * 4; }
    return (int)(prefix(n, r, five, four) - prefix(n, l - 1, five, four));
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static long long prefix(int level, long long length, const long long* five, const long long* four) {  // 칸토어 비트열의 처음 length개 위치에 있는 1의 개수를 재귀적으로 계산
//     if (!level) return length;  // 현재 칸토어 단계가 없으면 접두사에서 셀 길이 반환
//     long long block = five[level - 1], groups = length / block, rest = length % block;  // 한 하위 블록 길이 / 완전히 지난 블록 수 / 마지막 블록에서 남은 길이 저장
//     long long total = (groups - (groups > 2)) * four[level - 1];  // 완전히 지난 블록들의 1 개수 저장
//     return groups == 2 ? total : total + prefix(level - 1, rest, five, four);  // 완전히 지난 블록 수 / 완전히 지난 블록들의 1 개수 / 현재 칸토어 단계로 최종값 계산
// }  // 이 범위 끝
// int solution(int n, long long l, long long r) {  // 비트열은 이전 단계 네 덩어리와 가운데 0 덩어리로 나뉨; 완전한 덩어리는 4의 거듭제곱으로 세고 남은 부분만 재귀 처리
//     long long five[21] = {1}, four[21] = {1};  // 단계별 5의 거듭제곱 / 단계별 1 개수 저장
//     for (int i = 1; i <= n; ++i) { five[i] = five[i - 1] * 5; four[i] = four[i - 1] * 4; }  // 거듭제곱을 채울 단계 순서대로 확인; 단계별 5의 거듭제곱 / 단계별 1 개수 갱신
//     return (int)(prefix(n, r, five, four) - prefix(n, l - 1, five, four));  // 단계별 5의 거듭제곱 / 단계별 1 개수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 비트열은 이전 단계 네 덩어리와 가운데 0 덩어리로 나뉨; 완전한 덩어리는 4의 거듭제곱으로 세고 남은 부분만 재귀 처리
// 예: n=2의 [4,17]은 8개.; 비트열을 직접 만들지 않으며 시간·재귀 공간 O(n)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:14:27
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/031_148652_%EC%9C%A0%EC%82%AC_%EC%B9%B8%ED%86%A0%EC%96%B4_%EB%B9%84%ED%8A%B8%EC%97%B4/README.md)
