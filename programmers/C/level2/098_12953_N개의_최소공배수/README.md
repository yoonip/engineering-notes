# N개의 최소공배수

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12953) · Level 2 · C

현재까지의 최소공배수와 다음 수의 최소공배수를 반복 계산합니다. 먼저 최대공약수로 나눈 뒤 곱해 불필요하게 큰 중간 곱을 줄입니다.

예: [2,6,8,14]는 2→6→24→168입니다. 중간 결과가 int 범위 안에 있다는 조건에서, 원소 N개·중간 최댓값 V에 대해 시간은 O(N log V), 공간은 O(1)입니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int gcd(int a, int b) {
    while (b) { int r = a % b; a = b; b = r; }
    return a;
}
int solution(int arr[], size_t arr_len) {
    int answer = 1;
    for (size_t i = 0; i < arr_len; ++i) answer = answer / gcd(answer, arr[i]) * arr[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // sqrtl 등 실수 수학 함수의 선언
//
// static int gcd(int a, int b) {  // 나머지를 반복해서 최대공약수 구하기
//     while (b) { int r = a % b; a = b; b = r; }  // 나머지가 0이 될 때까지 두 값을 바꿔 최대공약수 계산
//     return a;  // 나머지가 0이 된 시점의 최대공약수 반환
// }  // 이 범위 끝
// int solution(int arr[], size_t arr_len) {  // 현재까지의 최소공배수와 다음 수의 최소공배수를 반복 계산합니다. 먼저 최대공약수로 나눈 뒤 곱해 불필요하게 큰 중간 곱을 줄입니다.
//     int answer = 1;  // 지금까지 원소들의 최소공배수 저장
//     for (size_t i = 0; i < arr_len; ++i) answer = answer / gcd(answer, arr[i]) * arr[i];  // 최소공배수에 합칠 원소 위치 순서대로 확인; 지금까지 원소들의 최소공배수 갱신
//     return answer;  // 지금까지 원소들의 최소공배수 반환
// }  // 이 범위 끝

// 풀이 요약
// 현재까지의 최소공배수와 다음 수의 최소공배수를 반복 계산합니다. 먼저 최대공약수로 나눈 뒤 곱해 불필요하게 큰 중간 곱을 줄입니다.
// 예: [2,6,8,14]는 2→6→24→168입니다. 중간 결과가 int 범위 안에 있다는 조건에서, 원소 N개·중간 최댓값 V에 대해 시간은 O(N log V), 공간은 O(1)입니다.
```


이 C 구현은 계산 결과와 중간 최소공배수가 int 범위에 들어갈 때 적용됩니다. [공식 제한사항](https://school.programmers.co.kr/learn/courses/30/lessons/12953)은 배열 길이와 원소 범위만 제시하며 결과의 int 범위를 별도로 보장하지 않습니다. 예를 들어 [97,89,83,79,73]의 최소공배수는 4,132,280,413으로 32비트 signed int의 최댓값 2,147,483,647을 넘습니다. 아래 채점 기록은 당시 제출 결과이며, 모든 명시적 입력에서 정수 오버플로가 없다는 뜻은 아닙니다.

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/098_12953_N%EA%B0%9C%EC%9D%98_%EC%B5%9C%EC%86%8C%EA%B3%B5%EB%B0%B0%EC%88%98/README.md)
