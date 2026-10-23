# 전국 대회 선발 고사

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181851) · Level 0 · C

## 풀이

참석 가능한 학생을 순회하면서 selected에 등수가 작은 세 학생의 번호를 순서대로 유지. 새 후보가 들어갈 자리를 찾으면 뒤의 번호를 밀어 넣고, 최종 세 번호를 10000a + 100b + c로 조합

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int rank[], size_t rank_len, bool attendance[], size_t attendance_len) {
    int selected[3] = {-1, -1, -1};
    for (size_t i = 0; i < rank_len; ++i) if (attendance[i]) {
        for (int j = 0; j < 3; ++j) if (selected[j] < 0 || rank[i] < rank[selected[j]]) {
            for (int q = 2; q > j; --q) selected[q] = selected[q - 1];
            selected[j] = (int)i;
            break;
        }
    }
    return 10000 * selected[0] + 100 * selected[1] + selected[2];
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int rank[], size_t rank_len, bool attendance[], size_t attendance_len) {  // 전국 대회 선발 고사 풀이 시작
//     int selected[3] = {-1, -1, -1};  // 등수순으로 선발할 학생 번호 세 개를 담는 selected를 미선발 표시 -1로 초기화
//     for (size_t i = 0; i < rank_len; ++i) if (attendance[i]) {  // 학생 번호 i를 순회하되 attendance[i]가 참인 참석 가능 학생만 선발 후보로 처리
//         for (int j = 0; j < 3; ++j) if (selected[j] < 0 || rank[i] < rank[selected[j]]) {  // 상위 세 자리 j를 살피며 빈자리이거나 현재 학생의 등수가 더 작은 첫 위치를 찾기
//             for (int q = 2; q > j; --q) selected[q] = selected[q - 1];  // 뒤쪽 자리부터 오른쪽으로 한 칸씩 옮겨 현재 학생을 등수순으로 끼워 넣을 자리를 만들기
//             selected[j] = (int)i;  // 현재 학생의 배열 인덱스 i를 학생 번호로 변환하여 선발 위치 j에 저장
//             break;  // 한 학생을 한 자리만 차지하게 하려고 선발 위치를 찾는 안쪽 반복문을 끝
//         }  // 블록 끝
//     }  // 블록 끝
//     return 10000 * selected[0] + 100 * selected[1] + selected[2];  // 등수가 높은 세 학생 번호를 a, b, c 순서로 10000a + 100b + c에 대입해 반환
// }  // 블록 끝

// 풀이 요약
// 참석 가능한 학생을 순회하면서 selected에 등수가 작은 세 학생의 번호를 순서대로 유지. 새 후보가 들어갈 자리를 찾으면 뒤의 번호를 밀어 넣고, 최종 세 번호를 10000a + 100b + c로 조합
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:19:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181851_%EC%A0%84%EA%B5%AD_%EB%8C%80%ED%9A%8C_%EC%84%A0%EB%B0%9C_%EA%B3%A0%EC%82%AC/README.md)
