#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(const char* babbling[], size_t babbling_len) {
    const char* words[4] = {"aya", "ye", "woo", "ma"}; int answer = 0;
    for (size_t b = 0; b < babbling_len; ++b) {
        const char* sound = babbling[b]; size_t i = 0; int previous = -1;
        while (sound[i]) {
            int found = -1;
            for (int w = 0; w < 4; ++w) if (w != previous && strncmp(sound + i, words[w], strlen(words[w])) == 0) { found = w; break; }
            if (found < 0) break;
            i += strlen(words[found]); previous = found;
        }
        if (!sound[i]) ++answer;
    }
    return answer;
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
// int solution(const char* babbling[], size_t babbling_len) {  // 허용된 네 발음을 앞에서부터 읽기; 바로 이전과 같은 발음을 연속해서 쓰지 않고 문자열을 끝까지 읽을 수 있는지 확인
//     const char* words[4] = {"aya", "ye", "woo", "ma"}; int answer = 0;  // 발음 가능한 네 소리 / 끝까지 발음 가능한 단어 수 저장
//     for (size_t b = 0; b < babbling_len; ++b) {  // 검사할 단어 위치 순서대로 확인
//         const char* sound = babbling[b]; size_t i = 0; int previous = -1;  // 현재 단어 / 다음에 읽을 발음 위치 / 바로 전 발음 번호 저장
//         while (sound[i]) {  // 단어 끝까지 다음 발음을 이어서 확인
//             int found = -1;  // 현재 위치와 맞는 발음 번호 저장
//             for (int w = 0; w < 4; ++w) if (w != previous && strncmp(sound + i, words[w], strlen(words[w])) == 0) { found = w; break; }  // 검사 중인 발음 후보 순서대로 확인; 찾는 이름 또는 앞부분 문자열이 같으면 현재 위치와 맞는 발음 번호 갱신
//             if (found < 0) break;  // 현재 위치와 맞는 발음 번호가 0보다 작으면 이번 후보 확인을 끝내기
//             i += strlen(words[found]); previous = found;  // 다음에 읽을 발음 위치 / 발음 가능한 네 소리 / 현재 위치와 맞는 발음 번호 더해 누적
//         }  // 이 범위 끝
//         if (!sound[i]) ++answer;  // 막힘없이 단어 끝까지 읽었으면 발음 가능한 단어로 세기
//     }  // 이 범위 끝
//     return answer;  // 끝까지 발음 가능한 단어 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 허용된 네 발음을 앞에서부터 읽기; 바로 이전과 같은 발음을 연속해서 쓰지 않고 문자열을 끝까지 읽을 수 있는지 확인
