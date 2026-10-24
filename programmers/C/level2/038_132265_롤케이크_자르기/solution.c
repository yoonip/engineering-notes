#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int topping[], size_t topping_len) {
    int maximum = 0;
    for (size_t i = 0; i < topping_len; ++i) if (topping[i] > maximum) maximum = topping[i];
    int* right = calloc((size_t)maximum + 1, sizeof(*right)); bool* left = calloc((size_t)maximum + 1, sizeof(*left));
    int left_kinds = 0, right_kinds = 0, answer = 0;
    for (size_t i = 0; i < topping_len; ++i) if (right[topping[i]]++ == 0) ++right_kinds;
    for (size_t i = 0; i < topping_len; ++i) {
        int value = topping[i];
        if (!left[value]) { left[value] = true; ++left_kinds; }
        if (--right[value] == 0) --right_kinds;
        answer += left_kinds == right_kinds;
    }
    free(right); free(left);
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
// int solution(int topping[], size_t topping_len) {  // 경계를 한 칸씩 옮기며 왼쪽은 등장 여부, 오른쪽은 개수 배열로 토핑 종류 수 관리; 두 종류 수가 같은 경계 세기
//     int maximum = 0;  // 토핑 번호 최댓값 저장
//     for (size_t i = 0; i < topping_len; ++i) if (topping[i] > maximum) maximum = topping[i];  // 토핑 번호의 최댓값을 찾아 개수 배열 범위 잡기
//     int* right = calloc((size_t)maximum + 1, sizeof(*right)); bool* left = calloc((size_t)maximum + 1, sizeof(*left));  // 오른쪽 조각의 토핑별 개수 / 왼쪽에서 본 토핑 여부 공간 확보하고 0으로 시작
//     int left_kinds = 0, right_kinds = 0, answer = 0;  // 왼쪽 토핑 종류 수 / 오른쪽 토핑 종류 수 / 양쪽 종류 수가 같은 절단 수 저장
//     for (size_t i = 0; i < topping_len; ++i) if (right[topping[i]]++ == 0) ++right_kinds;  // 오른쪽에서 처음 본 토핑일 때 종류 수 늘리기
//     for (size_t i = 0; i < topping_len; ++i) {  // 자르는 위치 순서대로 확인
//         int value = topping[i];  // 오른쪽에서 왼쪽으로 옮길 토핑 저장
//         if (!left[value]) { left[value] = true; ++left_kinds; }  // 왼쪽에 없던 토핑이면 방문 표시하고 종류 수 늘리기
//         if (--right[value] == 0) --right_kinds;  // 옮긴 뒤 오른쪽 개수가 0이 되면 오른쪽 종류 수 줄이기
//         answer += left_kinds == right_kinds;  // 양쪽 종류 수가 같은 절단 수 / 왼쪽 토핑 종류 수 / 오른쪽 토핑 종류 수 더해 누적
//     }  // 이 범위 끝
//     free(right); free(left);  // 오른쪽 조각의 토핑별 개수 / 왼쪽에서 본 토핑 여부 임시 공간 정리
//     return answer;  // 양쪽 종류 수가 같은 절단 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 경계를 한 칸씩 옮기며 왼쪽은 등장 여부, 오른쪽은 개수 배열로 토핑 종류 수 관리; 두 종류 수가 같은 경계 세기
// 예: 첫 예제는 네 번째·다섯 번째 토핑 뒤에서 잘라 2가지; 토핑 N개·종류 U개일 때 시간 O(N), 공간 O(U)
