#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int n) {
    int* answer = malloc(n * sizeof(*answer));
    int pos = 0;
    for (int d = 1; d <= n; ++d) if (n % d == 0) answer[pos++] = d;
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
// int* solution(int n) {  // 약수 구하기 풀이 시작
//     int* answer = malloc(n * sizeof(*answer));  // 약수의 개수는 n을 넘지 않으므로 정수 n개를 담을 결과 공간을 malloc으로 확보
//     int pos = 0;  // int 변수 pos는 찾은 약수의 개수이자 다음 약수를 기록할 위치이며, 0에서 시작
//     for (int d = 1; d <= n; ++d) if (n % d == 0) answer[pos++] = d;  // for로 후보 d를 1부터 n까지 오름차순으로 검사. n % d가 0일 때만 d를 결과에 넣고 pos를 증가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 1부터 n까지 오름차순으로 검사하여 n을 나누어떨어지게 하는 값만 저장. 작은 후보부터 확인하므로 결과도 오름차순임
