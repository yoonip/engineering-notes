#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(const char* s) {
    int n = (int)strlen(s), answer = 1;
    for (int center = 0; center < 2 * n - 1; ++center) {
        int left = center / 2, right = left + center % 2;
        while (left >= 0 && right < n && s[left] == s[right]) { --left; ++right; }
        if (right - left - 1 > answer) answer = right - left - 1;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(const char* s) {  // 팰린드롬은 중심에서 좌우가 대칭; 홀수 길이는 한 글자, 짝수 길이는 두 글자 사이를 중심으로 같은 글자 쌍이 이어지는 만큼 확장하기
//     int n = (int)strlen(s), answer = 1;  // 문자열 길이 / 가장 긴 팰린드롬 길이 저장
//     for (int center = 0; center < 2 * n - 1; ++center) {  // 홀수와 짝수 팰린드롬의 중심 순서대로 확인
//         int left = center / 2, right = left + center % 2;  // 확장할 왼쪽 끝 / 확장할 오른쪽 끝 저장
//         while (left >= 0 && right < n && s[left] == s[right]) { --left; ++right; }  // 문자열 범위 안에서 양쪽 글자가 같은 동안 팰린드롬 확장
//         if (right - left - 1 > answer) answer = right - left - 1;  // 양끝 불일치 직전까지의 길이가 더 길면 최장 길이 갱신
//     }  // 이 범위 끝
//     return answer;  // 가장 긴 팰린드롬 길이 반환
// }  // 이 범위 끝

// 풀이 요약
// 팰린드롬은 중심에서 좌우가 대칭; 홀수 길이는 한 글자, 짝수 길이는 두 글자 사이를 중심으로 같은 글자 쌍이 이어지는 만큼 확장하기
// 예: abacde에서 b를 중심으로 a·a까지 확장하면 aba의 길이 3.; abba 같은 짝수 길이도 사이 중심으로 잡아야 찾을 수 있음
// 시간 O(N²).; 중심 확장 자체는 추가 공간 O(1), 전체 문자열 역순 확인을 포함한 최대 추가 공간은 O(N)
