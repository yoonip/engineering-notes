#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len) {
    int counts[1000] = {0}, answer = -1, best = 0;
    for (size_t i = 0; i < array_len; ++i) ++counts[array[i]];
    for (int i = 0; i < 1000; ++i) {
        if (counts[i] > best) { best = counts[i]; answer = i; }
        else if (counts[i] == best) answer = -1;
    }
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
// int solution(int array[], size_t array_len) {  // 최빈값 구하기 풀이 시작
//     int counts[1000] = {0}, answer = -1, best = 0;  // 값별 빈도 배열, 최빈값 후보 answer, 최대 빈도 best 준비
//     for (size_t i = 0; i < array_len; ++i) ++counts[array[i]];  // 숫자마다 나온 횟수를 counts에 누적
//     for (int i = 0; i < 1000; ++i) {  // 가능한 값 0부터 999까지의 빈도 비교
//         if (counts[i] > best) { best = counts[i]; answer = i; }  // 더 많이 나온 숫자를 찾으면 최빈값 후보 교체
//         else if (counts[i] == best) answer = -1;  // 같은 최대 빈도를 가진 다른 값이 있으면 최빈값이 여러 개라는 -1 표시
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 등장 횟수를 센 뒤 가장 높은 빈도를 가진 값이 유일한지 확인
