# 도넛과 막대 그래프

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/258711) · Level 2 · C

## 풀이

진입·진출 차수로 추가 정점, 막대의 끝, 8자의 중심을 센 뒤 나머지를 도넛으로 계산
예: 첫 예제는 추가 정점 2의 진출 2개에서 막대 1개를 빼 [2,1,1,0].; 시간 O(E+M), 공간 O(M), M은 최대 정점 번호

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

int* solution(int** edges, size_t edges_rows, size_t edges_cols) {
    (void)edges_cols;
    int size = 0;
    for (size_t i = 0; i < edges_rows; ++i) for (int j = 0; j < 2; ++j) if (edges[i][j] > size) size = edges[i][j];
    int* incoming = calloc((size_t)size + 1, sizeof(*incoming)); int* outgoing = calloc((size_t)size + 1, sizeof(*outgoing));
    for (size_t i = 0; i < edges_rows; ++i) { ++outgoing[edges[i][0]]; ++incoming[edges[i][1]]; }
    int* answer = calloc(4, sizeof(*answer));
    for (int node = 1; node <= size; ++node) {
        if (!incoming[node] && outgoing[node] >= 2) answer[0] = node;
        else if (!outgoing[node] && incoming[node]) ++answer[2];
        else if (outgoing[node] == 2 && incoming[node] >= 2) ++answer[3];
    }
    answer[1] = outgoing[answer[0]] - answer[2] - answer[3]; free(incoming); free(outgoing);
    return answer;
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
// int* solution(int** edges, size_t edges_rows, size_t edges_cols) {  // 진입·진출 차수로 추가 정점, 막대의 끝, 8자의 중심을 센 뒤 나머지를 도넛으로 계산
//     (void)edges_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int size = 0;  // 가장 큰 정점 번호 저장
//     for (size_t i = 0; i < edges_rows; ++i) for (int j = 0; j < 2; ++j) if (edges[i][j] > size) size = edges[i][j];  // 간선 번호 순서대로 확인; 간선의 시작 또는 끝 위치 갱신
//     int* incoming = calloc((size_t)size + 1, sizeof(*incoming)); int* outgoing = calloc((size_t)size + 1, sizeof(*outgoing));  // 정점별 진입 차수 / 정점별 진출 차수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < edges_rows; ++i) { ++outgoing[edges[i][0]]; ++incoming[edges[i][1]]; }  // 간선 번호 순서대로 확인; 정점별 진출 차수 / 정점별 진입 차수 갱신
//     int* answer = calloc(4, sizeof(*answer));  // 추가 정점 도넛 막대 8자 개수 공간 확보하고 0으로 시작
//     for (int node = 1; node <= size; ++node) {  // 차수로 분류할 정점 순서대로 확인
//         if (!incoming[node] && outgoing[node] >= 2) answer[0] = node;  // 들어오는 간선이 없고 나가는 간선이 2개 이상인 정점을 생성 정점으로 선택
//         else if (!outgoing[node] && incoming[node]) ++answer[2];  // 나가는 간선이 없는 도착점 하나당 막대 그래프 하나
//         else if (outgoing[node] == 2 && incoming[node] >= 2) ++answer[3];  // 진출 차수가 2이고 진입이 2 이상인 교차점 하나당 8자 그래프 하나
//     }  // 이 범위 끝
//     answer[1] = outgoing[answer[0]] - answer[2] - answer[3]; free(incoming); free(outgoing);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 추가 정점 도넛 막대 8자 개수 반환
// }  // 이 범위 끝

// 풀이 요약
// 진입·진출 차수로 추가 정점, 막대의 끝, 8자의 중심을 센 뒤 나머지를 도넛으로 계산
// 예: 첫 예제는 추가 정점 2의 진출 2개에서 막대 1개를 빼 [2,1,1,0].; 시간 O(E+M), 공간 O(M), M은 최대 정점 번호
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:09:04
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/011_258711_%EB%8F%84%EB%84%9B%EA%B3%BC_%EB%A7%89%EB%8C%80_%EA%B7%B8%EB%9E%98%ED%94%84/README.md)
