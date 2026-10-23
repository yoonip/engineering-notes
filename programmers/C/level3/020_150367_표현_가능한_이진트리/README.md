# 표현 가능한 이진트리

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150367) · Level 3 · C

## 풀이

이진 문자열을 노드 수 1·3·7·15...에 맞춰 왼쪽에 0을 채우기; 중위 순회이므로 각 부분 문자열의 가운데가 루트
루트가 0이면 그 부분 트리 전체에 1이 없어야 하기; 루트가 1이면 왼쪽·오른쪽을 같은 규칙으로 확인; 문자열 길이 L에 대해 슬라이스를 포함한 시간 O(L log L), 추가 공간 O(L)
예: 5는 101이고 가운데 루트가 0인데 실제 자식 1이 있으므로 불가.; 42는 0101010이고 루트 1 아래의 각 부분 트리도 유효하므로 가능

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static bool valid(const char* bits, int length) {
    if (length == 1) return true;
    int middle = length / 2;
    if (bits[middle] == '0') { for (int i = 0; i < length; ++i) if (bits[i] == '1') return false; return true; }
    return valid(bits, middle) && valid(bits + middle + 1, middle);
}
int* solution(long long numbers[], size_t numbers_len) {
    int* answer = malloc(numbers_len * sizeof(*answer));
    for (size_t i = 0; i < numbers_len; ++i) {
        unsigned long long value = (unsigned long long)numbers[i]; int used = 0;
        for (unsigned long long n = value; n; n >>= 1) ++used;
        int size = 1; while (size < used) size = size * 2 + 1;
        char bits[128]; memset(bits, '0', (size_t)size);
        for (int j = size - 1; value; --j) { bits[j] = '0' + (value & 1u); value >>= 1; }
        answer[i] = valid(bits, size);
    }
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
// static bool valid(const char* bits, int length) {  // 조건을 모두 지키는 구조인지 확인
//     if (length == 1) return true;  // 현재 서브트리 비트 길이가 1이면 끝까지 조건을 지켰으니 성공
//     int middle = length / 2;  // 현재 서브트리의 루트 위치 저장
//     if (bits[middle] == '0') { for (int i = 0; i < length; ++i) if (bits[i] == '1') return false; return true; }  // 서브트리 루트가 0이면 아래 비트도 모두 0이어야 표현 가능
//     return valid(bits, middle) && valid(bits + middle + 1, middle);  // 빈 노드를 0으로 채운 포화 이진트리 표현 / 현재 서브트리의 루트 위치로 최종값 계산
// }  // 이 범위 끝
// int* solution(long long numbers[], size_t numbers_len) {  // 이진 문자열을 노드 수 1·3·7·15...에 맞춰 왼쪽에 0을 채우기; 중위 순회이므로 각 부분 문자열의 가운데가 루트
//     int* answer = malloc(numbers_len * sizeof(*answer));  // 숫자별 유효한 이진트리 여부 공간 확보
//     for (size_t i = 0; i < numbers_len; ++i) {  // 정수 입력 위치 순서대로 확인
//         unsigned long long value = (unsigned long long)numbers[i]; int used = 0;  // 아직 꺼내지 않은 정수 비트 / 숫자의 이진수 길이 저장
//         for (unsigned long long n = value; n; n >>= 1) ++used;  // 이진수 길이를 셀 사본 순서대로 확인; 숫자의 이진수 길이 갱신
//         int size = 1; while (size < used) size = size * 2 + 1;  // 포화 이진트리에 필요한 노드 수 저장
//         char bits[128]; memset(bits, '0', (size_t)size);  // 빈 노드를 0으로 채운 포화 이진트리 표현 / 포화 이진트리에 필요한 노드 수 초기화
//         for (int j = size - 1; value; --j) { bits[j] = '0' + (value & 1u); value >>= 1; }  // 오른쪽부터 채울 비트 위치 순서대로 확인; 빈 노드를 0으로 채운 포화 이진트리 표현 갱신
//         answer[i] = valid(bits, size);  // 숫자별 유효한 이진트리 여부 갱신
//     }  // 이 범위 끝
//     return answer;  // 숫자별 유효한 이진트리 여부 반환
// }  // 이 범위 끝

// 풀이 요약
// 이진 문자열을 노드 수 1·3·7·15...에 맞춰 왼쪽에 0을 채우기; 중위 순회이므로 각 부분 문자열의 가운데가 루트
// 루트가 0이면 그 부분 트리 전체에 1이 없어야 하기; 루트가 1이면 왼쪽·오른쪽을 같은 규칙으로 확인; 문자열 길이 L에 대해 슬라이스를 포함한 시간 O(L log L), 추가 공간 O(L)
// 예: 5는 101이고 가운데 루트가 0인데 실제 자식 1이 있으므로 불가.; 42는 0101010이고 루트 1 아래의 각 부분 트리도 유효하므로 가능
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/020_150367_%ED%91%9C%ED%98%84_%EA%B0%80%EB%8A%A5%ED%95%9C_%EC%9D%B4%EC%A7%84%ED%8A%B8%EB%A6%AC/README.md)
