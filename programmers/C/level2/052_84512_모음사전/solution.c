#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(const char* word) {
    const int weights[5] = {781,156,31,6,1};
    const char* vowels = "AEIOU"; int answer = 0;
    for (size_t i = 0; word[i]; ++i) answer += (int)(strchr(vowels, word[i]) - vowels) * weights[i] + 1;
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
// int solution(const char* word) {  // 각 자리에서 앞선 모음으로 시작하는 모든 접미 단어를 건너뛰고, 현재 접두 단어 자체의 순위 1을 더하기
//     const int weights[5] = {781,156,31,6,1};  // 각 자리에서 건너뛸 단어 수 저장
//     const char* vowels = "AEIOU"; int answer = 0;  // 모음의 사전 순서 / 모음 사전의 순번 저장
//     for (size_t i = 0; word[i]; ++i) answer += (int)(strchr(vowels, word[i]) - vowels) * weights[i] + 1;  // 단어의 현재 자리 순서대로 확인; 모음 사전의 순번 / 모음의 사전 순서 / 단어의 현재 자리 더해 누적
//     return answer;  // 모음 사전의 순번 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 자리에서 앞선 모음으로 시작하는 모든 접미 단어를 건너뛰고, 현재 접두 단어 자체의 순위 1을 더하기
// 예: 'I'는 앞의 A·E 그룹 781개씩을 지나 2×781+1=1563; 단어 길이 L에 대해 시간 O(L), 공간 O(1)
