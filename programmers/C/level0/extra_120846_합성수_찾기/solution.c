#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    int count = 0;
    for (int value = 4; value <= n; ++value)
        for (int d = 2; d <= value / d; ++d)
            if (value % d == 0) { ++count; break; }
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) {  // 합성수 찾기 풀이 시작
//     int count = 0;  // 합성수 개수를 0으로 시작
//     for (int value = 4; value <= n; ++value)  // 가장 작은 합성수 4부터 n까지 검사
//         for (int d = 2; d <= value / d; ++d)  // 2부터 현재 수의 제곱근 이하까지 1과 자신 외의 약수 탐색
//             if (value % d == 0) { ++count; break; }  // 약수를 하나라도 찾으면 합성수로 한 번 세고 약수 탐색 중단
//     return count;  // n 이하의 합성수 개수 반환
// }  // 블록 끝
// 풀이 요약
// 가장 작은 합성수 4부터 n까지 각 수의 제곱근 이하 약수를 탐색. 1과 자기 자신 외의 약수가 하나라도 있으면 합성수로 한 번 셈.
