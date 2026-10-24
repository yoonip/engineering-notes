#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

long long solution(int w, int h) {
    int a = w, b = h;
    while (b) { int r = a % b; a = b; b = r; }
    return (long long)w * h - ((long long)w + h - a);
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
// long long solution(int w, int h) {  // 대각선은 가로·세로 격자선을 지날 때 새 칸에 진입하기; 공통 격자점에서는 두 번 세므로 최대공약수만큼 보정해 잘린 칸은 w+h-gcd(w,h)
//     int a = w, b = h;  // 가로세로 길이의 최대공약수 후보 / 호제법의 두 번째 값 저장
//     while (b) { int r = a % b; a = b; b = r; }  // 호제법의 두 번째 값가 남아 있으면 반복; 호제법 나머지 / 가로세로 길이의 최대공약수 후보 / 호제법의 두 번째 값 저장
//     return (long long)w * h - ((long long)w + h - a);  // 가로세로 길이의 최대공약수 후보로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 대각선은 가로·세로 격자선을 지날 때 새 칸에 진입하기; 공통 격자점에서는 두 번 세므로 최대공약수만큼 보정해 잘린 칸은 w+h-gcd(w,h)
// 예: 8×12에서 잘린 칸은 8+12-4=16, 남는 칸은 80; 시간 O(log min(w,h)), 공간 O(1)
