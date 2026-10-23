#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

bool solution(const char* s) {
    size_t n = strlen(s); if (n != 4 && n != 6) return false;
    for (size_t i = 0; i < n; ++i) if (!isdigit((unsigned char)s[i])) return false;
    return true;
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
// bool solution(const char* s) {  // 길이가 4 또는 6인지 확인하고 모든 문자가 십진 숫자인지 확인
//     size_t n = strlen(s); if (n != 4 && n != 6) return false;  // 길이가 4나 6이 아니면 바로 false
//     for (size_t i = 0; i < n; ++i) if (!isdigit((unsigned char)s[i])) return false;  // 숫자가 아닌 문자가 하나라도 있으면 false
//     return true;  // 끝까지 조건을 지켰으니 성공
// }  // 이 범위 끝

// 풀이 요약
// 길이가 4 또는 6인지 확인하고 모든 문자가 십진 숫자인지 확인
