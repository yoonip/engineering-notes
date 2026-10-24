#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int overlaps(int time) {
    return time * 719 / 43200 + time * 59 / 3600 - time / 43200 + 1;
}
int solution(int h1, int m1, int s1, int h2, int m2, int s2) {
    int start = h1 * 3600 + m1 * 60 + s1, end = h2 * 3600 + m2 * 60 + s2;
    bool at_start = start * 719 % 43200 == 0 || start * 59 % 3600 == 0;
    return overlaps(end) - overlaps(start) + at_start;
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
// static int overlaps(int time) {  // 자정부터 해당 시각까지 시계 바늘 겹침 횟수 계산
//     return time * 719 / 43200 + time * 59 / 3600 - time / 43200 + 1;  // 자정부터 지난 초 수로 최종값 계산
// }  // 이 범위 끝
// int solution(int h1, int m1, int s1, int h2, int m2, int s2) {  // 초침은 시침을 43200/719초마다, 분침을 3600/59초마다 추월하기; 세 바늘이 함께 겹치는 12시간마다 중복을 빼기
//     int start = h1 * 3600 + m1 * 60 + s1, end = h2 * 3600 + m2 * 60 + s2;  // 관찰 시작 시각 / 관찰 끝 시각 저장
//     bool at_start = start * 719 % 43200 == 0 || start * 59 % 3600 == 0;  // 시작 순간에 이미 겹쳐 있는지 여부 저장
//     return overlaps(end) - overlaps(start) + at_start;  // 관찰 끝 시각 / 관찰 시작 시각 / 시작 순간에 이미 겹쳐 있는지 여부로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 초침은 시침을 43200/719초마다, 분침을 3600/59초마다 추월하기; 세 바늘이 함께 겹치는 12시간마다 중복을 빼기
// 누적 횟수의 차이에 시작 순간의 알람을 포함하기; 예: 12:00:00~12:00:30은 1회; 시간·공간 O(1)
