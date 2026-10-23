#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int price) {
    int percent = price >= 500000 ? 80 : price >= 300000 ? 90 : price >= 100000 ? 95 : 100;
    return price * percent / 100;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int price) {  // 옷가게 할인 받기 풀이 시작
//     int percent = price >= 500000 ? 80 : price >= 300000 ? 90 : price >= 100000 ? 95 : 100;  // 가격 구간별로 실제 결제 비율 선택: 80%, 90%, 95%, 100%
//     return price * percent / 100;  // 가격에 결제 비율을 곱하고 정수 나눗셈으로 소수 부분을 버려 반환
// }  // 블록 끝
// 풀이 요약
// 가격이 큰 할인 구간부터 검사해 결제 비율 선택. 정수 곱셈과 나눗셈으로 할인 가격의 소수 부분 버림.
