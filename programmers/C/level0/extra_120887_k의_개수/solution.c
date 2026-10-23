#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int i, int j, int k) {
    int count = 0;
    for (int n = i; n <= j; ++n)
        for (int value = n; value; value /= 10) count += value % 10 == k;
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
// int solution(int i, int j, int k) {  // k의 개수 풀이 시작
//     int count = 0;  // int 변수 count를 0으로 초기화하여 여러 수와 여러 자리에서 발견한 k의 횟수를 모두 누적
//     for (int n = i; n <= j; ++n)  // 바깥 for로 양의 정수 n을 i부터 j까지 양 끝을 포함하여 순회
//         for (int value = n; value; value /= 10) count += value % 10 == k;  // 안쪽 for에서 n의 사본 value를 10으로 나누며 자리를 하나씩 제거. value % 10이 k와 같은 자리마다 count에 1을 더하므로 한 수의 중복 자리도 각각 세기
//     return count;  // return으로 i부터 j까지에서 센 숫자 k의 총 등장 횟수를 반환
// }  // 블록 끝

// 풀이 요약
// i부터 j까지 각 정수에서 나머지와 정수 나눗셈으로 모든 자리를 읽기. 숫자 k와 같은 자리마다 1을 더하므로 한 수 안의 중복 등장도 모두 세기
