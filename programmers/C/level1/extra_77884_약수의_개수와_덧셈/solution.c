#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int left, int right) {
    int answer = 0;
    for (int n = left; n <= right; ++n) { int root = (int)sqrt((double)n); answer += root * root == n ? -n : n; }
    return answer;
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
// int solution(int left, int right) {  // 완전제곱수의 약수 개수만 홀수; 구간의 수 중 완전제곱수는 빼고 나머지는 더하기
//     int answer = 0;  // 약수 개수의 짝홀에 따른 합 저장
//     for (int n = left; n <= right; ++n) { int root = (int)sqrt((double)n); answer += root * root == n ? -n : n; }  // 현재 구간의 정수 순서대로 확인; 현재 수의 정수 제곱근 저장
//     return answer;  // 약수 개수의 짝홀에 따른 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 완전제곱수의 약수 개수만 홀수; 구간의 수 중 완전제곱수는 빼고 나머지는 더하기
