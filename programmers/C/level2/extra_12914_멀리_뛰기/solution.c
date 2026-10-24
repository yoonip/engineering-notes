#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

long long solution(int n) {
    int previous = 1, current = 1;
    for (int i = 2; i <= n; ++i) {
        int next = (previous + current) % 1234567;
        previous = current; current = next;
    }
    return current;
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
// long long solution(int n) {  // 마지막에 1칸 뛰면 n-1칸까지의 모든 방법, 2칸 뛰면 n-2칸까지의 모든 방법이 있음; 두 경우는 겹치지 않아 더하기
//     int previous = 1, current = 1;  // 두 칸 전까지의 이동 방법 수 / 한 칸 전까지의 이동 방법 수 저장
//     for (int i = 2; i <= n; ++i) {  // 채울 이동 거리 순서대로 확인
//         int next = (previous + current) % 1234567;  // 이번 거리의 이동 방법 수 저장
//         previous = current; current = next;  // 두 칸 전까지의 이동 방법 수 / 한 칸 전까지의 이동 방법 수 갱신
//     }  // 이 범위 끝
//     return current;  // 한 칸 전까지의 이동 방법 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 마지막에 1칸 뛰면 n-1칸까지의 모든 방법, 2칸 뛰면 n-2칸까지의 모든 방법이 있음; 두 경우는 겹치지 않아 더하기
// 예: f(2)=2,f(3)=3,f(4)=5; 이전 두 값만 보관하므로 시간 O(N), 공간 O(1)
