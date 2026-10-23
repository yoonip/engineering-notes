#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int n) {
    int answer = 0;
    while (n > 0) { answer = answer * 3 + n % 3; n /= 3; }
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
// int solution(int n) {  // 3으로 나눈 나머지를 차례로 읽기; 누적 값에 3을 곱하고 다음 나머지를 더하면 뒤집은 삼진수를 십진수로 계산할 수 있음
//     int answer = 0;  // 뒤집은 3진수를 십진수로 누적한 값 저장
//     while (n > 0) { answer = answer * 3 + n % 3; n /= 3; }  // 아직 읽지 않은 3진수 자리가 0보다 크면 반복; 뒤집은 3진수를 십진수로 누적한 값 갱신
//     return answer;  // 뒤집은 3진수를 십진수로 누적한 값 반환
// }  // 이 범위 끝

// 풀이 요약
// 3으로 나눈 나머지를 차례로 읽기; 누적 값에 3을 곱하고 다음 나머지를 더하면 뒤집은 삼진수를 십진수로 계산할 수 있음
