#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int n) {
    int answer = 0;
    for (int divisor = 1; divisor <= n; ++divisor) if (n % divisor == 0) answer += divisor;
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
// int solution(int n) {  // 1부터 n까지 검사해 n을 나누어떨어지게 하는 수를 더하기
//     int answer = 0;  // 약수의 합 저장
//     for (int divisor = 1; divisor <= n; ++divisor) if (n % divisor == 0) answer += divisor;  // 1부터 n까지 나눠 보고 나머지가 0인 약수만 합에 추가
//     return answer;  // 약수의 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 1부터 n까지 검사해 n을 나누어떨어지게 하는 수를 더하기
