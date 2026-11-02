# 스킬트리

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/49993) · Level 2 · C

선행 순서에 없는 스킬은 건너뛰고, 나머지가 skill의 앞부분과 일치하는지 확인합니다. 별도 문자열을 만들지는 않습니다.

예: skill=CBD에서 CBADF의 관련 스킬은 CBD, AECB는 CB이므로 둘 다 가능합니다. 입력 문자열 길이 합 L, 선행 스킬 길이 S에 대해 strchr 검색을 포함한 시간은 O(LS), 추가 공간은 O(1)입니다. 이 문제에서는 S가 알파벳 수로 제한됩니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(const char* skill, const char* skill_trees[], size_t skill_trees_len) {
    int answer = 0;
    for (size_t i = 0; i < skill_trees_len; ++i) {
        size_t index = 0; bool valid = true;
        for (size_t j = 0; skill_trees[i][j]; ++j) {
            char c = skill_trees[i][j];
            if (strchr(skill, c) == NULL) continue;
            if (skill[index] != c) { valid = false; break; }
            ++index;
        }
        answer += valid;
    }
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
// int solution(const char* skill, const char* skill_trees[], size_t skill_trees_len) {  // 선행 순서에 없는 스킬은 건너뛰고, 나머지가 skill의 앞부분과 일치하는지 확인합니다. 별도 문자열을 만들지는 않습니다.
//     int answer = 0;  // 선행 순서를 지킨 스킬트리 수 저장
//     for (size_t i = 0; i < skill_trees_len; ++i) {  // 확인할 스킬트리 위치 순서대로 확인
//         size_t index = 0; bool valid = true;  // 다음에 나와야 할 선행 스킬 / 현재 트리의 유효 여부 저장
//         for (size_t j = 0; skill_trees[i][j]; ++j) {  // 현재 스킬 위치 순서대로 확인
//             char c = skill_trees[i][j];  // 현재 스킬 문자 저장
//             if (strchr(skill, c) == NULL) continue;  // 선행 순서에 없는 스킬은 자유롭게 배울 수 있으므로 무시
//             if (skill[index] != c) { valid = false; break; }  // 다음 필수 스킬이 아니면 선행 순서 위반이므로 제외
//             ++index;  // 다음에 나와야 할 선행 스킬 갱신
//         }  // 이 범위 끝
//         answer += valid;  // 선행 순서를 지킨 스킬트리 수 / 현재 트리의 유효 여부 더해 누적
//     }  // 이 범위 끝
//     return answer;  // 선행 순서를 지킨 스킬트리 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 선행 순서에 없는 스킬은 건너뛰고, 나머지가 skill의 앞부분과 일치하는지 확인합니다. 별도 문자열을 만들지는 않습니다.
// 예: skill=CBD에서 CBADF의 관련 스킬은 CBD, AECB는 CB이므로 둘 다 가능합니다. 입력 문자열 길이 합 L, 선행 스킬 길이 S에 대해 strchr 검색을 포함한 시간은 O(LS), 추가 공간은 O(1)입니다. 이 문제에서는 S가 알파벳 수로 제한됩니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:21:27
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/068_49993_%EC%8A%A4%ED%82%AC%ED%8A%B8%EB%A6%AC/README.md)
