#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int common[], size_t common_len) {
    if (common[1] - common[0] == common[2] - common[1]) return common[common_len - 1] + common[1] - common[0];
    return common[common_len - 1] * (common[1] / common[0]);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int common[], size_t common_len) {  // 다음에 올 숫자 풀이 시작
//     if (common[1] - common[0] == common[2] - common[1]) return common[common_len - 1] + common[1] - common[0];  // 앞의 두 차이가 같으면 등차수열. 마지막 값에 공차를 한 번 더하기
//     return common[common_len - 1] * (common[1] / common[0]);  // 등차수열이 아니면 마지막 항에 첫 두 항의 정수 공비를 곱해 다음 항 반환
// }  // 블록 끝
// 풀이 요약
// 앞 세 항의 차이가 같으면 등차수열이고, 아니면 등비수열임
