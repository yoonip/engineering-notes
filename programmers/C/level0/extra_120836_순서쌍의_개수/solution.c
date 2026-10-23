#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    int count = 0;
    for (int i = 1; i <= n / i; ++i)
        if (n % i == 0) count += i == n / i ? 1 : 2;
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
// int solution(int n) {  // 순서쌍의 개수 풀이 시작
//     int count = 0;  // 곱이 n인 순서쌍 개수를 0으로 시작
//     for (int i = 1; i <= n / i; ++i)  // 1부터 n의 제곱근 이하까지 약수 후보 검사
//         if (n % i == 0) count += i == n / i ? 1 : 2;  // 약수 i와 n / i가 다르면 순서를 바꾼 두 쌍, 같으면 한 쌍만 추가
//     return count;  // 모든 약수 쌍으로 센 순서쌍 수 반환
// }  // 블록 끝
// 풀이 요약
// 약수 하나가 정해지면 다른 수는 n을 그 약수로 나눈 값임. 같은 두 수인 경우만 한 번 세기
