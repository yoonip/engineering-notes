#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int numbers[], size_t numbers_len, int n) {
    int sum = 0;
    for (size_t i = 0; i < numbers_len && sum <= n; ++i) sum += numbers[i];
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int numbers[], size_t numbers_len, int n) {  // n보다 커질 때까지 더하기 풀이 시작
//     int sum = 0;  // 누적 합계 저장
//     for (size_t i = 0; i < numbers_len && sum <= n; ++i) sum += numbers[i];  // 누적합이 n 이하인 동안 다음 수를 더해, 처음 n을 초과하면 종료
//     return sum;  // 처음으로 n을 초과하게 된 누적합 반환
// }  // 블록 끝// 풀이 요약
// 앞에서부터 더하며 누적합이 처음 n을 초과하는 순간 종료. n과 같을 때는 다음 원소도 더함.
