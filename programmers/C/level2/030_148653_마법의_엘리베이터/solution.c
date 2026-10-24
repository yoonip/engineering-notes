#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int storey) {
    int answer = 0;
    while (storey) {
        int digit = storey % 10; storey /= 10;
        if (digit > 5 || (digit == 5 && storey % 10 >= 5)) { answer += 10 - digit; ++storey; }
        else answer += digit;
    }
    return answer;
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
// int solution(int storey) {  // 일의 자리부터 0으로 만들기; 5보다 크면 올리고 작으면 내리며, 5면 다음 자리가 5 이상일 때 올리기
//     int answer = 0;  // 층수를 0으로 만드는 마법 돌 수 저장
//     while (storey) {  // 아직 처리하지 않은 높은 자리가 남아 있으면 반복
//         int digit = storey % 10; storey /= 10;  // 현재 층수의 일의 자리 저장
//         if (digit > 5 || (digit == 5 && storey % 10 >= 5)) { answer += 10 - digit; ++storey; }  // 일의 자리가 6 이상이거나 5인데 다음 자리도 5 이상이면 올림 쪽 선택
//         else answer += digit;  // 앞 조건이 아니면 층수를 0으로 만드는 마법 돌 수 / 현재 층수의 일의 자리 더해 누적
//     }  // 이 범위 끝
//     return answer;  // 층수를 0으로 만드는 마법 돌 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 일의 자리부터 0으로 만들기; 5보다 크면 올리고 작으면 내리며, 5면 다음 자리가 5 이상일 때 올리기
// 예: 16은 +1 네 번, -10 두 번으로 6개; 시간 O(log10(storey)), 공간 O(1)
