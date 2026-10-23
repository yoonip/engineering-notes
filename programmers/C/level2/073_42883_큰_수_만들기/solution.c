#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

char* solution(const char* number, int k) {
    size_t len = strlen(number), top = 0;
    char* answer = malloc(len + 1);
    for (size_t i = 0; i < len; ++i) {
        while (k && top && answer[top - 1] < number[i]) { --top; --k; }
        answer[top++] = number[i];
    }
    top -= k; answer[top] = '\0';
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
// char* solution(const char* number, int k) {  // 뒤에서 더 큰 숫자가 나오면 지울 수 있는 만큼 앞의 작은 숫자를 스택에서 제거; 삭제가 남으면 끝에서 지우기
//     size_t len = strlen(number), top = 0;  // 입력 숫자 길이 / 아직 남긴 숫자 수 저장
//     char* answer = malloc(len + 1);  // 큰 수를 만들기 위한 숫자 스택 공간 확보
//     for (size_t i = 0; i < len; ++i) {  // 다음에 읽을 숫자 위치 순서대로 확인
//         while (k && top && answer[top - 1] < number[i]) { --top; --k; }  // 삭제 기회가 남고 새 숫자가 더 크면 앞의 작은 숫자를 스택에서 제거
//         answer[top++] = number[i];  // 큰 수를 만들기 위한 숫자 스택 갱신
//     }  // 이 범위 끝
//     top -= k; answer[top] = '\0';  // 문자열 끝에 널 문자 붙이기
//     return answer;  // 큰 수를 만들기 위한 숫자 스택 반환
// }  // 이 범위 끝

// 풀이 요약
// 뒤에서 더 큰 숫자가 나오면 지울 수 있는 만큼 앞의 작은 숫자를 스택에서 제거; 삭제가 남으면 끝에서 지우기
// 예: 1924에서 1·2를 지우면 94.; 각 자릿수는 한 번씩 추가·제거되므로 시간·공간 O(N)
