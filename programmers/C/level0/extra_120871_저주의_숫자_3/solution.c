#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    int value = 0;
    for (int i = 0; i < n; ++i) {
        bool forbidden;
        do {
            ++value;
            forbidden = value % 3 == 0;
            for (int v = value; v; v /= 10) if (v % 10 == 3) forbidden = true;
        } while (forbidden);
    }
    return value;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) {  // 저주의 숫자 3 풀이 시작
//     int value = 0;  // int 변수 value를 0에서 시작하여 다음에 검사할 자연수 후보를 관리
//     for (int i = 0; i < n; ++i) {  // 바깥 for를 n번 반복하며, 각 반복에서 조건을 통과한 수 하나를 찾기
//         bool forbidden;  // bool 변수 forbidden은 현재 후보가 3의 배수이거나 숫자 3을 포함하여 제외 대상인지 표시
//         do {  // do 블록으로 다음 자연수 후보를 최소 한 번 검사하고, 끝의 while 조건으로 제외 대상이면 다시 시도
//             ++value;  // 전위 증가 ++value로 이전 후보보다 1 큰 자연수를 검사
//             forbidden = value % 3 == 0;  // value % 3이 0인지 검사하여 3의 배수이면 forbidden을 true로, 아니면 false로 초기화
//             for (int v = value; v; v /= 10) if (v % 10 == 3) forbidden = true;  // 후보의 사본 v를 10으로 나누며 각 자리를 확인. v % 10이 3인 자리가 하나라도 있으면 forbidden을 true로 표시
//         } while (forbidden);  // forbidden이 true인 동안 do 블록을 반복하고, false가 되면 유효한 수 하나를 찾은 것으로 처리
//     }  // 블록 끝
//     return value;  // return으로 n번째로 조건을 통과한 자연수 value를 반환
// }  // 블록 끝
// 풀이 요약
// 자연수를 1씩 늘리며 3의 배수이거나 숫자 3을 포함한 후보를 제외. 조건을 통과한 수를 n개 찾았을 때의 값 반환.
