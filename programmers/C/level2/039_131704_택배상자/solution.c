#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int order[], size_t order_len) {
    int* stack = malloc(order_len * sizeof(*stack)); size_t top = 0, answer = 0;
    for (size_t box = 1; box <= order_len; ++box) {
        stack[top++] = (int)box;
        while (top && answer < order_len && stack[top - 1] == order[answer]) { --top; ++answer; }
    }
    free(stack);
    return (int)answer;
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
// int solution(int order[], size_t order_len) {  // 상자를 순서대로 스택에 넣고, 스택 위가 다음 요청이면 즉시 적재하기; 마지막 도착 뒤에도 못 꺼낸 상자는 적재 불가
//     int* stack = malloc(order_len * sizeof(*stack)); size_t top = 0, answer = 0;  // 보조 컨테이너 벨트 / 보조 벨트의 상자 수 / 지금까지 실은 상자 수 공간 확보
//     for (size_t box = 1; box <= order_len; ++box) {  // 주 벨트에서 들어오는 상자 번호 순서대로 확인
//         stack[top++] = (int)box;  // 보조 컨테이너 벨트 갱신
//         while (top && answer < order_len && stack[top - 1] == order[answer]) { --top; ++answer; }  // 보조 벨트 맨 위가 다음 배송 상자와 같으면 꺼내 싣기
//     }  // 이 범위 끝
//     free(stack);  // 보조 컨테이너 벨트 임시 공간 정리
//     return (int)answer;  // 지금까지 실은 상자 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 상자를 순서대로 스택에 넣고, 스택 위가 다음 요청이면 즉시 적재하기; 마지막 도착 뒤에도 못 꺼낸 상자는 적재 불가
// 예: [4,3,1,2,5]에서는 4·3만 적재해 2.; 각 상자는 한 번씩 들어가고 나오므로 시간·공간 O(N)
