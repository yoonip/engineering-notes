#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int n) {
    int* answer = malloc(32 * sizeof(*answer));
    int pos = 0;
    for (int d = 2; d <= n / d; ++d)
        if (n % d == 0) {
            answer[pos++] = d;
            while (n % d == 0) n /= d;
        }
    if (n > 1) answer[pos++] = n;
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
// int* solution(int n) {  // 소인수분해 풀이 시작
//     int* answer = malloc(32 * sizeof(*answer));  // answer를 저장할 메모리 확보
//     int pos = 0;  // 결과에 저장한 서로 다른 소인수 개수를 0으로 시작
//     for (int d = 2; d <= n / d; ++d)  // 2부터 남은 수의 제곱근 이하까지 소인수 후보 검사
//         if (n % d == 0) {  // d가 약수이면 서로 다른 소인수로 한 번만 기록
//             answer[pos++] = d;  // 새 소인수 d를 한 번 저장하고 결과 원소 수 증가
//             while (n % d == 0) n /= d;  // 같은 소인수 d로 나누어지는 동안 모두 제거해 중복 기록 방지
//         }  // 블록 끝
//     if (n > 1) answer[pos++] = n;  // 작은 인수를 다 나눈 뒤 남은 1보다 큰 값도 소인수
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 작은 인수부터 나누되 같은 인수는 모두 제거한 후 한 번만 기록
