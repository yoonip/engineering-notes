#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    int n, m; if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int row = 0; row < m; ++row) { for (int col = 0; col < n; ++col) putchar('*'); putchar('\n'); }
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int main(void) {  // 한 줄에 별 n개와 줄바꿈을 출력하는 작업을 m번 반복합니다.
//     int n, m; if (scanf("%d %d", &n, &m) != 2) return 0;  // scanf로 정수 두 개를 읽고, 두 값 모두 읽지 못했으면 출력 없이 종료
//     for (int row = 0; row < m; ++row) { for (int col = 0; col < n; ++col) putchar('*'); putchar('\n'); }  // 출력 중인 행 순서대로 확인; 별을 한 줄 채우고 줄바꿈
//     return 0;  // 별 출력을 정상적으로 마치고 프로그램 종료
// }  // 이 범위 끝

// 풀이 요약
// 한 줄에 별 n개와 줄바꿈을 출력하는 작업을 m번 반복합니다.
