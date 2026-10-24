#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int search(unsigned full, unsigned columns, unsigned left, unsigned right) {
    if (columns == full) return 1;
    unsigned available = full & ~(columns | left | right);
    int count = 0;
    while (available) {
        unsigned position = available & (0u - available);
        available -= position;
        count += search(full, columns | position, (left | position) << 1, (right | position) >> 1);
    }
    return count;
}
int solution(int n) { return search((1u << n) - 1, 0, 0, 0); }

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static int search(unsigned full, unsigned columns, unsigned left, unsigned right) {  // 놓아야 할 전체 열 비트 / 퀸을 놓은 열 / 왼쪽 대각선 공격 위치 / 오른쪽 대각선 공격 위치 계산용 함수
//     if (columns == full) return 1;  // 모든 열에 퀸을 놓았으면 가능한 배치 한 개
//     unsigned available = full & ~(columns | left | right);  // 이번 행에서 가능한 열 저장
//     int count = 0;  // 조건에 맞는 배치 수 저장
//     while (available) {  // 이번 행에서 가능한 열가 남아 있으면 반복
//         unsigned position = available & (0u - available);  // 이번에 선택할 한 열 저장
//         available -= position;  // 이번 행에서 가능한 열 / 이번에 선택할 한 열에서 이번 사용량 빼기
//         count += search(full, columns | position, (left | position) << 1, (right | position) >> 1);  // 선택한 열과 두 대각선을 막고 다음 행에서 가능한 배치 수 더하기
//     }  // 이 범위 끝
//     return count;  // 조건에 맞는 배치 수 반환
// }  // 이 범위 끝
// int solution(int n) { return search((1u << n) - 1, 0, 0, 0); }  // 행마다 퀸을 하나 놓으며 사용한 열·두 대각선을 비트마스크로 관리하기; 공격받지 않는 열을 모두 시도하는 백트래킹

// 풀이 요약
// 행마다 퀸을 하나 놓으며 사용한 열·두 대각선을 비트마스크로 관리하기; 공격받지 않는 열을 모두 시도하는 백트래킹
// 예: n=4는 [1,3,0,2]·[2,0,3,1] 열 배치 두 가지; 탐색 시간 상한 O(n!), 재귀 공간 O(n)
