#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* letter) {
    const char* morse[] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};
    char* answer = malloc(strlen(letter) + 1);
    size_t pos = 0;
    const char* p = letter;
    while (*p) {
        while (*p == ' ') ++p;
        if (!*p) break;
        const char* start = p;
        while (*p && *p != ' ') ++p;
        size_t len = (size_t)(p - start);
        for (int i = 0; i < 26; ++i)
            if (strlen(morse[i]) == len && strncmp(start, morse[i], len) == 0) {
                answer[pos++] = 'a' + i; break;
            }
    }
    answer[pos] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// char* solution(const char* letter) {  // 모스부호 (1) 풀이 시작
//     const char* morse[] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};  // 배열 인덱스 0~25가 a~z에 대응하도록 모스부호 표 저장
//     char* answer = malloc(strlen(letter) + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     size_t pos = 0;  // 다음 문자를 쓸 위치는 0부터 시작
//     const char* p = letter;  // 다음에 읽을 모스부호의 위치를 가리키는 포인터 준비
//     while (*p) {  // 문자열 끝까지 모스부호를 하나씩 해독
//         while (*p == ' ') ++p;  // 모스부호 사이의 공백을 건너뜀
//         if (!*p) break;  // 공백 뒤에 문자열 끝이 오면 해독 종료
//         const char* start = p;  // 현재 모스부호의 시작 위치 기억
//         while (*p && *p != ' ') ++p;  // 다음 공백이나 끝까지 이동해 현재 부호의 끝 탐색
//         size_t len = (size_t)(p - start);  // 현재 모스 부호의 시작·끝 포인터 차이가 길이
//         for (int i = 0; i < 26; ++i)  // 알파벳 순서로 저장한 26개 모스부호와 현재 부호 비교
//             if (strlen(morse[i]) == len && strncmp(start, morse[i], len) == 0) {  // 길이가 같고 모든 부호 문자가 일치하는 표 항목 선택
//                 answer[pos++] = 'a' + i; break;  // 해당 알파벳을 결과에 추가하고 다음 모스부호로 넘어감
//             }  // 블록 끝
//     }  // 블록 끝
//     answer[pos] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 공백으로 구분된 모스부호를 a부터 z 순서의 표와 비교. 길이와 부호가 같은 항목의 인덱스를 알파벳으로 변환.
