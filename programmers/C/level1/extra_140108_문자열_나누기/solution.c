#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(const char* s) {
    int answer = 0, same = 0, different = 0; char first = 0;
    for (size_t i = 0; s[i]; ++i) {
        if (same == 0 && different == 0) first = s[i];
        if (s[i] == first) ++same; else ++different;
        if (same == different) { ++answer; same = different = 0; }
    }
    return answer + (same != 0 || different != 0);
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
// int solution(const char* s) {  // 첫 문자와 같은 문자 수와 다른 문자 수를 세기; 두 개수가 같아지는 즉시 분리하고 마지막 남은 부분도 한 묶음으로 세기
//     int answer = 0, same = 0, different = 0; char first = 0;  // 완성한 조각 수 / 조각 첫 문자와 같은 글자 수 / 조각 첫 문자와 다른 글자 수 / 현재 조각의 첫 문자 저장
//     for (size_t i = 0; s[i]; ++i) {  // 다음에 읽을 문자 위치 순서대로 확인
//         if (same == 0 && different == 0) first = s[i];  // 새 조각을 시작할 때 현재 문자를 기준 문자로 저장
//         if (s[i] == first) ++same; else ++different;  // 기준 문자와 같으면 same, 다르면 different 늘리기
//         if (same == different) { ++answer; same = different = 0; }  // 같은 문자와 다른 문자 수가 같아지면 한 조각을 완성하고 두 개수 초기화
//     }  // 이 범위 끝
//     return answer + (same != 0 || different != 0);  // 완성한 조각 수 / 조각 첫 문자와 같은 글자 수 / 조각 첫 문자와 다른 글자 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 첫 문자와 같은 문자 수와 다른 문자 수를 세기; 두 개수가 같아지는 즉시 분리하고 마지막 남은 부분도 한 묶음으로 세기
