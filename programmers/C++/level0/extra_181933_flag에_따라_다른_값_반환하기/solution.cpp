#include <stdbool.h>

int solution(int a, int b, bool flag) {
    return flag ? a + b : a - b;
}

// 전체 코드 줄별 설명
// #include <stdbool.h>  // C에서 bool·true·false 사용
//
// int solution(int a, int b, bool flag) {  // flag에 따라 다른 값 반환하기 풀이 시작
//     return flag ? a + b : a - b;  // 삼항 연산자 ?:로 flag에 따라 합 또는 차를 반환
// }  // 블록 끝

// 풀이 요약
// flag가 참이면 두 정수를 더하고, 거짓이면 빼기
