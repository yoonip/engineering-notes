# n + 1 카드게임

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/258707) · Level 3 · C

## 풀이

각 카드의 짝은 n+1-card로 유일하므로 서로 다른 쌍은 카드를 공유하지 않음; 완성된 쌍을 구매 비용 0·1·2로 분류해 매 라운드 가장 싼 쌍부터 쓰기
이미 뽑힌 카드의 구매 비용은 실제 쌍을 쓸 때 계산해도 됨; 최종 선택한 카드들을 처음 뽑을 때 샀다고 생각하면 같은 총비용 안의 유효한 전략; 시간·공간 O(N)
예: 초기 두 카드의 쌍을 먼저 사용하면 동전을 아껴 나중에 나온 카드로 추가 라운드를 진행할 수 있음; 카드를 모두 써도 다음 종료 라운드 번호까지 세기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int coin, int cards[], size_t cards_len) {
    int n = (int)cards_len, target = n + 1; bool* initial = calloc((size_t)n + 1, sizeof(*initial)); bool* drawn = calloc((size_t)n + 1, sizeof(*drawn)); int available[3] = {0}, round = 1;
    for (int i = 0; i < n / 3; ++i) initial[cards[i]] = true;
    for (int card = 1; card < target - card; ++card) available[0] += initial[card] && initial[target - card];
    for (int index = n / 3; index < n; index += 2) {
        for (int j = index; j < index + 2 && j < n; ++j) { int card = cards[j], partner = target - card; if (initial[partner]) ++available[1]; else if (drawn[partner]) ++available[2]; drawn[card] = true; }
        bool success = false;
        for (int price = 0; price < 3; ++price) if (available[price] && coin >= price) { --available[price]; coin -= price; ++round; success = true; break; }
        if (!success) break;
    }
    free(initial); free(drawn);
    return round;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int coin, int cards[], size_t cards_len) {  // 각 카드의 짝은 n+1-card로 유일하므로 서로 다른 쌍은 카드를 공유하지 않음; 완성된 쌍을 구매 비용 0·1·2로 분류해 매 라운드 가장 싼 쌍부터 쓰기
//     int n = (int)cards_len, target = n + 1; bool* initial = calloc((size_t)n + 1, sizeof(*initial)); bool* drawn = calloc((size_t)n + 1, sizeof(*drawn)); int available[3] = {0}, round = 1;  // 전체 카드 수 / 한 쌍의 목표 합 / 처음 공짜로 받은 카드 표시 / 라운드에서 꺼내 본 카드 표시 공간 확보하고 0으로 시작
//     for (int i = 0; i < n / 3; ++i) initial[cards[i]] = true;  // 초기 카드 위치 순서대로 확인; 처음 공짜로 받은 카드 표시 / 초기 카드 위치 확인
//     for (int card = 1; card < target - card; ++card) available[0] += initial[card] && initial[target - card];  // 새로 뽑은 카드 순서대로 확인; 0 1 2동전으로 만들 수 있는 쌍 수 / 처음 공짜로 받은 카드 표시 / 새로 뽑은 카드 더해 누적
//     for (int index = n / 3; index < n; index += 2) {  // 이번에 뽑을 카드 시작 순서대로 확인
//         for (int j = index; j < index + 2 && j < n; ++j) { int card = cards[j], partner = target - card; if (initial[partner]) ++available[1]; else if (drawn[partner]) ++available[2]; drawn[card] = true; }  // 이번 라운드의 카드 위치 순서대로 확인; 새로 뽑은 카드 / 목표 합을 만드는 반대 카드 / 라운드에서 꺼내 본 카드 표시 저장
//         bool success = false;  // 이번 라운드에 낼 쌍을 찾았는지 여부 저장
//         for (int price = 0; price < 3; ++price) if (available[price] && coin >= price) { --available[price]; coin -= price; ++round; success = true; break; }  // 만들 수 있는 쌍 중 동전 비용이 가장 작은 쌍부터 소비하고 다음 라운드 진행
//         if (!success) break;  // 이번 라운드에 낼 쌍을 찾았는지 여부가 없으면 이번 후보 확인을 끝내기
//     }  // 이 범위 끝
//     free(initial); free(drawn);  // 처음 공짜로 받은 카드 표시 / 라운드에서 꺼내 본 카드 표시 임시 공간 정리
//     return round;  // 현재까지 진행한 라운드 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 카드의 짝은 n+1-card로 유일하므로 서로 다른 쌍은 카드를 공유하지 않음; 완성된 쌍을 구매 비용 0·1·2로 분류해 매 라운드 가장 싼 쌍부터 쓰기
// 이미 뽑힌 카드의 구매 비용은 실제 쌍을 쓸 때 계산해도 됨; 최종 선택한 카드들을 처음 뽑을 때 샀다고 생각하면 같은 총비용 안의 유효한 전략; 시간·공간 O(N)
// 예: 초기 두 카드의 쌍을 먼저 사용하면 동전을 아껴 나중에 나온 카드로 추가 라운드를 진행할 수 있음; 카드를 모두 써도 다음 종료 라운드 번호까지 세기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/012_258707_n_%2B_1_%EC%B9%B4%EB%93%9C%EA%B2%8C%EC%9E%84/README.md)
