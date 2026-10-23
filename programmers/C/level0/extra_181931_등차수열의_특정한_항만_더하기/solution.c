#include <stdbool.h>
#include <stddef.h>

int solution(int a, int d, bool included[], size_t included_len) {
    int answer = 0;
    for (size_t i = 0; i < included_len; ++i) if (included[i]) answer += a + (int)i * d;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int solution(int a, int d, bool included[], size_t included_len) {  // 등차수열의 특정한 항만 더하기 풀이 시작
//     int answer = 0;  // 정수형 결과 누적값을 0으로 초기화
//     for (size_t i = 0; i < included_len; ++i) if (included[i]) answer += a + (int)i * d;  // for와 if로 포함할 항만 골라 a+i*d를 계산한 뒤 +=로 합계에 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 포함 여부가 참인 인덱스에서 첫 항과 공차로 해당 항을 구해 더하기
