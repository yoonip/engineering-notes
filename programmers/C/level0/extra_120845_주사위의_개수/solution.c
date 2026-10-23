#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int box[], size_t box_len, int n) {
    (void)box_len;
    return (box[0] / n) * (box[1] / n) * (box[2] / n);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int box[], size_t box_len, int n) {  // 주사위의 개수 풀이 시작
//     (void)box_len;  // 배열 크기처럼 함수 형식에 포함되지만 본문에서 사용하지 않는 매개변수임을 표시
//     return (box[0] / n) * (box[1] / n) * (box[2] / n);  // 가로·세로·높이 각각에 들어가는 주사위 수의 몫을 구해 곱함
// }  // 블록 끝
// 풀이 요약
// 각 방향에 몇 개씩 들어가는지 따로 구해 곱하기. 전체 부피만 나누면 남는 틈을 잘못 계산할 수 있음
