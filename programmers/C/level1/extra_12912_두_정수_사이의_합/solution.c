#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

long long solution(int a, int b) {
    long long start = a < b ? a : b, end = a > b ? a : b;
    return (start + end) * (end - start + 1) / 2;
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
// long long solution(int a, int b) {  // 두 끝값 중 작은 값과 큰 값을 구한 뒤 등차수열의 합 공식을 적용합니다. 중간 곱셈부터 long long으로 계산합니다.
//     long long start = a < b ? a : b, end = a > b ? a : b;  // 두 수 중 작은 끝점 / 두 수 중 큰 끝점 저장
//     return (start + end) * (end - start + 1) / 2;  // 양 끝값의 합에 정수 개수를 곱하고 2로 나누어 등차수열의 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 두 끝값 중 작은 값과 큰 값을 구한 뒤 등차수열의 합 공식을 적용합니다. 중간 곱셈부터 long long으로 계산합니다.
