#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char** solution(const char* my_string) {
    size_t count = 0;
    for (size_t i = 0; my_string[i]; ) {
        while (my_string[i] == ' ') ++i;
        if (!my_string[i]) break;
        ++count;
        while (my_string[i] && my_string[i] != ' ') ++i;
    }
    char** answer = malloc(count * sizeof(char*));
    size_t out = 0;
    for (size_t i = 0; my_string[i]; ) {
        while (my_string[i] == ' ') ++i;
        if (!my_string[i]) break;
        size_t start = i;
        while (my_string[i] && my_string[i] != ' ') ++i;
        size_t n = i - start;
        answer[out] = malloc(n + 1);
        memcpy(answer[out], my_string + start, n);
        answer[out++][n] = '\0';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char** solution(const char* my_string) {  // 공백으로 구분하기 2 풀이 시작
//     size_t count = 0;  // 공백으로 나뉘는 빈칸 아닌 단어 수를 0으로 시작
//     for (size_t i = 0; my_string[i]; ) {  // 문자열 끝까지 각 단어의 시작과 끝을 찾아 이동
//         while (my_string[i] == ' ') ++i;  // 단어 앞의 공백을 모두 건너뜀
//         if (!my_string[i]) break;  // 공백을 건너뛴 뒤 문자열 끝이면 더 읽을 단어가 없어 종료
//         ++count;  // 새로 찾은 단어 하나를 전체 단어 수에 추가
//         while (my_string[i] && my_string[i] != ' ') ++i;  // 공백이나 문자열 끝을 만날 때까지 현재 단어의 끝 탐색
//     }  // 블록 끝
//     char** answer = malloc(count * sizeof(char*));  // answer를 저장할 메모리 확보
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; my_string[i]; ) {  // 문자열 끝까지 각 단어의 시작과 끝을 찾아 이동
//         while (my_string[i] == ' ') ++i;  // 단어 앞의 공백을 모두 건너뜀
//         if (!my_string[i]) break;  // 공백을 건너뛴 뒤 문자열 끝이면 더 읽을 단어가 없어 종료
//         size_t start = i;  // 이번 단어가 시작한 위치 기억
//         while (my_string[i] && my_string[i] != ' ') ++i;  // 공백이나 문자열 끝을 만날 때까지 현재 단어의 끝 탐색
//         size_t n = i - start;  // 현재 단어의 시작과 끝 인덱스 차이로 문자 수 계산
//         answer[out] = malloc(n + 1);  // 결과를 저장할 메모리 확보
//         memcpy(answer[out], my_string + start, n);  // 현재 단어의 시작 위치부터 n글자를 새 단어 버퍼에 복사
//         answer[out++][n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 공백을 모두 건너뛰고 다음 공백 전까지를 한 단어로 복사. 연속 공백과 양 끝 공백은 빈 단어로 남기지 않음.
