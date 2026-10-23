#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int chicken) {
    int answer = 0;
    while (chicken >= 10) {
        int free_chicken = chicken / 10;
        answer += free_chicken;
        chicken = free_chicken + chicken % 10;
    }
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
// int solution(int chicken) {  // 치킨 쿠폰 풀이 시작
//     int answer = 0;  // 무료로 받은 치킨의 총수를 0으로 시작
//     while (chicken >= 10) {  // 쿠폰이 10장 이상이면 무료 치킨으로 교환
//         int free_chicken = chicken / 10;  // 쿠폰 10장당 받을 무료 치킨 수
//         answer += free_chicken;  // 이번 교환으로 받은 무료 치킨 수를 전체 합에 추가
//         chicken = free_chicken + chicken % 10;  // 무료 치킨에서 생긴 새 쿠폰에 기존 남은 쿠폰 합치기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 쿠폰을 치킨으로 바꾸고 서비스 치킨의 쿠폰까지 다시 교환
