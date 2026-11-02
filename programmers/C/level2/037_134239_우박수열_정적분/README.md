# 우박수열 정적분

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/134239) · Level 2 · C

우박수열의 인접 점 사이 사다리꼴 넓이를 누적합니다. 각 구간의 넓이는 끝 누적값에서 시작 누적값을 빼서 구합니다.

예: 5로 시작하는 수열 전체의 넓이는 33.0입니다. 구간 [3,-3]은 시작 3이 끝 2보다 커서 -1.0입니다. 수열 길이 L·질문 Q개에 대해 시간·결과 포함 공간은 O(L+Q)입니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

double* solution(int k, int** ranges, size_t ranges_rows, size_t ranges_cols) {
    (void)ranges_cols;
    size_t cap = 128, n = 0; double* prefix = malloc(cap * sizeof(*prefix)); prefix[0] = 0;
    long long value = k;
    while (value > 1) {
        long long next = value % 2 ? 3 * value + 1 : value / 2;
        if (n + 1 == cap) { cap *= 2; prefix = realloc(prefix, cap * sizeof(*prefix)); }
        prefix[n + 1] = prefix[n] + (value + next) / 2.0; ++n; value = next;
    }
    double* answer = malloc(ranges_rows * sizeof(*answer));
    for (size_t i = 0; i < ranges_rows; ++i) {
        int start = ranges[i][0], end = (int)n + ranges[i][1];
        answer[i] = start <= end ? prefix[end] - prefix[start] : -1.0;
    }
    free(prefix);
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
// double* solution(int k, int** ranges, size_t ranges_rows, size_t ranges_cols) {  // 우박수열의 인접 점 사이 사다리꼴 넓이를 누적합니다. 각 구간의 넓이는 끝 누적값에서 시작 누적값을 빼서 구합니다.
//     (void)ranges_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     size_t cap = 128, n = 0; double* prefix = malloc(cap * sizeof(*prefix)); prefix[0] = 0;  // 정적분 누적 배열 용량 / 우박 수열 구간 수 / 구간별 사다리꼴 넓이 누적합 공간 확보
//     long long value = k;  // 현재 우박 수열 값 저장
//     while (value > 1) {  // 현재 우박 수열 값이 1보다 크면 반복
//         long long next = value % 2 ? 3 * value + 1 : value / 2;  // 다음 우박 수열 값 저장
//         if (n + 1 == cap) { cap *= 2; prefix = realloc(prefix, cap * sizeof(*prefix)); }  // realloc으로 배열 용량을 늘리고 기존 누적값을 보존하기
//         prefix[n + 1] = prefix[n] + (value + next) / 2.0; ++n; value = next;  // 인접 두 우박수 사이 사다리꼴 넓이를 누적하고 다음 항으로 이동
//     }  // 이 범위 끝
//     double* answer = malloc(ranges_rows * sizeof(*answer));  // 질의별 정적분 값 공간 확보
//     for (size_t i = 0; i < ranges_rows; ++i) {  // 적분 범위 번호 순서대로 확인
//         int start = ranges[i][0], end = (int)n + ranges[i][1];  // 적분 시작 위치 / 마지막 위치 기준 오프셋을 적용한 끝 저장
//         answer[i] = start <= end ? prefix[end] - prefix[start] : -1.0;  // 질의별 정적분 값 갱신
//     }  // 이 범위 끝
//     free(prefix);  // 구간별 사다리꼴 넓이 누적합 임시 공간 정리
//     return answer;  // 질의별 정적분 값 반환
// }  // 이 범위 끝

// 풀이 요약
// 우박수열의 인접 점 사이 사다리꼴 넓이를 누적합니다. 각 구간의 넓이는 끝 누적값에서 시작 누적값을 빼서 구합니다.
// 예: 5로 시작하는 수열 전체의 넓이는 33.0입니다. 구간 [3,-3]은 시작 3이 끝 2보다 커서 -1.0입니다. 수열 길이 L·질문 Q개에 대해 시간·결과 포함 공간은 O(L+Q)입니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:16:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/037_134239_%EC%9A%B0%EB%B0%95%EC%88%98%EC%97%B4_%EC%A0%95%EC%A0%81%EB%B6%84/README.md)
