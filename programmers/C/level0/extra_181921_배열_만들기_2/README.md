# 배열 만들기 2

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181921) · Level 0 · C

## 풀이

범위 안의 각 수를 자릿수별로 검사해 0과 5로만 이루어진 수를 남기고, 없으면 -1을 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>

int* solution(int l, int r) {
    int* answer = malloc((r - l + 1) * sizeof(int));
    int used = 0;
    for (int value = l; value <= r; ++value) {
        int rest = value, valid = 1;
        while (rest) {
            int digit = rest % 10;
            if (digit != 0 && digit != 5) { valid = 0; break; }
            rest /= 10;
        }
        if (valid) answer[used++] = value;
    }
    if (!used) answer[used++] = -1;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
//
// int* solution(int l, int r) {  // 배열 만들기 2 풀이 시작
//     int* answer = malloc((r - l + 1) * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     int used = 0;  // 0과 5만으로 이루어져 결과에 넣은 정수 개수를 0으로 시작
//     for (int value = l; value <= r; ++value) {  // for로 l부터 r까지 양 끝을 포함하는 모든 정수를 검사
//         int rest = value, valid = 1;  // 검사할 수를 복사하고 모든 자릿수가 유효하다는 표시를 1로 초기화
//         while (rest) {  // 남은 수가 0이 아닐 동안 while로 자릿수 검사를 반복
//             int digit = rest % 10;  // 나머지 연산자 %로 현재 수의 마지막 자릿수를 구하기
//             if (digit != 0 && digit != 5) { valid = 0; break; }  // !=와 &&로 0과 5가 아닌 자릿수를 확인하면 실패 표시를 남기고 break로 검사를 끝
//             rest /= 10;  // 정수 나눗셈의 복합 대입 /=로 검사한 마지막 자릿수를 제거
//         }  // 블록 끝
//         if (valid) answer[used++] = value;  // if로 모든 자릿수가 유효한지 확인하고 결과에 넣은 뒤 저장 개수를 늘림
//     }  // 블록 끝
//     if (!used) answer[used++] = -1;  // !로 결과가 비었는지 검사하고 해당하면 -1을 첫 원소로 넣기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝// 풀이 요약
// 범위 안의 각 수를 자릿수별로 검사해 0과 5로만 이루어진 수를 남기고, 없으면 -1을 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:43:43
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181921_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_2/README.md)
