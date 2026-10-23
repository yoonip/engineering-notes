#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* a, const char* b) {
    int i = (int)strlen(a) - 1, j = (int)strlen(b) - 1, carry = 0;
    int capacity = (i > j ? i : j) + 3, length = 0;
    char* answer = malloc(capacity);
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += a[i--] - '0';
        if (j >= 0) sum += b[j--] - '0';
        answer[length++] = '0' + sum % 10;
        carry = sum / 10;
    }
    for (int p = 0; p < length / 2; ++p) {
        char c = answer[p]; answer[p] = answer[length - 1 - p]; answer[length - 1 - p] = c;
    }
    answer[length] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(const char* a, const char* b) {  // 두 수의 합 풀이 시작
//     int i = (int)strlen(a) - 1, j = (int)strlen(b) - 1, carry = 0;  // 두 문자열을 일의 자리부터 읽을 인덱스와 올림수 carry 준비
//     int capacity = (i > j ? i : j) + 3, length = 0;  // 긴 입력 길이에 최종 올림수와 종료 문자 여유를 더하고, 저장한 자릿수 length는 0으로 시작
//     char* answer = malloc(capacity);  // answer를 저장할 메모리 확보
//     while (i >= 0 || j >= 0 || carry) {  // 한쪽에 읽을 자릿수나 마지막 올림수가 남은 동안 덧셈 반복
//         int sum = carry;  // 이번 자리의 합을 앞자리에서 넘어온 올림수로 시작
//         if (i >= 0) sum += a[i--] - '0';  // a에 남은 끝자리 숫자를 더하고 다음 높은 자리로 이동
//         if (j >= 0) sum += b[j--] - '0';  // b에 남은 끝자리 숫자를 더하고 다음 높은 자리로 이동
//         answer[length++] = '0' + sum % 10;  // 나머지 연산자 %로 일의 자리를 구해 문자로 저장하고 length를 한 칸 늘림
//         carry = sum / 10;  // 정수 나눗셈 / 10으로 다음 자릿수의 올림을 계산
//     }  // 블록 끝
//     for (int p = 0; p < length / 2; ++p) {  // 낮은 자리부터 쓴 결과를 정상 순서로 뒤집기 위해 앞 절반 순회
//         char c = answer[p]; answer[p] = answer[length - 1 - p]; answer[length - 1 - p] = c;  // 앞 문자와 뒤의 대칭 문자를 임시 변수로 교환
//     }  // 블록 끝
//     answer[length] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 일의 자리부터 두 숫자와 올림을 더하기. 각 자릿수를 한 번씩 처리하므로 시간 O(두 문자열의 최대 길이)임
