#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

bool solution(const char* s) {
    int balance = 0;
    for (size_t i = 0; s[i]; ++i) {
        balance += s[i] == '(' ? 1 : -1;
        if (balance < 0) return false;
    }
    return balance == 0;
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
// bool solution(const char* s) {  // 모든 앞부분에서 여는 괄호 수≥닫는 괄호 수이고, 전체 개수가 같으면 올바른 괄호다
//     int balance = 0;  // 열린 괄호에서 닫힌 괄호를 뺀 수 저장
//     for (size_t i = 0; s[i]; ++i) {  // 확인할 괄호 위치 순서대로 확인
//         balance += s[i] == '(' ? 1 : -1;  // 열린 괄호에서 닫힌 괄호를 뺀 수 / 확인할 괄호 위치 더해 누적
//         if (balance < 0) return false;  // 열린 괄호에서 닫힌 괄호를 뺀 수가 0보다 작으면 조건을 못 지켰으니 실패
//     }  // 이 범위 끝
//     return balance == 0;  // 열린 괄호에서 닫힌 괄호를 뺀 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 모든 앞부분에서 여는 괄호 수≥닫는 괄호 수이고, 전체 개수가 같으면 올바른 괄호다
// 예: )()(는 첫 글자에서 바로 실패하고, (()(는 끝에 balance=2가 남아 실패하기; 시간 O(N), 공간 O(1)
